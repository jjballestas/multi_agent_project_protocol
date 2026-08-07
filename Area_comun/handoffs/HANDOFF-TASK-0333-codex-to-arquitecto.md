---
task_id: TASK-0333
from: Codex
to: Arquitecto
status: in_review
implementation_commit: 303a1d70
created_at: 2026-08-07T16:51:40Z
---

# HANDOFF TASK-0333 - untracked subtree turn gate

## Result

Commit `303a1d70` makes `dirty_worktree_paths` request
`git status --porcelain=v1 -z --untracked-files=all` in both the live runtime and the shipped
full-runtime mirror. The turn gate now sees every file below an untracked directory, so a report
that declares only `work/` cannot conceal `work/hidden/backdoor.py` or deeper files.

`dirty_tracked_worktree_paths` remains unchanged with `--untracked-files=no`. It is intentionally
tracked-only because its consumer decides whether a failed apply dirtied paths that existed before
the turn; admitting untracked output there would broaden rollback/recovery beyond that contract.

## Behavioral contract and mutation evidence

`NEG-TURN-UNTRACKED-SUBTREE-MUST-BE-DECLARED` runs in the already CI-wired
`run_runtime_turn_obstacle_cases.py` runner against a real temporary Git repository.

- Legacy query: `['work/']`; declaring `work/` yields no unreported path and would accept the turn.
- Fixed query: the three exact paths are visible; declaring only `work/` yields all three as
  unreported and rejects the turn.
- Legitimate control: declaring the same three exact paths yields no unreported path.
- Removing `--untracked-files=all` is killed by behavior.
- Leaving the option literal in unreachable code via `command[:4]` is also killed by behavior.
- The shipped full-runtime mirror is exercised against the same real repository and returns the
  same three exact paths.

## Complete executable Git-status reader inventory

Operational path decoders:

| Reader | Options | Purpose |
|---|---|---|
| `runtime/orchestrator.py:dirty_worktree_paths` | `--porcelain=v1 -z --untracked-files=all` | Enforce exact turn `changed_paths`; fixed here. |
| `runtime/orchestrator.py:dirty_tracked_worktree_paths` | `--porcelain=v1 -z --untracked-files=no` | Tracked-only apply/recovery baseline; intentionally unchanged. |
| `examples/full_runtime_instance/runtime/orchestrator.py` mirror pair | Same two modes | Shipped runtime mirror; kept aligned here. |
| `scripts/sweep_cron_zombies.py:dirty_paths` | `--porcelain=v1 -z --untracked-files=all` | Match dirty files to active claims. |
| `scripts/harness/peer_mailbox_cron.ps1:Get-GitStatusPorcelainUtf8` | `--porcelain=v1 -z --untracked-files=all` | Residue/admission checks. |

All other tracked `git status` invocations are connector classification or test/fixture probes.
They compare emptiness/whole output or deliberately reproduce legacy behavior; they do not decode
operational routes.

## Corpus impact

The tracked JSON turn corpus contains 16 reports. One report declares a directory
(`examples/context_cost_cases/`); none carries an associated dirty untracked subtree, so exact
replay of the corpus adds **0 rejected turns**. The one directory declaration is the only candidate
whose future behavior becomes stricter if a turn actually creates undeclared descendants, which is
the intended fail-closed direction.

## Exact-commit verification

Detached clean clone of `303a1d70` under the designated scratch root, removed after verification:

- `python scripts/test_exec_lease_harness.py` -> exit 0, 21/21.
- `python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py` -> exit 0.
- `python scripts/check_falsification_contracts.py --root .` -> exit 0, 48/48.
- `python scripts/validate_collaboration_state.py --root .` -> exit 0.
- `python scripts/scan_encoding.py --root .` -> exit 0.
- `python scripts/scan_domain_neutrality.py --root .` -> exit 0.
- Python compile and `git diff --check` -> exit 0; clone status remained empty.

## Independent review focus

1. Recompute the real-Git legacy/fixed comparison and both mutants.
2. Confirm an exact declaration remains accepted while the directory-only declaration is rejected.
3. Re-run the executable reader inventory and confirm the tracked-only reader remains unchanged.
4. Confirm the live runtime and shipped mirror remain behaviorally aligned.

Codex is maker only and did not review or ratify this work.
