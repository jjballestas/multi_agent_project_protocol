---
id: TASK-0035
owner: Codex
status: in_progress
type: implementation
priority: high
created_at: 2026-06-06
updated_at: 2026-06-06
depends_on: []
relates_to: [TASK-0021, TASK-0033]
phase: P2
spec_id: Area_comun/specs/SPEC-0034-mailbox-status-folder-gate.md
linked_decisions: [DECISION-0013, DECISION-0006, DECISION-0005, DECISION-0001]
execution_pipeline: [extender validate_mailbox en validate_collaboration_state.py (.py/.ps1) para recorrer open/answered/archived y fallar si frontmatter status != carpeta, conservar el subcaso actual, golden examples/mailbox_status_cases (consistente/answered-con-open/open-con-answered), CI ya corre el validador]
acceptance_criteria: [mensaje en answered/ con status open => validador FALLA con ruta, idem archived/, mensaje en open/ con status answered/archived => falla, repo real verde tras limpieza, paridad py/ps1, sin regresion]
test_plan: [golden examples/mailbox_status_cases + paridad ps1 atestiguada + validador/scan verdes en repo real]
closure_criteria: [check folder<->status como error en validate_mailbox py+ps1 + golden verdes + repo real verde + handoff autocontenido + claim liberado al pasar a in_review]
---

# TASK-0035 - Gate de consistencia mailbox status<->carpeta

> `implementation` -> SDD; implementar contra [SPEC-0034](../specs/SPEC-0034-mailbox-status-folder-gate.md)
> bajo DECISION-0013 (visibilidad/integridad de coordinacion) + DECISION-0006 (robustez). **PRIORIDAD
> ALTA:** la coordinacion es el nucleo del proyecto; este invariante evita que mensajes archivados
> parezcan abiertos para siempre (riesgo de mal-enrutado en el loop autonomo M2). Aditivo, neutral.

## Resumen
Tres partes, todas sobre el invariante "status del frontmatter = carpeta":
1. **Gate:** extender `validate_mailbox` (.py/.ps1) para recorrer `open`/`answered`/`archived` y **fallar**
   si el `status` no coincide con la carpeta (hoy solo revisa `open/` y como warning).
2. **Fix de la fuente:** `prune_state` (TASK-0034) mueve mensajes a `archived/` SIN actualizar `status`
   (dejo 41 en `archived/` con `status: answered`). Arreglar `prune_state.py`/`.ps1` para que al mover
   normalice el `status` a la carpeta destino.
3. **Normalizacion one-time:** sincronizar los 41 (y cualquier otro) desfasados para dejar el repo verde.
Paridad `.py/.ps1`, golden, y entra al gate de CI existente.

## archivos objetivo (previstos)
- `scripts/validate_collaboration_state.py` (`validate_mailbox`) + `.ps1`
- `scripts/prune_state.py` + `.ps1` (normalizar status al mover)
- `examples/mailbox_status_cases/` (incluye caso prune->archived con status correcto)
- normalizacion de los mensajes desfasados en `Area_comun/mailbox/archived/`

## Contexto / por que
Causa raiz: mover-a-answered es manual y no verificado. Mismo patron que el resto de fallos de
coordinacion de la sesion (convencion sin gate). Hermano del check de handoff-release de TASK-0033.

## Dogfood
Aplica liveness (senal de progreso por turno) + handoff-release (libera el claim al pasar a in_review,
commitea WIP antes). ASCII-only en mailbox/state (DECISION-0012).
