---
title: "ML Fundamentals — Losses, Optimization, Regularization, Metrics"
slug: "ml-fundamentals"
section: "fundamentals"
nav_order: 1
nav_label: "ML Fundamentals"
tags: ["loss-functions", "optimization", "regularization", "normalization", "metrics", "ranking", "interview-prep"]
updated: "2026-10-01"
---

## TL;DR

Interviewers probe fundamentals to test whether your applied experience rests
on real understanding. The entire page reduces to five instincts:
**1.** losses are chosen by output semantics (probabilities → CE, scores →
pairwise/listwise, distances → contrastive); **2.** optimization is controlling
step size and direction under noisy curvature; **3.** regularization is budget
management for model capacity; **4.** normalization is conditioning the
optimization landscape; **5.** metrics are business decisions disguised as
math. If you can derive softmax+CE, explain AdamW vs Adam, and justify
pairwise vs listwise for a given ranking product, you're through.

:::tldr
**Losses:** CE for distributions, MSE for regression, pairwise/listwise for
ranking. **Optimization:** AdamW with warmup+decay is the default; gradient
clipping bounds the worst step. **Regularization:** L2 shrinks, L1 selects,
dropout averages subnetworks, early stopping is free. **Metrics:** ranking
quality is NDCG/MAP/Recall@K territory — never accuracy. **Bias/variance:**
diagnose with train/val gaps, fix capacity or data accordingly.
:::

---

## Losses

### Cross-entropy

:::tldr
Cross-entropy measures how surprised your model is by the true labels under
its predicted distribution. Softmax + CE is the default training objective for
classification because the gradient is just $(\hat y - y)$ — clean, bounded,
and directly pushes probability mass toward the correct class.
:::

**30-second answer:** Cross-entropy $H(p, q) = -\sum_i p_i \log q_i$ is the
expected number of bits needed to encode the true distribution $p$ using your
model's distribution $q$. When $p$ is one-hot (the usual case), it reduces to
$-\log q_{\text{true class}}$ — the negative log-likelihood. Minimizing it is
maximum-likelihood estimation.

**Interview-depth:** CE is *not* symmetric ($H(p,q) \neq H(q,p)$) — $p$ is
ground truth, $q$ is the model. The decomposition $H(p,q) = H(p) +
D_{KL}(p \,\|\, q)$ shows minimizing CE equals minimizing KL divergence, since
$H(p)$ is constant. Two practical consequences: **(1)** CE punishes confident
mistakes harshly (the log blows up as $q_{\text{true}} \to 0$), which is why it
drives sharper discrimination than MSE-on-logits but also why mislabeled data
destroys CE training. **(2)** CE only cares about the true class's probability
mass, so it's insensitive to *how* the remaining mass is distributed — relevant
when you later distill (soft targets carry that discarded information).

**Intuition:** Think of it as a betting loss. Your model places bets across
classes; CE is what you lose when the true class comes up. Betting 0.99 on the
wrong class costs ~6.6 nats; betting 0.51 costs ~0.67. The log scale means
*overconfidence* in wrong answers is punished superlinearly — the model learns
to calibrate, not just to be right.

**Details:** Label smoothing replaces the one-hot target $p$ with
$(1-\epsilon)\cdot\text{onehot} + \epsilon/K$, capping the loss and preventing
the logits from diverging to $\pm\infty$ — the model can't push $q \to 1$ for
free anymore. This regularizes and improves calibration but slightly weakens
the top-class signal; common $\epsilon = 0.1$. Temperature scaling divides
logits by $T$ *after* training to recalibrate — post-hoc, doesn't change
accuracy, fixes the overconfidence CE training induces.

**Math:**
$$H(p,q) = -\sum_{i=1}^{K} p_i \log q_i, \qquad q_i = \frac{e^{z_i}}{\sum_j e^{z_j}}$$
$$\frac{\partial L}{\partial z_i} = q_i - y_i \quad \text{(softmax + CE; derived below in Backprop)}$$

**Code:**
```python
import numpy as np

def softmax(z):
    z = z - z.max(axis=-1, keepdims=True)  # stability: invariance to shift
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)

def cross_entropy(logits, y):  # y: int class indices
    q = softmax(logits)
    return -np.log(q[np.arange(len(y)), y] + 1e-12).mean()
```

**Follow-ups:**
- "Why not MSE on logits for classification?" → MSE saturates: when the model
  is confidently wrong, sigmoid/softmax derivatives are near zero and the
  gradient vanishes; CE's gradient $(\hat y - y)$ stays informative. Also MSE
  assumes Gaussian noise — wrong for categorical outputs.
- "How does label smoothing change the gradient?" → target becomes
  $(1-\epsilon)y + \epsilon/K$; the gradient pushes $q$ toward the smoothed
  distribution, so logits stay bounded instead of diverging.
- "CE with class imbalance?" → weight classes (weighted CE), focal loss
  $-(1-q_t)^\gamma \log q_t$ down-weights easy examples, or resample. Weighting
  changes the optimum toward recall on the rare class.

**Mistakes:**
- Forgetting the log is over *probabilities* — applying CE to raw logits
  without softmax (numerically it's the fused `softmax_cross_entropy` op;
  conceptually CE needs a distribution).
- Averaging vs. summing the loss across the batch changes the effective LR —
  be consistent, know which your framework uses.
- Using accuracy as a training signal proxy during training — CE trains,
  accuracy reports; they can diverge (better CE, same accuracy).

:::collapse Binary cross-entropy
For two classes, softmax+CE reduces to sigmoid+BCE:
$$L = -\big[y \log \sigma(z) + (1-y)\log(1-\sigma(z))\big], \qquad
\frac{dL}{dz} = \sigma(z) - y$$
Same gradient structure. Use BCE-with-logits (fused, stable) rather than
sigmoid-then-BCE. For multi-label problems (each class an independent binary
decision), BCE per class is correct; softmax+CE is wrong because classes
aren't mutually exclusive.
:::

### Contrastive losses

:::tldr
Contrastive losses shape an embedding space: pull similar pairs together, push
dissimilar pairs apart. Triplet loss and InfoNCE are the two workhorses —
triplet for metric learning with mined negatives, InfoNCE (softmax over
in-batch negatives) for representation learning at scale.
:::

**30-second answer:** Given anchor $a$, positive $p$, negatives $\{n_i\}$:
triplet loss enforces $d(a,p) + m < d(a,n)$ for each negative with margin $m$;
InfoNCE treats it as classification over the positive vs. all negatives:
$$L_{\text{InfoNCE}} = -\log \frac{e^{s(a,p)/\tau}}{\sum_i e^{s(a,n_i)/\tau}}$$

**Interview-depth:** The temperature $\tau$ controls *hardness focus*: small
$\tau$ sharpens the softmax, making the loss dominated by the hardest
negatives (large gradients on near-misses); large $\tau$ treats all negatives
more uniformly. Triplet loss lives or dies by **negative mining** — random
negatives give zero loss (already satisfy the margin) and zero gradient;
semi-hard negatives (further than the positive but within the margin) give the
most useful signal. In-batch negatives (InfoNCE) scale this: with batch $B$
you get $B-1$ negatives for free, which is why contrastive pretraining wants
huge batches (SimCLR) or memory banks/queues (MoCo). **Collapse mode:** without
negatives the model can map everything to a constant vector and get zero
loss — negatives (or asymmetric tricks like BYOL/SimSiam stop-gradients) are
what prevent representational collapse.

**Intuition:** You're sculpting a space where "nearby" means "semantically
similar." The margin/temperature sets how *strict* the neighborhood boundaries
are. Too strict (tiny margin, tiny $\tau$) and the model overfits to noise;
too lax and everything blurs together.

**Follow-ups:**
- "Why does InfoNCE need large batches?" → negatives come from the batch;
  more negatives = tighter bound on mutual information and harder negatives
  on average. MoCo's queue decouples batch size from negative count.
- "Triplet vs. InfoNCE?" → triplet gives explicit margin control and works
  with few negatives but needs mining; InfoNCE scales with batch size and is a
  proper probabilistic objective, easier to tune via $\tau$.
- "How do you pick the margin?" → start 0.2–0.5 on normalized embeddings
  (cosine space); tune on a validation retrieval metric (Recall@K), not the
  loss value.

**Mistakes:**
- Using Euclidean distance on unnormalized embeddings — scale dominates;
  normalize first and use cosine (or accept the distance is scale-sensitive).
- No hard-negative mining with triplet loss → loss goes to zero, model learns
  nothing, and it *looks* like training succeeded.
- Forgetting collapse: training "converges" to a constant embedding. Check
  embedding variance / pairwise distances as a sanity metric.

### Ranking losses: pointwise, pairwise, listwise

:::tldr
Ranking is Rui's home turf: pointwise treats ranking as regression/classification
per item (ignores relative order), pairwise learns "A beats B" preferences, and
listwise optimizes the whole ranked list against a list metric. Production
search almost always ends at pairwise or listwise — because the product *is*
the ordering, not the scores.
:::

**30-second answer:** **Pointwise:** predict a relevance label per query-item
pair (MSE or CE against graded labels); sort by score. **Pairwise:** given a
preferred item $i$ over $j$, minimize $\log(1 + e^{-(s_i - s_j)}})$ (RankNet) or
hinge $\max(0, m - (s_i - s_j))$ — the model learns relative preference.
**Listwise:** optimize the permutation directly, e.g. ListNet (CE between
predicted and true top-one distributions) or LambdaRank/LambdaMART (gradients
scaled by the NDCG delta of swapping a pair).

**Interview-depth:** This is where depth pays. **Pointwise** is easy to train
and calibrate (scores are meaningful probabilities/grades) but inconsistent
with ranking metrics: two models with identical pointwise loss can have
wildly different NDCG, because the loss doesn't know position 1 matters more
than position 10. It's still the right choice when you need *calibrated*
scores (e.g., blending with business rules, thresholding). **Pairwise**
(RankNet, BPR) aligns with the pairwise nature of preference data (clicks:
clicked > skipped-above) and is the workhorse of learning-to-rank; its
limitation is that not all pairs matter equally — a swap at ranks 1–2 moves
NDCG far more than at 99–100. **Listwise** fixes this: LambdaRank multiplies
the RankNet gradient by $|\Delta\text{NDCG}|$ from swapping the pair, so the
optimizer spends capacity where the metric lives. LambdaMART (GBDT +
lambda gradients) dominated industry LTR for a decade for tabular features;
neural listwise (ListNet, ApproxNDCG, neural sort relaxations) matters when
features are learned end-to-end.

**The position-bias connection:** click logs are the cheapest pairwise
signal (clicked item > skipped items above it), but clicks confound relevance
with position. Unbiased LTR corrects with inverse propensity weighting (IPS):
weight each pair by $1/P(\text{examined} \mid \text{position})$. If the
interviewer asks "how do you train a ranker on click logs," the expected
answer is: pairwise loss on click-vs-skip pairs + IPS debiasing, evaluated on
human-graded NDCG.

**Math (RankNet):**
$$L = \log\big(1 + e^{-\sigma(s_i - s_j)}\big), \qquad
\lambda_{ij} = \frac{\partial L}{\partial s_i} \cdot |\Delta\text{NDCG}_{ij}|
\ \text{(LambdaRank)}$$

**Code (pairwise hinge, numpy):**
```python
def pairwise_hinge(s_pos, s_neg, margin=1.0):
    return np.maximum(0.0, margin - (s_pos - s_neg)).mean()
```

**Follow-ups:**
- "When would you choose pointwise over pairwise?" → when scores must be
  calibrated/thresholded, when labels are graded relevance judgments (0–4) and
  plentiful, or as a first baseline before investing in listwise.
- "How do you evaluate before online A/B?" → offline: NDCG/MAP on held-out
  human-graded queries; interleaving or counterfactual (IPS) estimators on
  logs; then online A/B on the business metric.
- "Listwise with neural nets — what's hard?" → list metrics are
  non-differentiable (sorting is piecewise constant); need smooth
  relaxations (ApproxNDCG, differentiable sorting) or lambda-style gradient
  surgery.
- "Your NDCG improved but CTR didn't — what happened?" → offline/online gap:
  position bias in training, metric gaming (model learned the labeler's
  biases), or the head queries dominate NDCG while the business lives in the
  tail. Slice metrics by query segment.

**Mistakes:**
- Training pointwise on click labels as if they were relevance grades —
  clicks are biased, sparse, and binary; they're preference signals, not
  grades.
- Reporting accuracy or AUC for a ranking model instead of NDCG/MAP/Recall@K.
- Ignoring position bias: "our pairwise model trained on clicks works great
  offline" — offline on clicks just measures fit to the biased logger.

:::collapse MSE — when regression is the job
$$L = \tfrac{1}{n}\sum (y - \hat y)^2, \qquad \nabla = \tfrac{2}{n}(\hat y - y)$$
MSE is the MLE under Gaussian noise. It punishes large errors quadratically —
good when big misses are truly much worse, bad with outliers (consider Huber).
Never use MSE on logits for classification (saturation, wrong noise model).
For ranking *scores* that feed thresholds, pointwise MSE on graded labels is
fine and gives calibrated-ish outputs.
:::

---

## Optimization

### SGD and momentum

:::tldr
SGD steps opposite the minibatch gradient; momentum adds a velocity term that
dampens oscillation in steep directions and accelerates along consistent ones.
It's still the optimizer of choice for many vision/CNN setups where it
generalizes slightly better than adaptive methods.
:::

**30-second answer:** SGD: $\theta \leftarrow \theta - \eta \nabla
\hat L(\theta)$. Minibatch noise is a feature (escapes sharp minima, cheap
steps) and a bug (noisy convergence). Momentum: $v \leftarrow \beta v +
\nabla \hat L$; $\theta \leftarrow \theta - \eta v$ — exponential moving
average of gradients.

**Interview-depth:** Momentum's effective step size is $\eta/(1-\beta)$ along
persistent directions — with $\beta=0.9$ that's a 10× amplification, which is
why you *lower* the LR when adding momentum. Nesterov momentum evaluates the
gradient at the lookahead point $\theta - \eta\beta v$, a first-order
correction that reduces overshoot. The "SGD generalizes better than Adam"
folk result: adaptive methods can converge to sharper minima; on CNNs with
long schedules SGD+momentum often wins test accuracy by a hair, at the cost
of more LR tuning. For transformers, AdamW dominates and the debate is moot.

**Math:**
$$v_{t+1} = \beta v_t + g_t, \qquad \theta_{t+1} = \theta_t - \eta v_{t+1}$$

**Follow-ups:**
- "Why does momentum help in ravines?" → gradients oscillate across the
  ravine (cancel in the average) but point consistently along it (accumulate)
  — the velocity aligns with the valley floor.
- "Batch size vs. learning rate?" → linear scaling rule: when multiplying
  batch size by $k$, multiply LR by $k$ (keeps the per-epoch update
  magnitude roughly constant), with warmup to stabilize early training.

### Adam and AdamW

:::tldr
Adam adapts per-parameter step sizes using first and second moment estimates —
fast, robust to sparse gradients and bad conditioning. AdamW *decouples*
weight decay from the adaptive update, which is what you actually want for
regularization. If you train transformers, you use AdamW.
:::

**30-second answer:** Adam keeps $m_t = \beta_1 m_{t-1} + (1-\beta_1)g_t$
(mean) and $v_t = \beta_2 v_{t-1} + (1-\beta_2)g_t^2$ (uncentered variance),
bias-corrects both, and steps $\theta \leftarrow \theta - \eta \,
\hat m_t/(\sqrt{\hat v_t} + \epsilon)$.

**Interview-depth:** The key insight: Adam's step is approximately
$\pm \eta$ per coordinate (sign descent with magnitude normalization), which
makes it scale-invariant to gradient magnitudes — great for embeddings and
heterogeneous features. **The Adam-vs-AdamW distinction is the classic
interview trap:** in original Adam, "weight decay" was implemented as L2
regularization *added to the gradient* — but then it gets divided by
$\sqrt{\hat v_t}$, so parameters with large gradients get *less* decay. That's
not weight decay; it's a mess. AdamW (Loshchilov & Hutter) applies decay
directly: $\theta \leftarrow \theta - \eta\lambda\theta$, decoupled from the
adaptive scaling. Empirically AdamW generalizes better and its $\lambda$ is
interpretable. Defaults that work: $\beta_1=0.9$, $\beta_2=0.999$ (0.95 for
very long training), $\epsilon=10^{-8}$, $\lambda \in [0.01, 0.1]$.

:::warn
If an interviewer asks "why AdamW over Adam," the one-line answer is:
Adam's L2 is scaled by the adaptive denominator, so decay strength varies
per parameter — AdamW decouples it so every parameter decays at rate
$\eta\lambda$. Say that sentence verbatim and you'll pass the question.
:::

**Math:**
$$\hat m_t = \tfrac{m_t}{1-\beta_1^t}, \quad \hat v_t = \tfrac{v_t}{1-\beta_2^t}$$
$$\theta_{t+1} = \theta_t - \eta\left(\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}
+ \lambda\theta_t\right) \quad \text{(AdamW: decay outside the adaptive term)}$$

**Code (AdamW from scratch, numpy):**
```python
class AdamW:
    def __init__(self, params, lr=1e-3, b1=0.9, b2=0.999, eps=1e-8, wd=0.01):
        self.p, self.lr, self.b1, self.b2, self.eps, self.wd = params, lr, b1, b2, eps, wd
        self.m = [np.zeros_like(x) for x in params]
        self.v = [np.zeros_like(x) for x in params]
        self.t = 0
    def step(self, grads):
        self.t += 1
        for i, (p, g) in enumerate(zip(self.p, grads)):
            self.m[i] = self.b1*self.m[i] + (1-self.b1)*g
            self.v[i] = self.b2*self.v[i] + (1-self.b2)*g*g
            mh = self.m[i]/(1-self.b1**self.t); vh = self.v[i]/(1-self.b2**self.t)
            self.p[i] -= self.lr*(mh/(np.sqrt(vh)+self.eps) + self.wd*p)
```

**Follow-ups:**
- "Why bias correction?" → $m_0 = v_0 = 0$ biases early estimates toward
  zero; dividing by $(1-\beta^t)$ removes the bias. Matters most in the first
  ~hundred steps — i.e., exactly when warmup is active.
- "When does Adam fail?" → very noisy small-batch settings where $v_t$ is a
  bad variance estimate; generalization gap on some CNN tasks; and
  non-convergence counterexamples exist (fixed by AMSGrad). Also: Adam +
  L2-in-gradient is *not* AdamW — check your framework's default.
- "Epsilon — why does it matter?" → in half precision, $\sqrt{\hat v_t}$ can
  underflow; larger $\epsilon$ ($10^{-6}$–$10^{-4}$) stabilizes fp16 training.

**Mistakes:**
- Using Adam with `weight_decay` in a framework that folds it into the
  gradient (that's Adam-with-L2, not AdamW) and wondering why decay tuning
  does nothing predictable.
- Cranking LR without warmup on transformers — early gradients are huge and
  Adam's $v_t$ hasn't stabilized; warmup exists for this.
- $\beta_2 = 0.999$ with tiny batches: the second moment adapts too slowly
  to track the noise; consider 0.95.

### LR schedules, gradient clipping, weight decay

**Schedules:** Warmup (linear, ~1–5% of steps) stabilizes early adaptive
estimates; then decay — cosine annealing to ~10% of peak, or step decay. Cosine
is the default for transformers; linear decay to zero is common for
fine-tuning. The schedule *is* a hyperparameter: too-short warmup diverges,
too-long wastes compute.

**Gradient clipping:** Global-norm clipping — if $\|g\| > c$, scale
$g \leftarrow c \cdot g/\|g\|$. It doesn't change the *direction*, only bounds
the worst step. Essential for RNNs/transformers where one bad batch can
explode activations. $c = 1.0$ is the standard starting point. Note: with Adam
the per-coordinate normalization already bounds steps, but clipping still
protects against pathological batches.

**Weight decay:** L2 penalty $\tfrac{\lambda}{2}\|\theta\|^2$ shrinks weights
toward zero, penalizing large weights that memorize. In AdamW it's decoupled
(step above). Don't decay biases and normalization parameters (standard
practice — they don't overfit the same way, and decaying LayerNorm scale can
hurt).

:::collapse One-cycle and restarts
One-cycle (warmup up, anneal down, with momentum cycled inversely) trains fast
for fixed-budget settings. Cosine restarts (SGDR) periodically spike the LR to
escape minima and snapshot ensembles. Both are niche for large-scale
transformer training but fair game as "what else do you know" follow-ups.
:::

---

## Regularization

:::tldr
Every regularizer is a way to spend limited model capacity on signal instead
of noise. L2 shrinks weights, L1 zeroes them (feature selection), dropout
trains an ensemble of subnetworks, early stopping halts before memorization,
augmentation manufactures data. Stack them — they compose.
:::

**L1 vs L2:** L2 ($\lambda\|\theta\|_2^2$) penalizes quadratically — many small
weights, smooth shrinkage, differentiable everywhere. L1 ($\lambda\|\theta\|_1$)
penalizes linearly — the diamond-shaped constraint meets loss contours at
corners, producing exact zeros: automatic feature selection. L1 is
non-differentiable at 0 (use subgradients/proximal methods). Elastic net mixes
both. In deep learning L2 (as AdamW decay) dominates; L1 shows up in linear
models and sparse-feature regimes (ads CTR with billions of sparse IDs often
uses L1-ish or frequency-based pruning).

**Dropout:** During training, zero each activation with probability $p$ and
scale survivors by $1/(1-p)$ (inverted dropout — no test-time scaling needed).
Effect: trains an ensemble of $2^n$ thinned subnetworks sharing weights;
prevents co-adaptation of neurons. $p=0.1$–$0.5$; higher in large FC layers,
lower/zero in conv/transformer blocks (modern transformers often use 0.1 or
none with enough data). At test time dropout is off — the full network
approximates the ensemble average.

**Early stopping:** Monitor validation loss; stop (or checkpoint) at its
minimum. It's free regularization with one hyperparameter (patience). The
theory view: early stopping ≈ L2 regularization (limits how far weights travel
from init). Always checkpoint the best, not the last.

**Augmentation:** The highest-ROI regularizer when data is the bottleneck —
label-preserving transforms (crops, flips, color jitter; back-translation and
paraphrase for text; mixup/cutmix blending examples). It encodes invariances
you know hold. For ranking: query reformulation, negative sampling strategies,
and synthetic hard negatives are the augmentation analogues.

**Follow-ups:**
- "Why does dropout need the $1/(1-p)$ scaling?" → keeps the *expected*
  activation magnitude identical between train and test, so downstream layers
  see the same scale.
- "Dropout + BatchNorm — problem?" → yes, the classic conflict: dropout
  changes activation variance at train time while BatchNorm's running stats
  assume a fixed distribution — the "variance shift" hurts. LayerNorm +
  dropout is fine (per-example, no running stats).
- "How do you pick between more data and more regularization?" → diagnose
  first: big train/val gap = variance problem (regularize, augment, more
  data); both bad = bias problem (capacity, features, training).

**Mistakes:**
- Applying dropout at test time (or forgetting inverted scaling) — silent
  degradation.
- L1 on embeddings with Adam — the adaptive denominator fights the sparsity;
  use proper proximal updates or accept L2.
- Early stopping on a noisy validation metric without patience/smoothing —
  stops at noise, not at the minimum.

---

## Normalization

:::tldr
Normalization reconditions the optimization landscape: BatchNorm normalizes
across the batch (great for CNNs, breaks with small/variable batches and at
test-time distribution shift), LayerNorm normalizes per example across
features (batch-independent — the transformer default), RMSNorm drops the
mean-centering for speed (used by LLaMA). Transformers use LayerNorm/RMSNorm
because sequences vary in length, batches are small relative to model size,
and per-token statistics are well-defined where batch statistics aren't.
:::

**30-second answer:** BatchNorm: normalize each channel using batch mean/var,
then learnable affine $\gamma, \beta$; keeps running stats for inference.
LayerNorm: normalize across the feature dim *per example* — no batch
dependence, no running stats. RMSNorm: LayerNorm without mean subtraction,
just RMS scaling — cheaper, works as well in practice.

**Interview-depth — why transformers don't use BatchNorm:** **(1)** NLP
batches are small and sequences vary in length — batch statistics are noisy
and padding contaminates them. **(2)** At inference you often score one
example (or one token autoregressively) — BatchNorm's train/test mismatch
(running stats vs. batch stats) becomes a real distribution-shift hazard.
**(3)** Transformers already stabilize via residuals + careful init; the
marginal gain of batch statistics isn't worth the fragility. LayerNorm's
per-token normalization is well-defined for any batch size including 1, which
is exactly the autoregressive decoding regime. RMSNorm (LLaMA, Mistral) keeps
the benefit while dropping the mean-centering compute.

**Where normalization sits:** Post-LN (norm after residual add — original
Transformer) vs. Pre-LN (norm inside the residual branch, before
attention/FFN). Pre-LN is the modern default: gradients flow through the
clean residual path unimpeded, training is far more stable at depth, though
final-layer representations can be less expressive (fixed by a final LN).
If asked "why is training unstable," Pre-LN vs Post-LN is a top-three suspect.

**Math (LayerNorm):**
$$\mu = \tfrac{1}{d}\sum_i x_i, \quad \sigma^2 = \tfrac{1}{d}\sum_i (x_i-\mu)^2,
\quad \hat x_i = \frac{x_i - \mu}{\sqrt{\sigma^2 + \epsilon}}, \quad
y_i = \gamma_i \hat x_i + \beta_i$$
RMSNorm: $\hat x_i = x_i / \sqrt{\tfrac{1}{d}\sum_j x_j^2 + \epsilon}$.

**Code:**
```python
def layer_norm(x, gamma, beta, eps=1e-5):
    mu = x.mean(axis=-1, keepdims=True)
    var = x.var(axis=-1, keepdims=True)
    return gamma * (x - mu) / np.sqrt(var + eps) + beta
```

**Follow-ups:**
- "Why does BatchNorm help optimization?" → the honest answer: debated.
  Original claim (internal covariate shift reduction) is disputed; the
  best-supported story is that it smooths the loss landscape (better
  Lipschitz constants), allowing larger LRs. Say "it conditions the
  landscape; the covariate-shift story is contested" and you sound senior.
- "BatchNorm at test time?" → uses running mean/var (EMA of training stats),
  frozen affine params. Mismatch when test distribution shifts — a real
  production failure mode.
- "Why is LayerNorm's per-token statistic OK but BatchNorm's per-batch not?"
  → a token's feature vector is a fixed-size, semantically coherent unit;
  a batch is an arbitrary collection. Normalizing over features of one
  example is always well-defined.

**Mistakes:**
- Normalizing across the wrong axis (batch vs. feature) — the single most
  common LayerNorm implementation bug.
- Forgetting `eps` inside the sqrt → NaN when variance is ~0 (constant
  inputs, e.g., padding).
- Applying weight decay to $\gamma, \beta$ and biases — standard practice
  excludes them.

---

## Backprop

:::tldr
Backprop is the chain rule on a computational graph, evaluated reverse-mode:
one backward pass gives gradients for *all* parameters at ~2× the cost of
forward. The softmax+CE gradient $(\hat y - y)$ and the vanishing/exploding
analysis of repeated multiplication are the two derivations worth having
cold.
:::

**30-second answer:** Forward pass builds a graph of operations and caches
intermediate values; backward pass applies the chain rule from the loss
backward, each node multiplying the incoming gradient by its local Jacobian.
Reverse-mode AD computes the full gradient vector in one pass — that's why
it's linear in parameters, not quadratic.

**Interview-depth — what tensors are stored:** For each op, backward needs
whatever appears in its local derivative: linear layers store their *input*
($\partial (Wx)/\partial W = x^T$); activations store their *output*
(sigmoid: $\sigma(1-\sigma)$) or input (ReLU: mask of $x>0$); normalization
stores normalized values, mean, and inverse std. This is why training memory
≈ activations, not parameters — and why activation checkpointing
(recompute instead of store) trades 30% compute for large memory savings.

**Softmax+CE gradient (derive it live):** With $q_i = e^{z_i}/\sum_j e^{z_j}$
and $L = -\sum_k y_k \log q_k$:
$$\frac{\partial q_i}{\partial z_j} = q_i(\delta_{ij} - q_j), \qquad
\frac{\partial L}{\partial z_j} = -\sum_k y_k \frac{1}{q_k}
q_k(\delta_{kj} - q_j) = q_j - y_j$$
The beautiful result: **gradient = prediction minus target**. Bounded in
$[-1, 1]$, zero exactly at the optimum, no saturation pathology — this is
*why* softmax+CE trains well.

**Vanishing/exploding gradients:** A deep stack multiplies Jacobians:
$\partial L/\partial h_1 = \prod_{l} J_l \cdot \partial L/\partial h_L$.
If each $\|J_l\| < 1$ (sigmoid/tanh saturation, small weights), the product
decays exponentially → early layers freeze (vanishing). If $>1$, it explodes →
NaNs/divergence. Sigmoid is the classic vanisher (max derivative 0.25);
that's the historical reason for ReLU + careful init + residuals + gradient
clipping. LSTMs "solved" it with the constant-error carousel (additive cell
state, gradient flows undiminished); transformers sidestep recurrence
entirely, and residuals give every layer a direct gradient path.

**Code (manual backprop through one linear+softmax+CE layer):**
```python
# forward: z = X @ W + b ; q = softmax(z) ; L = CE(q, y)
# backward, given dL/dz = (q - y_onehot)/n:
dW = X.T @ dz          # (d_in, n) x (n, d_out)
db = dz.sum(axis=0)
dX = dz @ W.T          # propagate to earlier layers
```

**Follow-ups:**
- "Forward-mode vs reverse-mode AD?" → forward-mode cost scales with #inputs,
  reverse-mode with #outputs. One scalar loss + millions of params ⇒
  reverse-mode wins by ~6 orders of magnitude. Forward-mode is for
  few-inputs/many-outputs (e.g., Jacobians w.r.t. a small input).
- "Why do we need the graph / can't we do it numerically?" → finite
  differences need $O(P)$ forward passes for $P$ params and suffer
  truncation error; backprop needs one backward pass, exact to
  floating-point.
- "Explain gradient checkpointing." → don't store all activations; store a
  subset and recompute the rest during backward. Memory $O(\sqrt{n})$ for
  $n$ layers at ~1.3× compute. Standard for long-context training.

**Mistakes:**
- Forgetting `zero_grad()` — gradients accumulate across batches (a feature
  for accumulation, a bug otherwise).
- Backpropping through something you meant to detach (e.g., the target
  network in distillation/RL) — phantom gradient paths silently change the
  objective.
- In-place ops on tensors needed for backward (ReLU-in-place on its own
  input is fine; in-place on a *saved* tensor corrupts the graph).

---

## Metrics

### Classification metrics

:::tldr
Accuracy lies under class imbalance and cost asymmetry. Precision/recall/F1
describe the confusion matrix; ROC-AUC measures ranking quality of scores
across thresholds; PR-AUC is the honest metric for rare positives; calibration
measures whether predicted probabilities mean what they say.
:::

**30-second answer:** Precision = TP/(TP+FP) (of predicted positives, how
many right); Recall = TP/(TP+FN) (of actual positives, how many found); F1 =
harmonic mean. ROC-AUC = $P(\text{score}(+) > \text{score}(-))$ over random
pairs — threshold-independent ranking quality. PR-AUC integrates
precision-recall — use it when positives are rare (ROC-AUC looks deceptively
good). Calibration: does "70% confident" happen 70% of the time (reliability
diagrams, ECE)?

**Interview-depth:** **Accuracy paradox:** 99% negatives → a constant
classifier scores 99% accuracy and is useless. **F1 vs. business cost:** F1
weights precision/recall equally, but fraud detection wants recall (missing
fraud is expensive) while ad targeting wants precision (irrelevant ads burn
trust) — the metric must encode the cost matrix, and the *threshold* is a
business decision, not an ML one. **ROC-AUC's blind spot:** it's dominated by
high-score regions and insensitive to the top of the ranked list — for
recommendation/search you need position-aware metrics (below). **Calibration
matters when** probabilities feed downstream decisions (bidding, thresholding,
combining models) — CE-trained models are typically overconfident; fix with
temperature scaling or isotonic regression on a held-out set.

**Math:**
$$\text{Prec} = \tfrac{TP}{TP+FP}, \quad \text{Rec} = \tfrac{TP}{TP+FN},
\quad F_1 = \tfrac{2PR}{P+R}, \quad \text{AUC} = P(s_+ > s_-)$$

**Follow-ups:**
- "Your AUC is 0.95 but the product is bad — why?" → AUC is threshold-free
  and pair-based; the operating threshold may sit in a bad spot, the positive
  rate may be tiny (PR-AUC tells the truth), or the pairs that matter
  (top-K) aren't the pairs AUC weights.
- "How do you pick a threshold?" → maximize expected utility: threshold where
  marginal precision equals the cost ratio; or constrain one metric
  (recall ≥ 0.9) and maximize the other. Never default to 0.5 without saying
  why.
- "Micro vs macro averaging?" → micro aggregates counts (dominated by frequent
  classes); macro averages per-class metrics (every class counts equally).
  Report both when classes are imbalanced.

**Mistakes:**
- Reporting accuracy on imbalanced data.
- Tuning the threshold on the test set — threshold is a hyperparameter, tune
  on validation.
- Confusing a well-ranked model (high AUC) with a well-calibrated one.

### Ranking metrics — NDCG, MAP, MRR, Recall@K

:::tldr
Ranking metrics encode *position*: a relevant item at rank 1 is worth more
than at rank 10. NDCG (graded relevance, discounted by position, normalized)
is the default offline metric for search; MAP averages precision over recall
levels; MRR cares only about the first relevant result; Recall@K measures
retrieval coverage. Know which one matches the product's user behavior.
:::

**30-second answer:**
- **Recall@K** = fraction of all relevant items appearing in top K. Retrieval
  metric — did we find the candidates?
- **MRR** = mean of $1/\text{rank of first relevant}$. For known-item /
  question-answering — only the first hit matters.
- **MAP** = mean over queries of average precision (precision at each
  relevant item's rank, averaged). Binary relevance, rewards putting relevant
  items early.
- **NDCG@K** = $\text{DCG@K}/\text{IDCG@K}$ with
  $\text{DCG@K} = \sum_{i=1}^{K} \frac{2^{rel_i}-1}{\log_2(i+1)}$.
  Graded relevance (0–4), position discount, normalized to $[0,1]$ per query.

**Interview-depth — choosing between them:** The metric must match how users
consume the list. **Web search / feed ranking** → NDCG@K: graded relevance
(not all relevant items are equal), heavy top-weighting (users rarely scroll),
K matched to the visible viewport (NDCG@10 for page one). **Retrieval stage**
(two-tower candidate generation) → Recall@K with large K (100–1000): the
ranker downstream will reorder, so coverage is what matters; a retrieval
model with great NDCG@10 but poor Recall@1000 starves the ranker.
**Q&A / navigational** → MRR: one right answer, position 1 or bust.
**MAP** is the classic TREC metric; in industry it's largely superseded by
NDCG for graded labels but still standard for binary-relevance benchmarks.

**Why the $2^{rel}-1$ gain and $\log$ discount:** exponential gain says a
grade-4 item is worth far more than two grade-3s (strong relevance is
superlinearly valuable); log discount says rank 2 is nearly as good as rank
1 but rank 100 is nearly worthless — matching observed click decay. These
aren't arbitrary: they're fit to user behavior. If an interviewer asks "why
log base 2," the honest answer is convention calibrated to click curves —
the *shape* (steep early discount) matters, the base doesn't.

**Normalization matters:** DCG is query-dependent (a query with ten relevant
docs has higher achievable DCG than one with two); dividing by IDCG (DCG of
the ideal ordering) makes NDCG comparable across queries so the mean is
meaningful. Always report the K, the gain function, and the relevance grades
— "NDCG improved 2%" is meaningless without them.

**Position-bias-aware evaluation:** offline metrics computed on click logs
inherit position bias. IPS-weighted metrics or interleaving debias online
comparisons; human-graded test sets remain the gold standard for absolute
numbers. Slice by query segment (head/torso/tail) — aggregate NDCG hides
tail regressions behind head wins.

**Math:**
$$\text{DCG@K} = \sum_{i=1}^{K}\frac{2^{rel_i}-1}{\log_2(i+1)}, \qquad
\text{NDCG@K} = \frac{\text{DCG@K}}{\text{IDCG@K}}$$
$$\text{AP} = \frac{1}{|\text{rel}|}\sum_{k} P(k)\cdot rel(k), \qquad
\text{MRR} = \frac{1}{|Q|}\sum_q \frac{1}{\text{rank}_q}$$

**Code (NDCG@K, numpy):**
```python
def dcg(relevances, k):
    rel = np.asarray(relevances)[:k]
    return np.sum((2**rel - 1) / np.log2(np.arange(2, len(rel) + 2)))
def ndcg(ranked_rels, k):
    ideal = dcg(sorted(ranked_rels, reverse=True), k)
    return dcg(ranked_rels, k) / ideal if ideal > 0 else 0.0
```

**Follow-ups:**
- "NDCG@5 vs NDCG@100 — when each?" → @5/@10 for the ranking stage (what the
  user sees); @100+ for retrieval coverage diagnostics. Report both, optimize
  the one matching the stage.
- "Your model beats baseline on NDCG but loses the A/B — diagnose." →
  offline/online gap checklist: label staleness, position bias in training
  labels, metric gaming, head/tail skew, novelty effects in the A/B, or the
  baseline was already at the metric's ceiling and gains are noise (check
  significance + effect size).
- "How do you get relevance labels?" → human grading (expensive, gold),
  clicks with IPS debiasing (cheap, biased), LLM-as-judge (cheap, check
  agreement with humans first). Production systems use all three in a
  hierarchy.

**Mistakes:**
- Reporting NDCG without K, gains, or grade distribution.
- Averaging DCG instead of NDCG across queries (dominated by
  many-relevant-doc queries).
- Optimizing the retrieval stage on NDCG@10 instead of Recall@K — starves
  the ranker of candidates it could have ordered well.
- Evaluating a ranker on the same click logs it trained on without debiasing
  — measures fit to position bias, not relevance.

---

## Bias, variance, and overfitting

:::tldr
Bias = error from wrong assumptions (underfit); variance = error from
sensitivity to the training sample (overfit). Diagnose with the train/val
gap: both bad → bias (add capacity/features/training); train good, val bad →
variance (regularize, augment, more data). The double-descent footnote only
matters if someone asks.
:::

**30-second answer:** Expected test error decomposes (for MSE) into
$\text{bias}^2 + \text{variance} + \text{irreducible noise}$. High bias:
model too simple to capture the pattern — training error is high too. High
variance: model memorizes training noise — training error low, validation
high. Overfitting *is* high variance.

**Interview-depth:** The decomposition guides the fix, not the poetry.
**Learning curves** (error vs. training size): if train and val curves
converge to the same high error → bias problem, more data won't help; if a
gap persists and val is still falling → variance problem, more data *will*
help. **Modern caveat:** in the overparameterized regime, bigger models can
*reduce* variance (double descent / benign overfitting) — but the diagnostic
discipline is unchanged: look at the curves, then act. For ranking systems
specifically: overfitting often shows up as head-query memorization with tail
collapse — slice the val metric by segment before concluding.

**Math:**
$$\mathbb{E}[(y - \hat f(x))^2] = \underbrace{(f(x)-\mathbb{E}\hat f)^2}_{\text{bias}^2}
+ \underbrace{\mathbb{E}[(\hat f - \mathbb{E}\hat f)^2]}_{\text{variance}}
+ \sigma^2$$

**Follow-ups:**
- "Your deep net has high bias — what do you do?" → bigger model, train
  longer, better features/architecture, check for optimization failure
  (is train loss actually minimized?), label noise.
- "High variance — ranked fixes?" → (1) more/better data + augmentation,
  (2) regularization (weight decay, dropout, early stopping), (3) reduce
  capacity or ensemble. In that order of ROI.
- "Explain double descent in one minute." → past the interpolation
  threshold, larger models find smoother interpolating solutions and test
  error falls again; classical U-curve assumed model size ≈ capacity
  monotonically. It doesn't invalidate bias/variance — it refines what
  "capacity" means for overparameterized models.

**Mistakes:**
- Treating "overfitting" as the only failure mode — half of real debugging
  is underfitting (bad features, broken training, too-aggressive
  regularization).
- Adding regularization to fix high *bias* — regularization increases bias;
  you'll make it worse.
- Judging overfitting from training loss alone — without a validation curve
  you can't distinguish memorization from learning.

---

## Practice

- [ ] Derive the softmax+CE gradient $(\hat y - y)$ on paper, from the
  definition, without looking. Then extend it to label smoothing.
- [ ] Implement AdamW from scratch in numpy and match PyTorch's output on a
  toy problem for 10 steps.
- [ ] Write `dcg`/`ndcg` from memory; then explain why the gain is
  exponential and the discount logarithmic.
- [ ] Given a confusion matrix with 1% positives, compute precision, recall,
  F1, and explain why accuracy is misleading — out loud, in 60 seconds.
- [ ] Whiteboard pairwise (RankNet) loss and explain when you'd switch to
  LambdaRank-style $|\Delta\text{NDCG}|$ weighting.
- [ ] Diagnose: train NDCG 0.81, val NDCG 0.62, both flat with more data.
  Write the 3-sentence diagnosis and fix plan. (Answer: variance problem
  that more data isn't fixing → regularization/augmentation, or label
  noise; check head/tail slices.)
- [ ] Explain AdamW vs Adam in one sentence, then derive where the L2 term
  goes in each update.

[Previous: project deep-dive](#/project-deep-dive) · [Next: deep learning →](#/deep-learning)
