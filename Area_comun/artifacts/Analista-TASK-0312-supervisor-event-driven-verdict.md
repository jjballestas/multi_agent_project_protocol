---
artifact_id: Analista-TASK-0312-supervisor-event-driven-verdict
task_id: TASK-0312
reviewer: Analista
role: independent adversarial checker (maker != checker)
verdict: CHANGE-REQUIRED
created: 2026-08-02T18:29:00+02:00
---

# Analista verdict -- TASK-0312 supervisor event-driven de runtimes (front Zeus-protocol)

Voice: Analista, independent adversarial checker. I do not implement, promote, close or ratify.
This verdict gates the closure of TASK-0312.

## Verdict: CHANGE-REQUIRED

The event-driven model, the sandbox/allowlist, the off-by-default posture, the backoff and the
#4-hub-intact background are all VERIFIED GREEN. BUT the supervisor's own idle-shutdown (AC2, the
cost core) writes the SAME persistent `.stop` fail-safe marker used by the operator stop, and that
marker then PERMANENTLY BLOCKS the supervisor's own auto-revive (AC1) and the 0107 manual start.
After the supervisor puts an idle agent to sleep, it will NOT wake it for queued work -- only a
human `reenable` restores it. This breaks the revive<->sleep automation loop (DECISION-0057 / the
AC1<->AC2 cycle) that is the entire purpose of this task. Proven falsifiably below.

## Canonical anchor (no hot tree)
- Protocol hub HEAD: 359943a (validate exit 0, encoding 0, neutrality 0, drift 0).
- Product repo: D:/Agentes/Zeus/Zeus-protocol, commit a51c09912864bf3ad003db83e44d061b5555b884.
- Clean clone under scratch root: D:/Aegis_Scratch/Zp/r0312 (checked out a51c099, tree clean).
- Hub #4 config SHA-256: 2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354 (unchanged;
  matches the pinned fondo intocable and the handoff). Product commit a51c099 touches only
  public/app.js, src/server.js, tests/staticContract.test.js -- no hub artifact, config, genesis,
  registry or state.

## Reproduction (exit codes)
- Clean clone + checkout a51c099: tree clean.
- node --check src/server.js -> OK; node --check public/app.js -> OK.
- npm install: INSTALL_EXIT=0.
- npm test (clean clone): TEST_EXIT=0 -- tests 142, pass 122, fail 0, skipped 20 (slow tier).
  Matches the handoff (142/122/20/0).
- Hub gates at HEAD 359943a: validate_collaboration_state.py exit 0; scan_encoding.py exit 0;
  scan_domain_neutrality.py exit 0.

## The defect, proven (adversarial harness, real server child, real fs events)
I drove the real `src/server.js` with ZEUS_RUNTIME_SUPERVISOR_ENABLED=1 and IDLE_MS=1200 against a
temp protocol root, made agent "Codex" alive (a live pid recorded at the allowlist pidPath), let
the idle threshold fire, then injected real queued work while the runtime was down:

```
STEP2  after idle: stop marker present: true
       .stop content: "2026-08-02T16:...Z supervisor idle-threshold"   <- supervisor wrote the marker
STEP2b runtime down (sleeper killed): true                             <- production: stopEntry taskkill
STEP3  Codex decisions: [{action:"blocked",reason:"operator-stop-marker"} x3]  <- work queued + runtime down
VERDICT .stop-written-by-idle: true | after-work blocked: true | after-work relaunched: false
```

Root cause in src/server.js:
- stopEntry() (idle-threshold AND operator OFF) writes the persistent `.stop` marker unconditionally
  before taskkill: `writeFile(entry.stopPath, "... supervisor <reason>")` (server.js:1712).
- The auto-revive path treats ANY `.stop` as a hard stop: if work is demanded and the runtime is
  down, `if (await pathExists(entry.stopPath)) { record(..., "blocked", "operator-stop-marker");
  continue; }` (server.js:1742-1745) -- it never launches.
- The 0107 manual start button is blocked identically: `if (await pathExists(entry.stopPath)) throw
  new ClientError(409, "operator stop override is active")` (server.js:1643).
- Only `reenable` unlinks `.stop` (server.js:1634), and reenable is an explicit, confirm-gated,
  off-by-default HUMAN action (AC4b) -- not automatic.

Consequence: the supervisor can idle-park an agent exactly ONCE; thereafter it silently refuses to
wake it for queued work until a human clicks reenable. The same marker sharing also breaks the
AC4 override cycle: OFF (which also calls stopEntry -> writes `.stop`) followed by AUTO does NOT
auto-revive on demand either. The idle-park (transient cost action) inherits the operator
fail-safe's "stick until a human intervenes" semantics.

Why the shipped test suite misses it: the TASK-0312 test (tests/staticContract.test.js:1856) never
exercises the idle-stop -> work-arrives -> revive cycle with a live runtime. Its fixture runtime is
never actually alive (the allowlisted script is absent -> "start-failed: allowlisted runtime script
is unavailable"), so stopEntry's `.stop` write on idle is never reached, and the `.stop` block is
only tested for the operator path (manual start 409). The AC1<->AC2 loop is untested.

## Vector-by-vector

| Vector | Criterion | Result |
|--------|-----------|--------|
| Clean clone gate | npm test exit 0 @a51c099 | PASS (142/122/20/0) |
| AC1 event-driven (structure) | watch() on mailbox/state; no setInterval work loop; only one-shot setTimeout for idle | PASS (server.js:1762-1778; test asserts doesNotMatch setInterval) |
| AC1 wake-on-event (cold agent) | work event -> evaluate -> launch attempt | PASS (fs event fires evaluate; launch attempted when no `.stop`) |
| AC1 revive after supervisor idle-stop | work queued + runtime down (idle-parked) -> launch | SLIP (blocked by supervisor's own `.stop`; never relaunches) |
| AC2 idle shutdown | no work > threshold -> stop | PASS in isolation (idle timer fires stopEntry) |
| AC2 -> AC1 automation loop | sleep-when-idle then revive-on-demand (DECISION-0057) | SLIP (loop broken; one-shot per agent, then needs human reenable) |
| AC3 sandbox: unknown agent | rejected | PASS (400; server.js:1802 / test:1890) |
| AC3 sandbox: arbitrary fields (command/path/args) | rejected | PASS (400 via assertAllowedKeys; server.js:1786 / test:1892) |
| AC3 no shell | fixed powershell + fixed script, shell:false | PASS (server.js:1649-1654) |
| AC3 uno-y-solo-uno | never duplicates a live runtime | PASS (already-alive duplicatePrevented; server.js:1640-1641) |
| AC4 override OFF/ON | OFF never launched, ON always live | PASS-with-caveat (OFF writes `.stop`; OFF->AUTO won't auto-revive -- same root defect) |
| AC4 stop global sovereign | stop-supervisor ceases all management | PASS (globallyStopped; evaluate early-return; server.js:1718,1790-1794) |
| AC4b reenable | unlink `.stop`; `.stop` present blocks manual start | PASS (server.js:1633-1637; 409 test:1900-1904) |
| AC5 backoff + cap | exponential backoff, maxRetries cap, no infinite restart | PASS (server.js:1746-1758; test:1888) |
| AC6 observability | per-agent mode, last event, decision log with reason | PASS (contract; status()/loadRuntimeControlStates; server.js:1601-1607,1782-1784) |
| AC7 off-by-default | flag != 1 -> inert; control 403 | PASS (server.js:1763,1787; test:1866) |
| AC7 fondo intocable | #4 hub byte-identico; core neutral; drift 0 | PASS (config SHA unchanged; product touches only 3 product files) |
| Cost: no clock-poll in vacuum | no work -> no evaluate, no token burn | PASS (evaluate only on fs event/startup/control; watchers persistent:false) |

## Declared residuals / secondary observations (non-blocking)
- Hung-but-alive not detected: runtimeControlState reports status = pid?alive:dormant and computes
  staleAfterMs/ageMs but never uses them, so a runtime with a live pid but a frozen heartbeat is
  treated as "alive" -> supervisor records "keep" and never restarts it. Arguably outside AC5
  (which targets start failures), so declared as residual, not a blocker.
- `.stop` markers already encode authorship in content ("supervisor idle-threshold" vs
  "operator-front"), but the launch guards never read the content to distinguish them. This is the
  natural seam for the fix (see remediation).

## Closure recommendation: CHANGE-REQUIRED

The primary defect is a genuine functional failure of AC1 in the dominant down-reason and of the
AC1<->AC2 automation loop that is the point of the task. Default-to-not-closable is not even
needed here -- it is reproduced.

## Expected fix loop (bounded)
- Remediation (maker owns the design): stop conflating the operator fail-safe stop with the
  supervisor's transient idle-park. Options: (a) do NOT write the persistent operator `.stop` for a
  supervisor idle-park/OFF-park -- use an in-memory or clearly-supervisor-authored transient marker;
  or (b) have the auto-revive path clear a SUPERVISOR-authored `.stop` (distinguished by content)
  when fresh demand arrives, while preserving the operator's `.stop` fail-safe untouched. Preserve
  AC4b: an operator stop must still require a human reenable.
- Affected gates: npm test (clean clone, exit 0) PLUS a NEW permanent test that exercises the full
  cycle with a live runtime: alive -> idle-stop -> work queued -> AUTO-REVIVE succeeds; and the
  operator-stop path still blocks until reenable; and OFF -> AUTO auto-revives on demand.
- Re-judgement: I re-run this adversarial harness plus the clean-clone gate before any closing
  commit. Maximum 2 iterations; if unresolved after 2, escalate to the human owner.

-- Analista
