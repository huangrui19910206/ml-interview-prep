---
title: "Browserbase — Technical Screen: SWE, Core (Wed 2026-11-04, Daniel Rousso)"
slug: "browserbase"
section: "companies"
nav_order: 87
nav_label: "Browserbase"
tags: ["coding", "infrastructure", "distributed-systems", "browser-automation", "interviewing"]
updated: "2026-11-02"
company: "Browserbase"
priority: "p0"
status: "interviewing"
process_sources:
  - { label: "OFFICIAL", url: "", accessed: "2026-11-02", note: "Invite emails in jobs Gmail: 'Technical Screen', Wed 2026-11-04 10:00-11:00 AM PT (60 min), interviewer Daniel Rousso, role Software Engineer (Core); Zoom link on the calendar event. Recruiter line: Catherine Li (Talent) advanced Rui; scheduling was handled by direct message after her Greenhouse times-request failed to send" }
  - { label: "REPORTED", url: "https://simplify.jobs/p/93658c2b-9c2e-4538-a371-d47fdda75641/Software-Engineer", accessed: "2026-11-02", note: "Browserbase 'Software Engineer - Core Infrastructure' posting: build, operate and grow the Browserbase Core platform - robust, scalable distributed backends with developer-friendly APIs; Firecracker or similar VM-monitor experience named; $180k-$300k/yr; in person five days a week at SF HQ" }
  - { label: "REPORTED", url: "https://www.taskade.com/blog/history-of-browserbase", accessed: "2026-11-02", note: "Third-party company history: founded Jan 2024 by Paul Klein IV; $67.5M raised, $300M valuation after a $40M Series B (Notable Capital, Jun 2025); homepage claims 35M+ browser sessions/month across 10,000 customers; engineering shaped as ~3 infra teams, 1 Stagehand team, 1 Director team" }
  - { label: "SEARCHED - NONE FOUND", url: "", accessed: "2026-11-02", note: "Searches of 1point3acres, InterviewQuery, Glassdoor and Blind-style posts on 2026-11-02 found NO candidate reports of a Browserbase technical screen - results were dominated by BrowserStack (a different company) and unrelated startups. No public profile for Daniel Rousso was found either. Everything below about screen content is inference from the role and product, labelled as such - there is no leaked question to prep for" }
---

## TL;DR

**Status: advanced by Catherine Li (Talent). Next: Technical Screen,
Wed 2026-11-04, 10:00–11:00 AM PT, Daniel Rousso (engineer,
Browserbase), role: Software Engineer (Core). Zoom link is on the
calendar event.**

Be clear-eyed about the evidence: **no public 面经 for this screen
exists** — not on 一亩三分地， not on InterviewQuery, not on Glassdoor.
So this page does not prep a rumored question. It preps the shape that
a 60-minute first technical screen at a small infra startup almost
always takes — live practical coding with an engineer, weighted toward
the systems the team actually runs — and it builds that coding from
Browserbase Core's real problem space: browser-session lifecycle,
capacity, expiry, event streams, rate limits.

**Your mapping (say it in the room):** Core is a high-concurrency
session-serving platform — allocate a scarce resource fast, keep it
warm, reap it when idle, meter it per customer. That is the same
engineering shape as the serving and ranking infrastructure you run at
Coupang (high-QPS allocation under latency budgets), with headless
Chrome sessions instead of ranking requests. The search adjacency is
also real: Browserbase sells web data retrieval for AI agents, which
is your home turf pointed at the open web.

:::warn
**Prep window is tight by design:** Tue Nov 3 belongs to Harvey
(10:00 AM coding). Browserbase prep = one timed drill (below) plus a
30-minute product skim, split across Mon/Tue evening. Gym 8:00–9:30 AM
Wed is protected — be at the desk by 09:50.
:::

## Company & product

Browserbase runs real browsers in the cloud for AI agents. A developer
asks for a browser, gets one in seconds, connects over the Chrome
DevTools Protocol (CDP), and drives it with Playwright, Puppeteer,
Selenium, or Stagehand. Browserbase operates the fleet underneath:
session isolation, proxies and stealth/anti-bot fingerprinting,
CAPTCHA handling, regions, session recording/replay, and a live view a
human can take over. Founded January 2024 in SF by Paul Klein IV;
reported $67.5M raised at a $300M valuation (Series B, June 2025) and
35M+ sessions/month across ~10,000 customers.

- **Core (this role):** the platform itself — session allocation and
  lifecycle, the distributed backends and APIs every other team builds
  on. The Core Infrastructure posting names Firecracker-class VM
  monitors and developer-friendly APIs; sibling platform postings ask
  for Go or TypeScript backends and Postgres.
- **Stagehand:** their open-source AI browser-automation framework —
  natural-language primitives `act` / `extract` / `observe` plus an
  agent mode, on top of Playwright-style page APIs.
- **Director:** a no-code builder on top of Stagehand.

Context you already weighed when you kept this line moving: it is a
generalist SWE (Core) role — not an ML role — at a ~$300M Series B
that works five days a week in-office in SF. The screen will test
general engineering, not ML depth; your seniority has to show through
system judgment, API design, and how you handle lifecycle/concurrency
edge cases out loud.

## The screen — what to expect (INFERENCE, no reports exist)

Most likely shape for the 60 minutes:

1. **~5 min** — intros; expect one question about what you do at
   Coupang and why Browserbase. Have the two-sentence version ready.
2. **~40–45 min** — live coding in a shared editor over Zoom. For an
   infra team this is usually a *practical, possibly staged* problem
   (build the simple version, then add a constraint), not an exotic
   algorithm puzzle. Language: ask — Python is normally acceptable at
   screens even in TS/Go shops, but confirm in the first minute and
   don't burn time if they want TypeScript.
3. **~5–10 min** — your questions for them (staff-level list below).

Failure mode to avoid: treating this like a LeetCode race. At a
~50-person infra startup the signal they want is *would I trust this
person with the session fleet* — narrate lifecycle and failure cases
as you code, keep the code modular, and state complexity once, briefly.

## Targeted practice — the Core problem space

Ranked by how directly they map to what Core operates:

1. **Browser session manager (the drill, below).** Create / get /
   heartbeat / expire sessions with TTL, a hard capacity limit, and
   LRU eviction of idle sessions; expose simple stats. Dict + heap or
   OrderedDict; be able to say what changes under concurrency (one
   lock vs sharded locks vs an event loop).
2. **Rate limiter.** Token bucket and sliding-window variants, keyed
   per API key; return allow/deny plus retry-after. Thirty lines,
   no libraries.
3. **Session event stream processing.** Parse newline-delimited
   events (`session_id, timestamp, type, url, latency_ms`), then
   aggregate: counts by type, p95 latency, top-K domains. Streaming
   with bounded memory — your search-log instincts apply directly.
4. **LRU cache with TTL.** OrderedDict version in under 10 minutes;
   state get/put complexity and the expiry-check strategy (lazy vs
   sweeper).
5. **Retry with backoff + jitter, and a circuit-breaker sketch.**
   Scraping fleets live on this; know the failure vocabulary
   (retryable vs fatal, thundering herd, idempotency keys).
6. **In-memory pub/sub fan-out.** Subscribers per session, slow
   consumer policy (drop vs buffer vs disconnect) — this is the
   Live View / event-streaming shape.
7. **Top-K over sharded counts.** Merge of per-shard counters with a
   heap; home turf, just keep it crisp.

### Clarifying questions to open the coding with (2 minutes)

1. Language and environment — Python OK? Shared editor or my own?
2. Single-process in-memory scope, or should I design for multiple
   replicas from the start?
3. Session semantics: does expiry slide on activity (heartbeat) or is
   TTL fixed at creation?
4. At capacity: reject new sessions, queue them, or evict idle ones?
5. Do I need thread-safety, or is clean single-threaded structure
   enough with the concurrency story told verbally?

### Edge cases that earn the senior signal

- Heartbeat arriving after expiry (session already reaped) — recreate
  or error?
- Eviction choosing a session that is idle-but-connected vs truly
  abandoned.
- Clock handling: inject a clock / pass `now` in; never call wall
  time inside the core logic (testability point, say it out loud).
- Double-release / releasing an unknown session id.
- Stats correctness when evictions and expiries race.

### 60-minute drill (do once before Wed, timed)

Build the session manager in stages:

- 0–10 min: `create_session()` / `get_session()` / `release()` over a
  dict; capacity check.
- 10–25 min: TTL with lazy expiry on access + heartbeat that extends
  TTL; injected clock.
- 25–40 min: capacity pressure — LRU eviction of the idlest session;
  a periodic `reap()` that sweeps expired sessions in O(expired).
- 40–50 min: stats endpoint (active count, created/expired/evicted
  counters); slow-subscriber or rate-limit add-on if time remains.
- 50–60 min: re-read as the interviewer would; name the tests out
  loud: create-to-capacity, evict-idlest, heartbeat-after-expiry,
  double-release, reap correctness.

Plain Python, dicts/heap only, no libraries, no AI tools assumed.

## If it turns conversational: the 10-minute design sketch

"How would you allocate a browser session?" — the Core front door:

API request → auth + per-customer quota/rate limit → scheduler picks
a region → **warm pool** of pre-booted browser processes (Firecracker
microVM snapshots make cold start survivable; pool sizing is a
cost/latency trade-off — say that) → hand back a CDP endpoint →
heartbeat/idle-timeout reaper returns capacity → recordings and logs
stream off the box asynchronously. Failure vocabulary: host loss =
sessions on it die, clients retry with a fresh session (sessions are
ephemeral by design); noisy-neighbor isolation via per-session
containers/VMs; fleet cost dominated by idle capacity, so utilization
metrics drive pool policy. This is inference from the product, not a
reported question — but it is the conversation this team has daily.

## About the interviewer

**Daniel Rousso** — an engineer at Browserbase per the official
invite. Public searches on 2026-11-02 found no profile, talks, or
posts that can be attributed to him reliably (results were other
people with similar names), so nothing about his background is
claimed here. Plan for a Core-team engineer who works on the session
platform day to day: practical, product-adjacent questions will land
better than abstract ones.

## Questions to ask them (pick 3–4)

- What is Core's binding constraint right now — cold-start latency,
  fleet cost per session, or reliability at peak concurrency?
- Firecracker vs containers: where did you land, and what decided it?
- How is the warm pool sized, and who owns that trade-off?
- What does the on-call / incident profile look like for Core?
- How do Core, Stagehand, and Director split roadmap priority?
- What would this role own in its first 90 days?

## Later rounds (GENERIC INFERENCE — nothing reported)

Nothing public describes Browserbase's full loop. The generic shape
for a startup at this stage, to be ready for *if* it materialises: a
deeper coding or debugging round, a system-design round on the
session platform (the sketch above, extended: multi-region, recording
pipeline, quota/billing metering), a Stagehand/product conversation,
and a founder/values conversation. Do not prep these before the
screen reports back.

## Checklist

**Tue Nov 3 (after Harvey, keep it light — 45 min max)**

- [ ] 30-minute product skim: Browserbase homepage + docs concepts
      (Sessions, Contexts, Proxies, Stagehand's act/extract/observe).
- [ ] Read the clarifying questions and edge-case list once.
- [ ] If energy allows: the first 25 minutes of the drill only.

**Wed Nov 4 (morning of)**

- [ ] Gym 8:00–9:30 as usual; desk by 09:50, Zoom link from the
      calendar event tested.
- [ ] Editor sanity: plain Python ready, no autocomplete dependence.
- [ ] Two-sentence Coupang → Browserbase mapping in your head
      (session-serving ≈ high-QPS serving infra; web-data retrieval
      for agents = your search home turf).
- [ ] Remember: this 10:00 slot is the one you chose Wed–Fri over
      Catherine's Tue 1–2 PM offer — no conflicts on the day.
