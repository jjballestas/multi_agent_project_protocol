# HANDOFF TASK-0342 remediation 3 - blocked only on real Actions admission

task_id: TASK-0342
owner_maker: Codex
status: blocked
implementation_commit: `05ec641f23b008b59a79c80d02179479b6d209ad`
exact_pushed_head: `bb90a6ad89ac308e87e71194328f991cd6a5e639`

## Delivered implementation

- `scripts/scan_encoding.ps1 -DumpPolicy` serializes the effective skip policy at the exact point
  where the scanner consumes it, after every top-level assignment has executed.
- The permanent negative consumes runtime JSON, not a declaration-line regex.
- Production-script variants prove `+=` and a later assignment introduce a live `dist` divergence
  and are caught. A multiline array and trailing comment preserve behavior and remain accepted.
- A coordinate without a case-bearing character remains in the exact-coordinate universe and no
  longer causes a false-red manufactured case variant.
- Independent hidden sentinels bind `Scan-AsciiPath`, `Scan-AsciiStateJson`, and
  `Scan-MojibakeRoot`. Removing `-Force` from any one production function changes the measured set.

## Local evidence

- `python scripts/validate_collaboration_state.py`: PASS.
- `python scripts/scan_encoding.py`: PASS after one transient locked-file retry; the immediate
  diagnostic sweep found no persistently unreadable path and the repeated mandatory gate exited 0.
- Python and PowerShell neutrality gates: PASS.
- `python scripts/check_falsification_contracts.py --root .`: PASS.
- Inventory: `71/71` permanent negatives, with 14 boundaries for
  `NEG-ENCODING-SKIP-PATH-SEPARATOR`.
- Encoding runner: PASS locally with PowerShell 7 POSIX parity explicitly `UNMEASURED`.
- Compile, drift (`CLEAN up_to_seq=8612`), and diff gates: PASS.

## Blocking evidence

Real Actions run `31402650690` targets exact head `bb90a6ad`. All four jobs have empty step lists and
runner id 0. GitHub reports: `The job was not started because recent account payments have failed or
your spending limit needs to be increased.` No requested scanner or mutation step executed, so AC5
cannot be claimed and TASK-0342 cannot enter review yet.

## Coordination anomaly signaled

While Codex waited on the staged TASK-0328 transaction, commit `0c216cd6` included the already-written
TASK-0342 task-note and Codex-signed claim event inside a commit whose subject/trailer identify only
TASK-0328. Codex did not touch or rewrite the peer transaction. The implementation itself is isolated
in `05ec641f` with `Task-Id` and `Fixes-Task` trailers for TASK-0342.

## Required continuation

After Actions admission is restored, rerun the workflow on the same implementation code, capture the
four `POLICY_MUTATION` output lines plus the three independent hidden-enumeration mutants, recompute
the saldo from that run, and only then deliver to independent Analista review. Codex remains maker
only and has not reviewed or ratified the implementation.
