---
title: "Coding — ML-Relevant Python Exercises"
slug: "coding"
section: "coding"
nav_order: 1
nav_label: "Coding"
tags: ["coding", "python", "ml-coding", "numpy", "interview-prep"]
updated: "2026-10-01"
---

## TL;DR

MLE coding rounds test two things: **can you manipulate data structures under
time pressure**, and **can you implement the math you claim to understand**.
Every problem here is ML/AI-relevant — no binary-tree golf for its own sake.
For each problem, run the 8-step loop below out loud; interviewers score the
loop as much as the code.

:::tldr
The 8-step loop per problem: **QUESTION** (restate) → **CLARIFY** (2–3
questions) → **APPROACH** (say it before you write it) → **CODE** (clean,
runnable) → **TESTS** (hand-run on 2–3 cases incl. edge) → **COMPLEXITY**
(time + space) → **FOLLOW-UPS** (answer one proactively) → **COMMON BUGS**
(name yours before they do).
:::

## Interview answer

When the problem lands: restate it in one sentence, ask your clarifying
questions (input sizes? streaming or batch? mutability? precision
requirements?), state the approach and its complexity *before* touching the
keyboard, then write the simplest correct code first. Optimize only if asked.
For numpy/torch problems, narrate shapes at every step — shape bugs are where
ML coding rounds are won and lost.

## Intuition

MLE interviewers use coding as a **truth serum for the resume**. "Led
retrieval ranking" → implement top-K merge. "Built training pipelines" →
write the batching sampler. "Works on LLMs" → implement attention from
scratch. The problems below are chosen to map 1:1 onto resume claims — if you
can hand-write each solution cold, your deep-dive round gets much easier.

Two meta-skills carry every problem: **invariants** (what stays true at each
loop iteration — say it) and **shapes** (for tensor code, annotate every
transformation).

## Details

Level guide: **Warm-up** (10–15 min, should be automatic) · **Interview**
(25–35 min, the real thing) · **Hard** (35–45 min, staff bar / follow-up
depth). Do them in order; don't skip the warm-ups — they're the patterns the
harder problems compose.

:::collapse How to use this page
Read the QUESTION, close the page, and solve on paper/whiteboard using the
8-step loop. Then compare against the posted solution — not for the code, but
for the clarifying questions and follow-ups you missed. Track completion with
the checkboxes in [Practice](#practice).
:::

---

## Warm-up

### W1. Top-K frequent queries in a search log

**QUESTION.** Given a stream (list) of search query strings, return the K most
frequent. Ties broken arbitrarily.

**CLARIFY.** How large is K relative to N? (K small → heap; K ~ N → sort.)
Streaming or one-shot list? (One-shot here; streaming variant in follow-ups.)
Case sensitivity? (Assume exact match; note normalization as a real-world
step.)

**APPROACH.** Count with a hash map, then keep a min-heap of size K keyed by
count. O(N log K) time, O(N) space for counts.

**CODE.**

```python
import heapq
from collections import Counter

def top_k_queries(queries: list[str], k: int) -> list[tuple[str, int]]:
    if k <= 0:
        return []
    counts = Counter(queries)
    # min-heap of (count, query); smallest count at top, evicted past k
    heap: list[tuple[int, str]] = []
    for q, c in counts.items():
        heapq.heappush(heap, (c, q))
        if len(heap) > k:
            heapq.heappop(heap)
    return [(q, c) for c, q in sorted(heap, reverse=True)]  # descending by count
```

**TESTS.** `top_k_queries(["a","b","a","c","b","a"], 2)` →
`[('a',3),('b',2)]`. `k=0` → `[]`. `k > distinct` → all, sorted.

**COMPLEXITY.** Time O(N log K), space O(N) for the counter (heap is O(K)).

**FOLLOW-UPS.** True streaming with limited memory? → Count-Min Sketch +
min-heap ("heavy hitters"). Distributed logs? → map-side top-K, reduce-side
merge (each shard sends its local top-K; exact iff K covers the skew —
discuss approximation).

**COMMON BUGS.** Max-heap via negation and forgetting to flip back; pushing
all N then heapifying (O(N log N), fine but say why you didn't); tie-breaking
nondeterminism confusing the test.

### W2. Sliding-window rate limiter

**QUESTION.** Implement a rate limiter allowing at most `R` requests per
`W`-second sliding window per user.

**CLARIFY.** Per-user or global? (Per-user key.) What should happen on
exceed — reject or queue? (Reject with retry-after.) Clock source?
(Monotonic.)

**APPROACH.** Per user, keep a deque of request timestamps; on each request,
evict timestamps older than `now - W`; allow iff `len(deque) < R`. Invariant:
deque always holds exactly the requests inside the window, in order.

**CODE.**

```python
import time
from collections import deque, defaultdict

class SlidingWindowLimiter:
    def __init__(self, max_requests: int, window_s: float):
        self.R, self.W = max_requests, window_s
        self.hits: dict[str, deque[float]] = defaultdict(deque)

    def allow(self, user: str, now: float | None = None) -> bool:
        now = time.monotonic() if now is None else now
        q = self.hits[user]
        cutoff = now - self.W
        while q and q[0] <= cutoff:      # evict stale; invariant restored
            q.popleft()
        if len(q) >= self.R:
            return False
        q.append(now)
        return True
```

**TESTS.** R=2, W=60: allow, allow, reject at t=0,0,0; allow at t=61.
Boundary: request exactly at `now - W` is evicted (`<=`).

**COMPLEXITY.** Amortized O(1) per request (each timestamp pushed/popped
once); space O(R) per user.

**FOLLOW-UPS.** Distributed? → Redis sorted-set per user, ZREMRANGEBYSCORE +
ZCARD, or token bucket (see H3). Burst vs. smooth? → sliding window allows
R-sized bursts; token bucket smooths.

**COMMON BUGS.** Using `time.time()` (clock jumps); `deque` shared across
users; off-by-one on the window edge; unbounded memory when users are
one-shot (add TTL/eviction of idle users).

### W3. LRU cache for embeddings

**QUESTION.** Implement an LRU cache with `get`/`put`, capacity C — the shape
of a feature/embedding cache in front of a model server.

**CLARIFY.** Thread safety needed? (Note it; implement single-threaded, guard
with a lock in follow-up.) Eviction callback? (Note as extension.)

**APPROACH.** Hash map + doubly-linked list; `OrderedDict` gives both in one.
Invariant: iteration order = LRU → MRU; `get`/`put` move the key to MRU.

**CODE.**

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.d: OrderedDict[str, list[float]] = OrderedDict()

    def get(self, key: str) -> list[float] | None:
        if key not in self.d:
            return None
        self.d.move_to_end(key)          # MRU
        return self.d[key]

    def put(self, key: str, vec: list[float]) -> None:
        if key in self.d:
            self.d.move_to_end(key)
        self.d[key] = vec
        if len(self.d) > self.cap:
            self.d.popitem(last=False)   # evict LRU
```

**TESTS.** cap=2: put a,b; get a; put c → b evicted; get b → None.

**COMPLEXITY.** O(1) get/put, O(C) space.

**FOLLOW-UPS.** Make it thread-safe → `threading.Lock` around both methods
(or sharded locks). TTL per entry? → store `(vec, expiry)`, lazy-evict on
access. Why not `functools.lru_cache`? → no per-key TTL, unbounded key risk,
not size-aware (vectors differ in bytes).

**COMMON BUGS.** Forgetting `move_to_end` on `get` (then it's FIFO, not LRU);
evicting before insert vs. after; `popitem(last=True)` evicting the MRU.

### W4. Numerically stable softmax

**QUESTION.** Implement softmax over a 1-D numpy array, numerically stable.

**CLARIFY.** Axis? (1-D here; note axis param for batched.) dtype? (float64
accumulation, cast back.)

**APPROACH.** Subtract the max before exponentiating — the shift trick. Say
why: `exp(1000)` overflows float32/float64; shifting is exact because softmax
is translation-invariant.

**CODE.**

```python
import numpy as np

def softmax(logits: np.ndarray) -> np.ndarray:
    x = np.asarray(logits, dtype=np.float64)
    z = x - x.max()                 # shift trick: softmax(x) == softmax(x - c)
    e = np.exp(z)                   # now max(e) == 1, no overflow
    return e / e.sum()
```

**TESTS.** `softmax([1000, 1001, 1002])` ≈ `[0.09, 0.24, 0.67]`, sums to 1,
no inf. `softmax([-1000]*3)` → uniform (underflow to 0/0? check: z = 0s, e
= 1s → uniform — good, state why).

**COMPLEXITY.** O(N) time, O(N) space.

**FOLLOW-UPS.** Batched with temperature: `softmax(logits / T, axis=-1)` —
see H4 for top-p. Log-softmax for NLL stability: `z - logsumexp(z)`.

**COMMON BUGS.** Forgetting the shift (overflow on real logits); dividing by
`e.sum()` computed in float32; using it on already-softmaxed probs.
---

## Interview level

### I1. Merge K sorted posting lists (top-K retrieval merge)

**QUESTION.** K sorted lists of `(doc_id, score)` (descending by score).
Return the global top-K by score. This is the merge step of distributed
retrieval — each shard returns its local top-K.

**CLARIFY.** Sorted descending? (Yes.) Duplicate doc_ids across lists? (Assume
deduped upstream; note it.) K vs. total N? (K small.)

**APPROACH.** K-way merge with a max-heap over list heads: push head of each
list, pop max, advance that list. Stop after K pops. Invariant: heap always
holds the current best un-emitted element of each list.

**CODE.**

```python
import heapq

def merge_top_k(lists: list[list[tuple[int, float]]], k: int
                ) -> list[tuple[int, float]]:
    # max-heap via negated score; entry: (-score, list_idx, pos)
    heap: list[tuple[float, int, int]] = []
    for i, lst in enumerate(lists):
        if lst:
            doc, s = lst[0]
            heapq.heappush(heap, (-s, i, 0))
    out: list[tuple[int, float]] = []
    while heap and len(out) < k:
        neg_s, i, pos = heapq.heappop(heap)
        doc, s = lists[i][pos]
        out.append((doc, s))
        if pos + 1 < len(lists[i]):
            d2, s2 = lists[i][pos + 1]
            heapq.heappush(heap, (-s2, i, pos + 1))
    return out
```

**TESTS.** `[[(1,.9),(2,.5)],[(3,.8)],[]]`, k=2 → `[(1,.9),(3,.8)]`.
k larger than total → all, still sorted. Empty input → `[]`.

**COMPLEXITY.** Time O(K log L) for L lists (+O(L) setup); space O(L).

**FOLLOW-UPS.** This is exact top-K from per-shard top-K only if shards return
enough depth — in practice shards return top-K' > K or you accept
approximation; name the trade. Duplicates? → track seen doc_ids, skip.

**COMMON BUGS.** Forgetting the list index in the heap tuple (can't advance);
comparing tuples with unorderable payloads (put score first); min-heap used
as max without negation.

### I2. K-means (numpy, Lloyd's algorithm)

**QUESTION.** Implement k-means clustering: given X (n, d) and k, return
centroids and assignments.

**CLARIFY.** Init? (k-means++ preferred; random-choice acceptable, note
sensitivity.) Empty clusters? (Reinit to a random point — state the policy.)
Convergence? (Assignments stop changing or max_iters.)

**APPROACH.** Lloyd's iteration: assign each point to nearest centroid
(broadcasted squared distances), recompute centroids as means. Shapes:
X (n,d), C (k,d) → dists (n,k).

**CODE.**

```python
import numpy as np

def kmeans(X: np.ndarray, k: int, max_iters: int = 100, seed: int = 0):
    rng = np.random.default_rng(seed)
    n, d = X.shape
    # k-means++ seeding
    centroids = np.empty((k, d))
    centroids[0] = X[rng.integers(n)]
    for j in range(1, k):
        d2 = ((X[:, None, :] - centroids[:j][None, :, :]) ** 2).sum(-1).min(1)
        probs = d2 / d2.sum()
        centroids[j] = X[rng.choice(n, p=probs)]
    assign = np.zeros(n, dtype=int)
    for _ in range(max_iters):
        d2 = ((X[:, None, :] - centroids[None, :, :]) ** 2).sum(-1)  # (n, k)
        new_assign = d2.argmin(1)
        if np.array_equal(new_assign, assign) and _ > 0:
            break
        assign = new_assign
        for j in range(k):
            pts = X[assign == j]
            centroids[j] = pts.mean(0) if len(pts) else X[rng.integers(n)]
    return centroids, assign
```

**TESTS.** Two well-separated blobs (n=200, d=2) → assignments recover blobs
(check adjusted Rand or just visual means); k=1 → centroid = data mean.

**COMPLEXITY.** O(n·k·d) per iteration; O(n·k) temp memory for distances.

**FOLLOW-UPS.** Why k-means++? (O(log k) approximation guarantee vs.
arbitrary bad local minima.) High-d / large-n? → mini-batch k-means. Empty
cluster policy alternatives? (Drop the centroid; split the largest cluster.)

**COMMON BUGS.** Broadcasting shape error in distances — narrate
`(n,1,d)-(1,k,d)→(n,k,d)`; `argmin` on wrong axis; infinite loop from
oscillating assignments (the `_ > 0` guard); NaN when a cluster empties and
you take mean of nothing.

### I3. Logistic regression with gradient descent (numpy)

**QUESTION.** Binary logistic regression: implement `fit` (full-batch GD) and
`predict_proba` on X (n, d), y ∈ {0,1}.

**CLARIFY.** Include bias? (Yes — augment X with ones, or separate b; pick
augment and say so.) Regularization? (Note L2 as follow-up.) Stopping? (Fixed
iters + lr; note line search / Adam as production.)

**APPROACH.** Sigmoid hypothesis, binary cross-entropy loss; gradient is
`Xᵀ(σ(Xw) − y)/n`. Vectorize everything; shapes: X (n,d+1), w (d+1,).

**CODE.**

```python
import numpy as np

def sigmoid(z: np.ndarray) -> np.ndarray:
    # stable: avoid overflow for large negative z
    out = np.empty_like(z, dtype=np.float64)
    pos = z >= 0
    out[pos] = 1 / (1 + np.exp(-z[pos]))
    ez = np.exp(z[~pos])
    out[~pos] = ez / (1 + ez)
    return out

def fit_logreg(X: np.ndarray, y: np.ndarray, lr: float = 0.1,
               iters: int = 1000) -> np.ndarray:
    n = X.shape[0]
    Xa = np.hstack([X, np.ones((n, 1))])       # bias term; w: (d+1,)
    w = np.zeros(Xa.shape[1])
    for _ in range(iters):
        p = sigmoid(Xa @ w)                    # (n,)
        grad = Xa.T @ (p - y) / n              # (d+1,)
        w -= lr * grad
    return w

def predict_proba(X: np.ndarray, w: np.ndarray) -> np.ndarray:
    Xa = np.hstack([X, np.ones((X.shape[0], 1))])
    return sigmoid(Xa @ w)
```

**TESTS.** Linearly separable 2-D data → train accuracy ~100%, loss
decreases monotonically (assert `losses[-1] < losses[0]`). All y=0 →
probabilities → 0.

**COMPLEXITY.** O(iters·n·d) time, O(n·d) space.

**FOLLOW-UPS.** Add L2: `grad += λw` (don't regularize bias — say why).
Class imbalance? → sample weights in the gradient. Why not accuracy as the
training objective? (Non-differentiable; CE is the proper scoring rule.)

**COMMON BUGS.** Forgetting the bias column; `y` as int causing integer
division in old numpy habits; unstable sigmoid overflowing on `exp(-z)`;
gradient sign error (ascent instead of descent — the loss curve catches it).

### I4. Cross-entropy loss from scratch (multi-class)

**QUESTION.** Given logits (n, C) and integer labels (n,), compute mean
softmax cross-entropy — and its gradient w.r.t. logits.

**CLARIFY.** Reduction? (Mean.) Label smoothing? (Note as follow-up.)

**APPROACH.** Log-softmax via the shift trick, then NLL = −mean(log p of true
class). Gradient of CE w.r.t. logits is the famous `p − onehot(y)` over n —
derive it if asked; at minimum state it.

**CODE.**

```python
import numpy as np

def cross_entropy(logits: np.ndarray, labels: np.ndarray):
    n = logits.shape[0]
    z = logits - logits.max(axis=1, keepdims=True)   # (n, C), shift trick
    logsumexp = np.log(np.exp(z).sum(axis=1))        # (n,)
    logp = z - logsumexp[:, None]                    # log-softmax (n, C)
    loss = -logp[np.arange(n), labels].mean()
    # dL/dlogits = (softmax - onehot) / n
    grad = np.exp(logp)
    grad[np.arange(n), labels] -= 1
    grad /= n
    return loss, grad
```

**TESTS.** Gradient check vs. finite differences (`np.allclose` with
eps=1e-5). Perfect predictions (logit 10 on true class) → loss ≈ 0.
Uniform logits → loss = ln(C).

**COMPLEXITY.** O(n·C) time and space.

**FOLLOW-UPS.** Label smoothing: target becomes `(1−ε)·onehot + ε/C`; how
does the gradient change? (Same formula with smoothed target.) Class weights?
→ weight the per-sample loss.

**COMMON BUGS.** `logits.max(axis=1)` without `keepdims` (broadcast error);
forgetting `/n` in the gradient; computing softmax then log (underflow) —
always log-softmax first.

### I5. LayerNorm (numpy)

**QUESTION.** Implement LayerNorm over the last dimension, with learnable
γ, β and epsilon.

**CLARIFY.** Which axis? (Last — per-token in transformers.) Elementwise
affine? (Yes, γ/β.)

**APPROACH.** μ, σ² over last dim with keepdims; normalize; scale/shift.
Shapes: x (..., d), μ (..., 1).

**CODE.**

```python
import numpy as np

def layernorm(x: np.ndarray, gamma: np.ndarray, beta: np.ndarray,
              eps: float = 1e-5) -> np.ndarray:
    mu = x.mean(axis=-1, keepdims=True)              # (..., 1)
    var = ((x - mu) ** 2).mean(axis=-1, keepdims=True)
    xhat = (x - mu) / np.sqrt(var + eps)
    return gamma * xhat + beta                        # broadcast over ...
```

**TESTS.** Random (4, 8): output has ~zero mean / unit variance per row
*before* affine (test with γ=1, β=0). Constant row → output = β (var=0, eps
saves the division).

**COMPLEXITY.** O(N·d) time, O(N·d) space.

**FOLLOW-UPS.** LayerNorm vs. BatchNorm? (LN: per-sample, no batch dependence
→ right for variable-length sequences and small batches; BN: batch stats,
train/test mismatch.) RMSNorm? (Drop mean-centering: `x / rms(x) * γ` —
cheaper, used in LLaMA.) Backward pass? (Derive: gradient flows through μ
and σ² — a good whiteboard follow-up.)

**COMMON BUGS.** `keepdims=False` → broadcast crash; eps inside vs. outside
sqrt (convention: inside); normalizing over the wrong axis (batch dim).

### I6. Scaled dot-product attention (single head)

**QUESTION.** Implement `attention(Q, K, V, mask=None)`: Q (n, dk), K (m,
dk), V (m, dv).

**CLARIFY.** Causal mask? (Optional param; support additive −inf mask.)
Scaling? (1/√dk — and be ready to say why.)

**APPROACH.** Scores = QKᵀ/√dk → masked softmax over keys → @V. Narrate
shapes: (n,m) → (n,m) → (n,dv).

**CODE.**

```python
import numpy as np

def attention(Q: np.ndarray, K: np.ndarray, V: np.ndarray,
              mask: np.ndarray | None = None) -> np.ndarray:
    dk = Q.shape[-1]
    scores = Q @ K.T / np.sqrt(dk)          # (n, m)
    if mask is not None:
        scores = scores + mask              # additive: 0 / -inf
    z = scores - scores.max(axis=-1, keepdims=True)
    w = np.exp(z)
    w = w / w.sum(axis=-1, keepdims=True)   # softmax over keys
    return w @ V                            # (n, dv)
```

**TESTS.** With V = one-hot-ish rows, output ≈ convex combo of the right
rows. Causal mask (−inf upper triangle) on identity-ish QKᵀ → lower-triangular
weights. Row sums of w = 1.

**COMPLEXITY.** O(n·m·dk + n·m·dv) time, O(n·m) for the weight matrix.

**FOLLOW-UPS.** Why √dk? (Dot-product variance grows with dk; without scaling
softmax saturates → vanishing gradients.) Memory for long sequences? → the
(n,m) matrix is the bottleneck: FlashAttention tiles it; state the idea
(online softmax, never materialize the full matrix).

**COMMON BUGS.** Softmax over the wrong axis (queries instead of keys);
forgetting the scale; mask applied as multiplication by 0/1 instead of
additive −inf (leaks uniform weight); shape mismatch QKᵀ vs KQᵀ.

### I7. Multi-head attention (numpy)

**QUESTION.** Extend I6: h heads, d_model, with Q/K/V/O projections.

**CLARIFY.** d_model divisible by h? (Assume yes; assert it.) Biases?
(Skip; note.)

**APPROACH.** Project → split heads → per-head attention → concat → output
projection. Reshape discipline: (b, n, d) → (b, n, h, dh) → (b, h, n, dh).

**CODE.**

```python
import numpy as np

def split_heads(x: np.ndarray, h: int) -> np.ndarray:
    b, n, d = x.shape
    dh = d // h
    return x.reshape(b, n, h, dh).transpose(0, 2, 1, 3)  # (b,h,n,dh)

def merge_heads(x: np.ndarray) -> np.ndarray:
    b, h, n, dh = x.shape
    return x.transpose(0, 2, 1, 3).reshape(b, n, h * dh)

def mha(X: np.ndarray, Wq, Wk, Wv, Wo, h: int,
        mask: np.ndarray | None = None) -> np.ndarray:
    b, n, d = X.shape
    assert d % h == 0
    dh = d // h
    Q, K, V = X @ Wq, X @ Wk, X @ Wv          # (b,n,d)
    Q, K, V = split_heads(Q, h), split_heads(K, h), split_heads(V, h)
    scores = Q @ K.transpose(0, 1, 3, 2) / np.sqrt(dh)   # (b,h,n,n)
    if mask is not None:
        scores = scores + mask
    z = scores - scores.max(axis=-1, keepdims=True)
    w = np.exp(z)
    w = w / w.sum(axis=-1, keepdims=True)
    ctx = w @ V                               # (b,h,n,dh)
    return merge_heads(ctx) @ Wo              # (b,n,d)
```

**TESTS.** h=1 reduces to I6 (compare outputs). Permutation-equivariance:
shuffling input order shuffles output identically (no mask). Output shape
(b, n, d).

**COMPLEXITY.** O(b·n²·d) time (attention dominates), O(b·h·n²) weights.

**FOLLOW-UPS.** Why multiple heads? (Subspaces: different heads learn
different relation types; single head forces one relation per position pair.)
KV-cache for decoding? (Cache K/V per layer; decode is O(n) per step, not
O(n²).) GQA/MQA? (Share K/V across heads to shrink the cache.)

**COMMON BUGS.** Transpose order in split/merge (silent wrong results —
always test h=1 equivalence); scaling by √d instead of √dh; mask shape not
broadcastable to (b,h,n,n).

### I8. Reservoir sampling (streaming training-data sampler)

**QUESTION.** Sample k items uniformly from a stream of unknown length, one
pass, O(k) memory. (Downsampling a firehose for training-data curation.)

**CLARIFY.** Uniform over the stream? (Yes.) k vs. stream length? (k fixed,
stream longer.)

**APPROACH.** Fill reservoir with first k; item i (1-indexed) replaces a
random reservoir slot with probability k/i. Invariant: after seeing i items,
each is in the reservoir with probability min(1, k/i).

**CODE.**

```python
import random

def reservoir_sample(stream, k: int, seed: int = 0) -> list:
    rng = random.Random(seed)
    res: list = []
    for i, item in enumerate(stream, start=1):
        if len(res) < k:
            res.append(item)
        else:
            j = rng.randrange(i)      # 0..i-1
            if j < k:
                res[j] = item
    return res
```

**TESTS.** Statistical: stream 0..9999, k=100, repeat → each index appears
≈1% of the time (χ² or eyeball the histogram). k ≥ stream length → returns
all items.

**COMPLEXITY.** O(N) time, O(k) space, one pass.

**FOLLOW-UPS.** Weighted reservoir (Efraimidis–Spirakis: key = u^(1/w))?
Stratified (per-class reservoirs for balanced training data)? Prove the
invariant by induction — interviewers love this.

**COMMON BUGS.** `randrange(i)` vs `randint` off-by-one (probability must be
exactly k/i); 0-indexed enumerate breaking the probability; replacing without
the probabilistic gate (bias toward later items).
---

## Hard

### H1. Two-layer MLP with manual backprop (numpy)

**QUESTION.** Implement forward, backward, and a training loop for a
2-layer MLP (d → h → 1) with ReLU and sigmoid output, binary cross-entropy
loss. No autograd.

**CLARIFY.** Batch or SGD? (Full-batch GD for clarity.) Init? (He init for
ReLU — state it.) This is the "do you actually understand backprop" problem.

**APPROACH.** Cache pre-activations in forward; backward applies the chain
rule layer by layer. Shapes: X (n,d), W1 (d,h), b1 (h,), W2 (h,1), b2 (1,).

**CODE.**

```python
import numpy as np

def forward(X, W1, b1, W2, b2):
    Z1 = X @ W1 + b1            # (n, h)
    A1 = np.maximum(Z1, 0)      # ReLU
    Z2 = A1 @ W2 + b2           # (n, 1)
    A2 = 1 / (1 + np.exp(-Z2))  # sigmoid
    return {"X": X, "Z1": Z1, "A1": A1, "Z2": Z2, "A2": A2}

def backward(cache, W2, y):
    n = y.shape[0]
    A2, A1, Z1, X = cache["A2"], cache["A1"], cache["Z1"], cache["X"]
    dZ2 = (A2 - y.reshape(-1, 1)) / n        # dBCE/dZ2, sigmoid+CE fuse
    dW2 = A1.T @ dZ2                         # (h, 1)
    db2 = dZ2.sum(axis=0)                     # (1,)
    dA1 = dZ2 @ W2.T                         # (n, h)
    dZ1 = dA1 * (Z1 > 0)                     # ReLU gate
    dW1 = X.T @ dZ1                          # (d, h)
    db1 = dZ1.sum(axis=0)                    # (h,)
    return dW1, db1, dW2, db2

def train(X, y, h=16, lr=0.5, iters=2000, seed=0):
    rng = np.random.default_rng(seed)
    n, d = X.shape
    W1 = rng.normal(0, np.sqrt(2 / d), (d, h))   # He init
    b1 = np.zeros(h)
    W2 = rng.normal(0, np.sqrt(2 / h), (h, 1))
    b2 = np.zeros(1)
    for _ in range(iters):
        c = forward(X, W1, b1, W2, b2)
        dW1, db1, dW2, db2 = backward(c, W2, y)
        W1 -= lr * dW1; b1 -= lr * db1
        W2 -= lr * dW2; b2 -= lr * db2
    return W1, b1, W2, b2
```

**TESTS.** XOR or two-moons (n=400): train accuracy > 95%. Gradient check:
finite-difference each parameter matrix vs. analytic grads (do this once in
practice — it's the skill being tested). Loss decreases monotonically.

**COMPLEXITY.** O(iters·n·d·h) time; O(n·h) activation memory.

**FOLLOW-UPS.** Why does sigmoid+CE fuse to `A2 − y`? (Derive: the log
cancels the exp — do it on the board.) Dead ReLUs with bad init? (That's why
He init.) Extend to softmax + CE multi-class? (Same fused form: `P −
onehot`.)

**COMMON BUGS.** Forgetting `/n` in dZ2 (lr then means something different);
ReLU mask from A1 (`A1 > 0`) vs Z1 (same thing, but be consistent); shape
errors on b2 `(1,)` vs scalar; updating W2 before computing dA1 (use the old
W2 — order matters).

### H2. Dynamic batching scheduler (inference server)

**QUESTION.** Requests arrive with `prompt_tokens`; the server batches them
subject to `max_batch_tokens` per forward pass. Implement a scheduler that
packs queued requests greedily and returns batches. (Continuous batching is
the follow-up.)

**CLARIFY.** Objective? (Maximize throughput = minimize padding waste +
maximize utilization.) Preemption? (No — note it.) Arrival order fairness?
(FIFO within packable constraints; note starvation.)

**APPROACH.** Greedy first-fit by arrival: iterate the queue, add a request
to the current batch if it fits; else seal the batch. Track per-request
padding waste to report efficiency.

**CODE.**

```python
from dataclasses import dataclass, field

@dataclass
class Request:
    id: int
    prompt_tokens: int

@dataclass
class Batch:
    requests: list[Request] = field(default_factory=list)
    def total(self) -> int:
        return sum(r.prompt_tokens for r in self.requests)

class BatchScheduler:
    def __init__(self, max_batch_tokens: int):
        self.cap = max_batch_tokens
        self.queue: list[Request] = []

    def submit(self, req: Request) -> None:
        if req.prompt_tokens > self.cap:
            raise ValueError(f"request {req.id} exceeds capacity")
        self.queue.append(req)

    def schedule(self) -> list[Batch]:
        """Greedy first-fit, FIFO. Returns sealed batches; leftovers stay queued."""
        batches: list[Batch] = []
        cur = Batch()
        remaining: list[Request] = []
        for req in self.queue:
            if cur.total() + req.prompt_tokens <= self.cap:
                cur.requests.append(req)
            else:
                if cur.requests:
                    batches.append(cur)
                    cur = Batch()
                # retry in fresh batch (fits: checked at submit)
                cur.requests.append(req)
        if cur.requests:
            batches.append(cur)
        # NOTE: this simple version drains the queue; a real server keeps
        # leftovers when downstream is busy. See follow-ups.
        self.queue = remaining
        return batches

    @staticmethod
    def padding_waste(batch: Batch) -> int:
        if not batch.requests:
            return 0
        longest = max(r.prompt_tokens for r in batch.requests)
        return sum(longest - r.prompt_tokens for r in batch.requests)
```

**TESTS.** cap=10, requests [6,5,4] → batches [6],[5,4] (FIFO first-fit;
note [6,4],[5] would waste less — the greedy limitation, say it). Single
request > cap → ValueError.

**COMPLEXITY.** O(Q) per schedule call; O(Q) queue space.

**FOLLOW-UPS.** The real answer is **continuous batching** (Orca-style):
don't wait for the batch to finish — insert new requests as soon as any
sequence completes; batch membership changes per decode step. Padding waste
→ sort by length before packing, or use the longest-prefix grouping.
Starvation? → max wait time before a request jumps the queue.

**COMMON BUGS.** Forgetting the oversize-request check (one bad request
deadlocks the queue); mutating the queue while iterating; measuring waste
against the cap instead of the longest sequence.

### H3. Thread-safe token bucket

**QUESTION.** Token bucket rate limiter: capacity C tokens, refill rate r
tokens/sec, thread-safe `allow(n=1)`.

**CLARIFY.** Burst semantics? (Up to C instantly — that's the point vs.
sliding window.) Fractional tokens? (Yes — accumulate as float, spend ints.)

**APPROACH.** Lazy refill: on each call, add `r × elapsed` tokens (capped at
C), then spend if available. All under one lock. Invariant: `tokens ≤ C`
always; time only moves forward (monotonic clock).

**CODE.**

```python
import time
import threading

class TokenBucket:
    def __init__(self, capacity: float, refill_per_s: float):
        self.cap = capacity
        self.rate = refill_per_s
        self.tokens = capacity          # start full: allow burst
        self.last = time.monotonic()
        self.lock = threading.Lock()

    def allow(self, n: float = 1, now: float | None = None) -> bool:
        now = time.monotonic() if now is None else now
        with self.lock:
            elapsed = max(0.0, now - self.last)
            self.tokens = min(self.cap, self.tokens + elapsed * self.rate)
            self.last = now
            if self.tokens >= n:
                self.tokens -= n
                return True
            return False

    def retry_after(self, n: float = 1) -> float:
        """Seconds until n tokens are available (call without holding lock)."""
        with self.lock:
            deficit = max(0.0, n - self.tokens)
        return deficit / self.rate if self.rate > 0 else float("inf")
```

**TESTS.** C=5, r=1: 5 immediate allows, 6th rejected; `retry_after()` ≈ 1s;
advance clock 3s → 3 allows. Concurrency: 10 threads × allow → exactly 5
succeed initially (deterministic with injected `now`).

**COMPLEXITY.** O(1) per call; O(1) space — the win over sliding window.

**FOLLOW-UPS.** Distributed? → Redis + Lua script (refill-and-spend
atomically) or a centralized limiter service. Per-user buckets? → dict of
buckets + idle eviction (see W2's memory concern). Why `max(0, elapsed)`?
(Clock mocking in tests; monotonic shouldn't go backward but be safe.)

**COMMON BUGS.** Refill without the cap (unbounded burst after idle);
check-then-spend outside the lock (TOCTOU — two threads both see 1 token);
integer tokens losing fractional refill; `time.time()` instead of monotonic.

### H4. Temperature + top-p (nucleus) sampling

**QUESTION.** Implement next-token sampling: logits → temperature scaling →
top-p truncation → renormalize → sample. (The decoding loop of every LLM
serving stack.)

**CLARIFY.** Temperature edge cases? (T→0 = greedy; state it.) Batch? (1-D
here; note vectorization.) RNG? (Seeded default_rng.)

**APPROACH.** Divide by T, softmax, sort descending, keep the smallest set
with cumulative prob ≥ p, zero the rest, renormalize, `rng.choice`.

**CODE.**

```python
import numpy as np

def sample_top_p(logits: np.ndarray, temperature: float = 1.0,
                 top_p: float = 1.0, seed: int | None = None) -> int:
    assert temperature > 0 and 0 < top_p <= 1
    rng = np.random.default_rng(seed)
    z = np.asarray(logits, dtype=np.float64) / temperature
    z = z - z.max()
    probs = np.exp(z)
    probs /= probs.sum()
    if top_p < 1.0:
        order = np.argsort(-probs)                 # descending
        sorted_p = probs[order]
        cumsum = np.cumsum(sorted_p)
        # smallest k with cumsum >= p; always keep at least 1
        k = int(np.searchsorted(cumsum, top_p)) + 1
        keep = np.zeros_like(probs, dtype=bool)
        keep[order[:k]] = True
        probs = np.where(keep, probs, 0.0)
        probs /= probs.sum()                       # renormalize
    return int(rng.choice(len(probs), p=probs))
```

**TESTS.** top_p=1.0, T=1 → samples ∝ softmax (histogram check over 10k
draws). T→0.01 → always argmax (greedy). top_p→0+ → always argmax.
Logits `[5, 0, 0]`, top_p=0.5 → always token 0.

**COMPLEXITY.** O(V log V) from the sort; O(V) space. (V = vocab size.)

**FOLLOW-UPS.** Why renormalize after truncation? (Otherwise you're sampling
from a defective distribution — probabilities must sum to 1.) Top-k vs.
top-p? (Top-k is fixed count — bad when the distribution is flat or sharp;
top-p adapts.) Repetition penalty? → subtract from logits of seen tokens
before softmax.

**COMMON BUGS.** `searchsorted` off-by-one dropping the token that crosses p
(the `+1`); forgetting renormalization; applying temperature after softmax
(wrong — T scales logits); `argsort` ascending confusion.

---

## Follow-ups

:::collapse Cross-cutting follow-ups interviewers reuse
- **"Now make it batched / vectorized."** Every numpy problem: add the batch
  dim, keep `keepdims` discipline. Practice I4–I7 with a leading batch axis.
- **"Prove the invariant."** Reservoir sampling (I8) and the heap problems
  (W1, I1) — induction on the loop. Rehearse the 3-sentence version.
- **"What breaks at 100x scale?"** Heaps become sketches (W1), single buckets
  become Redis+Lua (H3), greedy batching becomes continuous batching (H2).
- **"Write the test first."** For I3/H1: assert loss decreases before you
  trust the gradients. Interviewers notice test discipline.
- **"Derive the gradient."** H1's fused sigmoid+CE, I4's `p − onehot` — do
  both on paper until they're reflexes.
:::

## Mistakes

- **Silent on shapes.** In numpy/torch code, never let a matrix multiply go
  by without stating both shapes. Half of ML coding failures are shape bugs
  the candidate never narrated.
- **Optimizing before correct.** Fancy heap when a sort would do; fused
  kernels before the naive loop works. Correct → clear → fast, in that order.
- **No edge cases in tests.** Empty input, k=0, single element, all-same —
  run these out loud even when they feel trivial.
- **Unstable numerics.** Raw `exp` on logits (W4, I4, H4), naive sigmoid
  (I3), variance without epsilon (I5). Interviewers plant large logits on
  purpose.
- **Forgetting the bias / normalization.** Logistic regression without bias
  (I3), attention without scaling (I6), probabilities that don't sum to 1
  (H4).
- **Concurrency hand-waving.** "Add a lock" without saying *what invariant
  the lock protects* (H3, W3). Name the critical section.
- **Can't state complexity.** "It's efficient" is not O(n·k·d). Practice saying
  time *and* space for every solution, including the constants that matter
  (the n×k distance matrix in I2).

## Practice

Work each problem with the 8-step loop before peeking. Check off when you can
solve it cold on a whiteboard inside the time budget.

**Warm-up** (10–15 min each)

- [ ] W1. Top-K frequent queries
- [ ] W2. Sliding-window rate limiter
- [ ] W3. LRU embedding cache
- [ ] W4. Stable softmax

**Interview** (25–35 min each)

- [ ] I1. Merge K sorted posting lists
- [ ] I2. K-means (numpy)
- [ ] I3. Logistic regression GD (numpy)
- [ ] I4. Cross-entropy + gradient
- [ ] I5. LayerNorm
- [ ] I6. Scaled dot-product attention
- [ ] I7. Multi-head attention
- [ ] I8. Reservoir sampling

**Hard** (35–45 min each)

- [ ] H1. 2-layer MLP, manual backprop
- [ ] H2. Dynamic batching scheduler
- [ ] H3. Thread-safe token bucket
- [ ] H4. Temperature + top-p sampling

Related: [ML System Design](#/ml-system-design) ·
[Agent Design](#/agent-design) · [Transformers](#/transformers)
