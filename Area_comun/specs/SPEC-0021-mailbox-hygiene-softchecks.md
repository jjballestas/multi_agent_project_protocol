---
spec_id: SPEC-0021-mailbox-hygiene-softchecks
task_id: TASK-0021
type: implementation
status: ready
linked_decisions: [DECISION-0005, DECISION-0006, DECISION-0001]
created_at: 2026-06-05
author: Claude
---

# SPEC-0021 — Soft-checks de higiene de mailbox

## Contexto
DECISION-0005 manda cerrar el loop con un código y **archivar** (`open/` → `answered/`) los mensajes
resueltos, pero nada lo **verifica**: mensajes resueltos quedan en `open/` y solo se detectan mirando
la carpeta a mano (gap real observado en sesión). Esta tarea hace esa disciplina verificable, suave y
aditiva (estilo TASK-0014).

## Alcance
- `scripts/validate_collaboration_state.py` y `.ps1` (paridad): soft-checks sobre `Area_comun/mailbox/open/`.
- Golden cases en `examples/mailbox_hygiene_cases/` (o reutilizar patrón de `compact_comms_validation_cases`).

## No-alcance
- **No** mover/archivar automáticamente (solo avisar).
- **No** errores: todo es WARNING (no rompe estado ni históricos).
- No tocar la lógica de validación existente (estado/SDD/perfiles/compacta).

## execution_pipeline
1. En ambos validadores, para cada `.md` en `Area_comun/mailbox/open/`:
   - WARNING si `status` ∈ {`answered`, `archived`} → "mensaje resuelto en open/; archivar a answered/".
   - WARNING si `type` ∈ {`ACK`, `FYI`} y `requires_response: false` → "no requiere respuesta; considerar archivar".
2. Mensajes con `status: open` y `requires_response: true` no se avisan (hilo legítimamente abierto).
3. Heurística conservadora: ante ausencia de campos, no avisar (compatibilidad con históricos).
4. Golden cases: open legítimo (sin warning); open con status answered (warning); FYI/ACK sin respuesta (warning).
5. Paridad `.py`↔`.ps1`; root y ejemplos existentes siguen verdes (sin nuevos errores). Handoff.

## acceptance_criteria
- `open/` con `status: answered|archived` ⇒ WARNING en `.py` y `.ps1` (exit 0, no error).
- `open/` con `type: ACK|FYI` + `requires_response:false` ⇒ WARNING.
- `open/` con `status: open` + `requires_response:true` ⇒ sin warning.
- Mensajes legacy sin campos nuevos no generan ruido.
- Paridad `.py`↔`.ps1`; root + ejemplos existentes verdes.

## linked_decisions
- `DECISION-0005`: define el archivado del loop; esta tarea lo hace verificable.
- `DECISION-0006`: convierte disciplina confiada a memoria en gate operativo.
- `DECISION-0001`: aditivo (solo WARNING) ⇒ MINOR; endurecer a ERROR sería MAJOR.

## test_plan
- Golden harness de mailbox (presencia/ausencia de WARNING por caso; paridad `.py` vs `.ps1`).
- `.py` y `.ps1` sobre root + ejemplos existentes ⇒ sin nuevos errores.

## closure_criteria
- Golden cases pasan en ambos validadores; paridad; root/ejemplos verdes.
- Handoff mapea criterios a evidencia; revisión cruzada del arquitecto OK; claim liberado.

## Risks
- Falsos positivos si un agente usa `status: open` como borrador. Mitigación: solo avisar en los
  patrones claros de §1; nunca error.

## Traceability
| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| WARN resuelto en open/ | TASK-0021 | golden status=answered | warning en .py/.ps1 sin error |
| WARN FYI/ACK sin respuesta en open/ | TASK-0021 | golden FYI | warning emitido |
| No ruido en históricos/legítimos | TASK-0021 | golden open+requires_response | sin warning |
