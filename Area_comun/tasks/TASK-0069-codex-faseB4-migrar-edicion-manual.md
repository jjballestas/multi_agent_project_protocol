---
id: TASK-0069
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-07
updated_at: 2026-06-07
depends_on: [TASK-0066, TASK-0067, TASK-0068]
relates_to: [TASK-0038, TASK-0048]
phase: P2
spec_id: Area_comun/specs/SPEC-0055-faseB4-migrar-edicion-manual.md
linked_decisions: [DECISION-0022, DECISION-0017, DECISION-0019, DECISION-0014]
execution_pipeline: [genesis POR REFERENCIA en runtime/protocol_replay.py - persistir el snapshot canonico content-addressed en runtime/state/snapshots/<hash>.json (fuera del prompt) + emitir evento protocol.genesis con snapshot_ref={hash,commit,actor,timestamp(provisto, no reloj),schema_version}; replay carga el snapshot por hash, RECOMPUTA y verifica el hash (mismatch/ausente => error/bloqueo seguro) y materializa bajo demanda; flag event_state.authoritative (live+template, default false) ADEMAS de enabled/materialize/enforce, solo adoption_tier=runtime; prohibicion de edicion manual reusando el hard-gate de B.3 (no mecanismo nuevo); operacion de migracion asistida (escribe snapshot + emite genesis-ref); docs migracion/reversa + nota AGENTS.md/.template/TASK_PROTOCOL; golden examples/runtime_protocol_genesis_ref_cases + CI; ENTREGAR APAGADA (no encender en el repo vivo)]
acceptance_criteria: [genesis emite snapshot_ref (hash/commit/actor/timestamp/schema_version) y NO incrusta el estado en el evento; snapshot persistido content-addressed fuera del prompt; replay verifica el hash y materializa, mismatch/ausente => bloqueo seguro; event log con genesis-ref es liviano (asercion de forma/tamano: sin blob de estado en el evento); modo authoritative on + edicion manual simulada => hard-fail (reusa B.3); off=byte-equivalente; round-trip genesis-ref->replay->materialize == estado canonico; rollback probado (encender->intents->apagar->editar a mano) sin perdida; determinismo (timestamp provisto, sin reloj/red); suite runtime + B.1/B.2/B.3 sin regresion; coordination-tier intacto; fallback N=2 byte-equivalente; paridad py/.ps1; gates py/ps verdes; NO encender authoritative/enforce en el repo vivo]
expected_output: runtime escritor autoritativo con genesis POR REFERENCIA content-addressed verificable + flag event_state.authoritative + prohibicion via hard-gate B.3 + migracion asistida + docs + golden runtime_protocol_genesis_ref_cases; ENTREGADO APAGADO; gates verdes.
test_plan: [golden: genesis-ref escribe snapshot+evento sin blob; round-trip; integridad hash mismatch/ausente => bloqueo; cold-start liviano; authoritative on + edicion manual => hard-fail; off byte-equivalente; rollback reversible sin perdida; determinismo; regresion B.1/B.2/B.3 + runtime; coordination-tier intacto; paridad py/ps]
question_to_resolve: ninguna (alcance B.4 acotado en SPEC-0055 + DECISION-0022). ENCENDER enforce/authoritative en la instancia viva NO entra en esta tarea (aprobacion separada del operador). Cambio incompatible mas alla de lo previsto => blocked + pregunta.
closure_criterion: genesis por referencia verificable + flag authoritative + prohibicion via B.3 + migracion asistida + docs + rollback probado + golden, ENTREGADO APAGADO, off=byte-equivalente; gates verdes; handoff autocontenido; release atomico (DECISION-0018).
closure_criteria: [genesis-ref (snapshot content-addressed fuera del prompt + evento con snapshot_ref hash/commit/actor/timestamp/schema_version, sin blob); replay verifica hash y materializa bajo demanda, bloqueo seguro ante mismatch/ausente; flag event_state.authoritative live+template=false; prohibicion de edicion manual reusa hard-gate B.3; migracion asistida + docs (incl. AGENTS.md/.template/TASK_PROTOCOL) + plan de rollback probado en golden; off=byte-equivalente; coordination-tier intacto; fallback N=2; determinismo; golden runtime_protocol_genesis_ref_cases + CI; suite runtime + B.1/B.2/B.3 sin regresion; paridad py/.ps1; ENTREGADO APAGADO (no encender en vivo); handoff autocontenido; release atomico (DECISION-0018)]
---

# TASK-0069 - Fase B.4: runtime escritor autoritativo + genesis por referencia + prohibir edicion manual

## Contexto

Ultima rebanada de la Fase B. B.1 (replay/drift) + B.2 (materializacion opt-in) + B.3 (drift hard-fail) ya
estan done. B.4 convierte al runtime en escritor autoritativo del estado (opt-in, runtime-tier) y prohibe la
edicion manual (reusando el hard-gate de B.3), con una migracion inicial por **genesis de referencia** segun
DECISION-0022 (ratificada por el operador, MINOR-con-migracion). Ver SPEC-0055.

## Restriccion clave del genesis (DECISION-0022, fijada por el operador)

Convertir el estado en genesis NO significa incrustar el estado en el contexto del agente. El genesis registra
una **referencia verificable** al snapshot de corte: `{hash, commit, actor, timestamp, schema_version}`. El
snapshot completo se persiste **content-addressed fuera del prompt** (`runtime/state/snapshots/<hash>.json`) y
solo se consulta/materializa cuando el runtime lo necesita; el replay **verifica el hash** antes de usarlo.

## Alcance (ver SPEC-0055)

1. Genesis por referencia + carga/verificacion del snapshot content-addressed (bloqueo seguro ante mismatch).
2. Flag `event_state.authoritative` (live + template, **default false**), solo runtime-tier.
3. Prohibicion de edicion manual reusando el hard-gate de B.3 (sin mecanismo nuevo).
4. Migracion asistida + docs (migracion/reversa + nota AGENTS.md/.template/TASK_PROTOCOL) + plan de rollback.
5. Golden `examples/runtime_protocol_genesis_ref_cases` + CI.

## Restricciones

- **ENTREGAR APAGADA.** NO encender `event_state.authoritative`/`enforce` en el repo vivo (activacion = paso
  aparte con aprobacion del operador + validacion replay/materializacion + rollback). Off=byte-equivalente.
- Determinismo (timestamp provisto, sin reloj/red); negative-replay intacto; **neutralidad**; **sin secretos**;
  ASCII en state (DECISION-0012); fallback N=2 byte-equivalente; coordination-tier intacto. Paridad py/.ps1.
- Cambio incompatible mas alla de lo previsto => `blocked` + pregunta.
- **Handoff autocontenido**; **release atomico** (DECISION-0018); anti-colision (DECISION-0020).

## Nota

Cuarta y ultima rebanada de Fase B (B.1+B.2+B.3 done -> **B.4**). Con B.4 done, la maquinaria del writer-vivo
queda completa pero APAGADA en la instancia viva; encenderla es decision operativa aparte del operador.
Promovida de a una (DECISION-0020). Codex autonomo: tomala cuando `ready`; GO enviado por mailbox.
