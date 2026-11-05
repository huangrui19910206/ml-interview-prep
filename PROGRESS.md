# Progress

## 2026-11-04 — Harvey page: 1point3acres recheck + reschedule

- Coding round rescheduled: Mon 2026-11-09 10:00 AM PT, Kevin Ko
  (was Tue Nov 3 / Nick Howlett). Page retitled; TL;DR, drill heading
  and morning checklist updated to Nov 9.
- 1point3acres recheck (Rui rule: 面经提前查、一亩三分地第一来源):
  canonical "Spreadsheet / Formula Engine" problem page — SWE+MLE,
  medium, frequency Very high, last asked 2026-10-27, phone-screen +
  onsite-coding, 18 related discussions; experience index shows
  spreadsheet screens reported 2026-10-27 / 10-26 / 10-23 / 09-25.
  BBS thread-1181256 (2026-06-25, Pass) confirms the part structure
  (Part 1 literals via hashmap; Part 2 formulas + invalid-input /
  cyclic-dependency validation, topological sort explicitly expected)
  and that the poster passed without finishing. AceOffer 50-report
  aggregate (updated Nov 2026): spreadsheet took over from Apr 2026
  (~16 reports vs ~19 highlighting earlier); new AI-assisted onsite
  coding round reported since late summer 2026 — added to Later
  rounds. InterviewQuery / Glassdoor recheck: no new Harvey-specific
  detail. Verdict: 2026-10-29 conclusions unchanged.

## 2026-11-04 — Sequen prep page

- Added `content/companies/sequen.md` (engineering interview Fri 2026-11-06,
  13:00–13:30 PT, Ethan Benjamin, Google Meet; coordinator Stephen Armanios).
  面经 verdict: NONE — searched 1point3acres first, then InterviewQuery /
  Glassdoor / Blind / levels.fyi, then open web (2026-11-04); zero candidate
  reports, no public interviewer profile. Page is inference-labelled:
  company/product brief (LEMs, in-session re-ranking, sub-20ms, $6M seed →
  $16M Series A → Series B announced), 30-minute playbook, six inferred
  topic areas mapped to Rui's Coupang ammunition, questions for Ethan,
  two-interview-day Friday checklist (Applied coding 10:15 AM same day).

## 2026-11-04 — Applied Intuition prep page

- Added `content/companies/applied-intuition.md` (coding round Fri 2026-11-06,
  10:15 AM PT, Martin Meinke, CoderPad/Python): official rubric from
  applied.co/technical-interview + engineering-blog no-AI screen format;
  reported signature question (transactional KV store, 1point3acres Aug 2026)
  with delta-stack reference implementation and drill protocol; ML PyTorch
  debugging variant; reported practical-problem set; 45-min pacing table;
  night-before/morning checklist. Gated resource page (interview157) noted
  as not read (401).

## 2026-10-01 — full curriculum deployed (evening)

**Live:** https://huangrui19910206.github.io/ml-interview-prep/

- **32 pages / 18 companies / 160 questions / 61 flashcards**, all live.
- Curriculum: transformers (deep, from-scratch impl + shape drills), ML fundamentals
  (837 lines), deep learning, LLM systems (inference/training/evals with real
  arithmetic), RAG/search, recsys, agent system design, coding (16 tested problems),
  debugging (13 broken programs, hint→solution UI), AI-native coding (5 builds +
  rubrics), behavioral (staff-level, Rui-mapped stories), ML system-design framework,
  project deep-dive framework, 30-min cram.
- Interactive: flashcards (deck filter/flip/shuffle), mock interview
  (company × type × difficulty × duration), question bank (4 filters) — all live
  with real data.
- Renderer bugfix shipped: inline `$…$` regex was DOTALL and swallowed
  `$200M`-style currency across newlines, eating `:::directive` blocks on 3 pages.
  Fixed to single-line + no-digit-after-`$`.
- Backlog: interview map matrix, Harvey page, resources page, Interview-Tomorrow /
  7-day plans, mobile visual QA.

## 2026-10-01 — v1 deployed

**Live:** https://huangrui19910206.github.io/ml-interview-prep/

v1 (built the evening before Rui's Uber interviews, Oct 2):
- Site shell: SPA, hash routing, sticky grouped nav, mobile drawer, dark/light mode
  (persisted, no-flash), client-side search (`/` shortcut, ranked), auto-TOC with
  scroll-spy, per-page progress + checkbox persistence (localStorage), KaTeX /
  Mermaid / highlight.js via CDN with offline graceful degradation.
- Interactive views: flashcards (deck filter, flip, shuffle), mock interview
  (company × type × difficulty × duration), question bank (filters) — all read
  `data/questions.json` / `data/flashcards.json` live; graceful empty states until
  seeded.
- Content (13 pages): 30-minute cram, Uber (p0, interviewing), DoorDash, Crusoe,
  Factory, Glean, Sierra, OpenAI, Anthropic, Google DeepMind, xAI, ML system-design
  18-step framework, project deep-dive framework.
- Source labeling: OFFICIAL / REPORTED BY CANDIDATES / INFERRED / LIKELY on process
  claims; REPRESENTATIVE PRACTICE on questions. No fabricated "company asked this".

## Next (see TODO.md)

- P0: DoorDash/Crusoe/Factory depth for upcoming rounds, debugging exercises,
  AI-native coding exercises
- P1: transformers (deep), ML fundamentals, LLM systems, RAG, recsys, agent design,
  coding, behavioral
- P2: seed flashcards + question bank (150+), interview map matrix
