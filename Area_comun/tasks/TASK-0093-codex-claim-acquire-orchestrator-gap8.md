---
id: TASK-0093
owner: Codex
status: in_review
type: implementation
priority: high
created_at: 2026-06-09
updated_at: 2026-06-09
depends_on: [TASK-0092]
relates_to: [TASK-0091, TASK-0088, SPEC-0064]
phase: P2
spec_id: Area_comun/specs/SPEC-0070-claim-acquire-orchestrator-gap8.md
linked_decisions: [DECISION-0027, DECISION-0022, DECISION-0020]
objective: (OFF-PILOT, no multiplicador) Cerrar el gap-8 del orquestador. Hoy el paso `claim` (runtime/orchestrator.py:482) es un NO-OP: el turno autonomo llega al gate sin claim activo y es rechazado ("no active claim"). El paso `claim` debe ADQUIRIR el claim del owner ruteado (actor_id = owner ruteado, por submit_intent) ANTES de adapter_for_turn/run_turn, con scope que cubra los changed_paths del turno; idempotente con pre-claim; conflicto si lo tiene otro agente (falla cerrada); release/handoff por outcome terminal. NO re-armar SA.4 ni correr el piloto.
expected_output: (1) runtime/orchestrator.py paso `claim` adquiere el claim del owner ruteado via el write-path autoritativo (submit_intent, claim op=acquire, actor_id=owner ruteado -> owner==actor_id pasa validate_scope_authority) ANTES de run_turn; scope deriva de la tarea ruteada y cubre changed_paths + derive_transition_scopes; idempotente si ya existe claim owner+task (byte-equivalente para goldens con pre-claim); conflicto si solapa claim de otro agente -> turno rechazado. (2) Reconciliacion del claim auto-reportado por el LLM (SPEC-0070 2.3): build_prompt deja de instruir el claim (o apply lo trata idempotente) -> sin doble-acquire. (3) Release/handoff por outcome terminal (done->handoff a in_review sin claim del owner; rejected/blocked->release re-reclamable), via submit_intent. (4) Golden determinista recorded (sin pre-claim aceptado / claim-de-otro rechazado / release-handoff por outcome) + byte-equivalencia de goldens con pre-claim + regresiones verdes + validador/neutralidad/encoding/drift0 + paridad .ps1 donde aplique. NO re-armar SA.4 (enabled=false) NI correr piloto.
question_to_resolve: Q1 fuente del scope del claim (tarea.scope/relevant_files/file vs unidad ruteada; definir fallback si insuficiente). Q2 confirmar por golden la via de reconciliacion (build_prompt deja de reclamar / apply idempotente) sin doble-acquire ni claim huerfano. Si la adquisicion programatica del claim como owner ruteado choca con alguna invariante del write-path -> blocked + nota. Si submit_intent rechaza, NO editar *.json a mano.
closure_criterion: el paso `claim` adquiere el claim del owner ruteado por submit_intent (owner==actor_id) ANTES del turno, scope cubre changed_paths, idempotente con pre-claim, conflicto con otro agente rechaza; reconciliacion sin doble-acquire; release/handoff por outcome terminal; golden determinista (sin-pre-claim aceptado / otro-agente rechazado / release-handoff) verde + byte-equivalencia de goldens con pre-claim + regresiones/validador/neutralidad/encoding verdes + drift 0; vendor-neutral; sin secretos; template intacto; SA.4 sigue DE-ARMADO; todo por submit_intent; handoff con evidencia (incluye una traza recorded del camino sin-pre-claim aceptado). El SMOKE REAL end-to-end (orquestador adquiere claim -> codex edita -> gate ACEPTA) lo hace Claude al ratificar (gate de cierre de (B)).
sdd_required: true
---

# TASK-0093 - El orquestador adquiere el claim del owner ruteado (gap-8, off-pilot)

> READY (encolada por Claude 2026-06-09 VIA submit_intent bajo enforce+authoritative). OFF-PILOT.
> Resuelve el hallazgo del 2do piloto (codex invoker): el invoker codex SI edita el README, pero el
> gate rechaza "no active claim" porque el paso `claim` del orquestador es un NO-OP. Ver SPEC-0070.
> SA.4 DE-ARMADO; NO re-armar ni piloto. El re-fire es paso posterior con GO separado del operador.

## Contexto

2do piloto (preset codex, invoker REAL) RECHAZADO por el gate con `semantic: no active claim for
report task_id and agent` (turn_validate.py:289-295). Raiz (gap-8): `runtime/orchestrator.py:482` es
`trace.append("claim")` -- un placeholder que no adquiere nada; el turno llega a `validate_turn` sin
claim activo y falla cerrada (cero footprint, drift 0, README intacto -> safety validada). El golden
de SA pre-crea el claim en el fixture, asi que el camino real "sin pre-claim" nunca se ejercito.
Restriccion del write-path (submit_intent.py:512-516): `claim acquire` exige `owner == actor_id`, asi
que Claude NO puede pre-crear el claim de Codex; la via correcta es que el orquestador lo adquiera
actuando como el owner ruteado.

## Alcance (SPEC-0070, opcion 1)

1. **Paso `claim` adquiere** el claim del owner ruteado (actor_id=owner) por submit_intent ANTES de
   run_turn; scope cubre changed_paths + derive_transition_scopes; idempotente con pre-claim;
   conflicto con claim de otro agente -> rechazo (falla cerrada).
2. **Reconciliacion** del claim auto-reportado por el LLM (sin doble-acquire): build_prompt deja de
   reclamar, o apply idempotente. Elegir UNA y fijarla en el golden.
3. **Release/handoff por outcome terminal** (done->handoff in_review; rejected/blocked->release).
4. **Golden recorded** (sin-pre-claim aceptado / otro-agente rechazado / release-handoff por outcome)
   + byte-equivalencia de goldens con pre-claim + regresiones verdes + paridad/CI.

## Restricciones (duras)

- OFF-PILOT: SA.4 sigue de-armado; NO re-armar NI correr piloto. enforce+authoritative ON: TODA
  transicion (incluida la del orquestador) por submit_intent; cero edicion manual de *.json.
- ASCII, sin secretos, determinista en CI (golden recorded). Template intacto. 1 commit/turno con
  rutas explicitas. NO cambiar el capability-gate. Capa C OFF.

## Cierre

Claude ratifica adversarialmente (golden + lectura del contrato + byte-equivalencia) y cierra por
submit_intent. DESPUES (Claude): SMOKE REAL end-to-end (orquestador adquiere claim -> codex edita ->
gate ACEPTA) sobre fixture/tarea de prueba de bajo riesgo -> si limpio, reporto al operador -> GO al
re-fire del piloto (re-armar preset codex, caps 2/1/180000, checkpoint tras turno 1).
