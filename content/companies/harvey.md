---
title: "Harvey — Coding: Building a Spreadsheet (Mon 2026-11-09, Kevin Ko)"
slug: "harvey"
section: "companies"
nav_order: 86
nav_label: "Harvey"
tags: ["coding", "graphs", "data-structures", "python", "interviewing", "legal-ai"]
updated: "2026-11-04"
company: "Harvey"
priority: "p0"
status: "interviewing"
process_sources:
  - { label: "OFFICIAL", url: "", accessed: "2026-10-29", note: "Confirmation email reported 2026-10-27 evening PT: coding round Tue 2026-11-03 10:00-11:00 AM PT with Nick Howlett, topic 'Coding - Building a Spreadsheet'; Zoom + BrightHire recording details in the calendar event. Recruiter line: Andrew Kim, Senior Technical Recruiter, advanced Rui 2026-10-21" }
  - { label: "REPORTED", url: "https://prachub.com/companies/harvey", accessed: "2026-10-29", note: "57 reported Harvey questions: coding circles retrieval + text-under-structure; the spreadsheet formula engine recurs in several variants — staged build (set/get first, formulas later), formulas evaluated in set_cell, eager formulas with constant-time cached reads + transitive dependency updates + CYCLE-REJECTING WRITES + atomic definition replacement, and cycle detection before evaluation. Other recurring coding: citation/highlight merging and ranking, in-memory file vault with duplicate-name handling, embedding retrieval with cosine similarity (notebook)" }
  - { label: "REPORTED", url: "https://www.techprep.app/blog/harvey-interview-process", accessed: "2026-10-29", note: "Process: recruiter screen (15-30m) -> HM screen (~45m) -> technical phone screen (~60m live coding, Python most common) -> virtual onsite 4-5 rounds (coding, system design e.g. document processing / RAG pipelines, product & AI thinking, behavioral); feedback often within 48h per stage; founder/exec round for senior+" }
  - { label: "REPORTED", url: "https://a16zjobs.substack.com/p/inside-harvey-the-4-year-old-legal", accessed: "2026-10-29", note: "Company profile: founded 2022 by Winston Weinberg (lawyer) + Gabe Pereyra (ex-DeepMind); valuation path $3B (Feb 2025) -> $5B -> $8B -> $11B (Mar 2026) -> $15.5B on a $550M round (Sep 2026); 3,000+ customers in 70 countries, 80% of Am Law 100; ARR above $400M; every all-hands opens with a customer interview; hiring screens for 'why transform legal work', not generic applied-AI enthusiasm" }
  - { label: "OFFICIAL", url: "", accessed: "2026-11-04", note: "Rescheduled 2026-11-03 by Andrew Kim (Senior Technical Recruiter): coding round moved to Mon 2026-11-09, 10:00-11:00 AM PT, interviewer Kevin Ko, topic unchanged ('Building a Spreadsheet'); replaces the Tue Nov 3 / Nick Howlett slot" }
  - { label: "REPORTED", url: "https://www.1point3acres.com/interview/problems/company/harvey/spreadsheet-formula-engine", accessed: "2026-11-04", note: "1point3acres recheck (Rui rule: 1p3a first). Canonical problem page 'Spreadsheet / Formula Engine': SWE+MLE, medium, frequency Very high, LAST ASKED 2026-10-27, used in phone-screen AND onsite-coding, 60 min, 18 related discussions (full statement members-only). Company bank indexes 26 coding problems; ~10 are spreadsheet variants incl. 'Mini Spreadsheet with Eager Evaluation and Cycle Detection' and 'Spreadsheet with O(1) Read and Dependency Management'. Experience index shows spreadsheet phone screens reported 2026-10-27, 2026-10-26, 2026-10-23 and 2026-09-25 (set_cell/get_cell) — question live and unchanged into late Oct 2026" }
  - { label: "REPORTED", url: "https://www.1point3acres.com/bbs/thread-1181256-1-1.html", accessed: "2026-11-04", note: "1point3acres BBS first-hand report, 2026-06-25, verdict Pass / Positive. Visible text: Part 1 = spreadsheet class with get_cell()/set_cell(), input is cell id + integer value, plain hashmap suffices. Part 2 (partly points-hidden): formulas, validation of invalid inputs and cyclic dependencies; interviewer explicitly expected TOPOLOGICAL SORT to compute values. Poster did NOT finish the question and still passed" }
  - { label: "REPORTED", url: "https://aceoffer.app/interviews/harvey/interview-process", accessed: "2026-11-04", note: "Aggregator over 50 candidate reports (Mar 2025 - Oct 2026), refreshed Nov 2026: through 2025/early-2026 ~19 reports got text highlighting; FROM APRIL 2026 the spreadsheet took over (~16 reports), highlighting still appears. Phone screen ~60 min, CoderPad in reports naming a tool, run against tests; 'an hour is tight' and over-talking before coding are repeated failure modes. NEW: since late summer 2026 recruiters describe an AI-ASSISTED onsite coding round (own IDE + Claude Code/Cursor, 60 min, working MVP under changing requirements); two Aug 2026 candidates still had standard rounds. InterviewQuery: no Harvey-specific page found in this recheck; Glassdoor: no new spreadsheet specifics beyond what aggregators already cite" }
---

## TL;DR

**Status: advanced by Andrew Kim (Senior Technical Recruiter) 2026-10-21;
rescheduled 2026-11-03. Next: Coding — "Building a Spreadsheet",
Mon 2026-11-09, 10:00–11:00 AM PT, Kevin Ko, Zoom + BrightHire recording.**

**1point3acres recheck 2026-11-04: nothing about this round has changed.
The spreadsheet question is still the live phone-screen question — last
reported asked 2026-10-27, frequency "very high". Details below.**

This is a practical modelling exercise, not LeetCode DS&A. You build a
small spreadsheet engine in stages: literals first, then formulas with
cell references, then recalculation on change, then cycle handling.
Reported variants differ on two axes, so clarify both in the first two
minutes: **(1) eager vs lazy evaluation** — at least one reported variant
evaluates in `set_cell` and wants O(1) cached reads; **(2) cycle
semantics** — some variants reject the *write* that would create a cycle
(and must do so atomically, leaving the old definition intact), others
raise/surface an error on read. Getting the variant right is half the
test; the graph machinery underneath is the same either way.

:::warn
**Do not prep generic LeetCode for this round.** The drill below is the
prep: one timed 60-minute spreadsheet build before Nov 9. Gym 8:00–9:30
AM is protected — be at the desk by 09:50.
:::

## Recheck 2026-11-04 — 1point3acres first (Rui's standing rule)

Checked directly on 1point3acres (question bank + BBS), then
InterviewQuery / Glassdoor. Verdict: **the 2026-10-29 conclusions hold;
the additions below sharpen pacing and part structure.**

- **Still the live question.** 1p3a's canonical problem page
  ("Spreadsheet / Formula Engine", SWE+MLE, medium) shows frequency
  **Very high, last asked 2026-10-27**, used in both phone screens and
  onsite coding, 60 min, 18 related discussions. The experience index
  shows spreadsheet phone screens reported 2026-10-27, 2026-10-26,
  2026-10-23 and 2026-09-25 — no rotation away from this question.
- **Part structure from a first-hand BBS report (2026-06-25, Pass).**
  Part 1: class with `get_cell()` / `set_cell()`; input is a cell id
  and an integer value; a plain hashmap suffices. Part 2: formulas
  plus validation — invalid inputs and cyclic dependencies — and the
  interviewer **explicitly expected topological sort** to compute
  values. (Part 2 detail is partly points-hidden on the forum; the
  visible fragments plus the bank's variant names agree with the
  staged build on this page.)
- **You do not have to finish to pass.** That poster did not complete
  the question and still passed. The repeated failure mode across
  reports is the opposite: discussion eating the coding time. Get
  Part 1 running in minutes, run code after each part, keep
  clarifying questions to the two-minute fork above.
- **Rotation context (50-report aggregator, updated Nov 2026).**
  Through 2025 and early 2026 most screens were the text-highlighting
  problem (~19 reports); **from April 2026 the spreadsheet took over
  (~16 reports)**. Highlighting still appears occasionally — it stays
  in Later rounds below, but the spreadsheet is the drill.
- **Format notes.** Reports naming a tool say CoderPad, ~60 minutes,
  run against tests; some interviewers bring tests, others have you
  write your own. Rui's own confirmation for Nov 9 says Zoom +
  BrightHire — follow the confirmation, and have tests ready to write
  yourself either way.
- **InterviewQuery / Glassdoor:** no Harvey-specific page or new
  spreadsheet detail found in this recheck beyond what the
  aggregators already cite. Not a gap in the prep — 1p3a is the
  deepest source for this company.

## Company & product

Harvey is the legal-AI platform: drafting and Q&A over firm documents,
secure document storage (Vault), review tables, multi-step agent
workflows, legal research with citations, Word/Outlook add-ins. Founded
2022 in SF by Winston Weinberg and Gabe Pereyra; seeded by the OpenAI
Startup Fund. 2026 trajectory is extreme even by AI standards: $11B
valuation in March, **$15.5B on a $550M round in September**, ARR above
$400M, 3,000+ customers, 80% of the Am Law 100. It also shipped its own
post-trained model (Tenet) and a legal-agent benchmark (LAB) in 2026.

**Your mapping (say it in the room):** Harvey's core engineering problems
are retrieval and evaluation over petabyte-scale document corpora —
searching, ranking citations, and verifying AI output before a lawyer
relies on it. That is your Coupang Search & Discovery home turf
(multi-stage ranking, generative retrieval, offline eval) pointed at
legal documents instead of products. In the behavioral/product rounds,
anchor on *why legal*: high-stakes, verification-obsessed work where a
wrong citation is a malpractice risk — evaluation rigor is the product.

## The exercise — what actually decides it

Build order that covers every reported variant:

1. **Stage 1 — literals.** `set_cell(name, value)` / `get_cell(name)`
   over a dict. Names are column letters + row number (`A1`, `C12`) —
   multi-letter columns exist in at least one variant, so parse with a
   regex, not `name[0]` / `name[1:]` assumptions.
2. **Stage 2 — formulas.** Content starting with `=` references other
   cells plus `+ - * /`, parentheses, unary minus. Tokenise and parse
   once on set (recursive descent or shunting-yard); store the AST and
   the precedent set. Never re-parse on read.
3. **Stage 3 — recalculation.** Keep reverse edges
   (`dependents[precedent] -> {cells that use it}`). On a write, either
   push: recompute transitive dependents in topological order (eager
   variant, reads stay O(1)); or mark them dirty and recompute lazily
   on get with memoisation inside one pass (handles the diamond case:
   D1 computed once, from consistent values).
4. **Stage 4 — cycles.** Self-reference and 2-cycles minimum. If the
   variant is cycle-rejecting writes: detect *before* committing —
   walk precedents of the new formula; if the cell itself is reachable,
   reject and leave the previous definition and all cached values
   untouched (atomicity is explicitly tested in one variant). If the
   variant is error-on-read: a `visiting` set during evaluation raises
   `#CYCLE!`.

### Clarifying questions to open with (2 minutes, don't skip)

1. Cell naming: single letter only, or multi-letter columns / big grid?
2. Values: integers, floats, text, empty cells — and what does `get` on
   a never-set cell return?
3. Formula grammar: just `+ - * /` and refs, or parentheses, unary
   minus, functions like `SUM(A1:A5)`?
4. Evaluation timing: eager on set (cached reads) or lazy on get?
5. Cycles: reject the write, error value, or exception? Can a cycle
   even be constructed — i.e. can a formula reference a not-yet-set
   cell?
6. API/error shape: class with `set_cell`/`get_cell`; errors as
   exceptions or sentinel strings?

### Edge cases to handle before extensions

- Overwriting a formula with a literal and vice versa — old precedents
  must be unwired, stale dependents must not linger.
- Division by zero; reference to an empty cell.
- Diamond dependency (A1→B1, A1→C1, B1+C1→D1): consistent values, D1
  evaluated once.
- Operator precedence and parentheses; `=-A1`.
- Rejected cycle write leaves the sheet exactly as it was (atomicity).

### Likely extensions if the core lands early

1. Range functions: `SUM(A1:A5)` — expand the range into precedents.
2. Error values (`#CYCLE!`, `#DIV/0!`) propagating through dependents.
3. Copy/paste with relative references — only if asked; don't
   volunteer scope.

### Complexity to state out loud

- Clean read: O(1) (cached). Eager write: O(size of the affected
  transitive-dependent subgraph). Lazy dirty read: O(affected subgraph),
  amortised by memoisation. Cycle check on write: O(reachable
  precedents).

## 60-minute practice drill (do once before Nov 9, timed)

- 0–10 min: literals + `set_cell`/`get_cell` + simple `=A1+B1`.
- 10–25 min: full parser — precedence, parentheses, unary minus,
  multi-letter columns.
- 25–40 min: dependency graph both directions; eager recompute in
  topological order; diamond case test.
- 40–50 min: cycle-rejecting write with atomic rollback; div-by-zero.
- 50–60 min: re-read as the interviewer would; name the tests out loud:
  chain update, diamond, self-cycle, 2-cycle, formula→literal
  overwrite, rejected write leaves state intact.

Plain Python, dicts only, no libraries, no AI tools assumed.

## Later rounds (REPORTED — for after Nov 9)

- **NEW — AI-assisted onsite coding (reported since late summer
  2026):** recruiters describe a 60-minute onsite round in your own
  IDE with an AI tool (Claude Code / Cursor), building a working MVP
  that runs locally while requirements change mid-round; graded on
  clarifying, decomposition, reviewing the AI's code and testing.
  No candidate report of the actual problem yet, and two Aug 2026
  candidates still had standard rounds — if the onsite comes, ask
  Andrew Kim which format applies.

- **System design:** document-processing / RAG pipelines over legal
  corpora, fault tolerance for sensitive data.
- **Coding variants beyond the spreadsheet:** embedding retrieval with
  cosine similarity in a notebook (plus choosing the metric), merging
  exact-word highlights across sources and ranking the citations they
  belong to, an in-memory file vault with duplicate-name suffixing.
- **Product/AI thinking:** how do you evaluate the correctness of an
  AI-generated legal brief; verification and citation discipline.
- **Behavioral:** project deep dive tied to Harvey's values; senior+
  may get a founder/exec round. Harvey screens explicitly for wanting
  to transform *legal* work — prepare one concrete, non-generic reason.

## Morning checklist (Mon Nov 9)

- [ ] Gym 8:00–9:30 as usual; desk by 09:50, Zoom + BrightHire consent
      handled on entry. Interviewer today is Kevin Ko.
- [ ] One pass over the clarifying questions and the eager-vs-lazy /
      reject-vs-error fork — say the fork out loud in the first two
      minutes.
- [ ] Python environment sanity: plain editor fluency, no autocomplete
      dependence.
- [ ] Pacing rule from the 1p3a recheck: Part 1 (literals) running in
      the first minutes, code run after every part — a clean partial
      beats a discussed-but-unfinished full build.
