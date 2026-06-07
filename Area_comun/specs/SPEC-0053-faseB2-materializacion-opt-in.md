---
spec_id: SPEC-0053-faseB2-materializacion-opt-in
task_id: TASK-0067
type: implementation
status: accepted
created_at: 2026-06-07
author: Claude (arquitecto)
linked_decisions: [DECISION-0017, DECISION-0015, DECISION-0014, DECISION-0011]
relates_to: [SPEC-0039, SPEC-0052, SPEC-0038]
---

> Segunda rebanada de la Fase B (SPEC-0039 sec.4, decomposicion en SPEC-0052). Construye sobre B.1
> (TASK-0066: replay/materialize/genesis/drift read-only). B.2 hace la materializacion OPT-IN: bajo flag
> explicito y solo en instancias runtime-tier, el runtime escribe los *.json desde el snapshot del log
> (log = fuente de verdad). El drift sigue en modo WARNING (no hard-fail; eso es B.3). El flujo de edicion
> manual del repo vivo NO se prohibe todavia (eso es B.4). Aditivo, gateado, off=byte-equivalente. Cambio
> incompatible del flujo manual => blocked + DECISION.

# SPEC-0053 - Fase B.2: materializacion opt-in del estado de protocolo

## 1. Objetivo

Permitir que el runtime MATERIALICE los `*.json` de estado (TASK_INDEX/PROJECT_STATE/CLAIMS) desde
`replay(log)` como fuente de verdad, de forma OPT-IN y reversible, reutilizando la maquinaria pura de B.1
(`materialize_protocol_state`, `build_genesis_snapshot`, `protocol_state_drift`). No cambia el default: con
la feature apagada, el comportamiento es byte-equivalente al actual (edicion manual intacta).

## 2. Alcance (aditivo, gateado, off=byte-equivalente)

1. **Genesis materializado:** una operacion explicita (p.ej. `protocol_replay.write_genesis(root)` + CLI/
   entrypoint del runtime) que, a partir del estado vivo, emite el evento/snapshot genesis al log y deja el
   log como fuente reproducible. No corre en validacion ni en apply; es un paso operativo deliberado.
2. **Materializacion opt-in:** una funcion `materialize_to_disk(root, snapshot)` que escribe los tres
   `*.json` canonicos desde el snapshot, gobernada por un modo nuevo `event_state.materialize` (default
   false) ADEMAS de `event_state.enabled`. Solo aplica en `adoption_tier=runtime`. Determinista y atomica
   (escritura todo-o-nada, consistente con la robustez de apply/TASK-0041); preserva encoding ASCII/sin BOM
   (DECISION-0012) y formato canonico.
3. **Cableado en el runtime SOLO:** la materializacion se invoca desde el path del runtime
   (`orchestrator`/`apply`) cuando `event_state.enabled && event_state.materialize && tier==runtime`, tras
   aplicar un turno. Si cualquiera de los flags esta off => el runtime NO materializa (comportamiento M2/actual).
4. **Drift sigue WARNING** (B.1). No se convierte en hard-fail (B.3, gateada).
5. **Idempotencia round-trip:** `materialize_to_disk(replay(log))` seguido de `replay(log)` no cambia el
   estado (estable); re-materializar es no-op si no hay drift.
6. Golden `examples/runtime_protocol_materialize_cases` + CI. Paridad de comportamiento py (la materializacion
   es del runtime py; el validador .ps1 no cambia su contrato).

## 3. Limites duros (NO en B.2)

- NO hard-fail por drift (B.3). NO prohibir/migrar la edicion manual (B.4). El repo vivo sigue en edicion
  manual: NO encender `event_state.materialize` en la instancia viva en esta tarea (queda off por defecto;
  encenderlo en el repo vivo es decision del operador).
- NO tocar el contrato del turn schema ni romper el fallback N=2.
- Cambio incompatible del flujo manual o del contrato => `blocked` + pregunta.

## 4. Tests (golden determinista, sin red)

1. `materialize_to_disk` desde un snapshot escribe los tres `*.json` canonicos esperados (encoding ASCII/sin BOM).
2. Round-trip: estado vivo -> genesis -> replay -> materialize -> mismo estado canonico (idempotente).
3. Atomicidad: un fallo simulado a mitad de escritura no deja `*.json` parcial (todo-o-nada).
4. Gating: con `materialize=false` o `enabled=false` o `tier!=runtime`, el runtime NO escribe (byte-equivalente).
5. Con materializacion on y log coherente, el validador no reporta drift; con divergencia introducida, WARNING.
6. Regresion: suite runtime completa + B.1 (`runtime_protocol_replay_cases`) intactos; fallback N=2 byte-equivalente.

## 5. SemVer

- MINOR (aditivo, doble-gated `enabled`+`materialize`, solo runtime-tier, off=byte-equivalente). La promocion
  a hard-fail (B.3) y la prohibicion de edicion manual (B.4) se evaluan por separado (posible MAJOR en B.4).
