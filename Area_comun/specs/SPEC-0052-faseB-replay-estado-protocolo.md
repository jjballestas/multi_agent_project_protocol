---
spec_id: SPEC-0052-faseB-replay-estado-protocolo
task_id: TASK-0066
type: implementation
status: accepted
created_at: 2026-06-07
author: Claude (arquitecto)
linked_decisions: [DECISION-0017, DECISION-0015, DECISION-0014, DECISION-0011]
relates_to: [SPEC-0039, SPEC-0038]
---

> Decomposicion de la Fase B de SPEC-0039 (event log como writer vivo del ESTADO DE PROTOCOLO), arrancada
> por instruccion del operador 2026-06-07 (post-v1.0). Fase B es el principal vehiculo concreto del paraguas
> TASK-0038 (criterios 11-12 SPEC-0038 + invariantes I5/I6 sobre estado de protocolo). Aditivo, gateado,
> byte-equivalente con la feature off. Cambio incompatible del flujo de edicion manual => blocked + DECISION.

# SPEC-0052 - Fase B: replay/materializacion del estado de protocolo

## 1. Objetivo

Llevar el event log de writer del *control-plane* (Fase A, TASK-0048) a writer del *estado de protocolo*
(TASK_INDEX/PROJECT_STATE/CLAIMS), con invariante objetivo
`hot *.json == materializa(replay(log) hasta up_to_seq)`. Se hace en rebanadas para acotar riesgo: el flujo
de edicion manual actual NO se toca hasta una rebanada posterior y gateada.

## 2. Decomposicion en rebanadas (aditivas, gateadas)

- **B.1 (esta tarea, TASK-0066): maquinaria read-only + drift en modo WARNING.**
  - Extender `replay_events` (o un `replay_protocol_state` paralelo) para reconstruir el estado de protocolo
    desde eventos de transicion: status de tareas (TASK_INDEX), active_tasks/decisions (PROJECT_STATE) y
    claims (CLAIMS).
  - `materialize_protocol_state(snapshot) -> dict` determinista (sin reloj/red), canonico (orden estable).
  - `build_genesis_snapshot(root)`: convierte el estado vivo actual de los `*.json` en el snapshot/evento
    inicial (genesis), sin escribirlo como verdad todavia.
  - Deteccion de **drift** `hot *.json` vs `materializa(replay(log))`: funcion pura + reporte. En el
    validador global se expone como **WARNING** y SOLO cuando `runtime/state/` existe y un flag de config
    (`event_state.enabled`, default false) esta activo. Con la feature off => comportamiento actual
    byte-equivalente (sin warning, sin gate).
  - NO materializa los `*.json` (no escribe estado de verdad), NO toca apply/orchestrator write-path, NO
    prohibe edicion manual. Todo es observacional/reversible.

- **B.2 (gateada, tarea aparte): genesis + materializacion opt-in.** Con `event_state.enabled` + un modo
  explicito, el runtime materializa los `*.json` desde el snapshot (log = fuente de verdad) en instancias
  runtime-tier; drift sigue warning.

- **B.3 (gateada): hard-fail.** El drift pasa de warning a hard-fail del validador global cuando el runtime
  es el escritor habitual (analogo al gate de Fase A 3.2).

- **B.4 (gateada, posible DECISION/MAJOR): migrar/prohibir edicion manual** del estado de protocolo (pasa por
  el runtime). Se evalua SemVer al activarla (MINOR-con-migracion o MAJOR).

## 3. Alcance de B.1 (TASK-0066)

1. `runtime/eventlog.py` (o modulo nuevo `runtime/protocol_replay.py`): `replay_protocol_state`,
   `materialize_protocol_state`, `build_genesis_snapshot`, `protocol_state_drift` (puras, deterministas).
2. Config `event_state.enabled` (live + template, default **false**) en `protocol.config.json`.
3. Validador global py/.ps1: cuando `runtime/state/` existe Y `event_state.enabled`, reporta drift como
   WARNING (nunca hard-fail en B.1). Con la feature off, byte-equivalente (sin cambios de salida).
4. Golden nuevo `examples/runtime_protocol_replay_cases` + CI.

## 4. Tests (golden determinista, sin red)

1. Replay de una secuencia de eventos de transicion -> snapshot de estado de protocolo esperado.
2. `materialize_protocol_state` idempotente y canonico (dos corridas == mismo dict).
3. `build_genesis_snapshot` del estado vivo -> replay(genesis) materializa de vuelta el mismo estado
   (round-trip).
4. Drift detectado cuando hot difiere del materializado; sin drift cuando coinciden.
5. Validador: con `event_state.enabled=false` o sin `runtime/state/` => salida byte-equivalente a hoy
   (sin warning); con ambos activos y drift => WARNING (no hard-fail).
6. Determinismo del replay (negative replay sin side-effects, reutilizando garantias de Fase 2).

## 5. Fuera de alcance (B.1)

- Materializar/escribir los `*.json` de estado como verdad (B.2).
- Hard-fail del validador por drift (B.3).
- Prohibir/migrar la edicion manual (B.4).
- Cambio incompatible del flujo manual => blocked + DECISION.

## 6. Invariantes y SemVer

- I5/I6 extendidos a estado de protocolo en modo observacional (no-enforcing en B.1).
- Objetivo final: `hot *.json == materializa(replay(log))` como hard-gate (B.3).
- **MINOR** (aditivo, config-gated, fallback byte-equivalente).
