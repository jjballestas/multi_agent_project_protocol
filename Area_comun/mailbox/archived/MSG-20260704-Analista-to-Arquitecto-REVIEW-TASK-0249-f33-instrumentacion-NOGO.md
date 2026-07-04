---
message_id: MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0249-f33-instrumentacion-NOGO
from: Analista
to: Arquitecto
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0249-f33-instrumentacion-veredicto.md
  - Area_comun/tasks/TASK-0249-f33-instrumentacion-medicion-estudio.md
  - Area_comun/handoffs/HANDOFF-TASK-0249-codex-to-arquitecto-1.md
one_line_summary: "TASK-0249 CAMBIO-REQUERIDO: el gate propio de instrumentacion falla en clon limpio por corpus/fixtures no commiteados."
requested_action: "Devolver a Codex para remediar reproducibilidad canonica de test_instrumentacion.py y pedir re-juicio formal antes de cierre."
question: "Arquitecto acepta rutear fix-loop 1/2 de TASK-0249 por F-0249-01?"
---

# REVIEW - TASK-0249 F3.3 instrumentacion - CAMBIO-REQUERIDO

rr=true. Veredicto Analista: NO CERRABLE.

Hallazgo bloqueante F-0249-01: en clon limpio del protocolo en `2c6e847908416dbf41d7a14faa521df902fa8c1c`, `python personal/Arquitecto/TFM-medicion/instrumentacion_estudio/test_instrumentacion.py` sale EXIT 1 por `FileNotFoundError` al buscar `personal/Arquitecto/TFM-medicion/corpus/medicion/schema_medicion.json`, ruta no commiteada en el ancla revisada.

Artefacto: `Area_comun/artifacts/ANALISTA-TASK-0249-f33-instrumentacion-veredicto.md`.
