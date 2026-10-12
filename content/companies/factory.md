---
title: "Factory — Machine Learning Engineer"
slug: "factory"
section: "companies"
nav_order: 40
nav_label: "Factory"
tags: ["agents", "ai-coding", "system-design", "deep-dive", "interviewing", "behavioral", "debugging"]
updated: "2026-10-11"
company: "Factory"
priority: "p0"
status: "interviewing"
process_sources:
  - { label: "CONFIRMED", url: "", accessed: "2026-10-11", note: "Gabe Remar email 2026-10-11 1:59 PM PT (Cc cathy.nghieu@factory.ai): next round is a 45-min debugging interview — Python or JS (candidate's choice), NO AI assistance, HackerRank with the interviewer sending the link at the start; graded on technical skills, communication, collaboration. Rui to share next-2-weeks availability via Ashby link" }
  - { label: "INFERRED", url: "", accessed: "2026-10-01", note: "No public interview-process info found for Factory (factory.ai). Rui's intro call was 2026-09-30 with Gabriel Remar; next rounds relayed as debug + AI coding. Sierra's official AI-native interview format (sierra.ai/blog/the-ai-native-interview) used as LIKELY analogue for the possible later AI-coding round — same category (AI coding agents), similar evaluation philosophy" }
  - { label: "OFFICIAL", url: "https://sierra.ai/blog/the-ai-native-interview", accessed: "2026-10-01", note: "Analogue only (not Factory's process): Sierra's AI-native onsite = Plan → Build (2h, any AI tools) → Review; debugging interview (improve a draft PR with coding agents); agency and judgment as the graded traits" }
  - { label: "REPORTED", url: "https://techfundingnews.com/factory-jumps-to-5b-in-5-months-with-200m-for-its-ai-droids/", accessed: "2026-10-01", note: "Factory raised $200M at $5B (Sept 2026, per WSJ via TFN); Droids #1 on Terminal-Bench; Factory Router cuts token spend >60%; customers include NVIDIA, Adobe, EY, MongoDB" }
---

## TL;DR

**No public interview-process information exists for Factory** — this page is
built from what Rui learned directly plus the closest verified analogue.
What you know:

- **Intro call done:** 2026-09-30 with Gabriel Remar. Relayed intel: headcount
  ~40/200, ~$1M in options, 5-day SFO RTO.
- **Next round — CONFIRMED 2026-10-11 by Gabe Remar:** a **45-min debugging
  interview**: Python or JS (your choice), **NO AI assistance**, HackerRank
  with the interviewer sending the link at the start. Graded on **technical
  skills, communication, collaboration**. Gabe asked you to share your
  next-2-weeks availability via the Ashby link.
- This contradicts the earlier Sierra-analogue assumption (agents *available*
  in the debug round) — the analogue now applies only to the possible later
  AI-coding round. Prep accordingly: this round is raw debugging, no tools.
- The company's bet — "Droids" autonomous coding agents for the enterprise,
  $200M at $5B (Sept 2026) — means they are hiring people who are **fluent
  with agents and opinionated about how software gets built**.

:::warn
Factory's actual process is unverified. The **45-min no-AI HackerRank debug
format is CONFIRMED by Gabe Remar's 2026-10-11 email** (details below). The
detailed format for any later AI-coding round is still a LIKELY analogue from
Sierra's published AI-native interview — confirm it with Gabe if it comes up.
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
- **Debugging judgment (CONFIRMED round, no AI):** the 45-min HackerRank debug
  round tests raw debugging — triage, root-cause, verification, narrated out
  loud. Agent assistance is explicitly off; "knowing when to trust vs. verify
  the agent" is a company-fit theme, not this round's graded skill.
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

### Upcoming — Debug round [CONFIRMED 2026-10-11, Gabe Remar email]

**Format:** 45 minutes on HackerRank (the interviewer sends the link at the
start). **Python or JS — your choice. NO AI assistance.** Graded on:
**technical skills, communication, collaboration**.

What this means for prep:

- **This is a raw-debugging round, not an agent-fluency round.** The rubric is
  classical: read buggy code fast, locate the bug, fix it, verify. The
  think-aloud methodology in [#/debugging](#/debugging) is exactly the graded
  skill — reproduce → isolate → hypothesize → verify, narrated out loud.
  (Note: the 13 broken programs on that page are ML-focused; the round is
  general Python/JS debugging, so also drill everyday gotchas: off-by-ones,
  aliasing/mutation, async/await races, closure capture, edge-case inputs.)
- **Language choice: pick Python** — it's your daily language and where your
  debugging is fastest. JS only if a round's problems turn out DOM/async-heavy
  and you genuinely prefer it. Decide *before* the round so there's no
  mid-interview waffling.
- **Collaboration is graded:** HackerRank debug rounds often have the
  interviewer watching silently or asking follow-ups. Treat them as a pair —
  narrate hypotheses, ask clarifying questions, verify fixes by running the
  tests, don't shotgun-change three things at once.
- **Communication is graded:** state the symptom precisely, name the
  hypothesis class before testing it, and say the root cause out loud after
  the fix (the interviewer's signal that you actually understood, not just
  pattern-matched).

### Possible — AI coding / build round [previously relayed, format UNCONFIRMED]

The original relay was "debug + AI coding"; the debug round is now confirmed
in the format above. If an AI-coding round follows, the Sierra AI-native
onsite remains the best verified analogue: **Plan** (ideate the product in
your domain) → **Build** (2 hours, any AI tools, interviewer steps out) →
**Review** (demo, then debate product flows and technical choices: data
model, abstractions, extensibility, path to production, how AI was used)
[OFFICIAL — Sierra's format, analogue]. Graded: **agency** (pivot when stuck)
and **judgment** (scoping) [OFFICIAL — Sierra's rubric, analogue].

### Possible — HM / values [INFERRED]

Standard closing: motivation, why Factory, operating in a 40→200-person
hypergrowth environment, 5-day RTO alignment.

## Priority topics

1. **No-AI debugging methodology (THIS ROUND):** reproduce → isolate →
   hypothesize → fix → regression-test, all narrated out loud. Reading
   unfamiliar codebases fast. HackerRank-style reps in **Python** (your daily
   language), time-boxed 20–30 min per bug.
2. **Communication + collaboration (graded in this round):** state symptoms
   precisely, name hypothesis classes before testing, say the root cause out
   loud after the fix; treat the interviewer as a pair, not an audience.
3. **Coding-agent fluency (company fit + possible later AI-coding round):**
   prompting, steering, verifying, and debugging agent output. NOT usable in
   the confirmed debug round — don't practice with tools for *this* one.
4. **Agent evaluation:** reliability metrics (pass^k-style thinking — see the
   Sierra page), Terminal-Bench-style evals, measuring "Agent Effectiveness"
   (their product term — have an opinion on what it should measure).
5. **LLM systems:** inference economics ($/token — Factory Router's whole pitch
   is cutting token spend 60%), model routing, eval harnesses.
6. **SDLC breadth:** testing, code review, CI/CD, incident response, docs —
   the Droids surface area; be conversant in all of it.
7. **Enterprise deployment:** on-prem/air-gapped constraints, security review
   posture, model-agnostic architecture (why it matters when Claude is down —
   Grinberg's own sales pitch).
8. **System design (possible later):** agent orchestration, tool-use architectures,
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

All REPRESENTATIVE PRACTICE for the confirmed debug round — inferred from the
format, not claimed as asked. **Do these WITHOUT AI tools**, mirroring the
round's no-AI rule.

**Debug round prep (Python, no AI, time-boxed, narrating out loud):**
- [ ] HackerRank-style rep: a buggy function + failing tests. 25 min, no AI.
      Narrate: symptom → isolation plan → hypothesis class → cheapest
      discriminating test → fix → re-run. Then say the root cause in one
      sentence.
- [ ] Bug with a silent wrong answer (not a crash): e.g. an off-by-one in a
      sliding window or an aliasing bug where a list is mutated in place.
      These are the ones that separate signal from noise — catch the bug by
      *reading*, then confirm with a minimal repro.
- [ ] Pair-debugging rep: debug while someone (or a voice note to yourself)
      asks follow-ups — practice answering "why do you think that?" without
      breaking your line of thought. This is the collaboration rubric.
- [ ] Work through the [#/debugging](#/debugging) methodology section and
      answer one broken program out loud end-to-end, as if the interviewer is
      watching. (The programs there are ML-flavored; the *narrated method* is
      what transfers.)

**AI coding / build prep (possible later round, analogue only):**
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

- [ ] **Language lock (2 min):** decide Python vs JS now — recommend Python
      (your daily language). No mid-round switching.
- [ ] **No-AI debug reps (20 min):** two time-boxed HackerRank-style bug fixes
      in Python, narrating out loud — methodology + communication in one rep.
      This is the single highest-leverage prep for the confirmed round.
- [ ] **Opinions (8 min):** write 3 sentences each on: agent effectiveness
      measurement, model-agnostic routing, what "agent-native development"
      changes about eng orgs — for the possible AI-coding/deep-dive rounds.
- [ ] Skim the Sierra page in this repo — its AI-native format remains your
      best verified window into how a *later* AI-coding round would be graded.
