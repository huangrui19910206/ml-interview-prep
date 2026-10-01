# Architecture — ml-interview-prep

Static single-page app. No backend, no build tools beyond `python3 build.py`,
no npm. Hash routing only, so it works on GitHub Pages from the branch root.

```
content/companies/*.md ─┐
content/pages/*.md ─────┤  YAML frontmatter + Markdown
                        ▼
                    build.py ──► index.html            (SPA shell, from assets/template.html)
                             ├─► data/content.json    (all pages, rendered HTML)
                             └─► data/search.json     (per-page search records)
data/questions.json ───── (authored by hand, read live by the app)
data/flashcards.json ──── (authored by hand, read live by the app)
assets/app.js ──► loaded by index.html, fetches data/*.json at boot
assets/style.css ──► theming via CSS variables
```

## build.py

Single-file pipeline, stdlib + `pyyaml` + `markdown` (pip). Both are optional:
if `markdown` is missing it falls back to a minimal built-in renderer
(`_minimal_md`); if `pyyaml` is missing it falls back to `_mini_yaml`, which
handles the SCHEMA.md frontmatter shapes (scalars, inline `[lists]`,
`- {flow dicts}`).

Render pipeline per page (`Renderer.render`):

1. **Protect** fenced code blocks, inline code spans, `$…$` / `$$…$$` math
   (stashed as `ZZ…ZZ` tokens so the Markdown parser and emphasis rules
   can't mangle them — e.g. `$x_i$` underscores).
2. **Extract** custom directive blocks (see below); their bodies are rendered
   recursively at restore time.
3. **Rewrite** `- [ ]` / `- [x]` task lists into
   `<input type="checkbox" class="task-cb" data-page="slug" data-task="N">`.
4. Run `python-markdown` (`fenced_code`, `tables`, `sane_lists`).
5. **Restore** stashed blocks; add `id` attributes to `h2`/`h3`
   (slugified) for the client-side TOC.

Directives (block-level, closed by a lone `:::` line):

| Directive | Output |
|---|---|
| `:::tldr … :::` | `<div class="callout tldr">` highlighted box |
| `:::warn … :::` | `<div class="callout warn">` warning box |
| `:::collapse TITLE … :::` | `<details class="collapse"><summary>TITLE</summary>` |
| ` ```mermaid ` fence | `<div class="mermaid">` (raw diagram source) |
| `$…$`, `$$…$$` | passed through untouched for KaTeX auto-render |

Validation (hard errors, exit non-zero): missing frontmatter, missing
`title`/`slug`/`section`, slug ≠ filename, duplicate slugs.
`--check` validates without writing.

Outputs:

- `data/content.json` — `{meta, pages[]}`. Each page: `slug, title, section,
  nav_order, nav_label, tags, updated, html`, plus company passthrough fields
  (`company, priority, status, process_sources`). `meta.sections` carries the
  canonical section order/labels/icons.
- `data/search.json` — per page: `slug, title, nav_label, section, tags,
  headings[], text` (HTML stripped, truncated to 30k chars).
- `index.html` — `assets/template.html` with `BUILDV` replaced by a content
  hash (cache-busting query param on `app.js`/`style.css`).

Deterministic: same input → byte-identical output (no timestamps baked in).

## app.js (vanilla SPA, ~1000 lines)

- **Boot**: reads theme, fetches the four JSON files in parallel
  (`fetchJson` returns `null` on failure — missing `questions.json` /
  `flashcards.json` render graceful empty states, never crash), builds the
  nav, then renders the current hash.
- **Router** (`parseRoute`, pure/tested): `#/` home · `#/slug` page ·
  `#/section/<id>` listing · `#/flashcards` · `#/mock` · `#/questions` ·
  anything else → friendly 404.
- **Home dashboard**: 12 cards (cram, mock, bank, flashcards, sections).
  Section cards show live `done/total` + progress bar; overall bar on top.
- **Page view**: title, meta row (section, updated, tags, company/priority/
  status badges), `process_sources` in a collapsible, Mark-complete button,
  sticky auto-TOC from `h2[id]`/`h3[id]` with IntersectionObserver scroll-spy
  (desktop right rail, hidden on mobile).
- **Search**: header box, `/` focuses, `Esc` clears, ↑/↓ + Enter navigate.
  `rankSearch` (pure/tested): all query terms must appear; scores
  title×6, headings×4, tags×3, body×1; shows a snippet.
- **Progress**: `mlip.done.v1` (`{slug: true}`) in localStorage; task
  checkboxes persist per page in `mlip.tasks.v1.<slug>` (`{taskIdx: true}`),
  with strikethrough styling.
- **Theme**: `data-theme` on `<html>`, toggle in topbar, `mlip.theme` in
  localStorage, `prefers-color-scheme` default; an inline head script sets the
  theme before first paint (no flash).
- **Flashcards** (`#/flashcards`): deck filter, click-to-flip CSS 3D cards,
  shuffle.
- **Mock** (`#/mock`): company × type × difficulty × duration → shuffled
  queue sized to fit the duration (≥1 question), one at a time, reveal-answer
  with optional `rubric` + `answer_ref` link, prev/next, finish summary.
- **Question bank** (`#/questions`): company/category/difficulty/label/text
  filters over `data/questions.json`.
- **CDN libs** (all guarded with `typeof` checks — site works offline without
  them): KaTeX 0.16.11 auto-render, Mermaid 11 (`mermaid.run` per render,
  theme-aware), highlight.js 11 (token colors come from our CSS variables so
  code blocks follow the theme).
- Mobile: hamburger → slide-in nav drawer + scrim; TOC hidden <1180px.
- Pure helpers (`parseRoute`, `rankSearch`, `filterQuestions`, `esc`) are
  exported under `module.exports` when loaded in node, so they can be unit
  tested without a browser (see QA below).

## style.css

Engineering-dashboard look: dense but readable. All colors via CSS variables
under `[data-theme="light"]` / `[data-theme="dark"]`; components (callouts,
cards, tables, code, badges, flashcards, mock) reference variables only.
Responsive breakpoints at 1180px and 820px. Minimal `@media print` rules.

## Content authoring

Add `content/pages/<slug>.md` or `content/companies/<slug>.md` per SCHEMA.md,
run `python3 build.py`, done. Internal links must be `[text](#/slug)`.
Mark trackable practice items with `- [ ]`.

## QA performed (v1, 2026-10-01)

- `python3 build.py --check` + full build: validates frontmatter/slugs.
- Back-to-back builds byte-identical (idempotent).
- `node --check assets/app.js` clean.
- jsdom harness (`/tmp/domtest/smoke.js`, 30 assertions, since removed):
  home/nav/footer, page render + TOC, mermaid/task/math/callout/collapse
  rendering, search results, theme toggle + persistence, mark-complete +
  nav dot, checkbox persistence, flashcards flip + deck filter, mock session
  start + reveal, question-bank filters, section listing, 404 — **all pass,
  zero JS errors**.
- Served via `python3 -m http.server`; all 7 assets return 200.

## Known limitations / follow-ups

- Search is client-side over `data/search.json` — fine at this scale; if the
  corpus grows 10×, consider a build-time inverted index.
- Mermaid re-renders per page view; theme changes re-render on next navigation
  (diagrams keep the theme they were rendered with until then).
- `:::collapse` inside list items isn't supported (block-level only).
- `$` currency figures in prose can be misread as math delimiters; prefer
  escaping or rewording in content.
- No service worker / offline bundling of CDN libs yet — offline degrades
  gracefully (no math/diagram/code-highlight rendering) but still readable.
