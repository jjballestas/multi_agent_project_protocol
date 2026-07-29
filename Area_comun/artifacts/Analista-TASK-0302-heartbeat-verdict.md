# VERDICT -- Analista adversarial review of TASK-0302

Reviewer: Analista (independent adversarial checker)
Task: TASK-0302 -- exec observability heartbeat (EXEC_RUNNING pid/elapsed) in the cron
harness, to end the mute 0/0-byte death of text-mode execs and give the watchdog a
reliable liveness signal. SOLO LOGGING by contract.
Date (local): 2026-07-29 ~14:12 (UTC+2)
Verdict: **OK-CLOSABLE**

## Canonical anchor
- Protocol HEAD reviewed: `6baa55f` (canonical origin/main). Implementation `6d96522`;
  delivery flip `35e2e0d`. The two reviewed code routes are byte-untouched between
  `6d96522` and HEAD (`git log 6d96522..HEAD -- <routes>` = empty).
- Task status at HEAD: `in_review`. Scope: HUB-ONLY. No Zeus product in scope.
- Clean clone: `D:/Aegis_Scratch/protocol/rev0302`, `git checkout 6baa55f`. All gates and
  behavioral vectors were run THERE, gated by EXIT code, never in the hot working tree.

## What the change does (verified in source)
The entire harness delta (`git diff a4931bb..HEAD -- scripts/harness/peer_mailbox_cron.ps1`,
i.e. pre-0302 parent to HEAD) is THREE additive hunks, nothing else:
1. A new param `[ValidateRange(0,2147483647)][int]$HeartbeatSeconds = 60` (0 = off).
2. Two init lines after `EXEC_START`: `$execStopwatch = [Stopwatch]::StartNew()` and
   `$nextHeartbeatSeconds = $HeartbeatSeconds`.
3. A side-effect-free `if` at the top of the existing `while (-not WaitForExit(1000))` loop:
   when `$HeartbeatSeconds -gt 0` and elapsed `>= $nextHeartbeatSeconds`, it computes
   `floor(elapsed)`, emits `Write-Log "EXEC_RUNNING pid=.. elapsed=<N>s message=<msg>"`,
   and advances `$nextHeartbeatSeconds = elapsed + $HeartbeatSeconds` (self-correcting
   cadence anchored to observed elapsed; no drift-accumulation, no double-emit).

The new locals (`$execStopwatch`, `$nextHeartbeatSeconds`, `$elapsedSeconds`,
`$HeartbeatSeconds`) are referenced ONLY in the param + init + this block
(grep-confirmed: lines 14, 1013-1014, 1026-1029; zero other consumers). The block has no
`continue`/`break`/`return`, mutates nothing outside its own locals, and does not touch the
process, deadlines, outcome, retry, post-delivery, or the ledger. Its one shared effect is
appending to the CRON log -- and the harness's own progress/liveness (`Get-ExecProgressState`,
`no_progress`/`hard_cap`/tree-kill) keys off `runtime/state/events.jsonl` bytes + the
stdout/stderr run logs, NOT the cron log. So extra cron-log writes cannot perturb any kill
decision. AC3 is therefore structurally guaranteed, not merely test-observed.

## Reproduction (clean clone, exit codes)
```
git checkout 6baa55f                                             -> HEAD 6baa55f
python scripts/validate_collaboration_state.py                  -> exit 0 (OK)
python scripts/scan_encoding.py                                 -> exit 0 (clean)
python scripts/scan_domain_neutrality.py                        -> exit 0
python examples/mailbox_retry_cases/run_mailbox_retry_cases.py  -> exit 0 (full bank PASS)
Parser::ParseFile(peer_mailbox_cron.ps1)                        -> 0 errors (PS1_PARSE=OK)
sha256(protocol.config.json HEAD) == sha256(a4931bb)            -> 2e35f26e.. == 2e35f26e..
protocol_state_drift(clean clone)                              -> has_drift=False up_to_seq=6716
git log 6d96522..HEAD -- ps1 py (reviewed routes)              -> empty (untouched since impl)
```

## Independent behavioral probe (I did not trust the fixture name)
I drove the REAL `.ps1` from the clean clone against a ~4s slow exec, parametrizing the
cadence (standalone driver reusing the bank's fixture builder), and parsed the produced
cron log with the exact regex:
```
HeartbeatSeconds=1 -> EXEC_RUNNING_count=4  elapsed=[1,2,3,4]  EXEC_START=yes  exec_completed=yes
HeartbeatSeconds=0 -> EXEC_RUNNING_count=0  elapsed=[]         EXEC_START=yes  exec_completed=yes
```
So the cadence is configurable and monotone while the exec lives (AC1), and the `0 = off`
guard truly suppresses emission WITHOUT breaking the wait loop or the exec's normal
completion.

## Vector-by-vector
| AC | Claim | Result | Evidence |
|----|-------|--------|----------|
| AC1 | EXEC_RUNNING pid/elapsed at configurable cadence (~60s default) while exec lives | PASS | Independent probe: 4 lines, elapsed 1..4s at cadence=1; EXEC_START + completion present |
| AC2 | Falsifiable regression: removing the emission makes the case FAIL, non-vacuously | PASS | Bank case `run_exec_running_heartbeat_case`: `assert exercise(runner)>=3` and mutant (line removed) `==0`; guarded by `assert heartbeat_line in runner_text` so the mutant is non-vacuous; whole bank green |
| AC3 | SOLO LOGGING: zero behavior change in outcome class / retry / post-delivery (0300) / liveness+hard_cap+tree-kill (0303/0304); all prior cases green & identical | PASS | Full `a4931bb..HEAD` .ps1 diff is additive-only; new locals isolated; liveness keys off events.jsonl not cron log; full retry bank (incl. 0300/0303/0304 cases) exit 0 |
| AC4 | Only the 2 routes; protocol.config.json byte-identical; .ps1 syntax valid; hub gates green | PASS | config sha256 identical (2e35f26e, fondo intocable); Parser 0 errors; validate/encoding/neutrality exit 0 |

## Declared residuals (non-blocking)
- The bank's heartbeat case asserts cadence>0 (>=3) and removal (==0) but does NOT itself
  lock the `HeartbeatSeconds=0` off-switch as a named regression; I covered that off path
  independently (0 emissions, exec still completes). Coverage note, not a defect.
- Out of scope BY DESIGN and correctly deferred: this does NOT detect a hung-but-alive
  text-mode exec (no real work signal exists in text-mode), does NOT switch output-format,
  and does NOT wire the Arquitecto watchdog to consume EXEC_RUNNING (skills layer, separate).
  The change only adds the log line the watchdog can later key off.
- The commit also moves ledger/state bookkeeping (claim acquire + ready->in_progress) and
  `runtime/state/*`; that is the expected governed transition for the task, not a scope
  breach of the two code routes.

## Closure recommendation
**OK-CLOSABLE.** AC1/AC2/AC4 verified behaviorally and by gates; AC3 (the critical
solo-logging vector) is structurally airtight -- the whole harness delta is additive,
side-effect-isolated logging, and the liveness machinery reads a different file. Fondo
intocable confirmed (config 2e35f26e, epoch 1.14.0 unchanged, drift clean).

-- Analista
