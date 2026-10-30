---
title: "Snorkel AI — Senior/Staff SWE, AI/ML (Coding Screen Fri 2026-10-30)"
slug: "snorkel"
section: "companies"
nav_order: 85
nav_label: "Snorkel"
tags: ["coding", "debugging", "data", "evaluation", "llm", "interviewing", "python"]
updated: "2026-10-29"
company: "Snorkel AI"
priority: "p0"
status: "interviewing"
process_sources:
  - { label: "OFFICIAL", url: "", accessed: "2026-10-29", note: "Joe Rufino 'Interview 1 Preparation' email 2026-10-21: Interview 1 is a LeetCode-style DSA problem on CoderPad, scored on (1) requirements gathering, (2) communication/collaboration, (3) completion — not just a correct answer" }
  - { label: "OFFICIAL", url: "", accessed: "2026-10-29", note: "Tyler Ng confirmation email 2026-10-23: Coding Screen Fri 2026-10-30 10:00-10:45 AM PT with Ryan Wong (Software Engineer, Operations), Zoom + CoderPad (link in email); DocuSign NDA sent 2026-10-22, must be signed by Rui" }
  - { label: "REPORTED", url: "https://www.1point3acres.com/bbs/thread-1181207-1-1.html", accessed: "2026-10-29", note: "1point3acres 2026-06-24, Senior AI/ML Eng onsite: 60-min CoderPad coding round is a DEBUGGING exercise ('Agent Eval Pipeline'), not LeetCode — small Python codebase + examples.json (~80 tasks, ~5 domains) + tests.py; fixes are 1 word / 1-2 lines; test thresholds are NOT the bug; refresh confusion matrix. Post outcome: WaitList, rated Hard. Middle of post is points-gated (>188) — visible setup + all tips read, hidden bug list not accessible" }
  - { label: "REPORTED", url: "https://www.interviewquery.com/guides/snorkel-ai-software-engineer", accessed: "2026-10-29", note: "Onsite = project deep dive (decisions/tradeoffs/ownership) + systems & coding (asked to design a job executor; actual expectation was a single-threaded workflow implementation, not distributed) + AI round (started vague; real ask = state-machine-style tagging workflow based on Snorkel's labeling approach)" }
  - { label: "REPORTED", url: "https://www.1point3acres.com/bbs/thread-1132217-1-1.html", accessed: "2026-10-29", note: "Oct 2026 replies name later rounds 'built with AI' and 'AI system design'; no questions/answers posted" }
  - { label: "REPORTED", url: "https://www.interview-coach-pro.com/companies/snorkel.ai/", accessed: "2026-10-29", note: "Aggregated flow: recruiter call -> technical screen (practical/hands-on) -> agent workflow / AI coding -> AI system design -> HM & culture; emphasis on running code, LLM API and agent workflow fluency" }
  - { label: "REPORTED", url: "https://duke.fm/2026/09/22/exclusive-snorkel-ai-valued-at-3-5-billion-amid-surging-demand-for-complex-ai-training-data-2/", accessed: "2026-10-29", note: "Reuters 2026-09-22: Series E $350M at $3.5B valuation (vs $1.3B May 2025); annualized revenue run-rate $350M+ from ~$20M a year earlier, driven by expert Data-as-a-Service launched Sep 2025; 'agentic data development platform' — experts design tasks/rubrics, AI automates QA" }
---

## TL;DR

**Status: recruiter Joe Rufino (intro done 2026-10-21, v6 resume sent).
Next: Coding Screen — Fri 2026-10-30, 10:00–10:45 AM PT, Ryan Wong
(Software Engineer, Operations), Zoom + CoderPad. No AI tools.**

Two different coding formats exist at Snorkel, and you should be ready for
both. **OFFICIAL** (Joe's prep email): tomorrow's Interview 1 is a
LeetCode-style DSA problem on CoderPad, graded on requirements gathering,
communication, and completion. **REPORTED** (一亩三分地 面经, onsite):
Snorkel's signature coding round is a 60-minute *debugging* exercise — an
"Agent Eval Pipeline" codebase you fix with one-line changes. The overlap is
what saves you: fluent Python, evaluation metrics cold, and narrating your
reasoning the whole way. Ryan sits in **Operations** — the org that runs the
expert-data eval pipelines — so the debugging/metrics flavor is a live
possibility even in the screen.

:::warn
**DocuSign NDA (sent by Tyler Ng 2026-10-22) must be signed before the
interview** — as of 2026-10-29 it is still unsigned in every record. Sign it
tonight; do not leave it for the morning. No AI assistance in live rounds.
:::

## Company & product

Snorkel AI spun out of the Stanford AI Lab in 2019 (CEO Alex Ratner). It
started as **programmatic weak supervision** — labeling functions instead of
hand labels, productized as Snorkel Flow. In Sep 2025 it launched expert
**Data-as-a-Service** and the business exploded: finished datasets, RL
environments, and evaluation benchmarks/rubrics delivered to frontier labs,
produced by an "agentic data development platform" — human experts design
tasks and grading rubrics, AI agents and automated QA do the production
labor. Sep 2026: **Series E, $350M at a $3.5B valuation** (2.7× the May 2025
round); revenue run-rate **$350M+**, up from ~$20M a year earlier.
Competitors: Scale AI, Surge AI, Mercor.

**Your mapping (say it in the room):** search ranking *is* data quality plus
evaluation at scale — graded relevance, per-segment metrics, pipelines that
decide what "good" means. Snorkel sells exactly that discipline, pointed at
frontier-model training data instead of search results. Your Coupang search
work (multi-stage ranking, generative retrieval, offline eval) is the same
muscle.

## Role expectations

Senior/Staff SWE on an AI/ML track. The interviewer being from **Operations**
engineering tells you the center of gravity: the systems that run expert-data
operations — task distribution, contributor (EC) workflows, eval pipelines,
quality measurement. The staff bar: drive an ambiguous problem end-to-end,
make tradeoffs out loud, ship production-quality Python. Pure algorithm
trivia is explicitly *not* the point (per both the official prep email and
the 面经).

## Interview process

Everything except R0/R1 is REPORTED by candidates.

| # | Round | Format | What actually decides it |
|---|-------|--------|--------------------------|
| R0 | Recruiter intro — Joe Rufino | 30 min call | ✅ Done 2026-10-21; v6 resume sent |
| R1 | **Coding Screen — Ryan Wong** | **45 min, Zoom + CoderPad** | **Requirements gathering → communication → completion (OFFICIAL rubric)** |
| R2 | Project deep dive | Onsite | Decisions, tradeoffs, ownership on past projects |
| R3 | Systems & coding | Onsite | "Job executor" style — real expectation: single-threaded workflow implementation, not a distributed design |
| R4 | Coding — Agent Eval Pipeline debugging | 60 min, CoderPad | Read unfamiliar code, isolate root causes, one-line fixes, narrate (面经) |
| R5 | AI round / AI system design | Onsite | State-machine tagging workflow à la Snorkel labeling; rounds named "built with AI" + "AI system design" in Oct 2026 reports |
| R6 | HM & culture | Onsite | Scope, collaboration, data-quality mindset |

## R1 — Tomorrow's Coding Screen (OFFICIAL format)

**The rubric is published — use it.** Joe's prep email scores three things:

1. **Requirements gathering** — before coding, ask: input format and size,
   constraints, expected output, edge cases (empty input? duplicates?
   sorted?). The first 3–5 minutes of questions are literally graded.
2. **Communication / collaboration** — think out loud continuously, state
   tradeoffs (optimal vs. maintainable), treat the interviewer as a resource,
   take hints warmly and visibly adjust.
3. **Completion** — working, efficient, maintainable code. Run your own test
   cases, including the edge cases you asked about. State complexity at the
   end without being asked.

**DSA brush list (medium difficulty, Python, no autocomplete):** hash-map
counting/frequency, two pointers, sliding window, BFS/DFS with `deque`,
heap top-K (`heapq.nlargest` and manual push/pop), binary search (`bisect`
and hand-rolled), intervals, basic string parsing. CoderPad has no IDE
autocomplete — have the stdlib names cold: `collections.defaultdict`,
`Counter`, `deque`, `heapq`, `bisect`, `itertools`, `sorted(key=...)`,
`enumerate`, `zip`.

**Pacing for 45 minutes:** ~5 min clarify + sketch approach → ~25 min code
→ ~10 min test/debug with narrated cases → ~5 min complexity + follow-up
variant. If two problems appear, finishing both cleanly beats one perfect
solution.

## R4 preview — the "Agent Eval Pipeline" debugging round (REPORTED 面经)

From the 一亩三分地 report (Senior AI/ML Engineer, onsite, Jun 2026 —
outcome WaitList, rated Hard). **This is the round Snorkel is known for;
drill it even though tomorrow is the screen.**

**The setup:** ~3 files on CoderPad. `examples.json` is the eval dataset —
roughly **80 tasks across ~5 domains (~16 per domain)**. Each example has:
the input/task given to the Expert Contributor (EC), a **golden label**
("pass" or "needs revision"), and the **golden response** (the exact expected
output — note: some golden responses are **JSON strings**). Plus the
implementation files and a `tests.py` with failing tests. Your job:
investigate, find the bugs, make the tests pass.

**The rules of the round (verbatim-grade tips from the post):**

- Fixes are **one word or 1–2 lines, max**. Big rewrites = wrong path.
- **The thresholds in the tests are NOT the bug.** Every time you want to
  change a `>` into a `>=` in a test — stop. The bug is in the
  implementation.
- **Read instruction_1 / instruction_2 first, then trace ONE example
  end-to-end** through the pipeline before touching anything.
- Refresh the **confusion matrix** before you start (below) — the eval
  computes precision/recall/accuracy-style metrics and you will stare at a
  metric function.
- It's collaborative and **you drive**: say what you understood → state your
  plan → fix → run tests → discuss. If you've somehow seen the problem
  before, do NOT speed-run it — they grade how you think, not typing speed.
- **Close with tradeoffs:** what other examples could this fix break, how
  you'd handle malformed JSON, whether per-class (per-domain) metrics are
  the right eval target. This discussion is part of the grade.

:::collapse Likely bug categories — INFERRED drill targets (not leaked answers)
The middle of the 面经 post (specific bugs) is points-gated and was not
readable; the categories below are inferred from the visible setup + tips,
and are the standard failure modes of an eval pipeline. Drill them so any
one-line bug looks familiar:

- **Metric mix-up:** precision and recall swapped in the metric function, or
  accuracy computed over the wrong denominator (e.g., only examples with a
  golden label, or only one class).
- **JSON-as-string comparison:** golden response is a JSON *string*; code
  compares it to a parsed dict, or string-compares two JSON blobs that
  differ only in key order/whitespace → false mismatches. Correct move:
  parse both sides, compare objects.
- **Label normalization:** "pass" vs "Pass" vs " pass" — missing
  `.strip().lower()` on one side of the comparison.
- **Aggregation error:** per-domain metrics averaged with the wrong weights
  (macro vs micro), or a domain silently dropped from the aggregate.
- **Threshold semantics in the implementation:** a score compared with the
  wrong operator/direction *in the pipeline code* (the test's threshold is
  correct — the implementation's use of it isn't).
- **Malformed-input handling:** an example with invalid JSON crashes the
  whole run instead of being counted/skipped per the instructions.
:::

**Tonight's drill (30 min):** write a tiny scorer yourself — 6 examples,
golden responses as JSON strings, a `score()` that computes per-domain and
overall precision/recall — then plant 3 one-line bugs from the list above
and debug it cold, out loud, timing yourself. Reading unfamiliar code calmly
is the skill being graded; this is the closest simulation available.

## Metrics you must have cold

The debugging round and the AI round both live on evaluation vocabulary.
From [ML Fundamentals](#/ml-fundamentals) (Metrics + tradeoffs sections):

- Confusion matrix: TP / FP / FN / TN from a 2×2 you can draw in 10 seconds.
- Precision = TP/(TP+FP) — "of the alarms, how many were real"; Recall =
  TP/(TP+FN) — "of the real cases, how many did we catch"; Accuracy =
  (TP+TN)/total — and why accuracy misleads when classes/domains are
  imbalanced.
- Per-domain (per-class) vs overall metrics; macro (average of per-class
  scores) vs micro (pool the counts first). With ~5 domains of ~16 tasks,
  one broken domain is invisible in the pooled number — that's exactly why
  per-class metrics are the closing-discussion topic.
- The eval-design tradeoff to voice: exact-match against golden responses is
  strict and brittle (JSON key order!) vs. rubric/graded scoring — precision
  of measurement vs. cost.

## Later rounds — what to prepare after the screen

- **Project deep dive:** they probe *decisions* — why this approach, how the
  team was structured, what tradeoffs. Lead with Coupang multi-stage search
  ranking and the generative-retrieval work; have the numbers and the
  "what I'd do differently" ready.
- **Systems & coding (job executor):** a candidate was told "design a job
  executor" and the real expectation was a **single-threaded workflow
  implementation**. Lesson: clarify scope and scale assumptions *before*
  designing distributed machinery — over-engineering reads as poor judgment
  here.
- **AI round:** starts high-level and stays vague until you push. The real
  question that emerged: **design a state-machine-style tagging workflow for
  incoming sentences**, based on Snorkel's labeling approach. The content is
  labeling mechanics — labeling functions, routing, decision flow, quality
  control — not model name-dropping. Drill clarifying questions until the
  concrete problem surfaces; that drilling is apparently expected.
- **"Built with AI" + "AI system design"** (named in Oct 2026 reports):
  expect a round where AI tools are allowed and the design object is an AI
  data/eval system — task design, rubrics, verifiers, RL environments.

## Questions to ask Ryan

1. What does Operations engineering own day to day — is it the eval
   pipelines behind the expert-data business?
2. What would the first project for this role look like?
3. How does the team measure eval-pipeline quality — per-domain metrics,
   agreement with expert gold labels?
4. What do the remaining rounds look like, and what's the timeline?

## Practice questions

- [ ] Two Sum variants / anagram grouping with a hash map — narrated, timed.
- [ ] Top-K frequent elements with a heap — narrated, timed.
- [ ] BFS shortest path on a grid with `deque` — narrated, timed.
- [ ] Sliding-window longest substring — narrated, timed.
- [ ] Draw the confusion matrix; compute precision/recall/accuracy for:
  80 tasks, pipeline says "pass" 50 times, 40 of those are truly pass, 10
  true passes were marked "needs revision". (P = 40/50 = 0.80, R = 40/50 =
  0.80, Acc needs TN — compute it.)
- [ ] Explain macro vs micro averaging across 5 domains of 16 tasks, and
  when each lies to you.
- [ ] Debug drill: self-built scorer with 3 planted one-line bugs (above).
- [ ] "Tell me about a data project that didn't go as expected" — reported
  Snorkel behavioral; prepare the Coupang evaluation/data story.
- [ ] Sketch a state-machine tagging workflow for incoming sentences:
  states, routing rules, human-in-the-loop points, quality checks.
- [ ] Why Snorkel, in 3 sentences, using the data-quality/evaluation mapping
  — no generic "I love your mission."

## 30-minute checklist — tomorrow morning (Fri 10/30, interview 10:00 AM)

- [ ] **NDA signed** (do it tonight, verify the DocuSign completion email).
- [ ] CoderPad link from Tyler's confirmation email opens; Python selected.
- [ ] Zoom link tested; quiet room; water.
- [ ] Gym 8:00–9:30 as usual — at your desk by 9:50, no 12:00 conflicts
  (interview ends 10:45).
- [ ] On paper next to you: precision / recall / accuracy formulas.
- [ ] One warm-up DSA problem, solved out loud.
- [ ] Four questions for Ryan (above) ready.
- [ ] Opening line ready: brief, warm, no comp talk; if scheduling comes up,
  technical rounds at 10:00 AM PT, recruiter/HM at 1:00–2:00 PM PT.
