---
artifact_id: Analista-TASK-0312-supervisor-park-revive-r2-verdict
task_id: TASK-0312
reviewer: Analista
role: independent adversarial checker (maker != checker)
iteration: r2 (remediation-1 re-review)
verdict: CHANGE-REQUIRED
created: 2026-08-02T19:35:00+02:00
---

# Analista verdict r2 -- TASK-0312 supervisor park-revive remediation (front Zeus-protocol)

Voice: Analista, independent adversarial checker. I do not implement, promote, close or ratify.
This verdict gates the closure of TASK-0312.

## Verdict: CHANGE-REQUIRED

The r1 SLIP is genuinely CLOSED: the supervisor idle-park no longer writes the persistent `.stop`
marker, so an idle-parked agent AUTO-REVIVES on queued work without a human reenable, and OFF->AUTO
auto-revives too. The core (event-driven, sandbox/allowlist, off-by-default, #4 hub intact) stays
GREEN. BUT the remediation's own semantic change (dropping the idle `.stop` write) EXPOSES a NEW,
falsifiable escape in the SAME sovereignty guarantee the task exists to protect (AC4 /
DECISION-0108): an operator STOP issued while the agent is ALREADY idle-parked is a silent no-op --
it returns `already-dormant`, writes NO `.stop`, and the supervisor then AUTO-REVIVES the agent on
the next queued work. The operator's sovereign stop does not stick. Reproduced on the real server
below. By the same logic that gated r1 (automation must not silently override operator/loop intent),
this gates closure.

## Canonical anchor (no hot tree)
- Protocol hub HEAD: 74aad88 (validate exit 0, encoding exit 0, neutrality exit 0, drift false).
- Product repo: D:/Agentes/Zeus/Zeus-protocol, remediation commit
  97c359e14ad41ef506b9d198ad47a761cbdc82c7 (on origin/main); pre-fix baseline
  a51c09912864bf3ad003db83e44d061b5555b884.
- Clean clone under scratch root: D:/Aegis_Scratch/Zp/r0312r2 (checkout 97c359e, tree clean).
- Baseline clone: D:/Aegis_Scratch/Zp/base0312 (checkout a51c099, NEW test file overlaid on OLD
  server.js to prove the shipped test is not tautological).
- Hub #4 config SHA-256: 2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354
  (unchanged; matches the pinned fondo intocable). Product commit 97c359e touches only
  src/server.js and tests/staticContract.test.js -- no hub artifact, config, genesis, registry or
  state.

## Reproduction (exit codes)
- Clean clone + checkout 97c359e: tree clean; node --check src/server.js OK; node --check tests OK.
- npm install (clean clone): INSTALL_EXIT=0.
- npm test (clean clone, 97c359e): TEST_EXIT=0 -- tests 143, pass 123, fail 0, skipped 20 (slow
  tier). Matches the handoff (123/20/0).
- New live-cycle test in isolation @97c359e: `node --test --test-name-pattern="transient parks
  auto-revive"` -> tests 1, pass 1, fail 0, skipped 0, EXIT 0 (it really RUNS, not skipped).
- Negative baseline (NEW test file overlaid on OLD a51c099 server.js): same pattern -> tests 1,
  FAIL 1, EXIT 1. The remediation test is not tautological; it distinguishes pre-fix from post-fix.
- Hub gates at HEAD 74aad88: validate_collaboration_state.py exit 0; scan_encoding.py exit 0;
  scan_domain_neutrality.py exit 0; protocol_state_drift has_drift = false.

## What IS fixed -- verified by my own adversarial harness (real server child, real fs events)
I drove the real 97c359e src/server.js (ZEUS_RUNTIME_SUPERVISOR_ENABLED=1, IDLE_MS=800) against a
temp protocol root, with a real alive runtime (powershell Start-Sleep child, live pid at pidPath):

```
PHASE_A idle-park no .stop: true | auto-revived: true | new pid: true (pid1=55884 pid2=8764)
PHASE_C op-stop-while-alive action: stopped | .stop written: true | stays blocked (no revive): true
```

- PHASE_A: the idle-threshold park kills the process and writes NO `.stop`; when I inject queued
  work the supervisor relaunches it with a FRESH pid, no human reenable. The r1 defect is gone.
- PHASE_C: an operator stop against an ALIVE agent still writes the persistent `.stop`
  (`operator-front`) and the supervisor stays blocked on the next work (decision
  `operator-stop-marker`) until reenable. Operator sovereignty preserved in this path.

## The NEW escape, proven (PHASE_B, same harness)
```
PHASE_B parked before op-stop: true | .stop before: false | op-stop action: already-dormant
        | .stop written by op-stop: false
PHASE_B ESCAPE -> agent revived after operator stop: true | blocked-decision present: false
VERDICT_B operator-stop-on-parked STICKS (down): false | ESCAPE(revived despite operator stop): true
```

Sequence: agent idle-parks (dormant, no `.stop`) -> operator issues STOP -> the runtime is not
alive, so `applyRuntimeControlAction` early-returns `already-dormant` and NEVER writes `.stop`
(src/server.js:1660-1661, before the `operator-front` write at 1664) -> I inject queued work ->
the supervisor sees no `.stop`, `demanded` true, runtime down -> it AUTO-REVIVES the agent. No
`blocked` decision is ever recorded. The operator's explicit stop silently failed to establish the
durable block that DECISION-0108 / AC4b promise ("an operator stop must require a human reenable").

Root cause: the persistent operator block is written ONLY on the live-kill branch of the operator
stop; the "already dormant" branch returns success without arming the block. Pre-fix this was
harmless because an idle-parked agent ALREADY carried a `.stop` (written by the old idle-park), so
operator-stop-on-parked was redundant. The remediation removed that idle `.stop` write (correctly,
to fix r1) and thereby turned operator-stop-on-parked into a silent no-op. This is squarely within
the blast radius of the change under review, not an unrelated pre-existing bug.

Why the shipped remediation test misses it: the new live-cycle test only issues the operator stop
while the agent is ALIVE (it revives first, then stops). It never exercises operator-stop against an
already-parked runtime -- the exact analogue of why the r1 test missed the r1 SLIP.

Realistic impact (supervisor enabled): the supervisor parks idle agents on its own schedule; an
operator who clicks STOP on an agent that happens to be parked at that instant gets `ok`, believes
it is durably stopped, and the supervisor silently revives it on the next mailbox message or ready
task. The operator has no reliable way to keep an agent down while the supervisor runs.

## Vector-by-vector

| Vector | Criterion | Result |
|--------|-----------|--------|
| Clean clone gate | npm test exit 0 @97c359e | PASS (143/123/0/20) |
| New test runs (not skipped) | live-cycle test executes @97c359e | PASS (1/1/0/0) |
| Negative baseline | new test on old a51c099 server FAILS | PASS (fails, exit 1 -> not tautological) |
| AC1 revive after supervisor idle-park | idle-park -> work -> AUTO-REVIVE (fresh pid), no reenable | PASS (PHASE_A; server.js:1715-1725 stopEntry no `.stop`) |
| AC2 idle shutdown | no work > threshold -> park (AUTO only, no queued work) | PASS (parkIfIdle server.js:1722-1725) |
| AC2 -> AC1 automation loop | sleep-when-idle then revive-on-demand (DECISION-0057) | PASS (loop closed) |
| AC4 override OFF then AUTO | OFF parks without `.stop`; OFF->AUTO auto-revives | PASS (server.js:1738 stopEntry, no `.stop`) |
| AC4 operator stop sovereign (agent ALIVE) | `.stop` written, blocks until reenable | PASS (PHASE_C; server.js:1664, 1754 blocked) |
| AC4 operator stop sovereign (agent PARKED) | operator stop must establish durable block | SLIP (no-op; no `.stop`; auto-revives -- server.js:1660-1661) |
| AC3 sandbox / allowlist / no-shell / uno-y-solo-uno | unchanged from r1 | PASS (not touched by 97c359e) |
| AC4b reenable | unlink `.stop`; present `.stop` blocks manual start (409) | PASS (server.js:1633-1637, 1643-1644) |
| AC5 backoff + cap | exponential backoff, maxRetries cap | PASS (server.js:1756-1770) |
| AC7 off-by-default | flag != 1 -> inert; control 403 | PASS |
| AC7 fondo intocable | #4 hub byte-identico; drift 0 | PASS (config SHA unchanged; product touches only 2 product files) |
| Cost: no clock-poll in vacuum | no work -> no evaluate | PASS (watchers persistent:false; evaluate only on fs event/startup/control) |

## Declared residuals / secondary observations (non-blocking, distinct from the SLIP)
- OFF override is an in-memory (session) pause, not persisted across a server restart; this matches
  the ACTION directive ("OFF como pausa auto-revivible"). The DURABLE operator block is the `.stop`
  marker via the stop button. Flagged so the operator/UI distinction is explicit; non-blocking.
- Narrow TOCTOU in parkIfIdle: it re-checks queuedAgents() before killing, but if work arrives
  between that check and the terminate, evaluate may record "keep" for a process the park then
  kills, leaving the agent down until the next fs event. Strictly better than pre-fix; non-blocking.
- Hung-but-alive still not detected (r1 residual persists): a live pid with a frozen heartbeat is
  treated as "alive"; staleAfterMs/ageMs are computed but never enforced. Outside AC5; non-blocking.

## Closure recommendation: CHANGE-REQUIRED
The r1 SLIP is closed and the core is green, but a confirmed, falsifiable NEW escape defeats the
operator-stop sovereignty guarantee (AC4 / DECISION-0108) under a realistic timing, and it is a
direct consequence of the change under review. Default-to-not-closable is not even needed here --
it is reproduced.

## Expected fix loop (bounded)
- Remediation (maker owns the design): the operator STOP must establish the durable block even when
  the agent is already dormant/parked -- i.e., write the persistent operator `.stop` (or an
  equivalent operator-authored durable marker) regardless of live-pid, so a stop always requires a
  human reenable. Preserve the r1 fix (supervisor idle-park / OFF park must remain a transient,
  auto-revivable state that writes no operator `.stop`). Keep the two markers distinct: transient
  supervisor park (no durable block) vs durable operator stop (needs reenable).
- Affected gates: npm test (clean clone, exit 0) PLUS a NEW permanent test that exercises
  operator-stop-WHILE-PARKED: alive -> idle-park -> operator STOP -> work queued -> STAYS BLOCKED
  (decision operator-stop-marker) until reenable; the test must FAIL against 97c359e and PASS after
  the fix. Do not regress the r1 live-cycle test (idle-park auto-revive; OFF->AUTO auto-revive).
- Re-judgement: I re-run this adversarial harness (all three phases) plus the clean-clone gate and
  the negative baseline before any closing commit.
- Iteration budget: this is remediation-1 rejected. Per the bounded loop, ONE more remediation
  iteration is permitted; if the operator-stop-on-parked hole is not closed cleanly in that next
  delivery, escalate to the human owner rather than open a further loop.

-- Analista
