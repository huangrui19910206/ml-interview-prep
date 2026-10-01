# Content Schema — ml-interview-prep

All curriculum content lives as Markdown files under `content/`. A Python
build script (`build.py`) renders them into a single-page app
(`index.html` + `data/content.json`). Adding a company = adding one file.

## Layout

```
content/
  companies/<slug>.md      # one per company, e.g. uber.md
  pages/<slug>.md          # curriculum pages, e.g. transformers.md, cram-30min.md
data/
  questions.json           # question bank (schema below)
  flashcards.json          # flashcards (schema below)
assets/
  style.css                # source stylesheet
  app.js                   # source SPA: router, search, theme, flashcards, mock mode, progress
```

## Markdown frontmatter (YAML, required)

```yaml
---
title: "Uber — Senior/Staff MLE Interview Prep"
slug: "uber"                    # must match filename, URL-safe, lowercase-hyphens
section: "companies"            # see sections below
nav_order: 10                   # ordering within its section nav
nav_label: "Uber"               # short label for nav
tags: ["system-design", "behavioral"]
updated: "2026-10-01"
# --- company pages only ---
company: "Uber"
priority: "p0"                  # p0 = Rui interviews here soon / top target
status: "interviewing"          # interviewing | target | research
process_sources:                # every process claim must trace to one of these
  - { label: "OFFICIAL",   url: "https://...", accessed: "2026-10-01", note: "Uber careers page" }
  - { label: "REPORTED",   url: "https://...", accessed: "2026-10-01", note: "2026 candidate report" }
  - { label: "INFERRED",   url: "",            accessed: "2026-10-01", note: "reasoning from JD + role level" }
---
```

### Sections

`cram` (rapid review) · `companies` · `fundamentals` (ML) · `deep-learning` ·
`transformers` · `llm-systems` · `rag` · `recsys` · `system-design` ·
`agent-design` · `coding` · `debugging` · `ai-coding` (AI-native build) ·
`deep-dive` (project) · `behavioral` · `resources`

## Markdown body conventions

Every concept page SHOULD follow this hierarchy (stop wherever depth suffices):

```
## TL;DR
## Interview answer
## Intuition
## Details
## Math
## Code
## Follow-ups
## Mistakes
## Practice
```

Company pages SHOULD follow:

```
## TL;DR
## Company & product
## Role expectations
## Interview process        (each round tagged OFFICIAL / REPORTED / INFERRED)
## Priority topics
## Company-specific themes
## Likely system-design domains
## Project deep-dive emphasis
## Recent work worth knowing
## Practice questions       (10-20)
## 30-minute checklist      ("interview tomorrow" checklist)
```

### Custom directives (the renderer supports these)

- `:::tldr ... :::` — highlighted TL;DR callout box
- `:::collapse TITLE` … `:::` — collapsible section (hints, solutions)
- `:::warn ... :::` — warning callout (e.g. anecdote vs official)
- Standard fenced code blocks with language tags (python, sql, bash).
- Math: inline `$...$` and block `$$...$$` (KaTeX auto-render).
- Mermaid: ```` ```mermaid ```` blocks render as diagrams.
- Internal links: `[text](#/slug)` — always hash routes.
- Footnote-style source refs: `[OFFICIAL: careers page](url)`.

### Source-labeling rules (non-negotiable)

- Company interview-process claims MUST be labeled
  `OFFICIAL` / `REPORTED BY CANDIDATES` / `INFERRED / LIKELY`.
- Never present an anecdote as official. Record URL + access date in
  `process_sources` frontmatter.
- Question bank items MUST be labeled
  `VERIFIED` / `REPORTED` / `REPRESENTATIVE PRACTICE`.
  Never fabricate "company X asked this."

## data/questions.json

```json
[
  {
    "id": "q-uber-sysdesign-001",
    "question": "Design ...",
    "companies": ["uber"],
    "category": "system-design",
    "difficulty": "hard",
    "time_min": 45,
    "frequency": "high",
    "label": "REPRESENTATIVE PRACTICE",
    "coding": false,
    "answer_available": true,
    "answer_ref": "#/system-design-framework",
    "source": { "url": "", "accessed": "2026-10-01", "note": "" }
  }
]
```

Categories: `coding` `ml-coding` `ml-fundamentals` `transformers` `llm-systems`
`system-design` `agent-design` `rag` `recsys` `debugging` `deep-dive`
`behavioral` `research`.

## data/flashcards.json

```json
[
  { "id": "fc-001", "front": "Why divide attention logits by sqrt(d_k)?",
    "back": "...", "tags": ["transformers"], "deck": "transformers" }
]
```

## Progress tracking

Content authors: mark practice items with `- [ ]` task lists where the user
should track completion. The app persists checkbox state + page-visited state
in localStorage.
