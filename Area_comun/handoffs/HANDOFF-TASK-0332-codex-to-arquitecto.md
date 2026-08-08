---
handoff_id: HANDOFF-TASK-0332-CODEX-TO-ARQUITECTO
task_id: TASK-0332
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-08-08T10:05:00Z
implementation_commit: 4205d04ddb92b43f0993224e7870900e924bd107
reviewer: Analista
---

# TASK-0332 behavioral date-offset contract

## Delivered result

Commit `4205d04ddb92b43f0993224e7870900e924bd107` adds permanent negative
`NEG-MEMORY-DATE-OFFSET-PII-BEHAVIOR` to the existing memory test runner and embedded
falsification inventory. Production `scripts/memory/build_memory_db.py` is unchanged.

The contract drives every timezone offset accepted by the current `DATE_RE` grammar through
`contains_pii`: no offset, `Z`, both signs for every minute from hours 00 through 13, and the
two endpoints `+14:00` and `-14:00`. The measured population is 1,684 offsets. Every member must
detect both a domain term in the timestamp itself and an email in a later list item.

The falsification target is `+06:15`. It is outside the former TASK-0317 behavior sample
`("", "Z", "+02:00", "-05:00", "-12:30")` and outside the TASK-0325 grammar-only sample
`("+05:45", "-09:45", "+13:00", "+14:00")`.

## AC1 prior falsification

At pre-implementation commit `2b57d56e26f59200630125ae22a714563e2ec59d`, a production mutant
inserted a narrow falsy return for the valid `+06:15` offset. The complete unmodified suite
reported `Ran 70 tests ... OK`, exit 0. This proves the prior contract gap by behavior.

## AC3 and AC4 mutation attribution

All three mutants are built from production source and loaded as executable modules. The permanent
negative does not inspect the AST.

| Form | Observable mutant result `(timestamp PII, later email PII)` | Contract that kills it |
|---|---:|---|
| Restructure all checks under `if not target offset` | `(False, True)` | New exhaustive timestamp behavior assertion |
| Filter the target offset in an external iterable helper | `(False, True)` | New exhaustive timestamp behavior assertion |
| Narrow `return False` at the target offset | `(False, False)` | New timestamp and later-item behavior assertions |

Each form was also applied directly to production in its own detached clone of the implementation
commit. The targeted permanent negative exited 1 for all three. For the restructure mutant, the
first failure is the source behavior subtest at offset `+06:15`, with expected `(True, True)` and
observed `(False, True)`; the failure is not merely an AST or source-shape check.

The existing contracts remain necessary and unchanged: TASK-0322 guards the grammar ranges,
TASK-0325 guards outer-loop `break`/`continue` ownership independent of a specific offset, and
TASK-0317 retains its original 333-member metadata and placement semantics. The new behavior
contract closes the disjoint offset gap without deleting or relaxing them.

## Verification evidence

Detached clone:
`D:/Aegis_Scratch/multi_agent_project_protocol/codex0332-4205d04d`, exact commit
`4205d04ddb92b43f0993224e7870900e924bd107`.

- `python scripts/memory/test_memory_db.py` -> exit 0; 71 tests.
- `python scripts/check_falsification_contracts.py --root . --inventory` -> exit 0;
  58 permanent negatives, 58 declared, 0 missing.
- Five directed TASK-0317/TASK-0322/TASK-0325 tests -> exit 0; 5 tests.
- `python scripts/validate_collaboration_state.py --root .` -> exit 0.
- `python scripts/scan_encoding.py` -> exit 0.
- `python scripts/scan_domain_neutrality.py --root .` -> exit 0.
- `python runtime/protocol_replay.py --check-drift --root .` -> exit 0; drift clean at seq 7960.
- `python -m py_compile scripts/memory/test_memory_db.py` -> exit 0.
- `git diff --exit-code 4205d04d^ 4205d04d -- scripts/memory/build_memory_db.py` -> exit 0.
- Final `git status --short` in the detached clone -> empty after evidence logs were moved outside
  the clone.

Codex is the maker only and did not review or ratify this work.

task_id: TASK-0332
status: in_review
executive_summary: The date-offset protection is now behavioral across all 1,684 accepted offsets, and the three requested bypass forms die. Production is unchanged.
artifacts:
  - path_or_commit: 4205d04ddb92b43f0993224e7870900e924bd107
  - path_or_commit: Area_comun/handoffs/HANDOFF-TASK-0332-codex-to-arquitecto.md
gates:
  - command: python scripts/memory/test_memory_db.py
    result: PASS
  - command: python scripts/check_falsification_contracts.py --root . --inventory
    result: PASS
  - command: python scripts/validate_collaboration_state.py --root .
    result: PASS
  - command: python scripts/scan_encoding.py
    result: PASS
  - command: python scripts/scan_domain_neutrality.py --root .
    result: PASS
next_recommended: Route exact commit 4205d04ddb92b43f0993224e7870900e924bd107 to Analista for independent review.
risks: The embedded inventory row is intentionally single-line to preserve existing line-bound neutrality exemptions; TASK-0329 owns removal of that coordinate coupling.
