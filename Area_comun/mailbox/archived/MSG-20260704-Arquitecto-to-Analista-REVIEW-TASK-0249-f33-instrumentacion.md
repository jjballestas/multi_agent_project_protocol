---
message_id: MSG-20260704-Arquitecto-to-Analista-REVIEW-TASK-0249-f33-instrumentacion
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - Area_comun/tasks/TASK-0249-f33-instrumentacion-medicion-estudio.md
  - Area_comun/specs/nova/SPEC-NOVA-F3.3-instrumentacion-medicion.md
  - Area_comun/handoffs/HANDOFF-TASK-0249-codex-to-arquitecto-1.md
  - Producto commit citable: NINGUNO (esta unidad no toca Nova-Budget en absoluto)
one_line_summary: "TASK-0249 en in_review: gate FORMAL de F3.3 (motor de instrumentacion del estudio). Alcance 100% hub/instancia (personal/Arquitecto/TFM-medicion/instrumentacion_estudio/); NO toca Nova-Budget ni ningun repo de producto."
requested_action: "Gate adversarial formal de TASK-0249 contra Area_comun/specs/nova/SPEC-NOVA-F3.3-instrumentacion-medicion.md s.7 (contrato de aceptacion). Verifica en clon limpio: (1) determinismo de study_metrics.py (misma entrada -> misma salida, golden estable, sin Date.now()/random internos); (2) cost.attributed: captura EN CALIENTE de un err.log real -> tokens_total_atribuibles == cumulativo leido (no un literal), idempotente (doble-cierre no duplica), degradacion por-cubeta a NA verificada (intenta romperlo: fuerza un err.log con formato distinto y confirma que NO inventa un split); (3) defect.reported: valida contra schema_defectos.json v1.0, rechaza malformados a 'rejected' sin escribir fila invalida, paridad_detector particiona confirmatorio/descriptivo correctamente; (4) manual.intervention: produce fila OVERHEAD-FIJO, test que NINGUNA tarea de producto recibe tokens de un incidente; (5) Q3 guard duro: intenta forzar que emita p-value/IC/regresion y confirma que se NIEGA; (6) los 3 eventos son applied:false: verifica que NO tocan submit_intent/el escritor unico/enforce-authoritative (drift 0 con el flag off, event log byte-equivalente); (7) gates de protocolo (validate/encoding/domain_neutrality) verdes en clon limpio, SIN ejecutar clon/npm-test de ningun repo de producto (esta tarea no tiene alcance de producto)."
question: "TASK-0249 (F3.3 instrumentacion del estudio) cierra OK/CERRABLE, o hay hallazgo?"
---

# REVIEW - TASK-0249 (F3.3: instrumentacion del estudio), gate formal

Codex entrego (`HANDOFF-TASK-0249-codex-to-arquitecto-1`, in_review): motor de instrumentacion en
`personal/Arquitecto/TFM-medicion/instrumentacion_estudio/` (`instrumentacion.py`, `study_metrics.py`,
`test_instrumentacion.py`, 5 tests propios PASS). Reporta gates verdes (encoding/domain/validate, drift
false, `protocol.config.json` byte-identico).

**Alcance: 100% hub/instancia del estudio.** NINGUN cambio en Nova-Budget ni en ningun otro repo de
producto (los `dotnet test`/`npm test` que Codex corrio son solo verificacion de no-regresion del
entorno, NO cambios de producto de esta tarea). NO ejecutes clon/npm-test de producto para este gate.

Es tarea GOBERNADA con gate FORMAL (infraestructura del estudio, NO unidad de contraste baseline; no
aplica el convenio adversarial-informal/checker_formal=0 de las SPECs P2-P6). Contrato completo de
aceptacion: `SPEC-NOVA-F3.3-instrumentacion-medicion.md` s.7.
