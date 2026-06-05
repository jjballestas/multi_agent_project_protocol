---
handoff_id: HANDOFF-TASK-0025-claude-to-codex-1
task_id: TASK-0025
from: Claude
to: Codex
status: done
requires_response: false
response_owner: none
created_at: 2026-06-05
---

# HANDOFF TASK-0025 - Frontmatter de mailbox minimo

> Implementado por Claude por direccion del operador (Codex fuera de sesion). Para tu ratificacion
> cuando vuelvas: la paridad `.ps1` es trivial (no hubo cambio de validador).

## Delta
- `Area_comun/protocol/MAILBOX_MESSAGE_TEMPLATE.md`: seccion **"Minimal frontmatter"** (set obligatorio
  + regla de omision + ejemplo FYI minimo).
- `examples/compact_comms_validation_cases/minimal_frontmatter/`: golden (exit 0) + README + caso en el
  runner `.ps1`.
- **Sin cambio en `validate_collaboration_state.py/.ps1`:** los checks de mailbox ya son condicionales
  (omitir campos opcionales no produce ERROR; `requires_response:true` sigue exigiendo
  `response_owner`/`requested_action`/`question`). Back-compat total.

## Evidencia (.py)
- `validate_collaboration_state.py --root .` -> OK; `scan_domain_neutrality.py` -> exit 0.
- Casos: `valid_compact`/`legacy_exempt`/`missing_context_refs_warning`/`minimal_frontmatter` -> 0;
  `missing_question` -> 1.
- Delta frontmatter: minimo `210` chars / `7` lineas vs legacy `532` / `19` -> **-61% chars**.

## Pendiente para Codex (no bloqueante)
- Ratificar la paridad `.ps1` corriendo `run_compact_comms_cases.ps1` (incluye el caso nuevo) en tu
  entorno PowerShell; deberia pasar sin cambios (no se toco el validador).
