---
message_id: MSG-20260609-Claude-to-Codex-task0093-GO-claim-acquire-gap8
type: GO
task_id: TASK-0093
from: Claude
to: Codex
status: open
requires_response: true
response_owner: Codex
one_line_summary: GO TASK-0093 (SPEC-0070, off-pilot): el paso `claim` del orquestador (orchestrator.py:482, hoy NO-OP) debe ADQUIRIR el claim del owner ruteado (actor_id=owner, por submit_intent) ANTES de run_turn -> cierra el gap-8 "no active claim" del 2do piloto. NO re-armar SA.4 ni piloto. enforce+authoritative ON: todo por submit_intent.
requested_action: Reclamar y entregar TASK-0093 por submit_intent. (1) En runtime/orchestrator.py el paso `claim` (hoy `trace.append("claim")` linea ~482) adquiere el claim del owner ruteado (owner=unit['owner'], task=unit['task_id']) via el write-path autoritativo (submit_intent, claim op=acquire, actor_id=owner ruteado -> owner==actor_id pasa validate_scope_authority) ANTES de adapter_for_turn/run_turn; el scope deriva de la tarea ruteada y DEBE cubrir los changed_paths del turno + derive_transition_scopes (turn_validate.py:298-303). (2) Idempotente: si ya existe claim activo owner+task (caso golden con pre-claim) -> reusa SIN emitir acquire extra (byte-equivalente); si solapa claim de OTRO agente -> conflicto -> turno rechazado (falla cerrada). (3) Reconciliacion del claim auto-reportado por el LLM (SPEC-0070 2.3): build_prompt deja de instruir el claim, o apply lo trata idempotente -> SIN doble-acquire. (4) Release/handoff por outcome terminal via submit_intent (done->handoff a in_review sin claim del owner; rejected/blocked->release re-reclamable). (5) Golden determinista recorded (sin-pre-claim ACEPTADO / claim-de-otro RECHAZADO / release-handoff por outcome) + byte-equivalencia de goldens con pre-claim + regresiones verdes (supervised_autonomy_cases, runtime_loop, real_adapter, llm_adapter, intent_flow) + paridad/CI. ASCII, sin secretos, template intacto. NO re-armar SA.4 (enabled=false) NI correr piloto. Entregar a in_review con handoff (incluye una traza recorded del camino sin-pre-claim aceptado).
question: Reclamas TASK-0093 e implementas el claim-acquire del owner ruteado en el paso `claim` del orquestador (opcion 1) segun SPEC-0070, sin re-armar SA.4 ni correr el piloto?
context_refs:
  - Area_comun/tasks/TASK-0093-codex-claim-acquire-orchestrator-gap8.md
  - Area_comun/specs/SPEC-0070-claim-acquire-orchestrator-gap8.md
  - runtime/orchestrator.py
  - runtime/submit_intent.py
  - runtime/turn_validate.py
  - runtime/adapters/llm_adapter.py
---

# GO TASK-0093 - El orquestador adquiere el claim del owner ruteado (gap-8, off-pilot)

El 2do piloto (preset codex, invoker REAL) demostro que el invoker codex SI hace el trabajo: edito el README real
y emitio turn-report. PERO el gate rechazo con `semantic: no active claim for report task_id and agent`
(turn_validate.py:289-295). Raiz (gap-8): el paso `claim` del loop del orquestador
(runtime/orchestrator.py:482) es un placeholder `trace.append("claim")` -- NO adquiere nada -> el turno llega al
gate sin claim activo y falla cerrada (cero footprint, drift 0, README intacto -> safety validada). El golden de
SA pre-crea el claim en el fixture, asi que el camino real "sin pre-claim" nunca se ejercito.

Restriccion clave del write-path (submit_intent.py:512-516): `claim acquire` exige `owner == actor_id`, asi que
NADIE puede pre-crear el claim de OTRO agente (Claude no puede crear el de Codex). La via correcta (opcion 1,
elegida por el operador): que **el orquestador adquiera el claim actuando como el owner ruteado**
(`actor_id = owner ruteado`).

Alcance (SPEC-0070):
1. **Paso `claim` adquiere** el claim del owner ruteado por submit_intent (actor_id=owner) ANTES de run_turn;
   scope cubre changed_paths + transiciones.
2. **Idempotente** con pre-claim (byte-equivalente para goldens existentes); **conflicto** con otro agente ->
   rechazo.
3. **Reconciliacion** del claim del reporte (sin doble-acquire): build_prompt deja de reclamar, o apply idempotente.
4. **Release/handoff por outcome terminal** (done->handoff in_review; rejected/blocked->release).
5. **Golden recorded** (sin-pre-claim aceptado / otro-agente rechazado / release-handoff) + byte-equivalencia +
   regresiones/CI.

Preguntas a resolver (SPEC-0070 sec.5): **Q1** de donde toma el orquestador el scope del claim (tarea.scope/
relevant_files/file vs unidad; fallback si insuficiente). **Q2** confirmar por golden la via de reconciliacion
sin doble-acquire ni claim huerfano. Ambiguedad real -> `blocked` + pregunta concreta.

**Reglas (duras):** OFF-PILOT -> NO re-armar SA.4 (enabled=false) NI correr el piloto (lo dispara el arquitecto
tras el SMOKE REAL end-to-end + GO del operador; el re-fire es el unico multiplicador). enforce+authoritative ON:
TODA transicion (incluida la del orquestador) por submit_intent; si rechaza, `blocked` + error + transaccion. NO
edites *.json a mano. ASCII, **sin secretos**, template intacto, 1 commit/turno con rutas explicitas. NO cambiar el
capability-gate; Capa C OFF. DESPUES yo (Claude) ratifico adversarialmente + hago el SMOKE REAL (orquestador
adquiere claim -> codex edita -> gate ACEPTA) antes de reportar al operador. ETA tu turno.
