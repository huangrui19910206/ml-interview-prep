# ml-interview-prep

A practical, fast interview-prep site for senior/staff ML Engineer, AI Engineer,
Research Engineer, ML Systems, Search/Recommendation, and AI Platform interviews
at leading AI companies. Built for **quick review before an interview** and
**hands-on practice** — not textbook reading.

**Live site:** https://huangrui19910206.github.io/ml-interview-prep/

## Stack

- Static single-page app, hash-routed (`#/slug`) — works on GitHub Pages with no backend.
- Content: Markdown files under `content/` with YAML frontmatter (see `SCHEMA.md`).
- `build.py` renders Markdown → `index.html` + `data/content.json`.
- Vanilla JS + CSS. KaTeX for math, Mermaid for diagrams, highlight.js for code.
  No framework, no build step beyond `python3 build.py`.
- Progress persisted in `localStorage`.

## Develop

```bash
python3 build.py          # rebuild index.html + data/
python3 -m http.server    # serve locally, open http://localhost:8000
```

## Deploy

Push to `main` — GitHub Pages serves the branch root directly. After pushing,
verify https://huangrui19910206.github.io/ml-interview-prep/ returns 200
(allow a few minutes on first deploy).

## Docs

- `SCHEMA.md` — content schema (start here to add content)
- `ARCHITECTURE.md` — site architecture
- `TODO.md` — build backlog
- `PROGRESS.md` — what shipped when
