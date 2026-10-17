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

## 人话版 — 先看这个 (Claude 那份看不懂很正常)

Claude 写的 `CODE_WALKTHROUGH.md` 是给"已经懂这个系统的人"看的提纲:全是表格和术语,没有讲**这东西到底在干嘛**。下面用人话讲一遍。先读这一节,懂了整个故事,后面的英文问答就是照着说而已。

### 一句话:这是一个"会自己查资料的研究员"

想象你雇了一个研究员,桌上有两样东西:

- **一本账本** — 三家公司 (苹果/微软/谷歌) 三年 (2023–2025) 的财务数字,整整齐齐记在表格里。查数字去账本里翻,这就是 **SQL 数据库**。
- **一柜子档案** — 一共 6 份 10-K 年报原文 (每家公司 2024、2025 各一份,每份上百页)。查"公司自己怎么说"就去翻档案,这就是 **PDF 检索**。

你问它一个问题,它自己判断:**这个问题查账本就行?查档案就行?还是两个都要查?** 查完把证据摆出来,再写一段带出处的回答。这就是全部。"Agentic RAG" 翻成人话就是:**让大模型自己决定查哪里、查几次,最后只准它拿查到的证据说话,不准瞎编。**

### 一个问题进来,会发生什么事 (拿 q_012 举例)

问题:"苹果大中华区收入 2024 到 2025 变了多少?10-K 里有没有解释为什么?"

- **第 1 步 — 调度员先想 (agent.py 里的 planner)**:这个问题一半是数字、一半是原因,所以要查两边:先账本、再档案。
- **第 2 步 — 查账本 (sql_tool.py)**:它把人话翻译成一句 SQL 查询,去账本里查出:大中华区 2024 年 669.5 亿、2025 年 643.8 亿,跌了约 3.8%。
- **第 3 步 — 查档案 (pdf_tool.py)**:它拿着"大中华区、iPhone、Mac"这些词去档案卡片里搜,翻到 10-K 原文那一段:大意是 iPhone 卖得少了,Mac 卖得多了、抵消了一部分。
- **第 4 步 — 写回答 (agent.py 里的 _synthesize)**:另一个环节专门负责写。它**只能用第 2、3 步查到的证据**,把数字和原因拼成一段话,还必须注明出处 (哪份 10-K、第几页)。
- **第 5 步 — 交卷**:答案连同证据一起返回。看答案的人点开证据,就能核对每个数字的来历。

记住这个五步流程,面试 walk 代码就是**带着面试官走这五步**,走到哪一步就打开哪个文件指给他看。下面英文部分 "The 5-minute walk" 就是这五步的英文版说法,一一对应。

### 提前干的一件事:把档案撕成小卡片 (ingest.py)

档案一共 6 份 PDF、上千页,现场一页页翻太慢。所以系统**提前**做了一次整理 (只做一次,不是每个问题都做):

- 把每页文字切成小段 (每段约 1,400 个字符),一共切出 **1,754 张"卡片"**。
- 每张卡片上写清楚:哪家公司、哪一年、第几页、属于年报的哪一节 (比如"风险因素"那一节)。
- 再给每张卡片算一个"意思指纹" (embedding,理解成:把这段话的意思变成一串数字),存起来。

这样查档案时有两种找法,系统**两种一起用** (这就是所谓 hybrid 混合检索):

- **按意思找**:问题和卡片的意思像不像 (指纹比对) — 好处是换个说法也能找到。
- **按关键词找 (BM25)**:问题里的词在卡片里出现得多不多 — 好处是专有名词 (比如 "Greater China") 不会漏。

两种找法各占一半分,再按公司和年份先筛掉不相关的 (问苹果就别翻微软的档案)。**为什么不用更高级的向量数据库?就 1,754 张卡片,挨个比一遍瞬间就完事,杀鸡不用牛刀** — 这句话面试时原样说就行,是加分项不是减分项。

### 每个文件是干什么的 (人话对照表)

- `server.py` — **前台窗口**。外面的人 (网页、命令行) 从这里递问题进来,也是从这里拿答案。
- `agent.py` — **调度员 + 写报告的人**。整个系统的大脑都在这:先决定查哪里 (planner),查完负责写最终回答 (_synthesize)。
- `tools/sql_tool.py` — **查账本的工具**。负责把人话翻译成 SQL、去数据库查、把结果连同"它到底查了哪一句 SQL"一起带回来。
- `tools/pdf_tool.py` — **查档案的工具**。负责用上面说的两种找法,从 1,754 张卡片里挑最相关的 8 张带回来。
- `ingest.py` — **整理档案的人**。提前把 6 份 PDF 撕成卡片、贴标签、算指纹,只跑一次。
- `llm.py` — **传话筒**。所有要动脑子的事 (做决定、翻译 SQL、写回答) 都要问大模型,这个文件就是统一给 Fireworks 打电话的入口,自带"打不通就重试"。
- `config.py` — **总开关面板**。用哪个模型、每次查几张卡片、最多查几轮,全写在这里,别处不散落。
- `evaluate.py` — **自测考试卷**。自动把 10 道练习题全跑一遍、按官方给的评分办法打分,顺便检查每道题"该查的地方查了没有"。
- `cli.py` / `web/index.html` — **两个入口**:一个在命令行里问,一个在网页里问,背后是同一个大脑。

### 三个"为什么这么设计" (面试官最爱问的,人话版)

- **为什么让大模型自己决定查哪里,而不是每次两个都查?** 都查又慢又吵:问个简单数字还翻出 8 张无关卡片,反而容易把写回答的带偏。该查什么查什么,这本身就是这份作业要考的核心能力。
- **为什么查账本要这么小心 (只读、只准 SELECT)?** 因为 SQL 是大模型现编的,万一它编错一句把账本改了/删了就完了。所以数据库用**只读**方式打开,从根上写不进去;再加一道检查:不是查询语句一律不执行。这叫"不信任模型生成的代码,先关进笼子再让它跑"。
- **为什么写回答要单独一步,不让调度员顺手写了?** 试过,会翻车:答案太长塞进调度员的回复格式 (JSON) 里会截断、把格式弄坏。分开之后各干各的:调度员的回复永远短小 (就说下一步查什么),写回答的只看证据写作文。**面试被问到时就这么讲:这是一个真实踩过的坑换来的设计。**

### 成绩怎么看 (别被数字唬住,也别吹过头)

- **对了 8/10,查的地方 10/10 都对。** 错的两道 (q_006、q_025) 都是"要列全、要分好几部分答"的大题:一道要把苹果供应链风险**列全**,系统翻到的卡片偏到关税那边去了,漏了"依赖少数供应商"这几条;一道要算**两年**的增速还要加一段战略解读,系统只答全了第一年。
- **错因不在"模型笨",在两个具体的机械限制** (这是你比 Claude 那份文档多知道的):查档案每次只带回 **8 张卡片、每张只给写回答的看前 600 字**;所有证据加起来**超过 9,000 字就截断**。题目一大,证据装不下,答案自然缺块。怎么修,后面英文 Q&A 里有现成说法。
- **一个诚实提醒**:所谓"路由 10/10"的算法是"该查的都查了就算对",多查了不扣分 (q_017 就多查了一次账本)。面试官如果翻到 evaluate.py 会看出来 — **自己先说,比被他指出来强得多。**

看懂上面这些,就可以往下看英文部分了:那边是**面试时具体怎么说** (台词 + 问答),不用再重新理解一遍。

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
