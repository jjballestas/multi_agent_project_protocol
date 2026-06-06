# Codex Memory

Last updated: 2026-06-05 20:41 Europe/Madrid

## Repository

`multi_agent_project_protocol` is the canonical, domain-neutral repository for the reusable
multi-agent software project protocol.

It dogfoods itself:

- `AGENTS.md` is the live project contract.
- `AGENTS.template.md` is the shipped template master.
- `protocol.config.json` is the live instance config.
- `protocol.config.template.json` is the shipped template master.
- `Area_comun/` contains shared protocol docs, live state, tasks, mailbox, handoffs and
  decisions.
- `Claude/` and `Codex/` are private agent areas.

Current released version observed in the session: `v0.7.0`.

## Current State At Session Close

- `TASK-0030` is implemented by Codex and left in `in_review` for Claude.
- There are no active claims in `Area_comun/state/CLAIMS.json`.
- A review message for Claude is open:
  - `Area_comun/mailbox/open/MSG-20260605-Codex-to-Claude-task0030-in-review.md`
- Handoff for Claude:
  - `Area_comun/handoffs/HANDOFF-TASK-0030-codex-to-claude-1.md`
- Claude's previous queue message was archived:
  - `Area_comun/mailbox/archived/MSG-20260605-Claude-to-Codex-cola-runtime-m1.md`

## Recently Completed / Reviewed Context

- `TASK-0023` measure_context_cost was done and ratified.
- `TASK-0024` state pruning was done and accepted:
  - added `CLAIMS_ARCHIVE.json` and `TASK_INDEX_ARCHIVE.json`;
  - validators read hot plus archive state;
  - cold-start state was reduced.
- `TASK-0027` runtime M0 was done and accepted:
  - `runtime/context.py`
  - `runtime/router.py`
  - `runtime/turn_validate.py`
  - `runtime/orchestrator.py`
  - golden cases for turn schema, semantic validation and router behavior.
- `TASK-0028` claims by row was done and accepted:
  - validators support `path#selector`;
  - runtime turn validation aligned;
  - runtime context reads archives so router sees archived dependencies.
- Claude published `v0.7.0`, closed earlier tokens including `TASK-0025`, and instructed Codex
  to continue with `TASK-0030`, then `TASK-0031`.

## TASK-0030 Deliverables

Implemented runtime M1 apply gate:

- `runtime/vcs.py`
  - commit selected paths;
  - reject policy paths unless explicitly allowed;
  - revert last commit;
  - discard worktree changes for failed apply.
- `runtime/gate.py`
  - runs Python collaboration validator;
  - runs domain-neutrality scan.
- `runtime/apply.py`
  - validates turn reports with `runtime.turn_validate`;
  - applies task status changes to task file, hot `TASK_INDEX.json`, and
    `PROJECT_STATE.active_tasks`;
  - applies claim acquire/release operations;
  - sends, answers and archives mailbox messages;
  - runs gate and commits on green;
  - on red gate, rolls back the turn changes and marks the task blocked.
- `examples/runtime_apply_cases/run_runtime_apply_cases.py`
  - temporary git repo fixtures;
  - 4 golden cases: valid commit, red gate rollback plus blocked task, policy rejection, invalid
    report no write.

## Validation Run Before Closing

All were green:

- `python scripts\validate_collaboration_state.py --root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .`
- `python scripts\scan_domain_neutrality.py --root .`
- `python examples\runtime_apply_cases\run_runtime_apply_cases.py`
- M0 regressions:
  - `python examples\runtime_turn_cases\run_runtime_turn_schema_cases.py`
  - `python examples\runtime_turn_cases\run_runtime_turn_semantic_cases.py`
  - `python examples\runtime_router_cases\run_runtime_router_cases.py`
- Instance regressions:
  - `python scripts\validate_collaboration_state.py --root examples\minimal_instance`
  - `python scripts\validate_collaboration_state.py --root examples\minimal_sdd_instance`
  - `python scripts\validate_collaboration_state.py --root examples\dotnet_enterprise_instance`
  - `python scripts\validate_collaboration_state.py --root examples\compact_communication_case`

Confirmed no active claims with:

```powershell
python -c "import json; h=json.load(open('Area_comun/state/CLAIMS.json', encoding='utf-8-sig')); print([c for c in h.get('claims', []) if c.get('status')=='active'])"
```

It printed `[]`.

## Git Status At Close

Expected dirty files from `TASK-0030`:

- deleted from open mailbox:
  - `Area_comun/mailbox/open/MSG-20260605-Claude-to-Codex-cola-runtime-m1.md`
- modified:
  - `Area_comun/state/CLAIMS.json`
  - `Area_comun/state/CLAIMS_ARCHIVE.json`
  - `Area_comun/state/PROJECT_STATE.json`
  - `Area_comun/state/TASK_INDEX.json`
  - `Area_comun/tasks/TASK-0030-codex-runtime-apply-gate.md`
- new:
  - `Area_comun/handoffs/HANDOFF-TASK-0030-codex-to-claude-1.md`
  - `Area_comun/mailbox/archived/MSG-20260605-Claude-to-Codex-cola-runtime-m1.md`
  - `Area_comun/mailbox/open/MSG-20260605-Codex-to-Claude-task0030-in-review.md`
  - `examples/runtime_apply_cases/`
  - `runtime/apply.py`
  - `runtime/gate.py`
  - `runtime/vcs.py`

Do not revert unrelated changes.

## Startup Checklist

1. Read `AGENTS.md`.
2. Read, in order:
   - `Area_comun/README.md`
   - `Area_comun/protocol/TASK_PROTOCOL.md`
   - `Area_comun/state/PROJECT_STATE.json`
   - `Area_comun/state/TASK_INDEX.json`
   - `Area_comun/state/CLAIMS.json`
   - `Area_comun/mailbox/open/`
3. Check `git status --short --branch`.
4. If Claude has reviewed `TASK-0030`, follow the mailbox outcome.
5. If `TASK-0030` is accepted/done and Claude's queue still points there, next likely Codex
   implementation task is `TASK-0031`.
6. Before editing any shared route, create or update an active claim listing the exact route or
   row selector in `scope`.

## Safety Notes

- Keep the protocol core domain-neutral.
- Do not introduce secrets.
- Do not change backward compatibility, boundaries or release policy without a recorded decision
  and human approval.
- Task status must match in the task file and `TASK_INDEX.json`.
- Shared work belongs in `Area_comun/`; private notes stay in `Codex/`.
