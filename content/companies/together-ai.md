---
title: "Together AI — Machine Learning Engineer"
slug: "together-ai"
section: "companies"
nav_order: 130
nav_label: "Together AI"
tags: ["inference", "system-design", "deep-dive", "interviewing", "llm", "gpu"]
updated: "2026-10-01"
company: "Together AI"
priority: "p2"
status: "target"
process_sources:
  - { label: "REPORTED", url: "https://www.techprep.app/blog/together-ai-interview-process", accessed: "2026-10-01", note: "techprep.app 2026 guide: recruiter 30m → tech phone 60m (one medium-hard problem w/ ML-systems twist: streaming token generator, batching scheduler) → take-home 4-8h (CUDA kernel for inference roles) → onsite 4-5 rounds (2 coding: algorithms + applied ML-systems; system design: 100+ open models on shared GPU fleet, multi-tenant LoRA; ML/research rounds; behavioral/HM)" }
  - { label: "REPORTED", url: "https://www.techinterview.org/companies/together-ai/", accessed: "2026-10-01", note: "techinterview.org guide (90 days old): corroborates phone screen → take-home → onsite shape" }
  - { label: "REPORTED", url: "https://www.designgurus.io/answers/detail/what-is-the-together-ai-interview-process-like-round-by-round", accessed: "2026-10-01", note: "designgurus: 2-4 weeks total; Glassdoor report: 4 technical rounds + infra exec final, ~3 weeks" }
---

## TL;DR

Strong REPORTED record — the clearest inference-infra loop in this repo:

- **Recruiter (30 min)** → **tech phone (60 min, one medium-hard problem
  with an ML-systems twist** — reported examples: streaming token generator,
  batching scheduler) → **take-home (4–8 hours; a CUDA kernel for inference
  roles)** → **onsite 4–5 rounds: 2 coding (algorithms + applied ML-systems),
  system design (100+ open models on a shared GPU fleet, multi-tenant LoRA),
  ML/research rounds, behavioral/HM** [REPORTED BY CANDIDATES].
- One Glassdoor report: 4 technical rounds + infra exec final, ~3 weeks
  [REPORTED BY CANDIDATES]. Total 2–4 weeks.
- **Center of gravity: inference performance and economics** — KV-cache math,
  continuous batching, speculative decoding, quantization, **$/token**.

## Company & product

Together AI: the open-model inference cloud — 100+ open models served as
APIs, plus training/fine-tuning. The business is **$/token economics**: serve
open weights cheaper and faster than anyone else via kernel-level optimization
(custom CUDA), smart batching, and fleet utilization. Research cred (Flash
Attention lineage via Tri Dao's orbit) plus production inference at scale.

## Role expectations

MLE at Together (INFERRED from the loop): inference optimization is the job
— CUDA kernels, batching schedulers, quantization, serving 100+ models on
one fleet. The take-home CUDA kernel for inference roles is the filter:
they hire people who can make tokens cheaper, not just call APIs.

Your edge: production serving numbers + the "5th Layer" systems piece; be
ready to go one level deeper than you've had to (kernel literacy is the gap
to close — see checklist).

## Interview process

All rounds REPORTED BY CANDIDATES (2026 guides).

### Recruiter (30 min)

Background, inference interest, level. Signal genuine $/token obsession.

### Tech phone (60 min) — one medium-hard problem, ML-systems twist

A single problem with an applied twist — reported examples: **streaming
token generator, batching scheduler** [REPORTED BY CANDIDATES]. Practice:
implement a correct, clean streaming/batching primitive and discuss the
production version (what breaks at 1M tokens/sec).

### Take-home (4–8 hours) — CUDA kernel for inference roles

The famous filter [REPORTED BY CANDIDATES]: write/optimize a CUDA kernel
(e.g., a fused attention or matmul variant). This decides the onsite —
invest real hours, profile, and write up what you tried.

### Onsite (4–5 rounds)

1. **Coding ×2:** algorithms + applied ML-systems (think: implement a
   scheduler, a cache, a batching policy).
2. **System design:** **100+ open models on a shared GPU fleet,
   multi-tenant LoRA** [REPORTED BY CANDIDATES] — the signature round.
3. **ML/research rounds:** inference optimization depth — quantization,
   speculative decoding, KV-cache.
4. **Behavioral/HM** (+ infra exec final in one report).

Timeline: 2–4 weeks [REPORTED BY CANDIDATES].

## Priority topics

1. **Inference optimization:** continuous batching, paged KV-cache,
   quantization (FP8/INT8/GPTQ/AWQ), speculative decoding — with the math.
2. **CUDA basics:** memory hierarchy, coalescing, occupancy, fusion — enough
   to survive the take-home (or know your gap honestly).
3. **$/token economics:** cost modeling per 1k tokens; batching vs latency
   tradeoffs.
4. **Multi-tenant serving:** LoRA adapters at scale (Punica-style),
   model multiplexing, cold starts.
5. **Applied ML-systems coding:** schedulers, caches, streaming generators.
6. **Transformers numerics:** softmax stability, attention variants.

## Company-specific themes

- **$/token is the scoreboard:** every optimization discussion should land
  on cost per token — it's the business model.
- **Open models as strategy:** breadth of 100+ models is the moat; serving
  heterogeneity (sizes, architectures) is the technical challenge.
- **Research→production:** FlashAttention lineage — they respect
  kernel-level work that ships.

## Likely system-design domains

REPRESENTATIVE PRACTICE (not reported as asked — do not claim otherwise):

1. Serve 100+ open models on a shared GPU fleet: routing, batching across
   models, utilization (the reported signature round).
2. Multi-tenant LoRA serving: adapter batching, memory management, cold
   starts.
3. Design continuous batching with chunked prefill: the scheduler, starvation
   policy, SLOs.
4. Design quantization rollout: quality gates, per-model calibration, rollback.
5. Design the $/token metering and cost-attribution system.

Use the 18-step framework in [#/ml-system-design](#/ml-system-design).

## Project deep-dive emphasis

- **Serving numbers lead:** QPS, p99, batching behavior, cost per prediction
  — translate everything into $/token thinking.
- The take-home is a *code* deep-dive: be ready to defend every kernel
  choice (memory access pattern, occupancy, why this fusion).
- One story of squeezing latency/cost out of a serving system.

Full prep: [#/project-deep-dive](#/project-deep-dive).

## Recent work worth knowing

Together publishes inference research and model releases steadily — check
their blog for the last 90 days before any real process. Durable anchor:
the **$/token positioning** and the open-model fleet breadth (100+ models).

## Practice questions

All REPRESENTATIVE PRACTICE — the phone/take-home shapes are REPORTED; the
rest are modeled, not claimed as asked.

**Phone-screen style (60 min, one problem + twist):**
- [ ] Implement a streaming token generator with backpressure; discuss the
      production version at 1M tokens/sec.
- [ ] Implement a continuous-batching scheduler: prefill/decode phases,
      starvation avoidance.

**Take-home style (CUDA):**
- [ ] Write a fused softmax kernel; profile and iterate on memory coalescing.
- [ ] Optimize a matmul for a specific shape; document the roofline analysis.

**System design:**
- [ ] 100+ open models, one GPU fleet: routing, batching, utilization —
      with $/token math.
- [ ] Multi-tenant LoRA at scale: adapter management, batching, cold starts.
- [ ] Your p99 doubled after a quantization rollout. Debug — hypotheses in
      priority order.

**ML depth:**
- [ ] KV-cache math for 70B @ 128k; then: how does GQA change the answer?
- [ ] Speculative decoding: when does it win, when does it lose? Show the
      arithmetic.

## 30-minute checklist

- [ ] **KV-cache + batching math (10 min):** 70B@128k memory; continuous
      batching throughput intuition — write both from memory.
- [ ] **CUDA honesty check (5 min):** assess your kernel gap; if real,
      schedule a weekend CUDA sprint before any take-home.
- [ ] **$/token framing (10 min):** reframe one Coupang serving story in
      $/token terms — practice the Together register.
- [ ] **Scheduler rep (5 min planning):** one 60-min streaming/batching
      implementation, timed.
