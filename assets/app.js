'use strict';
/* ML Interview Prep — vanilla SPA.
   Hash router, client search, theme, progress, flashcards, mock, question bank.
   Pure helpers (parseRoute, rankSearch, filterQuestions, esc) are exported for
   node-based tests; all DOM work is guarded so the file loads without a browser. */

const $ = (s, r) => (r || document).querySelector(s);
const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

const LS = {
  get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} },
};

/* ---------------- state ---------------- */
let META = { sections: [], pages: 0 };
let PAGES = [], BY_SLUG = {}, SECTIONS = [];
let SEARCH = [], QUESTIONS = [], FLASHCARDS = [];
let SEARCH_READY = false;

const LS_DONE = 'mlip.done.v1';
const LS_THEME = 'mlip.theme';
const taskKey = (slug) => `mlip.tasks.v1.${slug}`;
const getDone = () => LS.get(LS_DONE, {});
const setDone = (slug, val) => { const d = getDone(); if (val) d[slug] = true; else delete d[slug]; LS.set(LS_DONE, d); };

/* ---------------- routing (pure) ---------------- */
function parseRoute(hash) {
  const h = (hash || '').replace(/^#/, '');
  if (h === '' || h === '/') return { view: 'home' };
  if (h === '/flashcards') return { view: 'flashcards' };
  if (h === '/mock') return { view: 'mock' };
  if (h === '/questions') return { view: 'questions' };
  const m = h.match(/^\/section\/([a-z0-9-]+)$/);
  if (m) return { view: 'section', section: m[1] };
  const p = h.match(/^\/([a-z0-9-]+)$/);
  if (p) return { view: 'page', slug: p[1] };
  return { view: '404', raw: h };
}

/* ---------------- search (pure) ---------------- */
function tokenize(q) {
  return q.toLowerCase().split(/[^a-z0-9+]+/).filter((t) => t.length > 0);
}
function countHits(text, terms) {
  const t = text.toLowerCase();
  let n = 0;
  for (const term of terms) { let i = -1; while ((i = t.indexOf(term, i + 1)) !== -1) n++; }
  return n;
}
/** Rank search records for a query. Returns [{rec, score, snippet}]. */
function rankSearch(query, records) {
  const terms = tokenize(query).filter((t) => t.length >= 2);
  if (!terms.length) return [];
  const out = [];
  for (const rec of records) {
    const hay = `${rec.title} ${rec.nav_label} ${rec.headings.join(' ')} ${rec.text} ${(rec.tags || []).join(' ')}`;
    const low = hay.toLowerCase();
    if (!terms.every((t) => low.includes(t))) continue; // all terms must appear
    const score =
      6 * countHits(rec.title, terms) +
      4 * countHits(rec.headings.join(' '), terms) +
      3 * countHits((rec.tags || []).join(' '), terms) +
      1 * countHits(rec.text, terms);
    // snippet around first hit in body text
    let snippet = '';
    const first = terms.map((t) => low.indexOf(t)).filter((i) => i >= 0);
    if (first.length) {
      const pos = Math.min.apply(null, first.map((i) => Math.max(0, i - rec.title.length - rec.headings.join(' ').length)));
      const start = Math.max(0, pos - 60);
      snippet = rec.text.slice(start, start + 160).trim();
    }
    out.push({ rec, score, snippet });
  }
  out.sort((a, b) => b.score - a.score);
  return out.slice(0, 25);
}

/** Filter question-bank items. All filters optional. (pure) */
function filterQuestions(items, f) {
  return items.filter((q) => {
    if (f.company && !(q.companies || []).includes(f.company)) return false;
    if (f.category && q.category !== f.category) return false;
    if (f.difficulty && q.difficulty !== f.difficulty) return false;
    if (f.label && q.label !== f.label) return false;
    if (f.text) {
      const hay = `${q.question} ${q.id} ${(q.companies || []).join(' ')}`.toLowerCase();
      if (!f.text.toLowerCase().split(/\s+/).every((t) => hay.includes(t))) return false;
    }
    return true;
  });
}

function shuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/* ---------------- labels ---------------- */
function sectionMeta(id) {
  return SECTIONS.find((s) => s.id === id) || { id, label: id.replace(/-/g, ' '), icon: '📄' };
}
function labelBadge(label) {
  const cls = 'label-' + String(label || '').toLowerCase().replace(/[^a-z]+/g, '');
  return `<span class="badge ${cls}">${esc(label)}</span>`;
}

/* ============================ VIEWS ============================ */

const DASHBOARD = [
  { title: 'Interview Tomorrow', desc: 'Night-before checklist: what to review, logistics, mindset.', icon: '🌙', section: 'cram' },
  { title: '30-Min Cram', desc: 'Highest-yield rapid review right before you walk in.', icon: '⚡', section: 'cram' },
  { title: 'Mock Interview', desc: 'Timed practice — pick company, type, difficulty, duration.', icon: '🎙', view: 'mock' },
  { title: 'Question Bank', desc: 'Every practice question, filterable by company and topic.', icon: '❓', view: 'questions' },
  { title: 'Flashcards', desc: 'Flip-card recall for formulas, definitions, gotchas.', icon: '🗂', view: 'flashcards' },
  { title: 'Company Prep', desc: 'Process, rounds, and company-specific themes.', icon: '🏢', section: 'companies' },
  { title: 'ML Fundamentals', desc: 'Losses, optimization, metrics, bias/variance.', icon: '📐', section: 'fundamentals' },
  { title: 'Transformers', desc: 'Attention, shapes, from-scratch implementation drills.', icon: '🔁', section: 'transformers' },
  { title: 'LLM Systems', desc: 'Inference, KV cache, batching, quantization, training.', icon: '⚙', section: 'llm-systems' },
  { title: 'ML System Design', desc: 'Frameworks and reps for design rounds.', icon: '🏗', section: 'system-design' },
  { title: 'Coding', desc: 'Warm-ups, interview hards, ML-flavored coding.', icon: '💻', section: 'coding' },
  { title: 'Project Deep Dive', desc: 'Your stories, structured for staff-level depth.', icon: '🔬', section: 'deep-dive' },
];

function sectionPages(section) { return PAGES.filter((p) => p.section === section); }
function sectionProgress(section) {
  const pages = sectionPages(section);
  if (!pages.length) return null;
  const done = getDone();
  const n = pages.filter((p) => done[p.slug]).length;
  return { total: pages.length, done: n, pct: Math.round((100 * n) / pages.length) };
}

function cardLink(card) {
  if (card.view) return '#/' + card.view;
  return '#/section/' + card.section;
}
function cardMeta(card) {
  if (card.view === 'mock') return QUESTIONS.length ? `${QUESTIONS.length} questions` : 'bank loading…';
  if (card.view === 'questions') return QUESTIONS.length ? `${QUESTIONS.length} questions` : 'bank loading…';
  if (card.view === 'flashcards') return FLASHCARDS.length ? `${FLASHCARDS.length} cards` : 'no decks yet';
  const pr = sectionProgress(card.section);
  if (!pr) return 'coming soon';
  return `<span>${pr.done}/${pr.total} done</span><span>${pr.pct}%</span>`;
}
function cardBar(card) {
  const pr = card.section ? sectionProgress(card.section) : null;
  if (!pr) return '';
  return `<div class="mini-bar"><div style="width:${pr.pct}%"></div></div>`;
}

function viewHome() {
  const done = getDone();
  const total = PAGES.length, ndone = PAGES.filter((p) => done[p.slug]).length;
  const pct = total ? Math.round((100 * ndone) / total) : 0;
  const cards = DASHBOARD.map((c) => `
    <a class="dash-card" href="${cardLink(c)}">
      <span class="dc-icon">${c.icon}</span>
      <span class="dc-title">${esc(c.title)}</span>
      <span class="dc-desc">${esc(c.desc)}</span>
      <span class="dc-meta">${cardMeta(c)}</span>
      ${cardBar(c)}
    </a>`).join('');
  return `
  <div class="content-inner">
    <div class="dash-hero">
      <h1>ML Interview Prep</h1>
      <p>Rapid-review sheets, company intel, system-design frameworks, coding reps,
         mock interviews and flashcards — built for senior/staff ML interviews.</p>
      <div class="progress-wrap"><div class="progress-bar" style="width:${pct}%"></div></div>
      <div class="progress-label">${ndone} of ${total} pages complete · press <b>/</b> to search</div>
    </div>
    <div class="card-grid">${cards}</div>
    <h2 class="sec-title">All sections</h2>
    <p class="sec-sub">Every page, grouped. Check pages off as you finish them.</p>
    ${SECTIONS.map(secBlock).filter(Boolean).join('')}
  </div>`;
}

function secBlock(sec) {
  const pages = sectionPages(sec.id);
  if (!pages.length) return '';
  const pr = sectionProgress(sec.id);
  const rows = pages.map(pageRow).join('');
  return `
    <h3 class="sec-title" style="font-size:16px">${sec.icon} <a href="#/section/${sec.id}" style="color:var(--fg)">${esc(sec.label)}</a>
      <span style="font-weight:400;color:var(--fg-3);font-size:13px">· ${pr.done}/${pr.total} done</span></h3>
    <div class="page-list">${rows}</div>`;
}

function pageRow(p) {
  const done = !!getDone()[p.slug];
  const tags = (p.tags || []).slice(0, 3).map((t) => `<span class="tag">${esc(t)}</span>`).join('');
  return `
  <a class="page-row${done ? ' done' : ''}" href="#/${p.slug}">
    <span class="pr-title">${done ? '✓ ' : ''}${esc(p.nav_label)}</span>
    <span class="pr-tags">${tags}${p.priority === 'p0' ? '<span class="badge p0">P0</span>' : ''}</span>
  </a>`;
}

function viewSection(id) {
  const sec = sectionMeta(id);
  const pages = sectionPages(id);
  if (!pages.length) {
    return `<div class="content-inner"><div class="empty-state">
      <h2>${sec.icon} ${esc(sec.label)}</h2>
      <p>No pages here yet — content is being written.</p>
      <p><a class="btn" href="#/">← Back home</a></p></div></div>`;
  }
  return `<div class="content-inner">
    <div class="page-head"><h1>${sec.icon} ${esc(sec.label)}</h1>
    <div class="page-meta"><span>${pages.length} page${pages.length > 1 ? 's' : ''}</span></div></div>
    <div class="page-list">${pages.map(pageRow).join('')}</div>
  </div>`;
}

function metaLine(p) {
  const bits = [];
  bits.push(`<span>${esc(sectionMeta(p.section).label)}</span>`);
  if (p.updated) bits.push(`<span>updated ${esc(p.updated)}</span>`);
  (p.tags || []).forEach((t) => bits.push(`<span class="tag">${esc(t)}</span>`));
  if (p.company) bits.push(`<span class="tag">🏢 ${esc(p.company)}</span>`);
  if (p.priority) bits.push(`<span class="badge ${esc(p.priority)}">${esc(p.priority.toUpperCase())}</span>`);
  if (p.status) bits.push(`<span class="badge status-${esc(p.status)}">${esc(p.status)}</span>`);
  return bits.join('');
}

function sourcesBlock(p) {
  if (!p.process_sources || !p.process_sources.length) return '';
  const items = p.process_sources.map((s) => {
    const link = s.url ? `<a href="${esc(s.url)}" target="_blank" rel="noopener">[${esc(s.label)}] ${esc(s.note || s.url)}</a>`
                       : `<b>[${esc(s.label)}]</b> ${esc(s.note || '')}`;
    return `<li>${link} <span style="color:var(--fg-3)">(accessed ${esc(s.accessed || '')})</span></li>`;
  }).join('');
  return `<details class="collapse"><summary>Process sources (${p.process_sources.length})</summary>
    <div class="collapse-body"><ul>${items}</ul></div></details>`;
}

function viewPage(slug) {
  const p = BY_SLUG[slug];
  if (!p) return view404(slug);
  const done = !!getDone()[slug];
  return `<div class="content-inner">
    <div class="page-head">
      <h1>${esc(p.title)}</h1>
      <div class="page-meta">${metaLine(p)}</div>
      <div class="page-actions">
        <button class="btn${done ? ' done' : ' primary'}" id="done-toggle">${done ? '✓ Completed' : 'Mark complete'}</button>
        <a class="btn" href="#/section/${p.section}">← ${esc(sectionMeta(p.section).label)}</a>
      </div>
    </div>
    ${sourcesBlock(p)}
    <article class="prose" id="prose">${p.html}</article>
  </div>`;
}

function view404(slug) {
  return `<div class="content-inner"><div class="center-404">
    <h1>🤷 404</h1>
    <p>Nothing at <code>#/${esc(slug || '')}</code> — the page may not exist yet.</p>
    <p><a class="btn primary" href="#/">← Home</a>
       <a class="btn" href="#/questions">Question bank</a></p>
  </div></div>`;
}

/* ---------------- flashcards ---------------- */
function viewFlashcards() {
  if (!FLASHCARDS.length) {
    return `<div class="content-inner"><div class="page-head"><h1>🗂 Flashcards</h1></div>
      <div class="empty-state"><p>No flashcard decks yet — <code>data/flashcards.json</code> is empty or missing.</p>
      <p>Decks are being written; check back soon.</p></div></div>`;
  }
  const decks = [...new Set(FLASHCARDS.map((c) => c.deck || 'general'))].sort();
  const opts = ['<option value="">All decks</option>']
    .concat(decks.map((d) => `<option value="${esc(d)}">${esc(d)} (${FLASHCARDS.filter((c) => (c.deck || 'general') === d).length})</option>`))
    .join('');
  return `<div class="content-inner">
    <div class="page-head"><h1>🗂 Flashcards</h1>
      <div class="page-meta"><span>${FLASHCARDS.length} cards</span><span>click a card to flip</span></div></div>
    <div class="fc-controls">
      <select id="fc-deck" aria-label="Deck">${opts}</select>
      <button class="btn" id="fc-shuffle">🔀 Shuffle</button>
    </div>
    <div class="fc-grid" id="fc-grid"></div>
    <div class="fc-hint">Click any card to flip it.</div>
  </div>`;
}
function renderFcGrid(deck) {
  const grid = $('#fc-grid');
  if (!grid) return;
  let cards = FLASHCARDS.filter((c) => !deck || (c.deck || 'general') === deck);
  grid.innerHTML = cards.map((c) => `
    <div class="fc-card" data-id="${esc(c.id)}">
      <div class="fc-inner">
        <div class="fc-face fc-front">${esc(c.front)}<div class="fc-tags">${(c.tags || []).map((t) => `<span class="tag">${esc(t)}</span>`).join('')}</div></div>
        <div class="fc-face fc-back">${esc(c.back)}</div>
      </div>
    </div>`).join('') || '<div class="empty-state"><p>No cards in this deck.</p></div>';
  $$('.fc-card', grid).forEach((el) => el.addEventListener('click', () => el.classList.toggle('flipped')));
}
function shuffleFcGrid() {
  const grid = $('#fc-grid');
  if (!grid) return;
  const cards = $$('.fc-card', grid);
  shuffle(cards).forEach((c) => grid.appendChild(c));
}

/* ---------------- question bank ---------------- */
function uniq(arr) { return [...new Set(arr)].sort(); }

function viewQuestions() {
  if (!QUESTIONS.length) {
    return `<div class="content-inner"><div class="page-head"><h1>❓ Question Bank</h1></div>
      <div class="empty-state"><p>The question bank is empty — <code>data/questions.json</code> is missing or has no items yet.</p>
      <p>Questions are being written; check back soon.</p></div></div>`;
  }
  const companies = uniq(QUESTIONS.flatMap((q) => q.companies || []));
  const cats = uniq(QUESTIONS.map((q) => q.category).filter(Boolean));
  const diffs = uniq(QUESTIONS.map((q) => q.difficulty).filter(Boolean));
  const labels = uniq(QUESTIONS.map((q) => q.label).filter(Boolean));
  const sel = (id, opts, label) =>
    `<select id="${id}" aria-label="${label}"><option value="">${label}: all</option>` +
    opts.map((o) => `<option value="${esc(o)}">${esc(o)}</option>`).join('') + '</select>';
  return `<div class="content-inner">
    <div class="page-head"><h1>❓ Question Bank</h1>
      <div class="page-meta"><span>${QUESTIONS.length} questions</span></div></div>
    <div class="q-filters">
      ${sel('q-company', companies, 'Company')}
      ${sel('q-category', cats, 'Category')}
      ${sel('q-difficulty', diffs, 'Difficulty')}
      ${sel('q-label', labels, 'Label')}
      <input class="text-input" id="q-text" type="search" placeholder="Filter text…" aria-label="Filter text">
    </div>
    <div id="q-list"></div>
  </div>`;
}
function qCard(q) {
  const badges = [
    (q.companies || []).map((c) => `<span class="tag">🏢 ${esc(c)}</span>`).join(''),
    q.category ? `<span class="tag">${esc(q.category)}</span>` : '',
    q.difficulty ? `<span class="badge diff-${esc(q.difficulty)}">${esc(q.difficulty)}</span>` : '',
    q.time_min ? `<span class="tag">⏱ ${esc(q.time_min)} min</span>` : '',
    q.frequency ? `<span class="tag">freq: ${esc(q.frequency)}</span>` : '',
    q.label ? labelBadge(q.label) : '',
  ].filter(Boolean).join('');
  const ref = q.answer_available && q.answer_ref
    ? ` <a href="${esc(q.answer_ref)}" title="Open reference">→ reference</a>` : '';
  return `<div class="q-card" data-id="${esc(q.id)}">
    <div class="q-text">${esc(q.question)}</div>
    <div class="q-meta">${badges}${ref}</div>
  </div>`;
}
function renderQList() {
  const list = $('#q-list');
  if (!list) return;
  const f = {
    company: $('#q-company').value, category: $('#q-category').value,
    difficulty: $('#q-difficulty').value, label: $('#q-label').value,
    text: $('#q-text').value.trim(),
  };
  const items = filterQuestions(QUESTIONS, f);
  list.innerHTML = items.length
    ? `<p style="color:var(--fg-3);font-size:13px">${items.length} match${items.length > 1 ? 'es' : ''}</p>` + items.map(qCard).join('')
    : '<div class="empty-state"><p>No questions match these filters.</p></div>';
}

/* ---------------- mock interview ---------------- */
const mock = { queue: [], idx: 0, revealed: false, active: false };

function viewMock() {
  if (!QUESTIONS.length) {
    return `<div class="content-inner"><div class="page-head"><h1>🎙 Mock Interview</h1></div>
      <div class="empty-state"><p>Mock mode needs the question bank — <code>data/questions.json</code> is empty or missing.</p></div></div>`;
  }
  const companies = uniq(QUESTIONS.flatMap((q) => q.companies || []));
  const cats = uniq(QUESTIONS.map((q) => q.category).filter(Boolean));
  const diffs = uniq(QUESTIONS.map((q) => q.difficulty).filter(Boolean));
  const sel = (id, opts, label) =>
    `<label for="${id}">${label}</label><select id="${id}"><option value="">Any</option>` +
    opts.map((o) => `<option value="${esc(o)}">${esc(o)}</option>`).join('') + '</select>';
  return `<div class="content-inner">
    <div class="page-head"><h1>🎙 Mock Interview</h1>
      <div class="page-meta"><span>Timed practice, one question at a time</span></div></div>
    <div id="mock-root">
      <div class="mock-setup">
        <div class="form-row">${sel('m-company', companies, 'Company')}<span></span></div>
        <div class="form-row">${sel('m-category', cats, 'Type')}</div>
        <div class="form-row">${sel('m-difficulty', diffs, 'Difficulty')}</div>
        <div class="form-row"><label for="m-duration">Duration</label>
          <select id="m-duration"><option value="15">15 min</option><option value="30" selected>30 min</option><option value="45">45 min</option><option value="60">60 min</option></select></div>
        <div class="form-row"><span></span><button class="btn primary" id="m-start">Start session →</button></div>
      </div>
    </div>
  </div>`;
}
function mockQueue(f, minutes) {
  const pool = shuffle(filterQuestions(QUESTIONS, f));
  const queue = [];
  let used = 0;
  for (const q of pool) {
    const t = q.time_min || 30;
    if (queue.length && used + t > minutes) break;
    queue.push(q); used += t;
  }
  return queue.length ? queue : pool.slice(0, 1);
}
function startMock() {
  const f = {
    company: $('#m-company').value || undefined,
    category: $('#m-category').value || undefined,
    difficulty: $('#m-difficulty').value || undefined,
  };
  const minutes = parseInt($('#m-duration').value, 10) || 30;
  const queue = mockQueue(f, minutes);
  if (!queue.length) {
    $('#mock-root').innerHTML = `<div class="empty-state"><p>No questions match — broaden the filters.</p>
      <p><button class="btn" onclick="location.hash='#/mock'">← Back</button></p></div>`;
    return;
  }
  mock.queue = queue; mock.idx = 0; mock.revealed = false; mock.active = true;
  renderMockStage();
}
function mockBadges(q) {
  return [
    (q.companies || []).map((c) => `<span class="tag">🏢 ${esc(c)}</span>`).join(''),
    q.category ? `<span class="tag">${esc(q.category)}</span>` : '',
    q.difficulty ? `<span class="badge diff-${esc(q.difficulty)}">${esc(q.difficulty)}</span>` : '',
    q.time_min ? `<span class="tag">⏱ ${esc(q.time_min)} min</span>` : '',
    q.label ? labelBadge(q.label) : '',
  ].filter(Boolean).join('');
}
function renderMockStage() {
  const root = $('#mock-root');
  if (!root) return;
  const q = mock.queue[mock.idx];
  const rubric = q.rubric
    ? `<div class="mock-rubric"><b>Rubric</b><div class="answer-body">${
        Array.isArray(q.rubric) ? '<ul>' + q.rubric.map((r) => `<li>${esc(r)}</li>`).join('') + '</ul>' : esc(q.rubric)
      }</div></div>` : '';
  const ref = q.answer_available && q.answer_ref
    ? `<p><a href="${esc(q.answer_ref)}">→ Open reference material</a></p>` : '';
  root.innerHTML = `
  <div class="mock-stage">
    <div class="mock-progress">Question ${mock.idx + 1} of ${mock.queue.length} · ${esc(q.id || '')}</div>
    <div class="mock-q">${esc(q.question)}</div>
    <div class="mock-meta">${mockBadges(q)}</div>
    <div class="mock-answer">
      <button class="btn" id="m-reveal">${mock.revealed ? 'Hide answer' : 'Reveal answer / rubric'}</button>
      <div id="m-answer" ${mock.revealed ? '' : 'hidden'}>
        ${rubric}${ref}
        ${!rubric && !ref ? '<div class="answer-body">No written answer — talk through it out loud, then check the reference.</div>' : ''}
      </div>
    </div>
    <div class="mock-nav">
      <button class="btn" id="m-prev" ${mock.idx === 0 ? 'disabled' : ''}>← Prev</button>
      ${mock.idx < mock.queue.length - 1
        ? '<button class="btn primary" id="m-next">Next →</button>'
        : '<button class="btn primary" id="m-finish">Finish session</button>'}
      <button class="btn" id="m-quit">End</button>
    </div>
  </div>`;
  $('#m-reveal').addEventListener('click', () => {
    mock.revealed = !mock.revealed; renderMockStage();
  });
  const prev = $('#m-prev'); if (prev) prev.addEventListener('click', () => { mock.idx--; mock.revealed = false; renderMockStage(); });
  const next = $('#m-next'); if (next) next.addEventListener('click', () => { mock.idx++; mock.revealed = false; renderMockStage(); });
  const fin = $('#m-finish'); if (fin) fin.addEventListener('click', finishMock);
  $('#m-quit').addEventListener('click', finishMock);
  enhanceMath($('#m-answer'));
}
function finishMock() {
  mock.active = false;
  const root = $('#mock-root');
  if (root) root.innerHTML = `<div class="empty-state">
    <h3>Session complete — ${mock.queue.length} question${mock.queue.length > 1 ? 's' : ''} attempted.</h3>
    <p>Debrief: what was crisp, where did you ramble, what would you tighten?</p>
    <p><button class="btn primary" id="m-again">New session</button>
       <a class="btn" href="#/questions">Browse bank</a></p></div>`;
  const again = $('#m-again');
  if (again) again.addEventListener('click', () => { location.hash = '#/mock'; render(); });
}

/* ============================ CHROME ============================ */

function buildNav() {
  const nav = $('#nav');
  if (!nav) return;
  const done = getDone();
  let html = `<div class="nav-special" style="border:none;margin-top:0;padding-top:0">
      <a class="nav-link" data-route="home" href="#/">🏠 Home</a></div>`;
  html += `<div class="nav-sec"><div class="nav-sec-head">Practice</div>
      <a class="nav-link" data-route="mock" href="#/mock">🎙 Mock interview</a>
      <a class="nav-link" data-route="questions" href="#/questions">❓ Question bank</a>
      <a class="nav-link" data-route="flashcards" href="#/flashcards">🗂 Flashcards</a></div>`;
  for (const sec of SECTIONS) {
    const pages = sectionPages(sec.id);
    if (!pages.length) continue;
    html += `<div class="nav-sec"><a class="nav-sec-head" href="#/section/${sec.id}">${sec.icon} ${esc(sec.label)}</a>`;
    for (const p of pages) {
      html += `<a class="nav-link" data-slug="${p.slug}" href="#/${p.slug}">${esc(p.nav_label)}${done[p.slug] ? '<span class="done-dot">✓</span>' : ''}</a>`;
    }
    html += '</div>';
  }
  nav.innerHTML = html;
  $$('#nav a', document).forEach((a) => a.addEventListener('click', closeMobileNav));
}

function setActiveNav(route) {
  $$('#nav .nav-link').forEach((a) => a.classList.remove('active'));
  let sel = null;
  if (route.view === 'home') sel = '[data-route="home"]';
  else if (['mock', 'questions', 'flashcards'].includes(route.view)) sel = `[data-route="${route.view}"]`;
  else if (route.view === 'page') sel = `[data-slug="${route.slug}"]`;
  if (sel) { const el = $(sel, $('#nav')); if (el) el.classList.add('active'); }
}

function closeMobileNav() {
  document.body.classList.remove('nav-open');
  const t = $('#nav-toggle'); if (t) t.setAttribute('aria-expanded', 'false');
  const scrim = $('#sidenav-scrim'); if (scrim) scrim.hidden = true;
}

/* ---------------- theme ---------------- */
function currentTheme() {
  return document.documentElement.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
}
function applyTheme(t) {
  document.documentElement.setAttribute('data-theme', t);
  LS.set(LS_THEME, t);
  const btn = $('#theme-toggle');
  if (btn) btn.textContent = t === 'light' ? '☾' : '◐';
}

/* ---------------- search UI ---------------- */
let searchActive = -1;
function onSearchInput() {
  const box = $('#search'), panel = $('#search-results');
  const q = box.value.trim();
  if (q.length < 2 || !SEARCH_READY) { panel.hidden = true; panel.innerHTML = ''; return; }
  const results = rankSearch(q, SEARCH);
  searchActive = -1;
  panel.innerHTML = results.length ? results.map((r, i) => `
    <a class="sr-item" data-i="${i}" href="#/${r.rec.slug}">
      <div class="sr-title">${esc(r.rec.title)}</div>
      <div class="sr-meta">${esc(sectionMeta(r.rec.section).label)}${r.rec.headings.length ? ' · ' + esc(r.rec.headings[0]) : ''}</div>
      ${r.snippet ? `<div class="sr-snip">${esc(r.snippet)}…</div>` : ''}
    </a>`).join('')
    : '<div class="sr-empty">No matches. Try fewer words.</div>';
  panel.hidden = false;
}
function searchKeydown(e) {
  const panel = $('#search-results');
  if (panel.hidden) return;
  const items = $$('.sr-item', panel);
  if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
    e.preventDefault();
    searchActive = e.key === 'ArrowDown'
      ? Math.min(items.length - 1, searchActive + 1)
      : Math.max(0, searchActive - 1);
    items.forEach((el, i) => el.classList.toggle('active', i === searchActive));
    if (items[searchActive]) items[searchActive].scrollIntoView({ block: 'nearest' });
  } else if (e.key === 'Enter' && searchActive >= 0 && items[searchActive]) {
    items[searchActive].click();
  } else if (e.key === 'Escape') {
    panel.hidden = true; $('#search').blur();
  }
}

/* ---------------- post-render enhance ---------------- */
function enhanceCode(app) {
  if (!window.hljs) return;
  $$('pre code', app).forEach((el) => {
    if (el.classList.contains('hljs')) return;
    try { hljs.highlightElement(el); } catch (e) {}
  });
}
function enhanceMath(app) {
  if (!app || !window.renderMathInElement) return;
  try {
    renderMathInElement(app, {
      delimiters: [
        { left: '$$', right: '$$', display: true },
        { left: '$', right: '$', display: false },
      ],
      throwOnError: false,
    });
  } catch (e) {}
}
function enhanceMermaid(app) {
  if (!app || !window.mermaid) return;
  try {
    mermaid.initialize({ startOnLoad: false, theme: currentTheme() === 'dark' ? 'dark' : 'default', securityLevel: 'loose' });
    const nodes = $$('.mermaid', app).filter((n) => !n.hasAttribute('data-processed'));
    if (nodes.length) mermaid.run({ nodes });
  } catch (e) {}
}
function restoreTasks(app, slug) {
  const saved = LS.get(taskKey(slug), {});
  $$('input.task-cb', app).forEach((cb) => {
    const id = cb.getAttribute('data-task');
    if (saved[id]) cb.checked = true;
    paintTaskLi(cb);
    cb.addEventListener('change', () => {
      const s = LS.get(taskKey(slug), {});
      if (cb.checked) s[id] = true; else delete s[id];
      LS.set(taskKey(slug), s);
      paintTaskLi(cb);
    });
  });
}
function paintTaskLi(cb) {
  const li = cb.closest('li');
  if (li) li.classList.toggle('task-done', cb.checked);
}
function buildTOC(app) {
  const toc = $('#toc');
  const side = $('#tocside');
  if (!toc) return;
  const heads = $$('#prose h2[id], #prose h3[id]', app);
  if (!heads.length) { toc.innerHTML = ''; if (side) side.style.display = 'none'; return; }
  if (side) side.style.display = '';
  toc.innerHTML = '<div class="toc-title">On this page</div>' + heads.map((h) =>
    `<a href="javascript:void(0)" data-anchor="${h.id}" class="${h.tagName.toLowerCase()}">${esc(h.textContent)}</a>`
  ).join('');
  $$('#toc a', toc).forEach((a) => a.addEventListener('click', (e) => {
    e.preventDefault();
    const t = document.getElementById(a.getAttribute('data-anchor'));
    if (t) t.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }));
  // scroll spy
  const links = $$('#toc a', toc);
  const map = {};
  heads.forEach((h) => { map[h.id] = links.find((a) => a.getAttribute('data-anchor') === h.id); });
  if ('IntersectionObserver' in window) {
    const obs = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) {
          links.forEach((l) => l.classList.remove('active'));
          const l = map[en.target.id];
          if (l) l.classList.add('active');
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    heads.forEach((h) => obs.observe(h));
  }
}

/* ---------------- render ---------------- */
function render() {
  closeMobileNav();
  const app = $('#app');
  const route = parseRoute(location.hash);
  setActiveNav(route);
  const box = $('#search'); if (box && document.activeElement !== box) { /* keep query */ }
  $('#search-results').hidden = true;

  let html;
  if (route.view === 'home') html = viewHome();
  else if (route.view === 'section') html = viewSection(route.section);
  else if (route.view === 'flashcards') html = viewFlashcards();
  else if (route.view === 'mock') html = viewMock();
  else if (route.view === 'questions') html = viewQuestions();
  else if (route.view === 'page') html = viewPage(route.slug);
  else html = view404(route.raw);

  app.innerHTML = html;
  document.title = route.view === 'page' && BY_SLUG[route.slug]
    ? `${BY_SLUG[route.slug].title} · ML Interview Prep` : 'ML Interview Prep';
  window.scrollTo(0, 0);

  // wire view-specific controls
  if (route.view === 'page' && BY_SLUG[route.slug]) {
    const btn = $('#done-toggle');
    if (btn) btn.addEventListener('click', () => {
      const slug = route.slug;
      const nowDone = !getDone()[slug];
      setDone(slug, nowDone);
      btn.classList.toggle('done', nowDone);
      btn.classList.toggle('primary', !nowDone);
      btn.textContent = nowDone ? '✓ Completed' : 'Mark complete';
      buildNav(); setActiveNav(route);
    });
    restoreTasks(app, route.slug);
  }
  if (route.view === 'flashcards') {
    renderFcGrid('');
    const deckSel = $('#fc-deck'), shufBtn = $('#fc-shuffle');
    if (deckSel) deckSel.addEventListener('change', (e) => renderFcGrid(e.target.value));
    if (shufBtn) shufBtn.addEventListener('click', shuffleFcGrid);
  }
  if (route.view === 'mock') {
    const start = $('#m-start');
    if (start) start.addEventListener('click', startMock);
  }
  if (route.view === 'questions') {
    renderQList();
    ['q-company', 'q-category', 'q-difficulty', 'q-label'].forEach((id) => {
      const el = $('#' + id);
      if (el) el.addEventListener('change', renderQList);
    });
    const qt = $('#q-text');
    if (qt) qt.addEventListener('input', renderQList);
  }

  buildTOC(app);
  enhanceCode(app);
  enhanceMath(app);
  enhanceMermaid(app);
  app.focus({ preventScroll: true });
}

/* ---------------- data ---------------- */
async function fetchJson(url) {
  try {
    const r = await fetch(url);
    if (!r.ok) return null;
    return await r.json();
  } catch (e) { return null; }
}

async function boot() {
  // theme (inline head script already set data-theme; sync toggle icon)
  const t = document.documentElement.getAttribute('data-theme') || 'dark';
  applyTheme(t === 'light' ? 'light' : 'dark');

  $('#theme-toggle').addEventListener('click', () =>
    applyTheme(currentTheme() === 'light' ? 'dark' : 'light'));
  const navToggle = $('#nav-toggle');
  navToggle.addEventListener('click', () => {
    const open = document.body.classList.toggle('nav-open');
    navToggle.setAttribute('aria-expanded', String(open));
    $('#sidenav-scrim').hidden = !open;
  });
  $('#sidenav-scrim').addEventListener('click', closeMobileNav);

  const box = $('#search');
  box.addEventListener('input', onSearchInput);
  box.addEventListener('keydown', searchKeydown);
  box.addEventListener('focus', onSearchInput);
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-wrap')) $('#search-results').hidden = true;
  });
  document.addEventListener('keydown', (e) => {
    const tag = (document.activeElement || {}).tagName;
    if (e.key === '/' && tag !== 'INPUT' && tag !== 'TEXTAREA' && !e.metaKey && !e.ctrlKey) {
      e.preventDefault(); box.focus();
    }
  });

  $('#app').innerHTML = '<div class="content-inner"><p style="color:var(--fg-3)">Loading…</p></div>';

  const [content, search, questions, flashcards] = await Promise.all([
    fetchJson('data/content.json'),
    fetchJson('data/search.json'),
    fetchJson('data/questions.json'),
    fetchJson('data/flashcards.json'),
  ]);

  if (!content || !content.pages) {
    $('#app').innerHTML = `<div class="content-inner"><div class="empty-state">
      <h2>Couldn't load content</h2><p><code>data/content.json</code> is missing — run <code>python3 build.py</code>.</p></div></div>`;
    return;
  }
  META = content.meta || META;
  PAGES = content.pages || [];
  BY_SLUG = {};
  PAGES.forEach((p) => { BY_SLUG[p.slug] = p; });
  SECTIONS = (META.sections || []).concat(
    [...new Set(PAGES.map((p) => p.section))]
      .filter((id) => !(META.sections || []).some((s) => s.id === id))
      .map((id) => ({ id, label: id.replace(/-/g, ' '), icon: '📄' }))
  );
  SEARCH = search || [];
  SEARCH_READY = true;
  QUESTIONS = Array.isArray(questions) ? questions : [];
  FLASHCARDS = Array.isArray(flashcards) ? flashcards : [];

  const built = $('#built-at');
  if (built) built.textContent = `${PAGES.length} pages`;

  buildNav();
  window.addEventListener('hashchange', render);
  render();
}

/* node test exports (browser ignores) */
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { parseRoute, rankSearch, filterQuestions, tokenize, esc, shuffle, view404 };
}
if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
}
