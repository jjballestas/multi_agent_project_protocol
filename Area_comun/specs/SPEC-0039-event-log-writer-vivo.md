---
spec_id: SPEC-0039-event-log-writer-vivo
task_id: TASK-0048
type: implementation
status: accepted
created_at: 2026-06-06
author: Claude (arquitecto)
linked_decisions: [DECISION-0017, DECISION-0015, DECISION-0009, DECISION-0014, DECISION-0011]
relates_to: [SPEC-0038]
---

> SPEC de la Capa A.1 del inventario de cierre del nucleo N-agente (consolidacion, decision del
> operador 2026-06-06). Alcance aprobado: **A -> B incremental** (DECISION-0017). La Fase A (control-plane
> gate) se implementa ya (TASK-0048); la Fase B (replay del estado de protocolo) queda especificada y
> gateada. Cierra el FOLLOW-UP rastreado desde Fase 2 (TASK-0044).

# SPEC-0039 - Event log como writer vivo del estado

## 1. Problema

El event log (`runtime/eventlog.py`, Fase 2) existe y esta probado, pero es **aditivo/observacional**,
no el writer vivo del estado:

1. `apply.py` escribe el estado del protocolo DIRECTO a `Area_comun/state/*.json`. El event log no
   interviene en esa escritura.
2. `replay_events()` reconstruye SOLO el **control-plane de concurrencia** (`aggregate_versions`,
   `fencing_tokens`, `leases`, `idempotency_keys`, `rejections`), NO el estado de protocolo (status de
   tareas, claims, active_tasks).
3. `assert_snapshot_matches()` no esta cableado al validador global ni a apply/orchestrator.
4. Hoy la mayoria de las transiciones del estado de protocolo las hacen los agentes editando los JSON a
   mano, no el runtime.

Consecuencia: los criterios 11-12 de SPEC-0038 e invariantes I5/I6 no estan activos sobre el estado vivo.

## 2. Decision de alcance (DECISION-0017): A -> B incremental

- **Fase A (esta SPEC, TASK-0048):** control-plane gate. Bajo riesgo, aditivo, reversible.
- **Fase B (especificada, gateada):** estado de protocolo en el log + materializacion + genesis-snapshot
  + ventana de transicion warning->hard-fail. Se activa cuando el runtime sea el escritor habitual.

(Opciones descartadas por el operador: "solo A" sin camino a B, "B directa" por su alto impacto inmediato,
y "C dual-track" por complejidad/drift. Ver DECISION-0017.)

## 3. Fase A - Control-plane gate (alcance de TASK-0048)

### 3.1 Emision desde el runtime
En los turnos ejecutados por el runtime (`orchestrator --run` -> `apply.py`), el runtime invoca el
`EventWriter`:
- `acquire_claim(...)` al tomar un claim (lease + fencing_token por-aggregate).
- `apply_intent(...)` al aplicar una transicion (idempotency_key por tupla actor/task/transition/attempt/
  fencing; rechazo de fencing obsoleto).
De modo que el control-plane del log refleje los claims/intents que el runtime realmente aplica.

### 3.2 Gate de consistencia
- `assert_snapshot_matches(root)` como **hard-gate en apply** ANTES de commitear el turno del runtime:
  si el snapshot almacenado no coincide con `rebuild_snapshot` (up_to_seq + hash canonico), se aborta el
  commit (atomicidad: discard + block), consistente con la robustez de TASK-0041.
- El **validador global** (`scripts/validate_collaboration_state.py` y `.ps1`) corre
  `assert_snapshot_matches` **cuando `runtime/state/` existe y no esta vacio**. Asi, si el event log es
  writer activo, un snapshot incoherente es hard-fail repo-wide (cierra el FOLLOW-UP de Fase 2).

### 3.3 Fallback
- Si `runtime/state/` no existe o esta vacio (estado actual del repo vivo, donde el log aun no es writer
  del estado de protocolo), el gate global NO aplica: el validador se comporta como hoy. **Fallback N=2 y
  el flujo de edicion manual actual quedan intactos.**

### 3.4 Tests (golden nuevo: examples/runtime_eventlog_gate_cases)
- mismatch de snapshot detectado => apply aborta el commit (atomicidad).
- snapshot coherente => apply commitea.
- integracion apply+eventlog: un turno de runtime emite acquire_claim/apply_intent y el control-plane del
  log queda coherente con el snapshot.
- fallback: sin runtime/state, validador global verde (comportamiento actual).
- determinismo del replay (sin reloj/red), reutilizando las garantias del negative replay de Fase 2.

## 4. Fase B - Estado de protocolo en el log (ESPECIFICADA, GATEADA - no en TASK-0048)

Cuando el operador decida activarla:
- Extender `replay_events` para reconstruir el estado de protocolo (TASK_INDEX/PROJECT_STATE/CLAIMS) a
  partir de eventos de transicion; materializar los `*.json` desde el snapshot (log = fuente de verdad).
- `genesis-snapshot`: convertir el estado actual del repo en el evento/snapshot inicial.
- Ventana de transicion: el validador reporta drift entre hot `*.json` y `materializa(replay(log))` como
  **warning** primero, y se promueve a **hard-fail** cuando el runtime sea el escritor habitual.
- Migrar/prohibir la edicion manual de los `*.json` de estado de protocolo (pasa por el runtime).
- Invariante objetivo: `hot *.json == materializa(replay(log) hasta up_to_seq)`.
- Tests: replay del estado de protocolo, materializacion idempotente, genesis-snapshot, property I5/I6
  sobre estado de protocolo, concurrency simulation (inventario A.4) usando el log como verdad.

## 5. Invariantes

- I5: todo evento aplicado incrementa `seq` y `aggregate_version` (ya en eventlog).
- I6: `replay(log)` reconstruye el mismo snapshot; negative replay sin side-effects (Fase 2; extender a
  estado de protocolo en Fase B).
- I8: ningun intent se aplica dos veces (idempotencia, ya en eventlog).
- Fase B: `hot *.json == materializa(replay(log))` como hard-gate del validador global.

## 6. Riesgos y mitigaciones

- Doble fuente de verdad durante la transicion -> Fase B usa modo warning antes de hard-fail.
- Ediciones manuales concurrentes rompen el invariante si B se activa sin migrar el flujo -> B gateada y
  con ventana de transicion; Fase A no toca el flujo manual (gate solo si runtime/state existe).
- Determinismo del replay -> mantener negative replay (sin reloj/red).

## 7. SemVer

- Fase A: MINOR (aditivo, config/runtime-gated, fallback intacto).
- Fase B: MINOR-con-migracion o MAJOR si rompe el flujo de edicion manual; se evalua al activarla.
