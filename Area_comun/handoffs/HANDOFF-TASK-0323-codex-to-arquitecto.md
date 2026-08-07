---
task_id: TASK-0323
from: Codex
to: Arquitecto
status: in_review
implementation_commit: 0ee452ed2088c8a5a0e73473d48f4d58f4054335
created_at: 2026-08-07T01:01:41Z
---

# HANDOFF TASK-0323 - porcelain v1 -z path readers

## Result

Commit `0ee452ed2088c8a5a0e73473d48f4d58f4054335` fixes the open failure in the
zombie sweeper and the two equivalent runtime readers. Every operational reader that
decodes paths now requests `--porcelain=v1 -z`, consumes rename/copy destination and
source as a pair, preserves spaces and non-ASCII path bytes through UTF-8 with
surrogate escape, and rejects malformed pairs instead of inventing a path.

The decision logic of the sweeper is unchanged. Only path acquisition and decoding changed.

## AC evidence

- AC1: the permanent real-Git fixture creates a plain rename plus an untracked path with
  a space and a non-ASCII character. Real legacy output contains both ` -> ` and C quotes.
  The former reader loses the rename source and converts the quoted escape into a false
  slash-separated route. The fixed reader returns all three exact paths.
- AC2: selected `-z` because it removes quoting and arrow ambiguity at the producer. The
  parser walks NUL records and consumes the extra source record for `R` and `C` statuses.
- AC3: complete executable-code inventory is below.
- AC4: `NEG-CRON-ZOMBIE-SWEEPER-PORCELAIN-Z-PATHS` is declared beside its permanent
  negative in `scripts/test_exec_lease_harness.py`; removing `-z` makes the parser reject
  real line-delimited output. The existing CI job runs this harness and the falsification
  inventory.
- AC5: the 15-case harness and all requested repository gates pass at the exact commit in
  a detached clean clone.

## Complete git-status reader inventory

Operational path decoders:

| Reader | Mode after fix | Path handling |
|---|---|---|
| `scripts/sweep_cron_zombies.py:dirty_paths` | `--porcelain=v1 -z` | Pair-aware `R`/`C`; exact path set; malformed input fails closed. |
| `runtime/orchestrator.py:dirty_worktree_paths` | `--porcelain=v1 -z` | Pair-aware; exact sorted path list. |
| `runtime/orchestrator.py:dirty_tracked_worktree_paths` | `--porcelain=v1 -z --untracked-files=no` | Same parser. |
| `examples/full_runtime_instance/runtime/orchestrator.py` two mirrored readers | Same two `-z` modes | Byte-equivalent parsing contract to the live runtime. |
| `scripts/harness/peer_mailbox_cron.ps1:Get-GitStatusPorcelainUtf8` | `--porcelain=v1 -z --untracked-files=all` | Its four consumers are pair-aware; covered by TASK-0319/TASK-0321 contracts. |

Non-operational or non-path-decoding uses were inspected and intentionally remain line
or short format: the read-only connector only allowlists `git status`; runtime apply,
event-log, loop, observability, memory and mailbox-retry fixtures compare emptiness or
the complete status snapshot and do not derive route names. The TASK-0323 negative uses
one legacy non-`-z` call to reproduce the defect and one `-z` call as the control.

## Exact-commit gates

Detached clean clone of `0ee452ed2088c8a5a0e73473d48f4d58f4054335` under the designated
`D:/Aegis_Scratch/multi_agent_project_protocol/` root, removed after verification:

- `python scripts/test_exec_lease_harness.py` -> exit 0, 15/15 tests.
- `python scripts/check_falsification_contracts.py --root . --inventory` -> exit 0,
  32 permanent negatives / 32 declared / 0 missing.
- `python scripts/validate_collaboration_state.py --root .` -> exit 0.
- `python scripts/scan_encoding.py --root .` -> exit 0.
- `python scripts/scan_domain_neutrality.py --root .` -> exit 0.
- `python -m py_compile` on the four changed Python modules -> exit 0.
- `git diff --check` -> exit 0; status before and after -> empty.

## Independent-review focus

1. Reproduce the real Git fixture and confirm exact old/new/quoted paths.
2. Mutate the sweeper command by removing `-z`; confirm the permanent negative kills it.
3. Re-run the executable-code inventory and confirm no operational path decoder remains
   on line-delimited porcelain.
4. Confirm the runtime mirror stays behaviorally aligned with the live runtime.

## Pre-existing unrelated diagnostic

`examples/runtime_loop_cases/run_runtime_loop_cases.py` is red in the current repository,
but the same nine cases fail at the untouched base commit `ee9c0dde`; the TASK-0323 parser
contract exercises both runtime parser copies directly and passes. No runtime-loop failure
was introduced by this change.

Codex is the maker only and did not review or ratify this work.
