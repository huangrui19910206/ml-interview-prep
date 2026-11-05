---
title: "Applied Intuition — Coding Round (Fri 2026-11-06, Martin Meinke)"
slug: "applied-intuition"
section: "companies"
nav_order: 84
nav_label: "Applied Intuition"
tags: ["coding", "debugging", "python", "coderpad", "interviewing"]
updated: "2026-11-04"
company: "Applied Intuition"
priority: "p0"
status: "interviewing"
process_sources:
  - { label: "OFFICIAL", url: "https://applied.co/technical-interview", accessed: "2026-11-04", note: "Applied's own technical-interview guide: exercises are hand-selected per candidate background; mix of coding, system design, debugging; ML domain expertise tested if relevant. Rubric = collaborative ability (clarify ~2 min, brainstorm multiple approaches, talk continuously) + fast & performant code (speed matters, defensive coding, done > perfect) + code design & elegance (readability, testable code, unit tests if time, comments as notes-to-self). Coding interviews: NO generative AI; Google/search allowed only with screen shared. Non-coding interviews: no outside resources at all." }
  - { label: "OFFICIAL", url: "https://www.appliedintuition.com/engineering-blog/hiring-engineers-age-of-agents", accessed: "2026-11-04", note: "Applied engineering blog (Jul 2026), 'Hiring engineers for the age of agents': 'Keep our technical phone screen as is — a 45-minute coding task with no AI' (accountability: engineers own every line). Onsite redesigned: 45-min system design on a real Applied problem, then 2 hours to build a working prototype with any AI model, then a panel demo/walkthrough." }
  - { label: "OFFICIAL", url: "", accessed: "2026-11-04", note: "Beatrice Wang (Recruiting Coordinator) emails Nov 3-4, 2026: coding round Fri Nov 6, 10:15-11:00 AM PT with Martin Meinke; CoderPad https://app.coderpad.io/FXXNHNN7; Google Meet https://meet.google.com/tbb-kzgc-eny; Python is Rui's language. Nick Gutierrez sent the official technical-interview guide link. resource.applied.co/initial-interview is access-code gated (code interview157, from Beatrice's email) — fetch returned 401, content not read; open it yourself in a browser." }
  - { label: "REPORTED", url: "https://www.1point3acres.com/bbs/thread-1187656-1-1.html", accessed: "2026-11-04", note: "1point3acres, Aug 2026, Applied Intuition technical phone screen (在职跳槽, outcome Fail): opened with a background/experience chat, then the question was the TRANSACTIONAL KEY-VALUE STORE — the post notes it is the same question other 面经 had reported. The candidate had read the 面经 beforehand and still failed; the deciding details are points-gated (>188) and were not readable." }
  - { label: "REPORTED", url: "https://www.interviewquery.com/guides/applied-intuition-inc-software-engineer", accessed: "2026-11-04", note: "InterviewQuery guide: coding screen 45-60 min on CoderPad, LeetCode medium-to-hard, strong emphasis on finishing quickly and correctly. Reported problems: graph question, interval variant, Sudoku, Minesweeper, lane-merger algorithm, O(1) data structure for top-K logs; applied variants: parsing nested JSON from an API (max-velocity and range follow-ups), decoding a CAN frame, debugging existing code." }
  - { label: "REPORTED", url: "https://www.designgurus.io/answers/detail/what-is-the-applied-intuition-interview-process-like-round-by-round", accessed: "2026-11-04", note: "DesignGurus round-by-round (aggregator): phone screen 45-60 min CoderPad, one medium/hard problem with a practical angle; candidates for MACHINE LEARNING roles report a debugging task instead — fix a broken PyTorch script within 45 minutes. Also reports no AI coding assistants allowed in live rounds." }
  - { label: "REPORTED", url: "https://www.jointaro.com/interviews/companies/applied-intuition/experiences/embedded-software-engineer-canada-september-24-2025-no-offer-positive-47e3be3e/", accessed: "2026-11-04", note: "Taro candidate report, Sep 2025 (Embedded SWE, Canada): technical screen 45 min CoderPad — a fairly simple question; interviewer focused on DEBUGGING and CODE QUALITY over puzzle difficulty." }
  - { label: "REPORTED", url: "https://www.screna.ai/interview-questions/applied-intuition", accessed: "2026-11-04", note: "Screna (aggregator) corroborates the signature question: build an in-memory key-value store supporting SET, GET, DELETE and nested transactions with COMMIT and ROLLBACK semantics; also lists a multi-source-BFS grid problem variant." }
---

## TL;DR

**Status: HM round passed (Sergey Andreev, Head of Data & Compute).
Next: Coding round — Fri 2026-11-06, 10:15–11:00 AM PT, Martin Meinke,
CoderPad + Google Meet. Python. No AI tools.**

This is Applied's kept-as-is technical screen: **45 minutes, one exercise,
no generative AI** (OFFICIAL engineering blog). Exercises are
**hand-selected for your background** (OFFICIAL guide), so plan for three
possible formats, in this priority order:

1. **Transactional key-value store** — the signature Applied screen
   question, reported repeatedly (一亩三分地 + aggregators). Highest
   single-item probability. Drill it until the design is muscle memory.
2. **ML debugging variant** — ML candidates report fixing a broken
   PyTorch script in 45 min (REPORTED). Your background makes this a
   live possibility.
3. **Practical implementation** — nested-JSON/telemetry parsing or a
   data-structure design (REPORTED set: intervals, top-K logs, graph).

Whatever the format, the OFFICIAL rubric is the same: clarify first,
brainstorm approaches out loud, write fast clean code, debug defensively,
leave tests. A 一亩三分地 candidate who *knew the KV question in advance*
still failed — this round grades execution and communication, not recall.

:::warn
Applied's NDA (Ashby/HelloSign, sent Nov 2) is still unsigned in every
record — sign it before Friday if you haven't. Also Friday is a double:
Sequen's Ethan Benjamin interview is the same day at 1:00 PM PT. Pace
the morning accordingly.
:::

## Company & product

Applied Intuition builds the software toolchain autonomy programs run
on: high-fidelity simulation, scenario libraries, sensor models, and the
data infrastructure to validate vehicle intelligence at scale —
customers across automotive, trucking, defense, and off-road. Closed a
$600M Series F at a ~$15B valuation in June 2025 (REPORTED).

**Your mapping:** Sergey's org is **Data & Compute** — the platform that
feeds simulation and validation. That is ML platform / data infra at
scale, your home turf (multi-stage ranking pipelines, large-scale
retrieval, eval). If asked "why Applied": the product is an evaluation
machine for autonomy; your career is building evaluation-and-ranking
machines for search. Same discipline, higher stakes per decision.

## Interview process

| # | Round | Format | Status / source |
|---|-------|--------|-----------------|
| R0 | Recruiter chain — Rich Adao referral → Andy Goff → Nick Gutierrez (sourcer), Beatrice Wang (coordination) | Email | ✅ Done |
| R1 | Hiring-manager — Sergey Andreev, Head of Data & Compute | Video | ✅ Passed (confirmed Nov 2) |
| R2 | **Coding round — Martin Meinke** | **45 min, CoderPad + Meet, Python, no AI** | **Fri Nov 6, 10:15 AM PT — this page** |
| R3+ | Onsite / super day | 45-min system design (real Applied problem) → 2-hour build of that design, **AI allowed** → panel demo (OFFICIAL blog); further coding/behavioral rounds REPORTED | Later |

## The OFFICIAL rubric — how this round is actually scored

From Applied's own technical-interview guide. Three categories:

**Collaborative ability**
- **Understand the prompt.** Take ~2 minutes to ask questions and
  clarify assumptions *before* coding. This is explicitly scored.
- **Brainstorm multiple approaches.** Name 2–3 approaches with
  tradeoffs, then pick — don't silently start with the first idea.
- **Collaborate.** Narrate continuously; the interviewer is a sounding
  board, and hints only exist if they can see your thinking.

**Fast and performant code**
- **Speed matters** — fluency in your language is itself a signal.
- **Defensive coding** — debug as you go, not in a panic at the end.
- **Get to a solution** — done beats perfect; if you ship the simpler
  version, say the tradeoff and sketch the optimal one verbally.

**Code design and elegance**
- Readability: descriptive names, right level of abstraction.
- Testable code; write unit tests if time permits.
- Leave comments as notes-to-self where production code would do more
  (error handling, validation) — it shows judgment without burning time.

**Rules:** coding interviews ban generative AI outright. Google/search
is allowed **only with your screen shared**. Keep the desktop clean and
the CoderPad tab front and center.

## Drill 1 — Transactional key-value store (top priority)

**The reported spec** (一亩三分地 Aug 2026; corroborated by Screna):
an in-memory KV store with `SET / GET / DELETE` plus **nested
transactions**: `BEGIN` starts a transaction (transactions can nest),
`COMMIT` applies the innermost transaction's changes to its parent (or
to the store), `ROLLBACK` discards them. Reads inside a transaction see
that transaction's own writes and deletes.

**The design to have cold — delta stack with tombstones.** One dict per
open transaction; `None` marks a deletion. Lookups walk the stack from
the top down, then the base store. Commit merges one layer down;
rollback just pops. Every operation is O(depth) worst case, O(1) for
the common shallow case — say that, and note depth is small in
practice.

:::collapse Reference implementation — study it, don't memorize it
```python
class TransactionalKV:
    def __init__(self):
        self.store = {}   # committed data
        self.txns = []    # stack of per-transaction deltas; None = tombstone

    def get(self, key):
        for layer in reversed(self.txns):
            if key in layer:
                return layer[key]          # may be None -> deleted
        return self.store.get(key)

    def set(self, key, value):
        if self.txns:
            self.txns[-1][key] = value
        else:
            self.store[key] = value

    def delete(self, key):
        if self.txns:
            self.txns[-1][key] = None     # tombstone
        else:
            self.store.pop(key, None)

    def begin(self):
        self.txns.append({})

    def commit(self):
        if not self.txns:
            raise ValueError("no active transaction")
        top = self.txns.pop()
        for k, v in top.items():
            if self.txns:
                self.txns[-1][k] = v       # tombstones propagate down
            elif v is None:
                self.store.pop(k, None)
            else:
                self.store[k] = v

    def rollback(self):
        if not self.txns:
            raise ValueError("no active transaction")
        self.txns.pop()
```
:::

**Edge cases to volunteer before he asks** (this is where the round is
won): GET of a key deleted in an inner txn but present in the base;
COMMIT with no active transaction (error vs no-op — ask); nested
commit order (inner merges into parent layer, *not* straight to base);
SET then DELETE then SET again inside one txn; ROLLBACK of the
outermost txn leaves the base untouched.

**Likely follow-ups:** `COUNT(value)` — how many keys currently hold a
value (naive: scan the merged view, O(n); better: maintain per-layer
value-count deltas alongside the key deltas — same stack trick);
thread safety (one lock vs per-key); persistence (WAL/snapshot —
verbal only).

**The alternative design to mention in brainstorm:** single dict +
undo log (record inverse ops, rollback replays them). Simpler reads,
messier nested commits. Naming both, then picking the delta stack, is
exactly the "brainstorm multiple approaches" rubric item.

**Drill protocol (30 min, timed, out loud):** implement from a blank
CoderPad → run the scripted sequence (set a=1; begin; set a=2; begin;
delete a; get a → None; rollback; get a → 2; commit; get a → 2) →
add `count(value)` → narrate complexity. Repeat until it fits in
~20 minutes; the real round leaves room for the follow-up.

## Drill 2 — PyTorch debugging variant (ML background = live risk)

REPORTED for ML roles: **a broken PyTorch script, 45 minutes, make it
run / train correctly.** The format rewards a calm method more than
speed: state your hypothesis → isolate (one variable at a time) →
minimal fix → rerun. Narrate every step; silent staring is the failure
mode. Full method on the [Debugging](#/debugging) page.

:::collapse Bug categories to drill — INFERRED targets (standard failure modes, not leaked answers)
- `optimizer.zero_grad()` missing → gradients accumulate, loss plateaus
  or explodes.
- `model.eval()` forgotten at validation → dropout/BatchNorm make eval
  numbers noisy and non-reproducible.
- Loss reduction: `sum` where `mean` is intended → loss scales with
  batch size; or reduction over the wrong dimension.
- In-place ops on tensors needed for backward (`x += ...`, in-place
  ReLU) → autograd runtime error.
- Device mismatch: batch on CPU, model on CUDA (or vice versa).
- Dtype: labels not `long` for `CrossEntropyLoss`; inputs `double`
  vs model `float`.
- Missing `torch.no_grad()` in inference → memory growth / OOM.
- Silent broadcasting: `[B, 1]` vs `[B]` comparisons producing wrong
  metrics instead of an error.
- `scheduler.step()` called per-batch when it's per-epoch (or the
  reverse).
- Data-side: label off-by-one, transform applied in the wrong order,
  train stats (mean/std) computed including the validation split.
:::

**Drill (25 min):** take any small training loop, plant 3 bugs from
different categories above, then debug it cold and out loud. Practice
the sentence pattern: "Loss is doing X, which suggests Y — I'll check
Z first."

## Drill 3 — Practical implementation set (REPORTED)

Secondary reported problems, in rough priority for a Python/ML seat:

- **Nested JSON parsing** — parse nested telemetry/API records, then
  follow-ups like max velocity over a window and range queries. Drill:
  recursive vs iterative traversal, defensive `.get()` on missing keys,
  streaming vs load-all tradeoff.
- **Top-K logs data structure** — "O(1)-flavored" retrieval of the
  most frequent/recent entries: hash map + `heapq`, or `Counter` +
  `most_common`; be ready to discuss the true complexity honestly.
- **Interval variant** — sort by start, sweep, merge; `bisect` for
  insertion queries.
- **Graph / BFS** — multi-source BFS on a grid (one Screna-listed
  variant: minimize total distance to all marked cells, unreachable
  → −1). `collections.deque`, visited-at-enqueue.
- Sudoku / Minesweeper appear in generic SWE reports — know the shape
  (backtracking with constraint sets; grid reveal with BFS flood fill)
  but don't spend Thursday night here.

**CoderPad Python kit — have it cold, no autocomplete:** `dict` /
`collections.defaultdict`, `Counter`, `deque`, `heapq`, `bisect`,
`sorted(key=...)`, `enumerate`, `zip`, recursion limits, f-strings.
Set CoderPad to Python before the problem starts.

## Pacing — 45 minutes (10:15 start, hard stop 11:00)

| Clock | Move |
|-------|------|
| 0:00–0:03 | Background chat (REPORTED opener): 60-second Coupang summary ready, end with the Data & Compute mapping |
| 0:03–0:06 | Clarify: inputs, scale, edge cases, transaction semantics if KV — *graded, don't skip* |
| 0:06–0:09 | Brainstorm 2 approaches + tradeoffs, pick one, say why |
| 0:09–0:32 | Implement the core; defensive-debug as you go |
| 0:32–0:41 | Run tests: the examples given + your volunteered edge cases |
| 0:41–0:45 | Complexity, production notes (comments), follow-up variant, your questions |

If the problem is going long: say the tradeoff and ship the working
subset. "Done is better than perfect" is their printed rubric, not a
consolation prize.

## Questions to ask Martin

1. Which team are you on, and what does it own — simulation, data
   platform, or tooling?
2. What would the first project for this role look like on the Data &
   Compute side?
3. How is the codebase split between C++ and Python day to day?
4. What do the remaining rounds look like, and what's the timeline?

## Practice questions

- [ ] Transactional KV store from blank — full drill above, timed,
  narrated, ≤ 25 min including `count(value)`.
- [ ] KV follow-up answers out loud: nested commit order, tombstone
  semantics, undo-log vs delta-stack tradeoff.
- [ ] Plant-and-debug: PyTorch training loop with 3 planted bugs,
  fixed cold in ≤ 20 min, hypothesis-first narration.
- [ ] State `zero_grad` / `train()` vs `eval()` / loss-reduction /
  device-dtype checks as a 60-second mental checklist.
- [ ] Nested JSON: parse nested telemetry records; compute max
  velocity in a time window; answer a range query — narrated.
- [ ] Top-K frequent with `heapq` — plus an honest complexity answer.
- [ ] Interval merge + one `bisect` insertion variant — timed.
- [ ] Multi-source BFS on a grid — narrated, visited-at-enqueue.
- [ ] 60-second background opener: Coupang search ranking → Data &
  Compute mapping, no rambling.
- [ ] "Why Applied Intuition" in 3 sentences (evaluation machine for
  autonomy ↔ ranking/evaluation at Coupang).
- [ ] Complexity statements for every drill, unprompted: time, space,
  and the one tradeoff you'd revisit with more time.
- [ ] Skim the OFFICIAL guide once more tonight:
  https://applied.co/technical-interview — and open the gated
  candidate page https://resource.applied.co/initial-interview
  (access code: interview157) in your own browser.

## Checklist — night before & morning (Fri Nov 6, interview 10:15 AM)

**Thursday night**
- [ ] NDA signed (Ashby/HelloSign, sent Nov 2) — verify completion.
- [ ] KV drill + PyTorch debug drill done once each, timed.
- [ ] CoderPad link opens: https://app.coderpad.io/FXXNHNN7 — set
  language to Python.
- [ ] Meet link bookmarked: https://meet.google.com/tbb-kzgc-eny
- [ ] Desktop clean for screen share; AI assistants closed (banned in
  this round — Google only, screen shared).

**Friday morning**
- [ ] Gym 8:00–9:30 as usual; at your desk by 10:00, CoderPad open.
- [ ] Water, quiet room, camera/mic check on Meet by 10:05.
- [ ] Paper next to you: KV design sketch (delta stack + tombstone)
  and the PyTorch 60-second debug checklist.
- [ ] One warm-up: re-run the KV scripted test sequence mentally.
- [ ] Remember the double-header: Sequen at 1:00 PM — light lunch
  after 11:00, don't spend the gap re-litigating this round.
