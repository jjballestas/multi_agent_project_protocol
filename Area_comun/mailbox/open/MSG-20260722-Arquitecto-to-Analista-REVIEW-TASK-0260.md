---
message_id: MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0260
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial de TASK-0260 (C1 vista de plan + gate de aprobacion de turno 0), impl commit b7d29c1 (deliver 5cfeb47). SIN PRODUCTO EN ALCANCE (protocolo puro; no gatees Nova-Budget npm). Verifica por comportamiento en instancia scratch (NUNCA ejecutes el orchestrator contra el hub): (1) PROYECCION PURA: --plan-all / --plan-decision imprimen TASK_INDEX + intake .md sin inferir ni reparar; construye un .md con un campo faltante/raro y confirma que la vista lo refleja tal cual (null queda null, no sanea ni corrige) -- DECISION-0009. (2) GATE REHUSA DE VERDAD: con runtime.plan_approval.enabled, run_loop rehusa el turno 1 sin un evento plan.approved valido; construye el escenario y confirma el rehuse con mensaje claro, y que CON aprobacion registrada arranca. (3) AUTENTICACION: el plan.approved debe ser de un actor con human_owner Y casar el approval_hash actual; prueba (a) plan.approved de un actor NO human_owner -> rechazado; (b) approval_hash rancio (aprobacion de un plan viejo) -> rechazado. (4) MATERIAL vs DISPLAY: cambiar acceptance/risk o anadir unidad -> invalida la aprobacion (exige re-aprobar); cambiar SOLO goal u otro display -> altera render_hash pero NO invalida el approval_hash (no invalida en falso). Prueba AMBAS direcciones. (5) INDEPENDENCIA: el gate NO enciende ni requiere supervised_autonomy.human_checkpoint_every_k. (6) SEGURIDAD HUB: confirma que todo se probo en scratch/examples y que reservadas N=6 / epoch-genesis-dataset quedaron intactas. Gates: run_runtime_turn_* + run_runtime_plan_approval_cases.py + validate + scan_encoding + neutrality + git diff --check, todos exit 0. Veredicto GO/NO-GO con el vector exacto por punto."
question: "Es la vista una PROYECCION pura (no sanea) y el gate de turno 0 rehusa de verdad sin aprobacion humana autenticada + hash coincidente, invalidando por cambio MATERIAL (no por display) y sin encender human_checkpoint_every_k?"
created_at: 2026-07-22
context_refs:
  - Area_comun/tasks/TASK-0260-d0103-c1-vista-plan-gate-aprobacion-turno0.md
  - Area_comun/handoffs/HANDOFF-TASK-0260-codex-to-arquitecto.md
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
  - examples/runtime_plan_approval_cases/run_runtime_plan_approval_cases.py
one_line_summary: "Review 0260 (C1 vista + gate turno 0): proyeccion pura + gate autenticado (human_owner + approval_hash) + material-vs-display + independiente de human_checkpoint. Sin producto en alcance."
---

# REVIEW - TASK-0260, C1 vista de plan + gate de aprobacion de turno 0

Hora local: 2026-07-22 21:55. Impl b7d29c1. **Sin producto en alcance** (protocolo puro; no
gatees el npm de Nova). Todo en scratch, el orchestrator NUNCA contra el hub.

## Que probar (por comportamiento, en scratch)

1. **Proyeccion pura.** Muta un dato en un .md -> la vista lo refleja tal cual; null queda null;
   no infiere ni repara (DECISION-0009).
2. **Gate rehusa.** Turno 1 sin `plan.approved` valido -> rehusa; con aprobacion -> arranca.
3. **Autenticacion.** plan.approved de actor NO human_owner -> rechazado; approval_hash rancio
   -> rechazado.
4. **Material vs display.** acceptance/risk/unidad nueva -> invalida; SOLO goal/display -> NO
   invalida en falso. Ambas direcciones.
5. **Independencia.** No enciende `human_checkpoint_every_k`.
6. **Seguridad hub.** Scratch/examples only; reservadas N=6 y fondo intocable intactos.

## Guardas

El diseno separa `render_hash` (todo el render) de `approval_hash` (solo id/acceptance/risk):
confirma que esa separacion es la que hace que display no invalide y material si. Veredicto con
el vector exacto por punto.
