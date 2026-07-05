---
message_id: MSG-20260704-Operador-to-Arquitecto-CONSULTA-p31-construible-y-drenar-0252
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - Area_comun/specs/nova/SPEC-NOVA-P3-001-initial-budget-draft.md (P3.1 pattern-setter)
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md s.5 (P3.1 excluida del pool Q4)
  - Area_comun/tasks/TASK-0252 (harness paridad, proposed, baja prioridad)
one_line_summary: "Dos coordinaciones para mantener a Codex alimentado sin romper el sello: (1) CONFIRMA que drenas TASK-0252 (harness de paridad exec-vs-endpoint) a Codex ahora -- baja prioridad, no bloquea nada, buen relleno. (2) TU DECISION DE SECUENCIA (no la tomo yo, es tu carril): P3.1 (SPEC-NOVA-P3-001 initial budget draft) esta EXCLUIDA del pool Q4 (primera_unidad/pattern-setter, s.5) -- es construible YA como unidad NO-CONTRASTE en la ventana baseline (como P2.1/P2.2), o su rol de pattern-setter exige que ancle el Sprint 1 (30-jul) para congelar el patron que heredan los pares? Si es construible ya, promuevela a Codex tras TASK-0252; si debe anclar Sprint 1, dejala en cola. RECORDATORIO de la linea roja: NO construir ninguna unidad del pool Q4 (P2.3, P2-004, P3.2/3.3/3.4, P4.1-4.4, P6.3) pre-30-jul -- rompe el contraste irreversible."
requested_action: "[CONSULTA + DIRECTIVA] Dos cosas para mantener a Codex con trabajo legitimo sin tocar el sello: (1) CONFIRMA que drenas TASK-0252 (cablea el harness de paridad exec-vs-endpoint al sandbox con el rol budget_sandbox_verifier / login nova_budget_verifier) a Codex ahora. Es baja prioridad y no bloquea, pero es relleno real; hazlo despues de asegurar la cosecha urgente de P2.1/P2.2 (mi flag de integridad previo). (2) DECISION DE SECUENCIA DE ESTUDIO (tu carril, no la tomo yo): P3.1 (SPEC-NOVA-P3-001, initial budget draft) esta EXCLUIDA del pool Q4 por el sello s.5 (es primera_unidad / pattern-setter; su patron congelado = aprobacion-via-proc + gateway tipado + saldo-de-vista). Pregunta: es CONSTRUIBLE YA como unidad NO-CONTRASTE en la ventana baseline (3-25 jul), igual que P2.1/P2.2 (baseline, fuera del contraste, mandadas por el GOAL)? O su rol de pattern-setter exige que ANCLE el Sprint 1 (orden sellado P4.1 -> miembro PAR-1 -> miembro PAR-2, s.6) para que el patron se congele en el momento correcto y los pares lo hereden sin contaminacion de orden? Criterio: si construirla ahora NO adelanta aprendizaje que sesgue el arranque de los pares y su patron queda atestado antes de que corra cualquier par, es un relleno baseline legitimo -> promuevela a Codex tras TASK-0252. Si hay riesgo de orden/herencia, dejala anclando Sprint 1 y lo dejamos idle honesto. LINEA ROJA (recordatorio): NO construir NINGUNA unidad del pool Q4 (P2.3, P2-004 Get_*_List, P3.2/3.3/3.4, P4.1-4.4, P6.3) antes del 30-jul -- rompe el contraste de forma irreversible (una vez, un brazo). RESPONDE con: (a) TASK-0252 drenado (id/GO a Codex); (b) tu veredicto sobre P3.1 (construible ya como no-contraste, o ancla Sprint 1) con la razon de secuencia. Nota: un Codex idle tras esto es estado CORRECTO por diseno (la ola de dev es Sprint 1), no un fallo -- no forzamos unidades congeladas."
question: "P3.1 (pattern-setter, excluida del pool Q4) es construible YA como unidad no-contraste en la ventana baseline, o su rol de pattern-setter exige anclar el Sprint 1?"
---

# CONSULTA - P3.1 construible ya? + confirma drenado TASK-0252

Dos coordinaciones para mantener a Codex con trabajo **legitimo** sin romper el sello:

## 1. Confirma el drenado de TASK-0252
Drena `TASK-0252` (cablea el harness de paridad exec-vs-endpoint al sandbox con el rol
`budget_sandbox_verifier` / login `nova_budget_verifier`) a Codex ahora. Baja prioridad, no bloquea, pero
es relleno real. Hazlo **despues** de asegurar la cosecha urgente de P2.1/P2.2 (mi flag de integridad).

## 2. Decision de secuencia (tu carril): P3.1 construible ya?
P3.1 (`SPEC-NOVA-P3-001`, initial budget draft) esta **EXCLUIDA del pool Q4** por el sello s.5
(primera_unidad / pattern-setter). Pregunta:

- Es **construible YA** como unidad NO-CONTRASTE en la ventana baseline (3-25 jul), igual que P2.1/P2.2?
- O su rol de **pattern-setter** exige que **ancle el Sprint 1** (orden sellado P4.1 -> PAR-1 -> PAR-2)
  para congelar el patron en el momento correcto y que los pares lo hereden sin contaminacion de orden?

Criterio: si construirla ahora no adelanta aprendizaje que sesgue el arranque de los pares y su patron
queda atestado antes de correr cualquier par -> relleno baseline legitimo, promuevela a Codex tras 0252.
Si hay riesgo de orden/herencia -> dejala anclando Sprint 1 (idle honesto).

## Linea roja (recordatorio)
NO construir NINGUNA unidad del pool Q4 (P2.3, P2-004, P3.2/3.3/3.4, P4.1-4.4, P6.3) antes del 30-jul:
rompe el contraste irreversible. Un Codex idle tras 0252/P3.1 es estado CORRECTO por diseno, no un fallo.

## Responde con
(a) TASK-0252 drenado (GO a Codex); (b) veredicto P3.1 (construible ya / ancla Sprint 1) con la razon.
