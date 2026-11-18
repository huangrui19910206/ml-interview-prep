---
title: "Applied Intuition — Onsite Loop (Mon 2026-12-07, Sunnyvale HQ)"
slug: "applied-intuition"
section: "companies"
nav_order: 84
nav_label: "Applied Intuition"
tags: ["system-design", "ai-coding", "coding", "behavioral", "deep-dive", "interviewing"]
updated: "2026-11-18"
company: "Applied Intuition"
priority: "p0"
status: "interviewing"
process_sources:
  - { label: "OFFICIAL", url: "https://www.appliedintuition.com/engineering-blog/hiring-engineers-age-of-agents", accessed: "2026-11-18", note: "Applied engineering blog (Jul 22, 2026), 'Hiring engineers for the age of agents' — fetched and read in full 2026-11-18. Phone screen kept as-is: 45-min coding, NO AI ('engineers are still responsible for every line'). Onsite redesigned: 45-min system design on an open-ended problem 'usually derived from something we've actually had to solve at Applied', then 2 hours to build a working prototype of that design with ANY AI model and any frameworks, then a demo in front of a panel of engineers — walk through what you built, the decisions you made, and what you'd do differently. Trial data: 30+ real onsites; interviewer confidence 4.0-4.7/5 on practical skills, tackling unfamiliar challenges, technical communication, logical thinking, technical mastery; code elegance deliberately scored lower here (covered by the phone screen). Blog also says the format is STILL BEING SCALED across the company — not every loop runs it yet." }
  - { label: "OFFICIAL", url: "https://applied.co/technical-interview", accessed: "2026-11-04", note: "Applied's own technical-interview guide: exercises are hand-selected per candidate background; mix of coding, system design, debugging; ML domain expertise tested if relevant. Rubric = collaborative ability (clarify ~2 min, brainstorm multiple approaches, talk continuously) + fast & performant code + code design & elegance. Coding interviews: NO generative AI; Google/search allowed only with screen shared." }
  - { label: "OFFICIAL", url: "", accessed: "2026-11-18", note: "Rui's own loop: HM round with Sergey Andreev (Head of Data & Compute) passed (confirmed Nov 2); coding round Fri Nov 6 with Martin Meinke PASSED. Onsite booked for Mon Dec 7, 2026, 1:00-5:00 PM PT at Sunnyvale HQ (860 W California Ave), confirmed by Rui Nov 18 after the feedback/next-steps call with coordinator Sophia Conn. Round-by-round schedule and interviewer names NOT yet received — Sophia to send. Applied NDA still unsigned in every record as of Nov 18." }
  - { label: "REPORTED", url: "https://landthelab.com/companies/applied-intuition", accessed: "2026-11-18", note: "LandTheLab reconstruction (sources incl. official site + 1point3acres): 7 rounds total; onsite = system design 45 min (Excalidraw / CoderPad drawing) -> AI-assisted build 120 min (Claude Code or a provided Claude model expected) -> project presentation 30 min (present what you built in the onsite, OR a prepared past project). Coding is the most reported question type (28 of 39); reported design question: design a job scheduler (possibly retired)." }
  - { label: "REPORTED", url: "https://www.fastprep.io/applied-intuition-interview", accessed: "2026-11-18", note: "FastPrep catalog of Applied-tagged public reports, several last reported Nov 2026. Coding: KV store with nested transactions (Phone AND Onsite), resolve variable equations with dependency errors (DFS), compilation order / topological sort, parse nested message types, locate vehicles with square queries, file-backed dense Game of Life, ring buffer operations, hash map with separate chaining (Onsite). System design: 'Design a Distributed Simulation Platform' — run large reproducible simulation jobs across shared compute, hardware-requirement-aware placement, durable progress, fair admission, one authoritative result. Project coding: driving log ingestion and playback windows; design a real-time 3D log playback system." }
  - { label: "REPORTED", url: "https://www.jointaro.com/interviews/companies/applied-intuition/experiences/software-engineer-full-stack-mountain-view-california-september-29-2026-no-offer-positive-ff42e25e/", accessed: "2026-11-18", note: "Taro/Glassdoor candidate reports (multiple, 2025-2026) describing the CLASSIC super day: half-day onsite = 2 coding + 1 system design + 1 behavioral with the hiring manager; or 3x 45-min technical + 1x 45-min behavioral with the tech lead. Behavioral is a career-history deep dive — one report: 'essentially a deep dive into my backstory, starting from late high school... why I made certain decisions... cultural fit.' Coding screen question reported: topological sort. Virtual-onsite variant: 30-min group intro + 3x 45-min coding + 45-min HM." }
  - { label: "REPORTED", url: "https://www.designgurus.io/answers/detail/what-to-expect-in-the-applied-intuition-system-design-interview", accessed: "2026-11-18", note: "DesignGurus system-design synthesis: 45-60 min round on autonomy-flavored problems — the simulation platform (thousands of scenarios vs an autonomy stack; hard parts = scheduling compute, exact reproducibility, pass/fail scoring), fleet drive-log pipelines (one drive = terabytes; storage cost, event indexing, replay), 'design an off-road autonomous vehicle', V2X communication simulation; occasionally a general question (maps-like service, distributed cache)." }
  - { label: "REPORTED", url: "https://www.screna.ai/interview-questions/applied-intuition", accessed: "2026-11-18", note: "Screna (aggregator): signature screen question = in-memory KV store with SET/GET/DELETE + nested transactions (COMMIT/ROLLBACK). Onsite system-design reports: (1) find duplicate files across a massive POSIX-like filesystem using METADATA ONLY (size/timestamps/inode; symlink loops, hard links, permission errors, define 'duplicate'); (2) transactional KV store as a full design deep-dive with distributed-systems tradeoffs pushed hard. Also a multi-source-BFS grid problem and a mini-interpreter (lexer/parser/AST) report." }
  - { label: "REPORTED", url: "https://www.1point3acres.com/bbs/thread-1187656-1-1.html", accessed: "2026-11-04", note: "1point3acres, Aug 2026, Applied technical phone screen (outcome Fail): opened with background chat, then the TRANSACTIONAL KEY-VALUE STORE — the post notes it is the same question other mianjing had reported. Candidate knew the question in advance and still failed; deciding details are points-gated and were not readable. Lesson stands for any onsite coding round: execution + communication graded, not recall." }
  - { label: "REPORTED", url: "https://www.interviewquery.com/guides/applied-intuition-inc-software-engineer", accessed: "2026-11-18", note: "InterviewQuery guide (updated 2026-11-03; synthesized from 30 candidate reports): loop mixes coding, design, and motivation/fit conversations; onsite coding reported as LeetCode medium-hard with practical twists (Sudoku, intervals variant, Minesweeper class); a situational/scoping round is also reported; career deep-dives are a named feature of the process." }
  - { label: "REPORTED", url: "https://latent.space/wiki/applied-intuition-c9e9e7c4/", accessed: "2026-11-18", note: "Latent Space company profile (sources as of 2026-09-17) for product facts: Neural Sim (Jan 2025) reconstructs virtual worlds from drive logs and renders camera/lidar for novel poses (Gaussian splatting + diffusion); SDS for Automotive (Aug 2025) end-to-end ADAS platform; Dana (launched Jul 21, 2026) — agentic platform connecting sensor-data curation, workflow orchestration, simulation, evaluation and analysis; defense lines Acuity + Axion, EpiSci tactical-AI acquisition; ~1,000 engineers, engineering = 83% of the company; 18 of the top 20 global automakers are customers." }
---

## TL;DR

**Status: HM round passed (Sergey Andreev, Head of Data & Compute) and
the Nov 6 coding round passed (Martin Meinke). Next: the onsite —
Mon Dec 7, 2026, 1:00–5:00 PM PT, in person at Sunnyvale HQ
(860 W California Ave). Coordinator: Sophia Conn. Round-by-round
schedule not yet sent — confirm it with her when it arrives.**

The single most important prep fact: **Applied redesigned its onsite
in 2026, and said so on its own engineering blog** (OFFICIAL). The new
format is not a stack of LeetCode rounds:

1. **45-min system design** — an open-ended problem "usually derived
   from something we've actually had to solve at Applied."
2. **2-hour build** — implement a working prototype of *the system you
   just designed*, with **any AI model and any frameworks** allowed.
3. **Panel demo** — present to a panel of engineers: what you built,
   the decisions you made, **what you would do differently**.

That trio is 3h15m of your 4-hour block. The remaining ~45 min most
likely holds a **domain deep-dive with Sergey's Data & Compute team**
and/or the **career-history behavioral** Applied is known for
(REPORTED). Both are prepared below.

:::warn
**Format risk — plan for the fork.** The official blog says the new
format is *still being scaled* across a 1,000-engineer company, and
candidate reports through late 2026 still describe the CLASSIC super
day (2 coding + 1 design + 1 behavioral, all no-AI). Your loop is
senior, staff-level, and team-specific (Data & Compute), which is
exactly where formats vary. The prep below is built so the design +
build core is unavoidable either way, and keeps a compressed coding
drill set warm in case a standalone coding round appears. When Sophia
sends the schedule, re-check this page against it the same day.
:::

**What wins this onsite, in one line:** a defensible design of a
simulation/data system, shipped as a *running* prototype in two hours
with AI leverage, defended with numbers — plus a career narrative that
makes "search ranking / ML platform at Coupang scale" sound like the
same job as "data & compute for autonomy validation." Because it is.

## Company & product

Applied Intuition builds the software toolchain autonomy programs run
on: high-fidelity simulation, scenario libraries, sensor models, and
the data infrastructure to validate vehicle intelligence at scale —
18 of the top 20 global automakers are customers, plus trucking,
defense, and off-road (REPORTED, Latent Space profile). $600M Series F
at a ~$15B valuation, June 2025. Roughly 1,000+ engineers; engineering
is ~83% of the company — an engineering-led culture with a systems
bar, not a web-app bar.

Recent work worth knowing cold (all REPORTED from the Latent Space
profile, sources to Sep 2026):

- **Neural Sim** (Jan 2025) — reconstructs virtual worlds from drive
  logs and renders camera/lidar from *novel* poses (Gaussian splatting
  + diffusion), so a tested system can depart from the recorded
  trajectory. Speed and cost decide whether RL on top is practical.
- **SDS for Automotive** (Aug 2025) — a learned end-to-end ADAS /
  autonomy stack (perception → planning → control) with inspectable
  intermediate outputs. Applied now ships the stack, not just the
  tools.
- **Dana** (Jul 2026) — the agentic layer over the whole toolchain:
  agents connect sensor-data curation, workflow orchestration,
  simulation, evaluation, and analysis through one interface. This is
  the most Data-&-Compute-shaped launch they have: it *is* an ML
  platform story.
- **Defense** — Acuity (ground/air/maritime autonomy) and Axion
  (mission tooling/simulation); EpiSci's tactical AI folded in.

**Your mapping, unchanged from the screen and now sharper:** Sergey's
org is **Data & Compute** — the platform that feeds simulation and
validation: log ingestion, scenario data, sim compute scheduling,
evaluation infrastructure. Your career is building ranking-and-
evaluation machines for search at Coupang/Pinterest scale. Simulation
validation is an evaluation machine for autonomy; scenario triage is a
retrieval problem; sim-vs-real gap is train–serve skew with higher
stakes. Say exactly that when "why Applied" comes — it will.

## Role expectations

Senior Staff-level seat on the Data & Compute / ML platform side
(INFERRED from the HM and the loop so far). What that bar looks like
at Applied specifically:

- **Systems engineering first.** The company's interview gravity is
  C++/systems-flavored even when the role is Python/ML-platform:
  memory, I/O, concurrency, and data layout get probed. Answer design
  questions down to the data path, not just boxes.
- **Ownership of outcomes, end to end.** The build round is literally
  "here is a problem, ship a working thing, defend it." Staff signal
  = scoping judgment under a hard clock.
- **AI fluency as table stakes, judgment as the differentiator.**
  OFFICIAL: "AI fluency is important, but only one aspect of the job…
  decision-making, technical excellence, and cultural factors matter
  more than ever." Engineers are accountable for every line, AI-written
  or not.
- **Customer obsession, stated as a value:** "Move fast, move safe;
  Never disappoint the customer; Raise the quality bar; Laugh a lot"
  (REPORTED via DesignGurus). For a platform role, your customers are
  the autonomy teams — frame platform stories that way.

## Interview process

| # | Round | Format | Status / source |
|---|-------|--------|-----------------|
| R0 | Recruiter chain — Rich Adao referral → Andy Goff → Nick Gutierrez; Sophia Conn (coordination) | Email | ✅ Done |
| R1 | Hiring-manager — Sergey Andreev, Head of Data & Compute | Video | ✅ Passed (confirmed Nov 2) |
| R2 | Coding — Martin Meinke, 45 min, CoderPad, Python, no AI | Video | ✅ Passed (Nov 6) |
| R3 | **Onsite — Mon Dec 7, 1:00–5:00 PM PT, Sunnyvale HQ** | **In person, 4 hours** | **This page** |

Inside the onsite — what the evidence supports:

| Block | Length | Source |
|-------|--------|--------|
| System design — open-ended, from a real Applied problem | 45 min | OFFICIAL blog |
| Build — working prototype of your design, any AI model/frameworks | 2 hours | OFFICIAL blog |
| Panel demo — what you built, decisions, what you'd do differently | ~30 min | OFFICIAL blog (length REPORTED by LandTheLab) |
| Domain deep-dive with the hiring team and/or career-history behavioral | ~45 min | INFERRED — fills the 4-hour block; both round types are REPORTED staples of Applied loops |

Classic-format reports (for the fork): 2× ~60-min coding (LeetCode
medium-hard, practical twists) + 1× design + 1× behavioral/HM
(REPORTED, Glassdoor/Taro/DesignGurus). If your schedule email shows
that shape instead, the design prep below still applies and the
compressed coding set in Priority 4 is your coverage.

**Signals the new format is scored on** (OFFICIAL, interviewer
confidence ratings from the company's own trial): practical skills,
tackling unfamiliar challenges, technical communication, logical
thinking, technical mastery. Code elegance is deliberately *not* what
the onsite measures — the screen already did. Translation: a running,
well-explained, honestly-traded-off prototype beats a beautiful
half-finished one. Every time.

## Priority 1 — System design (45 min): the round that picks your build

This round does double duty: it is scored on its own, **and it chooses
what you build for the next two hours.** Design something you can
actually prototype — a clean core with named extension points beats a
sprawling architecture you cannot stand up. Say that tradeoff out loud
in the design itself: "I'll design the full system, but the buildable
core is X; Y and Z slot in behind these interfaces." Interviewers
wrote that sentence into the format on purpose.

**Mechanics (from the OFFICIAL interview guide, still the house
rubric):** ~2 minutes clarifying before drawing; brainstorm 2
approaches with tradeoffs, then commit; narrate continuously; put
numbers on everything (scenarios/day, GB per log, jobs/hour, p99
budget). Design discussion is usually on a whiteboard/Excalidraw
(REPORTED).

### Design A — Distributed simulation platform (have this cold)

The single most on-target reported prompt for this org (REPORTED,
FastPrep, Nov 2026): *run large, reproducible simulation jobs across
shared compute — place each phase only on hardware meeting its
declared requirements, preserve durable progress, admit work fairly,
produce one authoritative result.*

- **Objects:** Scenario (versioned: world, actors, triggers, pass/fail
  criteria) × StackBuild (the autonomy binary/config under test) ×
  Seed → a **Run**. The Run is the unit of scheduling, billing, and
  truth.
- **Submission path:** API → validation (scenario compiles? assets
  exist?) → Run records in a durable queue, keyed by
  `(scenario_version, stack_build, seed)` — the idempotency key that
  makes "one authoritative result" enforceable: a duplicate submission
  returns the existing Run instead of executing twice.
- **Scheduler:** two-level — admission (per-team fair-share quotas +
  priorities; a release-blocking regression suite preempts a research
  sweep) → placement (match declared requirements: GPU model, RAM,
  sensor-model licenses, region) onto a heterogeneous fleet. Bin-pack
  with requirement vectors; keep a small hot reserve for interactive
  single-scenario debugging runs — latency for one Run matters as much
  as throughput for 100k.
- **Execution:** workers pull leases with heartbeats; **checkpoint at
  phase boundaries** (load → simulate → score) so a preempted or
  crashed job resumes instead of restarting — "durable progress" is
  the phrase in the prompt, spend real time on it. Deterministic mode:
  pinned stack build, pinned scenario assets, fixed seed, single-
  threaded scoring path; say what determinism costs (~10–30%
  throughput) and when you waive it.
- **Results:** artifacts (logs, metrics, failure clips) to object
  storage; a results DB holds exactly one authoritative row per Run
  key — retries write to staging and a finalize step promotes
  atomically. Failure clustering by signature (stack trace / violated
  criterion) so 40k failures triage into 12 bugs.
- **Numbers to volunteer:** 50k–200k scenarios per nightly regression;
  1–10 min per scenario → 10k+ core-hours/night; log retention is the
  cost bomb — keep full artifacts for failures, sampled artifacts for
  passes, TTL everything else.
- **Follow-ups they will push:** What breaks first at 10×? (Scheduler
  throughput and asset-fetch bandwidth, not worker CPU — pre-stage
  scenario assets to node-local cache.) How do you prove a failure is
  real and not infra flake? (Automatic single retry on a different
  node; flake-rate per node tracked and drained.) Sim-vs-real gap?
  (That's evaluation methodology: scenario coverage metrics +
  correlation of sim pass rates with track results.)

### Design B — Drive-log ingestion, indexing & replay (have this cold)

The other half of Data & Compute (REPORTED, DesignGurus/FastPrep):
*a fleet produces terabytes per drive; engineers must find one event
in a million hours and replay it.*

- **Ingest:** vehicles/depots upload chunked, checksummed, resumable
  (multipart to object storage); an ingest manifest per drive (vehicle,
  time range, sensor set, software version) lands in a metadata DB.
  Raw logs are immutable; everything downstream is derived and
  rebuildable.
- **Indexing pipeline:** stream/batch jobs scan new logs and extract
  an **event index** — hard braking, disengagements, near-miss
  triggers, sensor dropouts, plus cheap signals (speed, location,
  weather tags). Index rows point to (log, time-window) — the log
  itself stays in cold storage. This is a feature-store shape: offline
  extraction, online lookup, versioned extractors, backfills when an
  extractor improves.
- **Query & replay:** engineers query by event type/time/geo/stack
  version → the replay service fetches just the needed windows
  (byte-range reads), and streams them into open-loop replay or scene
  reconstruction (the Neural Sim angle: render from novel poses when
  the tested system departs from the recorded path).
- **Tradeoffs to name:** index granularity (per-second vs per-event)
  vs extraction cost; hot tier for the last N days vs cold archive;
  privacy/retention per customer contract; backfill priority vs fresh
  ingest when compute is contended.
- **Your bridge line:** "This is the same architecture as a search
  index with a very expensive document — you never scan the corpus,
  you build the inverted index once and serve windows." (Coupang
  retrieval instincts, autonomy corpus.)

### Design backups — know the shape, 5 minutes each

- **Job scheduler** (REPORTED, LandTheLab; possibly retired):
  cron + DAG dependencies, retries with backoff, exactly-once vs
  at-least-once, worker leases, backfill semantics. If drawn, reuse
  Design A's scheduler vocabulary.
- **Duplicate-file finder, metadata only** (REPORTED onsite,
  Screna): group by size → hash *metadata-preserving* fingerprints
  (inode sets expose hard links for free) → partial-content-free
  disambiguation is impossible in general — the scored insight is
  defining "duplicate" operationally (same size + same hash of first/
  last blocks if reads allowed; if truly metadata-only, report
  *candidates* with a confidence story). Traversal: iterative stack,
  visited-inode set against symlink loops, permission errors logged
  not fatal, memory-bounded external sort at scale.
- **Off-road autonomous vehicle** (REPORTED, DesignGurus): decompose
  perception (lidar/camera/radar fusion) → localization without lane
  markings or GPS → route + local planning → control; then pivot to
  the part that is actually Applied: how you *validate* it — scenario
  library for the terrain, log replay, sim regression gates. The
  validation half is where this company lives; spend your minutes
  there.
- **Transactional KV store as a design** (REPORTED onsite, Screna):
  the screen question grown up — single-node delta-stack semantics
  (your Nov 6 drill) extended to sharding, replication, and what
  nested transactions even mean once a transaction spans shards
  (they mostly don't — say so, and design the boundary).

## Priority 2 — The 2-hour build: a shipping exercise, not a coding test

You are building **your Design A/B** (or whatever the design round
produced) as a working prototype, with any AI model and frameworks
(OFFICIAL). The panel demo afterwards grades decisions, not diff size.
Run it like a staff engineer with a hard deadline:

**Minute 0–15 — scope ruthlessly, in writing.**
- Restate the design in 3 lines; circle the **smallest end-to-end
  slice** that demonstrates the core idea (for Design A: submit a run
  → scheduler places it → worker executes a stub simulation →
  authoritative result stored and queryable). Everything else is a
  named stub behind a real interface.
- Write the demo script *first*: the exact commands/outputs the panel
  will see. Build backwards from it.
- Open a `NOTES.md` and keep a running decision log — every tradeoff,
  every cut, every "with more time I would…". The demo explicitly asks
  for that list; writing it live means you never scramble for it.

**Minute 15–90 — build in vertical slices, run after each.**
- Skeleton + storage first (in-memory or SQLite is fine — say why),
  then one full request path, then the second feature (fair-share
  admission, checkpoint/resume, event index — whichever is your
  design's signature move).
- Use the AI like a fast junior pair: small prompts, review every
  line before it lands, run tests after each slice. OFFICIAL principle
  to embody: engineers own every line that ships. If the AI writes
  something you can't explain, rewrite it — the panel *will* ask.
- Checkpoint working states (git commits or saved copies) so a bad
  refactor at minute 100 never costs you the demo.

**Minute 90–115 — harden the demo path.**
- Freeze features. Re-run the demo script end to end twice. Add the
  one failure case that shows judgment (kill a worker mid-run → lease
  expires → another worker resumes from checkpoint).
- Prepare the 60-second "what I'd do differently" list from NOTES.md:
  real persistence, auth, horizontal scheduler scaling, the
  determinism tax — with the *order* you'd do them in and why.

**Minute 115–120 — breathe.** Demo from the script, not from memory.

**Pre-build your environment this weekend (do not improvise on site):**
- Your AI tool of choice logged in and warm on the machine you'll use
  (confirm with Sophia whether it's your laptop or a provided one —
  ask when the schedule email arrives).
- A practiced toy scaffold in Python: job queue + worker loop + result
  store + tiny CLI/API. If you have run the Design A slice once at
  home in ~90 minutes, the onsite build is a variation, not a cold
  start. One timed mock is the highest-value prep item on this page.
- Boilerplate at your fingertips: `argparse`/FastAPI skeleton, SQLite
  schema setup, a lease/heartbeat loop, a fair-share round-robin —
  the Data & Compute shapes.

**Demo delivery:** narrate as *decisions*, not features — "I made the
Run key the idempotency boundary, which is what buys one authoritative
result; the cost is…". Show the failure case unprompted. End with the
differently-list and the production roadmap in priority order. That
arc — scope, ship, defend, extend — is the staff signal the format was
built to surface.

## Priority 3 — Domain deep-dive: Data & Compute, your home turf

If a deep-dive round appears, expect Sergey's team to probe how you
think about *their* platform problems (INFERRED from the org + the
reported question set). Probable probes and your angles:

- **"Simulation results don't reproduce. Debug the platform."** —
  layered: nondeterminism sources (seeds, floating-point order,
  unpinned assets/builds, wall-clock dependencies), then the platform
  answer: content-addressed assets, hermetic run manifests, replay
  tooling that diffs two runs' manifests before diffing outputs. Your
  skew-audit discipline from ranking transfers 1:1.
- **"Engineers say search over logs is too slow / scenarios are stale."**
  — platform-as-product: your customers are internal teams; their top
  pain is the roadmap. Index freshness SLAs, extractor backfill
  policy, cost per query surfaced to the team that caused it.
- **"How do you evaluate an evaluation platform?"** — coverage metrics
  (scenario space vs real-world event distribution), sim-real
  correlation tracking, flake rate, time-from-code-change to
  trustworthy regression verdict. The platform's metric is other
  teams' velocity *and* the verdict's trustworthiness — both, or
  neither counts.
- **Dana / agents angle** — if they raise the agentic platform:
  agents operating data curation → simulation → evaluation is an
  orchestration + guardrails problem: tool APIs with idempotent
  effects, eval gates between stages, full lineage of agent actions.
  Your agent-design prep applies directly; keep it concrete and
  cost-aware.

**Numbers to have cold before Monday** (from your own work — no new
research, just rehearsal): corpus/index size, peak QPS, p99 latency
budget and its split, offline→online metric deltas from one flagship
project, infra cost per 1k queries/runs if you know it. Five numbers,
memorized, deployable in any round. See [Metrics discipline](#/snorkel)
— same drill, different company.

## Priority 4 — If a standalone coding round appears (classic fork)

Compressed insurance only — the screen already proved raw coding, so
an onsite coding round would reuse the same reported family. Keep
these warm at "can implement cleanly in 30–40 min, narrated" level;
the full drills from the Nov 6 page are summarized here.

**Transactional KV store (still the signature question — reported for
onsite too).** Delta stack with tombstones: one dict per open
transaction, `None` = deletion; lookups walk the stack top-down then
the base; commit merges one layer down (tombstones propagate);
rollback pops. Volunteer the edge cases first: GET after inner-txn
delete, commit with no active transaction, nested commit order, SET→
DELETE→SET in one txn. Follow-ups: `COUNT(value)` via per-layer
value-count deltas; the undo-log alternative and why you didn't pick
it. (Full reference implementation was on the Nov 6 version of this
page — re-derive it once this weekend, don't re-read it.)

**The rest of the reported set (FastPrep/Screna, Nov 2026):**

- **Resolve variable equations with dependency errors** — parse
  `a = b + 1` lines in any order; evaluate via DFS + memo over the
  dependency graph; cycles and undefined variables reported per
  variable, not fatal to the whole map.
- **Compilation order / topological sort** — Kahn's or DFS post-order;
  state the cycle answer (no valid order → return the cycle) before
  coding.
- **Parse nested message types / TLV reassembly** — length-prefixed
  frames arriving fragmented and out of order; buffer per stream,
  emit complete messages in order; malformed-length handling is the
  scored edge.
- **Hash map with separate chaining** — implement, don't import:
  hash, bucket list, resize at load factor; narrate collision and
  worst-case defenses.
- **Ring buffer** — fixed array + head/tail + count (or one-empty-slot
  convention — pick one and say why); overwrite-oldest variant.
- **File-backed Game of Life** — grid too big for memory: stream
  row-triples from disk, write the next generation row by row; the
  point is the I/O pattern, not the rules.
- **Multi-source BFS grid** — total distance to all marked cells,
  unreachable → −1; visited-at-enqueue.
- **Mini interpreter** — lexer → parser (AST) → evaluator for a small
  expression language; if it appears, scope-print statements first.

House rules if this round is live and human-led (OFFICIAL guide):
no generative AI, clarify ~2 min, brainstorm approaches out loud,
defensive debugging as you go, tests if time. Done beats perfect.

## Project deep-dive emphasis

LandTheLab's reconstruction includes a **30-min project presentation**
— present what you built in the onsite, *or a prepared past project*
(REPORTED). Prepare one past project to present cold, in case the
slot is yours to fill:

- **Pick:** the Coupang generative-retrieval / ranking platform work —
  closest in shape to Data & Compute (corpus, index, serving, eval).
- **Arc (30 min):** problem and stakes (2) → architecture with the
  data path drawn (8) → the two hardest decisions and what you
  rejected (8) → failure story and what it changed (5) → metrics,
  before/after, with your five numbers (4) → what you'd rebuild today
  (3). Leave air for interruptions — deep-dives grade the follow-ups,
  not the monologue.
- **Pre-answer the Applied-flavored follow-ups:** How did you know the
  offline win was real? (skew discipline) · What broke at 10×? · Where
  did the platform end and the model begin? · Who were your customers
  and how did you prioritize them?

## Behavioral — the career-history round

Applied's behavioral is not a STAR sampler. REPORTED shape: a
**career-history deep dive** — with the tech lead or HM, walking your
backstory chronologically (one candidate: "starting from late high
school"), probing *why you made each decision*, what you liked and
disliked at each stop, and whether the through-line fits this
company's culture. A separate fit thread runs through the whole day —
interviewers push back to see composure (REPORTED).

**Prepare the narrative, not anecdotes:**

- **Chronology with decision points:** SJTU → NYU → Pinterest search
  discovery → Meta recommendations → Coupang search ranking (Senior
  Staff). At each transition: what you were optimizing for, what you
  learned that the previous stop couldn't teach, what you'd do
  differently. Gaps or pivots get one honest sentence each — no
  defensiveness; they're probing judgment, not loyalty.
- **The "why Applied, why now" answer (3 sentences, rehearsed):**
  the product is an evaluation machine for autonomy; your career is
  building evaluation-and-ranking machines for search; Data & Compute
  is where those two become the same job — plus the honest pull of
  physical-world stakes after a decade of digital ranking.
- **Map stories to their stated values** (REPORTED): *Move fast, move
  safe* — a ship-fast story with the guardrail you built first.
  *Never disappoint the customer* — a platform story where an internal
  team's deadline outranked your roadmap. *Raise the quality bar* —
  a time you blocked a launch/regression and were right. *Ownership* —
  a failure that was yours, fixed, and institutionalized.
- **Questions they ask that are really fit tests:** "What did you
  dislike about each role?" (answer with scope/craft frustrations,
  never people) · "Why leave Coupang now?" (pull toward Applied's
  problem, not push away from Coupang) · "How do you handle being
  told your design is wrong?" (the panel demo is the live version of
  this — stay curious, concede points with data).

## Questions to ask (onsite edition)

For the Data & Compute engineers / Sergey if he joins:
1. What does Data & Compute own today vs. what the autonomy teams
   still run themselves — and where is that boundary moving?
2. Where does simulation compute hurt most right now: scheduling,
   asset/data movement, or result triage?
3. How is Dana changing what the platform team builds — are agents
   now a primary *user* of the data platform?
4. What would the first 90 days of this role own?

For Sophia (logistics, ask when the schedule arrives — don't wait
for Monday):
1. Exact round list + interviewer names for Dec 7?
2. Build round: my laptop or a provided machine? Which AI tools are
   pre-provisioned, and can I use my own accounts?
3. NDA — records show it unsigned; can you resend so it's done
   before the onsite?
4. Check-in: building entrance, parking, arrival time?

## Practice questions

- [ ] Timed mock #1 (the big one): 45-min design of the distributed
  simulation platform, out loud → 2-hour build of its core slice with
  AI → 30-min demo to an empty room, recorded. Full onsite in one
  sitting, this weekend.
- [ ] Design A cold-recall: draw the simulation platform from memory
  in 5 min; recite the Run key, the checkpoint story, and the 10×
  answer without notes.
- [ ] Design B cold-recall: log ingestion → event index → replay
  windows; state the three tradeoffs unprompted.
- [ ] Build scaffold run: job queue + worker lease/heartbeat + result
  store + demo script, from your own boilerplate, ≤ 90 min.
- [ ] Decision-log habit: redo the mock's NOTES.md from memory —
  every cut and tradeoff, in demo order.
- [ ] KV store re-derive from blank (no peeking), ≤ 25 min, with
  `count(value)` and the edge-case list spoken first.
- [ ] Variable-equations evaluator: DFS + memo, cycle and undefined
  handling, ≤ 30 min narrated.
- [ ] One more coding family member cold: hash map with chaining OR
  TLV reassembly — your weaker one — ≤ 35 min.
- [ ] Career-history walk, out loud, ≤ 12 min: every transition with
  its decision reason; no rambling, no defensiveness.
- [ ] "Why Applied Intuition" in 3 sentences; "why leave Coupang" in
  2; "what I disliked at each stop" without naming people.
- [ ] Past-project presentation (Coupang retrieval/ranking), 30 min
  with the clock visible; then answer the 4 Applied-flavored
  follow-ups out loud.
- [ ] Five numbers memorized: corpus size, peak QPS, p99 split, one
  flagship before/after delta, one cost figure.
- [ ] Values mapping: one story each for move-fast-move-safe,
  never-disappoint-the-customer, raise-the-quality-bar, ownership —
  3 minutes each, timed.
- [ ] Demo-day logistics rehearsed: environment warm (AI tool logged
  in), boilerplate repo local, NOTES.md template ready.
- [ ] Re-read the OFFICIAL blog post once, Sunday night:
  https://www.appliedintuition.com/engineering-blog/hiring-engineers-age-of-agents

## Checklist — weekend before & day of (Mon Dec 7, onsite 1:00 PM)

**By Sunday night (Dec 6)**
- [ ] Sophia's schedule email received and checked against this page;
  any surprise round (standalone coding? second design?) gets a
  focused hour, not a panic.
- [ ] NDA status resolved — signed, or a direct ask to Sophia sent.
  (Still unsigned in every record as of Nov 18.)
- [ ] Full mock done (Practice #1); build environment verified on the
  machine you'll actually use; AI accounts logged in.
- [ ] Career narrative + project presentation each rehearsed once,
  out loud, timed.
- [ ] Route planned: Cupertino → 860 W California Ave, Sunnyvale —
  ~20 min; target arrival 12:30 PM for a 1:00 PM start.

**Monday (Dec 7)**
- [ ] Gym 8:00–9:30 as usual; light lunch by ~11:45 (the day runs
  1:00–5:00 with no real break — eat like it).
- [ ] Photo ID, laptop + charger (if BYO confirmed), water bottle,
  a snack for the build block.
- [ ] Leave by ~12:10 PM; check in by 12:30; use the wait to re-read
  your design-A one-pager, not your phone.
- [ ] During the build: NOTES.md open from minute 0; commit/save a
  working state before any refactor; demo script written before
  code.
- [ ] Close the day: thank-you specifics noted (names, the design
  problem, one panel comment) while they're fresh — they feed the
  follow-up email the same evening.
