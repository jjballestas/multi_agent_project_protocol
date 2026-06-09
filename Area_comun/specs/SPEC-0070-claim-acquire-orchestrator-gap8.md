---
spec_id: SPEC-0070-claim-acquire-orchestrator-gap8
task_id: TASK-0093
type: design
status: ready
created_at: 2026-06-09
author: Claude (arquitecto)
linked_decisions: [DECISION-0027, DECISION-0022, DECISION-0020, DECISION-0021]
relates_to: [TASK-0091, TASK-0092, SPEC-0069, SPEC-0064]
---

> PROMOVIDA por Claude (2026-06-09) bajo enforce+authoritative. OFF-PILOT (NO multiplicador).
> Cierra el gap-8 del orquestador: el paso `claim` (orchestrator.py:482) es un NO-OP, asi que el
> turno autonomo llega al gate SIN claim activo y es rechazado ("no active claim"). SA.4 sigue
> DE-ARMADO; el re-fire es un paso posterior con GO separado del operador.

# Diseno - El orquestador adquiere el claim del owner ruteado (gap-8, opcion 1)

## 1. Contexto (hallazgo del 2do piloto, codex invoker)

El 2do piloto (preset codex, invoker REAL) demostro que el invoker codex SI hace el trabajo: codex
edito el README real y emitio un turn-report. PERO el gate rechazo el turno con `semantic: no active
claim for report task_id and agent` (`runtime/turn_validate.py:289-295`).

Raiz (gap-8): el paso `claim` del loop del orquestador es un placeholder. En
`runtime/orchestrator.py:482` solo hay `trace.append("claim")` -- NO adquiere nada. El loop pasa
`route -> (claim NO-OP) -> adapter -> run_turn -> validate`. Cuando llega a `validate_turn`, este
exige que exista un claim activo cuyo `task_id`+`owner` casen con el turn-report
(`turn_validate.py:289-303`); como nadie lo adquirio, falla cerrada.

El golden de SA hasta hoy PRE-CREA el claim del owner en el fixture, por lo que nunca ejercito el
camino real "sin pre-claim". El piloto-1 (claude) tambien fallo aqui (#3), pero quedo enmascarado por
el fallo de capability (#1). Confirmado por replay del piloto-2: cero footprint, drift 0, README
intacto -- el sobre/gate protegio el repo (safety validada).

Restriccion dura del write-path (`runtime/submit_intent.py:512-516`): un intent `claim acquire`
EXIGE `owner == actor_id`. Por eso un agente NO puede pre-crear el claim de OTRO (p.ej. Claude no
puede crear el claim de Codex). La unica via correcta: que el orquestador adquiera el claim
**actuando como el agente ruteado** (`actor_id = owner ruteado`).

## 2. Alcance (opcion 1, elegida por el operador)

### 2.1 El paso `claim` adquiere el claim del owner ruteado ANTES del turno
En `runtime/orchestrator.py` (paso `claim`, hoy linea 482), ANTES de `adapter_for_turn`/`run_turn`,
el orquestador adquiere el claim de la unidad ruteada:
- `owner` = `unit["owner"]` (el agente que correra su turno autonomo); `task_id` = `unit["task_id"]`.
- La adquisicion va POR el write-path autoritativo (`runtime/submit_intent.py`, intent `claim`
  `op=acquire`) con `actor_id = owner ruteado`. Asi `owner == actor_id` pasa
  `validate_scope_authority`. Semantica: "el orquestador-corriendo-como-owner reclama su propia
  tarea". NUNCA editar `CLAIMS.json` a mano (bajo enforce eso es hard-fail por drift).
- **Scope del claim:** debe CUBRIR los `changed_paths` que el turno reportara y los `derive_transition_scopes`
  que `turn_validate` valida (`turn_validate.py:298-303`). Derivar el scope de la definicion de la
  tarea ruteada (su `scope`/`relevant_files`/`file` en estado). DECIDIR explicitamente la fuente del
  scope (ver Q1). Si el turno escribe fuera del scope del claim, el gate sigue rechazando (correcto).

### 2.2 Idempotencia y conflicto (falla cerrada)
- Si YA existe un claim activo del mismo `owner`+`task_id` (caso del golden con pre-claim) -> procede
  reutilizandolo, SIN emitir un evento nuevo -> los goldens existentes con pre-claim quedan
  **byte-equivalentes** (no aparece un claim acquire extra).
- Si existe un claim activo de OTRO agente que solapa el scope -> CONFLICTO -> el turno se rechaza
  (falla cerrada). Reusar la deteccion de solape de `validate_scope_authority`
  (`submit_intent.py:518-524`).

### 2.3 Reconciliacion con el claim auto-reportado por el LLM (clave)
El turn-report endurecido de SPEC-0069/TASK-0092 incluye una transicion `claim` ademas de
`task_status`. Como el orquestador ya adquirio el claim autoritativamente, el claim del REPORTE NO
debe re-adquirir (doble-acquire -> conflicto consigo mismo). Reconciliar de forma explicita; opcion
recomendada:
- `build_prompt` (`runtime/adapters/llm_adapter.py`) deja de instruir el `claim acquire` al agente: el
  orquestador ya reclamo. El turn-report solo lleva la EDICION + la transicion `task_status`
  (p.ej. `in_progress -> in_review`). El paso `apply` (`apply_gate_and_commit`) NO re-adquiere.
- Alternativa aceptable: mantener el claim en el reporte pero que el apply lo trate como idempotente
  (no-op si ya lo tiene el owner). Elegir UNA y dejarla determinista en el golden.
- **NO confiar en el claim auto-reportado por el LLM como fuente de verdad** (descarta opcion 3): la
  autoridad del claim es el orquestador, no el reporte.
- NO rutear un turno extra solo-para-claim (descarta opcion 2).

### 2.4 Liberacion / handoff por outcome terminal (definir explicito)
Al cierre del turno (paso `apply`/post-turno), segun el outcome terminal del turno:
- `done`/entrega (`-> in_review`): HANDOFF del claim (el owner suelta y la tarea queda `in_review`
  sin claim activo del owner, conforme a la regla de seccion 7 de AGENTS.md: "una tarea revisada no
  debe retener el claim activo de su owner").
- `rejected`/`blocked`: RELEASE del claim para que la tarea sea re-reclamable (no dejar claim
  huerfano). Bajo `rejected` con cero footprint (como el piloto-2), liberar igualmente.
- Todo via el write-path autoritativo (`claim op=release`), nunca edicion manual.
- Definir la tabla outcome->accion de claim de forma explicita en el codigo y en el golden.

## 3. Invariantes (duras)
1. **OFF-PILOT:** SA.4 sigue DE-ARMADO (`runtime.real_invoker.enabled=false`,
   `runtime.supervised_autonomy.enabled=false`). NO re-armar el registro NI correr el piloto. El
   re-fire es un paso posterior con GO separado del operador (el unico multiplicador).
2. **enforce+authoritative ON:** TODA transicion de ledger (incluida la adquisicion/liberacion del
   claim por el orquestador) va por `submit_intent`; CERO edicion directa de `*.json` (drift 0
   sostenido, si no hard-fail).
3. **Capability-gate intacto:** no se toca `required_capability_for_report`; codex=implementer ya
   cubre. SA.4 y Capa C nunca juntos; Capa C OFF.
4. ASCII, sin secretos, determinista en CI (golden recorded, sin red). Template intacto. Paridad
   `.ps1` donde aplique. 1 commit/turno con rutas explicitas.

## 4. Cierre (DoD)

### 4.1 Golden (determinista, recorded, sin red)
- **Sin pre-claim:** el orquestador adquiere el claim del owner ruteado -> el turno procede -> el
  turn-report COMPLETO es ACEPTADO por el gate (changed_paths dentro del scope, transicion valida,
  agent == owner con claim activo).
- **Claim de otro agente (solape):** el paso `claim` detecta conflicto -> el turno se RECHAZA (falla
  cerrada), cero footprint.
- **Release/handoff por outcome terminal:** un caso por cada outcome terminal (done->handoff a
  in_review sin claim del owner; rejected->release re-reclamable; blocked->release).
- **Byte-equivalencia:** los goldens existentes que PRE-CREAN el claim (idempotencia 2.2) siguen
  byte-equivalentes (no aparece un acquire extra). Regresiones verdes: `supervised_autonomy_cases`,
  `runtime_loop`, `real_adapter`, `llm_adapter`, `intent_flow`, `llm_turn_wrapper_cases`.
- Validador / neutralidad / encoding verdes; drift 0; paridad `.ps1` donde aplique.

### 4.2 Smoke real (el gate, lo ejecuta Claude al ratificar; off-pilot, sin re-armar)
UNA corrida real end-to-end por el invoker codex donde **el orquestador adquiere el claim** y luego
codex edita el README y emite el turn-report, y el gate ACEPTA: `changed_paths` + transicion
`task_status` + `agent=Codex` con claim activo. Sobre un fixture aislado / tarea de prueba de bajo
riesgo (NO la tarea-objetivo del piloto; el piloto sigue OFF). Si el gate aun rechaza por claim/scope
-> iterar (sigue off-pilot). Solo con ese smoke LIMPIO se considera (B) cerrado y se reporta al
operador para el GO al re-fire.

## 5. Preguntas a resolver (handoff autocontenido)
- **Q1 (fuente del scope del claim):** de donde toma el orquestador el scope a reclamar para cubrir
  los `changed_paths` del turno -- del `scope`/`relevant_files`/`file` de la tarea en estado, o de la
  unidad ruteada? Si la tarea no declara scope suficiente, definir el fallback (p.ej. el `file` de la
  tarea + el directorio objetivo) y documentarlo. Si queda ambiguo -> `blocked` + pregunta concreta.
- **Q2 (reconciliacion 2.3):** confirmar por golden cual de las dos vias (build_prompt deja de
  reclamar / apply idempotente) queda elegida, y que no hay doble-acquire ni claim huerfano.

## 6. Fuera de alcance
- Re-armar SA.4 / correr el piloto (paso posterior, GO separado del operador; el multiplicador).
- Cambiar el capability-gate (descartado en SPEC-0069).
- Capa C del bridge (OFF; nunca junto con SA.4).
- claude como invoker de turnos implementer (no tiene la capability).
