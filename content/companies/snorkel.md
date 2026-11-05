---
title: "Snorkel AI — Senior/Staff SWE, AI/ML (Building with AI Nov 10 · AI System Design Nov 12)"
slug: "snorkel"
section: "companies"
nav_order: 85
nav_label: "Snorkel"
tags: ["coding", "debugging", "system-design", "data", "evaluation", "llm", "interviewing", "python"]
updated: "2026-11-04"
company: "Snorkel AI"
priority: "p0"
status: "interviewing"
process_sources:
  - { label: "OFFICIAL", url: "", accessed: "2026-11-04", note: "Tyler Ng confirmation email 2026-11-04 13:02 PT: two 60-min technical rounds scheduled — Tue 2026-11-10 10:00-11:00 AM PT 'Building with AI' with Martin He (Software Engineer), Zoom; Thu 2026-11-12 10:00-11:00 AM PT 'AI System Design' with Mengdie Hu (Software Engineer), Zoom; HackerRank link https://hr.gs/1ec4172 for the sessions" }
  - { label: "OFFICIAL", url: "", accessed: "2026-11-04", note: "Coding screen PASSED: Fri 2026-10-30 with Ryan Wong cleared with strong feedback (Arouj Khan, Lead Recruiter, took over scheduling from Joe Rufino); check-in booked Thu 2026-11-05 13:00 PT" }
  - { label: "OFFICIAL", url: "", accessed: "2026-10-29", note: "Joe Rufino 'Interview 1 Preparation' email 2026-10-21: Interview 1 is a LeetCode-style DSA problem on CoderPad, scored on (1) requirements gathering, (2) communication/collaboration, (3) completion — not just a correct answer" }
  - { label: "REPORTED", url: "https://www.glassdoor.co.in/Interview/Snorkel-AI-Interview-Questions-E5809965.htm", accessed: "2026-11-04", note: "Glassdoor, Sept 2026, Redwood City, via recruiter: recruiter screen -> technical screen -> 1-hour live coding LLM GRADING exercise with prescribed inputs and output labels -> design exercise on building a GRADING LOOP -> career fit interview. Single candidate report; closest public match to the two confirmed round names" }
  - { label: "REPORTED", url: "https://www.1point3acres.com/bbs/thread-1181207-1-1.html", accessed: "2026-11-04", note: "1point3acres 2026 (Apr-Jun), Senior AI/ML Eng onsite: 60-min CoderPad coding round is a DEBUGGING exercise ('Agent Eval Pipeline'), not LeetCode — small Python codebase + examples.json (~80 tasks, ~5 domains) + tests.py; fixes are 1 word / 1-2 lines; test thresholds are NOT the bug; refresh confusion matrix. Outcome: WaitList, rated Hard. Middle of post is points-gated — visible setup + all tips read, hidden bug list not accessible" }
  - { label: "REPORTED", url: "https://www.1point3acres.com/bbs/thread-1132217-1-1.html", accessed: "2026-10-29", note: "Oct 2026 replies name later rounds 'built with AI' and 'AI system design' — confirms the round NAMES exist publicly, but no questions/answers posted" }
  - { label: "REPORTED", url: "https://www.interviewquery.com/guides/snorkel-ai-software-engineer", accessed: "2026-11-04", note: "InterviewQuery, synthesized from 2 candidate reports: onsite = project deep dive (decisions/tradeoffs/ownership) + systems & coding (asked to design a job executor; actual expectation was a single-threaded workflow implementation, not distributed) + AI round (started vague, had to probe; real ask = state-machine-style tagging workflow for incoming sentences, based on Snorkel's labeling workflow)" }
  - { label: "REPORTED", url: "https://www.glassdoor.co.nz/Interview/Snorkel-AI-Software-Engineer-Interview-Questions-EI_IE5809965.0,10_KO11,28.htm", accessed: "2026-11-04", note: "Glassdoor SWE, Redwood City: virtual onsite = 2 coding + 1 design + 1 manager + 1 VP, splittable over 2 days; phone screen coding, Python recommended; onsite coding = 2 medium LeetCode-style questions. Another Jan 2025 report: coding rounds have a 'tricky' part, interviewers push you to implement fast; DSA (hashmaps/stacks/heaps/queues) + basic system design" }
  - { label: "REPORTED", url: "https://www.jointaro.com/interviews/companies/snorkel-ai/experiences/ml-engineer-united-states-december-1-2024-declined-offer-negative-0455d492/", accessed: "2026-11-04", note: "Taro, Dec 2024, ML Engineer (got offer): tech screen + 4-round onsite; screen and 2 onsite rounds coding, rest system design + behavioral; coding non-LeetCode style, questions are long — ~10 min just to understand the prompt" }
  - { label: "OFFICIAL", url: "https://snorkel.ai/blog/ai-agents-you-can-trust/", accessed: "2026-11-04", note: "Snorkel's own published eval doctrine: define 'good' at four levels — task, trace, outcome, rubric; evaluation is a lifecycle (understand -> build -> execute -> diagnose-and-report), not a launch gate; every disagreement is adjudicated and fed back into the rubric" }
  - { label: "OFFICIAL", url: "https://snorkel.ai/blog/walkthrough-driving-data-centric-ai-agent-development-with-snorkel/", accessed: "2026-11-04", note: "Snorkel Evaluate walkthrough: off-the-shelf LLM-as-a-judge agrees with experts only ~70-75% of the time; alignment comes from prompt tuning + programmatic weak supervision (multiple prompts / labeling functions -> distilled evaluators) + SME validation; error analysis by slicing the benchmark" }
  - { label: "REPORTED", url: "https://duke.fm/2026/09/22/exclusive-snorkel-ai-valued-at-3-5-billion-amid-surging-demand-for-complex-ai-training-data-2/", accessed: "2026-10-29", note: "Reuters 2026-09-22: Series E $350M at $3.5B valuation (vs $1.3B May 2025); annualized revenue run-rate $350M+ from ~$20M a year earlier, driven by expert Data-as-a-Service launched Sep 2025" }
---

## TL;DR

**Status: coding screen PASSED (Fri 2026-10-30, Ryan Wong — cleared with
strong feedback). Two 60-minute technical rounds are now scheduled, both
10:00–11:00 AM PT:**

- **Tue Nov 10 — "Building with AI", Martin He (Software Engineer)**
- **Thu Nov 12 — "AI System Design", Mengdie Hu (Software Engineer)**
- HackerRank link for the sessions: https://hr.gs/1ec4172

**面经 verdict (researched 2026-11-04 — 一亩三分地 / InterviewQuery /
Glassdoor / Taro):** no public post describes these two rounds under their
exact names with content — the Oct 2026 一亩三分地 thread confirms the
names ("built with AI", "AI system design") but posts no questions. The
closest real reports, and what this page is built on:

- **Glassdoor, Sept 2026 (REPORTED, single candidate):** after the screens
  came "an hour-long live coding **LLM grading exercise with prescribed
  inputs and output labels**", then "a **design exercise on building a
  grading loop**", then a career-fit interview. That maps almost 1:1 onto
  your two rounds — Building with AI ≈ live-build a grader; AI System
  Design ≈ design the grading loop. The mapping is **INFERRED**; the
  report itself is real.
- **一亩三分地 (REPORTED):** Snorkel's other known live-coding format is a
  60-min **debugging** exercise on an "Agent Eval Pipeline" codebase —
  one-line fixes, confusion matrix, thresholds are not the bug (full
  breakdown below). If Building with AI is not a build, it is this.
- **InterviewQuery (REPORTED):** the AI design round can start deliberately
  vague — the real ask emerged only after probing (a state-machine tagging
  workflow). Clarifying questions are part of the test.

Either way, both rounds live in one world: **evaluation pipelines and
grading loops for AI outputs** — which is Snorkel's entire business, and
your search-ranking eval experience restated. Fluent Python, metrics cold,
narrate everything.

:::warn
**DocuSign NDA (sent by Tyler Ng 2026-10-22) is still unsigned as of
2026-11-04** — it likely gates any finals after these rounds. Sign it
before Nov 10, not the morning of. No AI assistance in live rounds unless
the round itself provides the tool (Building with AI may — follow the
interviewer's setup, not assumptions).
:::

## Company & product

Snorkel AI spun out of the Stanford AI Lab in 2019 (CEO Alex Ratner). It
started as **programmatic weak supervision** — labeling functions instead
of hand labels, productized as Snorkel Flow. In Sep 2025 it launched expert
**Data-as-a-Service** and the business exploded: finished datasets, RL
environments, and evaluation benchmarks/rubrics delivered to frontier labs,
produced by an "agentic data development platform" — human experts design
tasks and grading rubrics, AI agents and automated QA do the production
labor. Sep 2026: **Series E, $350M at a $3.5B valuation** (2.7× the May 2025
round); revenue run-rate **$350M+**, up from ~$20M a year earlier.
Competitors: Scale AI, Surge AI, Mercor.

**Your mapping (say it in the room):** search ranking *is* data quality plus
evaluation at scale — graded relevance labels, per-segment metrics,
pipelines that decide what "good" means. Snorkel sells exactly that
discipline, pointed at frontier-model training data instead of search
results. Your Coupang work (multi-stage ranking, generative retrieval,
offline eval gating launches) is the same muscle.

## Interview process

| # | Round | Format | Status / what decides it |
|---|-------|--------|--------------------------|
| R0 | Recruiter intro — Joe Rufino | 30 min call | ✅ Done 2026-10-21; Arouj Khan (Lead Recruiter) now owns scheduling |
| R1 | Coding Screen — Ryan Wong | 45 min, Zoom + CoderPad | ✅ **Passed 2026-10-30, strong feedback** |
| R2 | **Building with AI — Martin He** | **60 min, Tue Nov 10, 10:00 AM PT, Zoom + HackerRank** | **Live build (likely an LLM grading exercise) or eval-pipeline debugging — see below** |
| R3 | **AI System Design — Mengdie Hu** | **60 min, Thu Nov 12, 10:00 AM PT, Zoom** | **Design a grading / evaluation loop — see below** |
| R4+ | Career fit / HM / project deep dive | REPORTED as later rounds | Decisions, tradeoffs, ownership; not yet scheduled |

Also REPORTED across candidates: virtual onsites of 2 coding + 1 design +
manager/VP rounds; coding questions are long and practical, not LeetCode
trivia — budget real minutes to understand the prompt before writing code.

## R2 — Building with AI (Tue Nov 10, Martin He)

### What it most likely is

**REPORTED + INFERRED:** the Sept 2026 Glassdoor candidate's "hour-long
live coding LLM grading exercise with prescribed inputs and output labels"
is the best public match for this slot. Concretely, expect something like:
you are given inputs (tasks / model outputs) and a prescribed label set
(e.g. pass / needs-revision, or a rubric), and you **build a working
grading program live** — prompt + model call (or a provided stub), parse
the structured output, score it against golden labels, iterate until the
grader agrees with the goldens. The HackerRank link is the session
platform. **Variant B** is the 一亩三分地 debugging format (next section)
— the two share the same skeleton: an eval pipeline, golden labels, and
metrics. Prepare for the build; the debugging drill is your insurance.

### The 60-minute playbook (build variant)

- **Minutes 0–5 — frame it out loud:** restate the task, pin the I/O
  contract (input fields, exact label set, output format), ask what
  "good" means — agreement with goldens on the sample set? Which errors
  cost more, false-pass or false-revise? Graded on framing first.
- **Minutes 5–15 — skeleton end-to-end:** load examples → call grader with
  a trivial v0 prompt → parse → compare → print agreement + confusion
  matrix. A dumb pipeline that runs beats a smart half-pipeline.
- **Minutes 15–40 — iterate on disagreements:** print the actual
  disagreements, cluster them (format failures vs. rubric ambiguity vs.
  genuinely hard cases), fix the largest cluster first — usually prompt
  rubric precision + few-shot examples drawn from the goldens themselves.
- **Minutes 40–50 — harden:** malformed JSON from the model (strip code
  fences, retry with a repair prompt, never crash), empty/oversized
  inputs, deterministic settings (temperature 0), a small cache so re-runs
  are cheap.
- **Minutes 50–60 — close with judgment:** report per-slice agreement (per
  domain, not just overall), name the residual error modes, say what you
  would do with another hour — calibration set, a second judge + 
  adjudication, distilling the judge into a smaller evaluator. This
  closing discussion is part of the grade in every Snorkel report.

### Fluency checklist (have these cold, no autocomplete assumptions)

- Structured LLM output: JSON mode / schema-constrained replies; prompt
  anatomy for a judge — role, rubric with explicit criteria per label,
  few-shot examples, "output only this JSON".
- Robust parsing: `json.loads` with a fallback path, fence-stripping,
  validating against the label set, counting parse failures as a metric.
- Agreement math on the fly: accuracy/agreement rate, confusion matrix,
  per-class precision/recall, Cohen's kappa if you want the senior flex
  ($\kappa = (p_o - p_e)/(1 - p_e)$ — observed vs. chance agreement).
- Batch hygiene: retries with backoff, rate-limit awareness, logging
  prompts+outputs for post-hoc error analysis (traces, in Snorkel speak).

### Variant B — the "Agent Eval Pipeline" debugging round (REPORTED 面经)

From the 一亩三分地 report (Senior AI/ML Engineer, onsite, spring 2026 —
outcome WaitList, rated Hard). If Nov 10 opens as a debugging exercise
instead of a build, this is the round:

**The setup:** ~3 files on CoderPad. `examples.json` is the eval dataset —
roughly **80 tasks across ~5 domains (~16 per domain)**. Each example has:
the input/task given to the Expert Contributor (EC), a **golden label**
("pass" or "needs revision"), and the **golden response** (the exact
expected output — note: some golden responses are **JSON strings**). Plus
the implementation files and a `tests.py` with failing tests. Your job:
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
- It's collaborative and **you drive**: say what you understood → state
  your plan → fix → run tests → discuss. If you've somehow seen the problem
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

**Drill (45 min, do it twice before Nov 10):** (1) Build variant — write a
mini LLM-grader against 10 hand-made examples with golden labels, compute
agreement + confusion matrix, iterate the prompt once on disagreements.
(2) Debug variant — take your own scorer, plant 3 one-line bugs from the
list above, debug it cold, out loud, timed. Reading unfamiliar code calmly
and iterating a grader on evidence are the two skills being graded.

## R3 — AI System Design (Thu Nov 12, Mengdie Hu)

### What it most likely is

**REPORTED + INFERRED:** the same Sept 2026 Glassdoor flow puts "a design
exercise on **building a grading loop**" right after the live grading
build. Expect a prompt in the family: *design the system that grades
agent/model outputs against expert rubrics, at scale, and feeds the
results back into better data.* Alternates from InterviewQuery: an AI
workflow design that starts vague (their report: a state-machine tagging
workflow for incoming sentences, à la Snorkel's labeling system) — if the
prompt opens fuzzy, the probing *is* the exercise: ask until the concrete
system surfaces, then design it.

### The design, in Snorkel's own vocabulary (OFFICIAL doctrine)

Anchor the whole answer on Snorkel's published framework — it is both
correct and their house language:

- **Define "good" at four levels: task, trace, outcome, rubric.** The task
  spec (specificity), the trace (what the agent retrieved/did, not just
  the final answer), the outcome (what changed in the real workflow), and
  the rubric (complete? grounded? policy-aligned? auditable?).
- **Evaluation is a lifecycle, not a launch gate:** understand → build →
  execute → diagnose-and-report → feed back into the next data cycle.
  Snorkel's product loop is literally named **Evaluate → Curate → Refine**.
- **"We evaluate our evaluators":** reviewer/judge calibration is measured
  and corrected, not assumed. Off-the-shelf LLM-as-a-judge agrees with
  experts only **~70–75%** (Snorkel's own number) — alignment is a system
  feature: prompt tuning, programmatic weak supervision (multiple prompts
  / labeling functions combined into distilled evaluators), SME validation
  sets.
- **Every disagreement is adjudicated and fed back into the rubric** —
  the disagreement queue is the highest-value component in the system.
- **Prefer verifiable endpoints:** deterministic verifiers, unit tests,
  state asserts, DB diffs over open-ended prose grading wherever the task
  allows; score the trace (right tools, right order, safe) as well as the
  outcome.

### Reference architecture (walk it in this order)

- **Clarify first (5 min):** what is being graded (agent traces? single
  answers?), who writes rubrics, volume/day, latency budget (offline
  batch vs. inline gate), cost ceiling, what decision the score drives
  (ship/no-ship, RL reward, data filtering). State assumptions numerically.
- **Benchmark & rubric service:** versioned datasets (tasks, golden
  labels, gold traces), versioned rubrics — every score must be
  reproducible against (dataset version, rubric version, grader version).
- **Execution harness:** runs the model/agent over the benchmark, captures
  **full traces** (tool calls, retrievals, intermediate state), sandboxed
  and deterministic where possible; templated scenarios with difficulty
  knobs to scale coverage.
- **Grader layer, cheapest-first:** (1) programmatic verifiers —
  deterministic checks, format/schema validation, unit-test-style
  asserts; (2) LLM judges with rubric prompts, temperature 0, structured
  output; (3) human experts, routed by low judge confidence, judge
  disagreement, high-stakes slices, plus a random audit sample.
- **Scoring & slicing:** aggregate + per-slice metrics (per domain, per
  difficulty, per error mode), confusion matrix vs. goldens, judge–expert
  agreement tracking over time; a broken slice must be visible even when
  the pooled number looks fine.
- **Diagnosis loop:** failure taxonomy tagging, disagreement queue with
  adjudication UI, adjudications versioned back into the rubric; outputs
  drive targeted data collection (Curate) and the next benchmark revision
  (Refine). Regression sets freeze past failures so fixes don't silently
  regress.
- **Cross-cutting:** trace storage + lineage (every score traceable to
  inputs), contamination controls (benchmark leakage into training data),
  cost accounting per graded item, difficulty calibration against frontier
  models so the benchmark stays discriminative.

### Your unfair advantage — say it explicitly

This is isomorphic to search evaluation: graded relevance judgments ≈
rubric grades; per-query-segment metrics ≈ slicing; offline eval gating a
ranking launch ≈ eval gating a model release; inter-annotator agreement ≈
judge calibration. Walk one Coupang example through the loop (how a
relevance-label disagreement changed the rubric) and the design stops
being hypothetical.

### Pitfalls (reported failure modes in Snorkel design rounds)

- Jumping to boxes before defining the rubric and what decision the score
  drives.
- Treating the LLM judge as ground truth — no calibration set, no
  agreement metric, no adjudication path.
- Designing for the pooled metric only; no slicing, so a dead domain
  hides inside a green dashboard.
- No versioning → scores that can't be compared across weeks.
- Over-engineering distribution before scope is pinned (the InterviewQuery
  job-executor lesson: the expected answer was a *single-threaded
  workflow*, not a distributed system — clarify scale before scaling).

## Metrics you must have cold

Both rounds live on evaluation vocabulary:

- Confusion matrix: TP / FP / FN / TN from a 2×2 you can draw in 10 seconds.
- Precision = TP/(TP+FP) — "of the alarms, how many were real"; Recall =
  TP/(TP+FN) — "of the real cases, how many did we catch"; Accuracy =
  (TP+TN)/total — and why accuracy misleads when classes/domains are
  imbalanced.
- Per-domain (per-class) vs overall metrics; macro (average of per-class
  scores) vs micro (pool the counts first). With ~5 domains of ~16 tasks,
  one broken domain is invisible in the pooled number — that's exactly why
  per-class metrics are the closing-discussion topic.
- Judge quality: raw agreement rate, and Cohen's kappa when chance
  agreement is high (e.g. 90% of labels are "pass" — 85% agreement can be
  worse than it looks).
- The eval-design tradeoff to voice: exact-match against golden responses
  is strict and brittle (JSON key order!) vs. rubric/graded scoring —
  precision of measurement vs. cost.

## Practice questions

- [ ] Build drill (timed, 45 min): mini LLM-grader over 10 examples with golden labels; print agreement + confusion matrix; iterate the rubric prompt once on the disagreements and re-measure.
- [ ] Debug drill (timed, 30 min): self-built scorer with 3 planted one-line bugs from the categories above; narrate the root-cause hunt.
- [ ] Confusion matrix math: 80 tasks, pipeline says "pass" 50 times, 40 of those are truly pass, 10 true passes were marked "needs revision" — compute precision, recall, accuracy (find TN first), then per-domain macro vs micro if domain A (16 tasks) scored 0.
- [ ] Design drill (timed, 45 min, out loud): "Design a grading loop for a customer-support agent" — clarify → scale math → architecture → grader layering → disagreement/adjudication → slicing → feedback into data collection.
- [ ] Design variant: state-machine tagging workflow for incoming sentences — states, routing rules, human-in-the-loop points, quality checks (InterviewQuery-reported format).
- [ ] Explain, in Snorkel's words: task / trace / outcome / rubric; Evaluate → Curate → Refine; "we evaluate our evaluators" — 60 seconds each, no notes.
- [ ] Why does an off-the-shelf LLM judge plateau at ~70–75% expert agreement, and what are the three alignment levers (prompt tuning, weak supervision/distillation, SME validation)?
- [ ] Cohen's kappa: judge and expert agree on 85 of 100 items, both say "pass" ~90% of the time — compute kappa and explain why raw agreement flatters the judge.
- [ ] Malformed-JSON gauntlet: write the parse-with-fallback function from memory (fences, trailing commas, prose around JSON) and say how each failure mode should be *counted* in an eval.
- [ ] Two medium DSA refreshers in Python, narrated (the onsite family still includes them per Glassdoor): hash-map counting + heap top-K.
- [ ] Project story, 3 minutes: a Coupang evaluation/data-quality decision — the disagreement, the rubric change, the metric that moved. (Deep-dive and fit rounds probe exactly this.)
- [ ] "Why Snorkel" in 3 sentences using the data-quality/evaluation mapping — no generic mission talk.

## Questions to ask

For Martin (Nov 10):
1. What does the team own day to day — the eval pipelines behind the expert-data business, or customer-facing agent builds?
2. In the grading stack, how much is programmatic verification vs. LLM judges vs. expert review today?
3. How do you measure grader quality internally — agreement with goldens, per-domain?

For Mengdie (Nov 12):
1. How are rubrics versioned and adjudicated when experts disagree?
2. What does the feedback loop from eval results into new data collection look like in practice?
3. What are the remaining rounds after this, and the timeline? (Also fine on Nov 10 if it fits.)

## 30-minute checklist — Tue Nov 10 (Building with AI, 10:00 AM)

- [ ] **NDA signed** (do it before, verify the DocuSign completion email).
- [ ] HackerRank link (https://hr.gs/1ec4172) opens; test the environment early if the link allows a dry run.
- [ ] Zoom link from Tyler's confirmation tested; quiet room; water.
- [ ] Gym 8:00–9:30 as usual — at your desk by 9:50. Nothing at 12:00 (round ends 11:00).
- [ ] On paper next to you: precision / recall / accuracy + kappa formulas; the build playbook's five phases.
- [ ] One warm-up: re-run your mini-grader drill for 10 minutes, out loud.
- [ ] Opening line ready: brief, warm; the search-ranking = evaluation mapping in one sentence.

## 30-minute checklist — Thu Nov 12 (AI System Design, 10:00 AM)

- [ ] Sketch the reference architecture once from memory (benchmark/rubric service → harness → graders → scoring/slicing → diagnosis loop) before the call.
- [ ] Snorkel vocabulary warm: task/trace/outcome/rubric; Evaluate → Curate → Refine; the 70–75% judge-agreement figure and the three alignment levers.
- [ ] One Coupang eval story loaded (disagreement → rubric change → metric moved) for the mapping moment.
- [ ] Zoom link tested; scratch paper + pen for the diagram talk-through; water.
- [ ] Gym 8:00–9:30 as usual — desk by 9:50; round ends 11:00, lunch hour stays clear.
- [ ] Closing questions for Mengdie ready (above).
