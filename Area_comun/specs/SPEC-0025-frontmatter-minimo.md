---
spec_id: SPEC-0025-frontmatter-minimo
task_id: TASK-0025
type: implementation
status: ready
linked_decisions: [DECISION-0008, DECISION-0005, DECISION-0001]
created_at: 2026-06-05
author: Claude
---

# SPEC-0025 — Frontmatter de mailbox mínimo

## Contexto
DECISION-0008 §3: el frontmatter del mailbox es 65% relleno (ratio 1,9); muchos campos van
`none`/vacíos. Un set mínimo + omitir vacíos reduce el overhead manteniendo trazabilidad. Ver
[DISENO-eficiencia-de-tokens.md](../artifacts/DISENO-eficiencia-de-tokens.md) §3. Complementa DECISION-0005.

## Alcance
- `Area_comun/protocol/MAILBOX_MESSAGE_TEMPLATE.md`: variante mínima + regla de omisión.
- `validate_collaboration_state.py`/`.ps1`: aceptar el set mínimo; no exigir campos omitidos.
- Golden cases en `examples/compact_comms_validation_cases/` (o nuevo) para mínimo y legacy.

## No-alcance
- No invalidar mensajes históricos (frontmatter completo sigue válido). No cambiar los **códigos** de
  tipo (DECISION-0005). No validar longitud.

## execution_pipeline
1. Definir set **obligatorio**: `message_id`, `type`, `task_id`, `from`, `to`, `status`,
   `one_line_summary`; condicional: `requires_response:true` ⇒ `requested_action` + `question`.
2. Regla de **omisión**: no emitir `response_owner`/`requested_action`/`question`/`*_refs`/
   `deadline_or_blocking_level`/`requires_response` cuando son `none`/vacíos/`false`-por-defecto.
3. Actualizar template con ejemplo mínimo (FYI ~7 líneas de frontmatter).
4. Validador: si falta un campo **omitible**, asumir su default (no error); mantener checks vigentes
   (open+requires_response:true ⇒ requested_action+question; soft-checks de higiene TASK-0021).
5. Golden cases: mensaje mínimo válido; mensaje legacy completo válido; medir delta con SPEC-0023.

## acceptance_criteria
- Mensaje con set mínimo ⇒ válido (sin ERROR) en `.py` y `.ps1`.
- Campos omitidos asumen default; no se exigen.
- Mensajes legacy (frontmatter completo) siguen válidos.
- Checks existentes intactos (requires_response, higiene mailbox).
- Overhead frontmatter medido baja (objetivo ~35% relleno); reportado before/after.

## linked_decisions
- `DECISION-0008` §3 (fuente); `DECISION-0005` (no rompe códigos/compacidad); `DECISION-0001`
  (aditivo ⇒ MINOR; cambiar obligatorios sería MAJOR).

## test_plan
- Golden cases mínimo/legacy en `.py`/`.ps1` (paridad); `measure_context_cost` antes/después.
- root + ejemplos existentes siguen verdes.

## closure_criteria
- Template mínimo + validador compatible hacia atrás; golden cases verdes con paridad; delta medido;
  revisión del arquitecto OK; claim liberado.

## Risks
- Omitir campos que algún check usa ⇒ falsos negativos. Mitigación: el set obligatorio cubre lo que
  el validador parsea; los omitibles tienen default seguro.

## Traceability
| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| Set mínimo válido | TASK-0025 | golden mínimo .py/.ps1 | sin ERROR |
| Back-compat legacy | TASK-0025 | golden legacy | válido |
| Overhead baja medido | TASK-0025 | measure antes/después | delta en handoff |
