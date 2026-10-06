---
title: "Anthropic — Staff Software Engineer, Search (OA passed 2026-10-06)"
slug: "anthropic"
section: "companies"
nav_order: 80
nav_label: "Anthropic"
tags: ["llm", "system-design", "deep-dive", "interviewing", "research", "safety", "search", "values", "swe"]
updated: "2026-10-06"
company: "Anthropic"
priority: "p0"
status: "interviewing"
process_sources:
  - { label: "REPORTED", url: "https://github.com/amitgaur/ai-interviewing/blob/HEAD/research/anchor-anthropic.md", accessed: "2026-10-01", note: "Researched 2026-04-16: recruiter screen → CodeSignal take-home (~90m, 4 escalating levels; e.g. in-memory DB → filtered scans → TTL → compression) → HM 1:1 → virtual onsite (~4h, 4 rounds: coding, system design e.g. distributed search 1B docs/1M QPS, safety/ethics behavioral) → references; values round is a hard gate" }
  - { label: "REPORTED", url: "https://www.finalroundai.com/blog/anthropic-interview-process", accessed: "2026-10-01", note: "SWE = 2 coding + system design + values; MLE/RE = lighter coding + 1-2 ML deep rounds + research presentation/take-home + values" }
  - { label: "OFFICIAL", url: "https://www.anthropic.com/candidate-ai-guidance", accessed: "2026-10-01", note: "Anthropic's official AI-use policy for candidates — read before interviewing" }
  - { label: "REPORTED", url: "https://www.1point3acres.com/bbs/thread-1190157-1-1.html", accessed: "2026-10-06", note: "1point3acres 2026 compilation (25 posts, updated ~Oct 2): OA is build-a-system multi-stage not LeetCode; recruiter screen digs why-Anthropic + AI safety ~20 min and fails shallow answers; senior+ tech phone often starts with SD; onsite 4-5 rounds; 2026 new rounds: agentic coding (Claude Code on real repo), network debugging role-play; slow — 2-3 weeks between rounds, 1-2 months total; template rejections, no feedback; team match after pass" }
  - { label: "REPORTED", url: "https://www.interviewquery.com/guides/anthropic-software-engineer", accessed: "2026-10-06", note: "OA (90-min proctored, 4 progressive levels) → live 90-min CodeSignal screen → final loop; references contacted at multiple points in parallel with interviews" }
  - { label: "REPORTED", url: "https://medium.com/@mockingbird_71808/a-breakdown-of-anthropics-5-round-swe-loop-073723fde2ca", accessed: "2026-10-06", note: "2026-06-29: recruiter screen → 90-min OA → HM deep-dive → two-part virtual onsite on different days (part 2 only if part 1 passes); breadth across coding/SD/project ownership/ethical reasoning; AI assistance prohibited in all live rounds" }
  - { label: "REPORTED", url: "https://www.tryexponent.com/experiences/anthropic-senior-software-engineer-interview-2ffa5f", accessed: "2026-10-06", note: "Senior SWE Safeguards 2026: onsite = HM + coding + company values + SD + coding; values round run by nontechnical people 'like a therapy session' probing feelings; prep behaviorals harder than technicals; skepticism beats generic 'I love your mission'" }
  - { label: "REPORTED", url: "https://medium.com/@hack2hire.share/what-anthropic-actually-tests-and-what-gets-candidates-rejected-2026-2726b802f250", accessed: "2026-10-06", note: "Analysis of 15 firsthand 2026 reports: coding gate is library fluency (PIL/concurrency), narrated testing scored explicitly; SD is written Google-Doc 'Prompt Playground' (no diagrams), hold your structure vs aggressive pacing; values round needs a NAMED Anthropic value + personal history + critique of Anthropic tradeoffs; project retro is 20-min candidate-driven + adversarial challenge; <24h rejection = technical fail, 2-3 days = culture/HM fail" }
  - { label: "OFFICIAL", url: "https://interviews.modernloop.io/o/anthropic/a/92e4eede-69eb-4c49-9994-d831e77e1a74", accessed: "2026-10-06", note: "Candidate portal (logged in): no values/fit questions or rubrics published — only the 7 guiding principles, NDA + AI-usage policy; recruiter screen rescheduled to Thu Oct 8, 11:30 AM PT" }
  - { label: "REPORTED", url: "https://github.com/schuture/anthropic-interview-notes", accessed: "2026-10-06", note: "Curated 2026 aggregation (culture README + recruiter-screen README): ~30 deduped values questions incl. RSP-change tradeoff, breakthrough-delay hypotheticals, authority pushback, persuadability, moral-revision stories" }
  - { label: "REPORTED", url: "https://www.tryexponent.com/experiences/anthropic-senior-software-engineer-interview-2ffa5f", accessed: "2026-10-06", note: "Verified firsthand SWE Safeguards debrief (Jan 2026 interview): verbatim values questions ('against your values' + feelings drill-down, feedback on mission), 'bullish on Anthropic' flagged at recruiter screen" }
  - { label: "REPORTED", url: "https://www.interviewing.io/anthropic-interview-questions", accessed: "2026-10-06", note: "2026 conversations with Anthropic engineers: neutral interviewers, 3-4 level follow-ups, rehearsed answers read as 'clean, complete, emotionally flat'; references probed on conflict/ethical friction" }
  - { label: "REPORTED", url: "https://www.livemint.com/news/world/mission-vs-profit-at-anthropic-a-former-employees-account-of-the-tech-firms-interview-process-11761758121433.html", accessed: "2026-10-06", note: "Axios reprint: Blind poster rejected after answering equity-to-zero hypothetical with money as headline; two ex-employees dispute the question's exact use" }
  - { label: "REPORTED", url: "https://www.1point3acres.com/bbs/thread-1190157-1-1.html", accessed: "2026-10-06", note: "2026 summary thread: 4 dated HR-screen reports (Anthropic-vs-other-labs, past-work-vs-safety, company news, risk/benefit, underrated problem); 10-yr candidate rejected for shallow safety answers" }
  - { label: "REPORTED", url: "https://www.glassdoor.com/Interview/Anthropic-Interview-E8109027.htm", accessed: "2026-10-06", note: "2026 SWE reports: OA is 4-stage same-problem build-up (OOP, refactors); onsite = phone screen + code screen + Coderpad + SD + presentation + ethical AI; reported questions: 'what ways do you disagree with our AI approach?', effective-altruism beliefs, 'design a chat app'; even max OA score doesn't guarantee human review" }
---

## TL;DR

**Status: CodeSignal pre-screen passed 2026-10-06 (a day early); Anthropic
NDA signed and acknowledged. Next: recruiter call with Yulia Serhiyenia,
Thu 2026-10-08 11:30–11:50 AM PT** (moved from Wed 10/7 by you; new Meet
link on the calendar event).

The two gates that eliminate the most qualified candidates are **not**
technical — they're the recruiter screen (why-Anthropic + AI safety depth)
and the values round (demonstrated, not stated, alignment). Prepare those
first; the technical rounds reward practical engineering over LeetCode.

:::warn
OFFICIAL: **no AI assistance in any live round** —
[anthropic.com/candidate-ai-guidance](https://www.anthropic.com/candidate-ai-guidance).
Violating it is an instant fail. Prep solo, think solo.
:::

## The process at a glance

OA ✅ done (90 min, 4 progressive build-a-system levels — "get it built,
running, handle edge cases"). Everything below is REPORTED BY CANDIDATES
(Oct 2026 refresh).

| # | Round | Format | What actually decides it |
|---|-------|--------|--------------------------|
| R0 | Recruiter / HR screen | 20–30 min video | **GATE #1** — why-Anthropic + AI safety, answered with depth |
| R1 | Technical phone | 60–90 min | Senior+: usually **SD first** (search/inference); else practical coding |
| R2 | HM deep-dive | 45–60 min | Scope & influence at staff level; team fit |
| R3 | Coding × 1–2 | 45–60 min each | **Library fluency** (PIL, concurrency) + narrated testing |
| R4 | System design | 50–55 min | Depth on requirements/schema/scaling; written or whiteboard |
| R5 | Project deep-dive | 45–60 min | 20-min driven presentation + adversarial defense |
| R6 | Values / culture | 45–60 min | **GATE #2** — demonstrated alignment, named values, real tradeoffs |

The onsite is split into **two parts on different days** — part 2 is only
scheduled if part 1 passes [REPORTED]. 2026-new round types seen on some
loops: **agentic coding** (real repo, Claude Code, produce a PR) and
**network debugging role-play**. Possible, not certain.

## Company & role in one paragraph

Anthropic (Claude) — safety-first research culture: **Constitutional AI**,
interpretability as a research *program*, and unusually good engineering
writing (e.g. "Demystifying evals for AI agents": most agent failures are
broken harnesses, not weak models). For **Staff SWE, Search**: the staff
bar is **scope and influence**, not just depth — expect R2/R5 to probe
technical direction-setting across teams, quality bars, and cross-team
disagreements. Your Coupang tech-lead story (Search & Discovery, generative
retrieval, multi-stage ranking) is the anchor for the whole loop.

---

## R0 — Recruiter / HR screen · GATE #1

**Format:** 20–30 min video (your intro call with Yulia, Thu 10/8
11:30 AM, is the opening of this stage; the substantive screen may be
the same call or scheduled right after). **What they're testing:** whether you've actually
thought about *this* lab — ~20 min of why-Anthropic + AI safety deep-dive
[REPORTED]. A 10-year candidate failed here for shallow answers.

**How to answer — the 2-minute why-Anthropic.** Structure it in four
beats. Below each beat is an angle from *your* background — make it yours,
don't memorize a script:

1. **Personal hook (30s)** — one moment where safety/reliability *cost*
   you something real. Yours: holding back the Coupang generative-retrieval
   launch when offline metrics hid a training–serving skew (your 5th Layer
   story). "Choosing measurement honesty over shipping" is a lived value,
   not a slogan.
2. **Why this lab, not others (45s)** — name *specific* things:
   Constitutional AI as a research program (RLAIF, the critique loop), the
   interpretability agenda ("what is the model actually doing" as a
   first-class question), the evals culture. Contrast without trashing
   others.
3. **What you'd build (30s)** — tie to Search: abuse-resistant retrieval,
   eval rigor for RAG. "I'm allergic to metrics that lie."
4. **Honest tension (15s)** — one thing you're genuinely unsure about
   (open vs. closed, pace of deployment). Skepticism signals thinking;
   pure praise signals rehearsal.

:::collapse How to answer each safety question (2026 reported set)
- **"What does AI safety mean to you, personally?"** — Don't define the
  field; narrate *your contact* with it: "In ranking I've lived the mild
  versions — reward hacking (the model games the click objective), eval
  gaming (offline metrics that don't predict online), feedback loops
  (ranking shapes the data it trains on). Safety at scale is those failure
  modes with higher stakes and less reversibility." Then: where you think
  the hard problems are — deployment, misuse, concentration of power.
- **"How is Anthropic different from other AI labs?"** — Research-led
  safety (interpretability as a *program*, not a team), public technical
  writing, measured deployment posture. Cite one artifact you actually
  read (a paper or engineering post).
- **"What happens if AI is misused?"** — Walk a mechanism, not slogans.
  Your domain: search/ranking manipulation — adversaries manufacture
  engagement signals (click farms, content farms tuned to the ranker); at
  LLM scale, prompt-injection in indexed content and corpus poisoning.
  "The system millions trust to tell them what's true becomes a
  manipulation surface." Then one mitigation direction (adversarial evals,
  provenance).
- **"Biggest risks and benefits of advanced AI?"** — Two-sided, specific,
  personal: which risk worries *you* most given what you've built, and
  which benefit motivates your work.
- **"React to a recent Anthropic announcement."** — Skim the blog/newsroom
  the week of the interview. Bring one take with an argument *and* a
  counter-argument.
- **"What ways do you disagree with our AI approach?"** — Honest, with
  reasoning. Example angle (make it yours): "I worry caution can become a
  brand story — does the interpretability agenda cash out into deployment
  decisions, or stay a research program while the product ships anyway? I
  don't have the answer; that's a reason to be inside the room."
- **"If we abandoned AI ambitions for safety and the stock went to zero,
  how would you feel?"** (Axios-reported culture question) — There's no
  right answer; they're testing whether you've thought about the tradeoff.
  Honest version: "I'd be disappointed — lying otherwise would be fake —
  but a lab that won't sacrifice revenue for safety isn't the lab I signed
  up for. What I'd want is to understand the reasoning, not just the
  outcome."
:::

**Prep checklist:**
- [ ] Read Anthropic's **Core Views on AI safety** (official site) +
  Constitutional AI one-pager (critique loop, RLAIF, failure modes)
- [ ] Write your 2-minute why-Anthropic (four beats above); say it out
  loud once — specific > sweeping
- [ ] Prepare one dual-use walkthrough (search/ranking manipulation) and
  one recent-news take (argument + counter-argument)
- [ ] Rehearse the equity-to-zero question in your own honest words

**Failure modes:** generic "I love your mission"; zero Anthropic-specific
knowledge (no paper/post/product detail); treating safety as compliance;
unable to name a genuine disagreement.

---

## R1 — Technical phone

**Format:** 60–90 min. For senior+ this is **often system design first**
[REPORTED] — inference/search-flavored. Otherwise practical coding in the
OA spirit (log parsing, file dedup, concurrent crawler). Interviewers tend
to be quiet; it reads as evaluation, not collaboration.

**What they're testing:** can you do the actual job's core work under mild
pressure — production-flavored design or build-and-extend coding.

**How to handle it:**
- If SD: open with 5 min of clarifying questions (read/write mix, scale,
  latency budget, freshness SLA) before drawing anything. Then use the
  R4 search framework below — the phone SD is usually a narrower slice of
  it (e.g. "design the indexing pipeline" or "design inference batching").
- If coding: state the plan first ("I'll walk the tree, hash in chunks so
  I don't load whole files, then..."), then code. Narrate continuously.

**Prep checklist:**
- [ ] Search SD framework (R4) — be able to whiteboard the 8 steps from
  memory
- [ ] Inference batching numbers: batching vs. latency tradeoff, KV-cache
  memory math (see R4 worked example)
- [ ] Concurrent crawler: sync version → async version, thread-safe
  visited set

---

## R2 — HM deep-dive

**Format:** 45–60 min with the hiring manager. **What they're testing:**
staff-level scope and influence, technical taste, team fit. Note: the HM
can appear **cold or disengaged** — that's reported as normal, not a
signal. Poor team fit here can block an offer regardless of earlier rounds.

**How to answer — prepare 3 scope & influence stories** (not just
technical wins). For each: situation → your call → who you had to convince
→ what happened → what it cost:

1. **Set a technical direction** — yours: the Coupang generative-retrieval
   bet as tech lead. What the options were, why you chose it, who
   disagreed, what happened.
2. **Resolved a cross-team disagreement** — incentives in conflict
   (e.g. another team optimizing for ship velocity vs. your quality bar).
   How you reasoned, not just the outcome.
3. **Raised a quality bar / held a launch** — the 5th Layer hold-back
   works here too; emphasize the *organizational* courage, not just the
   technical finding.

Plus:
- **30-second "what I want to build" pitch** — Search direction + why
  you're the person (feeds team-match later).
- **3 questions for the HM**: team roadmap for the next year, what
  "great" looks like for staff on this team, the biggest risk to the
  team's mission right now.

**Prep checklist:**
- [ ] Write the 3 stories with the beats above; 90-sec and 5-min versions
- [ ] 30-sec pitch out loud once
- [ ] 3 HM questions ready (genuinely curious ones — they can tell)

---

## R3 — Coding rounds × 1–2

**Format:** 45–60 min each, live coding (Coderpad-style). 2026
high-frequency: **file deduplication**, **image processing pipeline**,
**concurrent crawler**. You may get **no test cases** and have to fix your
own environment issues — practice debugging blind. TypeScript sometimes
allowed.

**What they're actually testing** (15-report 2026 analysis): **library
fluency, not algorithms** — PIL/Pillow and Python concurrency primitives
are the gate; pure LeetCode prep doesn't transfer. And **narrated testing
is scored explicitly**: thinking aloud while verifying beats a silently
completed solution.

**How to work each drill** (45–60 min each, blind, no harness):

:::collapse Drill 1 — File deduplication
Say the plan first: "I'll walk the tree with os.walk, hash each file in
chunks (don't load multi-GB files whole), map hash → paths in a dict,
report groups with >1 path." Edge cases to call out: empty files (all
hash equal — decide policy), "no duplicates → no output" (this exact edge
failed a candidate who needed a hint), symlinks, permission errors.
Then: "now concurrent" — ThreadPoolExecutor (IO-bound), thread-safe
result collection; mention why threads not processes here, and where you'd
switch (CPU-bound hashing at scale). Also be ready for "cpu/io related"
follow-ups [REPORTED].
:::

:::collapse Drill 2 — Image processing pipeline
PIL resize/rotate on a batch — **say the output dimensions out loud as
you go** (interviewers probe this; one candidate argued a full round over
it). Then batch loop → add multiprocessing → harden against corrupt
files (try/except per file, log-and-continue, don't kill the batch).
Follow-ups stack: pipeline parallelism on top of multiprocessing.
:::

:::collapse Drill 3 — Concurrent crawler
"Given a helper that crawls a URL": BFS with a queue, same-hostname check
via urlparse, strip fragments, dedupe via visited set. Write single-thread
first, then convert: ThreadPoolExecutor + lock around the visited set, or
asyncio + semaphore. Call out politeness/robots only if asked — don't
gold-plate.
:::

**Working discipline (this is scored):** think aloud the entire time —
"I'll do X because Y". Run tiny tests as you go and narrate results.
When stuck, say what you'd check next. Clean names, small functions.

**Prep checklist:**
- [ ] Each drill once, timed, blind (no test harness), narrating out loud
- [ ] PIL quick-ref: resize/rotate/convert sizes — know the API cold
- [ ] concurrency quick-ref: ThreadPoolExecutor, locks, asyncio.Semaphore

---

## R4 — System design

**Format:** 50–55 min. Two possible shapes: classic whiteboard, or the
2026 "Prompt Playground" — a **written Google-Doc discussion, no diagrams
expected or evaluated**. Either way they go **deep on one topic**
(requirements → schema → scaling), not broad. The interviewer may drive
pacing aggressively — **hold your own structure**; deferring to their
rhythm is how candidates drop requirements/scaling depth.

**Time allocation:** 5 min clarifying → 5 min high-level → 25 min deep
dive (pick the hardest part) → 10 min failure modes → 5 min evals.

### The search round — 1B docs, 1M QPS, p99 < 100ms (reported example)

Your home turf. Walk it with arithmetic, not adjectives:

1. **Scope:** read-heavy? write rate? freshness SLA (seconds vs minutes)?
   Query mix (head/torso/tail) — the tail decides the architecture.
2. **Indexing pipeline:** crawl/ingest → parsing → tokenization →
   inverted index build; batch vs. streaming updates; segment merges.
3. **Sharding:** document sharding (scatter-gather, tail latency) vs. term
   sharding (hot-term skew); hybrid. Shard count from QPS ÷ per-shard QPS.
4. **Replication & consistency:** N replicas for QPS; freshness lag budget
   per replica; what "stale" means to the user.
5. **Caching layers:** query-result cache (head), posting-list cache,
   ranking-feature cache; invalidation on index updates.
6. **Retrieval → ranking:** candidate gen (BM25/ANN) → multi-stage
   ranking; where the LLM/reranker sits and what it costs; cross-shard
   top-k merge with score normalization.
7. **Failure & tail:** hot shards, slow-shard hedging, graceful degradation
   (fewer stages under load), load shedding, backpressure.
8. **Evals/observability:** relevance metrics, latency histograms, index
   health, A/B infra.

Follow-up traps: hot-term skew, freshness-vs-TTL tension, hedging cost,
what breaks first at 10×.

### Inference batching — worked numbers (2026 canonical question)

"Single GPU, up to 100 inputs/batch, users submit synchronously and wait."
What they want: queueing under random arrivals (Little's law), the
batching↔latency tradeoff **with numbers**, KV-cache memory math, load
shedding — not just the happy path.

KV-cache intuition to have ready (70B-class, fp16): per token ≈ 2 ×
layers × hidden × 2 bytes ≈ 2×80×8192×2 ≈ **2.6 MB/token**. 100
concurrent sequences × 2k tokens ≈ **520 GB** — doesn't fit one GPU.
*That's* why batching strategy, chunked prefill, and paged attention
exist. Say this arithmetic out loud; it's the whole point of the
question.

### Design-doc review drill (2026 trend)

You're handed a doc and asked to find holes. Lens: unstated assumptions,
missing failure modes, gameable metrics, scaling cliffs, "what would you
measure first." Practice on one of your own design docs.

**Prep checklist:**
- [ ] Search framework: full walkthrough with numbers, out loud, 40 min
- [ ] Batching question: queueing + KV-cache math from memory
- [ ] Red-team one of your own design docs (5 holes minimum)
- [ ] If written-format: practice *typed* reasoning — no diagram crutch

Framework reference: [#/ml-system-design](#/ml-system-design).

---

## R5 — Project deep-dive

**Format:** 45–60 min. Opens with a **20-minute presentation you drive
without prompting**, then an **adversarial challenge phase** targeting
every detail you moved past quickly. Interviewers return to the exact
spots you glossed over — that's the test.

**How to structure the 20 minutes** (use your 5th Layer story — it's
exactly the careful empirical work they respect):

1. **Context (2 min):** the system, your role, the stakes.
2. **Problem (3 min):** the training–serving skew — what you observed,
   why it mattered.
3. **Approach (5 min):** *how you measured it* — methodology is what
   they'll attack, so give it weight.
4. **Decision (3 min):** holding the launch — the tradeoff, who had to
   be convinced.
5. **Impact (3 min):** what changed (metrics, process).
6. **Reflection (4 min):** what you'd do differently; open questions.
   ("I don't know" + "here's how I'd find out" beats bluffing.)

**Adversarial prep method:** list 10 details you'd normally gloss over;
prepare 2-minute depth on each. Rehearse: "why this metric and not that
one?", "what's the counterfactual?", "what would falsify your
conclusion?", "would this replicate with a different measurement?"

**Prep checklist:**
- [ ] 20-min presentation timed, out loud, no slides needed
- [ ] 10 glossed-over details → 2-min depth each
- [ ] Second story ready (Coupang ranking rigor: the slow careful
  experiment you chose over the fast one)

Full method: [#/project-deep-dive](#/project-deep-dive).

---

## R6 — Values / culture · GATE #2

**Format:** 45–60 min with **nontechnical interviewers**. Candidates
describe it as "like a therapy session" — they probe *how you felt*, not
just what you did. This is where most technically-passing candidates get
eliminated [REPORTED]. Rejections landing 2–3 days after the onsite (vs.
<24h for technical fails) point here.

**The mechanic most candidates miss:** questions are "suggested rather
than fully scripted" (wording varies), interviewers stay neutral and
follow up 3–4 levels deep — and they will **deliberately disagree with
you** to see whether you update for a good reason or just fold. Pleasant
agreement always loses; changing your mind *and* holding a well-defended
position can both be right. Rehearsed answers have a signature interviewers
recognize: "clean, complete, emotionally flat." Genuine ones are messier —
starting in the wrong place, self-correcting, carrying real uncertainty.

**What they're actually testing:** *demonstrated* alignment, not stated.
"I care about responsible AI" fails — it would pass anywhere. They want:
a **specifically-named Anthropic value** + your personal history with it +
critical thinking about Anthropic's *own* tradeoffs.

**The 7 highest-leverage questions — answer frameworks.** Each gives the
beats, then your talking points. Say them out loud once each.

<details>
<summary><b>1. "Tell me about a time you built something against your
values" → "How did you feel then? How about now?"</b></summary>

Beats: (1) real stakes — what, who wanted it, what resisting cost;
(2) name the violated value in plain words; (3) concrete action (data,
escalation, refusal) — not just feelings; (4) **the feeling layer** —
"it felt like he wanted me to name the discomfort instead of
rationalizing it away" [REPORTED]; say "I felt…" out loud; (5) cost +
what you'd do differently. Avoid: trivial examples, positive spin,
rationalizing the outcome into a win.

Your angle: the ship-velocity-vs-measurement-rigor tension — pressed to
ship a ranking change without proper measurement. What the data showed,
who pushed and why, how you escalated with evidence, the frustration of
being the blocker. → **Put the mission first** + **Hold light and shade**.
</details>

<details>
<summary><b>2. "What ways do you disagree with our AI approach?"</b></summary>

Beats: (1) one specific thing you buy — so the critique lands as
engaged, not hostile; (2) ONE specific disagreement — name the
mechanism, not a vibe (e.g. how ASL capability thresholds cash out into
deployment decisions; the eval-to-deployment gap); (3) what your own view
trades away; (4) what evidence would change your mind. "I agree with
everything" reads as not having done the reading. Avoid: grievances, a
critique you can't defend for two follow-ups.

Your angle: "I buy the ASL framework — but as someone who has shipped
ranking systems, my question is how capability thresholds cash out into
deployment decisions. In search we learned offline evals systematically
miss deployment failure modes" [your skew story]. "I'd want to see the
mechanism that closes that loop, not just the research." →
**Ignite a race to the top on safety** + **Do the simple thing that
works**.
</details>

<details>
<summary><b>3. "How would you feel if safety decisions sent the stock to
zero?"</b></summary>

Beats: (1) be honest — don't perform indifference to money; (2)
separate what you can assess (was the safety call principled? what does
it mean for your work Monday?) from what you can't (the stock);
(3) state your ordering plainly: judge the decision by its safety
reasoning, not its financial consequence. The documented reject move is
making money the headline ("I would not be happy if the stock went to
0" — interviewer visibly disliked it). Avoid: claiming you'd feel
nothing.

Your angle: "I'd want to understand the reasoning first — principled
call on real evidence, or panic? If the reasoning holds, that's exactly
the company I signed up for. The financial hit is real and I'd be honest
about that — but I wouldn't want to work somewhere that reverses a
safety call to protect the stock." → **Put the mission first**.
</details>

<details>
<summary><b>4. "Tell me about a time you raised a concern that slowed or
blocked a launch" / "…you argued against shipping"</b></summary>

Beats: (1) what you saw — the data, precisely; (2) steelman the other
side (why they wanted to ship); (3) your escalation path, with evidence;
(4) what it cost — timeline, social capital ("one that cost nothing
proves nothing"); (5) how it felt to be the blocker; (6) outcome + what
you'd do differently. Avoid: flawless-hero framing; skipping the other
side's case.

Your angle: the training–serving skew flagged pre-launch — your
centerpiece story. The skew you measured, why the team wanted to ship
anyway, how you brought data not just worry, the delay it caused, the
discomfort of slowing a launch everyone wanted. → **Put the mission
first** + **Ignite a race to the top on safety**.
</details>

<details>
<summary><b>5. "Why Anthropic, specifically — not another lab?"</b></summary>

Beats: (1) one specific thing about their work you hold an opinion on
(not "the mission matters"); (2) a piece of your history showing the
interest predates the interview; (3) forward: what you want to build
here and why only here. "I'm bullish on Anthropic" got flagged at a
recruiter screen as not good enough. Avoid: anything that would work at
any frontier lab.

Your angle: "What pulled me is that safety is the organizing principle,
not a constraint bolted on after — **Ignite a race to the top on
safety** as the actual job description. In generative retrieval I kept
hitting the gap between offline evals and deployment reality; I want to
work where closing that gap *is* the mission. And **Do the simple thing
that works** matches how I actually build — empirical iteration over
clever architectures." History anchor: the skew story as the moment you
realized measurement rigor is a safety practice.
</details>

<details>
<summary><b>6. "What would make you want to leave Anthropic?"</b></summary>

Beats: (1) ONE concrete condition — a specific mission reversal (e.g.
shipping a capability your own evals flagged as unsafe, to hit a revenue
target); (2) why that line and not another — connect it to the value you
joined for; (3) calm tone, not ultimatum energy. Avoid: "if things got
bad"; petty grievances; sounding like you'd hop at the first
disagreement.

Your angle: "If I saw us ship something our own safety work said wasn't
ready — because a competitor shipped first. I joined for **Put the
mission first**; if the final arbiter stopped being the mission, I'd have
to go." This also inoculates you against the race-dynamics follow-ups.
</details>

<details>
<summary><b>7. "Breakthrough with unquantified risk — delay? What if a
competitor ships anyway?"</b></summary>

Beats: (1) state decision CRITERIA before the verdict: reversibility of
harm, visibility of failure modes, whether a narrower release captures
the benefit; (2) apply them; (3) on the race follow-up: separate "is
slowing down the right call" from "does it change what competitors do" —
a correct safety practice doesn't stop being correct because it fails
industry-wide. Distinguish "behind on a competitive metric" from "ceding
the field to less careful actors." Avoid: absolutism ("always delay") or
flip-flopping as facts change without naming what moved you.

Your angle: search launch discipline — staged rollouts, holdback groups,
kill criteria. "In ranking we never shipped without a kill criterion and
a way to see the failure. Same here: name the redline, ship narrowly
inside it, invest the 'lost' time in the eval that lets us ship
confidently." → **Hold light and shade** + **Do the simple thing that
works**.
</details>

**More reported questions** (bank — know your one-line take for each):

- *Motivation:* "Which of Anthropic's values resonates with you — with
  a concrete example of when you **acted** on it, not merely admired
  it?"; "Why does AI safety matter to you personally?"; "How does your
  past work relate to AI safety?"; "Comment on recent company news";
  "What's an underrated AI problem?"; "Biggest risks and benefits of
  advanced AI" (one-sided answers fail — that's **Hold light and shade**
  in miniature)
- *Critical engagement:* "Do you have any feedback on Anthropic's
  mission?"; "What does Anthropic get wrong about AI safety?"; "Which
  part of the RSP would you change — and what would that trade away?"
  (only works if you've actually read it); "Which risk do you take most
  seriously, and what evidence would change your view?"
- *Hypotheticals:* "Caught between a commercial deadline and a safety
  concern — how do you decide?"; "Assigned to a project you believe is
  unsafe — concrete process?"; "Balance helpfulness vs harmlessness in
  launch criteria?"; deployment sim: model giving overconfident wrong
  answers in high-risk contexts — delay? guardrails? disclose?
- *Stories:* "A time you did something that conflicted with your
  values"; "A time you disagreed with someone with authority over you
  and pushed back"; "A time someone persuaded you to change a
  genuinely-held position — what evidence moved you?"; "A mistake where
  you were the one who was wrong"; "A moral dilemma — two obligations
  pulling apart, what you knowingly gave up"; "A working relationship
  that broke down, and how you repaired it"; "Most personally
  transformative experience"; EA beliefs (honest, reasoned, personal —
  don't perform)

**Failure modes — what got real candidates rejected:**

- The equity-to-zero hypothetical answered with money as the headline
  ("I would not be happy if the stock went to 0") — interviewer
  visibly disliked it [REPORTED, via Axios].
- 10 years of experience, rejected at the **recruiter screen** for
  generic AI-safety answers ("safety 答得浅") — the values filter fires
  before any technical round [1point3acres].
- "I'm bullish on Anthropic" at the recruiter screen — flagged as not
  good enough [Exponent].
- Four pre-packaged STAR stories shoehorned into whatever gets asked —
  "the fastest way to fail" [firsthand PM report].
- Professional values that would pass at any company ("I care about
  responsible AI", "I value technical rigor") — consistent fail pattern
  across 15 reports.

**Your 4 core stories.** Tell each with the feeling included
(frustration, doubt, relief), not just the logic. 90-sec and 5-min
versions + a "what I learned about myself" closer:

1. **Raised a concern others dismissed** — yours: flagging the
   training–serving skew pre-launch. Beats: what you saw, who disagreed
   and why, what you did (data? escalation?), how it felt to push, what
   happened, what you'd do differently.
2. **Changed your mind on evidence** — a ranking approach you reversed.
   Emphasize the *moment*: what evidence tipped you, how it felt to admit
   it, what it cost.
3. **Moral gray area** — a disagreement where both sides had a point
   (ship velocity vs. measurement rigor; a teammate's shortcut). Show the
   reasoning, not just the outcome.
4. **Tough feedback** — what stung, what was true in it, what changed
   after. The therapy-session favorite.

Then the values-specific layer — **use the official vocabulary.** The
candidate portal (checked 2026-10-06) publishes no values-round questions
or rubrics, but it does publish Anthropic's **7 guiding principles** —
these are the named values the round is built on. Name one *verbatim*,
then your example, then one critique of an Anthropic tradeoff:

| Principle (official) | Your story hook |
|---|---|
| **Put the mission first** | Flagging the training–serving skew pre-launch: you slowed a launch for correctness. Mission as final arbiter over ship velocity. |
| **Do the simple thing that works** | Your empirical ranking work: the simplest approach that iterated beat the clever one. |
| **Ignite a race to the top on safety** | Why Anthropic specifically: search/ranking manipulation as the dual-use risk you know firsthand. |
| **Hold light and shade** | Your moral-gray-area story: holding both the upside of generative retrieval and its failure modes at once. |
| **Be helpful, honest, and harmless** | Tough-feedback story: low-ego, direct communication, assuming good intentions. |
| **Be good to our users** | Coupang search quality work: going above and beyond for the user as the baseline expectation. |
| **Act for the global good** | Long-term view: decisions that maximize positive outcomes for humanity, not just the quarter. |

Critique example to pair with your named value: "I admire the
interpretability agenda — but how directly does it cash out into
deployment decisions? I'd want to see the mechanism, not just the
research." Skepticism with homework beats praise.

- **"What ways do you disagree with our AI approach?"** — see R0 guide.
- **Effective altruism beliefs** — honest, reasoned, personal (reported
  Glassdoor question). Don't perform; reflect.

**Prep checklist:**
- [ ] 4 stories written with beats; both lengths rehearsed out loud
- [ ] 7 frameworks above: say each answer out loud once, feelings
  included — no clean flat STAR recitations
- [ ] One named value + example + tradeoff critique, in your own words
- [ ] RSP skimmed (one thing you'd keep, one you'd change + its cost)
- [ ] Disagreement drill: for each of your 7 answers, argue the other
  side for 60 seconds — interviewers will
- [ ] Attitude check: honest self-reflection > polished STAR; a little
  skepticism > mission-praise

Full behavioral method: [#/behavioral](#/behavioral).

---

## Logistics — pace, references, rules

- **Pace:** 2–3 weeks between rounds is normal; 1–2 months end to end.
  Keep other processes warm; silence ≠ rejection for weeks.
- **References:** may be contacted **mid-process, in parallel** with
  interviews — have your list ready early.
- **No AI assistance** in any live round (official policy).
- **Comp:** offers are **not negotiable** (standardized process, per
  Axios) — no counteroffer strategy applies here.
- **Reading the signals:** rejection <24h after onsite ≈ technical round
  failed; 2–3 days later ≈ culture/HM. Don't over-read silence before
  that.
- **Team match** comes after the loop — passing doesn't guarantee a team
  wants you. Keep your "what I want to build" pitch sharp (R2).

**Universal reading (do before any round):**
- [ ] [Candidate AI guidance](https://www.anthropic.com/candidate-ai-guidance)
  (official — non-negotiable)
- [ ] "Demystifying evals for AI agents" (Anthropic engineering blog —
  broken harnesses > weak models)
- [ ] Anthropic blog/newsroom, last 90 days — one take with argument +
  counter-argument

---

## 30-minute checklist — before the recruiter call (Thu 10/8, 11:30 AM)

- [ ] **2-minute why-Anthropic (10 min):** four beats (R0); say it out
  loud once. Specific > sweeping.
- [ ] **Safety talking points (10 min):** your personal definition, one
  dual-use walkthrough (search/ranking manipulation), biggest risk +
  benefit with your own angle.
- [ ] **This week's Anthropic news (5 min):** skim the blog; one take
  with argument + counter-argument.
- [ ] **AI policy (5 min):** candidate-ai-guidance — read it.
