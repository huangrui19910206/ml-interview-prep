---
title: "Interview in 30 Minutes"
slug: "cram-30min"
section: "cram"
nav_order: 1
nav_label: "30-Min Cram"
tags: ["cram", "interview-prep", "uber", "doordash"]
updated: "2026-10-01"
---

## TL;DR

Six cheat sheets, 5 minutes each. Skim the bold lines. Each sheet ends with three
lines you can say *verbatim* in the interview. If time runs out: read sheets 3
(system design), 5 (deep dive), 6 (behavioral) — they carry the two Uber rounds
tomorrow (Technical Architecture @ 11:00, Scope & Impact @ 1:30).

:::warn
This page is dense on purpose. Don't memorize — pattern-match. When an
interviewer asks, the bold phrase in each bullet is the thing to say first.
:::

---

## Sheet 1 — ML Fundamentals (5 min)

- **Bias–variance:** error = bias² + variance + noise. Staff framing: "at Coupang scale
  variance is dominated by **feedback loops and nonstationarity**, not model capacity —
  so I invest in freshness and exploration, not bigger nets."
- **Metrics:** precision/recall/F1 for classification; **AUC for ranking sanity**; NDCG
  and MRR for ranked lists (use NDCG for search, recall@K for retrieval). Online:
  conversion rate, sessions per user; guardrails: latency p99, infrastructure cost.
- **Why AUC can lie:** high AUC with a skewed top of the funnel is meaningless for a
  search page — top-10 precision/NDCG decides the product. Say: "I evaluate at the
  decision boundary the product actually uses."
- **Cross-entropy:** $L = -\sum_i y_i \log \hat{y}_i$. Logistic regression is
  cross-entropy on a sigmoid; gradient $= (\sigma(w^\top x) - y)\,x$. Say it without
  thinking.
- **Regularization:** L2 shrinks, L1 sparsifies (feature selection at scale), dropout
  ≈ model averaging, early stopping = implicit capacity control. For GBDTs: leaf
  constraints, min-child-weight, and **learning-rate × n_estimators** is the knob.
- **Calibration:** models that rank well are often miscalibrated. Platt scaling,
  isotonic regression. Say: "If the score drives a threshold or a price, it must be
  calibrated; if it only ranks, calibration is optional."
- **Leakage:** any feature not available at serving time. Staff trap: **train–serve
  skew from label delay** — use short-horizon proxies (click) for features, long-horizon
  outcomes (return rate) for labels, and never let a delayed feature into the
  serving path without a backfill strategy.
- **Imbalance:** sample weights / focal loss; evaluation on precision@K, not
  accuracy. **Cold start:** content-based + heuristics until behavior accumulates,
  then blend (exploration budget).

**Say this in the interview:**
1. "I'd frame this as ranking, not classification — so I'd evaluate with NDCG and
   calibrate only if the score drives a downstream decision."
2. "The biggest risk here is train–serve skew: anything not available at serving
   time must stay out of training."
3. "I'd start with a GBDT on strong features, establish the metric baseline, then
   justify deep learning only if the residual gap pays for the serving cost."

---

## Sheet 2 — Transformer + LLM Systems (5 min)

- **Attention math:** $\text{Attn}(Q,K,V) = \text{softmax}(QK^\top/\sqrt{d_k})V$.
  Divide by $\sqrt{d_k}$ so the variance of dot products stays ≈1 and the softmax
  doesn't saturate. Complexity $O(n^2 d)$ in sequence length — the reason context
  windows are a systems problem.
- **Why multi-head:** different heads learn different relations (positional, syntactic,
  coreference) in parallel subspaces; concatenated then projected.
- **Positional info:** learned / sinusoidal / RoPE. RoPE = rotate query/key by
  position-dependent angle — relative positions fall out of the dot product. Know:
  "RoPE generalizes to longer contexts better than absolute embeddings."
- **KV cache:** inference stores K,V per token per layer → memory $O(L \cdot n \cdot d)$.
  Enables $O(1)$-per-token decode instead of $O(n)$ recompute. Bottleneck is **memory
  bandwidth, not FLOPs** at batch-size 1 — that's why batching/continuous batching
  matters.
- **Batching:** static batching wastes compute on padding; **continuous batching**
  (vLLM-style) swaps finished requests in. PagedAttention = KV cache as virtual
  memory pages. Say: "prefill is compute-bound, decode is memory-bound."
- **Quantization:** INT8/INT4 weights, ~4× memory cut for ~small quality loss.
  GGUF/AWQ/GPTQ differ in calibration needs. KV-cache quantization for long context.
- **Alignment:** SFT → reward model → RLHF/PPO; DPO skips the reward model with a
  closed-form pairwise objective. Know the failure modes: reward hacking, mode
  collapse, length bias.
- **MoE:** sparse routing to expert FFNs; capacity without proportional compute.
  Watch for: expert load imbalance, communication cost in distributed training.
- **RAG triage (30 seconds):** chunk → embed → ANN (HNSW) → retrieve top-K →
  rerank (cross-encoder) → generate with citations. Failure modes: bad chunking,
  stale index, the LLM ignoring context.

**Say this in the interview:**
1. "Attention is $O(n^2 d)$, so at scale the context window is a systems problem —
   the KV cache makes decode memory-bandwidth-bound, which is why continuous
   batching is the first optimization I'd reach for."
2. "I'd evaluate a retrieval system with recall@K on the retriever and NDCG after
   the reranker, because the two stages have different jobs."
3. "For alignment I'd start with DPO over a frozen reward-model-free setup unless
   I need the reward model for online RL — reward hacking is the failure mode I'd
   watch for either way."

---

## Sheet 3 — ML System Design (5 min)

45-minute clock. Spend 5 on clarify, 5 on objectives/metrics, 10 on data+features,
15 on model+serving, 5 on eval/experimentation, 5 on monitoring/failure modes.

- **Clarify (2–3 questions max):** who uses it, what decision the model output
  drives, latency budget, scale (QPS, corpus size), how often labels arrive.
- **Objectives:** product objective (e.g. "increase conversion per search") →
  ML objective (pairwise ranking loss) → offline metric (NDCG@10) → online metric
  (conversion, A/B) → guardrails (p99 latency, cost). **Staff signal: name the
  metric you'd get fired for moving the wrong way.**
- **Data/labels:** positive/negative construction (clicks with dwell-time debias?
  purchases?), position-bias correction (examination hypothesis, IPS), negative
  sampling for retrieval, cold-start plan.
- **Features:** query, item, query×item cross features; streaming vs batch;
  **point-in-time correctness** for training joins (the #1 production bug).
- **Model:** retrieval (two-tower / ANN) → ranking (GBDT → deep). Baseline first,
  deep only with justification. Train–serve parity plan.
- **Serving:** batch vs online, feature fetch path, model server, fallback to
  heuristic on timeout. P99 budget split: features X ms, model Y ms.
- **Eval:** offline replay on logged data + interleaving before full A/B.
- **Monitoring:** feature drift, prediction drift, label-delay monitoring,
  business-metric dashboards with alerts.
- **Failure modes:** 3 named ones + mitigations each. Staff signal: "the thing
  that breaks at 3am is X, and the mitigation is Y."

**Say this in the interview:**
1. "The product decision is ___, so the ML objective is ___, and the metric I'd
   be fired for is ___."
2. "My biggest design risk is train–serve skew, so I'd enforce point-in-time
   feature joins from day one."
3. "Baseline first — GBDT with strong features — and I'll justify deep learning
   only against the measured residual gap."

---

## Sheet 4 — Coding Patterns (5 min)

- **Two pointers / sliding window:** sorted arrays, longest-substring variants.
- **Heap:** top-K (min-heap of K), merge K sorted lists, median stream (two heaps).
- **Binary search:** on answer space ("minimize max pages") as well as arrays.
- **Trie:** prefix problems, autocomplete. **Graph BFS/DFS:** shortest path, islands,
  topological sort (Kahn's). **DP:** knapsack, LIS, edit distance — state + transition
  in one sentence before coding.
- **Python interview fluency:** `heapq`, `bisect`, `collections.deque/Counter/defaultdict`,
  `itertools`. Know `heapq.nlargest` exists but coding it is the point.
- **Interview mechanics:** restate the problem, give 2 examples (one edge), state
  brute force + complexity, then optimize. **Write a test before you run.**
  At senior level, the *optimization trajectory* (brute → better) is scored
  separately from the final solution — narrate every step up.
- **ML coding traps:** shape mismatches (assert shapes), masking in attention
  (softmax over padded tokens), in-place ops breaking autograd, NaN from
  log(0) — add epsilon.

**Say this in the interview:**
1. "Brute force is $O(n^2)$ because ___, so I'll trade ___ for $O(n \log n)$."
2. "Let me pin the invariant first: at every step, ___ holds."
3. "Edge case check: empty input, single element, duplicates — I'll test all three."

---

## Sheet 5 — Project Deep Dive (5 min)

Pick ONE project (Coupang search ranking — see [#/project-deep-dive](#/project-deep-dive)). Structure:
**Context → Problem → Scale → Your ownership → Architecture → Key decisions +
alternatives rejected → Hardest problem → Metrics → Results → What broke →
What you'd change.**

- **Ownership must be personal:** "I designed ___, I chose ___ over ___ because ___."
  "We" is fine for context; the decision sentence must be "I".
- **Scale numbers ready:** QPS, corpus size, latency budget, team size, timeline.
  A staff candidate who can't quote their own numbers is a red flag.
- **Alternatives considered:** name at least 2 things you rejected and *why* —
  this is where staff-level judgment is scored.
- **Hard problem:** the thing that took weeks and almost failed. Name the wrong
  turn you took first — vulnerability reads as seniority.
- **Measurable impact:** before/after metric with numbers, business translation
  ("+X% conversion = $Y").
- **What broke:** one real production incident, your role in the fix, the structural
  change afterward.
- **Trap:** reciting your résumé. The interviewer wants **judgment under
  uncertainty**, not a tour.

**Say this in the interview:**
1. "The project that best shows my staff-level judgment is ___. I personally
   owned the decision to ___, which the team initially disagreed with."
2. "The hardest problem was ___. My first approach failed because ___, and the
   thing that actually worked was ___."
3. "Measured impact: ___ went from ___ to ___. If I did it again, I'd change ___
   because ___."

---

## Sheet 6 — Behavioral / Staff Stories (5 min)

Uber's Scope & Impact round (1:30 PM) is scored on **scope, agency, influence**.
Every answer needs: situation (org context), your agency (what *you* decided),
opposition (who disagreed), outcome (numbers), lesson (what you'd repeat).

- **Prepare 5 stories:** (1) biggest technical decision owned, (2) cross-team
  influence without authority, (3) project that failed / hard pivot, (4) grew
  someone or raised a team's bar, (5) said NO to scope or killed a project.
- **STAR+:** Situation, Task, Action (yours), Result (numbers) — plus **"what I
  decided"** as a separate beat. Staff interviewers listen for decisions, not tasks.
- **Scope language:** "owned the ranking roadmap for a 12-person team across
  search and discovery," "drove adoption across 4 teams," "decisions affecting
  $X GMV."
- **Disagreement story:** name the competing priority honestly, explain how you
  addressed it (data, prototype, written doc), not that you "convinced everyone."
- **Failure story:** pick a real one; the lesson must be structural ("we changed
  the process to ___"), not moral.
- **Why Uber / why Core Services:** "I want my next system to be the *platform*
  other teams build on — after years owning ranking end-to-end, I know what a
  good ML platform feels like from the consumer side, and I want to build it."

**Say this in the interview:**
1. "The largest technical decision I've owned is ___. Two teams disagreed
   because ___, and it resolved when I ___."
2. "I knew the project was working when the metric moved from ___ to ___, and
   the org changed ___ as a result."
3. "What I'd do differently: I'd have ___, which is why I now always ___
   before committing a team to a direction."

---

## 30-second scan (right before the call)

- Metrics triad: offline (NDCG/AUC) → online (conversion/A-B) → guardrail (p99, cost)
- Train–serve skew is the #1 design risk; point-in-time joins are the fix
- Attention: $O(n^2 d)$, $\div \sqrt{d_k}$, decode is memory-bandwidth-bound
- Deep dive: I decided, I was wrong once, here's the number
- Staff = scope + decisions + influence, not bigger models

- [ ] Sheet 1 skimmed · Sheet 2 skimmed · Sheet 3 skimmed
- [ ] Sheet 4 skimmed · Sheet 5 story rehearsed once · Sheet 6 stories loaded
