#!/usr/bin/env python3
"""Build the ml-interview-prep static site.

Reads content/companies/*.md + content/pages/*.md (YAML frontmatter + Markdown),
renders to HTML, and emits:
  index.html          - SPA shell (from assets/template.html)
  data/content.json   - all pages: slug, title, section, nav_order, nav_label,
                        tags, updated, html (+ company fields)
  data/search.json    - per-page search records (title, headings, plain text)

Usage: python3 build.py [--check]     # --check validates content, writes nothing
Idempotent: same input -> same output (no timestamps baked into JSON).
"""

import hashlib
import html as htmlmod
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
DATA = ROOT / "data"
ASSETS = ROOT / "assets"

# ---------------------------------------------------------------- frontmatter

try:
    import yaml

    def parse_frontmatter(text):
        return yaml.safe_load(text) or {}
except ImportError:  # minimal YAML-subset fallback
    def parse_frontmatter(text):
        return _mini_yaml(text)


def _strip_quotes(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s


def _flow_value(s):
    """Parse a simple inline scalar / [list] / {dict} value."""
    s = s.strip()
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        if not inner:
            return []
        return [_strip_quotes(p) for p in re.split(r",(?![^{]*})", inner)]
    if s.startswith("{") and s.endswith("}"):
        d = {}
        for part in re.split(r",(?![^\[]*\])", s[1:-1]):
            if ":" in part:
                k, v = part.split(":", 1)
                d[_strip_quotes(k)] = _coerce(_strip_quotes(v))
        return d
    return _coerce(_strip_quotes(s))


def _coerce(s):
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    if s.lower() in ("true", "yes"):
        return True
    if s.lower() in ("false", "no"):
        return False
    return s


def _mini_yaml(text):
    """Handles the SCHEMA.md frontmatter shapes: scalars, inline lists/dicts,
    and one-level block lists of '- { ... }' flow dicts."""
    data, cur_list_key = {}, None
    for line in text.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        m = re.match(r"^(\s*)-\s+(.*)$", line)
        if m and cur_list_key:
            data[cur_list_key].append(_flow_value(m.group(2)))
            continue
        m = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2)
            if val == "":
                data[key] = []
                cur_list_key = key
            else:
                data[key] = _flow_value(val)
                cur_list_key = None
    return data


def split_frontmatter(text, path):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not m:
        raise ValueError(f"{path}: missing YAML frontmatter (--- ... ---)")
    return parse_frontmatter(m.group(1)), m.group(2)

# ------------------------------------------------------------ markdown render

try:
    import markdown as _md

    HAVE_MARKDOWN = True
except ImportError:
    HAVE_MARKDOWN = False


def _slugify(text):
    text = re.sub(r"<[^>]+>", "", text).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "section"


# placeholder tokens: plain alphanumerics, invisible to the markdown parser
def _tok(kind, i):
    return f"ZZ{kind}{i:04d}ZZ"


class Renderer:
    """Markdown -> HTML with ml-interview-prep directives.

    Pipeline: protect fenced code / inline code / math / mermaid, extract
    :::directive blocks, rewrite task lists, run python-markdown, restore.
    """

    def __init__(self, slug):
        self.slug = slug
        self.task_idx = 0
        self.store = {}

    # -- protection -----------------------------------------------------
    def _stash(self, kind, value):
        i = len([k for k in self.store if k[0] == kind])
        tok = _tok(kind, i)
        self.store[(kind, i)] = value
        return tok

    def _protect_fences(self, text):
        def sub(m):
            lang, code = m.group(1) or "", m.group(2)
            if lang.strip().lower() == "mermaid":
                return self._stash("MERMAID", code.strip("\n"))
            return self._stash(
                "CODE",
                f'<pre><code class="language-{htmlmod.escape(lang.strip())}">'
                f"{htmlmod.escape(code.strip(chr(10)))}</code></pre>",
            )

        return re.sub(r"```(\w*)\n(.*?)```", sub, text, flags=re.S)

    def _protect_inline_code(self, text):
        return re.sub(
            r"`([^`\n]+)`",
            lambda m: self._stash("INLINE", htmlmod.escape(m.group(1))),
            text,
        )

    def _protect_math(self, text):
        text = re.sub(
            r"\$\$(.+?)\$\$",
            lambda m: self._stash("DMATH", "$$" + m.group(1) + "$$"),
            text,
            flags=re.S,
        )
        # Inline math: single-line only (no re.S), and never treat currency
        # like $200M / $5B / $/token as math: opening $ must not be
        # followed by $ or a digit.
        return re.sub(
            r"(?<!\$)\$(?![\$\d])([^$\n]+?)(?<!\$)\$(?!\$)",
            lambda m: self._stash("IMATH", "$" + m.group(1) + "$"),
            text,
        )

    # -- directives ------------------------------------------------------
    def _extract_directives(self, text):
        lines, out = text.splitlines(), []
        i = 0
        while i < len(lines):
            m = re.match(r"^\s*:::(tldr|warn|collapse)\s*(.*)$", lines[i])
            if not m:
                out.append(lines[i])
                i += 1
                continue
            kind, arg = m.group(1), m.group(2).strip()
            body, i = [], i + 1
            while i < len(lines) and not re.match(r"^\s*:::\s*$", lines[i]):
                body.append(lines[i])
                i += 1
            i += 1  # consume closing :::
            out.append(self._stash(kind.upper(), (arg, "\n".join(body))))
        return "\n".join(out)

    def _rewrite_task_lists(self, text):
        def sub(m):
            self.task_idx += 1
            checked = m.group(2).lower() == "x"
            box = (
                f'<input type="checkbox" class="task-cb" data-page="{self.slug}" '
                f'data-task="{self.task_idx}"{" checked" if checked else ""}>'
            )
            # Stash the raw HTML so the markdown pass (and _inline escaping
            # in the fallback renderer) can't mangle it; restored in render().
            return f"- {self._stash('TASKCB', box)} "

        return re.sub(r"^(\s*)-\s+\[([ xX])\]\s+", sub, text, flags=re.M)

    # -- main ------------------------------------------------------------
    def render(self, text, inner=False):
        text = self._protect_fences(text)
        text = self._protect_inline_code(text)
        text = self._protect_math(text)
        text = self._extract_directives(text)
        text = self._rewrite_task_lists(text)

        if HAVE_MARKDOWN:
            body_html = _md.markdown(
                text, extensions=["fenced_code", "tables", "sane_lists"]
            )
        else:
            body_html = _minimal_md(text)

        # restore: directives first (their bodies get rendered recursively)
        def restore(kind, fn):
            nonlocal body_html
            for (k, i), val in list(self.store.items()):
                if k == kind:
                    body_html = body_html.replace(
                        f"<p>{_tok(kind, i)}</p>", fn(val)
                    )
                    body_html = body_html.replace(_tok(kind, i), fn(val))

        restore("TLDR", lambda v: self._callout("tldr", "TL;DR", v[1]))
        restore("WARN", lambda v: self._callout("warn", "⚠ Note", v[1]))
        restore(
            "COLLAPSE",
            lambda v: self._collapse(v[0], v[1]),
        )
        restore("MERMAID", lambda v: f'<div class="mermaid">{v}</div>')
        restore("TASKCB", lambda v: v)
        restore("DMATH", lambda v: v)
        restore("IMATH", lambda v: v)
        restore(
            "CODE",
            lambda v: re.sub(
                r'class="language-">', 'class="language-plaintext">', v
            )
            if 'class="language-">' in v
            else v,
        )
        restore("INLINE", lambda v: f"<code>{v}</code>")

        if not inner:
            body_html = self._add_heading_ids(body_html)
        return body_html

    def _render_inner(self, text):
        sub = Renderer(self.slug)
        sub.task_idx = self.task_idx
        out = sub.render(text, inner=True)
        self.task_idx = sub.task_idx
        # merge stashes that only inner used (harmless: keyed uniquely anyway)
        self.store.update(sub.store)
        return out

    def _callout(self, cls, label, body):
        return (
            f'<div class="callout {cls}"><div class="callout-label">{label}</div>'
            f'<div class="callout-body">{self._render_inner(body)}</div></div>'
        )

    def _collapse(self, title, body):
        title_html = _md.markdown(title).strip() if HAVE_MARKDOWN else htmlmod.escape(title)
        title_html = re.sub(r"^<p>(.*)</p>$", r"\1", title_html, flags=re.S)
        return (
            f'<details class="collapse"><summary>{title_html}</summary>'
            f'<div class="collapse-body">{self._render_inner(body)}</div></details>'
        )

    def _add_heading_ids(self, html):
        def sub(m):
            level, inner_html = m.group(1), m.group(2)
            if 'id="' in m.group(0)[: m.group(0).index(">")]:
                return m.group(0)
            return f"<h{level} id=\"{_slugify(inner_html)}\">{inner_html}</h{level}>"

        return re.sub(r"<h([23])>(.*?)</h\1>", sub, html, flags=re.S)


def _minimal_md(text):
    """Fallback renderer if python-markdown is unavailable."""
    out, in_list, list_tag, last_li = [], False, None, None
    in_quote, quote_buf = False, []

    def flush_quote():
        nonlocal in_quote, quote_buf
        if not in_quote:
            return
        paras, cur = [], []
        for ql in quote_buf:
            if ql.strip():
                cur.append(ql.strip())
            elif cur:
                paras.append(" ".join(cur))
                cur = []
        if cur:
            paras.append(" ".join(cur))
        if paras:
            out.append(
                "<blockquote>"
                + "".join(f"<p>{_inline(p)}</p>" for p in paras)
                + "</blockquote>"
            )
        in_quote, quote_buf = False, []

    for line in text.splitlines():
        if line.startswith(">"):
            content = line[1:]
            if content[:1] == " ":
                content = content[1:]
            if in_list:
                out.append(f"</{list_tag}>")
                in_list, last_li = False, None
            quote_buf.append(content)
            in_quote = True
            continue
        flush_quote()
        if line.startswith("ZZ") and line.endswith("ZZ"):
            if in_list:
                out.append(f"</{list_tag}>")
                in_list, last_li = False, None
            out.append(line)
            continue
        m = re.match(r"^(#{1,4})\s+(.*)", line)
        if m:
            if in_list:
                out.append(f"</{list_tag}>")
                in_list, last_li = False, None
            out.append(f"<h{len(m.group(1))}>{_inline(m.group(2))}</h{len(m.group(1))}>")
            continue
        m = re.match(r"^(\s*)[-*]\s+(.*)", line)
        if m:
            if not in_list:
                out.append("<ul>")
                in_list, list_tag = True, "ul"
            out.append(f"<li>{_inline(m.group(2))}</li>")
            last_li = len(out) - 1
            continue
        if re.match(r"^\s*\d+\.\s+", line):
            if not in_list or list_tag != "ol":
                if in_list:
                    out.append(f"</{list_tag}>")
                out.append("<ol>")
                in_list, list_tag = True, "ol"
            out.append(f"<li>{_inline(re.sub(r'^\s*\d+\.\s+', '', line))}</li>")
            last_li = len(out) - 1
            continue
        if not line.strip():
            if in_list:
                out.append(f"</{list_tag}>")
                in_list, last_li = False, None
            continue
        # Indented continuation of the current list item: fold into the <li>
        # instead of breaking out into a separate paragraph.
        if in_list and last_li is not None and re.match(r"^\s+\S", line):
            out[last_li] = (
                out[last_li][: -len("</li>")] + " " + _inline(line.strip()) + "</li>"
            )
            continue
        if in_list:
            out.append(f"</{list_tag}>")
            in_list, last_li = False, None
        out.append(f"<p>{_inline(line)}</p>")
    flush_quote()
    if in_list:
        out.append(f"</{list_tag}>")
    return "\n".join(out)


def _inline(text):
    text = htmlmod.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text

# ------------------------------------------------------------------ sections

SECTIONS = [
    ("cram", "Interview Cram", "⚡"),
    ("companies", "Company Prep", "🏢"),
    ("fundamentals", "ML Fundamentals", "📐"),
    ("deep-learning", "Deep Learning", "🧠"),
    ("transformers", "Transformers", "🔁"),
    ("llm-systems", "LLM Systems", "⚙️"),
    ("rag", "RAG & Retrieval", "🔎"),
    ("recsys", "Recommenders", "🎯"),
    ("system-design", "ML System Design", "🏗️"),
    ("agent-design", "Agent Design", "🤖"),
    ("coding", "Coding", "💻"),
    ("debugging", "Debugging", "🐛"),
    ("ai-coding", "AI-Native Coding", "✨"),
    ("deep-dive", "Project Deep Dive", "🔬"),
    ("behavioral", "Behavioral", "💬"),
    ("resources", "Resources", "📚"),
]
SECTION_ORDER = {sid: i for i, (sid, _, _) in enumerate(SECTIONS)}

# --------------------------------------------------------------------- build

REQUIRED = ("title", "slug", "section")


def load_pages():
    pages = []
    seen = set()
    for subdir in ("companies", "pages"):
        d = CONTENT / subdir
        if not d.exists():
            continue
        for path in sorted(d.glob("*.md")):
            fm, body = split_frontmatter(path.read_text(encoding="utf-8"), path)
            for field in REQUIRED:
                if not fm.get(field):
                    raise ValueError(f"{path}: frontmatter missing required '{field}'")
            slug = str(fm["slug"])
            if slug != path.stem:
                raise ValueError(f"{path}: slug '{slug}' must match filename")
            if slug in seen:
                raise ValueError(f"{path}: duplicate slug '{slug}'")
            seen.add(slug)
            renderer = Renderer(slug)
            html = renderer.render(body)
            page = {
                "slug": slug,
                "title": str(fm["title"]),
                "section": str(fm["section"]),
                "nav_order": int(fm.get("nav_order", 999)),
                "nav_label": str(fm.get("nav_label", fm["title"])),
                "tags": list(fm.get("tags", []) or []),
                "updated": str(fm.get("updated", "")),
                "html": html,
            }
            for extra in ("company", "priority", "status", "process_sources"):
                if fm.get(extra) is not None:
                    page[extra] = fm[extra]
            pages.append(page)
    pages.sort(
        key=lambda p: (
            SECTION_ORDER.get(p["section"], 999),
            p["nav_order"],
            p["nav_label"].lower(),
        )
    )
    return pages


def plain_text(html):
    text = re.sub(r"<[^>]+>", " ", html)
    text = htmlmod.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def build_search(pages):
    records = []
    for p in pages:
        headings = re.findall(r"<h[23][^>]*>(.*?)</h[23]>", p["html"], flags=re.S)
        headings = [plain_text(h) for h in headings]
        text = plain_text(p["html"])
        if len(text) > 30000:  # keep the index lean
            text = text[:30000]
        records.append(
            {
                "slug": p["slug"],
                "title": p["title"],
                "nav_label": p["nav_label"],
                "section": p["section"],
                "tags": p["tags"],
                "headings": headings,
                "text": text,
            }
        )
    return records


def load_json_if_exists(path):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def main():
    check_only = "--check" in sys.argv
    pages = load_pages()
    companies = [p for p in pages if p["section"] == "companies"]

    questions = load_json_if_exists(DATA / "questions.json") or []
    flashcards = load_json_if_exists(DATA / "flashcards.json") or []

    content = {
        "meta": {
            "version": 1,
            "pages": len(pages),
            "companies": len(companies),
            "questions": len(questions),
            "flashcards": len(flashcards),
            "sections": [
                {"id": sid, "label": label, "icon": icon}
                for sid, label, icon in SECTIONS
            ],
        },
        "pages": pages,
    }
    content_json = json.dumps(content, ensure_ascii=False, separators=(",", ":"))
    search_json = json.dumps(
        build_search(pages), ensure_ascii=False, separators=(",", ":")
    )

    if check_only:
        print(f"CHECK OK: {len(pages)} pages ({len(companies)} companies), "
              f"{len(questions)} questions, {len(flashcards)} flashcards")
        return 0

    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "content.json").write_text(content_json, encoding="utf-8")
    (DATA / "search.json").write_text(search_json, encoding="utf-8")

    version = hashlib.sha1(content_json.encode()).hexdigest()[:8]
    template = (ASSETS / "template.html").read_text(encoding="utf-8")
    (ROOT / "index.html").write_text(
        template.replace("BUILDV", version), encoding="utf-8"
    )

    print(f"Built {len(pages)} pages ({len(companies)} companies), "
          f"{len(questions)} questions, {len(flashcards)} flashcards "
          f"-> index.html + data/content.json + data/search.json [v{version}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
