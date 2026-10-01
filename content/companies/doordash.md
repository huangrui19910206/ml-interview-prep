---
title: "DoorDash — Machine Learning Engineer"
slug: "doordash"
section: "companies"
nav_order: 20
nav_label: "DoorDash"
tags: ["recsys", "system-design", "deep-dive", "interviewing", "behavioral", "ai-coding"]
updated: "2026-10-01"
company: "DoorDash"
priority: "p0"
status: "interviewing"
process_sources:
  - { label: "OFFICIAL", url: "https://doordash.mxcedar.com/65452d165efa39c9bf578524/f/B0j2btr3c3K04DuDw/", accessed: "2026-10-01", note: "DoorDash MLE candidate prep kit (fetched 2026-10-01): Round 2 loop = 4 modules — AI Code Craft Challenge (60m), ML System Design (60m), Domain Knowledge (60m), Engineering Values + HM Chat (45m). Starter code via HackerRank; AI editor allowed; full-screen share" }
  - { label: "REPORTED", url: "https://www.teamblind.com/post/doordash-codecraft-32wlnglb", accessed: "2026-10-01", note: "Blind thread (May 2026): CodeCraft candidates report practical business-module coding, e.g. Dasher payout logic" }
  - { label: "REPORTED", url: "https://www.teamblind.com/post/doordash-codecraft-interview-coming-up-qxhw1ryh", accessed: "2026-10-01", note: "Blind thread: CodeCraft reported as non-LeetCode practical coding despite the format's claims" }
  - { label: "REPORTED", url: "https://leetcode.com/discuss/post/7405621/doordash-codecraft-by-anonymous_user-xvze/", accessed: "2026-10-01", note: "LeetCode discuss: one candidate reported a LeetCode-ish tree-diffing problem in CodeCraft" }
  - { label: "REPORTED", url: "https://www.1point3acres.com/interview/thread/1021269", accessed: "2026-10-01", note: "1point3acres: DoorDash MLE onsite thread (Chinese)" }
  - { label: "INFERRED", url: "", accessed: "2026-10-01", note: "Rui's Round 1 (2026-10-07, Xiaochang Miao) is labeled 'ML Domain Knowledge' — INFERRED to match the prep kit's Domain Knowledge round; the 4-module loop likely follows as Round 2 if Round 1 passes" }
---

## TL;DR

**Your Round 1 (Wed 2026-10-07, 1:00–2:00 PM PDT, Xiaochang Miao) is "ML Domain
Knowledge"** — INFERRED to be the prep kit's 60-minute Domain Knowledge round:
a business case + ML depth in a domain relevant to *your* background (search /
recommendation). The prep kit describes the **Round 2 loop as 4 modules, all
60 min except the last (45 min)**:

1. **AI Code Craft Challenge** (60 min) — practical business-module coding with
   AI editor allowed (Cursor/Claude Code/Codex/Copilot), graded on
   problem-solving, AI fluency, code quality, communication. NOT LeetCode-style
   [OFFICIAL]. Candidates report practical problems (e.g. Dasher payout logic),
   though one reported a tree-diffing problem [REPORTED BY CANDIDATES].
2. **ML System Design** (60 min) — components, data pipelines, iteration /
   experimentation, metrics, reliability and scaling [OFFICIAL].
3. **Domain Knowledge** (60 min) — business case + ML domain knowledge relevant
   to your background; if unsure which domain, ask your recruiter [OFFICIAL].
4. **Engineering Values + HM Chat** (45 min) — behavioral on the DoorDash
   Principles [OFFICIAL].

Round 1 is your highest-leverage prep: treat it as a business-case + ML-depth
screen with a DoorDash-flavored framing.

:::warn
The prep kit covers the "Round 2" loop; your Oct 7 round is Round 1. Round 1's
exact format is INFERRED from the prep kit's Domain Knowledge module — confirm
the domain with Noe Perez (the prep kit explicitly says to ask your recruiter).
:::

## Company & product

DoorDash is the US last-mile delivery marketplace leader — food delivery
(Restaurant), plus grocery, retail, and "new verticals" (alcohol, beauty,
electronics). The business is a three-sided marketplace: consumers, merchants,
and Dashers (drivers), matched in real time with fees, ETAs, dispatch, and
pricing all ML-driven.

Why that matters for your interview: DoorDash's ML is **marketplace operations
at scale** — dispatch optimization, ETA prediction, Dasher pay/pricing, ads and
promotion targeting, and increasingly **multi-vertical recommendations** (a
consumer who orders tacos and groceries in one app needs a recommender that
bridges behavioral silos — exactly what their RecSys 2025 paper tackles). Ads
are a growing profit engine ("deep learning for ads conversion in last-mile
delivery," arXiv Feb 2025). Your Coupang search/ranking background maps directly
onto their recommendations and ads teams.

## Role expectations

MLE at DoorDash spans recommendations, search, ads, logistics/dispatch, and
pricing. Expect the profile they screen for in the prep kit:

- **Business-case fluency:** the Domain Knowledge round is explicitly a *business
  case* + ML depth, so you need to reason about marketplace dynamics (supply /
  demand balance, Dasher incentives, merchant value) as well as models.
- **End-to-end ML ownership:** pipelines, experimentation, metrics, reliability
  — the system-design module's graded dimensions read like a "production MLE"
  checklist, not a modeling quiz.
- **AI-native coding:** the CodeCraft module grades *AI fluency* — they want to
  see you work *with* an AI editor (prompting, verifying, steering), matching
  the industry shift (cf. Sierra's official AI-native interview doctrine and
  Fireworks AI's interview rethink — both in this repo).

## Interview process

The OFFICIAL 4-module Round 2 loop (from the candidate prep kit, fetched
2026-10-01), each tagged:

### Round 1 — ML Domain Knowledge screen (your Oct 7 round) [INFERRED]

Your invite says "ML Domain Knowledge" with Xiaochang Miao. The prep kit's
**Domain Knowledge (60 min)** is the best match: *"business case + ML domain
knowledge in a domain relevant to candidate's background"* [OFFICIAL]. Expect:

- A business scenario grounded in DoorDash's marketplace (likely
  recommendations/search given your background), with follow-up ML depth —
  e.g., "design the ranking for the home feed," then drill into features,
  labels, position bias, experimentation.
- Rapid-fire ML fundamentals are possible, but the prep kit's framing is
  domain-first, not trivia-first.

**Action item:** email Noe Perez to confirm which domain to prepare (the prep
kit explicitly invites this: *"if unsure which domain, ask your recruiter"*
[OFFICIAL]).

### Module 1 — AI Code Craft Challenge (60 min) [OFFICIAL]

- Your own laptop, your AI editor of choice (Cursor, Claude Code, Codex,
  Copilot), starter code delivered via HackerRank, **full-screen share**.
- Practical business-module coding — candidates report problems like Dasher
  payout logic [REPORTED BY CANDIDATES], i.e., implement a realistic
  marketplace computation with edge cases.
- Graded on: problem-solving, **AI fluency** (how you prompt/verify/steer the
  agent), code quality, communication.
- "Not LeetCode-style" [OFFICIAL] — but hedge: one candidate reported a
  tree-diffing problem [REPORTED BY CANDIDATES], so keep basic data-structure
  fluency warm.

### Module 2 — ML System Design (60 min) [OFFICIAL]

- Graded dimensions straight from the prep kit: **system components, data
  pipelines, iteration/experimentation, metrics, reliability and scaling**.
- This is a production-ML checklist: expect to be pressed on training/serving
  skew, feature pipelines, experiment design, and what breaks in prod.

### Module 3 — Domain Knowledge (60 min) [OFFICIAL]

- Business case + ML domain knowledge in a domain relevant to your background.
- Your likely domain: recommendations/search — prepare to discuss retrieval,
  ranking, personalization, and multi-vertical behavior (their RecSys 2025 work
  is tailor-made conversation material).

### Module 4 — Engineering Values + HM Chat (45 min) [OFFICIAL]

- Behavioral on the **DoorDash Principles**. Prepare stories mapping to: bias
  for action, customer obsession (three-sided: consumer/merchant/Dasher),
  ownership, disagree-and-commit, operational excellence.

## Priority topics

1. **Recommendation systems:** two-tower retrieval, ANN, multi-stage ranking,
   personalization, cold start — your home turf; expect it as the Domain
   Knowledge center of gravity.
2. **Multi-vertical / cross-domain recommendation:** bridging behavioral silos
   across food, grocery, retail (their RecSys 2025 "Mind the Gap" paper — read
   the abstract at minimum).
3. **Ads & conversion modeling:** deep learning for ads conversion in delivery;
   calibration, delayed feedback, position bias.
4. **Marketplace dynamics:** dispatch, ETA prediction, Dasher pay/pricing,
   supply-demand balancing, surge-like incentives.
5. **Experimentation:** A/B design for marketplaces (interference/SUTVA
   violations — treatment leaks across the two sides), interleaving,
   guardrail metrics.
6. **Production ML:** training–serving skew, feature pipelines, point-in-time
   correctness, monitoring/drift, reliability and scaling (the Module 2 graded
   dimensions verbatim).
7. **Practical coding fluency with AI editors:** practice one 60-min session in
   Cursor/Claude Code with screen share on a realistic business-logic problem
   (e.g., payout/pricing computation with edge cases).

## Company-specific themes

- **Three-sided marketplace:** every model decision touches consumers,
  merchants, and Dashers — incentives and fairness across sides are first-order
  design constraints, not footnotes.
- **Last-mile logistics:** dispatch, batching, ETA, routing — real-time
  optimization with hard latency budgets.
- **Multi-vertical expansion:** the strategic bet — one app for food, grocery,
  retail. Their published work on bridging behavioral silos across verticals is
  the clearest public signal of where recsys investment is going.
- **Ads as profit engine:** conversion modeling in a delivery context (delayed
  outcomes, sparse conversions, merchant-side value).
- **Operational excellence:** DoorDash culture prizes operators; the Values
  round will probe ownership and bias for action with real receipts.

## Likely system-design domains

REPRESENTATIVE PRACTICE (not reported as asked — do not claim otherwise):

1. Design the home-feed recommendation system for a multi-vertical delivery app
   (food + grocery + retail): retrieval, ranking, bridging cross-vertical
   behavior.
2. Design an ads conversion prediction system for last-mile delivery: features,
   delayed labels, calibration, serving at scale.
3. Design ETA prediction for deliveries: data, features, model, monitoring.
4. Design a Dasher dispatch/matching system: real-time constraints, batching,
   pay computation.
5. Design the ML platform pieces: feature pipelines with point-in-time
   correctness, experimentation infra handling marketplace interference,
   model monitoring and rollback.
6. Your Coupang search-ranking stack, reframed for DoorDash's catalog: what
   transfers, what changes with three-sided dynamics.

Use the 18-step framework in [#/ml-system-design](#/ml-system-design).

## Project deep-dive emphasis

The Domain Knowledge round will likely pull on your background — prepare:

- **Coupang search ranking end-to-end** (query rewriting → retrieval →
  multi-stage ranking → LLM discovery), with a DoorDash translation ready:
  "here's how I'd adapt this to multi-vertical recommendations."
- **One ads/pricing-adjacent story** if you have it; otherwise frame ranking
  metric work (NDCG → business metric) as the analogue.
- Decisions with rejected alternatives, scale numbers, the thing that almost
  failed, measured impact.

Full prep: [#/project-deep-dive](#/project-deep-dive).

## Recent work worth knowing

1. **"Mind the Gap: Using LLMs to bridge behavioral silos in multi-vertical
   recommendations"** — DoorDash engineering blog, Dec 3, 2025; RecSys 2025
   paper. Directly relevant to the Domain Knowledge round if your domain is
   recsys: [careersatdoordash.com](https://careersatdoordash.com/blog/doordash-llms-bridge-behavioral-silos-in-multi-vertical-recommendations/)
2. **"Deep learning for ads conversion in last-mile delivery"** — arXiv, Feb
   2025: [arxiv.org/abs/2502.10514](https://arxiv.org/abs/2502.10514)
3. **Personalized cuisine filter** — DoorDash engineering blog (product-side ML
   personalization): [careersatdoordash.com](https://careersatdoordash.com/blog/personalized-cuisine-filter/)

Dropping one informed reference ("I saw your RecSys '25 work on bridging
behavioral silos across verticals — is that the team's direction for the home
feed?") signals genuine interest and gives the interviewer a thread to pull.

## Practice questions

All REPRESENTATIVE PRACTICE — modeled on the prep kit's stated dimensions and
marketplace-ML patterns, not claimed as asked.

**Domain Knowledge (Round 1 — highest priority):**
- [ ] Design ranking for DoorDash's home feed across food, grocery, and retail.
      How do you handle users whose behavior is siloed in one vertical?
- [ ] How would you use LLMs to bridge behavioral silos in multi-vertical
      recommendations? (Their RecSys 2025 direction — have a real opinion.)
- [ ] Walk through your Coupang ranking stack. Which pieces transfer to
      delivery recommendations, and what breaks?
- [ ] Design an experiment for a new ranking model when treatment leaks across
      consumers and merchants (marketplace interference). How do you measure
      the true effect?
- [ ] How do you correct for position bias in delivery-app click data? Compare
      IPS, two-tower, and randomization approaches.
- [ ] Sparse conversions, delayed labels: design the label pipeline and loss
      for an ads conversion model in last-mile delivery.

**AI Code Craft (prep for the loop):**
- [ ] Implement Dasher payout computation with surge multipliers, tips, and
      edge cases (mid-delivery cancellations, stacked orders) — with an AI
      editor, narrating your prompts and verifying its output.
- [ ] Given a stream of delivery events, compute per-merchant rolling prep-time
      estimates with late/out-of-order data.

**ML System Design (prep for the loop):**
- [ ] Design the feature pipeline for ETA prediction: streaming vs batch,
      point-in-time correctness, freshness SLAs.
- [ ] Your ranking model's offline NDCG improved but the A/B is flat — debug
      live, hypotheses in priority order.
- [ ] Design model monitoring for a dispatch model: what drifts, what pages
      you at 3am, rollback gates.

**Values/HM (prep for the loop):**
- [ ] Tell me about a time you owned an outcome end-to-end with incomplete
      data. Map it to a DoorDash Principle.
- [ ] Describe a disagreement with a partner team (product/ops) over an ML
      decision. How did it resolve?

## 30-minute checklist

Before Oct 7, 1:00 PM:

- [ ] **Email Noe Perez (5 min):** confirm which domain the ML Domain Knowledge
      round will cover.
- [ ] **RecSys paper (10 min):** read the "Mind the Gap" blog/abstract; write
      3 sentences of opinion on LLM-bridged multi-vertical recs.
- [ ] **Domain narrative (10 min):** rehearse the 5-minute Coupang ranking
      walkthrough with the DoorDash translation ("what I'd change for
      multi-vertical delivery").
- [ ] **Interference answer (5 min):** one crisp paragraph on marketplace
      experiment design under SUTVA violations — the most likely "business
      case" trap.
- [ ] Skim [#/cram-30min](#/cram-30min) sheets 3 (ranking), 5 (experiment),
      6 (production ML).
