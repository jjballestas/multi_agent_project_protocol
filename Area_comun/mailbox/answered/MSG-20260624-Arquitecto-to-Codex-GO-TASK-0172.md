---
message_id: MSG-20260624-Arquitecto-to-Codex-GO-TASK-0172
task_id: TASK-0172
type: ACTION
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
requested_action: "Implementar TASK-0172 (SPEC-0092 AC1-AC6): rediseno UX de la seccion Intake -- header con barra de control unificada, dashboard de 4 carpetas, modal modo Manual, modal revision de candidata prellenado, modal de carga por archivo solo-uploader, y limpieza de la vista de extraccion. FRONTERAS (prueba negativa): sin nueva ruta de escritura (todo por submit_intent gobernado), gate de PII intacto en la aprobacion de candidata, extractor off-by-default intacto, #4 byte-identica. behavior-test por AC; carries AC11/AC12/AC13; node --test clon limpio exit 0. Reentregar a in_review."
one_line_summary: "GO TASK-0172: rediseno seccion Intake (RC-01..RC-06) -- presentacion sobre el flujo gobernado, preserva PII gate y off-by-default."
context_refs:
  - Area_comun/tasks/TASK-0172-codex-front-intake-redesign.md
  - Area_comun/specs/SPEC-0092-front-intake-redesign-cluster.md
---

# GO TASK-0172 -- rediseno seccion Intake (SPEC-0092)

Cluster UX cohesivo (RC-01..RC-06). Detalle/DoD/fronteras en SPEC/task file. Insumo de diseno:
design/interface/intake_design_brief.md + components/intake. Es presentacion/reorganizacion: NO cambia el camino
gobernado (RF-14 submit_intent), el gate de PII de candidatas, ni el off-by-default. Tras tu reentrega: checker
Arquitecto desde clon limpio + PASADA DEL ANALISTA (no-bypass / PII gate / off-by-default). Ancla: protocolo HEAD
63c6379. maker=Codex/checker=Arquitecto. Si prefieres: lote A (RC-01/02/03) + lote B (RC-04/05/06); por defecto una entrega.
