---
title: "Anthropic — Machine Learning Engineer"
slug: "anthropic"
section: "companies"
nav_order: 80
nav_label: "Anthropic"
tags: ["llm", "system-design", "deep-dive", "interviewing", "research", "safety"]
updated: "2026-10-01"
company: "Anthropic"
priority: "p1"
status: "target"
process_sources:
  - { label: "REPORTED", url: "https://github.com/amitgaur/ai-interviewing/blob/HEAD/research/anchor-anthropic.md", accessed: "2026-10-01", note: "Researched 2026-04-16: recruiter screen → CodeSignal take-home (~90m, 4 escalating levels; e.g. in-memory DB → filtered scans → TTL → compression) → HM 1:1 → virtual onsite (~4h, 4 rounds: coding, system design e.g. distributed search 1B docs/1M QPS, safety/ethics behavioral) → references; values round is a hard gate" }
  - { label: "REPORTED", url: "https://www.finalroundai.com/blog/anthropic-interview-process", accessed: "2026-10-01", note: "SWE = 2 coding + system design + values; MLE/RE = lighter coding + 1-2 ML deep rounds + research presentation/take-home + values" }
  - { label: "OFFICIAL", url: "https://www.anthropic.com/candidate-ai-guidance", accessed: "2026-10-01", note: "Anthropic's official AI-use policy for candidates — read before interviewing" }
---

## TL;DR

Frontier lab; per your stated preferences these are **reference points, not
targets**. REPORTED shape (researched Apr 2026):

- **Recruiter screen → CodeSignal take-home (~90 min, 4 escalating levels —
  e.g., in-memory DB → filtered scans → TTL → compression)** → **HM 1:1** →
  **virtual onsite (~4 hours, 4 rounds: coding, system design, e.g.
  distributed search over 1B docs at 1M QPS, safety/ethics behavioral)** →
  references.
- **The values round is a hard gate** [REPORTED BY CANDIDATES].
- MLE/Research tracks: lighter coding + **1–2 ML deep rounds** + research
  presentation/take-home + values.
- OFFICIAL: read **[anthropic.com/candidate-ai-guidance](https://www.anthropic.com/candidate-ai-guidance)**
  — their AI-use policy for candidates — before any round.

## Company & product

Anthropic: the Claude model family, known for the safety-first research
culture — **Constitutional AI**, interpretability research, and widely-cited
engineering writing (including the "Demystifying evals for AI agents" piece
that adopted Sierra's τ-bench pass^k framing). The culture prizes careful
reasoning, intellectual honesty, and safety impact alongside capability.

## Role expectations

MLE/Research Engineer at Anthropic (INFERRED):

- **ML depth with safety awareness:** Constitutional AI, RLHF/RLAIF variants
  (GRPO is a named topic in 2026 reports), evals, interpretability.
- **Systems thinking:** scaling laws, compute estimation — researchers are
  expected to reason about training economics.
- **Values alignment:** the values round gates offers; it's about how you
  reason under uncertainty and disagreement, not reciting principles.
- **Communication:** research presentation for RE tracks — clarity under
  expert questioning.

## Interview process

All rounds REPORTED BY CANDIDATES (Apr 2026 research + 2026 guides).

### Recruiter screen → CodeSignal take-home (~90 min)

4 escalating levels on one growing system — e.g., build an in-memory DB, add
filtered scans, add TTL, add compression. This is a **design-evolution**
exercise: clean abstractions matter more than speed, because each level
builds on the last. Practice: pick one system and extend it 3 times.

### HM 1:1

Background, research taste, team fit. For research tracks: what problems do
you want to work on and why.

### Virtual onsite (~4 hours, 4 rounds)

1. **Coding** — practical, in the CodeSignal spirit (extend a system).
2. **System design** — e.g., distributed search over 1B docs at 1M QPS
   [REPORTED BY CANDIDATES] — your search background is directly relevant.
3. **ML deep round(s)** (MLE/RE): transformers, training dynamics, evals;
   2026 topics include Constitutional AI, scaling laws, GRPO,
   interpretability, compute estimation.
4. **Safety/ethics behavioral + values** — the **hard gate**. Expect
   scenarios probing judgment under uncertainty, disagreement handling, and
   genuine engagement with safety.

Then **references** before the offer.

### Research presentation / take-home (RE tracks)

Present your best work to experts; defend methodology. Your "5th Layer"
training–serving skew piece is strong material — a subtle real-world
phenomenon, paper-quality writeup.

## Priority topics

1. **Constitutional AI / alignment:** RLAIF, harmlessness–helpfulness
   tradeoffs, red-teaming concepts.
2. **Post-training:** RLHF, DPO, GRPO (2026-named), reward hacking.
3. **Transformers & training:** attention, optimization, scaling laws,
   compute estimation (FLOPs math for training runs).
4. **Interpretability:** features, circuits — conversational fluency, not
   implementation.
5. **Eval design:** their engineering blog sets the bar — eval hygiene,
   broken-harness failure modes, LLM-as-judge limits.
6. **System design:** distributed search at 1B docs / 1M QPS (reported
   example) — retrieval, sharding, caching.
7. **CodeSignal-style evolution problems:** in-memory DB → scans → TTL →
   compression; practice the *extension* pattern.

## Company-specific themes

- **Safety as first-class:** not a compliance checkbox — the research culture
  treats safety as the hard technical problem. Engage sincerely.
- **Intellectual honesty:** the values round probes how you handle being
  wrong and uncertain — "I don't know, here's how I'd find out" beats
  bluffing.
- **Writing culture:** Anthropic's engineering blog is unusually good; clear
  technical writing is a hiring signal (your Medium piece helps).
- **Candidate AI guidance:** they have an *official policy* on AI use in
  interviews — read it; violating it is an instant fail.

## Likely system-design domains

REPRESENTATIVE PRACTICE (not reported as asked — do not claim otherwise):

1. Distributed search over 1B docs at 1M QPS (the reported example):
   sharding, replication, caching, ranking merge.
2. Design a Constitutional-AI training pipeline: data, critique loop, eval
   gates.
3. Design eval infrastructure for a frontier model: harness reliability,
   contamination controls, human eval.
4. Design inference for Claude-scale traffic: batching, caching, cost.
5. Design a red-teaming platform: attack generation, scoring, regression.

Use the 18-step framework in [#/ml-system-design](#/ml-system-design).

## Project deep-dive emphasis

- **Research presentation:** lead with the "5th Layer" — training–serving
  skew in generative retrieval. It's exactly the kind of careful empirical
  work Anthropic respects.
- For MLE tracks: Coupang ranking with emphasis on measurement rigor and
  the decisions where you chose the careful experiment over the fast one.
- Values-round stories: a time you raised a concern others dismissed; a time
  you changed your mind on evidence.

Full prep: [#/project-deep-dive](#/project-deep-dive).

## Recent work worth knowing

1. **Candidate AI guidance** (OFFICIAL): [anthropic.com/candidate-ai-guidance](https://www.anthropic.com/candidate-ai-guidance)
   — read before any round.
2. **"Demystifying evals for AI agents"** (Anthropic engineering) — adopts
   τ-bench's pass^k; know its thesis (broken harnesses, not weak models,
   explain low scores).
3. Check Anthropic's research blog for the last 90 days before any real
   process — interpretability and safety agendas move fast.

## Practice questions

All REPRESENTATIVE PRACTICE — modeled on reported Anthropic patterns, not
claimed as asked.

**CodeSignal-style:**
- [ ] Build an in-memory KV store; extend: filtered scans → TTL expiry →
      compression. Keep the abstraction clean across all 4 levels (90 min).

**ML depth:**
- [ ] Explain Constitutional AI: the critique loop, where it beats RLHF, its
      failure modes.
- [ ] Estimate training FLOPs for a 70B model on 2T tokens. Show the math;
      then estimate the cluster and time.
- [ ] What is GRPO, and when would you prefer it over PPO for post-training?
- [ ] Design an eval for instruction-following that resists contamination and
      harness bugs.

**System design:**
- [ ] Distributed search: 1B docs, 1M QPS, p99 < 100ms. Shard, replicate,
      cache, merge — with the arithmetic.
- [ ] Design the data flywheel for preference data: collection, quality
      control, dedup, privacy.

**Values (hard gate — prepare seriously):**
- [ ] Tell me about a time you disagreed with your team's direction on
      technical-safety grounds. What did you do?
- [ ] Describe a decision you made under deep uncertainty. How did you
      reason, and what would change your mind?
- [ ] When have you chosen the slower, more careful path over shipping fast?

## 30-minute checklist

- [ ] **Read the AI policy (5 min):** [candidate-ai-guidance](https://www.anthropic.com/candidate-ai-guidance)
      — non-negotiable.
- [ ] **FLOPs math (10 min):** write the 70B/2T-tokens training estimate once
      from memory.
- [ ] **Values stories (10 min):** load 2 stories — raising a concern,
      changing your mind on evidence — told with intellectual honesty.
- [ ] **CodeSignal rep (5 min planning):** schedule one 90-min
      build-and-extend session before any screen.
