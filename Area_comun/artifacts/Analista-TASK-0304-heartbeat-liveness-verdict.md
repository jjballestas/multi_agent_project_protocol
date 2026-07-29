# VERDICT -- Analista adversarial review of TASK-0304

Reviewer: Analista (independent adversarial checker)
Task: TASK-0304 -- exec-lease heartbeat must reflect REAL liveness (no self-bump) +
frozen-exec coverage with ProgressFreshSeconds>0
Date (local): 2026-07-29 ~13:05 (UTC+2)
Verdict: **OK-CLOSABLE**

## Canonical anchor
- Protocol HEAD reviewed: `7804dae` (canonical origin/main; the fix `45bed5d` is contained
  in it; delivery flip `f1da7a6`).
- Scope: HUB-ONLY. No Zeus product in scope.
- Clean clone: `D:/Aegis_Scratch/protocol/a304adv`, `git checkout 7804dae`. All gates and
  behavioral vectors were run THERE, gated by EXIT code, never in the hot working tree.

## What the fix does (verified in source)
`Get-ExecProgressState` no longer derives progress from the lease heartbeat. The removed
block computed `heartbeat_fresh` from `Lease.heartbeat_monotonic` (which
`Update-ExecLeaseHeartbeat` bumps to `now` every loop iteration, so it was ALWAYS fresh at
production `ProgressFreshSeconds=15`). Now `progressing = run_log_growing OR ledger_growing`
only -- real output signals. `heartbeat_monotonic` is still WRITTEN (lease liveness marker,
lines 177/189) but is NO LONGER READ by any progress or kill decision (grep-confirmed: zero
other consumers). This satisfies AC1's "retire the heartbeat as a progress signal" option.

## Reproduction (clean clone, exit codes)
```
git checkout 7804dae                                              -> HEAD 7804dae
grep -c heartbeat_fresh scripts/harness/peer_mailbox_cron.ps1     -> 0
python examples/mailbox_retry_cases/run_mailbox_retry_cases.py    -> exit 0 (full suite PASS)
python scripts/validate_collaboration_state.py                    -> exit 0 (OK)
python scripts/scan_encoding.py                                   -> exit 0 (clean)
python scripts/scan_domain_neutrality.py                          -> exit 0
Parser::ParseFile(peer_mailbox_cron.ps1)                          -> 0 errors (PS1_PARSE=OK)
protocol.config.json md5 (HEAD) == md5 (45bed5d^)                 -> e2e3cff1... == e2e3cff1...
protocol_version (epoch)                                          -> 1.14.0 (pinned, unchanged)
protocol_state_drift                                             -> verdict=CLEAN up_to_seq=6698
```
Note: the validator is slow (~29s) and briefly appeared to hang while a background git
maintenance/gc (triggered by fetch/clone) competed for I/O; once that finished it exits 0
deterministically both in-place (cold start) and in the clean clone. Not a state defect.

## Vector-by-vector (PASS / SLIPS)

| # | Vector | Expectation | Result |
|---|--------|-------------|--------|
| AC1 | Heartbeat retired as progress signal | `heartbeat_fresh` gone; progress from run-log/ledger only; heartbeat not consumed elsewhere | PASS |
| AC1 | Frozen exec detected `no_progress` BEFORE hard_cap @FreshSeconds=15 | new case: `EXEC_HUNG reason=no_progress`, no `hard_cap`, `TREE_KILL_COMPLETE`, elapsed<12 | PASS |
| AC2 | New regression case @FreshSeconds>0 exists | `run_frozen_exec_with_production_freshness_case` (FreshSeconds=15) in suite `main()` | PASS |
| AC2 | Falsifiability: re-inject self-bump -> case FAILS | see Mutation A below | PASS (mutant killed, static AND behavioral) |
| AC3 | No regression: 0303 / 0300 / RETRY / delivery green | full suite exit 0 (pre_delivery_and_liveness, complete_tree_kill, post_delivery_timeout, retry/outcome, torn-tail, contracts) | PASS |
| AC3 | De-regression: a PROGRESSING exec (run-log growing) is NOT killed; mutate-to-kill -> 0303 FAILS | see Mutation B below | PASS (guard catches over-correction) |
| AC4 | Scope = 2 routes; config byte-identical; .ps1 syntax valid | net non-ledger paths = the 2 in-scope routes + governance artifacts (task/handoff/Codex memory); config md5 identical; PS1_PARSE=OK | PASS |
| Gate | validate / encoding / neutrality exit 0 | all exit 0 in clean clone | PASS |

**SLIPS found: none.**

## Adversarial falsifiability (the two mutations I was asked to run)

### Mutation A -- re-inject the self-bump (must break AC1/AC2)
Restored `scripts/harness/peer_mailbox_cron.ps1` from `45bed5d^` (the pre-fix version, i.e.
`heartbeat_fresh` back in `Get-ExecProgressState`), kept the fixed test file.
- Result: suite exit 1. First tripwire is a STATIC guard
  `assert "heartbeat_fresh" not in <Get-ExecProgressState source>` -- it kills the exact-revert
  mutant immediately.
- Because the static guard short-circuits before the behavioral body, I did NOT rubber-stamp
  it: I bypassed that assert and re-ran. With the self-bump live, the frozen exec was NOT
  harvested early -- the runner blew past the 15s harness timeout (`subprocess.TimeoutExpired`)
  instead of the baseline `<12s` `no_progress` kill. So the early `no_progress` detection is
  genuinely a BEHAVIORAL consequence of the fix, not just a string check.

### Mutation B -- over-correct: force `progressing = $false` (must break AC3)
Mutated `progressing = ($reasons.Count -gt 0)` to `progressing = $false`.
- Result: suite exit 1 at `run_pre_delivery_and_liveness_cases` (the 0303 progressing case).
- Log evidence: the progressing exec (stderr `working-N` every 400ms = run-log growing) was
  killed at `EXEC_HUNG reason=no_progress` ~2s after `EXEC_START`, never reaching
  `EXEC_PROGRESSING reason=run_log_growing` nor `hard_cap`. The assertion
  `EXEC_PROGRESSING and reason=run_log_growing in log` fails.
- Conclusion: the suite catches over-correction. We do NOT kill real work (the 0299 incident
  had a growing run-log and stays protected).

## Declared residuals (non-blocking)
- R1 (cosmetic): `Get-ExecProgressState` keeps now-unused parameters `$Lease` and
  `$FreshSeconds`. No behavior/parse impact. Optional future cleanup.
- R2 (by design): `Update-ExecLeaseHeartbeat` still bumps `heartbeat_monotonic` each
  iteration; the field survives as a lease liveness marker but is not consumed for progress.
  Consistent with AC1's chosen option (retire as progress signal). Not a defect.
- R3 (falsifiability completeness note): the frozen case's first tripwire is a static
  source-grep for the literal `heartbeat_fresh`. It kills the exact-revert mutant. A
  differently-named progressing-forcing signal would slip past the static string but is still
  caught behaviorally by the `no_progress` / `hard_cap` assertions (verified via the bypass
  run). Minor -- the AC-named mutation is killed both ways.
- R4 (out of scope, already declared in intake): the Arquitecto health watchdog (skills layer)
  has the MIRROR defect (err.log 0-byte -> false "hung"). Explicitly out of scope for 0304;
  tracked separately. Not part of this gate.

## Closure recommendation
**OK-CLOSABLE.** AC1-AC4 met, all hub gates green (validate/encoding/neutrality exit 0),
`.ps1` parses, config byte-identical (epoch 1.14.0), drift CLEAN. Falsifiability holds in
BOTH directions: a returned self-bump lets a frozen exec survive (caught), and an
over-correction that kills a progressing exec is caught (0303 fails). This closes the R1
residual converged on in TASK-0303. Maker != checker preserved; Codex may proceed to the
done-flip after Arquitecto ratifies.

-- Analista
