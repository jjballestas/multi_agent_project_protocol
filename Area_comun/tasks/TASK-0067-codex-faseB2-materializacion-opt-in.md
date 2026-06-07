---
id: TASK-0067
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-07
updated_at: 2026-06-07
depends_on: [TASK-0066]
relates_to: [TASK-0038, TASK-0048]
phase: P2
spec_id: Area_comun/specs/SPEC-0053-faseB2-materializacion-opt-in.md
linked_decisions: [DECISION-0017, DECISION-0015, DECISION-0014]
execution_pipeline: [reutilizar la maquinaria pura de B.1 (runtime/protocol_replay.py); anadir write_genesis (emite el snapshot genesis al log desde el estado vivo, operacion explicita) + materialize_to_disk(root, snapshot) determinista y atomica (escritura todo-o-nada de los 3 *.json canonicos, ASCII/sin BOM); modo event_state.materialize (live+template, default false) ADEMAS de event_state.enabled; cablear la materializacion SOLO en el path del runtime (orchestrator/apply) cuando enabled && materialize && adoption_tier=runtime, tras aplicar un turno; drift sigue WARNING (no hard-fail); golden examples/runtime_protocol_materialize_cases + CI]
acceptance_criteria: [materialize_to_disk escribe los 3 *.json canonicos esperados (ASCII/sin BOM); round-trip genesis->replay->materialize idempotente; atomicidad todo-o-nada ante fallo a mitad; con materialize=false o enabled=false o tier!=runtime el runtime NO escribe (byte-equivalente); validador sin drift con log coherente y WARNING con divergencia; suite runtime completa + runtime_protocol_replay_cases (B.1) intactos; fallback N=2 byte-equivalente; gates py/ps verdes; NO hard-fail por drift; NO prohibir edicion manual; NO encender materialize en el repo vivo]
expected_output: materializacion opt-in del estado de protocolo desde el log (write_genesis + materialize_to_disk doble-gated, solo runtime-tier) cableada en el runtime, off=byte-equivalente + golden runtime_protocol_materialize_cases; gates verdes.
test_plan: [golden: materialize escribe canonico; round-trip idempotente; atomicidad; gating off=byte-equivalente; drift coherente/divergente; regresion suite runtime + B.1; fallback N=2; paridad de gates py/ps]
question_to_resolve: ninguna (alcance B.2 acotado en SPEC-0053); si la materializacion exige hard-fail por drift, prohibir edicion manual o cambiar el contrato del turno => blocked + pregunta (eso es B.3/B.4, gateado).
closure_criterion: materializacion opt-in doble-gated (enabled+materialize, solo runtime-tier) + write_genesis + atomicidad + drift WARNING + off=byte-equivalente + golden + gates verdes; handoff autocontenido; release atomico (DECISION-0018).
closure_criteria: [write_genesis + materialize_to_disk deterministas/atomicos/canonicos (ASCII/sin BOM); modo event_state.materialize live+template=false; cableado solo en runtime cuando enabled&&materialize&&tier=runtime; drift sigue WARNING (no hard-fail); off=byte-equivalente; golden runtime_protocol_materialize_cases + CI; suite runtime + B.1 sin regresion; fallback N=2 byte-equivalente; paridad gates py/ps; handoff autocontenido; release atomico - claim liberado al pasar a in_review (DECISION-0018)]
---

# TASK-0067 - Fase B.2: materializacion opt-in del estado de protocolo

## Contexto

B.1 (TASK-0066, done) entrego la maquinaria pura read-only (replay/materialize/genesis/drift). B.2 la hace
util de forma OPT-IN: bajo `event_state.enabled` + un modo nuevo `event_state.materialize` y solo en
`adoption_tier=runtime`, el runtime ESCRIBE los `*.json` desde `replay(log)` (log = fuente de verdad). El
drift sigue WARNING (no hard-fail = B.3) y la edicion manual NO se prohibe (= B.4). Aditivo, doble-gated,
off=byte-equivalente. Ver SPEC-0053.

## Alcance (ver SPEC-0053 sec.2)

1. `write_genesis(root)` + `materialize_to_disk(root, snapshot)` deterministas y **atomicos** (todo-o-nada,
   ASCII/sin BOM, canonico).
2. Modo `event_state.materialize` (live + template, **default false**), ADEMAS de `event_state.enabled`.
3. Cableado SOLO en el runtime (`orchestrator`/`apply`) cuando `enabled && materialize && tier==runtime`.
4. Golden `examples/runtime_protocol_materialize_cases` + CI.

## Restricciones

- **Aditivo, doble-gated, off=byte-equivalente.** NO hard-fail por drift (B.3). NO prohibir/migrar la
  edicion manual (B.4). **NO encender `event_state.materialize` en el repo vivo** (queda off; encenderlo es
  decision del operador).
- Determinismo (sin reloj/red); atomicidad consistente con apply/TASK-0041; **neutralidad**; **sin secretos**;
  ASCII en state (DECISION-0012). Fallback N=2 byte-equivalente.
- Cambio incompatible del flujo manual o del contrato del turno => `blocked` + pregunta.
- **Handoff autocontenido**; **release atomico** (DECISION-0018); anti-colision (DECISION-0020):
  archivos-antes-de-claim, staging explicito, aserciones tras el ledger.

## Nota

Segunda de 4 rebanadas de Fase B (B.1 done -> **B.2 materializacion opt-in** -> B.3 hard-fail -> B.4
migrar/prohibir edicion manual, posible DECISION/MAJOR). Promovida de a una (DECISION-0020). Codex autonomo:
tomala cuando `ready`; GO enviado por mailbox.
