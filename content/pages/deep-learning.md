---
title: "Deep Learning — Architecture, Initialization, and Training Dynamics"
slug: "deep-learning"
section: "deep-learning"
nav_order: 1
nav_label: "Deep Learning"
tags: ["neural-networks", "transformers", "initialization", "normalization", "optimization", "backprop", "interview-prep"]
updated: "2026-10-01"
---

## TL;DR

Deep learning interviews test whether you understand *training dynamics*, not
whether you can name architectures. Five questions carry the page: **why
LayerNorm works** (per-example statistics, stable across batch sizes, clean
gradient paths); **why residuals help** (identity path gives gradients a
highway and turns depth into iterative refinement); **why init matters**
(preserve activation/gradient variance across layers or the signal dies at
layer 1); **why gradients vanish/explode** (repeated Jacobian multiplication);
**why AdamW over Adam** (decoupled weight decay — see [ML
Fundamentals](#/ml-fundamentals)). Plus the mechanic's view: what
`backward()` actually does and which tensors it must keep alive.

:::tldr
**Init:** He for ReLU, Xavier for tanh/sigmoid — keep variance ≈ 1 per
layer. **Residuals:** $x + F(x)$ makes depth safe; gradients flow through the
identity. **Norm:** Pre-LN + residuals is the stable transformer recipe.
**Optim:** AdamW + warmup + cosine decay + grad clipping. **Instability
checklist:** LR too high → clip/warmup; Post-LN at depth → Pre-LN; bad init
→ He/Xavier; fp16 overflow → loss scaling / bigger epsilon.
:::

---

## MLP: forward and backward, end to end

:::tldr
An MLP is affine transforms interleaved with nonlinearities. The forward pass
caches what backward needs; the backward pass is one reverse sweep of
Jacobian-vector products. If you can write both directions for a 2-layer net
in numpy, you understand backprop — everything else is bookkeeping.
:::

**30-second answer:** Layer $l$: $z^{(l)} = W^{(l)}a^{(l-1)} + b^{(l)}$,
$a^{(l)} = \phi(z^{(l)})$. Forward computes and caches $(z^{(l)}, a^{(l)})$.
Backward: $\delta^{(L)} = \nabla_{a^{(L)}}L \odot \phi'(z^{(L)})$,
$\delta^{(l)} = (W^{(l+1)T}\delta^{(l+1)}) \odot \phi'(z^{(l)})$,
$\nabla_{W^{(l)}}L = \delta^{(l)} a^{(l-1)T}$.

**Interview-depth:** Two facts interviewers love. **(1)** The backward pass
costs ~2× a forward pass (one matmul for $\nabla_W$, one for $\nabla_x$ per
layer) — so a training step is ~3× inference FLOPs. **(2)** What must be
cached: for a linear layer, the *input* $a^{(l-1)}$ (since $\nabla_W$ is an
outer product with it); for ReLU, just the *sign mask* (1 bit per element);
for LayerNorm, the normalized output, mean, and inverse std. Memory during
training is dominated by these saved activations — parameters are the small
part. This is the entire motivation for activation checkpointing and the
reason "can it fit" questions are about batch × sequence × hidden, not
parameter count.

**Intuition:** Think of forward as water flowing through pipes (values) and
backward as pressure flowing back (gradients). Each valve (op) needs to
remember its setting (cached tensors) to know how much pressure to pass
upstream and how much its own parameters should turn.

**Math:**
$$\delta^{(l)}_j = \phi'(z^{(l)}_j)\sum_k W^{(l+1)}_{kj}\,\delta^{(l+1)}_k,
\qquad
\frac{\partial L}{\partial W^{(l)}_{ji}} = \delta^{(l)}_j a^{(l-1)}_i$$

**Code (2-layer MLP, full forward + backward, numpy):**
```python
import numpy as np

def forward(X, W1, b1, W2, b2):
    Z1 = X @ W1 + b1            # cache X, Z1
    A1 = np.maximum(Z1, 0)      # ReLU; cache mask Z1 > 0
    Z2 = A1 @ W2 + b2           # cache A1
    return Z2, (X, Z1, A1)

def backward(dZ2, cache, W1, W2):
    X, Z1, A1 = cache
    n = X.shape[0]
    dW2 = A1.T @ dZ2 / n; db2 = dZ2.mean(axis=0)
    dA1 = dZ2 @ W2.T
    dZ1 = dA1 * (Z1 > 0)        # ReLU mask
    dW1 = X.T @ dZ1 / n; db1 = dZ1.mean(axis=0)
    return dW1, db1, dW2, db2
# dZ2 for softmax+CE is (softmax(Z2) - Y_onehot) / n  -- see ML Fundamentals
```

**Follow-ups:**
- "What's the FLOP ratio of train to inference?" → ~3:1 (forward + 2× for
  backward). Optimizer states (Adam: 2× params in fp32) dominate *memory*
  alongside activations.
- "Why cache the mask for ReLU instead of Z1?" → 1 bit vs 32 bits per
  element; the derivative only needs the sign.
- "What breaks if you forget to cache?" → you recompute (checkpointing) or
  you're wrong — there's no third option.

**Mistakes:**
- Dividing by $n$ inconsistently between loss and gradients — pick mean
  reduction everywhere and keep it.
- Applying the ReLU mask from the wrong layer's $Z$ — off-by-one-layer bugs
  that still "train" but to a worse optimum.
- In-place ReLU on a tensor autograd saved — corrupts the backward graph
  (PyTorch will error; numpy silently gives wrong answers).

---

## Embeddings

:::tldr
An embedding layer is a lookup table: integer token → dense vector. It's a
linear layer with a one-hot input, which means its backward pass is sparse —
only rows for tokens in the batch get gradients. That sparsity is why
embeddings have their own optimization quirks.
:::

**30-second answer:** $E \in \mathbb{R}^{V \times d}$; token $i$ maps to row
$E_i$. Forward is a gather; backward is a scatter-add of gradients into the
touched rows. Untouched rows get zero gradient — no update, no decay (unless
your optimizer decays them anyway — AdamW's decoupled decay *does* touch all
rows, which is a subtle regularization difference vs. sparse Adam).

**Interview-depth:** **(1)** Because updates are sparse and frequencies are
Zipf-distributed, rare tokens get few, noisy updates — adaptive optimizers
(Adam) help enormously here vs. SGD, since per-coordinate scaling compensates
for update-count disparity. **(2)** Tying input and output embeddings (weight
tying, $W_{out} = E^T$) halves parameters in the embedding-heavy regime and
usually helps — standard in small LMs. **(3)** Positional information isn't in
the lookup: sinusoidal, learned absolute, or rotary (RoPE) encodings add
order; RoPE bakes relative position into attention via rotation, which is why
it extrapolates better to longer contexts.

**Follow-ups:**
- "Why does Adam beat SGD for embeddings?" → sparse, imbalanced update
  counts; per-coordinate second moments normalize the effective step per
  token by its update history.
- "Embedding dim vs. vocab size — how do you choose?" → dim scales with the
  information per token and data size; rule of thumb $d \propto V^{1/4}$
  (e.g., $V=50k \Rightarrow d \approx 512$–$1024$); ablate on the downstream
  metric, not intuition.
- "What goes wrong with huge embedding tables?" → memory (table is often the
  largest single tensor), slow sparse updates, and stale rows for rare tokens.

**Mistakes:**
- Applying dropout *to* embedding rows as if they were activations — standard
  dropout is on the looked-up vectors, not the table.
- Forgetting padding-index masking — the pad row accumulates garbage
  gradients.
- fp16 embedding tables with large vocab — underflow in rarely-updated rows;
  keep embeddings in fp32 (standard mixed-precision practice).

---

## Activations

:::tldr
ReLU won because its derivative is 0 or 1 — no saturation on the positive
side, cheap, and sparsity falls out for free. Sigmoid/tanh saturate (max
derivatives 0.25/1.0, vanishing in deep stacks). GELU/SiLU are the smooth
modern defaults for transformers — ReLU with a probabilistic taper that
trains slightly better.
:::

**30-second answer:** Sigmoid $\sigma(x) = 1/(1+e^{-x})$, derivative
$\sigma(1-\sigma) \le 0.25$ — saturates both sides, output not zero-centered.
Tanh: zero-centered, derivative $\le 1$, still saturates. ReLU: $\max(0,x)$,
derivative 0/1 — no positive-side saturation, dead neurons on the negative
side. GELU: $x\Phi(x)$ — smooth, weights inputs by "probability of being
kept"; SiLU/Swish: $x\sigma(x)$, same family, used in LLaMA FFNs.

**Interview-depth:** The activation's derivative bound *is* the
vanishing-gradient story: a 50-layer sigmoid MLP multiplies up to $0.25^{50}$
through the chain — dead on arrival. ReLU's piecewise-linear 0/1 derivative
removes the <1 contraction on active paths, which is half of why deep nets
became trainable (init + residuals + norm are the other half). **Dying ReLU:**
neurons stuck with all-negative pre-activations get zero gradient forever —
mitigated by lower LRs, better init, or LeakyReLU/GELU. **Why GELU over ReLU
in transformers:** smoothness (nonzero gradients everywhere help
optimization) and slight empirical gains; the cost is negligible next to
attention. SwiGLU (gated SiLU variant) is the current FFN default in LLaMA —
a *gated* linear unit, which adds multiplicative interaction capacity.

**Math:**
$$\text{ReLU}'(x) = \mathbf{1}_{x>0}, \quad \sigma'(x) = \sigma(x)(1-\sigma(x)),
\quad \text{GELU}(x) = x\Phi(x) \approx 0.5x\big(1+\tanh(\sqrt{2/\pi}(x+0.0447x^3))\big)$$

**Follow-ups:**
- "Why is zero-centered output good?" → non-zero-centered activations (all
  positive, like sigmoid/ReLU outputs) make gradients w.r.t. weights all
  share a sign per neuron, forcing zigzag optimization. Tanh and normalized
  activations avoid this.
- "ReLU vs GELU — when does it matter?" → at transformer scale, GELU/SiLU
  consistently buy a small but real gain; below that, ReLU is fine and
  cheaper. It's a 1%-level decision, not an architecture decision.
- "What are gated linear units?" → $\text{GLU}(x) = (xW_1) \odot
  \sigma(xW_2)$ — the gate multiplicatively modulates the projection;
  SwiGLU swaps in SiLU. More expressive FFN at ~1.5× params for the same
  hidden size.

**Mistakes:**
- Sigmoid/tanh in a deep hidden stack "because it's smooth" — smoothness
  doesn't help if the gradient is $10^{-30}$.
- Softmax as a *hidden* activation — it's a normalizer, not a nonlinearity;
  it couples all units and destroys per-unit gradient independence.
- Forgetting activations are elementwise — no, attention's softmax doesn't
  count as "the activation function."

---

## Initialization — Xavier and He, and why it matters

:::tldr
Init matters because deep nets multiply: if each layer scales variance by
$c$, after $L$ layers the signal is $c^L$ — exponentially exploded or
vanished before training even starts. Xavier ($1/\text{fan}_{in}$) preserves
variance through tanh/sigmoid; He ($2/\text{fan}_{in}$) corrects for ReLU
killing half the activations. Get this wrong and layer 1 is dead on arrival.
:::

**30-second answer:** For $y = Wx$ with independent zero-mean $W, x$:
$\text{Var}(y) = \text{fan}_{in}\,\text{Var}(W)\,\text{Var}(x)$. Setting
$\text{Var}(W) = 1/\text{fan}_{in}$ (Xavier) keeps $\text{Var}(y) =
\text{Var}(x)$. ReLU zeroes half the outputs, halving variance — so He uses
$2/\text{fan}_{in}$ to compensate. Sample uniform on
$[-\sqrt{6/\text{fan}}, \sqrt{6/\text{fan}}]$ or normal with that variance.

**Interview-depth — the derivation interviewers want:** Assume $x_i$ i.i.d.
with variance $v$, $w_{ij}$ i.i.d. zero-mean with variance $\sigma_w^2$,
independent of $x$. Then $\text{Var}(y_j) = \sum_i \text{Var}(w_{ij}x_i) =
\text{fan}_{in}\,\sigma_w^2\,v$ (using $\text{Var}(wx) = \text{Var}(w)
\text{Var}(x)$ for independent zero-mean). For variance preservation,
$\sigma_w^2 = 1/\text{fan}_{in}$. The *backward* pass gives the symmetric
condition $\sigma_w^2 = 1/\text{fan}_{out}$; Xavier averages them
($2/(\text{fan}_{in}+\text{fan}_{out})$). For ReLU: $\text{Var}(\text{ReLU}(y))
\approx \tfrac{1}{2}\text{Var}(y)$ (half the mass at zero, mean shifts —
the $\tfrac12$ is approximate but works), so $\sigma_w^2 = 2/\text{fan}_{in}$.

**Why it matters — the failure modes:** init too small → activations shrink
layer by layer → gradients vanish → early layers never move (looks like
"training plateaued at init loss"). Init too large → activations explode →
saturation/NaN in the first steps (looks like "loss went to NaN at step 3").
Both are *indistinguishable from broken code* at first glance — checking
activation/gradient norms per layer at init is the standard smoke test
("are my per-layer stds ≈ 1?").

**Transformers specifically:** residual branches get *scaled* init (e.g.,
GPT-2 scales residual-projection weights by $1/\sqrt{2N}$ for $N$ layers) so
the $N$ residual additions don't inflate variance by $N$. Embedding tables
use small normal init ($\sigma \approx 0.02$); the final LayerNorm before the
output head keeps logits bounded. If asked "how do you init a transformer,"
the answer is: small normal almost everywhere, He/Xavier for the FFNs,
scaled-down init on residual output projections.

**Code:**
```python
def he_init(fan_in, fan_out):
    return np.random.randn(fan_in, fan_out) * np.sqrt(2.0 / fan_in)
def xavier_init(fan_in, fan_out):
    limit = np.sqrt(6.0 / (fan_in + fan_out))
    return np.random.uniform(-limit, limit, size=(fan_in, fan_out))
```

**Follow-ups:**
- "Why not just init everything to zero?" → symmetry: all neurons in a layer
  compute the same function and get identical gradients — the network never
  breaks symmetry. (Biases *can* be zero; weights cannot.)
- "Why not init large and let training shrink it?" → large init saturates
  activations immediately; saturated units have ~zero gradient, so training
  can't shrink anything. You're stuck at step 0.
- "Does init matter with Adam?" → yes — Adam normalizes *gradient* scale,
  not activation scale. Dead/saturated activations give no gradient signal
  for Adam to normalize; garbage in, garbage out.
- "What about the $1/\sqrt{2N}$ residual scaling — derive the intuition?" →
  $N$ residual adds of variance-$v$ branches give total variance $\approx
  Nv$; scaling each branch's output weights by $1/\sqrt{N}$ (× $1/\sqrt{2}$
  for the two sublayers) keeps the sum at $v$.

**Mistakes:**
- Xavier with ReLU (under by 2× — slow but usually survivable) or He with
  tanh (over by 2× — saturation risk).
- Forgetting `fan_in` vs `fan_out` orientation for your weight layout
  ($W \in \mathbb{R}^{d_{in} \times d_{out}}$ vs transposed).
- Zero-init on weights "to be safe" — symmetry trap above.
- Same init scale for the residual output projection as the rest — the
  $N$-layer variance accumulation needs the $1/\sqrt{2N}$ correction.

---

## Residual connections — why they help

:::tldr
$y = x + F(x)$: the identity path lets gradients flow backward unimpeded
($\partial y/\partial x = I + \partial F/\partial x$ — the $I$ never
vanishes), and turns depth from "learn the whole mapping" into "learn the
refinement." That's why 1000-layer nets train and plain 50-layer nets don't.
:::

**30-second answer:** Without residuals, the gradient to early layers is a
product of $L$ Jacobians — exponential vanish/explode. With residuals, each
layer's Jacobian is $I + J_F$; the identity term guarantees a direct,
unattenuated path from loss to every layer. Optimization-wise, learning a
residual correction is easier than learning a full transform (identity is the
default, not something to be discovered).

**Interview-depth:** Two complementary views. **Gradient view:** unrolling
$y_L = x_0 + \sum_l F_l(x_l)$ shows every layer contributes *additively* —
the network is an ensemble of $2^L$ paths of varying depth (Veit et al.),
and crucially the length-1 paths (single residual hops) carry gradient
directly. Deleting individual residual layers at test time barely hurts —
evidence the net doesn't rely on any single deep path. **Representation
view:** layers iteratively refine rather than transform; early layers needn't
preserve everything because the skip carries the raw signal forward.
**Pre-LN synergy:** with Pre-LN ($x + \text{Sublayer}(\text{LN}(x))$), the
main path is *pure identity* — no normalization sits on the gradient highway.
Post-LN puts LN on the highway (LN's Jacobian rescales gradients), which is
why Post-LN needs warmup and careful LR while Pre-LN trains stably at depth.

**Math:**
$$\frac{\partial L}{\partial x} = \frac{\partial L}{\partial y}
\left(I + \frac{\partial F}{\partial x}\right)$$
Even if $\|\partial F/\partial x\| \to 0$, the gradient $\partial L/\partial y$
passes through unchanged via $I$.

**Follow-ups:**
- "Why not concatenate instead of add?" → dimension growth ($d \to 2d \to
  4d$…) and no identity gradient path; DenseNet does it but pays the param
  cost. Addition keeps width constant and the Jacobian identity-centered.
- "Do residuals help representational capacity or just optimization?" →
  primarily optimization — a plain net can *represent* anything a residual
  net can, it just can't be *trained* to. (Depth helps capacity; residuals
  unlock the depth.)
- "Highway networks vs residuals?" → highways learn the mixing gate
  $y = T \odot F(x) + (1-T) \odot x$; residuals fix $T = 1$. The learned gate
  turned out unnecessary — fixed identity trains better and simpler.

**Mistakes:**
- Putting dropout *on* the residual highway (drops the identity path —
  defeats the purpose); dropout goes inside $F(x)$.
- Dimension-mismatched skips handled by zero-padding instead of a learned
  projection — fine occasionally, but the projection is standard.
- Assuming residuals fix bad init — they fix the *gradient path*, not
  activation scale; you still need sane init (hence the $1/\sqrt{2N}$
  scaling).

---

## Normalization in depth — why LayerNorm works

:::tldr
LayerNorm works because it makes each layer's input distribution
batch-independent and well-conditioned: per-token mean/variance normalization
plus a learned affine keeps activations in the range where nonlinearities and
attention are well-behaved, and its gradient rescaling smooths the loss
landscape. RMSNorm keeps the wins and drops the centering cost.
:::

**30-second answer:** For each token vector $x$: subtract mean, divide by
std, apply learned $\gamma, \beta$. This bounds activation scale regardless
of what previous layers did, keeps attention logits in a sane range (no
saturation of softmax), and makes the optimization landscape smoother
(LN's Jacobian adaptively rescales gradients). Unlike BatchNorm it needs no
batch statistics — works for batch size 1, variable lengths, autoregressive
decoding.

**Interview-depth — the three "why it works" stories:** **(1) Scale control:**
attention computes $\text{softmax}(QK^T/\sqrt{d})$ — if $Q, K$ scales drift,
logits explode and softmax saturates to one-hot (zero gradient) or collapse
to uniform (no discrimination). LN pins the scale every block. **(2)
Landscape smoothing:** like BatchNorm, LN improves the Lipschitz properties
of the loss — gradients are better-behaved, larger LRs work. The
"internal covariate shift" story is the folk version; the defensible version
is conditioning. **(3) Gradient structure:** the LN backward pass re-centers
and rescales the incoming gradient ($\partial \text{LN}/\partial x$ subtracts
the gradient's mean and projects out the radial component) — this acts as an
adaptive per-token gradient normalization, which stabilizes training
independently of the forward-pass story.

**Pre-LN vs Post-LN, precisely:** Post-LN: $x_{l+1} = \text{LN}(x_l +
F(x_l))$ — LN sits on the main path, so at init the expected gradient norm
*grows* with depth (each LN's Jacobian amplifies), requiring warmup and
small LR; but final representations are well-normalized. Pre-LN:
$x_{l+1} = x_l + F(\text{LN}(x_l))$ — main path is pure identity, gradient
norms are depth-independent at init, training is stable with big LRs; the
cost is that the final output scale grows with depth (fixed by a terminal
LN). Modern LLMs: Pre-LN + final LN. If training a deep transformer is
unstable, "switch Post-LN to Pre-LN" is the first thing to try.

**RMSNorm:** drops mean-centering ($\hat x = x / \text{RMS}(x)$) — one less
pass over the vector, invariant to rescaling, and empirically matches
LayerNorm in LLMs (LLaMA, Mistral). The centering was never load-bearing;
the *scaling* is.

**Code (LayerNorm forward + backward, numpy):**
```python
def layernorm_forward(x, gamma, beta, eps=1e-5):
    mu = x.mean(axis=-1, keepdims=True)
    xc = x - mu
    var = (xc**2).mean(axis=-1, keepdims=True)
    invstd = 1.0 / np.sqrt(var + eps)
    xhat = xc * invstd
    return gamma * xhat + beta, (xhat, invstd, gamma)

def layernorm_backward(dy, cache):
    xhat, invstd, gamma = cache
    d = xhat.shape[-1]
    dxhat = dy * gamma
    # gradient through normalize: recenter + remove radial component
    dxc = (dxhat - dxhat.mean(axis=-1, keepdims=True)
           - xhat * (dxhat * xhat).mean(axis=-1, keepdims=True)) * invstd
    dgamma = (dy * xhat).sum(axis=tuple(range(dy.ndim - 1)))
    dbeta = dy.sum(axis=tuple(range(dy.ndim - 1)))
    return dxc, dgamma, dbeta
```

**Follow-ups:**
- "Why not BatchNorm in transformers?" → covered in [ML
  Fundamentals](#/ml-fundamentals): noisy batch stats at small/variable
  batch sizes, train/test mismatch in autoregressive single-example
  decoding, padding contamination. LayerNorm is per-example by construction.
- "Does LayerNorm have a downside?" → it discards scale information (all
  token vectors get unit norm) — the learned $\gamma$ must reintroduce any
  meaningful scale; and its per-token statistics add compute at every block
  (hence RMSNorm, fused kernels).
- "Why does the LN gradient subtract its own mean?" → normalization is
  shift-invariant ($\text{LN}(x + c) = \text{LN}(x)$), so the gradient must
  be orthogonal to the shift direction — the Jacobian projects it out. Same
  for scale invariance → radial projection.

**Mistakes:**
- Normalizing over the batch axis instead of the feature axis (silent shape
  bug — "works" but isn't LayerNorm).
- Forgetting $\epsilon$ inside the sqrt — NaN on constant vectors.
- Post-LN with a large LR and no warmup, then blaming the architecture.

---

## Optimization for deep nets — AdamW, schedules, clipping

:::tldr
The transformer training recipe: AdamW ($\beta_1=0.9$, $\beta_2=0.95$–$0.999$,
weight decay 0.01–0.1 excluding biases/norms), linear warmup (1–5% of steps),
cosine decay to ~10% of peak LR, global-norm gradient clipping at 1.0. Every
piece fixes a specific failure mode — know which.
:::

**30-second answer:** Warmup tames the early steps when Adam's second moments
are uninitialized and gradients are largest. Cosine decay anneals into a good
minimum. Clipping bounds the worst single step (one bad batch can't undo
hours of training). Decoupled weight decay regularizes without interacting
with adaptive scaling. (Full AdamW mechanics in [ML
Fundamentals](#/ml-fundamentals).)

**Interview-depth — which piece fixes what:** **Warmup:** at step 0,
$\hat v_t$ is garbage (bias correction dividing tiny numbers) and the loss
landscape is unexplored — full-LR steps can permanently damage early
features (especially embeddings). **Cosine vs. step decay:** cosine spends
more steps at moderate LRs, which empirically finds flatter minima; step
decay is fine but touchier. **Clipping:** with Adam the update is already
per-coordinate bounded, but a pathological batch can still produce a large
*collective* step in a bad direction — clipping at global norm 1.0 is cheap
insurance, near-mandatory for RNNs, standard for transformers. **$\beta_2 =
0.95$:** for very long training runs the 0.999 default adapts too slowly to
nonstationary curvature; 0.95 is the modern LLM default. **Mixed precision:**
fp16 halves memory and speeds up matmuls; loss scaling prevents gradient
underflow; keep master weights + optimizer states in fp32, embeddings in
fp32. bf16 (no loss scaling needed, wider dynamic range) is preferred where
hardware supports it.

**Follow-ups:**
- "Why exclude biases and norm params from weight decay?" → they don't cause
  overfitting the way weights do (a bias shift isn't memorization), and
  decaying LayerNorm's $\gamma$ toward zero collapses representations.
- "Your loss spikes mid-training — debug order?" → (1) bad batch / data
  bug, (2) LR too high for current phase, (3) clipping disabled or too
  loose, (4) fp16 overflow (check loss scaling), (5) Post-LN instability.
  Check gradient norms per layer — the guilty layer is usually obvious.
- "When would you use SGD over AdamW for a deep net?" → rarely for
  transformers; some CNN/vision setups where SGD+momentum generalizes a
  hair better and you can afford the LR tuning. Know it's a real tradeoff,
  not a default.

**Mistakes:**
- Warmup too short relative to total steps — the divergence it was supposed
  to prevent happens at step 200 instead of step 20.
- Clipping *per-parameter* instead of global norm — destroys the update
  direction; always global norm.
- Decaying the LR to exactly 0 with cosine and then wondering why continued
  training does nothing — 10% floor, or restart.

---

## Gradient flow — vanishing, exploding, and training instability

:::tldr
Every layer multiplies the gradient by its Jacobian. Chain $L$ of them and
you get exponential behavior: all $<1$ → vanish, any $>1$ → explode. The
complete mitigation stack is: sane init (He/Xavier) + ReLU-ish activations +
residuals + Pre-LN + gradient clipping + warmup. Instability debugging is
checking which layer of this stack broke.
:::

**30-second answer:** $\partial L/\partial h_1 = (\prod_{l=2}^{L} J_l)\,
\partial L/\partial h_L$. Sigmoid's max derivative 0.25 gives
$0.25^{50} \approx 10^{-30}$ — early layers freeze. Large weights or
unclipped RNN steps give $\|J\| > 1$ repeatedly — NaN. Each mitigation
attacks one factor: init sets $\|J\| \approx 1$ at start, ReLU avoids the
0.25 contraction, residuals add an identity path that bypasses the product,
clipping caps the worst case.

**Interview-depth — the instability debugging checklist** (in order):
**1. Look at per-layer gradient norms** at init and step 100 — healthy: all
within ~10× of each other; sick: exponential decay/growth across depth tells
you exactly where the product breaks. **2. Check activation norms per layer**
— same story from the forward side. **3. Suspects in order:** LR too high
(loss spikes/NaN early) → missing/short warmup → Post-LN at depth → bad init
scale → fp16 overflow (gradients underflow to zero *or* overflow — check
loss-scaler behavior) → data bug (one corrupt batch with huge values).
**Attention-specific:** $QK^T$ growing with $d$ is handled by the
$1/\sqrt{d}$ scale; without it, softmax saturates and attention gradients
die — the same saturate-and-vanish story as sigmoid, one level up.

**The LSTM footnote:** LSTMs "solved" vanishing for sequences with the cell
state's *additive* update ($c_t = f_t \odot c_{t-1} + i_t \odot \tilde c_t$)
— when the forget gate is ~1, gradient flows back through time unattenuated
(the constant error carousel). Transformers made it moot by removing
recurrence, but the additive-preservation idea is the same one residuals
use. If an interviewer asks "how did LSTMs help vanishing gradients," that's
the sentence.

**Math:**
$$\left\|\frac{\partial L}{\partial h_1}\right\| \le
\left(\prod_{l=2}^{L}\|J_l\|\right)\left\|\frac{\partial L}{\partial h_L}\right\|,
\qquad J_l = \text{diag}(\phi'(z^{(l)}))\,W^{(l)}$$

**Follow-ups:**
- "How do you *detect* vanishing vs. exploding in practice?" → log
  per-layer gradient norms + update-to-parameter ratios
  ($\|\Delta\theta\|/\|\theta\| \approx 10^{-3}$ is healthy). Vanishing:
  early-layer norms ~0; exploding: norms spike then NaN.
- "Why doesn't the transformer have vanishing gradients across *sequence*
  length?" → no recurrent product over time steps; attention connects all
  positions in one hop (path length $O(1)$), so gradient paths don't grow
  with sequence length. Depth still matters — hence residuals.
- "Gradient clipping fixes exploding — what fixes vanishing?" → clipping
  only caps; vanishing needs architectural fixes (residuals, better
  activations, init, normalization). No optimizer setting recovers a
  $10^{-30}$ gradient.

**Mistakes:**
- Treating clipping as a vanishing-gradient fix — it only bounds large
  steps.
- Blaming the optimizer for what is an architecture problem (and vice
  versa) — check per-layer norms *before* tuning hyperparameters.
- Ignoring the data: a single batch with extreme values causes "exploding
  gradients" that no architecture change will fix.

---

## What happens during `backward()` — the mechanic's view

:::tldr
`loss.backward()`: autograd walks the graph in reverse topological order;
each node runs its saved `backward` closure, which needs the tensors cached
during forward (linear: input; ReLU: mask; norm: stats). Gradients accumulate
into `.grad` buffers. Then the optimizer reads `.grad`, updates params,
and you zero the buffers. Memory ≈ saved activations; compute ≈ 2× forward.
:::

**30-second answer:** Forward built a DAG of `Function` nodes, each holding
references to its inputs (or whatever its derivative needs). `backward()`
seeds the output gradient with 1 and propagates: each node computes
vector-Jacobian products for its inputs and passes them upstream. Leaf
tensors with `requires_grad` accumulate into `.grad`. Non-scalar losses need
an explicit `gradient` argument (usually ones — i.e., sum).

**Interview-depth — what's stored and why it costs so much:** For a
transformer training step, saved tensors include: every linear layer's input
($B \times T \times d$ each — the big one), attention probabilities
($B \times H \times T \times T$ — quadratic in sequence length, the reason
long-context training is memory-bound), dropout masks, LN statistics, and
embedding gather indices. That's why activation memory scales with batch ×
seq × layers × hidden, and why **activation checkpointing** (recompute
forward activations during backward instead of storing) and **FlashAttention**
(never materialize the $T \times T$ matrix) are the two biggest memory wins
in modern training. Optimizer states are the other half: Adam keeps $m$ and
$v$ per parameter in fp32 = 2× params on top of the fp32 master copy.

**The `.grad` accumulation gotcha:** `backward()` *adds* to `.grad`; the
optimizer never clears it. Forget `zero_grad()` and your effective batch is
"everything since the last zero" with a side of wrongness. (Deliberate
accumulation across micro-batches is exactly this mechanism used
intentionally.)

:::collapse retain_graph and friends
`backward()` frees the graph by default (saved tensors released). Calling it
twice needs `retain_graph=True` (multi-task losses, GAN-style alternating
updates). `torch.no_grad()` / `detach()` cuts graph construction —
inference and target networks. `grad()` (functional API) returns gradients
without touching `.grad` buffers — cleaner for meta-learning and
double-backward (Hessian-vector products via grad-of-grad).
:::

**Follow-ups:**
- "Why does training use 3–4× inference memory?" → params (1×) + fp32
  master copy + Adam $m$, $v$ (2×) + saved activations (often the largest
  term, scales with batch/seq). Inference needs params + KV cache only.
- "Explain activation checkpointing's tradeoff." → store activations every
  $k$-th layer, recompute the rest in backward: memory $O(n/k + k)$-ish at
  ~30% extra compute. Standard for long sequences.
- "What does `loss.backward()` do for a non-scalar loss?" → errors unless
  you pass `gradient=` — autograd needs a vector-Jacobian product seed;
  the default seed of 1 only makes sense for scalars (it's $dL/dL$).

**Mistakes:**
- `zero_grad()` after `step()` vs before `backward()` — either works if
  consistent; mixing them across accumulation loops doesn't.
- Backpropagating through a metric or a target network you meant to freeze
  — phantom gradients, silently wrong objective.
- In-place ops on saved tensors — autograd's version-counter errors exist
  to catch exactly this; don't "fix" them by cloning blindly, understand
  which tensor needed saving.

---

## Practice

- [ ] Write the 2-layer MLP forward/backward above from memory; verify
  gradients with finite differences on a tiny example.
- [ ] Derive He init ($2/\text{fan}_{in}$) from the variance-propagation
  argument, stating each independence assumption.
- [ ] Implement LayerNorm forward + backward in numpy; gradient-check it.
- [ ] On paper: show why $y = x + F(x)$ preserves gradient flow even when
  $\partial F/\partial x \to 0$; then explain Pre-LN vs Post-LN gradient
  norms at init.
- [ ] Given per-layer gradient norms decaying 10× per layer from output to
  input, write the 4-sentence diagnosis and the fix stack in order.
- [ ] Explain AdamW vs Adam in one sentence; then say exactly where weight
  decay is applied in each update rule.
- [ ] Whiteboard what tensors a transformer block must cache for backward,
  and name the two biggest memory wins (checkpointing, FlashAttention) with
  their tradeoffs.
- [ ] 60-second talk: "why does my transformer diverge at step 500?" —
  walk the instability checklist out loud.

[Previous: ← ML fundamentals](#/ml-fundamentals) · [Next: system design →](#/ml-system-design)
