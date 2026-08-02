---
artifact: Analista-TASK-0312-operator-stop-parked-r3-verdict
task_id: TASK-0312
reviewer: Analista
role: adversarial-checker
verdict: OK-CLOSABLE
iteration: r3-FINAL
created: 2026-08-02T17:47:00Z
local_time: 2026-08-02 19:47 CEST (UTC+2)
---

# Analista verdict -- TASK-0312 r3 (FINAL): operator-stop-while-parked remediation

## Verdict: OK-CLOSABLE

The remediation-2 closes the PHASE_B escape (operator STOP against a parked/dormant runtime now
arms the durable `.stop` marker before the dormant early-return, so queued work stays blocked
until explicit re-enable), with no regression of PHASE_A (idle auto-revive) or PHASE_C
(stop-while-alive), no confirmed new escape, and the #4 hub byte-identical. Two non-blocking
residuals declared below.

## Canonical anchor (never a hot working tree)

- Product repo: D:/Agentes/Zeus/Zeus-protocol -- commit `ff02135` (== origin/main). Fix on `97c359e`.
- Hub HEAD (protocol): `12c3de9`.
- Review executed in a CLEAN CLONE checked out at `ff02135`
  (D:/Aegis_Scratch/zeus/0312r3), gated by EXIT CODE, not in-place.
- Product commit `ff02135` touches ONLY `src/server.js` (+6/-3) and `tests/staticContract.test.js`
  (+10). It does not touch the hub, the #4 chain, agent_registry, genesis, or any protocol boundary.

## The fix under review (byte-level)

`applyRuntimeControlAction` (src/server.js): the operator STOP now writes the durable `.stop`
marker BEFORE the dormant check, and the early-return happens after the write:

```
  await mkdir(dirname(entry.stopPath), { recursive: true });
  await writeFile(entry.stopPath, `${new Date().toISOString()} operator-front\n`, "utf8");
  if (before.status !== "alive" || !before.pid) {
    return { ok: true, action: "stopped", agentId, alreadyDormant: true };
  }
  await terminateRuntimeProcess(entry, before.pid);
```

At `97c359e` the parked branch early-returned `already-dormant` with `...before` and NEVER wrote
`.stop` -- that was the escape: a subsequent demand event auto-revived the parked agent.

## Reproduction (exit codes)

| Gate | Command | Result |
|------|---------|--------|
| syntax | `node --check src/server.js` / `tests/staticContract.test.js` | OK |
| full suite (clean clone @ff02135) | `npm test` | EXIT 0 -- tests 143, pass 123, fail 0, skipped 20 (slow subprocess tier) |
| r3 live-cycle test ran (not skipped) | grep of test output | `TASK-0312 supervisor transient parks auto-revive while operator stop remains persistent` PASS (8187ms, real server + real PowerShell child + real fs markers) |
| NEGATIVE BASELINE | old server `97c359e` + new test `ff02135`, `node --test --test-name-pattern="transient parks auto-revive"` | EXIT 1 -- fail 1: `alreadyDormant` actual `undefined`, expected `true`. The test genuinely gates the fix. |
| hub validator | `python scripts/validate_collaboration_state.py` | EXIT 0 |
| hub encoding scan | `python scripts/scan_encoding.py` | EXIT 0 |
| hub neutrality scan | `python scripts/scan_domain_neutrality.py` | EXIT 0 |
| hub #4 drift | sha256(protocol.config.json) | `2E35F26E...B354` (byte-identical to pinned; drift nil) |

## Vector-by-vector (the three phases of the live cycle + new-escape hunt)

| Vector | Behavior exercised | PASS / SLIP |
|--------|--------------------|-------------|
| PHASE_A idle-park -> auto-revive (no reenable) | AUTO agent, no demand -> `stop/idle-threshold` (no `.stop`); new mailbox event -> relaunch, `revivedPid != initialPid` | PASS |
| PHASE_B operator-stop-while-PARKED -> blocked until reenable | parked agent -> operator STOP returns `alreadyDormant:true` and writes `.stop`; queued work -> `blocked/operator-stop-marker`, status stays `dormant`; only `reenable` frees it | PASS (the r2 fix; fails at baseline) |
| PHASE_C operator-stop-while-alive -> blocked until reenable | alive agent -> operator STOP writes `.stop` + terminates; queued work -> `blocked/operator-stop-marker` | PASS |
| Marker durability | a 200 STOP response always implies `.stop` written (mkdir/writeFile throw -> action throws, no false success); no supervisor path (idle park, OFF, global stop) unlinks `.stop` -- only `reenable` does | PASS |
| Transient parks never write the marker | idle-threshold park and OFF override terminate the process but leave no `.stop`; AUTO restores revivability | PASS |
| Sandbox / allowlist (inherited 0107) | fixed 3-agent allowlist; unregistered agent, arbitrary command/path/args, control chars, unconfirmed -> rejected server-side | PASS (existing suite green) |
| Event-driven, no clock-poll | supervisor wakes on fs watchers over mailbox/open + TASK_INDEX; no `setInterval` idle loop | PASS |
| Off-by-default + #4 intact | flag off -> supervisor inert; tuning params outside the pinned config; hub config byte-identical | PASS |
| NEW-escape hunt | see residuals -- no path found that defeats the durable-marker guarantee | no confirmed escape |

## Declared residuals (NON-BLOCKING -- do not gate closure)

1. **Theoretical TOCTOU: concurrent operator-stop-while-parked vs a supervisor launch on the same
   event.** If `evaluate` for a demanded dormant agent passes its `pathExists(stopPath)` check
   (false) and, in the same async gap, an operator STOP writes `.stop` and returns (without
   terminating, because its `before` snapshot was dormant), a live child could still be spawned if
   `applyRuntimeControlAction("start")`'s own `pathExists(stopPath)` re-check strictly precedes the
   STOP's `writeFile`. Assessment: (a) NOT a regression -- at `97c359e` the parked-stop wrote no
   marker at all, so r2 is strictly better; (b) the start path's independent `.stop` re-check
   narrows the window to a sub-await interleave; (c) the durable-marker guarantee itself always
   holds -- the anomaly is at most a transient live process, which the supervisor parks on the next
   idle window (no demand) and then blocks. Not deterministically reproducible; documented as
   theoretical, not a confirmed escape. A future hardening could re-assert the marker inside the
   spawn critical section, but it is out of scope for r3.

2. **`reenable` does not itself trigger `evaluate`.** After `reenable` unlinks `.stop`, the runtime
   relaunches on the NEXT filesystem event on mailbox/open or TASK_INDEX, not synchronously on the
   reenable call. In the live-cycle test a fresh mailbox write drives the relaunch. In production,
   with peers actively writing the mailbox, an event is imminent, so AC4b ("tras limpiar + hay
   trabajo -> se lanza") holds in practice. This matches prior (r1/r2) behavior -- not a new
   regression and not a stop-escape; noted as a minor liveness observation.

## Closure recommendation

**OK-CLOSABLE.** PHASE_B is closed with a durable, re-enable-gated marker; PHASE_A and PHASE_C
show no regression; the new test falsifiably gates the fix (green @ff02135, red @97c359e); the full
suite is green in a clean clone; the hub #4 is byte-identical with all hub gates at exit 0. The two
residuals above are non-blocking and explicitly declared. No maker!=checker violation: Codex
implemented, Analista verified independently in a clean clone.

-- Analista (independent adversarial checker)
