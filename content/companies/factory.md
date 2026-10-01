---
title: "Factory — Machine Learning Engineer"
slug: "factory"
section: "companies"
nav_order: 40
nav_label: "Factory"
tags: ["agents", "ai-coding", "system-design", "deep-dive", "interviewing", "behavioral"]
updated: "2026-10-01"
company: "Factory"
priority: "p0"
status: "interviewing"
process_sources:
  - { label: "INFERRED", url: "", accessed: "2026-10-01", note: "No public interview-process info found for Factory (factory.ai). Rui's intro call was 2026-09-30 with Gabriel Remar; next rounds relayed as debug + AI coding. Sierra's official AI-native interview format (sierra.ai/blog/the-ai-native-interview) used as LIKELY analogue — same category (AI coding agents), similar evaluation philosophy" }
  - { label: "OFFICIAL", url: "https://sierra.ai/blog/the-ai-native-interview", accessed: "2026-10-01", note: "Analogue only (not Factory's process): Sierra's AI-native onsite = Plan → Build (2h, any AI tools) → Review; debugging interview (improve a draft PR with coding agents); agency and judgment as the graded traits" }
  - { label: "REPORTED", url: "https://techfundingnews.com/factory-jumps-to-5b-in-5-months-with-200m-for-its-ai-droids/", accessed: "2026-10-01", note: "Factory raised $200M at $5B (Sept 2026, per WSJ via TFN); Droids #1 on Terminal-Bench; Factory Router cuts token spend >60%; customers include NVIDIA, Adobe, EY, MongoDB" }
---

## TL;DR

**No public interview-process information exists for Factory** — this page is
built from what Rui learned directly plus the closest verified analogue.
What you know:

- **Intro call done:** 2026-09-30 with Gabriel Remar. Relayed intel: headcount
  ~40/200, ~$1M in options, 5-day SFO RTO.
- **Next rounds (relayed by recruiter): debug + AI coding.**
- **LIKELY format** (analogue: Sierra's official AI-native interview, same
  category): a **debugging round** (review/improve a draft PR in a medium-sized
  codebase *with* coding agents) and an **AI coding/build round** (2-hour build
  with any AI tools, then demo + debate technical choices). Graded traits in
  the analogue: **agency** (pivot when stuck) and **judgment** (scoping,
  tradeoffs).
- The company's bet — "Droids" autonomous coding agents for the enterprise,
  $200M at $5B (Sept 2026) — means they are hiring people who are **fluent
  with agents and opinionated about how software gets built**.

:::warn
Factory's actual process is unverified. The debug + AI-coding shape comes from
your recruiter relay; the detailed format below is a LIKELY analogue from
Sierra's published AI-native interview. Confirm the format with Gabe before
each round.
:::

## Company & product

Factory (founded 2023 by Matan Grinberg and Eno Reyes) builds **"Droids"** —
autonomous AI coding agents for the enterprise: not autocomplete, but agents
that write, test, review, document, deploy, and handle incident response
across the SDLC. Positioning: LLM-agnostic, IDE-agnostic, deployable in cloud,
on-prem, or air-gapped environments. Enterprise customers include NVIDIA,
Adobe, EY, MongoDB, Palo Alto Networks, Bayer, Zapier. Proof points they cite:
#1 on Terminal-Bench; **Factory Router** (auto-assigns the right model per task,
cuts token spend >60%); "Agent Effectiveness" (measuring enterprise AI-spend
ROI).

Trajectory: $50M Series B (Sept 2025) → $150M at $1.5B (April 2026, Khosla-led)
→ **$200M at $5B (Sept 2026)** — tripling in five months. First COO hired Sept
2026 (investor-turned-operator Francesca LaBianca) — the "moving from invention
to scale" signal.

## Role expectations

MLE at Factory, INFERRED from the product and the relayed rounds:

- **Agent fluency as a first-class skill:** you will be evaluated *working
  with* coding agents, not just writing code. Steering, verifying, and
  debugging agent output is the job.
- **Debugging judgment:** the debug round tests whether you can take a draft
  PR / buggy system and improve it with agents — triage, root-cause, and
  knowing when to trust vs. verify the agent.
- **Systems thinking about the SDLC:** Droids span testing, review, docs,
  deployment, incident response — expect breadth across the development
  lifecycle, not just model code.
- **Enterprise grounding:** regulated/air-gapped deployments, eval of agent
  effectiveness, unit economics (token spend) — the business is selling to
  Fortune 500 engineering orgs.

Your edge: multi-turn conversational agent experience (the recruiter-note
credential line used in outreach) plus deep ML systems background — you can
talk agent *evaluation* (reliability, pass^k-style thinking from the τ-bench
world) with unusual authority for an MLE candidate.

## Interview process

### Completed — Intro call (2026-09-30, Gabriel Remar) [REPORTED BY RUI]

Covered: headcount ~40/200, ~$1M options, 5-day SFO RTO. Next: debug + AI
coding rounds.

### Upcoming — Debug round [LIKELY, format from Sierra analogue]

Sierra's published debugging interview (the closest verified analogue):
**review and improve a draft PR in a medium-sized codebase, with coding agents
available** [OFFICIAL — Sierra's format, used here as analogue]. If Factory's
version rhymes:

- You'll get a repo + a draft PR (or a buggy feature) and agent tooling.
- Graded on: triage speed, root-cause reasoning, quality of the improvement,
  and **how you use the agent** (delegation vs. abdication).
- Prep: practice a 90-min session — clone an unfamiliar repo, run its tests,
  fix a real bug *with* Claude Code/Cursor, narrate your verification steps.

### Upcoming — AI coding / build round [LIKELY, format from Sierra analogue]

Sierra's AI-native onsite = **Plan** (ideate the product in your domain) →
**Build** (2 hours, any AI tools, interviewer steps out) → **Review** (demo,
then debate product flows and technical choices: data model, abstractions,
extensibility, path to production, how AI was used) [OFFICIAL — Sierra's
format, analogue]. Graded: **agency** (pivot when stuck) and **judgment**
(scoping) [OFFICIAL — Sierra's rubric, analogue].

If Factory's version rhymes, expect: a scoped build task, 1–2 hours with full
agent tooling, then a review where they debate your *choices* — data model,
abstractions, what you'd do with a week. The review is where seniority shows:
anyone can generate code; few can defend the architecture.

### Possible — HM / values [INFERRED]

Standard closing: motivation, why Factory, operating in a 40→200-person
hypergrowth environment, 5-day RTO alignment.

## Priority topics

1. **Coding-agent fluency:** prompting, steering, verifying, and debugging
   agent output — practice *with* the tools, on screen, narrating.
2. **Debugging methodology:** reproduce → isolate → hypothesize → fix →
   regression-test; reading unfamiliar codebases fast.
3. **Agent evaluation:** reliability metrics (pass^k-style thinking — see the
   Sierra page), Terminal-Bench-style evals, measuring "Agent Effectiveness"
   (their product term — have an opinion on what it should measure).
4. **LLM systems:** inference economics ($/token — Factory Router's whole pitch
   is cutting token spend 60%), model routing, eval harnesses.
5. **SDLC breadth:** testing, code review, CI/CD, incident response, docs —
   the Droids surface area; be conversant in all of it.
6. **Enterprise deployment:** on-prem/air-gapped constraints, security review
   posture, model-agnostic architecture (why it matters when Claude is down —
   Grinberg's own sales pitch).
7. **System design (likely):** agent orchestration, tool-use architectures,
   eval pipelines.

## Company-specific themes

- **"Paving the roads":** Factory's thesis is that agents are only as effective
  as the infrastructure behind them (docs, test coverage, CI/CD) — the product
  is the *foundation*, not just the agent. Echo this framing.
- **Model-agnosticism as strategy:** dynamic routing across Claude/GPT/Gemini/
  DeepSeek — resilience *and* cost. Factory Router is the concrete artifact.
- **Agent-native development:** "the most substantive shift since the move to
  the cloud" (Grinberg) — have a genuine opinion on what changes in how
  engineering orgs operate.
- **Enterprise wedge:** regulated industries, air-gapped deployments, measuring
  AI-spend ROI — this is where they win vs. Cursor/Copilot.

## Likely system-design domains

REPRESENTATIVE PRACTICE (not reported as asked — do not claim otherwise):

1. Design an agent-effectiveness evaluation platform: what to measure, how to
   attribute value, how to run it continuously across an enterprise codebase.
2. Design a model router: task classification, cost/quality tradeoffs, fallback
   when a provider is down.
3. Design a multi-agent coding system: decomposition, verification, merge
   semantics, human-in-the-loop gates.
4. Design eval-driven agent development: harnesses, regression gates, pass^k-
   style reliability metrics.
5. Design incident-response automation: detection → triage → mitigation with
   agent assistance and safety rails.

## Project deep-dive emphasis

- **Your conversational-agent work** is the lead story: multi-turn agents,
  tool use, evaluation, reliability — map it directly onto Droids.
- **Eval thinking is your differentiator:** most candidates can demo agent
  usage; few can design the *measurement* of agent quality. Bring the τ-bench
  / pass^k framing (Sierra page) as shared vocabulary.
- One story of debugging a complex system under time pressure (the debug
  round's behavioral shadow).

Full prep: [#/project-deep-dive](#/project-deep-dive).

## Recent work worth knowing

1. **$200M at $5B valuation** (Sept 2026; WSJ via techfundingnews) — tripling
   in five months; Khosla, Blackstone, Sequoia; angels incl. Marc Benioff:
   [techfundingnews](https://techfundingnews.com/factory-jumps-to-5b-in-5-months-with-200m-for-its-ai-droids/)
2. **$150M Series C at $1.5B** (April 2026, Khosla-led) + Droids launch,
   #1 Terminal-Bench claim:
   [techfundingnews](https://techfundingnews.com/factory-ai-150m-series-c-unicorn-ai-agents-developers/)
3. **First COO** (Francesca LaBianca, ex-Mantis VC investor) — Sept 2026
   scale-up signal:
   [ainvest](https://www.ainvest.com/news/factory-names-investor-coo-real-story-ai-coding-2609/)

## Practice questions

All REPRESENTATIVE PRACTICE — inferred from the relayed rounds and the
AI-native interview analogue, not claimed as asked.

**Debug round prep (do these hands-on, with an agent, narrating):**
- [ ] Clone an unfamiliar mid-size repo. Get tests green, find and fix a real
      bug with Claude Code/Cursor — time-boxed 90 min, narrate every
      verification step.
- [ ] Given a draft PR with a subtle concurrency bug: write the review
      comments you'd leave, then implement the fix with agent assistance.
- [ ] An agent-generated refactor broke 12 tests. Triage: which failures are
      real regressions vs. brittle tests? Decide what to keep.

**AI coding / build prep:**
- [ ] 2-hour build: a small eval harness for a coding agent (run tasks, score
      outcomes, report pass^k-style reliability). Then defend: data model,
      abstractions, path to production.
- [ ] Build a model-router prototype: given a task description, pick the
      cheapest model likely to succeed; defend the routing policy.

**Discussion / deep-dive:**
- [ ] How would you measure "Agent Effectiveness" for an enterprise customer?
      Define the metric, the counterfactual, the gaming risks.
- [ ] When should an agent ask the human vs. act autonomously? Design the
      escalation policy for a deploy agent.
- [ ] Your Droids fleet's token spend doubled this month. Debug the cost —
      hypotheses in priority order.
- [ ] Design the eval gate that blocks a bad agent version from reaching
      customers. What breaks in the harness itself?

## 30-minute checklist

- [ ] **Confirm format (5 min):** ask Gabe what the debug and AI-coding rounds
      actually look like (repo provided? which agent tools? time-box?).
- [ ] **Agent reps (15 min):** one timed 60-min fix-a-bug-with-Claude-Code
      session, narrating verification out loud — the single highest-leverage
      prep for both relayed rounds.
- [ ] **Opinions (10 min):** write 3 sentences each on: agent effectiveness
      measurement, model-agnostic routing, what "agent-native development"
      changes about eng orgs.
- [ ] Skim the Sierra page in this repo — its AI-native format is your best
      verified window into how these rounds are graded.
