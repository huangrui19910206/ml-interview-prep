---
title: "Project Deep Dive — Staff-Level Framework"
slug: "project-deep-dive"
section: "deep-dive"
nav_order: 1
nav_label: "Project Deep Dive"
tags: ["deep-dive", "behavioral", "staff", "interview-prep"]
updated: "2026-10-01"
---

## TL;DR

The deep dive tests one thing: **judgment under uncertainty at scale**. The
interviewer is listening for six signals — *what you personally did, why this
design, what was hard, what scale, what tradeoffs, what measurable impact*.
Structure every answer as: Context → Problem → Scale → Ownership → Architecture
→ Decisions → Alternatives → Tradeoffs → Hard problems → Metrics → Results →
Failures → Lessons → What I'd change. Lead with ownership, end with what you'd
change.

:::warn
The #1 staff-level failure: a technically strong candidate who can't say "I
decided" — everything is "we." "We" describes the team; the interview scores
*you*.
:::

## Interview answer (the 5-minute narrative)

Pick **one** project — for Rui, that's Coupang search ranking. Memorize this arc:

1. **Context (30s):** "At Coupang I was tech lead for Search & Discovery —
   query rewriting, retrieval, multi-stage ranking, LLM-powered discovery —
   serving [QPS] over [corpus size] with a p99 budget of [X]ms."
2. **Problem (30s):** "The problem was ___. The business cost of not solving it
   was ___."
3. **Your ownership (30s):** "I personally owned ___. The team was N people; I
   set the technical direction and made the final call on ___."
4. **Architecture (60s):** Draw it. Data flow, serving path, latency split.
5. **Key decision + rejected alternative (60s):** "I chose X over Y because…"
6. **Hardest problem (45s):** "The thing that almost failed was ___. My first
   approach was wrong because ___."
7. **Result (30s):** "___ went from ___ to ___, which meant ___ for the
   business."
8. **What I'd change (15s):** "With hindsight I'd ___."

Then stop talking. Let them pull threads — the follow-ups are where the level
is decided.

## The full framework (for 45–60 min deep dives)

### Context → Problem → Scale

- **Context:** org, team, your role, timeline. One or two sentences.
- **Problem:** the business problem, not the technical one. "Search conversion
  was X and the headroom was Y" beats "we needed a better ranker."
- **Scale:** QPS, corpus/users, latency budget, data volume, team size,
  timeline. **Have the numbers.** A staff candidate who hedges on their own
  scale numbers fails the round.

### Ownership → Architecture

- **Ownership:** name the decisions that were *yours*: the architecture, the
  modeling choice, the rollout plan, the kill decision. "I decided" sentences,
  minimum three.
- **Architecture:** the end-to-end diagram — training and serving. Mark team
  boundaries: what your team owned vs. consumed. Staff signal: you can draw the
  parts you *didn't* build and explain the interface contract.

### Decisions → Alternatives → Tradeoffs

- For each major decision: the options, the criteria, the choice, the price.
  Minimum **three** decisions with rejected alternatives.
- **Tradeoffs** must be quantified where possible: "Option A: +1.2% NDCG at
  +30ms p99 and $X/month. Option B: +0.4% at +5ms. We shipped B first because
  latency was the binding constraint, then revisited A after the infra
  upgrade."
- Staff signal: decisions you made *against* the team's initial instinct, with
  the evidence that changed minds.

### Hard problems → Metrics → Results

- **Hard problems:** the thing that took weeks. Name your wrong first approach —
  vulnerability reads as seniority.
- **Metrics:** offline, online, guardrails. The metric you'd get fired for.
- **Results:** before → after with numbers, business translation ("+X%
  conversion ≈ $Y GMV/quarter").

### Failures → Lessons → What I'd change

- **Failures:** one real production incident. Your role, the fix, the
  *structural* change afterward (process, monitoring, architecture) — not just
  "we fixed the bug."
- **Lessons:** what you now do differently *by default*.
- **What I'd change:** one substantive thing. "Nothing, it went great" is a
  fail. The best answer names a real tradeoff you'd now resolve differently.

---

## Fill-in template — Rui's Coupang search-ranking project

Fill this in tonight. One line each — then rehearse out loud.

```text
PROJECT: Coupang Search & Discovery ranking (tech lead, 2023–present)

CONTEXT:  Team of ___, owning query rewriting → retrieval → multi-stage
          ranking → LLM-powered product discovery.

PROBLEM (business): _______________________________________________
SCALE:    QPS ____, corpus ____ items, p99 budget ____ms,
          training data ____ events/day, team ____, timeline ____.

MY OWNERSHIP (3 "I decided" sentences):
  1. I decided ___________________________________________________
  2. I decided ___________________________________________________
  3. I decided ___________________________________________________

ARCHITECTURE (draw it):
  query → [rewriting] → [retrieval: ______] → [ranking stages: ______]
        → [serving: ______] ; features from ______ ; labels from ______

DECISION 1: chose ______ over ______, because ______ (price: ______)
DECISION 2: chose ______ over ______, because ______ (price: ______)
DECISION 3: chose ______ over ______, because ______ (price: ______)

HARDEST PROBLEM: _________________________________________________
  My first (wrong) approach: _____________________________________
  What actually worked: __________________________________________

METRICS: offline ______, online ______, guardrails ______.
  Fire-me metric: ______.
RESULTS: ______ went from ______ to ______ (≈ $______ business impact).

FAILURE: ________________________________________________________
  Structural change afterward: ___________________________________

WHAT I'D CHANGE: _________________________________________________

PLATFORM ANGLE (for Core Services): as a platform 3 teams build on,
  I'd extract ______ as the shared layer, because ______.
```

**The platform angle is not optional tomorrow.** Both interviewers are Core
Services. End your narrative with one sentence on what generalizes.

---

## 15+ aggressive follow-ups (with model answers)

These are what a staff interviewer asks after the narrative. Practice answering
in 60–90 seconds each.

1. **"What did *you* personally do vs. the team?"**
   Model: "The team built the pipelines; I personally owned three decisions:
   the two-stage architecture, the pairwise loss formulation, and the staged
   rollout. Here's the decision I made that the team initially disagreed with…"

2. **"Why this architecture and not [simpler alternative]?"**
   Model: Price both. "The simpler alternative captures ~70% of the gain at 20%
   of the cost — we actually shipped it as v1. The full architecture was
   justified only after v1 validated the headroom."

3. **"What was the hardest technical problem, really?"**
   Model: Name the weeks-long one, your wrong first approach, the insight.
   Never: "everything went smoothly."

4. **"Walk me through the serving path at p99. Where does the time go?"**
   Model: Budget split with numbers: "retrieval 40ms, feature fetch 60ms,
   ranking 60ms… the binding piece was feature fetch, so we…"

5. **"How did you handle train–serve skew?"**
   Model: "Point-in-time feature joins, enforced by [mechanism]. The one time it
   bit us was ___, and we caught it via ___."

6. **"Your offline metric went up but online didn't. What did you do?"**
   Model: Hypothesis order — censoring/leakage in offline eval, position bias in
   labels, insufficient experiment power, interference. "In our case it was
   ___, and the fix was ___."

7. **"Who disagreed with your approach and how did it resolve?"**
   Model: Name the role and their concern honestly. "The infra team pushed back
   on serving cost. I built the cost model showing break-even at +0.5%
   conversion; we agreed on a 2-week shadow validation. They were right to push
   — it forced the cheaper design."

8. **"What would break first at 10× scale?"**
   Model: One component, with numbers. "Feature-store read QPS — we're at 20K
   with 3× headroom; at 10× we'd shard by entity key and add request
   coalescing."

9. **"Tell me about a production incident."**
   Model: What broke, blast radius, your role in detection/fix, the structural
   change. End on the structural change — that's the staff signal.

10. **"How did you decide the retraining cadence?"**
    Model: "Measured, not habitual: we tracked concept drift on the delayed
    labels and set the cadence where marginal gain flattened — daily
    incremental, weekly full."

11. **"What did you choose NOT to build?"**
    Model: Name the tempting scope you killed and the reasoning. "We killed the
    real-time personalization layer — the latency cost exceeded the measured
    headroom, and v1 didn't need it."

12. **"How did you evaluate the LLM-powered discovery piece?"**
    Model: "Offline: human-rated relevance on a sampled query set + NDCG on the
    reranked slice. Online: A/B on conversion with a hallucination guardrail —
    every generated snippet was constrained to catalog attributes. The failure
    mode we watched was fabricated product claims."

13. **"How did you grow the engineers on the team?"**
    Model: Specific, not philosophy: "I moved [person] from pipeline work to
    owning the ranking experiment design; within two quarters they were running
    the A/B review. The mechanism was weekly design reviews where I asked
    questions instead of giving answers."

14. **"What technical debt did you deliberately take on?"**
    Model: Name it, the interest rate, and the payoff plan. "We hardcoded the
    feature config for v1 to hit the date — interest was every experiment needed
    an eng change; we paid it down in v2 with the config service."

15. **"If you joined Uber Core Services, what from this project generalizes?"**
    Model: "The feature-freshness tiering and the point-in-time join discipline
    — those are platform problems, not ranking problems. I'd productize them."

16. **"What would you do differently with twice the team / half the time?"**
    Model: Shows sequencing judgment. "Half the time: ship the GBDT v1 and the
    logging; cut the deep ranker. Twice the team: parallelize the platform
    extraction — but not the modeling, that's coordination overhead."

17. **"Convince me this wasn't just throwing a bigger model at it."**
    Model: "The model change was worth +0.8%; the label debiasing +1.5% and the
    retrieval recall fix +2.1%. The unglamorous work carried the result —
    here's the ablation."

---

## Staff-level traps

- **Vague ownership.** "We decided…" for every decision. Fix: rehearse three
  "I decided" sentences until they're automatic.
- **No metrics.** A 10-minute narrative with zero numbers. Fix: memorize five
  numbers — scale (QPS, corpus), latency, before/after metric, business impact.
- **No alternatives considered.** "We just built it this way." Fix: three
  rejected alternatives with reasons, one of which the team initially preferred.
- **No failure.** "It went smoothly." Nobody believes it; it signals either
  small scope or no self-awareness. Fix: one real incident + structural change.
- **No "what I'd change."** Signals you stopped thinking. Fix: one substantive
  answer that shows a tradeoff you'd now resolve differently.
- **Résumé recitation.** Listing projects instead of going deep on one. Fix:
  one project, full depth; offer the second only if asked.
- **Defensiveness on disagreement questions.** The interviewer *wants* to hear
  about conflict — it's where influence is scored. Fix: name the disagreement
  proudly and explain the resolution mechanism.
- **Platform-blindness (tomorrow specifically).** Describing a product system
  with no view of what generalizes. Fix: the platform-angle sentence at the
  end of every narrative.

## Intuition (why this round exists)

At senior staff, the company is buying **judgment**: which problems to solve,
which designs survive contact with reality, which bets pay off. The deep dive
is a retrospective case study of your judgment. Every question is a variant of:
"Show me a hard call you made, why it was right, and what it cost." Technical
depth is table stakes — the differentiator is decisions with receipts.

## Practice

- [ ] Fill in the template above — every blank, tonight.
- [ ] Rehearse the 5-minute narrative out loud, timed. Twice.
- [ ] Answer follow-ups 1, 7, 9, 11 out loud — these are the highest-signal.
- [ ] Write down your five numbers on an index card: QPS, corpus, p99,
      before/after metric, business impact.
- [ ] Prepare the platform-angle closing sentence.
