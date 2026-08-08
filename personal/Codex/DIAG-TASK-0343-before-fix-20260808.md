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
- Diagnostic rerun 31269815427 attempt 2 exposes the complete CI path:
  `head_changed`, successful residue quarantine, `rollback_probe_failed`, then
  `ledger_unreadable_after_exec`. The signed ledger nevertheless survives byte
  for byte. `Restore-TransientExecResidue` produces `rollback_probe_failed` from
  its trap before the preserved-record writer, and its unreadable-head guard
  produces the later defer. Therefore CI has no values for any of the three
  logged fields: `seq_before=<not emitted>`, `seq_after=<not emitted>`, and
  `proof=<not emitted>`.
- Producer: `scripts/harness/peer_mailbox_cron.ps1` reads both heads through
  `scripts/ledger_head.py`; its preserved branch logs the pre-exec head, the
  post-exec head, and the proof implementation label after two identical disk
  proofs and derived-state verification. The fixture agent appends signed events
  with sequence 1, 2, and 3 during its third execution.

## Diagnostic requirement before repair

The assertion remained unchanged through both diagnostic runs. The difference is
the conservative rollback path, not the final governed state: local proves the
stable disk branch and logs `0 -> 3 / disk`; CI preserves the same signed events
through defer and emits none of those fields. The repair may therefore bind the
pre/post ledger state itself without changing production rollback behavior.

## Whole-file literal inventory (pre-fix)

The full AST-assisted assertion sweep found no host-absolute path literal. All
path assertions are fixture-relative and name the artifact whose behavior they
exercise. The remaining counter literals classify as follows (pre-fix lines):

- Protocol properties: retry attempts `1/2/3` (1635-1637), cleared retry count
  `0` (956), and total fake executions `5` (1648). These are deliberate state
  machine expectations, not environment-derived observations.
- Timing tolerances: elapsed `<18` (1078), measured heartbeat range `1..4`
  (1086), elapsed `>=4` (1252), and elapsed `<12` (1324). These are explicit
  behavioral windows and remain unchanged.
- Liveness/mutation cardinalities: heartbeat count `>=3` (1170), mutant count
  `0` (1173), one expected process-tree survivor (1417), and one quarantined
  residue (1603). These are contract cardinalities and remain unchanged.
- Brittle ledger observations: event head `seq == 3`, claims `seq == 3`
  (1622-1623), and the combined log literal `seq_before=0 seq_after=3
  proof=disk` (1642). These three are replaced together by a relational
  before/after comparison of the complete signed event list and claims state.

Other fixture paths at 503, 516, 754, 765, 776, 862, 868, 1364, and
1601-1630 assert existence, content, or quarantine location of a named fixture
artifact. They do not embed a host root or platform separator and remain in
scope as behavioral checks.
