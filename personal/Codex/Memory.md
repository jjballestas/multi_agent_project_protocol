# Codex Memory

Last updated: 2026-06-06 Europe/Madrid

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

Current released version observed in the session: `v0.8.0`.

## Latest Session Close - 2026-06-06

The current project is in P2 after runtime M1/v0.8.0. The live runtime is enabled in the dogfood
instance, but real LLM autonomy is not enabled. The next expected work is M2 hito 2: adapter LLM real,
single-turn only, with replay comparison and human gate.

Important current state:

- `TASK-0035` is accepted and `done`. It closed the mailbox `status` <-> folder bug:
  - validator hard-fails mismatches in `open/`, `answered/`, and `archived/`;
  - `prune_state.py` normalizes `status: archived` before moving messages to `archived/`;
  - `examples/mailbox_status_cases/` covers 5 cases;
  - CI runs the mailbox status golden.
- Latest commits at close:
  - `5f81f49 chore(mailbox): close task0035 acceptance messages`
  - `cf90389 feat(P2): cerrar TASK-0035 a DONE - bug mailbox status<->carpeta CERRADO de raiz + blindado`
  - `2a7e241 chore(protocol): hand off task0035 for review`
  - `dd85ed5 feat(protocol): enforce mailbox status folders`
- Mailbox `open/` was clean at close: only `.gitkeep`.
- No active Codex task/claim should be assumed. Always re-check `Area_comun/state/CLAIMS.json`.
- `prune_state --check` was green at close, with cold start around `8141` tokens after final cleanup.
- Validation at close was green:
  - `python scripts\validate_collaboration_state.py --root .`
  - `powershell -NoProfile -File scripts\validate_collaboration_state.ps1 -Root .`
  - `python scripts\scan_encoding.py --root .`
  - `python scripts\prune_state.py --root . --check`

Potential next item:

- Claude created `Area_comun/specs/SPEC-0035-adapter-llm-real.md` for `TASK-0036`, status `proposed`.
  It describes M2 hito 2: `LLMAdapter`, pluggable invoker, `RecordedInvoker`, replay comparison,
  budget/allowlist limits, `--adapter llm --once`, no autonomy, no live API in CI.
- At the time it was observed, there was no mailbox message and no claim associated with SPEC-0035.
  Do not edit it unless there is a current claim/instruction or the user/Claude opens the task.

Coordination rules learned the hard way:

- Before any shared edit, inspect `TASK_INDEX.json`, `CLAIMS.json`, and `Area_comun/mailbox/open/`.
- If a mailbox message no longer applies, move it out of `open/` using the protocol:
  claim first, set frontmatter `status` to the destination folder, move file, validate, release claim,
  and commit if shared state changed.
- When moving a task to `in_review`, commit WIP first and release the claim immediately in the same
  handoff movement.
- Do not leave active claims after a handoff. The validator has a handoff-release gate.
- ASCII-only still applies to `Area_comun/mailbox/**` and `Area_comun/state/*.json`; avoid PowerShell
  `Set-Content` BOM in state files, or rewrite with Python UTF-8 no BOM before closing.

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
