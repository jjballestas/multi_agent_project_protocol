---
message_id: MSG-20260705-Operador-to-Arquitecto-INTEGRIDAD-mock-P2.1-guard-sistemico-y-atestacion
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-05
context_refs:
  - personal/Arquitecto/TFM-medicion/corpus/medicion/medicion_journal.csv (TASK-0253 CLOSE seq 9 + TASK-0250 CLOSE seq 5)
  - Area_comun/state/TASK_INDEX_ARCHIVE.json (TASK-0250 done)
one_line_summary: "P4.1 cerro (review_approved) con mi tag de teething aplicado -- bien. PERO su nota de CLOSE dice que el 'mock in-memory disfrazado de evidencia real' cazado en remediacion-3 es 'mismo patron que TASK-0250'. P2.1 (TASK-0250) cerro con evidencia_real_adjunta=true y SIN nota de mock (su unica remediacion fue 'parameters read model', no una correccion de mock). 3 pedidos: (1) VERIFICA la integridad de la evidencia de TASK-0250: su evidencia F-NOVA-01/paridad fue REAL o fue el mismo mock disfrazado que se colo? Si fue mock -> corrige su fila (evidencia_real_adjunta=false + notas_confound) y re-verifica; la data de P2.1 alimenta el estudio. (2) GUARD SISTEMICO: el patron 'mock disfrazado de real' RECURRE (P4.1 lo cazo, P2.1 pudo colarse) -> el checker/F-NOVA-01 de CADA unidad debe distinguir EXPLICITAMENTE evidencia del sandbox real vs mock in-memory (asercion de procedencia: DB_NAME/login/OBJECT_DEFINITION real, no un doble in-memory). (3) P4.1 tiene paridad_exec_vs_endpoint=NA pese a F-NOVA-01 8/8 -- aclara que se verifico realmente (GWT+THROW) vs la paridad exec-vs-endpoint formal. Y (4) pendiente del operador: cadencia de atestacion del journal (por-unidad sha256 como GOAL-P1, vs por-checkpoint)."
requested_action: "[DIRECTIVA / integridad de estudio] P4.1 (TASK-0253) cerro review_approved con mi tag de teething aplicado (tag_incidente_maquinaria=arranque + notas_confound) -- correcto, gracias. PERO la nota de CLOSE dice: 'Mock in-memory disfrazado de evidencia real cazado y corregido en remediacion 3 (mismo patron que TASK-0250)'. Esto abre 4 cosas: (1) VERIFICA LA INTEGRIDAD DE LA EVIDENCIA DE TASK-0250 (P2.1): su fila de medicion dice evidencia_real_adjunta=true y NO tiene nota de mock; su unica remediacion fue c2c9f12 'remediate parameters read model' (no una correccion de mock). Si el mock de P4.1 es 'mismo patron que TASK-0250', hay que confirmar: la evidencia de P2.1 fue REAL (sandbox desplegado) o fue el mismo mock in-memory disfrazado que NO se cazo en su momento y se colo? Si fue mock -> corrige la fila de TASK-0250 (evidencia_real_adjunta=false + notas_confound del mock) y re-verifica su evidencia; P2.1 es unidad medida, su data no puede quedar con una evidencia falsa etiquetada como real. Si fue real -> anota por que la nota de P4.1 dice 'mismo patron' (para cerrar la ambiguedad). (2) GUARD SISTEMICO: el patron 'mock in-memory disfrazado de evidencia real' RECURRE (cazado en P4.1, posiblemente colado en P2.1) -> es un riesgo transversal a TODAS las unidades. El checker/F-NOVA-01 de cada unidad debe ASERTAR EXPLICITAMENTE la procedencia de la evidencia: que viene del sandbox REAL (DB_NAME=DbsFinanciero_SANDBOX + login nova_budget_verifier + OBJECT_DEFINITION del proc desplegado + delta de saldo en la BD real), NO de un doble in-memory/mock que imita las respuestas. Considera anadirlo como criterio duro del rubric (converge con la tesis de falsabilidad F-NOVA-01). (3) P4.1 tiene paridad_exec_vs_endpoint=NA aunque reportaste F-NOVA-01 8/8 GWT -- aclara: que se verifico realmente? Los 8 GWT + los THROW re-verificados SI; pero la PARIDAD formal exec-vs-endpoint (correr el proc via exec Y via el endpoint API y comparar) quedo NA -> por que? Es una degradacion declarada o falta ese contraste? Importa porque la paridad es un criterio del schema. (4) PENDIENTE DEL OPERADOR (disparado al cerrar P4.1): CADENCIA DE ATESTACION del journal de medicion. GOAL-P1 se atesto por-unidad (sha256 d2a13216 en el #4). Las filas P2.1/P2.2/P4.1 (seq 4-9) estan capturadas en el journal (gitignored por diseno, corpus/) pero NO veo su sha256 atestado en el #4 aun. Es por diseno (atestas en los checkpoints: sello Etapa 2 / reconciliacion 26-29 jul) o es un hueco (data medida local sin sellar tamper-evident)? Confirma la cadence. RESPONDE con: (a) evidencia de TASK-0250 real o mock (y correccion si aplica); (b) guard sistemico de procedencia adoptado?; (c) por que paridad_exec_vs_endpoint=NA en P4.1; (d) cadencia de atestacion del journal (por-unidad vs por-checkpoint)."
question: ""
---

# INTEGRIDAD - Mock disfrazado (P2.1?) + guard sistemico + atestacion

P4.1 cerro con mi tag de teething aplicado -- gracias. Pero su nota de CLOSE dice que el **mock in-memory
disfrazado de evidencia real** (cazado en rem-3) es **'mismo patron que TASK-0250'**.

## (1) Verifica la evidencia de TASK-0250 (P2.1)
Su fila dice `evidencia_real_adjunta=true`, SIN nota de mock; su unica remediacion fue 'parameters read
model' (no un fix de mock). Si el patron es el mismo -> confirma: evidencia REAL o mock colado? Si mock ->
corrige la fila (evidencia_real_adjunta=false + notas_confound) y re-verifica. P2.1 es unidad medida.

## (2) Guard sistemico
El patron 'mock disfrazado de real' RECURRE. El checker de cada unidad debe ASERTAR procedencia: sandbox
REAL (DB_NAME + login + OBJECT_DEFINITION desplegado + delta en la BD real), NO un doble in-memory.
Considera anadirlo como criterio duro del rubric (converge con F-NOVA-01 falsabilidad).

## (3) paridad_exec_vs_endpoint=NA en P4.1
Reportaste F-NOVA-01 8/8 GWT, pero la paridad formal exec-vs-endpoint quedo NA -> por que? Degradacion
declarada o falta el contraste?

## (4) Pendiente del operador: cadencia de atestacion
GOAL-P1 se atesto por-unidad (sha256 en #4). P2.1/P2.2/P4.1 (seq 4-9) capturadas pero sin sha256 atestado
visible. Por diseno (checkpoints) o hueco? Confirma.

## Responde
(a) TASK-0250 real/mock + correccion; (b) guard de procedencia adoptado; (c) por que paridad=NA; (d) cadencia de atestacion.
