# Startup Prompt For Next Session

You are Codex in `d:\Agentes\multi_agent_project_protocol`.

Read first:

1. `AGENTS.md`
2. `personal/Codex/Memory.md`
3. `Area_comun/state/PROJECT_STATE.json`
4. `Area_comun/state/TASK_INDEX.json`
5. `Area_comun/state/CLAIMS.json`
6. `Area_comun/mailbox/open/`

Then run:

```powershell
git status --short
python runtime\orchestrator.py --plan
python scripts\validate_collaboration_state.py --root .
python scripts\prune_state.py --root . --check
```

Current known state:

- Live version is `0.10.0`; v1.0 track is in progress.
- `TASK-0061` is done and accepted.
- `TASK-0062` is done and accepted; it closed the wrapper LLM real functional block.
- `TASK-0063` is in_review; Codex delivered docs of adoption + N-agent runtime docs.
- Active claims should be none.
- No Codex-ready task is expected until Claude reviews/responds.
- `orchestrator --plan` may point to Claude answering
  `MSG-20260607-Codex-to-Claude-anomalia-task0063-go-ledger`.

Important open coordination:

- `MSG-20260607-Codex-to-Claude-task0063-in-review.md`
  - requires Claude review.
- `MSG-20260607-Codex-to-Claude-anomalia-task0063-go-ledger.md`
  - requires Claude response; it was materially resolved by ledger reconciliation but remains open.
- FYI messages `task0060-accepted` and `task0062-accepted` may remain open and produce validator warnings only.

Do not start new work just because a GO file exists. Confirm all of these first:

1. `TASK_INDEX.json` has the task as `ready`.
2. `PROJECT_STATE.json#active_tasks` agrees.
3. No active claim conflicts.
4. Dependencies are done.
5. Mailbox GO/spec/task are coherent.

If the user asks to monitor:

1. Poll `mailbox/open`, `TASK_INDEX.json`, `CLAIMS.json`, `PROJECT_STATE.json`.
2. React to Claude deliverables automatically when ledger and claims are consistent.
3. If a mismatch persists after a brief recheck, notify Claude via mailbox per DECISION-0018.
4. Keep updates short.

Copy-paste instruction for another session:

```text
Lee AGENTS.md y personal/Codex/Memory.md. Luego revisa PROJECT_STATE, TASK_INDEX, CLAIMS y mailbox/open. Ejecuta git status --short, python runtime\orchestrator.py --plan, python scripts\validate_collaboration_state.py --root . y python scripts\prune_state.py --root . --check. Estado esperado: TASK-0062 done/accepted, TASK-0063 in_review con handoff abierto para Claude, sin claims activos. El plan puede pedir respuesta de Claude al mensaje de anomalia TASK-0063. No reclames D2.4 ni ninguna tarea nueva hasta que TASK_INDEX/PROJECT_STATE/mailbox/claims esten coherentes.
```
