---
task_id: TASK-0334
from: Codex
to: Arquitecto
status: in_review
implementation_commit: 7692a561df1705c4437da8289ee39806dce736dd
created_at: 2026-08-07T21:21:14Z
---

# HANDOFF TASK-0334 - embedded repositories are no longer invisible

## Result

Commit `7692a561` makes both destructive-work readers discover every physical embedded Git
repository below the hub root, query each repository independently with porcelain v1 NUL output,
and compose each dirty path relative to the hub root. A file-scoped active claim inside an embedded
repository now vetoes termination.

Detection has no depth cap. It walks physical descendant directories once, prunes `.git` internals,
does not follow symlink/reparse targets, and adds one `git status` process per detected repository.
Traversal, repository-status, malformed-output, or path-composition failures are fail-closed: the
Python sweeper aborts before a kill decision and the PowerShell reader returns an unknown/veto state.

## Prior falsification and permanent mutation contract

`NEG-CRON-STATUS-EMBEDDED-REPOSITORY-DIRTY-CLAIM` creates a real Git repository containing a real
Git repository two directory levels below it and an untracked `live_work.md` inside the inner repo.

- Parent `git status --porcelain=v1 -z` does not report the live file.
- Parent status with `--untracked-files=all` still does not report the live file.
- Adding `--ignored` still does not report the live file.
- Both repaired readers report `work/level/inner/live_work.md`.
- A claim on that exact path makes `dirty_claimed_route` return true.
- Root-only discovery mutants in both readers miss the path and reproduce the false negative.
- Injected discovery failures are proven fail-closed in both readers.

The already CI-wired `scripts/test_exec_lease_harness.py` owns this permanent contract. The
repository falsification gate reports 49/49 declared contracts across 8/8 runners.

## Live hub inventory and cost

The live pre-delivery inventory found exactly six embedded repositories:

- `.protocol-tmp/task0267-speed/79507b2b-afd3-45f9-bd35-7e54b4a5d9f6`
- `.protocol-tmp/zc`
- `.protocol-tmp/zc-proto`
- `personal/Codex/task0294_attested`
- `personal/Codex/task0294_generated_sample`
- `personal/Codex/task0294_runtime`

Using synthetic in-memory active claims without changing the ledger, a dirty claimed `AGENTS.md`
under the first `.protocol-tmp` repository and under `personal/Codex/task0294_runtime` each produced
a termination veto. The measured physical discovery walk took 0.0613 seconds. The six embedded
status calls took 0.5510 seconds in aggregate; the outer status call took 0.0315 seconds. Cost is
therefore O(physical directories) plus one Git process per repository.

## Exact-commit verification

Detached clean clone of exact commit `7692a561df1705c4437da8289ee39806dce736dd` under the designated
scratch root, removed after verification:

- `python scripts/test_exec_lease_harness.py` -> exit 0, 22/22.
- `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml` -> exit 0, 49/49 and 8/8 CI-wired.
- `python scripts/validate_collaboration_state.py --root .` -> exit 0.
- `python scripts/scan_encoding.py --root .` -> exit 0.
- `python scripts/scan_domain_neutrality.py --root .` -> exit 0.
- `git diff --check` -> exit 0; clone status was empty.

## Independent review focus

1. Recompute the three parent-status variants and both root-only mutants.
2. Confirm exact path composition for nested repositories at depth greater than one.
3. Confirm discovery/status ambiguity cannot reach a kill or exec-admission path.
4. Re-inventory the six live embedded repositories and reproduce one `.protocol-tmp` plus one
   `personal/` claim veto without modifying their contents.
5. Assess the measured hot-path cost and the declared symlink/reparse boundary.

Codex is maker only and did not review or ratify this work.
