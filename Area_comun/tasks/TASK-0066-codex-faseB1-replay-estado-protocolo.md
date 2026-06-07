---
id: TASK-0066
owner: Codex
status: ready
type: implementation
priority: high
created_at: 2026-06-07
updated_at: 2026-06-07
depends_on: [TASK-0048]
relates_to: [TASK-0038, TASK-0044]
phase: P2
spec_id: Area_comun/specs/SPEC-0052-faseB-replay-estado-protocolo.md
linked_decisions: [DECISION-0017, DECISION-0015, DECISION-0014]
execution_pipeline: [implementar replay/materializacion del estado de protocolo en runtime (replay_protocol_state + materialize_protocol_state deterministas/canonicos + build_genesis_snapshot del estado vivo + protocol_state_drift puras, sin reloj/red); config event_state.enabled live+template default false; validador global py/.ps1 reporta drift como WARNING SOLO cuando runtime/state existe Y event_state.enabled (con feature off => byte-equivalente, sin warning, sin hard-fail); golden examples/runtime_protocol_replay_cases + CI; NO materializar los *.json como verdad, NO tocar apply/orchestrator write-path, NO prohibir edicion manual (rebanadas B.2-B.4, gateadas)]
acceptance_criteria: [replay_protocol_state reconstruye status de tareas/active_tasks/decisions/claims desde eventos; materialize idempotente y canonico; genesis round-trip (replay(genesis) materializa el mismo estado vivo); drift detectado/ausente correctamente; con event_state.enabled=false o sin runtime/state la salida del validador es byte-equivalente a hoy; con ambos activos y drift => WARNING (nunca hard-fail en B.1); golden + validador/encoding/neutralidad/prune py/ps verdes; suite runtime sin regresion; determinismo (negative replay sin side-effects)]
expected_output: maquinaria read-only de replay/materializacion/genesis del estado de protocolo + drift en modo warning gateado (off=byte-equivalente) + golden runtime_protocol_replay_cases; gates verdes.
test_plan: [golden: replay->snapshot esperado; materialize idempotente/canonico; genesis round-trip; drift presente/ausente; validador byte-equivalente con feature off y WARNING con feature on+drift; determinismo negative replay; paridad py/.ps1; suite runtime completa + gates py/ps verdes]
question_to_resolve: ninguna (alcance B.1 acotado en SPEC-0052); si la reconstruccion del estado exige cambiar el write-path o el flujo de edicion manual => blocked + pregunta (eso es B.2-B.4, gateado).
closure_criterion: replay/materialize/genesis/drift del estado de protocolo (read-only) + WARNING gateado off=byte-equivalente + golden + gates verdes + determinismo; handoff autocontenido; release atomico (DECISION-0018).
closure_criteria: [replay_protocol_state + materialize_protocol_state + build_genesis_snapshot + protocol_state_drift deterministas/canonicos; config event_state.enabled live+template=false; validador py/.ps1 WARNING-only gateado, off=byte-equivalente; golden runtime_protocol_replay_cases + CI; suite runtime sin regresion; paridad py/.ps1; gates py/ps verdes; handoff autocontenido; release atomico - claim liberado al pasar a in_review (DECISION-0018)]
---

# TASK-0066 - Fase B.1: replay/materializacion del estado de protocolo (read-only + drift warning)

## Contexto

El event log es writer del control-plane (Fase A, TASK-0048) pero NO del estado de protocolo. Fase B
(SPEC-0039 sec.4, decompuesta en SPEC-0052) lo lleva a writer del estado en rebanadas aditivas/gateadas.
Esta es **B.1**: la maquinaria read-only (replay + materializacion + genesis + drift) y un drift en modo
WARNING gateado. NO cambia el write-path ni el flujo de edicion manual (eso es B.2-B.4, gateado). Arrancada
por el operador (2026-06-07, post-v1.0). Avanza el paraguas TASK-0038 (criterios 11-12 SPEC-0038, I5/I6).

## Alcance (ver SPEC-0052 sec.3)

1. `replay_protocol_state` / `materialize_protocol_state` / `build_genesis_snapshot` / `protocol_state_drift`
   deterministas, canonicos, sin reloj/red.
2. Config `event_state.enabled` (live + template, default **false**).
3. Validador global py/.ps1: drift como **WARNING** solo con `runtime/state/` presente Y `event_state.enabled`;
   feature off => byte-equivalente.
4. Golden `examples/runtime_protocol_replay_cases` + CI.

## Restricciones

- **Aditivo, config-gated, off=byte-equivalente.** NO materializar *.json como verdad, NO tocar
  apply/orchestrator write-path, NO prohibir edicion manual (rebanadas posteriores, gateadas).
- **Determinismo:** negative replay sin side-effects (Fase 2). **Neutralidad**; **sin secretos**; ASCII en
  state (DECISION-0012). Paridad py/.ps1.
- Cambio incompatible del flujo manual => `blocked` + pregunta.
- **Handoff autocontenido**; **release atomico** (DECISION-0018): handoff + in-review + claim liberado + flip
  en el mismo paso. Aplica DECISION-0020 (anti-colision): archivos-antes-de-claim, staging explicito,
  aserciones tras el ledger.

## Nota

Primera de 4 rebanadas de Fase B (B.1 read-only -> B.2 materializacion opt-in -> B.3 hard-fail -> B.4
migrar/prohibir edicion manual, posible DECISION/MAJOR). Promovida de a una (DECISION-0020). Codex autonomo:
tomala cuando `ready`; GO enviado por mailbox.
