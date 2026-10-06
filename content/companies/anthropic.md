---
title: "Anthropic — Staff Software Engineer, Search (OA passed 2026-10-06)"
slug: "anthropic"
section: "companies"
nav_order: 80
nav_label: "Anthropic"
tags: ["llm", "system-design", "deep-dive", "interviewing", "research", "safety", "search", "values", "swe"]
updated: "2026-10-06"
company: "Anthropic"
priority: "p0"
status: "interviewing"
process_sources:
  - { label: "REPORTED", url: "https://github.com/amitgaur/ai-interviewing/blob/HEAD/research/anchor-anthropic.md", accessed: "2026-10-01", note: "Researched 2026-04-16: recruiter screen → CodeSignal take-home (~90m, 4 escalating levels; e.g. in-memory DB → filtered scans → TTL → compression) → HM 1:1 → virtual onsite (~4h, 4 rounds: coding, system design e.g. distributed search 1B docs/1M QPS, safety/ethics behavioral) → references; values round is a hard gate" }
  - { label: "REPORTED", url: "https://www.finalroundai.com/blog/anthropic-interview-process", accessed: "2026-10-01", note: "SWE = 2 coding + system design + values; MLE/RE = lighter coding + 1-2 ML deep rounds + research presentation/take-home + values" }
  - { label: "OFFICIAL", url: "https://www.anthropic.com/candidate-ai-guidance", accessed: "2026-10-01", note: "Anthropic's official AI-use policy for candidates — read before interviewing" }
  - { label: "REPORTED", url: "https://www.1point3acres.com/bbs/thread-1190157-1-1.html", accessed: "2026-10-06", note: "1point3acres 2026 compilation (25 posts, updated ~Oct 2): OA is build-a-system multi-stage not LeetCode; recruiter screen digs why-Anthropic + AI safety ~20 min and fails shallow answers; senior+ tech phone often starts with SD; onsite 4-5 rounds; 2026 new rounds: agentic coding (Claude Code on real repo), network debugging role-play; slow — 2-3 weeks between rounds, 1-2 months total; template rejections, no feedback; team match after pass" }
  - { label: "REPORTED", url: "https://www.interviewquery.com/guides/anthropic-software-engineer", accessed: "2026-10-06", note: "OA (90-min proctored, 4 progressive levels) → live 90-min CodeSignal screen → final loop; references contacted at multiple points in parallel with interviews" }
  - { label: "REPORTED", url: "https://medium.com/@mockingbird_71808/a-breakdown-of-anthropics-5-round-swe-loop-073723fde2ca", accessed: "2026-10-06", note: "2026-06-29: recruiter screen → 90-min OA → HM deep-dive → two-part virtual onsite on different days (part 2 only if part 1 passes); breadth across coding/SD/project ownership/ethical reasoning; AI assistance prohibited in all live rounds" }
  - { label: "REPORTED", url: "https://www.tryexponent.com/experiences/anthropic-senior-software-engineer-interview-2ffa5f", accessed: "2026-10-06", note: "Senior SWE Safeguards 2026: onsite = HM + coding + company values + SD + coding; values round run by nontechnical people 'like a therapy session' probing feelings; prep behaviorals harder than technicals; skepticism beats generic 'I love your mission'" }
---

## TL;DR

**Status: OA passed 2026-10-06. Next: intro/recruiter call with Yulia
Serhiyenia, Wed 2026-10-07 11:00–11:20 AM PT.** REPORTED 2026 shape (25-post
1point3acres compilation, Oct 2026):

- **Recruiter/HR screen (~30 min) → technical phone (senior+ often SD
  first, else practical coding) → virtual onsite 4–5 rounds (SD, coding,
  HM, project deep-dive, values/culture)** → team match → references.
  Your OA (build-a-system, multi-stage) already cleared the first filter.
- **Gate #1 is the recruiter screen, not the onsite:** ~20 min of
  why-Anthropic + AI safety deep-dive; shallow answers fail people with 10
  years of experience [REPORTED]. Prepare this FIRST.
- **Gate #2 is the values round:** run by nontechnical interviewers, feels
  like a therapy session — they probe *how you felt*, not just what you
  did. Skeptical honesty beats generic "I love your mission" [REPORTED].
- Pace is **slow**: 2–3 weeks between rounds, 1–2 months end to end.
  Rejections are template with no feedback.
- OFFICIAL: **no AI assistance in any live round** —
  [candidate-ai-guidance](https://www.anthropic.com/candidate-ai-guidance).
  References may be contacted *mid-process*, in parallel with interviews.

## Company & product

Anthropic: the Claude model family, known for the safety-first research
culture — **Constitutional AI**, interpretability research, and widely-cited
engineering writing (including the "Demystifying evals for AI agents" piece
that adopted Sierra's τ-bench pass^k framing). The culture prizes careful
reasoning, intellectual honesty, and safety impact alongside capability.

## Role expectations

Staff Software Engineer, Search (INFERRED from JD + level):

- **Staff bar = scope and influence, not just depth.** Expect the HM and
  deep-dive rounds to probe: leading a technical direction across teams,
  setting quality bars, resolving cross-team disagreements. Your Coupang
  tech-lead story (Search & Discovery, generative retrieval) is the anchor —
  prepare 2–3 scope-and-impact narratives, not just technical ones.
- **Search domain depth:** retrieval architecture, indexing pipelines,
  ranking/re-ranking, query understanding, latency budgets, freshness vs.
  cost tradeoffs. This is your home turf — the SD round likely lives here
  (reported example: distributed search over 1B docs at 1M QPS).
- **AI-adjacent fluency:** retrieval-augmented generation, evals, safety as
  a systems concern (abuse-resistant serving, prompt-injection
  considerations in a search stack).
- **Values alignment:** the values round gates offers; it's about how you
  reason under uncertainty and disagreement, not reciting principles.

## Interview process

OA ✅ passed 2026-10-06 (90 min, 4 progressive build-a-system levels —
**not** LeetCode; "get it built, running, and handle edge cases" is the
bar). All remaining rounds REPORTED BY CANDIDATES (Oct 2026 refresh).

### Recruiter / HR screen (~30 min) — GATE #1

**Substantive and failable.** Expect ~20 min of *why Anthropic* + AI safety
deep-dive [REPORTED Oct 2026]. Sample questions seen in 2026:

- How is Anthropic different from other AI labs, and why Anthropic *over
  the others*?
- What does AI safety mean to you, personally? What happens if AI is misused?
- What's the most underrated problem in AI right now?
- React to a recent Anthropic announcement — what's your read?

Failure mode: answering *why Anthropic* shallowly. A 10-year candidate
failed here [REPORTED]. Prepare a 2-minute, specific, slightly skeptical
version (see the answer bank below) — generic mission-praise reads as
unprepared.

Your intro call (Yulia, 10/7, 20 min) is the opening of this stage; the
substantive screen may be the same call or scheduled right after.

### Technical phone (60–90 min)

For senior+ this is **often system design first** [REPORTED Oct 2026] —
inference/search-flavored (e.g., inference batching; distributed search).
Otherwise practical coding in the OA spirit: parsing logs, file
deduplication, concurrent crawler. Interviewers are quiet; it reads as
evaluation, not collaboration.

### Virtual onsite — two parts on different days (4–5 rounds)

Part 2 is only scheduled if part 1 passes [REPORTED].

1. **HM deep-dive** — background, scope, technical taste, team fit. At staff
   level: org-level impact stories.
2. **Coding × 1–2** — practical, CodeSignal-spirit. 2026 high-frequency:
   **file deduplication**, **image processing pipeline** (resize/rotate,
   PIL, batch, multiprocessing), **concurrent crawler** (sync first, then
   async; visited-set thread safety). TypeScript sometimes allowed; you may
   get **no test cases and have to fix your own environment issues**
   [REPORTED] — practice debugging blind.
3. **System design** — inference/search production: batching strategies, KV
   cache, GPU memory, load shedding, idempotency. 2026 trend: **design-doc
   review** — you're handed a doc and asked to find its holes.
4. **Project deep-dive** — your best work under expert questioning. The
   "5th Layer" training–serving skew writeup is strong material.
5. **Values / culture** — GATE #2. See templates below.

2026-new round types seen on SWE loops: **agentic coding** (real repo,
Claude Code, produce a PR) and **network debugging role-play** (perf/infra).
Prepare for the possibility, not the certainty.

### Logistics and failure modes

- **Pace:** 2–3 weeks between rounds is normal; 1–2 months end to end.
  Don't idle — keep other processes warm.
- **Feedback:** rejections are template, no feedback given. Silence ≠
  rejection for weeks.
- **References:** may be contacted **mid-process, in parallel** with
  interviews — have your list ready early [REPORTED].
- **No AI assistance in any live round** (OFFICIAL policy) — prep solo,
  think solo.
- **Team match** happens after the loop: passing the loop doesn't guarantee
  a team wants you; have a crisp "what I want to build" pitch.

## Why Anthropic & AI safety — answer bank

This is the highest-leverage prep on the page: it's the round that fails
the most qualified candidates, and it comes *first*.

:::tldr
Have a 2-minute why-Anthropic that is **specific, personal, and slightly
skeptical**. Read **Anthropic's Core Views on AI safety** + the
Constitutional AI paper summary + the last 90 days of Anthropic news before
any screen. Shallow = fail.
:::

### The 2-minute framework

1. **Personal hook (30s):** one concrete moment from your work where safety/
   reliability *actually* cost you something — e.g., holding back a
   generative-retrieval launch at Coupang because offline metrics hid a
   serving skew (your 5th Layer story). Real stakes > abstract concern.
2. **Why this lab, not others (45s):** name something *specific* —
   Constitutional AI as a research program, the interpretability agenda,
   the evals culture ("Demystifying evals" and broken-harness thinking).
   Contrast without trashing others.
3. **What you'd build (30s):** tie to the Search role — abuse-resistant
   retrieval, evaluation rigor for RAG, measurement honesty.
4. **Honest tension (15s):** one thing you're genuinely unsure about
   (capability vs. safety tradeoffs, open vs. closed). Skepticism signals
   thinking; pure praise signals rehearsal.

### Safety questions seen in 2026 screens — talking points

- **"What does AI safety mean to you?"** — Don't define the field; define
  *your* relationship to it. Failure modes you've touched (reward hacking
  in ranking, eval gaming, feedback loops), plus where you think the hard
  problems are (deployment, misuse, concentration of power).
- **"How is Anthropic different from other AI labs?"** — Research-led
  safety (Constitutional AI, interpretability as a *program* not a team),
  public technical writing, slower/measured deployment posture. Have one
  concrete artifact to cite (a paper or engineering post you actually read).
- **"What happens if AI is misused?"** — Show you can reason about
  dual-use concretely: pick one domain (e.g., search/ranking
  manipulation, persuasion at scale) and walk through the mechanism, not
  slogans.
- **"Biggest risks and benefits of advanced AI?"** — Two-sided, specific,
  and personal: which risk worries *you* most given what you've built, and
  which benefit motivates your work.
- **"React to a recent Anthropic announcement."** — Check their blog/news
  the week of the interview. Have a take with a supporting argument and a
  counter-argument.

### Mistakes that fail this round

- Generic "I love your mission / AI safety is important."
- Knowing *zero* Anthropic-specific work (no paper, no post, no product
  detail).
- Treating safety as compliance rather than a technical problem.
- Being unable to name a genuine disagreement or uncertainty.

## Priority topics

1. **Constitutional AI / alignment:** RLAIF, harmlessness–helpfulness
   tradeoffs, red-teaming concepts.
2. **Post-training:** RLHF, DPO, GRPO (2026-named), reward hacking.
3. **Transformers & training:** attention, optimization, scaling laws,
   compute estimation (FLOPs math for training runs).
4. **Interpretability:** features, circuits — conversational fluency, not
   implementation.
5. **Eval design:** their engineering blog sets the bar — eval hygiene,
   broken-harness failure modes, LLM-as-judge limits.
6. **System design:** distributed search at 1B docs / 1M QPS (reported
   example) — retrieval, sharding, caching.
7. **CodeSignal-style evolution problems:** in-memory DB → scans → TTL →
   compression; practice the *extension* pattern.

## Company-specific themes

- **Safety as first-class:** not a compliance checkbox — the research culture
  treats safety as the hard technical problem. Engage sincerely.
- **Intellectual honesty:** the values round probes how you handle being
  wrong and uncertain — "I don't know, here's how I'd find out" beats
  bluffing.
- **Writing culture:** Anthropic's engineering blog is unusually good; clear
  technical writing is a hiring signal (your Medium piece helps).
- **Candidate AI guidance:** they have an *official policy* on AI use in
  interviews — read it; violating it is an instant fail.

## Likely system-design domains

REPRESENTATIVE PRACTICE (not reported as asked — do not claim otherwise).
Use the 18-step framework in [#/ml-system-design](#/ml-system-design).

### The search round — 1B docs, 1M QPS, p99 < 100ms (reported example)

Your home turf. Walk it with arithmetic, not adjectives:

1. **Scope:** read-heavy? write rate? freshness SLA (seconds vs minutes)?
   Query mix (head/torso/tail) — the tail decides the architecture.
2. **Indexing pipeline:** crawl/ingest → parsing → tokenization → inverted
   index build; batch vs. streaming index updates; segment merges.
3. **Sharding:** document sharding (scatter-gather, tail latency) vs. term
   sharding (hot-term skew); hybrid. Shard count from QPS ÷ per-shard QPS.
4. **Replication & consistency:** N replicas for QPS; freshness lag budget
   per replica; what "stale" means to the user.
5. **Caching layers:** query-result cache (head queries), posting-list
   cache, ranking-feature cache; invalidation on index updates.
6. **Retrieval → ranking:** candidate generation (BM25/ANN), then
   multi-stage ranking; where the LLM/reranker sits and what it costs;
   merge across shards (top-k merge, score normalization).
7. **Failure & tail:** hot shards, slow-shard hedging, graceful degradation
   (fewer stages under load), load shedding, backpressure.
8. **Eval/observability:** relevance metrics, latency histograms, index
   health, A/B infra.

Follow-up traps to rehearse: hot-term skew, index-freshness vs. cache-TTL
tension, tail-latency hedging cost, what breaks first at 10×.

### Inference-flavored (2026 canonical shape)

"Design an inference batching system for a single GPU: up to 100 inputs per
batch, users submit synchronously and wait." What it tests in 50–55 min:
queueing under random arrivals, batching vs. latency tradeoff, KV-cache
memory math, load shedding, and failure-mode reasoning — not just the happy
path. Practice saying the latency/throughput tradeoff *with numbers*.

### Design-doc review drill (2026 trend)

You're handed a doc and asked to find holes. Practice lens: unstated
assumptions, missing failure modes, metrics that can be gamed, scaling
cliffs, and "what would you measure first."

### Other domains

2. Design a Constitutional-AI training pipeline: data, critique loop, eval
   gates.
3. Design eval infrastructure for a frontier model: harness reliability,
   contamination controls, human eval.
4. Design inference for Claude-scale traffic: batching, caching, cost.
5. Design a red-teaming platform: attack generation, scoring, regression.

## Project deep-dive emphasis

- **Research presentation:** lead with the "5th Layer" — training–serving
  skew in generative retrieval. It's exactly the kind of careful empirical
  work Anthropic respects.
- For MLE tracks: Coupang ranking with emphasis on measurement rigor and
  the decisions where you chose the careful experiment over the fast one.
- Values-round stories: a time you raised a concern others dismissed; a time
  you changed your mind on evidence.

Full prep: [#/project-deep-dive](#/project-deep-dive).

## Recent work worth knowing

1. **Candidate AI guidance** (OFFICIAL): [anthropic.com/candidate-ai-guidance](https://www.anthropic.com/candidate-ai-guidance)
   — read before any round.
2. **"Demystifying evals for AI agents"** (Anthropic engineering) — adopts
   τ-bench's pass^k; know its thesis (broken harnesses, not weak models,
   explain low scores).
3. Check Anthropic's research blog for the last 90 days before any real
   process — interpretability and safety agendas move fast.

## Values round — story templates

Run by **nontechnical interviewers**; they probe *how you felt*, not just
what you did — candidates describe it as "like a therapy session"
[REPORTED 2026]. Prepare 4 stories; tell each with the feeling included
(frustration, doubt, relief), not just the logic. Skeptical honesty beats
mission-praise.

- [ ] **Raised a concern others dismissed:** e.g., flagging the
      training–serving skew risk before a launch. Beats: what you saw, who
      disagreed and why, what you did (data? escalation?), how it felt to
      push, what happened, what you'd do differently.
- [ ] **Changed your mind on evidence:** a technical bet you reversed
      (ranking approach, launch decision). Emphasize the *moment* of
      changing your mind — what evidence tipped you, how it felt to admit
      it, what it cost.
- [ ] **Moral gray area / conflict:** a disagreement where both sides had
      a point (ship velocity vs. measurement rigor; a teammate's shortcut).
      Show how you reasoned, not just the outcome.
- [ ] **Tough feedback received (or given):** what stung, what was true
      in it, what changed afterward. This one is the therapy-session
      favorite.

Drill: for each story, prepare the 90-second version and the 5-minute
version, plus one "what did you learn about yourself" closer. Full
behavioral prep: [#/behavioral](#/behavioral).

## Practice questions

All REPRESENTATIVE PRACTICE — modeled on reported 2026 Anthropic patterns,
not claimed as asked.

**Practical coding (2026 high-frequency):**
- [ ] **File dedup drill:** walk a directory tree, hash files, report
      duplicates. Handle the "no duplicates → no output" edge; then make
      it concurrent. No test harness — debug blind.
- [ ] **Image pipeline drill:** resize/rotate a batch (PIL), then add
      multiprocessing, then harden against corrupt files. Say the output
      dimensions out loud as you go — interviewers probe them.
- [ ] **Concurrent crawler drill:** sync crawl of one hostname (strip
      fragments, dedupe), then convert to async with a thread-safe visited
      set.
- [ ] Build an in-memory KV store; extend: filtered scans → TTL expiry →
      compression. Keep the abstraction clean across all 4 levels (90 min).

**System design:**
- [ ] Distributed search: 1B docs, 1M QPS, p99 < 100ms. Shard, replicate,
      cache, merge — with the arithmetic (use the framework above).
- [ ] Single-GPU inference batching: 100 inputs/batch, synchronous users.
      Queueing, latency/throughput tradeoff with numbers, KV-cache math,
      load shedding.
- [ ] Design-doc review: take any design doc you wrote, red-team it for
      unstated assumptions and missing failure modes.

**ML depth:**
- [ ] Explain Constitutional AI: the critique loop, where it beats RLHF, its
      failure modes.
- [ ] Estimate training FLOPs for a 70B model on 2T tokens. Show the math;
      then estimate the cluster and time.
- [ ] What is GRPO, and when would you prefer it over PPO for post-training?
- [ ] Design an eval for instruction-following that resists contamination and
      harness bugs.

**Values (hard gate — prepare seriously):** use the story templates above;
add:
- [ ] Describe a decision you made under deep uncertainty. How did you
      reason, and what would change your mind?
- [ ] When have you chosen the slower, more careful path over shipping fast?

## 每轮备战资料清单

按轮次列出：读什么、写什么、练什么。整理自 2026 年 REPORTED 面经
（地里 25 帖汇总、Axios 文化面报道、Exponent/Medium 实战帖），非官方流程承诺。

### Recruiter / HR screen — 明天 10/7，GATE #1

读：
- [ ] Anthropic **Core Views on AI Safety**（官网，通读）
- [ ] **Constitutional AI** 一页纸：critique loop、RLAIF、failure modes
- [ ] 过去 90 天 Anthropic 新闻，准备 1 个带正反论据的观点
写：
- [ ] **2 分钟 why-Anthropic 稿**（personal hook + why this lab + 想做什么 + 一个 honest tension），说出来不背稿
- [ ] "如果公司为安全放弃业务、股权归零，你怎么看"——先自己写一遍诚实答案（Axios 报道的文化面真题；Blind 上有候选人答"不开心但希望 ethical + 可持续"，面试官不喜欢——这题没有标准答案，考察的是你的真实推理）
挂人点：why Anthropic 答得浅，10 年经验也挂。别背 mission statement。

### Technical phone（senior+ 常 SD 起手）

练：
- [ ] search SD 八步框架默写一遍（本页上文）
- [ ] inference batching 的数字：batching vs. latency tradeoff、KV cache 内存估算、load shedding
- [ ] concurrent crawler：sync 版 → async 版，visited 集合线程安全
习惯：面试官偏安静、偏评估；先讲思路（做什么、重点在哪、为什么选这个方案）再写码。

### HM deep-dive

准备：
- [ ] 2–3 个 **scope & impact** 故事：Coupang tech lead 期间定的技术方向、跨团队分歧怎么解决、质量标准怎么立
- [ ] 30 秒"想做什么" pitch（Search 方向 + 为什么是你）
- [ ] 反问 HM 的 3 个问题（团队 roadmap、staff 的成功标准、当前最大风险）

### Coding 轮 ×1–2

练（每个 45–60 分钟，**盲调、无 test case**，自己修环境问题）：
- [ ] **file dedup**：目录树遍历 → hash → 去重报告 → "无重复则无输出"边界 → 并发版
- [ ] **image pipeline**：PIL resize/rotate → batch → 多进程 → 坏文件加固；大声报出每步输出尺寸（面试官会抠）
- [ ] **concurrent crawler**：只爬同 hostname、去 fragment、去重 → 并发
习惯：沟通 > 一次写对；变量命名规范；讲 tradeoff 的适用场景（"数据量很小时 linear search 可能更快"这类工程判断是 staff 加分项）。

### System design 轮

练：
- [ ] distributed search（1B docs / 1M QPS / p99 < 100ms）全流程**带数字**走一遍：shard、replica、cache 层、ranking merge、tail 处理
- [ ] follow-up traps：hot-term skew、freshness vs. cache TTL 的 tension、hedging 成本、10× 流量先崩哪里
- [ ] **design-doc review**：拿自己写过的设计文档红队一遍——找 unstated assumptions、缺失的 failure mode、可被 gaming 的指标

### Project deep-dive

准备：
- [ ] **"5th Layer" 故事线**：现象 → 测量 → 决策 → 影响（5 分钟版 + 15 分钟版）
- [ ] 预演 expert 追问：为什么这个实验设计？反事实是什么？换种测量方式结论还成立吗？
- [ ] Coupang ranking 严谨性故事：选"慢而谨慎的实验"而非"快的"的那次

### Values / culture 轮 — GATE #2

准备（用本页故事模板）：
- [ ] 4 个故事各备 90 秒版 + 5 分钟版 + "这让我学到了什么"收尾，**讲感受不只讲逻辑**
- [ ] 一个真实道德困境：两难是什么、你的推理过程、事后怎么看
- [ ] 态度：诚实自省 > 打磨过的 STAR；带一点怀疑精神。据教练反馈，把这轮当标准 behavioral 背稿的人表现反而差——面试官要的是真实的自我反思和道德复杂性。
- [ ] 了解：**offer 薪资不接受谈判**（Axios 报道：标准流程，no counteroffer）——这家不适用谈判策略。

### 通用资料（全流程）

- [ ] [candidate-ai-guidance](https://www.anthropic.com/candidate-ai-guidance)（官方 AI 使用政策，live 轮禁用 AI 辅助——必读）
- [ ] "Demystifying evals for AI agents"（Anthropic engineering blog，eval  hygiene 的标杆）
- [ ] reference 名单提前准备好（背调可能在流程中途并行启动）
- [ ] 慢流程心态建设：轮次间隔 2–3 周正常，全程 1–2 个月；拒信是模板不给 feedback，别内耗

## 30-minute checklist — before the recruiter call (Wed 10/7, 11 AM)

- [ ] **2-minute why-Anthropic (10 min):** write it with the framework
      above; say it out loud once. Specific > sweeping.
- [ ] **Safety talking points (10 min):** your personal definition, one
      dual-use walkthrough (search/ranking manipulation), biggest risk +
      benefit with your own angle.
- [ ] **This week's Anthropic news (5 min):** skim the blog/newsroom; have
      one take with an argument and a counter-argument.
- [ ] **AI policy (5 min):** [candidate-ai-guidance](https://www.anthropic.com/candidate-ai-guidance)
      — non-negotiable before any live round.
