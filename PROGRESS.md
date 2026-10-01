# Progress

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
