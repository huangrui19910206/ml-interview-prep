---
title: "Google DeepMind — Machine Learning Engineer"
slug: "google-deepmind"
section: "companies"
nav_order: 90
nav_label: "Google DeepMind"
tags: ["llm", "system-design", "deep-dive", "interviewing", "research"]
updated: "2026-10-01"
company: "Google DeepMind"
priority: "p1"
status: "target"
process_sources:
  - { label: "REPORTED", url: "https://github.com/ombharatiya/ai-engineer-interview-questions/blob/HEAD/14-company-interview-questions/google-deepmind.md", accessed: "2026-10-01", note: "July 2026 guide: recruiter → HM screen → tech phone screen(s) (Google-style coding) → ML breadth 'quiz' (rapid-fire CS/math/ML) → ML coding (implement ML primitive from scratch; code must run) → systems/design (distributed training for RE) → paper discussion (RS) → leadership/team-lead chats → people & culture → hiring committee; at least one stage onsite since 2025" }
  - { label: "REPORTED", url: "https://github.com/shanmukhdatta/coding-interview-questions/blob/HEAD/AI-Companies-Interview-Questions.md", accessed: "2026-10-01", note: "2026: ML quiz ~2h (4x30m sections: CS fundamentals, math, stats, ML); 2 CoderPad coding rounds; ML/system design; paper discussion; 6-10 weeks total; AI tools prohibited in technical rounds (2026 policy)" }
---

## TL;DR

Frontier lab; per your stated preferences these are **reference points, not
targets**. The process is the **longest and most academic** in this repo
[REPORTED BY CANDIDATES]:

- **Recruiter → HM screen → tech phone screen(s) (Google-style coding)** →
  **ML breadth "quiz" (~2 hours, 4×30-min sections: CS fundamentals, math,
  stats, ML)** → **ML coding (implement an ML primitive from scratch — code
  must run)** → **systems/design (distributed training for research
  engineers)** → **paper discussion (research scientists)** →
  leadership/team-lead chats → **people & culture** → hiring committee.
- **At least one stage onsite since 2025**; total **6–10 weeks**.
- **AI tools prohibited in technical rounds** (2026 policy) [REPORTED BY
  CANDIDATES] — the opposite of the AI-native wave; prepare to code unaided.

## Company & product

Google DeepMind: Gemini models, the research lab behind AlphaGo/AlphaFold/
AlphaEvolve, operating inside Google with TPU-scale compute. The culture is
research-first and academic: paper discussions are a formal interview stage,
and the ML quiz tests breadth like a qualifying exam.

## Role expectations

SWE / Research Engineer / Research Scientist tracks differ (INFERRED):

- **SWE:** Google-style coding bar + ML fluency; systems depth valued.
- **Research Engineer:** distributed training, implementation from scratch —
  the "code must run" ML coding round is the filter.
- **Research Scientist:** paper discussion + research taste; publications
  help.
- All tracks: the **ML quiz** demands genuine breadth across CS, math,
  stats, and ML — no narrow specialists.

## Interview process

All rounds REPORTED BY CANDIDATES via 2026 aggregated guides.

### Tech phone screen(s) — Google-style coding

Classic Google coding: data structures, algorithms, clean implementation.
CoderPad reported (2 rounds in some funnels). **No AI tools.**

### ML breadth "quiz" (~2 hours)

The signature stage: **4×30-minute rapid-fire sections — CS fundamentals,
math, stats, ML** [REPORTED BY CANDIDATES]. Think qualifying exam: probability,
linear algebra, optimization, ML theory, CS basics — fast recall under
pressure. Prep with flashcards and timed drills, not deep dives.

### ML coding — implement from scratch (code must run)

Implement an ML primitive from scratch — e.g., attention, an optimizer step,
a sampling routine — and **the code must actually run** [REPORTED BY
CANDIDATES]. Practice: numpy-only implementations, debugged until they
execute, no libraries to hide behind.

### Systems/design (RE) / Paper discussion (RS)

- Research Engineers: **distributed training** system design — parallelism
  strategies, TPU topology, fault tolerance.
- Research Scientists: **paper discussion** — deep dive on a paper (yours or
  theirs); expect methodological challenge.

### Leadership, team-lead, people & culture → hiring committee

Team matching, "Googleyness"-style culture round, then committee. Slow:
**6–10 weeks** end to end.

## Priority topics

1. **ML quiz breadth:** probability (Bayes, distributions, MLE/MAP), linear
   algebra (eigendecomp, SVD), optimization (convexity, SGD variants),
   stats (hypothesis testing, bias/variance) — rapid recall.
2. **ML from scratch:** attention, softmax numerics, layer norm, Adam step,
   backprop through simple graphs — numpy-only, runnable.
3. **Transformers:** full architecture, variants, training dynamics.
4. **Distributed training:** data/tensor/pipeline parallelism, ZeRO,
   checkpointing, TPU topology basics.
5. **Google-style coding:** the classic bar — clean, correct, analyzed.
6. **Paper literacy:** be ready to discuss *their* recent work, not just
   yours.

## Company-specific themes

- **Academic rigor:** the quiz + paper discussion are closer to a PhD
  qualifying process than a typical industry loop — breadth and precision
  are graded.
- **TPU-scale thinking:** Google's compute substrate is TPUs; know the
  basics of the stack even as an outsider.
- **No-AI-tools policy (2026):** deliberate contrast with Sierra/Factory —
  they test unaided fundamentals. Don't let agent fluency atrophy your
  from-scratch skills.
- **Patience required:** 6–10 weeks with an onsite stage — plan around it.

## Likely system-design domains

REPRESENTATIVE PRACTICE (not reported as asked — do not claim otherwise):

1. Design distributed training for a 100B+ model: parallelism, checkpointing,
   fault recovery, goodput.
2. Design inference at Google scale: batching, caching, TPU utilization.
3. Design an eval harness for a research result: ablations, statistical
   rigor, reproducibility.
4. Design data pipelines for multimodal training: dedup, filtering, mixing.

Use the 18-step framework in [#/ml-system-design](#/ml-system-design).

## Project deep-dive emphasis

- **Paper discussion (RS):** your "5th Layer" piece is ideal — a real
  phenomenon, careful analysis, honest about limitations. Expect: "what's
  the strongest objection to your claim?"
- **ML coding:** the deep-dive is *live implementation* — practice narrating
  while writing numpy.
- Quiz prep rewards the opposite of deep-dives: breadth drills.

Full prep: [#/project-deep-dive](#/project-deep-dive).

## Recent work worth knowing

DeepMind publishes prolifically — before any real process, read their recent
papers in your area (Gemini technical reports, AlphaEvolve follow-ups).
Durable anchors:

1. The **no-AI-tools-in-technical-rounds** 2026 policy — the process fact
   that most affects your prep.
2. The **ML quiz** format (4×30-min: CS/math/stats/ML) — the stage with no
   analogue elsewhere in this repo.

## Practice questions

All REPRESENTATIVE PRACTICE — modeled on reported DeepMind patterns, not
claimed as asked.

**ML quiz drills (30-min timed, rapid-fire):**
- [ ] Derive the bias-variance decomposition. State the assumptions.
- [ ] Eigenvalues of a covariance matrix: what do they tell you about the
      data? When is SVD preferable to eigendecomposition?
- [ ] MLE vs MAP: write both estimators for a Gaussian mean; explain the
      prior's role as regularization.
- [ ] Why does Adam need bias correction? Derive it.
- [ ] CS fundamentals: hash table vs balanced tree tradeoffs; when does
      quicksort degrade and how do you fix it?

**ML coding (numpy-only, must run):**
- [ ] Implement multi-head attention from scratch with causal masking;
      verify output shapes and numerical sanity.
- [ ] Implement one AdamW step from scratch; test on a tiny regression.
- [ ] Implement top-k/top-p sampling; verify the distribution sums to 1.

**Systems / discussion:**
- [ ] Design data-parallel training with gradient accumulation across 256
      accelerators: where's the bottleneck?
- [ ] Discuss a recent DeepMind paper in your area: method, ablations you'd
      demand, strongest objection.

## 30-minute checklist

- [ ] **Quiz flashcards (15 min):** 20 rapid-fire cards across math/stats/ML;
      drill until recall is instant.
- [ ] **Numpy rep (15 min):** one from-scratch implementation (attention or
      Adam step), run it, fix the bugs — unaided, no AI tools.
