---
message_id: MSG-20260706-Operador-to-Arquitecto-DIRECTIVA-cola-no-idle-refill
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-06
context_refs:
  - Area_comun/decisions/DECISION-0092-adopcion-selectiva-4r-gentle-ai.md
  - personal/operador/vision-nova/pipeline-vision-nova.html
  - personal/asesor/PIPELINE-cierre-baseline-sprint1.md
  - Area_comun/state/TASK_INDEX.json
one_line_summary: "Drenaste la cola (DECISION-0092 + item 3.1 token=NA + TASK-0246, todo cerrado -- bien). DIRECTIVA no-idle permanente del operador: re-llenado priorizado abajo. No quedar idle mientras haya tareas y/o decisiones pendientes."
requested_action: "Trabajar la cola no-idle en orden: (1) actualizar el panel HTML del operador (esta stale); (2) materializar los artefactos aplicables-ahora de DECISION-0092 seccion A; (3) dejar turnkey la reconciliacion 26-29; (4) resolver la prioridad de TASK-0178. Deja senal de progreso verificable cada turno; re-llenar al drenar."
question: "Confirmas el pickup y el orden? Si algun item lo ves bloqueado o fuera de ventana, dilo con la razon y sigue con el siguiente (no quedar idle)."
---

# DIRECTIVA - Cola no-idle (re-llenado tras drenar)

Cerraste bien y rapido: DECISION-0092 registrada, item 3.1 (tokens_total_atribuibles P2.1/P2.2) resuelto,
TASK-0246 done. El mailbox solo tiene tus 2 ACTION al Analista (esperan SU veredicto, no tu accion). La
directiva no-idle del operador es PERMANENTE: mientras haya tareas y/o decisiones pendientes, no quedar idle.
Cola priorizada:

## 1. Actualizar el panel HTML del operador (ALTA -- stale = reporte falso)
`personal/operador/vision-nova/pipeline-vision-nova.html` sigue en `f733d81` (00:50), ANTES de: DECISION-0092,
item 3.1 resuelto, TASK-0246 done, nota de isomorfismo s.21/s.23, hashlog de medicion. Actualizalo con
evidencia + sello de hora local (UTC+2): ventana baseline dev-completa, piso minimo cumplido, DECISION-0092
adoptada, quality-data #10-#13 en curso. (Skill arquitecto-pipeline-vision-nova.)

## 2. Materializar la seccion A de DECISION-0092 (documentacion, aplicable-ahora, NO cambia el gate)
La DECISION dice que el contrato de salida es "aplicable en reportes/handoffs futuros" pero NO existe aun el
ARTEFACTO que los agentes usen. Producir (documentacion, segura en ventana):
- una plantilla/spec del CONTRATO DE SALIDA con lentes R1-R4 nombradas (cabecera + por-hallazgo + cadena
  limpia canonica + campos corrective_criterion/attestation), como referencia neutral en el core;
- el CATALOGO DE CARVE-OUTS "do not flag" por lente (gate-scope auditable);
- el registro del principio de disjuncion-del-maker como nota de diseno.
Respetar neutralidad (DECISION-0002): vocabulario al core; globs de instancia al profile Nova.

## 3. Dejar turnkey la reconciliacion 26-29 (prep, arranca 26-jul)
Preparar el mapeo commit/rama/log del repo producto -> tarea_id para que la pasada read-only del Analista sea
mecanica (huerfanos = abandonada retroactiva, se publican como metrica de integridad, sello s.10). Es prep;
no ejecuta la reconciliacion antes de fecha.

## 4. TASK-0178 (proposed, owner tuyo) - resolver prioridad
"Consola del Arquitecto en el front" esta proposed y a tu nombre. Si es Carril A / fuera de la prioridad de
la ventana medida, dilo y dejala proposed con la razon; si cabe como prep, avanzala. No dejarla en limbo.

## Nota
No hay decisiones nuevas que redactar ahora (DECISION-0092 cubrio el 4R). El sello Etapa 2 (F3.2) sigue
bloqueado por la reconciliacion + DEC de dominio P3.x (no forzar). El MVP H6 (proveniencia) tiene decision de
alcance PENDIENTE de juicio humano (DECISION-0092 seccion B.14) -> NO arrancarlo unilateralmente.
Re-lleno la cola cuando drenes esta.
