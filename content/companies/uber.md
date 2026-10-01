---
title: "Uber — Senior Staff MLE, Core Services Engineering"
slug: "uber"
section: "companies"
nav_order: 1
nav_label: "Uber"
tags: ["system-design", "ml-platform", "behavioral", "deep-dive", "interviewing"]
updated: "2026-10-01"
company: "Uber"
priority: "p0"
status: "interviewing"
process_sources:
  - { label: "REPORTED", url: "https://medium.com/@hack2hire.share/uber-interview-process-rounds-format-timeline-2026-bfd6c32e08cc", accessed: "2026-10-01", note: "Uber interview process 2026: OA on HackerRank, phone screen, VO (coding x2, system design, deep dive/behavioral); from 10 firsthand reports through 2026-05-01" }
  - { label: "REPORTED", url: "https://medium.com/@hack2hire.share/what-uber-actually-tests-and-what-gets-candidates-rejected-2026-29dd5b7d6f9c", accessed: "2026-10-01", note: "What Uber actually tests: independently-scored components (test-writing, optimization trajectory), L5+ deep dive requires slides" }
  - { label: "REPORTED", url: "https://interviewing.io/uber-interview-questions", accessed: "2026-10-01", note: "interviewing.io: recruiter call, tech phone screen, onsite 4-5.5h; ML engineers matched to a specific team early" }
  - { label: "REPORTED", url: "https://www.upgrad.com/blog/uber-interview-questions/", accessed: "2026-10-01", note: "Onsite: coding, software architecture, behavioral; architecture questions rooted in candidate experience" }
  - { label: "REPORTED", url: "https://www.finalroundai.com/blog/staff-engineer-interview", accessed: "2026-10-01", note: "Generic staff-interview dimensions: architectural judgment, scope ownership, cross-team influence (2025-2026 bar)" }
  - { label: "INFERRED", url: "", accessed: "2026-10-01", note: "Round names, order, and durations from Rui's confirmed schedule; 'Technical Architecture' = system/architecture round, 'Scope & Impact' = staff-level leadership/deep-dive round" }
---

## TL;DR

Two rounds tomorrow, both 60 min on Zoom with shared link, both via HackerRank:

- **11:00 AM — Technical Architecture (Eric Chen).** LIKELY: architecture-heavy
  interview — either design an ML system (possibly rooted in *your* past work) or a
  deep technical walkthrough of your Coupang architecture. Prep: one crisp
  end-to-end architecture narrative + one ML system design (platform-flavored).
- **1:30 PM — Scope & Impact (Bharat Kalyanpur).** LIKELY: staff-level leadership
  interview — largest thing you've driven, decisions, cross-team influence,
  measurable impact. Prep: 3 stories with numbers, named disagreement, structural
  lessons. This round is often the level decider at staff.

Both interviewers sit in Core Services — weight **platform thinking** (feature
stores, serving infra, training/serving parity, multi-tenant ML platform) over
marketplace product trivia.

:::warn
Round formats below are labeled per the schema. Uber's process is partly
decentralized by team — expect variance. The two confirmed rounds are from your
schedule; everything about their internal format is INFERRED.
:::

## Company & product

Uber is the global rideshare + delivery marketplace (Mobility, Delivery/Eats,
Freight) — tens of millions of trips/day, operating in 70+ countries. The
business is a two-sided marketplace with real-time matching: every rider request
triggers dispatch, pricing (surge), ETA, fraud/risk, and routing decisions in
hundreds of milliseconds.

Why that matters for this interview: Uber's ML is **decision infrastructure** —
models that must be correct, fast, and safe at 250K+ predictions/sec, with
feedback loops that directly move revenue. Core Services is the org that builds
the shared substrate (compute, storage, data/ML platforms) everyone else builds
on. They hire senior staff to make **platform bets with multi-team impact**,
not to tune one model.

## Role expectations

**Senior Staff MLE, Core Services Engineering** (SF/Seattle/Sunnyvale; base band
reported ~$267K–$297K; 10+ yrs experience; [REPORTED: job listings](https://jobright.ai/jobs/h1b-visa-sponsored-staff-machine-learning-engineer-jobs-in-Seattle%2C%20WA)).

Senior Staff ≈ L6+ at Uber. What the level means here:

- **Technical strategy:** you set direction for ML systems that multiple product
  teams consume — not one model, a *capability* (e.g., "every team can serve a
  model at p99 < 50ms without owning infra").
- **Ambiguity ownership:** define the problem, the metrics, and the rollout —
  nobody hands you a scoped ticket.
- **Cross-org influence:** architecture reviews, standards, deprecations —
  decisions that survive contact with teams you don't manage.
- **Judgment over throughput:** knowing what *not* to build, when a heuristic
  beats a model, when to kill a platform component.

Your edge: 3 years as tech lead of Search & Discovery at Coupang (query rewriting
→ retrieval → multi-stage ranking → LLM discovery) plus Meta Feed rec and
Pinterest search. You have consumed ML platforms at scale — frame yourself as the
candidate who knows what great platform feels like from the user side and can
now build it.

## Interview process

Your confirmed schedule (from your calendar — not a public claim):

- 11:00 AM–12:00 PM PT, **Technical Architecture** — Eric Chen
- 1:30–2:30 PM PT, **Scope & Impact** — Bharat Kalyanpur
- Both via HackerRank links, shared Zoom link, coordinator Tyler Wong.

What the broader process looks like for senior MLE candidates [REPORTED BY CANDIDATES]:

- **Recruiter screen** (30 min): background, motivation, level alignment.
- **Technical phone screen** (30–45 min): coding + tradeoff discussion for L5+;
  brute-force → optimize trajectory, scored separately.
- **Virtual onsite** (4–5.5 h): typically 2 coding rounds, 1–2 system-design /
  architecture rounds, 1 deep-dive + behavioral. For L5+, the deep dive has
  historically required a **formal slide presentation (~25 min) with Q&A**, not a
  casual walkthrough.
- **Team matching:** ML engineers are often matched to a specific team/org early;
  your panel is likely all from Core Services and draws from a company-wide
  question bank with hiring-manager variance.

Round-by-round for tomorrow (each tagged):

### Round 1 — Technical Architecture [INFERRED]

**Most likely shape:** an architecture round with an ML-systems flavor. Two
variants to prepare for:

1. **Design an ML system** (45-min design compressed): e.g., "design Uber's ETA
   prediction platform" or "design a feature store for 5,000 models." They will
   judge scoping, tradeoff narration, and depth in one chosen slice — *depth
   within a scoped slice beats full-product breadth* [REPORTED BY CANDIDATES].
2. **Architecture deep-dive on your past work:** "Walk us through the Coupang
   search ranking architecture end-to-end; now redesign it for 10× scale / as a
   multi-tenant platform." This is the variant where your background is the
   weapon — see [#/project-deep-dive](#/project-deep-dive).

Either way, expect follow-ups on: training–serving parity, feature freshness,
failure modes, cost/latency tradeoffs, and "why not the simpler alternative."
Full framework: [#/ml-system-design](#/ml-system-design).

### Round 2 — Scope & Impact [INFERRED]

**Most likely shape:** staff-level leadership/behavioral interview with technical
teeth. The interviewer is testing five things [REPORTED BY CANDIDATES + generic
staff rubrics]:

1. **Largest thing you've driven** — scope, duration, org footprint.
2. **Architectural judgment** — a decision where reasonable people disagreed,
   and why your call was right (with the receipt).
3. **Cross-team influence without authority** — how you moved people you
   didn't manage.
4. **Impact at scale** — org-level outcomes with numbers, not individual output.
5. **Technical strategy** — what you'd build/change for the org in the next
   2 years.

This is frequently the **level decider**: strong technicals + weak scope story =
senior offer instead of senior staff. Bring numbers, named disagreement, and at
least one "I was wrong and changed course" beat — it reads as seniority, not
weakness.

## Priority topics

Ranked for a Senior Staff MLE in Core Services (platform-weighted):

1. **ML platform architecture:** feature stores, model registry, training/serving
   parity, multi-tenant serving, standardized training pipelines. Know
   Michelangelo's shape cold (see Recent work).
2. **Training–serving skew:** point-in-time joins, feature freshness, streaming
   vs batch features, label delay.
3. **Online inference at scale:** p99 latency budgets, batching, caching,
   fallbacks, cost per prediction.
4. **Ranking & retrieval:** two-tower retrieval, ANN (HNSW), multi-stage
   ranking, position-bias correction, NDCG/recall@K. (Your home turf — use it
   as the example domain, but pivot to platform implications.)
5. **Experimentation:** A/B design, interleaving, guardrail metrics, delayed
   outcomes.
6. **Reliability:** failure modes of ML systems, monitoring (feature/prediction
   drift), incident response, rollback gates.
7. **Distributed systems basics:** consistency, partitioning, geospatial indexing
   (H3), streaming (Flink/Kafka-style), exactly-once semantics where relevant.
8. **LLM systems (secondary):** inference optimization, eval, RAG — relevant as
   "LLM-powered product discovery" is on your résumé; expect one question.

## Company-specific themes

Know these well enough to drop one reference each — they show you did homework:

- **Marketplace dynamics:** two-sided (rider/driver, eater/courier), real-time
  matching, surge pricing as supply-demand control, ETA as the core prediction
  product. Marketplace feedback loops: your model changes behavior, which changes
  your training data.
- **Matching & dispatch:** batch matching windows, geospatial indexing (Uber's
  H3 hexagonal grid is the canonical example of "right abstraction, huge
  leverage" — a platform story).
- **ETA / forecasting:** sequence models over traffic, the canonical "prediction
  at massive scale with strict latency" example.
- **Fraud, risk & safety:** adversarial setting — fraud models face an adaptive
  adversary, so stationarity assumptions break; retraining cadence and feature
  secrecy matter.
- **Surge pricing:** optimization under fairness/regulatory constraints —
  good example of "ML decision with business guardrails."
- **Platform theme (weight this most):** Uber's ML history is "from 7 bespoke
  systems to 5,000+ production models on one platform" [REPORTED BY CANDIDATES,
  describing Michelangelo]. The lesson they want you to internalize: **the
  leverage is in the platform, not the model.**

## Likely system-design domains

REPRESENTATIVE PRACTICE (not reported as asked — do not claim otherwise):

1. **Design a feature store** for thousands of models: online/offline split,
   point-in-time correctness, backfill, freshness SLAs.
2. **Design model serving for 250K predictions/sec at p99 < 50ms:** batching,
   caching, multi-model routing, fallbacks.
3. **Design Uber ETA prediction end-to-end:** features (traffic, weather,
   driver), sequence model, serving path, monitoring.
4. **Design a multi-tenant ML training platform:** scheduling, resource
   isolation, experiment tracking, cost attribution.
5. **Design driver–rider matching:** geospatial index, batch matching, real-time
   constraints (more product-flavored; less likely for Core Services, but be
   ready).
6. **Design a real-time fraud/risk scoring system:** streaming features,
   adversarial adaptation, human review loop.
7. **Redesign your Coupang ranking stack as a platform** three teams can build
   on — the "architecture deep-dive" variant of round 1.

For each: use the 18-step framework in [#/ml-system-design](#/ml-system-design).

## Project deep-dive emphasis

Round 1 may *be* a deep dive on your architecture. Ruthless checklist:

- **One project, end to end:** Coupang search ranking (query rewriting → retrieval
  → multi-stage ranking → LLM discovery). 5-minute crisp narrative, then let them
  pull threads.
- **Draw the architecture** before they ask: data flow, serving path, latency
  budget split, team boundaries.
- **Decisions with rejected alternatives:** at least 3 ("we chose X over Y
  because…").
- **Scale numbers:** QPS, corpus, p99, team size, timeline — from memory, no
  hedging.
- **The hard part:** the thing that almost failed, your wrong first approach.
- **Measured impact:** metric before → after, business translation.
- **Platform angle:** "what would this look like as a platform 3 teams build on"
  — have one slide's worth of answer ready, because Core Services will ask.

Full prep: [#/project-deep-dive](#/project-deep-dive).

## Recent work worth knowing

(Real items; URLs are from public sources. Cite dates as shown.)

1. **Michelangelo — Uber's ML-as-a-service platform.** The canonical Uber ML
   story: standardized path from research to runtime — feature store (batch +
   streaming features), model registry, unified serving. Reported shape: ~10,000
   shared features, highest-traffic models at 250K+ predictions/sec, p95
   inference under ~5–10ms, thousands of production models
   [REPORTED BY CANDIDATES — treat numbers as approximate].
   Uber's own writeup: [Michelangelo ML platform](https://www.uber.com/us/en/blog/michelangelo-machine-learning-platform/)
   (Uber blog; accessed 2026-10-01). **Why it matters tomorrow:** it's the
   reference architecture for every platform question they'll ask, and the
   "platform > model" lesson is the thesis of your candidacy.
2. **Uber's AI decision engine for pricing/routing (Jan 2026 coverage).**
   Overview of how Michelangelo powers surge, ETA, routing, and fraud at
   "millions of real-time predictions per second"
   ([Medium, Jan 2026](https://medium.com/@anavale_19459/inside-ubers-ai-decision-engine-for-pricing-routing-and-customer-experience-d03168f29e8d);
   third-party summary, not Uber-official). Useful for one-line references in
   the Scope & Impact round: "I know your pricing and ETA stack runs on a shared
   feature layer — that's exactly the leverage point I'd look to extend."

Optional third reference if conversation allows: **H3** (Uber's open-source
hexagonal geospatial index) — the textbook "right abstraction" platform story.

## Practice questions

All REPRESENTATIVE PRACTICE — modeled on reported Uber MLE/system-design
patterns, not claimed as asked. - [ ] task lists for tracking.

**Technical Architecture (round 1):**
- [ ] Design a feature store serving 5,000 production models with online and
      offline access. How do you guarantee point-in-time correctness?
- [ ] Design model serving for 250K predictions/sec, p99 < 50ms. Walk through
      the request path and the latency budget.
- [ ] Walk me through your Coupang search-ranking architecture end-to-end.
      Now redesign the serving path for 10× QPS.
- [ ] Design Uber's ETA prediction system: data, features, model, serving,
      monitoring. What breaks first at 3am?
- [ ] Design a multi-tenant ML training platform: scheduling, isolation,
      experiment tracking, cost attribution across teams.
- [ ] Your ranking model's offline NDCG improved but the A/B is flat. Debug it
      live — enumerate hypotheses in priority order.
- [ ] Design real-time fraud scoring with streaming features. How do you handle
      an adaptive adversary?
- [ ] "Why not just use a heuristic / GBDT / a bigger model?" — defend your
      modeling choice against the simpler alternative (expect this as a
      follow-up to everything).

**Scope & Impact (round 2):**
- [ ] Tell me about the largest technical decision you've owned. Who disagreed,
      and how did it resolve?
- [ ] Describe a migration or platform rollout that took more than two
      quarters. What did you get wrong at the start?
- [ ] Tell me about a time you changed the direction of a project already
      underway. What was the cost of being wrong?
- [ ] How have you influenced a technical decision across teams you didn't
      manage? Be specific about the mechanism (doc, prototype, review).
- [ ] Tell me about a time you killed a project or said no to scope. How did
      you make the call defensible?
- [ ] What does your current org do that won't survive 5× growth, and how would
      you sequence fixing it?
- [ ] If you joined Core Services, what would you build or change in the first
      year? (Have a real answer — platform-flavored, informed by Michelangelo.)
- [ ] Tell me about a production incident in your ML system. Your role, the fix,
      and what changed structurally afterward.

## 30-minute checklist

Do this tonight or tomorrow morning before 11:00 AM:

- [ ] **Architecture narrative (10 min):** rehearse the 5-minute Coupang
      end-to-end walkthrough once, out loud. Draw it on paper.
- [ ] **One platform design (10 min):** sketch feature-store or model-serving
      design; write the latency budget and 3 failure modes.
- [ ] **Scope stories (10 min):** load 3 stories — biggest decision, cross-team
      influence, failure/pivot — each with numbers and a named disagreement.
- [ ] Say out loud: your "why Uber Core Services" (platform leverage thesis),
      your "what I'd build in year one" (one concrete platform bet).
- [ ] Logistics: HackerRank links open, Zoom link ready, water, notebook for
      drawing. Camera-on interviews — check lighting.
- [ ] Skim [#/cram-30min](#/cram-30min) sheets 3, 5, 6 one final time.
