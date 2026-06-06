---
handoff_id: HANDOFF-TASK-0031-codex-to-claude-1
task_id: TASK-0031
spec_id: Area_comun/specs/SPEC-0030-adapter-replay-loop.md
from: Codex
to: Claude
date: 2026-06-06
status: for_review
requires_response: no
response_owner: none
acceptance_criteria_verified: yes
tests_run:
  - python examples/runtime_loop_cases/run_runtime_loop_cases.py
  - python examples/runtime_apply_cases/run_runtime_apply_cases.py
  - python examples/runtime_router_cases/run_runtime_router_cases.py
  - python examples/runtime_turn_cases/run_runtime_turn_schema_cases.py
  - python examples/runtime_turn_cases/run_runtime_turn_semantic_cases.py
  - python scripts/validate_collaboration_state.py --root .
  - python scripts/scan_domain_neutrality.py --root .
  - powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_collaboration_state.ps1 -Root .
  - powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_domain_neutrality.ps1 -Root .
spec_deviations:
  - none
decisions_referenced:
  - DECISION-0009
  - DECISION-0001
---

# Handoff: TASK-0031 Runtime M1 Replay Loop

## 1. Minimal Context
Implemented SPEC-0030: vendor-neutral `AgentAdapter`, deterministic replay adapter, `--run` loop and
JSONL run-log. Runtime remains opt-in; live `protocol.config.json` still has `runtime.enabled:false`.

## 2. What Was Done
- Added `runtime/adapters/base.py` with `ContextPack`, `TurnReport` and `AgentAdapter`.
- Added `runtime/adapters/replay.py` with deterministic report loading from file or sorted directory.
- Added `runtime/runlog.py` with injectable/deterministic run ids.
- Extended `runtime/orchestrator.py` with `--run`, `--once`, `--max-iter`, `--adapter replay`,
  `--replay-report` and `--run-id`.
- Added `examples/runtime_loop_cases/run_runtime_loop_cases.py` with 5 golden cases.
- Answered `MSG-20260606-Claude-to-Codex-task0031-coord` by implementing `--run-id` plus deterministic
  default `RUN-<sha256-prefix>`.

## 3. What Was Not Done
- No real LLM adapter. M2 remains responsible for Claude/Codex adapters.
- No automatic claim acquisition. The M1 loop relies on existing active claims so `turn_validate`
  can enforce the write allowlist deterministically.

## 4. Acceptance Criteria Verified
| Criterion | Evidence | Status |
|-----------|----------|--------|
| `--run --once` applies 1 turn + 1 commit | `case_once_commits_one_turn` checks git log +1, task `done`, exact `RUN-fixture-once.jsonl` | met |
| Sequence is deterministic and `--max-iter` cuts in N | `case_sequence_max_iter_cuts` leaves first task `done`, second `ready` with one commit | met |
| `human_required` stops before continuing | `case_human_required_stops_without_commit` keeps task `ready` and git log unchanged | met |
| `--plan` remains read-only | `case_plan_is_read_only`; live `python runtime/orchestrator.py --plan` returned `next: null` after mailbox answer | met |
| `runtime.enabled:false` aborts `--run` | `case_enabled_false_aborts_run`; live config remains false | met |
| Same interface for replay/future real adapter | Orchestrator depends on `AgentAdapter` protocol and adapter name only | met |

## 5. Tests Run
All commands listed in frontmatter passed. Python/Powershell validator and neutrality scan both returned
exit code 0.

## 6. Spec Deviations
none

## 7. Requested Action
Claude: review TASK-0031 against SPEC-0030 and ratify or request changes.

## 8. Risks and Assumptions
- Assumption: automatic claim acquisition belongs to M2 or a follow-up, because M1 tests stay deterministic
  with pre-existing active claims.
- Run logs are written as runtime output; turn commits still include the report-declared changed paths only.

## 9. Open Questions / BLOCKED
none

## 10. Pointers
- Task: `Area_comun/tasks/TASK-0031-codex-runtime-adapter-loop.md`
- Spec: `Area_comun/specs/SPEC-0030-adapter-replay-loop.md`
- Handoff: `Area_comun/handoffs/HANDOFF-TASK-0031-codex-to-claude-1.md`
- Golden: `examples/runtime_loop_cases/run_runtime_loop_cases.py`
