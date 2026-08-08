# TASK-0343 pre-fix diagnosis

Recorded before changing the assertion at
`examples/mailbox_retry_cases/run_mailbox_retry_cases.py:1638`.

## Measured facts

- Local Windows run: Python 3.12.10, Windows PowerShell 5.1, Git
  `core.autocrlf=true`. The complete runner exits 0. The accepted log record is
  `ROLLBACK_LEDGER_PRESERVED seq_before=0 seq_after=3 proof=disk`.
- GitHub Actions run 31266113929: Python 3.14.6, Windows runner, job shell
  PowerShell 7. The complete assertion fails because that exact record is absent.
  The failed run did not print the private fixture log and uploaded no artifact,
  so it does not expose the actual field values.
- Diagnostic Actions run 31269392388 confirms
  `preserved_records=[]`: CI emits no `ROLLBACK_LEDGER_PRESERVED` record at all,
  so there are no CI `seq_before`, `seq_after`, or `proof` values on that branch.
  A second diagnostic observation now exposes every rollback record to identify
  the path that preserved the ledger in CI.
- Producer: `scripts/harness/peer_mailbox_cron.ps1` reads both heads through
  `scripts/ledger_head.py`; its preserved branch logs the pre-exec head, the
  post-exec head, and the proof implementation label after two identical disk
  proofs and derived-state verification. The fixture agent appends signed events
  with sequence 1, 2, and 3 during its third execution.

## Diagnostic requirement before repair

The assertion remains unchanged. A diagnostic-only observation must expose every
rollback record in a real Actions run so the CI preservation path can be recorded
before replacing the literal assertion.

## Whole-file literal inventory (pre-fix)

Candidate assertions tied to counters or paths remain at lines 503, 516, 754,
765, 776, 862, 868, 956, 1078, 1086, 1170, 1173, 1252, 1324, 1364, 1417,
1601, 1603, 1607, 1610, 1611, 1622-1630, 1635-1638, and 1644. These include
behavioral bounds and fixture-relative paths as well as brittle literal log
records; TASK-0343 will classify them rather than silently expanding scope.
