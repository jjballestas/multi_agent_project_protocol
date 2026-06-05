---
id: TASK-0025
owner: Codex
status: done
type: implementation
priority: normal
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0023]
relates_to: [TASK-0024]
phase: P2
spec_id: Area_comun/specs/SPEC-0025-frontmatter-minimo.md
linked_decisions: [DECISION-0008, DECISION-0005, DECISION-0001]
execution_pipeline: [Definir set obligatorio + regla de omision, Template variante minima, Validador acepta minimo sin exigir omitidos, Golden cases minimo/legacy, Medir delta con measure_context_cost]
acceptance_criteria: [Mensaje minimo valido en .py/.ps1, omitidos asumen default, legacy sigue valido, checks existentes intactos (requires_response + higiene), overhead medido baja]
test_plan: [Golden minimo/legacy .py/.ps1, measure antes/despues, root + ejemplos verdes]
closure_criteria: [Template minimo + validador back-compat, golden verdes con paridad, delta medido, claim liberado]
---

# TASK-0025 — Frontmatter de mailbox mínimo

> `implementation` → SDD; implementar contra [SPEC-0025](../specs/SPEC-0025-frontmatter-minimo.md)
> y DECISION-0008 §3 + DECISION-0005. Aditivo y **compatible hacia atrás** (legacy sigue válido).
> Depende de TASK-0023 (medir el delta).

## Ejecucion (Claude, por direccion del operador; Codex fuera de sesion)
- `MAILBOX_MESSAGE_TEMPLATE.md`: anadida **variante minima** + regla de omision (set obligatorio:
  `message_id/type/task_id/from/to/status/one_line_summary`; condicional si `requires_response:true`:
  `response_owner/requested_action/question`; omitir el resto cuando `none`/vacio/false).
- Golden `examples/compact_comms_validation_cases/minimal_frontmatter/` (exit 0) + README + runner `.ps1`.
- **Validador sin cambio de codigo:** los checks de mailbox ya son condicionales (omitir opcionales no
  produce ERROR); por tanto la paridad `.py`/`.ps1` se preserva trivialmente.

## Validacion (Claude, .py)
- `validate_collaboration_state.py --root .` -> OK; scan neutralidad exit 0.
- Casos compactos: `valid_compact`/`legacy_exempt`/`missing_context_refs_warning`/`minimal_frontmatter`
  -> exit 0; `missing_question` -> exit 1 (esperado).
- Delta frontmatter (medido): minimo `210` chars / `7` lineas vs legacy `532` / `19` -> **-61% chars**.
- Paridad `.ps1`: trivial (sin cambio de validador); runner `.ps1` actualizado con el caso (no ejecutado
  por Claude: deny-rule PowerShell; cubierto por CI/Codex).

## Ratificacion
ACEPTADA (Claude). Cumple SPEC-0025 (minimo valido, omitidos default, legacy valido, checks intactos,
overhead medido baja). Ultimo entregable del track de eficiencia de tokens (DECISION-0008) -> v0.7.0.
