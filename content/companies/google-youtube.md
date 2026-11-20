---
title: "Google / YouTube — Staff Applied ML SWE, Recommendations: Phase 1 (Fri 2026-12-11, virtual)"
slug: "google-youtube"
section: "companies"
nav_order: 83
nav_label: "Google / YouTube"
tags: ["system-design", "recsys", "behavioral", "deep-dive", "interviewing"]
updated: "2026-11-20"
company: "Google / YouTube"
priority: "p0"
status: "interviewing"
process_sources:
  - { label: "OFFICIAL", url: "", accessed: "2026-11-20", note: "Rui's own loop (emails + calendar, verified 2026-11-20): application submitted Nov 16 for Staff Applied ML SWE, Recommendations, YouTube (San Bruno); recruiter Kyle Richey (kylerichey@google.com); reference Yunsong Guo (Director of Eng, Search). Google Hiring Assessment PASSED Sep 10, 2026 (24-month validity). Google NDA SIGNED Nov 17 via DocuSign. Coordinator Sobha Hamsitha Kalavakolanu (sobhah@xwf.google.com, Randstad Sourceright) confirmed Phase 1 on Fri Dec 11, 2026: Interview 1, 13:00-13:45 PT (Meet sbs-esce-aep) and Interview 2, 14:30-15:30 PT (Meet ydc-aohp-wdy + a shared Google Doc to open alongside). Interviewer names and round types were NOT stated in the scheduling email. Earlier process intel (recruiter chain, Nov 2026): Phase 1 = ML Recommendations Architecture (60m) + Technical Leadership (45m); Phase 2 in person = ML Recs Architecture 60m + Coding 45m x2. The Dec 11 durations (45m + 60m) are consistent with that shape — mapping below is INFERRED from durations, not confirmed." }
  - { label: "OFFICIAL", url: "https://d3no4ktch0fdq4.cloudfront.net/public/course/files/Google-Interview-Prep-Guide-Business_Interviews.pdf", accessed: "2026-11-20", note: "Google's own Interview Prep Guide: interviewers assess four attributes — General Cognitive Ability, Leadership, Role-Related Knowledge, Googleyness — via behavioral ('Tell me about a time when...') + hypothetical questions; Google recommends STAR and preparing several examples per attribute. Leadership explicitly includes mobilizing others when you were NOT officially the leader. No brain teasers." }
  - { label: "OFFICIAL", url: "https://research.google.com/pubs/archive/45530.pdf", accessed: "2026-11-20", note: "Covington, Adams & Sargin, 'Deep Neural Networks for YouTube Recommendations', RecSys 2016 — the canonical public description: two networks (candidate generation as extreme multiclass classification over millions, hundreds retrieved; ranking with rich user-item features), ranking objective = expected watch time per impression via weighted logistic regression (NOT CTR: 'often promotes deceptive videos that users do not complete'), Example Age feature for freshness, offline metrics guide iteration but live A/B decides. Describes the system at publication time, not today's stack — use as the defensible design foundation." }
  - { label: "OFFICIAL", url: "https://daiwk.github.io/assets/youtube-multitask.pdf", accessed: "2026-11-20", note: "Zhao et al., 'Recommending What Video to Watch Next: A Multitask Ranking System', RecSys 2019 — Wide & Deep + MMoE (per-task gates over shared experts) over engagement tasks (clicks, watch time) and satisfaction tasks (likes, dismissals, ratings); selection/position bias handled by a shallow tower that takes position x device and is treated as missing at serving (10% position dropout in training); reported +0.45% engagement / +3.07% satisfaction vs shared-bottom in live experiments." }
  - { label: "OFFICIAL", url: "https://dl.acm.org/doi/10.1145/3298689.3346996", accessed: "2026-11-20", note: "Yi et al., 'Sampling-Bias-Corrected Neural Modeling for Large Corpus Item Recommendations', RecSys 2019 — YouTube's two-tower retrieval: in-batch negatives are biased under popularity skew; fix = streaming estimate of item frequency + logQ sampling-bias correction. Validated in live A/B on YouTube." }
  - { label: "REPORTED", url: "https://www.1point3acres.com/bbs/thread-988481-1-1.html", accessed: "2026-11-20", note: "1point3acres searched FIRST (standing rule) on 2026-11-20: NO readable 2025-2026 report for Google YouTube Staff/L6 MLE Phase 1, ML Recommendations Architecture, or Technical Leadership exists there. The site's 2025 Google ML interview-database entries (threads 1161213, 1135566, 1141654, 1113681) are login-gated ('Please log in to view interview details'); index snippets show fraud-detection design / new-grad / DeepMind topics — none YouTube, none Staff. The one fully readable thread (988481, 2022, HR screen) only confirms the generic prep handout: G&L questions start 'Tell me about a time when...', prepare STAR, most questions are under-specified so clarify first. 面经 for this loop therefore rests on the aggregators + Google's own papers below — labeled as such everywhere on this page." }
  - { label: "REPORTED", url: "https://www.interviewquery.com/guides/google-ml-engineer", accessed: "2026-11-20", note: "InterviewQuery Google MLE guide (updated 2026-11-16, synthesized from 10 candidate reports): the loop is NOT uniform — ask the recruiter what the team's loop is. ML domain round reported: a single resume project drilled end to end (lifecycle, decisions, math, tradeoffs, complexity, how you communicated it). ML system design reported: for a senior candidate, an open-ended discussion tied to challenges the team is actively facing, in a recommendation domain; you drive the structure and explain tradeoffs. After the loop: hiring committee + team match." }
  - { label: "REPORTED", url: "https://www.datainterview.com/courses/google-machine-learning-engineer/youtube-recommendations", accessed: "2026-11-20", note: "DataInterview YouTube-recommendations worked lesson (updated 2026-10-12; explicitly 'a design you could defend in an interview, informed by the papers, not a description of today's YouTube'): home feed (no query, history only) vs watch-next (conditioned on current video) changes the model; worked assumptions 500M DAU, 10M-video index, 200 ms server budget, 500 candidates to ranker. Its follow-up cluster list and L4/L5/L6 differentiators are quoted on this page as expert guidance, NOT a Google rubric (its own label)." }
  - { label: "REPORTED", url: "https://www.hellointerview.com/guides/google/l6", accessed: "2026-11-20", note: "Hello Interview Google L6 guide: onsite ~5-6 rounds; for ML roles one coding round can be replaced by a domain round and there may be two ML design discussions; at L6 system design + leadership carry the most weight — coding well but showing only L5 design/strategy is a common down-level path. Its G&L description separates Technical Leadership & Initiative (multi-team efforts, influence without authority, architectural decisions, mentoring at scale) from Googleyness (ambiguity, bias for action, humility)." }
  - { label: "REPORTED", url: "https://gitgood.dev/prep/google-l6-swe", accessed: "2026-11-20", note: "GitGood L6 guide: 'L6 is where the bar shifts from great IC to multiplier'; the hiring committee explicitly evaluates 'has this person operated at staff scope before' — project-scope stories ('I shaped my team's roadmap') are below bar vs org-scope ('I shifted our org's technical direction'); leadership round probes cross-team technical strategy, senior-engineer disagreement, recovering from decisions that went wrong, influencing roadmaps without authority, mentoring senior ICs." }
  - { label: "REPORTED", url: "https://interviewlegend.com/guides/companies/google/behavioral/googleyness", accessed: "2026-11-20", note: "InterviewLegend G&L guide (search snippet readable 2026-11-20; page itself firewall-blocked): in 2026 reports G&L usually sits in the virtual first round, ~45 min, run by one Googler rarely from your future team. Most-reported prompt themes, in order: (1) ambiguity / requirements changed midway, (2) biggest professional mistake or a goal you missed, (3) disagreement with a colleague or manager (sometimes pushback from someone more senior), (4) conflicting priorities under a tight deadline, (5) someone taking credit for your work, (6) receiving (or giving) critical feedback." }
  - { label: "REPORTED", url: "https://www.fastprep.io/experience/google-swe-iii-ml-interviews-11-experiences-part-1-of-3-c2wxv27ku9", accessed: "2026-11-20", note: "FastPrep aggregate of 21 Google ML-track loops, Oct 2025 - Nov 2026 (mostly L4 — pattern evidence only, NOT YouTube/L6): ML system design in 8 of 21 reports, G&L in 16 of 21; no YouTube recommendations case among the detailed reports. Also reported: hiring committees sometimes request ADD-ON rounds (extra coding / G&L / technical) when one interview leaves them short of signal." }
---

## TL;DR

**Status: Phase 1 CONFIRMED — Fri Dec 11, 2026, virtual (Google
Meet). Interview 1: 13:00–13:45 PT. Interview 2: 14:30–15:30 PT.
Coordinator: Sobha Hamsitha Kalavakolanu; recruiter: Kyle Richey.
Role: Staff Applied ML SWE, Recommendations, YouTube (San Bruno).
GHA passed (Sep 10, 2026); NDA signed (Nov 17).**

:::warn
**Round-type mapping is UNCONFIRMED — read this first.** Sobha's
scheduling email did NOT name interviewers or round types. The
expected Phase 1 shape from earlier process intel is **ML
Recommendations Architecture (60 min) + Technical Leadership
(45 min)**, and the booked durations fit it exactly (45 + 60). The
natural mapping is Interview 1 (45m) = Technical Leadership and
Interview 2 (60m) = ML Recommendations Architecture — but that is
INFERRED from durations, and the reverse assignment (or a project
deep-dive / RRK variant) is possible. This page prepares both rounds
fully, plus a deep-dive fallback, so the order doesn't matter. When
Sobha or Kyle confirms the mapping, re-check this page the same day.
:::

**What wins Phase 1, in one line:** an architecture answer that is
literally YouTube's own published design — two-stage funnel,
watch-time objective, position-bias correction — driven at Staff
scope (you question the objective, sequence the build, price the
serving), plus leadership stories that are org-scope, not
project-scope. The #1 documented L6 failure mode is not weak tech;
it is **down-leveling because the evidence reads L5**: team-level
stories, waiting to be prompted in design, no cost/strategy layer.

**Your unfair advantage:** this is your home domain. Coupang search
ranking / generative retrieval and Pinterest search discovery *are*
candidate generation + ranking + evaluation at scale. The design
round asks you to redesign the system class you have run for a
decade — the prep below is about speaking it in YouTube's published
vocabulary and at Google's Staff bar, not learning a new field.

## Company & product

YouTube recommendations is the surface that decides most of what
2B+ users watch: home feed (no query — pure personalization from
history) and watch-next / Up Next (conditioned on the current
video). The public technical canon is three Google papers, and they
are the vocabulary of this interview:

- **Covington et al. 2016** — the two-network funnel: candidate
  generation as extreme multiclass classification (millions →
  hundreds), ranking with rich user×item features; objective =
  **expected watch time per impression**, explicitly not CTR.
- **Yi et al. 2019** — two-tower retrieval at corpus scale;
  in-batch negatives are popularity-biased; logQ correction.
- **Zhao et al. 2019** — multitask ranking: MMoE over engagement +
  satisfaction tasks; position bias quarantined in a shallow tower.

Know going in: these papers describe the system *at publication
time* (REPORTED caveat, DataInterview). Use them as the defensible
design foundation and say so if asked — "the current stack isn't
public; here's the design I'd defend and how I'd evolve it" is the
Staff answer, not a weakness.

## Role expectations

Staff (L6) Applied ML SWE on YouTube Recommendations, San Bruno.
What the bar is, per the L6 guides (REPORTED) and Google's own
attribute framework (OFFICIAL):

- **The four attributes are the scorecard:** General Cognitive
  Ability, Role-Related Knowledge, Leadership, Googleyness.
  Interviewers write independent feedback; a **hiring committee of
  Googlers who never met you** decides, and can down-level. Every
  answer must survive being summarized in a packet by someone who
  wasn't in the room — specific, quantified, org-scope.
- **Design + leadership carry the most weight at L6** (REPORTED,
  Hello Interview). Coding is Phase 2's problem (2× 45m, per earlier
  intel); Phase 1 is where level is set.
- **Staff scope = multiplier:** influencing technical direction
  across teams, owning ambiguous problems where the right approach
  isn't obvious, mentoring senior engineers, recovering from
  decisions that went wrong (REPORTED, GitGood/Hello Interview).

## Interview process

| # | Stage | Format | Status / source |
|---|-------|--------|-----------------|
| R0 | Application + recruiter chain — Kyle Richey; reference Yunsong Guo | Email | ✅ Submitted Nov 16 |
| R1 | Google Hiring Assessment | Online | ✅ Passed Sep 10, 2026 (valid 24 months) |
| R2 | NDA | DocuSign | ✅ Signed Nov 17 |
| R3 | **Phase 1 — Fri Dec 11, 2026** | **Virtual, 2 sessions** | **This page** |
| R4 | Phase 2 (expected) | In person: ML Recs Arch 60m + Coding 45m ×2 | INFERRED from earlier intel — not yet scheduled |

Inside Phase 1 (mapping INFERRED from durations — see the warning
in the TL;DR):

| Session | When | Length | Expected content | Source |
|---------|------|--------|------------------|--------|
| Interview 1 | 13:00–13:45 PT · Meet sbs-esce-aep | 45 min | Technical Leadership (G&L variant) | INFERRED |
| Interview 2 | 14:30–15:30 PT · Meet ydc-aohp-wdy + shared Google Doc | 60 min | ML Recommendations Architecture | INFERRED |

Logistics already in the calendar events: open the Meet link *and*
the shared interview document for Interview 2; if an interviewer
hasn't joined within 10 minutes, contact Sobha or
google-candidate-support@google.com; backup phone on file
+1 917-244-6633. Sobha's email also linked Google's tech-interview
guide (Google Drawings in Docs) — the architecture round is a
drawing-and-talking round, not a coding round.

Process facts worth knowing (REPORTED): the loop is **not uniform**
across Google (InterviewQuery, from candidate reports) — which is
why the mapping above stays labeled inferred. Hiring committees
sometimes request **add-on rounds** when one interview leaves them
short of signal (FastPrep aggregate) — a Phase 1 that spawns an
extra round is normal process, not a soft rejection.

## Priority 1 — ML Recommendations Architecture (the 60-min round)

The expected prompt family (REPORTED, convergent across guides that
present them as Google MLE prompts): **"Design the recommendations
on the YouTube home page"** / "Design an end-to-end recommendation
system for YouTube — candidate generation, ranking, feature
engineering, model architecture, serving infrastructure for
billions of daily recommendations." Variants: watch-next instead of
home; Shorts instead of long-form. No verbatim L6 leak was publicly
readable — 一亩三分地's 2025 entries are login-gated (see
process_sources); treat the prompt family as near-certain and the
exact wording as unknown.

**Minute 0–5 — clarify the surface, out loud.** The single highest-
leverage move: home feed vs watch-next changes the model. Home has
no query — personalization from history alone. Watch-next is
conditioned on the current video (session + seed item dominate).
Shorts changes the objective again (swipe-through, completion,
session depth). Ask, pick one (home is the default worked case),
and state your assumptions with numbers: ~500M DAU, ~10M-video
retrieval index (state yours), **200 ms server budget**, new uploads
recommendable within minutes (REPORTED worked assumptions,
DataInterview). Then drive — at L6 the interviewer should mostly be
asking follow-ups, not steering.

### The funnel — have this cold

1. **Candidate generation / retrieval — millions → hundreds.**
   Two-tower model: user tower (watch-history video IDs embedded
   and averaged — Covington tried sum/avg/max, averaging won;
   search tokens embedded/averaged; region/device embedded;
   demographics normalized) × item tower (content features), score
   = dot product, serving = **ANN nearest-neighbour search** over
   precomputed item vectors (softmax probabilities are *not* needed
   at serving — scoring reduces to NN search, which is what makes
   tens-of-ms latency possible). Training: extreme multiclass
   classification (predict next watch), sampled softmax with
   several thousand negatives + importance weighting. **Modern
   trap to name unprompted:** in-batch negatives are biased under
   popularity skew — popular items get over-penalized; the fix is a
   streaming item-frequency estimate + **logQ correction** (Yi et
   al. 2019). Run **multiple candidate sources in parallel** —
   two-tower ANN, co-visitation/co-occurrence lists, subscriptions,
   trending-by-region, fresh uploads — then merge, dedupe, filter
   watched/ineligible. A video retrieval drops can never come back;
   this stage is judged on **recall**, the next on ordering.
2. **Pre-ranking — ~10k → ~100–500.** A light, cheap model (GBDT /
   skinny MLP, can be distilled from the heavy ranker) on cheap
   features. REPORTED (Interview101 HC debrief): an answer that
   stops at two stages and omits this cascade is marked *failing*
   Role Knowledge. Name it, cost it, move on.
3. **Heavy ranking — hundreds scored with rich features.** The
   features retrieval can't afford: user×item crosses (watches from
   this channel, last watch of this topic, which source nominated
   the candidate and with what score, times already shown to this
   user). Hundreds of features; categorical embeddings sized
   ~log(cardinality), large vocabularies truncated; continuous
   features CDF-normalized to [0,1) plus square/sqrt transforms
   (Covington — a classic follow-up probe). Architecture: Wide &
   Deep → **MMoE multitask** (below).
4. **Re-ranking / slate.** Diversity caps (e.g. max N per creator
   per page), freshness slots, policy/eligibility, editorial pins —
   kept **outside the model** so they change without retraining
   (Google Rules of ML: separate the policy layer from ranking).

### The label — where the round is decided

- **Not CTR.** Covington, quotable: ranking by CTR "often promotes
  deceptive videos that users do not complete." Objective =
  **expected watch time per impression**.
- **Technique:** weighted logistic regression — clicked impressions
  weighted by their watch time, unclicked weight 1; at inference
  output **exp(logit)**, not sigmoid — the odds approximate expected
  watch time per impression. Know the arithmetic cold; it is *the*
  signature detail of this design.
- **Multitask extension (Zhao et al. 2019):** engagement tasks
  (click, watch time) + satisfaction tasks (like, dismiss, rating)
  in one model. Shared-bottom causes negative transfer when tasks
  conflict → **MMoE**: shared experts, a separate softmax gate per
  task. Predictions combined by weighted multiplication, weights
  tuned by A/B; pointwise loss for serving simplicity. Reported
  live deltas vs shared-bottom: +0.45% engagement, +3.07%
  satisfaction.
- **The L6 move — question the objective itself** (expert guidance,
  DataInterview's own label: industry practice, not a Google
  rubric): raw watch time is a noisy proxy that rewards clickbait
  and harms retention. Propose satisfaction labels (survey-derived
  scores), long-term holdbacks, and creator/content-quality
  guardrails *as part of the design*, not as an afterthought.

### Bias, freshness, cold start, exploration — the follow-up belt

These are the reported follow-up clusters (DataInterview's list,
near-verbatim). Have a 60-second answer for each:

- **"Your logs come from the current system. So?"** — position /
  selection bias: slot 1 gets clicks regardless of quality; training
  naively learns the old ranker's placement and locks in a feedback
  loop. Zhao fix: position (crossed with device) goes *only* into a
  shallow tower whose output adds to the main logit; 10% position
  dropout in training; position treated as missing at serving.
  Reported: +0.24% live engagement vs −0.07% for position as a
  normal main-model feature. Never let position be a crossed
  feature in the main model.
- **"How do new videos get recommended?"** — freshness stack:
  dedicated fresh-uploads candidate source; content features in the
  item tower so an unwatched video still gets a vector; hash
  buckets for unseen IDs; **Example Age** feature (Covington: feed
  the training example's age as a feature, set it to zero at
  serving, so the model stops under-ranking rising videos);
  frequent index rebuilds; read the user's last watches at request
  time; sequential/continuous training.
- **Candidate-generation training traps** (name them before asked):
  train on *all* watches including off-YouTube embeds, not only
  recommendation-driven watches, or new content can never surface;
  fixed number of examples per user so heavy users don't dominate;
  predict the *next* watch with history rolled back to before the
  label — no leakage from the source surface.
- **Cold start, users:** demographics/context priors (region,
  device, language — Covington), onboarding picks, session signals,
  regional popularity fallback for logged-out.
- **Exploration:** unseen videos have no labels and no reweighting
  recovers them — reserve a small traffic slice; per-slot risk
  budget (safe at top, explore lower); bandit framing
  (Thompson/UCB/ε-greedy) and how you'd price exploration cost vs
  long-term discovery.
- **"It's too slow — what levers?"** Parallel sources with
  timeouts (drop the slowest), cache user history + user-tower
  embedding, fewer candidates to the ranker, distilled/lighter
  ranker, shard the ranker. Walk a budget: e.g. history fetch ~15 ms
  + ANN ~10 ms + slowest parallel source ~25 ms + ranking 500
  candidates — land well inside 200 ms and say what degrades first.

### Evaluation — close the design with it

- **Retrieval:** Recall@K (K ≈ ranker depth, e.g. 500) on a later
  held-out week + ANN index recall vs exact search.
- **Ranking:** per-task AUC; watch-time-weighted pairwise loss
  (Covington's metric — best ranker 34.6% mispredicted watch time
  on next-day holdout in the paper).
- **Online:** offline numbers only *earn* an A/B. Decide on watch
  time per session + return/retention + satisfaction (dismissal
  rate, surveys); guardrails on latency, "not interested" rate,
  creator impression spread. **Dual framework** (REPORTED strong-
  hire marker, Interview101): session engagement vs 7-day return,
  with alerting when they diverge. Long-term holdbacks for
  retention/fatigue — the L6 answer includes them unprompted.

### Your bridges (Coupang/Pinterest → YouTube)

- Generative retrieval at Coupang ≈ candidate generation with
  learned item representations — say how Semantic IDs / tokenized
  retrieval compares with two-tower ANN (index freshness, ID
  cold-start, serving cost) instead of pretending they're identical.
- Search ranking skew discipline = the train/serve parity and
  position-bias stories above; Pinterest discovery = the
  multi-source candidate blend. Every YouTube mechanism above has a
  scar from your own systems — attach one number or one failure to
  each stage and the round reads as experience, not recitation.

## Priority 2 — Technical Leadership (the 45-min round)

**What this round most plausibly is** (INFERRED mapping, stated
plainly): Google does not publicly name a round "Technical
Leadership." The public names are **Googleyness & Leadership
(G&L)** and its L6 variant ("Googleyness++" / leadership & impact).
The recruiter's label most plausibly maps to the L6 G&L round —
~45 min, one Googler, rarely from your future team (REPORTED,
InterviewLegend). It formally evaluates two things (REPORTED, Hello
Interview):

- **Technical Leadership & Initiative** — leading multi-team
  technical efforts, influencing without authority, driving
  architectural decisions, mentoring engineers at scale.
- **Googleyness** — comfort with ambiguity, bias for action,
  collaborative mindset, humility, learning from failure, user
  focus — *at the strategic altitude expected of Staff.*

OFFICIAL anchor (Google's own prep guide): Leadership = how you
used communication and decision-making to mobilize others,
**including when you weren't officially the leader**; questions are
behavioral ("Tell me about a time when…") + hypothetical; prepare
several STAR examples per attribute.

### The bar: org scope, not project scope

The single most-cited L6 down-level trigger (REPORTED, GitGood +
Hello Interview + Assisted Voice, convergent): the hiring committee
asks "has this person operated at Staff scope before?" — and
**project-scope stories fail it.** Calibration, verbatim from the
guides: "I shaped my team's roadmap" is below bar; "I shifted our
org's technical direction" is in range. Every story you tell must
show at least one of:

- Impact **beyond your team** — multi-team/org systems, decisions
  other teams built on.
- **Influence without authority** — a roadmap or architecture call
  you moved across teams you don't manage, including engineers more
  senior than you who disagreed.
- **Technical strategy** — you set direction and *sequenced* it;
  tradeoffs made under incomplete information.
- **Recovery** — a decision (yours) that proved wrong, how you
  detected it, communicated it, and what changed. Google values the
  honesty explicitly (REPORTED, Codemia: "a technical decision that
  was later proven wrong" is a stock prompt; intellectual honesty is
  the scored trait).
- **Multiplication** — senior engineers you grew, standards you set
  that outlived your project.

### Most-reported prompt themes (2026 reports, REPORTED)

InterviewLegend's ordering of what G&L actually asked in 2026
reports — prepare a story for each, in this priority order:

1. **Ambiguity / requirements changed midway** (most reported theme)
2. **Biggest professional mistake, or a goal you didn't hit**
3. **Disagreement with a colleague or manager** (sometimes:
   pushback from someone *more senior*)
4. **Conflicting priorities under a tight deadline**
5. **Someone taking credit for your work**
6. **Receiving critical feedback** (some rounds flip it: giving it)

Plus the L6 leadership-round samples from Onsites.fyi (REPORTED):
"Tell me about a time you overhauled a legacy system — how did you
manage risk?" · "Describe a cross-org project you led from design
to delivery." · "How have you handled misalignment between
engineering and product priorities?" · "How do you scale your
influence as the org grows?"

### Story bank — build these six before Dec 11

Map each to a real episode from Pinterest / Meta / Coupang; STAR,
≤3 minutes each, ending on *what changed because of you*:

- [ ] **Org-direction story** — a technical direction you shifted
  beyond your team (e.g. the generative-retrieval direction at
  Coupang): who resisted, what evidence moved them, what the org
  does differently now.
- [ ] **Ambiguity story** — an under-defined problem you framed
  yourself and moved without waiting for permission.
- [ ] **Wrong-decision story** — a call that proved wrong; detection,
  disclosure, recovery, and the institutional fix. No blame-shifting;
  red flag in every guide: speaking negatively about past employers
  or colleagues.
- [ ] **Senior-disagreement story** — consensus built among senior
  engineers who disagreed, ideally including someone more senior.
- [ ] **Mentoring/multiplier story** — a senior engineer you grew
  toward Staff, or a standard (review bar, eval methodology) you set
  that other teams adopted.
- [ ] **Failure-under-pressure story** — conflicting priorities, a
  deadline, something that still went wrong, and what you learned —
  Google explicitly values stories where things went wrong over
  perfect stories (REPORTED, Hello Interview).

Delivery rules: credit the team while keeping your own decisions
visible ("I proposed/decided/drove" inside "we shipped"); quantify
scope (teams, engineers, traffic, revenue-adjacent metrics) so the
HC packet writes itself; never criticize a past employer — scope and
craft frustrations only.

## Priority 3 — If a session becomes a project deep-dive (fallback)

InterviewQuery's reported ML domain round is a **single resume
project drilled end to end** (REPORTED): lifecycle, technical
decisions, the math, tradeoffs, complexity, and how you communicated
it. If Interview 1 opens with "tell me about your work at Coupang,"
switch modes — this is scored RRK, not small talk.

- **Pick the flagship:** the Coupang generative-retrieval / search
  ranking work — closest in shape to YouTube Recs (corpus, index,
  serving, eval). Walk it as: problem & stakes → architecture with
  the data path → two hardest decisions and what you rejected →
  failure story → metrics before/after → what you'd rebuild today.
- **Pre-answer the probes:** Why this model family over the
  alternative? Where did offline gains fail to transfer online
  (skew)? What broke at 10×? Where did the platform end and the
  model begin? Who consumed your system and how did you prioritize
  them?
- **Five numbers, memorized** (same drill as every p0 page): corpus/
  index size, peak QPS, p99 latency and its split, one flagship
  offline→online delta, one cost figure. Deploy them in *both*
  rounds — they are also the leadership round's scope evidence.

## Questions to ask

For the architecture interviewer:
1. Where does the recommendations stack hurt most right now —
  retrieval quality, ranking capacity, or freshness of the index?
2. How is the objective evolving — where do satisfaction signals sit
  against watch time in the current ranking function?
3. What would this role own in its first two quarters: a surface, a
  stage of the funnel, or a platform piece?

For the leadership interviewer:
1. How are Staff engineers here expected to split time between their
  team's roadmap and org-level technical direction?
2. What does the team-match / project-assignment process look like
  after the hiring committee for this role?

For Kyle/Sobha (logistics, before Dec 11):
1. Can you confirm which session is which round type, and the
  interviewers' names? (Unblocks nothing — prep covers both — but
  ask once.)
2. Phase 2 shape and likely timing, given the holidays?

## Practice questions

- [ ] **Design cold-run #1 (timed, 60 min, out loud):** "Design the
  YouTube home page recommendations" — clarify surface, state scale
  + 200 ms budget, draw the funnel, land the label section without
  prompting. Record it; check you said *pre-ranking* unprompted.
- [ ] Design variant: same design as **watch-next** — narrate only
  what changes (seed-item conditioning, session features, candidate
  sources) in ≤ 10 min.
- [ ] Label arithmetic drill: derive expected watch time from
  weighted logistic regression (clicked weighted by watch time,
  exp(logit) at inference) on a whiteboard, ≤ 3 min, no notes.
- [ ] Bias drill: explain the Zhao shallow-tower fix and the
  +0.24% vs −0.07% contrast; then the logQ correction for in-batch
  negatives; each ≤ 2 min.
- [ ] Follow-up belt, 60 seconds each: Why two stages? · How do new
  videos surface? · Cold-start a new user? · Exploration budget —
  how priced? · Offline metric per stage? · Three latency levers?
- [ ] L6 layer drill: take your design and add, unprompted — the
  objective critique (satisfaction labels, holdbacks), the build
  sequence with experiment gates, and the cost line (candidates
  scored × ranker size vs serving cores).
- [ ] Leadership story bank: all six stories in Priority 2, timed
  ≤ 3 min each, each ending on an org-scope outcome sentence.
- [ ] Down-level audit: re-listen to your story recordings and flag
  any sentence whose scope is only your own team — rewrite or
  replace those stories.
- [ ] Deep-dive fallback: flagship Coupang project walk, 12 min
  version + 30 min version, with the five numbers embedded.
- [ ] Covington re-read (skim, 20 min): funnel + weighted logistic
  + Example Age — the three quotable mechanisms.
- [ ] Zhao re-read (skim, 15 min): MMoE gates + shallow-tower bias
  handling — be able to draw both from memory.
- [ ] "Why YouTube Recs, why now" in 3 sentences; "why leave
  Coupang" in 2 — pull toward the problem, never push away.

## Checklist — before & day of (Fri Dec 11, 2026)

**By Thursday night (Dec 10)**
- [ ] Round-mapping confirmation asked of Sobha/Kyle (one email);
  if it lands, re-check this page against it — prep covers both
  orders either way.
- [ ] Two timed design runs + story bank recorded and audited for
  project-scope sentences.
- [ ] Five numbers memorized; Covington/Zhao mechanisms drawable
  from memory.
- [ ] Google Drawings in Docs: open the shared interview document
  once to confirm access, and practice drawing the funnel in it —
  the design round is a drawing round.

**Friday (Dec 11)**
- [ ] Gym 8:00–9:30 as usual; lunch inside the 12:00–13:00 block —
  Interview 1 starts at 13:00 sharp, there is no buffer after lunch.
- [ ] 12:45: join-ready — Meet link for Interview 1
  (sbs-esce-aep) open, water, notes closed except this page's
  checklists. (The recurring Office Happy Hour on the calendar at
  13:00 is tentative — the interview owns the slot.)
- [ ] 13:45–14:30 break: reset; open Interview 2's Meet
  (ydc-aohp-wdy) **and** the shared Google Doc; re-read the
  follow-up belt (Priority 1) once.
- [ ] If an interviewer hasn't joined within 10 minutes: contact
  Sobha or google-candidate-support@google.com (per the scheduling
  email) — don't just wait.
- [ ] Same evening: write down interviewer names, the exact design
  prompt wording, and every follow-up asked, while fresh — they set
  up Phase 2 prep (and any HC add-on round).
