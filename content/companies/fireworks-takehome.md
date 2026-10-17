---
title: "Fireworks AI — Take-Home Code Walkthrough Prep"
slug: "fireworks-takehome"
section: "companies"
nav_order: 141
nav_label: "Fireworks Take-Home Walk"
tags: ["fireworks", "take-home", "rag", "agents", "deep-dive", "interviewing"]
updated: "2026-10-17"
company: "Fireworks AI"
priority: "p0"
status: "interviewing"
process_sources:
  - { label: "INFERRED", url: "", accessed: "2026-10-17", note: "Next round walks the submitted take-home code (per Rui 2026-10-17); prep built from a full read of the actual submission code in the private take-home-assignment repo, commit a9018fe" }
---

## TL;DR

Your take-home is **done and in the private repo** (`take-home-assignment/fireworks-ai/`, commit `a9018fe`, pushed 2026-10-17 by Claude). Next round walks this code — this page is the walk script.

- **What it is:** a local agentic RAG system ("10-K Analyst") over Apple / Microsoft / Alphabet financials. An LLM planner routes each question to a **SQL tool** (structured financials in SQLite), a **PDF tool** (hybrid search over the six 10-Ks), or both, then a separate synthesis step writes a grounded, cited answer.
- **Scoreboard to quote:** **8/10 correct, 10/10 routing** on the public dev set (your own eval harness, the key's own three scoring methods). The two misses are q_006 and q_025 — both multi-part narrative questions. Know them cold (section below).
- **Stack in one breath:** Python + FastAPI, Fireworks `gpt-oss-120b` for planner / text-to-SQL / synthesis / judge, `nomic-embed-text-v1.5` (768-d) for embeddings, 1,754 chunks in a local numpy store + BM25, no vector DB.
- **The three design choices you will be graded on:** (1) portable JSON-action planner loop instead of provider function-calling, (2) final answer composed in a *separate* synthesis call over collected evidence, (3) hybrid dense+BM25 retrieval with company/year metadata filtering.

:::tldr
Before the walkthrough round, fix the submission package first (next section) — two README-vs-code mismatches are exactly the kind of thing a code walk surfaces. Then rehearse the 5-minute walk and the two misses.
:::

## Fix before you submit (zip is due Tue Oct 20)

The code is coherent; the *package* has traps. Fix these before zipping for Ashby:

- **SUBMISSION_README.md is stale on two defaults.** It says `FW_MODEL` defaults to `llama-v3p3-70b-instruct` and `FW_TOP_K` defaults to 6. The actual code (`app/config.py`) defaults to **`gpt-oss-120b`** and **`TOP_K = 8`**. If an interviewer opens the README and then config.py, you look sloppy. Fix the README, not the code — the results were produced with gpt-oss-120b / top-k 8.
- **Two READMEs problem.** The folder still contains the *assignment's* original README (161 lines) alongside `SUBMISSION_README.md` and `REPORT.md`. In the submission zip, your README must be the one with run instructions — rename/replace so a reviewer cannot pick the wrong one.
- **The API key file was deleted from HEAD — on purpose, but know where your key lives now.** Commit `a9018fe` removed `FIREWORKS_API_KEY.txt` from tracking and added it to `.gitignore` (good hygiene for a submission). The key still exists in git history (commit `1d5ec87`) and in the Fireworks console. For your live demo you need it as an env var: `export FIREWORKS_API_KEY=...` — retrieve it *before* the interview, not during.
- **`data/index/` is not in the repo** (gitignored, derived artifact). A fresh clone cannot answer PDF questions until `python -m app.ingest` runs (needs the key, embeds 1,754 chunks once). For the demo, build the index the night before and verify `/health` shows `index_present: true`.
- **There are no unit tests.** The only verification is `app/evaluate.py` over the 10 dev questions. If asked "how did you test this?", do not invent tests — say the eval harness *is* the test surface (numeric / entity / judge scoring + routing check per question), and name what you would add first (golden SQL validation cases + retrieval recall checks). See Q&A below.
- **Claude wrote a `CODE_WALKTHROUGH.md` inside the repo** — it is a good skeleton (and this page follows the same map), but it glosses over the weaknesses in the "Honest weaknesses" section below. Interviewers will find those; you want to say them first.

## The 30-second pitch (memorize this)

> "It's an agentic RAG system over three companies' financials. An LLM planner decides, per question, whether to hit a SQL tool for structured financials, a PDF tool for 10-K narrative, or both, and it can chain steps. A separate synthesis step writes a grounded answer that cites the exact SQL it ran and the 10-K pages it used. It runs as an HTTP API, a web UI, and a CLI, with an evaluation harness that scores against the public dev set. Everything is local; only model calls go to Fireworks."

Why this pitch works: it names routing (the graded skill), grounding/citations (the trust story), and the local-only-except-inference boundary (the AMLE customer story) in four sentences.

## The 5-minute walk (order to present in)

Walk in request order, not file-alphabetical order. Open each file as you name it.

- **Stop 1 — `app/server.py` (entry, 70 lines).** "POST /api/chat takes {question}, returns {answer, content, evidence, modalities}. Both `answer` and `content` are returned for contract compatibility. There's a /health endpoint and the UI is served from the same process." Have the UI open; ask one question live if the setup is warm.
- **Stop 2 — `app/agent.py` (the brain, 135 lines).** "This is the planner loop. Each turn the model returns ONE small JSON action — sql, pdf, or final. Tool results come back as Observations. Budget is 5 steps (`MAX_AGENT_STEPS`). When it says final, a separate `_synthesize()` call composes the answer from the evidence list only."
- **Stop 3 — `app/tools/sql_tool.py` (103 lines).** "Schema-aware text-to-SQL. The live schema is read from sqlite_master and injected into the prompt with domain facts — tickers, fiscal-year ends, segment and region names. Safety story: read-only connection (`mode=ro`), single-statement SELECT/WITH validation, write/DDL keywords rejected, and the executed SQL is returned as evidence so every number is traceable. One retry that re-prompts with the SQLite error."
- **Stop 4 — `app/ingest.py` + `app/tools/pdf_tool.py` (the retrieval).** "Ingest: PyMuPDF extracts per page, chunks at 1,400 chars with 200 overlap, each chunk tagged company / year / page / section, embedded once into a local store — 1,754 chunks. Search: hybrid — dense cosine plus BM25, each min-max normalized, combined 50/50, with metadata filtering by company and year parsed from the question. BM25 alone is the fallback if embeddings are unavailable."
- **Stop 5 — `app/evaluate.py` (proof, 131 lines).** "The brief shipped no evaluator, so this is mine. It runs all 10 dev questions, writes dev_answers.json, scores with the key's own three methods, and separately checks routing — did the agent use at least the required modalities. Result: 8/10 correct, 10/10 routing. The two misses are both multi-part narrative questions, and I can show you exactly why each failed." (This line invites the deep-dive on your terms.)
- **Close — `REPORT.md`.** "Trade-offs and what I'd do with more time are written up: section-aware retrieval, a reranker, deeper multi-part planning, real streaming, confidence/abstention."

## Numbers you must not fumble

- Chunks: **1,754** · chunk size **1,400 chars**, overlap **200** (character-based, per PDF page) · min chunk kept: 60 chars
- Retrieval: **top-k 8** (`FW_TOP_K`) · hybrid weight **50/50** after min-max normalization
- Agent: **max 5 planner steps** · planner JSON capped at 400 tokens per turn · synthesis capped at 900 tokens, evidence JSON truncated at **9,000 chars** (know this — it matters for q_025)
- SQL: row fetch limit **200** · one error-driven retry · DB has 5 tables, 3 companies x 3 fiscal years (2023–2025)
- PDFs: **only FY2024 + FY2025** 10-Ks (6 files). SQL has FY2023 data; there is **no FY2023 narrative** — do not claim otherwise
- Models: planner/SQL/synthesis/judge all `gpt-oss-120b` by default (judge overridable via `FW_JUDGE_MODEL`) · embeddings `nomic-embed-text-v1.5`, 768-d, ingested in batches of 64
- LLM client: temperature 0 · chat retries 3x with linear backoff (1.5s, 3s) · `chat_json` retries once with more tokens plus a "short valid JSON only" nudge, then brace-extraction
- Eval: accuracy **8/10 = 0.80** · routing **10/10 = 1.00** (superset definition — see trap below)
- Cost per question (estimate, say it as an estimate): roughly 4–8 model calls — one planner call per step, one extra LLM call per SQL tool use (text-to-SQL generation), one embedding call per PDF search, one synthesis call. Latency is dominated by these serial calls, not by retrieval (numpy cosine over 1,754 vectors is effectively instant)

## The 10 dev questions — what happened on each

| Q | Tier / route required | What the system did | Result | If probed, say |
|---|---|---|---|---|
| q_001 Apple FY2025 revenue | T1 · SQL | One SQL call, revenue = 416,161,000,000 | Correct (fuzzy numeric exact) | "The trivial case — the point is it did NOT waste a PDF search." |
| q_006 Apple supply-chain risk factors | T1 · PDF | One PDF search, top-8 chunks leaned trade/tariff + disruption passages | **MISS** — under-weighted single/limited-source components and third-party-manufacturer dependence, which the gold answer leads with | Root-cause section below. This is your most important rehearsed answer. |
| q_008 MSFT US revenue share FY2025 | T1 · SQL | SQL over geographic_revenue, 51.3% | Correct | "Ratio pushed into SQL; synthesis just reports it." |
| q_011 Fastest revenue growth, two most recent FYs | T2 · SQL | SQL across all three, GOOGL about 15.1% | Correct (entity) | Note the scorer only checks the entity — your answer also carried the rate. |
| q_012 Greater China change + does the 10-K explain why | T2 · SQL+PDF | SQL: 66.95B to 64.38B, −3.8%; PDF: lower iPhone, partly offset by Mac | Correct (judge) | **Your best demo question** — shows true multi-modal chaining and citation. |
| q_014 MSFT segment definitions + revenue each | T2 · SQL+PDF | PDF for the three definitions, SQL for 120.8B / 106.3B / 54.6B | Correct (judge) | "Definitions live in narrative, numbers live in the DB — neither tool alone answers it." |
| q_017 Google Services components + YouTube ads change | T2 · PDF (required) | Used **PDF + SQL** (extra modality), YouTube 36.1B to 40.4B, +11.7% | Correct (judge) | If asked why SQL on a PDF-required question: the planner over-fetched; it helped cross-check segment totals but cost an extra call. Honest, and it tees up the routing-definition trap below. |
| q_018 Highest current ratio, most recent FY | T2 · SQL | SQL ratio across companies, GOOGL about 2.01x | Correct (entity) | Same entity-scorer note as q_011. |
| q_022 Largest absolute revenue increase + segment breakdown | T3 · SQL | One SQL path: GOOGL +52.8B total; Services +37.8B, Cloud +15.5B, Other Bets −0.1B | Correct (judge) | The hardest pure-SQL question — segment_revenue components plus the hedging line explain why segments do not sum exactly to the total. |
| q_025 Apple Services growth 2 years vs iPhone + strategic importance | T3 · SQL+PDF | Got FY23→24 Services growth (12.9%) but answer truncated the second year and the strategic-importance narrative | **MISS** | Root-cause section below. |

## The two misses — root cause, mapped to real code

Do not say "the model got it wrong." Both misses have mechanical causes you can point at in the code. That is the senior-level answer.

### q_006 — enumeration question, retrieval breadth failure

- The question asks to **enumerate** risk factors. The system made **one** PDF call with **top-k 8**, and `format_evidence()` truncates **each chunk to 600 chars** before synthesis. Adjacent risks (trade/tariffs, disruption events) crowded out the specific component-sourcing passages.
- Section tagging in `ingest.py` is a regex heuristic (`SECTION_RE`) carried forward page by page — chunks *know* their section, but `pdf_search()` **never boosts by section**. An Item 1A question gets no Item 1A preference.
- Fix to propose (in order): section-aware boost for enumeration/risk questions + larger top-k for those, then a reranker over a wider candidate pool, then a synthesis prompt that enumerates exhaustively (the prompt already asks for comprehensive enumeration — retrieval, not synthesis, was the bottleneck; the judge's feedback proves it: the missing factors never reached the prompt).

### q_025 — multi-part question, planning + context-budget failure

- The question has **three sub-goals**: Services growth for *each of two years*, iPhone growth for the same years, and the narrative on strategic importance. The planner never decomposes it into an explicit checklist, so nothing verifies coverage before `final`.
- Hard budget interaction: **5 planner steps max**, and `_synthesize()` truncates the whole evidence JSON at **9,000 chars**. With several SQL results plus 8 PDF chunks at 600 chars each, later evidence can be cut before synthesis ever sees it.
- Fix to propose: planner emits sub-goals up front and checks them off before finalizing; raise/restructure the evidence budget (summarize per-tool evidence instead of one flat truncation); split synthesis per sub-goal for multi-part questions.

### The sentence that ties both together

> "Both misses are the same lesson: single-shot retrieval and a flat context budget are fine for lookup questions and break on breadth questions — enumeration and multi-part. The fixes are retrieval breadth for the first and explicit sub-goal planning for the second, not prompt-tuning to these two questions, which would just overfit the public set before a hidden set."

That last clause matters: the REPORT already states you deliberately did not hand-tune to the two misses because grading uses a hidden set. Be ready to defend that choice — it is a strength, and interviewers from Fireworks' "judge the code quality" school will probe it.

## Honest weaknesses (say them before they find them)

- **SSE is an envelope, not streaming.** `server.py` runs `agent.answer()` to completion, *then* yields one `answer` event. It satisfies the alternate contract shape; it is not token streaming. The report lists real streaming as future work — keep the story consistent.
- **The FastAPI handler blocks.** `chat()` is `async def` but calls the synchronous agent directly, so one slow question blocks the event loop. Fine for a local POC; in production you'd run it in a threadpool or make the pipeline async. Say this unprompted if server code is on screen.
- **`ALLOWED_TABLES` is defined but never enforced.** `sql_tool.py` declares the table allowlist, but `_validate()` only checks single-statement + SELECT/WITH + forbidden keywords (plus the read-only connection underneath). The defense-in-depth claim is "read-only URI is the hard boundary; validation is the soft one" — and wiring the allowlist into validation is a one-function fix you can describe precisely.
- **Routing accuracy is a superset metric.** `evaluate.py` counts routing correct when used modalities *include* the required ones (q_017 used an extra SQL call and still counts). "10/10 routing" means "never missed a required modality," not "always minimal." If they read evaluate.py, they will see this — say it first.
- **The judge grades its own family.** Judge defaults to the same `gpt-oss-120b` as the generator (`FW_JUDGE_MODEL` defaults to `FW_MODEL`). Self-preference bias is real; mitigations you can name: the two non-judge methods (numeric/entity) are deterministic, the judge prompt is gold-anchored, and a different judge model is a one-env-var change.
- **Min-max normalization is pool-relative.** Hybrid scores are normalized within the *filtered candidate pool*, so the same chunk can score differently depending on the filter. Fine for top-k ranking inside one query; not a calibrated relevance score. If pushed, this is where a reranker or RRF (reciprocal rank fusion) replaces the hand-rolled 50/50.
- **Chunking is character-based and page-bound.** Tables split mid-row, a chunk never crosses a page boundary, and the cited page is the **PDF page number** (PyMuPDF page index + 1), not the printed folio number on the page. Citations are verifiable in the PDF file, which is the honest framing.
- **Embeddings have no retry.** `llm.chat` retries with backoff; `llm.embed` does not — a transient failure during ingest kills the build. One-line fix, name it if ingest is on screen.
- **No observability beyond prints.** `verbose` prints plans; there are no traces, token/cost accounting, or latency metrics. For an AMLE story this is the biggest production gap — see the scale-up answer.
- **Unused dependencies.** `requirements.txt` includes pandas and requests, which the app code does not import (left over from the starter). Harmless, but if they ask, own it: "starter residue, would prune."

## Likely questions — and your answers

**Why a JSON-action loop instead of native function-calling?**
Portability and debuggability. Any Fireworks chat model can emit small JSON; the control flow is inspectable in logs, and I'm not coupled to one provider's tool-call dialect — which matters because the whole premise is running *open* models on Fireworks. Cost: a few extra tokens and my own parsing/validation burden (`chat_json` hardening exists precisely because of that).

**Why is synthesis a separate call?**
Two reasons, one learned the hard way: a long answer inside the planner's JSON field truncated mid-string and broke parsing. And separation is a grounding boundary — the synthesizer sees *only* the evidence list, so its job is composition and arithmetic over cited facts, not recall.

**Why hybrid retrieval? Why 50/50?**
Dense misses exact tokens — segment names like "Intelligent Cloud", regions like "Greater China". BM25 misses paraphrase. 50/50 after normalization is a robust default, not a tuned optimum; with a labeled set I'd tune the weight or move to RRF + a reranker, which is improvement #2 in the report (`qwen3-reranker-8b` is already available on the account).

**Why no vector database?**
1,754 vectors. Brute-force numpy cosine is effectively instant and has zero ops cost. A vector DB earns its keep around 100k+ chunks or when you need concurrent writers/filtering at scale. Choosing *not* to add infrastructure is a trade-off I'm making deliberately, with a stated break point.

**How do you prevent hallucination?**
Layered, and honestly bounded: synthesis is instructed to use only the evidence; SQL answers carry the executed query and rows; PDF answers carry page citations; the API/UI expose the evidence trail so a human can verify in one click. What it does *not* have: a post-hoc verifier that checks every claim against the evidence — that's the confidence/abstention item in the report. Don't overclaim.

**Text-to-SQL is dangerous. Defend it.**
The hard boundary is the database opened read-only (`mode=ro`) — even a bad query cannot write. Above that: single-statement validation, SELECT/WITH only, write/DDL keywords rejected, 200-row fetch cap. The error retry re-prompts with the SQLite error once, then surfaces failure rather than looping. Residual risks to name yourself: a valid-but-expensive query (no timeout today), and the unused ALLOWED_TABLES allowlist (see weaknesses).

**How did you evaluate, and why should I trust it?**
I built the harness because the brief intentionally shipped none. Three scorers mirror the public key's own methods: fuzzy numeric (extract numbers, handle $/billions/%, 2% tolerance, percent-as-fraction allowed), exact entity, and a gold-anchored LLM judge. Plus routing coverage per question. I trust it as a *development signal* — 10 questions is small, the judge shares a model family with the generator, and the real grade is a hidden set, which is exactly why I fixed general weaknesses instead of overfitting the two public misses.

**Why gpt-oss-120b? Why nomic embeddings?**
gpt-oss-120b gave reliable JSON planning and strong finance reasoning at open-model cost on Fireworks — the AMLE customer story in miniature: a capable open model on Fireworks instead of a closed API. Both are config-swappable by env var, and the judge model is separately overridable. Nomic v1.5: 768-d, cheap, solid on English financial prose.

**What breaks first at real scale?**
In order: (1) the flat 9,000-char evidence truncation and 5-step budget on breadth questions; (2) brute-force cosine past ~100k chunks; (3) the blocking server handler under concurrency; (4) no caching — repeated questions re-pay full planner+tool cost. Each has a named fix in the report.

**A customer wants this over their private filings, multi-tenant. What changes?**
This is the AMLE pivot — connect it to Fireworks' private-data thesis. Per-tenant index isolation or ACL metadata filtering at retrieval time (filter *before* top-k, never post-filter), document-level permissions enforced in the tool layer not the prompt, re-ingest pipeline for filing updates, per-tenant eval sets, and token/cost observability per request. The agent core — planner, tools, grounded synthesis — carries over unchanged; the trust boundary moves into retrieval.

**How did you use AI assistance? (They will ask — the report discloses Claude.)**
Answer exactly as the report does, in first person: an AI coding assistant helped scaffold and iterate; you directed the architecture, routing and evaluation design, and model/trade-off decisions, and reviewed and tested all code. Then prove it: this whole page exists so every mechanism above is explainable by *you*, unprompted, with the file open. Fireworks' own 2026 interview rethink (judging code quality, steering agents) means "I steered, I verified, here is what I changed my mind on" is the strongest possible framing — have one concrete example ready: the separate-synthesis decision came from a real truncation failure during development.

**What would you do with one more week?**
The report's five, in order: section-aware retrieval for enumeration questions; a reranker over hybrid candidates; sub-goal planning with coverage checks for multi-part questions; token-level SSE streaming + response caching; confidence scoring with abstention when evidence is thin. Then the production layer: async server, timeouts on SQL, embed retries, traces with per-step cost.

## Live demo script (rehearse once, end to end)

Run the night before: pull the repo, set `FIREWORKS_API_KEY`, `python -m app.ingest` (index must exist), start `python -m app.server`, check `/health`.

- **Demo 1 (SQL only):** "What was Apple's total net revenue in fiscal year 2025?" — show the generated SQL in the evidence panel. Point: routing restraint + traceable number.
- **Demo 2 (SQL+PDF, the money demo):** q_012 Greater China. Show both evidence types side by side and the page citation. Point: multi-modal chaining.
- **Demo 3 (honesty demo, optional but powerful):** q_006 supply-chain risks. Show the answer, then say what it under-weights and why (top-k breadth + no section boost). Volunteering a known failure with a mechanism and a fix is the strongest signal in a code walk.
- **Fallback:** if the network or API fails live, `dev_answers.json` + `eval_report.json` are in the repo — walk the stored answers and the evidence shape instead. Never debug credentials on camera.

## 30-minute checklist (before the round)

- [ ] Repo pulled at `a9018fe`; you can open every file in the walk order without searching
- [ ] SUBMISSION_README mismatches fixed in your head at minimum: model = gpt-oss-120b, top-k = 8 (fix the file too if the zip is not yet sent)
- [ ] API key exported, index built, server starts, /health green, one live question answered
- [ ] 30-second pitch said out loud once; 5-minute walk timed once
- [ ] q_006 and q_025 root causes rehearsed with file + function names (pdf_search top-k / format_evidence 600-char cap; _synthesize 9,000-char cap / MAX_AGENT_STEPS 5)
- [ ] The five honest weaknesses you will volunteer: SSE envelope, blocking handler, unused ALLOWED_TABLES, superset routing metric, same-family judge
- [ ] One "what I'd do with a week" answer and one AMLE customer-scale answer ready
- [ ] AI-assistance answer rehearsed in first person, consistent with REPORT.md's disclosure

## Related

- Company page: [Fireworks AI](#/fireworks-ai) — process, system-design domains, company background
- Submission source: private repo `huangrui19910206/take-home-assignment`, folder `fireworks-ai/` (REPORT.md, SUBMISSION_README.md, CODE_WALKTHROUGH.md, eval_report.json)
- Assignment details: due Tue Oct 20, 2026 via Ashby zip — no GitHub link in the submission, repo stays private
