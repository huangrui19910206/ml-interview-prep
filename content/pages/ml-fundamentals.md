---
title: "ML Fundamentals — Losses, Optimization, Regularization, Metrics"
slug: "ml-fundamentals"
section: "fundamentals"
nav_order: 1
nav_label: "ML Fundamentals"
tags: ["loss-functions", "optimization", "regularization", "normalization", "metrics", "ranking", "interview-prep"]
updated: "2026-10-07"
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

### Classification metrics: the confusion matrix and friends

:::tldr
Every classification metric is arithmetic on four counts — TP, FP, FN, TN.
Precision = "of the alarms I raised, how many were real"; recall = "of the
real cases, how many did I catch." F1 is their harmonic mean. Accuracy is the
one metric you should distrust on sight whenever classes are imbalanced.
:::

**30-second answer:** Draw the 2×2: rows are *actual* (positive/negative),
columns are *predicted*. TP = predicted positive and right; FP = predicted
positive and wrong (false alarm); FN = predicted negative and wrong (miss);
TN = predicted negative and right. Then:
$$\text{Precision} = \tfrac{TP}{TP+FP}, \qquad \text{Recall} = \tfrac{TP}{TP+FN}$$
Precision answers "how trustworthy are my positive predictions";
recall answers "how complete is my coverage of the positives."

**The worked example you should be able to do live:** 1,000 transactions, 10
are fraud (1% positive rate). Your model flags 20 as fraud and catches 8 of
the 10. So TP=8, FP=12, FN=2, TN=978. Precision = 8/20 = **40%** (3 of every 5
alarms are false). Recall = 8/10 = **80%** (caught most fraud). Accuracy =
986/1000 = **98.6%** — looks excellent, tells you nothing: a model that flags
*nothing* scores 99%. This is the accuracy paradox, and interviewers use it
as a shibboleth — if you quote accuracy on imbalanced data unprompted, you
fail the question.

**Interview-depth — the precision/recall tradeoff:** they're joined at the
threshold. Lower the decision threshold → more positives predicted → recall
goes up, precision goes down (more false alarms). Raise it → the reverse.
There is no free lunch; the *operating point* is a business decision about
relative costs. **Spam filter** (false positive = legit email hidden):
precision matters, a missed spam (FN) is cheap. **Fraud / cancer screening**
(false negative = disaster): recall matters, false alarms are cheap to review.
**F1** $= 2PR/(P+R)$ is the harmonic mean — it punishes extreme imbalance
between the two (P=1.0, R=0.1 gives F1≈0.18, not 0.55), which is why it's the
default single number when you need *both* but have no cost model. **F-beta**
generalizes: $F_\beta = (1+\beta^2)PR/(\beta^2 P + R)$; $\beta=2$ weights
recall 2×, $\beta=0.5$ weights precision 2×. If the interviewer names
asymmetric costs, name $F_\beta$, don't just say "F1."

**Specificity and friends:** Specificity = TN/(TN+FP) = 1 − FPR — the
true-negative rate; clinicians love it, ML interviews rarely need it beyond
the definition. Balanced accuracy = (recall + specificity)/2 — a quick fix
for accuracy under imbalance.

**Math:**
$$F_1 = \frac{2}{\frac{1}{P}+\frac{1}{R}} = \frac{2TP}{2TP+FP+FN}$$

**Code:**
```python
def prf(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2*p*r/(p+r) if p+r else 0.0
    return p, r, f1
# fraud example: prf(8, 12, 2) -> (0.40, 0.80, 0.533)
```

**Follow-ups:**
- "Precision 90%, recall 30% — good model?" → "For what?" If false alarms are
  expensive (ad targeting, email), that's a fine operating point; if misses
  are expensive, it's terrible. Then ask about the positive rate — with 1%
  positives, 90% precision is genuinely strong.
- "Why harmonic mean, not arithmetic?" → the harmonic mean is dominated by
  the smaller value, so gaming one metric while tanking the other scores
  badly. Arithmetic mean would let P=1.0, R=0.01 look respectable.
- "Your precision dropped after launch — diagnose." → label shift (positive
  rate changed), threshold drift, feature staleness, or an upstream change
  flooding you with easy negatives. Check the confusion matrix *counts*, not
  just the ratios.

**Mistakes:**
- Quoting accuracy on imbalanced data without mentioning the base rate.
- Tuning the threshold on the test set — the threshold is a hyperparameter;
  tune it on validation, report on test.
- Comparing F1 across datasets with different positive rates — F1 depends on
  prevalence; it's not comparable across different base rates.

### Precision-recall curves and PR-AUC

:::tldr
A PR curve sweeps the decision threshold and plots precision vs. recall —
it shows the *entire tradeoff*, not one operating point. PR-AUC (average
precision) summarizes it. For rare positives it's the honest metric: its
random baseline is the positive rate itself, so a bad model can't hide.
:::

**30-second answer:** Sort examples by score, sweep the threshold from strict
to lax, and at each step record (recall, precision). Plot precision (y) vs.
recall (x). The area under it — PR-AUC, usually computed as *average
precision* (AP, the precision at each threshold weighted by the recall gain)
— is a threshold-free summary. A random classifier scores PR-AUC ≈ positive
rate (e.g., 0.01 for 1% fraud), so unlike ROC-AUC there's no deceptive 0.5
floor to hide behind.

**Interview-depth — reading the curve:** the curve starts at the
highest-threshold point (low recall, usually high precision) and ends at
recall = 1 (precision = positive rate — you've flagged everything). A good
model's curve hugs the top-right: high precision *maintained* as recall
grows. The shape tells you where the model struggles: a sharp early drop
means the top-scoring positives are polluted with false alarms — your best
bets aren't trustworthy. **Why AP not just AUC of the curve:** the standard
computation (average precision = $\sum_k P(k)\,\Delta R(k)$) weights precision
by actual recall gains, which handles the curve's sawtooth interpolation
correctly; naive trapezoidal integration overstates it.

**Why PR beats ROC on imbalanced data:** ROC plots TPR vs. FPR, and
FPR = FP/(FP+TN) — with 99% negatives, the TN term swamps everything, so
thousands of false alarms barely move FPR. ROC-AUC 0.95 can coexist with
precision of 10%. The PR curve has no TN term — every false alarm directly
hurts precision. Rule of thumb: if the positive class is rare *and* it's the
class you care about, PR-AUC is the primary metric; ROC-AUC is the secondary.

**Math:**
$$\text{AP} = \sum_{k} P(k)\,\Delta R(k), \qquad
\text{random baseline} = \frac{\#\text{positives}}{\#\text{total}}$$

**Code (PR curve sweep, numpy):**
```python
def pr_curve(y_true, scores):
    order = np.argsort(-scores)          # strict -> lax threshold
    y = np.asarray(y_true)[order]
    tp = np.cumsum(y); fp = np.cumsum(1 - y)
    precision = tp / (tp + fp)
    recall = tp / tp[-1]
    ap = np.sum(precision[1:] * np.diff(recall))  # average precision
    return recall, precision, ap
```

**Follow-ups:**
- "PR-AUC 0.6 on 1% positives — good?" → enormously better than the 0.01
  baseline — 60× random. Always interpret PR-AUC *relative to prevalence*.
- "When is ROC-AUC the better choice?" → balanced classes, or when both
  classes' ranking quality matters symmetrically (e.g., general classifier
  benchmarking). Also ROC-AUC has nicer statistical properties (it's a
  proper ranking probability, $P(s_+ > s_-)$).
- "Davis & Goadrich?" → the 2006 result interviewers sometimes name-drop: a
  model dominates in ROC space iff it dominates in PR space — but PR space
  *magnifies* differences in the high-precision region that ROC compresses.
  Say that and move on.

**Mistakes:**
- Reporting PR-AUC without the positive rate — 0.6 means opposite things at
  1% vs. 40% prevalence.
- Using ROC-AUC as the *only* metric for fraud/disease/rare-event problems.
- Interpolating the PR curve linearly between points (optimistic); use the
  standard AP computation.

### Threshold selection: turning scores into decisions

:::tldr
The model outputs scores; the *product* needs decisions. The threshold is
chosen from costs, not from the model: pick the point on the PR/ROC curve
that maximizes expected utility, or the best precision subject to a recall
floor the business sets. 0.5 is a default, not a decision.
:::

**30-second answer:** Three legitimate ways: **(1)** cost-based — threshold
where marginal precision equals the cost ratio
$\tfrac{\text{cost(FP)}}{\text{cost(FN)}}$; **(2)** constraint-based — "recall
≥ 0.9" (compliance/fraud), then maximize precision; **(3)** F1-max — the
threshold maximizing F1 on validation, the defensible default with no cost
model. All tuned on validation, never test.

**Interview-depth:** the cost-based rule falls out of expected utility: flag
when $P(\text{pos}\mid x) \cdot \text{cost(FN)} > (1-P) \cdot
\text{cost(FP)}$. Note this needs *calibrated* probabilities — an
uncalibrated model's "0.7" isn't 70%, so cost-based thresholding on raw
scores misfires (see calibration below). In practice most teams use the
constraint form because businesses state floors ("catch 95% of fraud"),
not cost ratios. **Revisit cadence:** thresholds decay — retune on a schedule
or when the positive rate drifts; a threshold tuned on last quarter's
traffic is a silent regression.

**Follow-ups:**
- "Why not just use 0.5?" → 0.5 is optimal only for balanced classes with
  symmetric costs — roughly never in production. It's the absence of a
  decision disguised as one.
- "Threshold for a ranking model?" → rankers usually don't threshold for
  ordering, but the *retrieval* stage does (score cutoff for candidate
  generation) — tuned on Recall@K, not precision.

### Regression metrics: MAE, RMSE, R²

:::tldr
MAE = average absolute miss (robust, speaks in the unit of the target);
RMSE = square-root of average squared miss (punishes big errors, same units);
R² = fraction of variance explained (1 = perfect, 0 = "just predict the
mean"). Pick by how the business prices errors: linearly → MAE,
superlinearly → RMSE.
:::

**30-second answer:** For targets $y$ and predictions $\hat y$:
$$\text{MAE} = \tfrac{1}{n}\sum|y-\hat y|, \quad
\text{RMSE} = \sqrt{\tfrac{1}{n}\sum(y-\hat y)^2}, \quad
R^2 = 1 - \tfrac{\sum(y-\hat y)^2}{\sum(y-\bar y)^2}$$
MAE's minimizer is the conditional *median*; MSE/RMSE's is the conditional
*mean* — so MAE shrugs off outliers while RMSE chases them.

**Interview-depth — choosing:** **MAE** when every unit of error costs the
same (ETA minutes, price dollars) and you don't want a few wild outliers
driving the model — it's robust and directly interpretable ("off by $12 on
average"). **RMSE** when large errors are disproportionately bad (a 60-minute
ETA miss ruins the delivery, six 10-minute misses don't) — the squaring makes
the optimizer care about the tail. **R²** for communicating fit quality to
non-technical stakeholders ("explains 83% of the variance"), and as a
scale-free comparator — but it can be *negative* (worse than predicting the
mean) and it rewards fitting the bulk while hiding tail behavior, so never
use it alone. **MAPE** (mean absolute *percentage* error) looks intuitive but
is asymmetric (penalizes over-prediction more) and explodes near zero
targets — mention it only to say why you avoid it.

**Follow-ups:**
- "RMSE went down but the product got worse?" → the model traded many small
  errors for a few catastrophic ones, or the error distribution shifted
  (check MAE alongside — if MAE rose while RMSE fell, the tail got worse).
  Report both, always.
- "R² of 0.99 — celebrate?" → check for leakage first: near-perfect R² on a
  real problem usually means the target (or a proxy) leaked into the
  features. Also check it's computed out-of-sample.
- "Why does minimizing MSE give the mean?" → $\arg\min_c \mathbb{E}[(y-c)^2]
  = \mathbb{E}[y]$; for MAE, $\arg\min_c \mathbb{E}|y-c|$ = median. One-line
  derivation each — worth having cold.

**Mistakes:**
- Reporting RMSE without units/context — "RMSE 4.2" is meaningless until
  you know the target's scale; pair it with MAE or a naive baseline.
- Using MAPE with zero/near-zero targets.
- Forgetting R² needs a *held-out* set — in-sample R² always flatters.

### Calibration: do the probabilities mean what they say?

:::tldr
A model can rank perfectly (AUC 1.0) while its probabilities are garbage
(everything scored 0.51/0.49). Calibration — "of the times I said 70%, did
it happen 70% of the time" — is what makes scores usable for thresholding,
bidding, and combining models. Measure with reliability diagrams / ECE;
fix with temperature scaling or isotonic regression on held-out data.
:::

**30-second answer:** Bin predictions by confidence (0.6–0.7, 0.7–0.8, …),
plot mean predicted probability vs. actual positive rate per bin — that's the
reliability diagram; perfect calibration is the diagonal. ECE (expected
calibration error) = average absolute gap, weighted by bin size. CE-trained
deep nets are systematically *overconfident*; temperature scaling (divide
logits by $T>1$, tuned on validation) is the one-parameter fix that keeps
accuracy identical.

**Interview-depth:** **Ranking ≠ calibration:** AUC only cares about order,
so a model can separate classes perfectly yet output unusable probabilities.
**When it matters:** anywhere a probability feeds a decision — ad bidding
(bid = pCTR × value), cost-based thresholding (above), model blending,
fraud review prioritization. **When it doesn't:** pure ranking products
(search order) where only relative scores matter. **Isotonic regression**
(non-parametric, more flexible) vs. **Platt/temperature scaling**
(parametric, less data-hungry): use temperature when you have little
calibration data, isotonic when you have plenty. Always fit on held-out data
— calibrating on train is self-deception.

**Follow-ups:**
- "High AUC but bad business metric — calibration?" → it's on the checklist:
  if downstream thresholds/bids were set assuming calibrated scores, an
  overconfident model systematically overbids/over-flags.
- "Does label smoothing help calibration?" → yes — it caps overconfidence
  during training, a rare case where a training trick directly improves
  calibration.

### Choosing metrics: the decision table

:::tldr
The metric is a business decision disguised as math: match it to what the
product *does* with the output and what failure costs. When in doubt, report
a pair (one threshold-free, one at the operating point) — never a single
number without its context.
:::

| Situation | Reach for | Avoid |
|---|---|---|
| Balanced binary classification | Accuracy, F1, ROC-AUC | — |
| Rare positives you must catch (fraud, disease) | PR-AUC, recall at fixed precision | Accuracy, ROC-AUC alone |
| False alarms expensive (spam, ads) | Precision at fixed recall, PR-AUC | Recall alone |
| Search / feed ranking | NDCG@K (K = viewport) | Accuracy, AUC |
| Candidate retrieval (two-tower) | Recall@K, K large (100–1000) | NDCG@10 |
| One right answer (Q&A, navigational) | MRR | MAP/NDCG |
| Regression, errors cost linearly | MAE | RMSE (outlier-driven) |
| Regression, big misses costly | RMSE (+ MAE alongside) | R² alone |
| Scores feed bids/thresholds/blends | ECE / calibration + a ranking metric | AUC alone |
| Multi-class, balanced | Accuracy, macro-F1 | — |
| Multi-class, imbalanced | Macro-F1, per-class PR | Accuracy, micro-F1 alone |

**The interview answer pattern:** "I'd pick *X* because the product does *Y*
with the output and a false *Z* costs *W*; I'd also track *X′* as a guardrail
because *X* is blind to *V*." Concrete: "PR-AUC as primary because fraud is
1% and misses cost 100× false alarms; recall-at-95%-precision as the
operating metric the business signs off on; calibration (ECE) as guardrail
because scores feed the review-queue prioritizer." That sentence structure —
metric, product reason, cost reason, guardrail — is what "how do you choose
metrics" is really testing.

**Follow-ups:**
- "One metric to rule them all?" → there isn't one; anyone selling a single
  metric is selling Goodhart's law. Report a small suite: one threshold-free,
  one at the operating point, one guardrail.
- "Offline metric improved, online didn't — ?" → the offline/online gap
  checklist from ranking metrics: label staleness, position/selection bias,
  head/tail skew, novelty effects, or the gain is within noise (check
  significance, not just the point estimate).

**Mistakes:**
- Letting the metric choose the product instead of the reverse ("our AUC
  went up" while the business metric flatlines).
- Single-metric reporting without the operating context (threshold, K,
  prevalence, grade distribution).
- Changing the metric mid-project to make results look better — pick it from
  the product requirements *before* modeling, and write down why.

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

### Metric tradeoffs by use case: five worked scenarios

:::tldr
Every metric choice trades what you reward against what you go blind to.
The interview-ready move for any scenario: name the primary metric, say what
it rewards, name its blind spot, and pair it with a guardrail metric that
covers the blind spot. One metric never survives contact with the product.
:::

**1. Fraud detection — 0.1% positives, a miss costs 100× a false alarm.**
Candidates: ROC-AUC, PR-AUC, recall@95%-precision, F2.
- **ROC-AUC** rewards overall ranking across all thresholds. Blind to the
  operating region: 0.97 AUC can coexist with 5% precision at the threshold
  you'd actually ship, because FPR's TN denominator swallows false alarms.
- **PR-AUC** rewards holding precision while catching more fraud — honest
  under imbalance. Blind to the exact operating point: two models with equal
  PR-AUC can need very different thresholds to be usable.
- **recall@fixed-precision** rewards the business contract ("catch 90% of
  fraud without growing the review queue"). Blind to everything outside that
  point — and gameable by nudging the threshold.
- **Pick:** PR-AUC for model selection (threshold-free), recall@95%-precision
  as the launch gate the business signs off on. **Guardrail:** review-queue
  precision drift week-over-week — catches prior/label shift that static
  metrics miss.

**2. Search ranking — graded relevance, users rarely scroll past 10.**
Candidates: NDCG@10, NDCG@100, MAP, MRR, Recall@1000.
- **NDCG@10** rewards the best docs in the visible viewport, grade-weighted.
  Blind to tail coverage: a model can ace @10 by memorizing head queries
  while the tail rots.
- **Recall@1000 / NDCG@100** rewards coverage for downstream stages. Blind to
  user-visible quality: optimizing @1000 can promote clickbaity
  near-relevant docs.
- The deeper tradeoff is **cross-stage**: the retrieval stage must optimize
  Recall@K with large K because the ranker reorders anyway; the ranking stage
  optimizes NDCG@K with K = viewport. Optimizing retrieval on NDCG@10
  starves the ranker of candidates it could have ordered well — the most
  common stage-metric mismatch in production search.
- **Pick:** NDCG@10 primary for the ranker, Recall@1000 guardrail for
  retrieval. **Slice both by head/torso/tail** — aggregate NDCG hides tail
  regressions behind head wins.

**3. Spam filter — a false positive (legit mail in spam) is the catastrophe.**
Candidates: precision@90%-recall, F0.5, PR-AUC, accuracy.
- **Accuracy** rewards nothing: 99.9% legit mail means "flag nothing" scores
  99.9%. Mention it only to dismiss it.
- **precision@fixed-recall** rewards the actual user pain (inbox cleanliness
  at an acceptable catch rate). Blind to recall collapse: 99.99% precision
  is trivial if you catch almost nothing.
- **F0.5** (β=0.5) rewards precision-weighted balance in a single number for
  model selection. Blind to the absolute operating point the product ships.
- **Pick:** F0.5 or PR-AUC for selection, precision@90%-recall as the ship
  gate. **Guardrail:** FP rate on a held-out sample of *important* mail —
  false positives aren't uniform; one missed job offer outweighs ten missed
  newsletters, so weight the eval set accordingly.

**4. ETA / price regression — most errors small, a few catastrophic.**
Candidates: MAE, RMSE, MAPE, R².
- **MAE** rewards typical-case accuracy and shrugs off outliers. Blind to the
  tail: usually off by 2 min but sometimes 60 looks great on MAE — and loses
  customers.
- **RMSE** rewards tail discipline; the squaring forces the optimizer to care
  about big misses. Blind to interpretability under skew: one bad segment can
  dominate the number while the typical experience is fine.
- The tradeoff *is* the business's error cost curve: linear cost → MAE;
  superlinear (one 60-min miss loses the customer, six 10-min misses don't)
  → RMSE.
- **Pick:** optimize RMSE, always report MAE alongside. If MAE improves while
  RMSE worsens, your tail is rotting — that divergence is the guardrail.
  Never MAPE near zero targets (asymmetric, explodes).

**5. Multi-class, imbalanced — e.g., ticket routing over 50 categories.**
Candidates: accuracy, micro-F1, macro-F1, per-class PR.
- **Accuracy / micro-F1** rewards head-class performance — dominated by
  frequent classes. A model ignoring 40 rare categories can still score 90%.
- **Macro-F1** rewards every class equally — punishes ignoring the tail.
  Blind to business importance: not all rare classes matter equally.
- **Pick:** macro-F1 for selection (forces tail coverage), per-class
  precision/recall table for the launch review so stakeholders see *which*
  classes fail. **Guardrail:** worst-class recall — the min, not the mean, is
  what users in that segment actually experience.

**The meta-pattern — say this verbatim in the interview:** "No single metric
survives contact with the product. I pick a primary metric matching the
decision the product makes, a threshold-free metric for model selection, and
a guardrail for what the primary is blind to — and I re-derive the choice
whenever the cost structure changes." Then one line of Goodhart's law: once
the team bonuses on NDCG@10, expect rank-10 gaming — which is exactly why the
guardrail exists.

**Mistakes:**
- Using one metric for both model selection and launch gating. Selection
  wants threshold-free (PR-AUC, NDCG); gating wants the operating point
  (recall@precision, NDCG@10 at the ship threshold). Different jobs, different
  metrics.
- Copying the metric from a paper benchmark instead of deriving it from the
  product's cost structure.
- Averaging metrics across segments with wildly different base rates without
  slicing — the aggregate will lie to you.

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
- [ ] Sketch a PR curve from 5 scored examples by hand; mark where the random
  baseline sits and explain why PR-AUC beats ROC-AUC at 1% prevalence.
- [ ] "Fraud team, 1% positives, a miss costs 100x a false alarm" — name your
  primary metric, operating-point metric, and guardrail, each with one
  sentence of justification (use the decision-table pattern).
- [ ] 60 seconds each, out loud: primary + guardrail metrics for (a) fraud at
  0.1% positives, (b) a spam filter where false positives are catastrophic,
  (c) ETA regression with occasional catastrophic misses. Name what each
  primary metric is blind to.
- [ ] Whiteboard pairwise (RankNet) loss and explain when you'd switch to
  LambdaRank-style $|\Delta\text{NDCG}|$ weighting.
- [ ] Diagnose: train NDCG 0.81, val NDCG 0.62, both flat with more data.
  Write the 3-sentence diagnosis and fix plan. (Answer: variance problem
  that more data isn't fixing → regularization/augmentation, or label
  noise; check head/tail slices.)
- [ ] Explain AdamW vs Adam in one sentence, then derive where the L2 term
  goes in each update.

[Previous: project deep-dive](#/project-deep-dive) · [Next: deep learning →](#/deep-learning)
