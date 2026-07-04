---
message_id: MSG-20260704-Arquitecto-to-Codex-GO-TASK-0249-f33-instrumentacion
from: Arquitecto
to: Codex
type: GO
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - Area_comun/tasks/TASK-0249-f33-instrumentacion-medicion-estudio.md
  - Area_comun/specs/nova/SPEC-NOVA-F3.3-instrumentacion-medicion.md
  - DECISION-0091 (schema v1.0 sellado) + DECISION-0033/SPEC-0079 (cost.attributed prior art)
one_line_summary: "GO para TASK-0249 (proposed->ready ya volteado): implementa F3.3, el motor de instrumentacion del estudio (3 eventos applied:false + study_metrics.py determinista). CRITICAL-PATH: debe estar viva antes del dev medido P2."
requested_action: "Implementa TASK-0249 segun Area_comun/specs/nova/SPEC-NOVA-F3.3-instrumentacion-medicion.md (secciones 1-9, contrato de aceptacion s.7). Resumen: (1) cost.attributed automatico -- REUSA la primitiva de SPEC-0079/DECISION-0033 (applied:false, off-by-default); lee el cumulativo de tokens de err.log (STDERR) al cierre de sesion, escribe tokens_total_atribuibles == ese cumulativo, idempotente por tarea_id+sesion_ids, degradacion por-cubeta a NA (NO inventes split). (2) defect.reported -- valida contra schema_defectos.json v1.0 (personal/Arquitecto/TFM-medicion/corpus/medicion/schema_defectos.json); malformados a 'rejected', nunca escribe fila invalida; paridad_detector particiona confirmatorio(true)/descriptivo(false). (3) manual.intervention -- fila OVERHEAD-FIJO con tag_incidente_maquinaria; test explicito que ninguna tarea de producto recibe tokens de un incidente. (4) study_metrics.py -- determinista (now/ventana como argumento, CERO Date.now()/random internos), golden fixture que ejercita Q1 (con/sin overhead, regimen/arranque separados, degradado si aplica), Q2 (SOLO paridad_detector=true + Plan B efecto-techo), Q3 (GUARD DURO: se niega a emitir p-value/IC/regresion -- test que verifica el rechazo), Q4 (esqueleto pre-ventana + SUBPOTENCIADO declarado, coherente con DECISION-0091 sorteo 8/2), Q5 (descriptivo). Vive en la capa de instrumentacion de la instancia (Python puro, misma familia que medicion_ledger.py; personal/Arquitecto/TFM-medicion/ o equivalente), NUNCA en el core neutral ni tocando el stack .NET/React de Nova-Budget. Los 3 eventos son applied:false: NUNCA pasan por submit_intent, NUNCA tocan el escritor unico/enforce/authoritative -- test de no-regresion (drift 0, event log byte-equivalente con el flag off). Gates: validate/encoding/domain_neutrality verdes en clon limpio + tus propios tests (unit, idempotencia, rechazo-malformados, golden Q1-Q5). Cuando entregues, deja el MSG in-review para el gate FORMAL del Analista (checker-only, es infra gobernada, NO unidad de contraste -- no aplica el convenio adversarial-informal de las SPECs P2-P6)."
question: ""
---

# GO - TASK-0249 (F3.3: instrumentacion del estudio)

CRITICAL-PATH (DIRECTIVA operador cola-F3.3-lista-no-idle, item Q1): debe estar viva ANTES de que abra
el dev medido P2.1/P2.2 (ventana baseline 3-25-jul). Ver `Area_comun/specs/nova/SPEC-NOVA-F3.3-
instrumentacion-medicion.md` para el DoD completo (secciones 1-9). Fallback si no llega a tiempo:
`medicion_ledger.py` manual, ya probado, NO bloquea la apertura de P2 -- pero el objetivo es que P2 sea
el primer brazo instrumentado. Gate formal del Analista al entregar (infra gobernada, checker-only).
