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
    return sorted(heap, reverse=True)  # descending by count
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
