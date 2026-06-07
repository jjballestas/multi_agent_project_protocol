---
id: TASK-0068
owner: Codex
status: ready
type: implementation
priority: high
created_at: 2026-06-07
updated_at: 2026-06-07
depends_on: [TASK-0066, TASK-0067]
relates_to: [TASK-0038, TASK-0048]
phase: P2
spec_id: Area_comun/specs/SPEC-0054-faseB3-drift-hard-fail.md
linked_decisions: [DECISION-0017, DECISION-0015, DECISION-0014]
execution_pipeline: [anadir flag event_state.enforce (live+template, default false); validador global py/.ps1 => si enabled && enforce && runtime/state tiene contenido y hay drift, validation.fail (hard-fail) en vez de warn, con paths listados; gate en apply (runtime): antes de commitear el turno, si enabled && enforce y hay protocol_state_drift, abortar el commit (discard+block, atomico); reutilizar protocol_state_drift/materialize de B.1/B.2 (solo cambia severidad warn->fail bajo flag); golden examples/runtime_protocol_enforce_cases + CI]
acceptance_criteria: [enforce=true + drift => validador hard-fail (exit!=0) con paths; enforce=true + coherente => pasa; enforce=false o sin runtime/state => warning-only/byte-equivalente a B.1; apply aborta el commit ante drift con enforce (todo-o-nada) y commitea si coherente; tier!=runtime no fuerza enforce; suite runtime + B.1 + B.2 sin regresion; fallback N=2 byte-equivalente; paridad py/.ps1; NO prohibir edicion manual; NO encender enforce en el repo vivo]
expected_output: drift del estado de protocolo como hard-fail bajo event_state.enforce (validador + gate en apply), triple-gated, off=byte-equivalente + golden runtime_protocol_enforce_cases; gates verdes.
test_plan: [golden: enforce+drift hard-fail; enforce+coherente pasa; enforce off byte-equivalente; apply aborta/commitea; combinaciones de flags; regresion B.1/B.2/runtime; fallback N=2; paridad py/ps]
question_to_resolve: ninguna (alcance B.3 acotado en SPEC-0054); si exige prohibir/migrar edicion manual o cambiar el contrato del turno => blocked + pregunta (eso es B.4, posible DECISION/MAJOR).
closure_criterion: drift hard-fail bajo event_state.enforce (validador + apply) triple-gated + off=byte-equivalente + golden + gates verdes; handoff autocontenido; release atomico (DECISION-0018).
closure_criteria: [flag event_state.enforce live+template=false; validador py/.ps1 hard-fail bajo enabled+enforce+runtime/state con drift (warning-only si off); gate en apply aborta el commit ante drift con enforce (atomico); reutiliza B.1/B.2 sin nueva maquinaria de estado; off=byte-equivalente; golden runtime_protocol_enforce_cases + CI; suite runtime + B.1 + B.2 sin regresion; fallback N=2; paridad py/.ps1; handoff autocontenido; release atomico (DECISION-0018)]
---

# TASK-0068 - Fase B.3: drift del estado de protocolo como hard-fail

## Contexto

B.1 (done) dio replay/drift read-only (drift=WARNING). B.2 (done) materializa el estado desde el log
(opt-in). B.3 promueve el drift a **hard-fail** PERO solo cuando `event_state.enforce` esta on (= el runtime
es el escritor habitual), para no romper la edicion manual del repo vivo. Cierra el invariante objetivo de
Fase B: `hot *.json == materializa(replay(log))` como hard-gate. Ver SPEC-0054.

## Alcance (ver SPEC-0054 sec.3)

1. Flag `event_state.enforce` (live + template, **default false**).
2. Validador global py/.ps1: drift => `fail` (no `warn`) cuando `enabled && enforce && runtime/state`.
3. Gate en apply: abortar el commit del turno ante drift con enforce (atomico, discard+block).
4. Golden `examples/runtime_protocol_enforce_cases` + CI.

## Restricciones

- **Aditivo, triple-gated, off=byte-equivalente.** NO prohibir/migrar edicion manual (B.4). **NO encender
  enforce en el repo vivo.** Determinismo; atomicidad (apply/TASK-0041); neutralidad; sin secretos; ASCII
  (DECISION-0012); fallback N=2 byte-equivalente. Cambio incompatible => `blocked`.
- **Handoff autocontenido**; **release atomico** (DECISION-0018); anti-colision (DECISION-0020):
  archivos-antes-de-claim, staging explicito, aserciones tras el ledger.

## Nota

Tercera de 4 rebanadas de Fase B (B.1 done -> B.2 done -> **B.3 hard-fail** -> B.4 migrar/prohibir edicion
manual, posible DECISION/MAJOR + aprobacion humana). Promovida de a una (DECISION-0020). Codex autonomo:
tomala cuando `ready`; GO enviado por mailbox.
