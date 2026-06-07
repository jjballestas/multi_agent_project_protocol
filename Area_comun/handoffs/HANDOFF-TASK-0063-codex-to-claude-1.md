---
handoff_id: HANDOFF-TASK-0063-codex-to-claude-1
task_id: TASK-0063
from: Codex
to: Claude
status: in_review
created_at: 2026-06-07
context_refs:
  - Area_comun/specs/SPEC-0049-d2.3-docs-adopcion.md
  - README_INSTANCIACION.md
  - Area_comun/protocol/N_AGENT_RUNTIME.md
---

# Handoff TASK-0063 - Docs de adopcion

## Resumen

Entrego D2.3 como documentacion solamente. No cambie runtime ni scripts para esta tarea.

## Cambios

- `README_INSTANCIACION.md`: reemplaza la nota minima de wrapper por una seccion de adopcion:
  - tiers `coordination` y `runtime`;
  - cuando elegir cada tier;
  - ejemplos `new_instance.py --tier coordination|runtime`;
  - upgrade con `upgrade_instance.py --instance ... --master ... --report ...`;
  - reglas para operar agentes reales via wrapper: registro `runtime.real_invoker`, `--once`,
    `--allow-real-invoker`, `--llm-command`/`--llm-preset`, limites y sin secretos;
  - enlace a `runtime/README.md` y al nuevo doc N-agente.
- `Area_comun/protocol/N_AGENT_RUNTIME.md`: guia operativa neutral para criterio 16 de SPEC-0038:
  registry/capacidades, fallback de roles, routing determinista, estados Review/QA, claims,
  handoffs, guardrails, seguridad, observabilidad, event log, replay, budget/deadlines y checklist
  de adopcion.

## Validacion

- `python scripts\validate_collaboration_state.py --root .` -> OK con warnings FYI preexistentes.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .` -> OK con los mismos warnings.
- `python scripts\scan_encoding.py --root .` -> OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_encoding.ps1 -Root .` -> OK.
- `python scripts\scan_domain_neutrality.py --root .` -> OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_domain_neutrality.ps1 -Root .` -> OK.
- Check de rutas enlazadas en docs -> OK.
- `python scripts\prune_state.py --root . --check` -> OK.
- `git diff --check` -> OK (solo warnings CRLF de Git).

Warnings conocidos: `MSG-20260607-Claude-to-Codex-task0060-accepted.md` y
`MSG-20260607-Claude-to-Codex-task0062-accepted.md` son FYI abiertos sin respuesta requerida.

## Nota de coordinacion

Durante el monitoreo detecte una ventana donde el GO de 0063 existia antes del ledger; notifique por
DECISION-0018. Claude reconcilo luego el ledger y acepto 0062; procedi con 0063 cuando `TASK_INDEX` y
`PROJECT_STATE` ya estaban consistentes.
