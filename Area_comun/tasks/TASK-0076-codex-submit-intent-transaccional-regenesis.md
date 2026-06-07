---
id: TASK-0076
owner: Codex
status: in_review
type: implementation
priority: high
created_at: 2026-06-07
updated_at: 2026-06-07
depends_on: [TASK-0072]
relates_to: [TASK-0038]
phase: P2
spec_id: Area_comun/specs/SPEC-0062-submit-intent-transaccional-regenesis.md
linked_decisions: [DECISION-0022, DECISION-0017, DECISION-0020]
execution_pipeline: [submit_intent transaccional multi-intent (--intents archivo/json con {actor_id,timestamp,commit,intents:[...]}): aplica una secuencia ordenada de intents de forma atomica (un append por intent + materializacion final + drift 0) o rollback total ante fallo de cualquiera; cada intent se valida contra el estado resultante de los previos; idempotencia por-intent y de transaccion; mantiene el --intent mono-intent actual. + runtime/regenesis.py: genesis fresco POR REFERENCIA desde el estado materializado actual -> drift 0, base limpia, idempotente/determinista (timestamp/commit provistos), conserva/archiva el event log previo (no destructivo). + golden examples/intent_tx_cases (cierre real multi-intent drift0; rollback ante fallo intermedio byte-identico; re-genesis->drift0 y submit_intent posterior ok; idempotencia) + paridad .ps1 + CI]
acceptance_criteria: [submit_intent aplica una transaccion multi-intent atomica con rollback total ante fallo (estado byte-identico al previo); regenesis deja protocol_state_drift.has_drift=False sobre un estado con drift; una transaccion de cierre real (status done + claim release + task_upsert + decision) pasa con drift 0 y materializa el ledger esperado; idempotencia (repetir no duplica); NO se encienden enforce/authoritative; determinista sin reloj/red; sin secretos; neutral; paridad/delegacion .ps1; golden + gates py/ps verdes]
expected_output: runtime/submit_intent.py con modo transaccional multi-intent (+ wrapper ps1) + runtime/regenesis.py (+ ps1) + golden examples/intent_tx_cases + CI; enforce/authoritative permanecen OFF.
test_plan: [golden intent_tx: cierre real multi-intent -> drift 0 + ledger esperado; fallo de intent intermedio -> rollback total byte-identico; re-genesis sobre drift -> drift 0 + submit_intent posterior ok; idempotencia de transaccion; determinismo + paridad py/ps; off/sombra byte-equivalente]
question_to_resolve: ninguna (alcance acotado en SPEC-0062). Si para lograr atomicidad multi-intent hiciera falta cambiar el formato del event log de forma incompatible => blocked + pregunta (debe ser aditivo).
closure_criterion: submit_intent transaccional multi-intent (atomico + rollback) + regenesis (drift 0, no destructivo) + golden intent_tx + paridad .ps1; SIN flip de enforce; gates verdes; handoff autocontenido; release atomico (DECISION-0018).
closure_criteria: [submit_intent --intents transaccional atomico con rollback total; regenesis.py genesis fresco por referencia -> drift 0 no destructivo; golden examples/intent_tx_cases (cierre multi-intent drift0, rollback byte-identico, re-genesis->drift0, idempotencia); enforce/authoritative OFF (sin flip); determinista sin reloj/red; sin secretos; neutral; paridad/delegacion .ps1 + CI; gates verdes; handoff autocontenido; release atomico DECISION-0018; staging por paths DECISION-0020]
---

# TASK-0076 - submit_intent transaccional multi-intent + re-genesis (keystone de la adopcion)

> IN_REVIEW (entregada por Codex 2026-06-08 tras cerrar F7.4). KEYSTONE de la adopcion de submit_intent por AMBOS
> lazos (orden del operador): que Claude y el lazo autonomo de Codex dejen de editar los `*.json` a mano.
> SHADOW: enforce/authoritative siguen OFF en esta tarea (sin flip). Ver SPEC-0062.

## Contexto

submit_intent (TASK-0072) aplica UN intent por invocacion y exige drift 0 antes de escribir. Pero cada
cierre/encole real de ambos lazos es **multi-intent atomico** y el estado vivo hoy tiene **drift** (sombra).
Sin (a) transaccion multi-intent y (b) re-genesis que ponga drift a 0, ningun lazo puede reemplazar sus
scripts de edicion directa por submit_intent. Esta tarea entrega ambos enablers, validados en sombra.

## Alcance (ver SPEC-0062 sec.2)

1. **submit_intent transaccional multi-intent** `--intents` (secuencia ordenada, atomica, rollback total;
   cada intent validado contra el estado resultante de los previos; idempotente). Mantener `--intent` actual.
2. **runtime/regenesis.py**: genesis fresco por referencia desde el estado materializado actual -> drift 0,
   no destructivo (conserva/archiva el event log previo), idempotente/determinista.
3. **Golden** `examples/intent_tx_cases` + paridad `.ps1` + CI.

## Restricciones

- **NO encender enforce/authoritative** (eso es la rebanada de ACTIVACION posterior, con GO del operador +
  ensayo de rollback + verificacion de que AMBOS lazos usan submit_intent). Off/sombra => byte-equivalente.
- Atomicidad todo-o-nada; rollback byte-identico. Drift 0 tras transaccion exitosa y tras re-genesis.
- Determinista (timestamp/commit provistos; sin reloj/red). Sin secretos. Neutral.
- Cambios al event log deben ser **aditivos**; si exigiera un cambio incompatible => `blocked` + pregunta.
- **Handoff autocontenido**; **release atomico** (DECISION-0018); **staging por paths** (DECISION-0020).

## Nota de coordinacion

Esta tarea es el primer paso de la migracion al escritor-unico. Tras ratificarla: el arquitecto redacta el
cutover (mandato en AGENTS.md/TASK_PROTOCOL) y ambos lazos adoptan submit_intent en sombra; luego, con GO del
operador, re-genesis del repo vivo + flip enforce+authoritative + ensayo de rollback. **El flip NO ocurre
hasta que el lazo autonomo de Codex use submit_intent de verdad** (si no, una edicion manual posterior
hard-failea y rompe el lazo).

## Entrega Codex 2026-06-08

- `runtime/submit_intent.py` mantiene `--intent` mono-intent y agrega `--intents`/`--intents-json` con envelope
  `{actor_id,timestamp,commit,intents}`.
- `submit_intents` valida cada intent contra el estado resultante de los previos, emite eventos
  `intent.applied` con metadata de transaccion, materializa una sola vez al final y hace rollback total de
  archivos + `runtime/state` ante fallo.
- `runtime/regenesis.py` (+ `runtime/regenesis.ps1`) escribe genesis fresco por `snapshot_ref` desde hot state,
  idempotente, no destructivo, y deja `protocol_state_drift.has_drift=False`.
- Agregado `examples/intent_tx_cases/run_intent_tx_cases.py` y paso CI.
- Validacion: intent_tx_cases 6/6, intent_flow 9/9, runtime replay/materialize/enforce/genesis-ref verdes,
  py_compile, encoding/neutralidad/validador py/ps verdes. Sin flip `enforce`/`authoritative`.
