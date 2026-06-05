---
handoff_id: HANDOFF-TASK-0004-codex-to-claude-1
task_id: TASK-0004
from: Codex
to: Claude
date: 2026-06-05
status: ready_for_review
requires_response: yes
response_owner: Claude
requested_action: Review scripts/new_instance.py, README_INSTANCIACION.md and examples/generated_minimal_instance; if acceptable, mark TASK-0004 done.
---

# Handoff: TASK-0004 scaffolding script

## Summary

Implemented `scripts/new_instance.py`, a cross-platform Python stdlib scaffolding script that
creates a valid protocol instance from the neutral template masters.

## Deliverables

- `scripts/new_instance.py`
- `README_INSTANCIACION.md` updated with automatic and manual instantiation flows
- `examples/generated_minimal_instance/` generated as controlled evidence

## Behavior

- Requires the minimum requested parameters:
  - `--source-template`
  - `--target`
  - `--project-name`
  - `--project-goal`
  - `--project-description`
  - `--architect`
  - `--implementer`
  - `--human-owner`
  - `--phase-id`
  - `--phase-name`
  - `--phase-goal`
- Supports optional `--protocol-version`; if omitted, it discovers the source template version
  from `protocol.config.json` or `PROJECT_STATE.json`, falling back to `0.1.0`.
- Copies canonical templates:
  - `AGENTS.template.md` -> `AGENTS.md`
  - `protocol.config.template.json` -> `protocol.config.json`
  - `Area_comun/README.template.md` -> `Area_comun/README.md`
  - `PROJECT_STATE.template.json` -> `PROJECT_STATE.json`
  - `TASK_INDEX.template.json` -> `TASK_INDEX.json`
  - `CLAIMS.template.json` -> `CLAIMS.json`
- Creates required support folders under `Area_comun/`.
- Leaves `TASK_INDEX.json` empty but valid.
- Fails on a non-empty target unless `--force` is passed.
- Fails if any `{{...}}` placeholder remains unresolved.

## Design Notes

The script intentionally does not copy this repository's live task backlog, decisions, handoffs,
reports or mailbox messages into a new instance. It copies the neutral protocol docs and report
template, then creates empty operational folders with `.gitkeep` where applicable. This keeps the
generated instance domain-neutral and avoids leaking dogfooding history.

No profile work was started. `DECISION-0002` is respected: profile implementation remains for
future tasks after `TASK-0005`.

## Evidence

Generation command used:

```powershell
python scripts\new_instance.py --source-template . --target examples\generated_minimal_instance --force --project-name generated_minimal_instance --project-goal "Exercise the scaffolding script with a minimal valid protocol instance." --project-description "Temporary generated instance used to verify TASK-0004 scaffolding." --architect Claude --implementer Codex --human-owner "operador humano" --phase-id P0 --phase-name "Initial setup" --phase-goal "Create a valid initial protocol state."
```

Validation results:

```text
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .
OK: collaboration state is valid.

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root examples\minimal_instance
OK: collaboration state is valid.

python scripts\validate_collaboration_state.py --root .
OK: collaboration state is valid.

python scripts\validate_collaboration_state.py --root examples\minimal_instance
OK: collaboration state is valid.

python scripts\validate_collaboration_state.py --root examples\generated_minimal_instance
OK: collaboration state is valid.
```

Placeholder scan for `examples/generated_minimal_instance` returned no matches:

```powershell
rg "\{\{[A-Z0-9_]+\}\}" examples\generated_minimal_instance
```

## Open Questions

None blocking.
