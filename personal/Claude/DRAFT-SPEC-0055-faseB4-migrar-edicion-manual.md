---
spec_id: SPEC-0055-faseB4-migrar-edicion-manual
task_id: TASK-0069
type: implementation
status: draft
created_at: 2026-06-07
author: Claude (arquitecto)
linked_decisions: [DECISION-0022, DECISION-0017, DECISION-0019, DECISION-0014, DECISION-0011]
relates_to: [SPEC-0039, SPEC-0052, SPEC-0053, SPEC-0054, SPEC-0038]
---

> DRAFT en personal/Claude/ (Fase B.4, ultima rebanada de la Fase B). El operador autorizo INICIAR B.4 y
> fijo la restriccion del genesis (referencia verificable, no volcado). NO promover a ready hasta: (1) B.3
> (TASK-0068) done, y (2) DECISION-0022 ratificada por el operador (cambio de frontera del modo operativo).
> Se monta sobre B.1/B.2/B.3.

# SPEC-0055 - Fase B.4: runtime escritor autoritativo + genesis por referencia + prohibir edicion manual

## 1. Objetivo

Cerrar la Fase B: el runtime pasa a ser el **escritor autoritativo** del estado de protocolo en instancias
runtime-tier que lo activen, y se **prohibe la edicion manual** de `Area_comun/state/*.json` (rechazada por el
hard-gate de B.3 como drift). La migracion inicial usa un **genesis por referencia** (no por volcado) segun
DECISION-0022.

## 2. Genesis por referencia (restriccion del operador, DECISION-0022 punto 2)

Hoy `write_genesis` (B.2) emite un evento `protocol.genesis` que incrusta el estado. B.4 lo cambia a la forma
de **referencia verificable**:

1. **Snapshot content-addressed fuera del prompt.** El estado de corte canonico se persiste en
   `runtime/state/snapshots/<hash>.json` (o ruta equivalente), donde `<hash>` es el hash canonico del
   snapshot. No entra al contexto del agente ni se incrusta en el evento.
2. **Evento genesis = puntero verificable.** El payload del evento `protocol.genesis` registra solo:
   `snapshot_ref = { hash, commit, actor, timestamp, schema_version }`.
   - `hash`: hash canonico del snapshot (integridad / content-addressing).
   - `commit`: SHA de git del corte (trazabilidad).
   - `actor`: quien hizo el corte.
   - `timestamp`: logico/provisto como argumento (NO reloj del runtime; preserva el determinismo del replay,
     Fase 2 negative-replay).
   - `schema_version`: version del esquema del snapshot.
3. **Replay verifica e hidrata bajo demanda.** Al encontrar un `protocol.genesis` con `snapshot_ref`, el
   replay carga `runtime/state/snapshots/<hash>.json`, **recomputa el hash canonico y exige que coincida**
   con `snapshot_ref.hash` (si no coincide o falta => error de integridad, bloqueo seguro), y materializa
   desde ahi. El snapshot se consulta solo cuando el runtime lo necesita (no en cold-start del agente).
4. **Compatibilidad:** se mantiene el camino de B.1 (genesis embebido) para los golden existentes si hace
   falta, pero el genesis AUTORITATIVO (migracion de produccion) usa la forma por referencia. Documentar cual
   es cual.

## 3. Modo autoritativo + prohibicion de edicion manual

1. **Flag de modo** `event_state.authoritative` (live + template, default false) ADEMAS de
   `enabled+materialize+enforce`. Solo aplica a `adoption_tier=runtime`.
2. **Prohibicion:** con el modo on, la edicion manual de `Area_comun/state/*.json` produce drift y es
   **rechazada** por el hard-gate de B.3 (validador fail + apply aborta). El flujo correcto: emitir intents
   al runtime. (No se anade un mecanismo de bloqueo nuevo: se reusa el enforce de B.3; B.4 = migracion +
   activacion + documentacion del modo.)
3. **Migracion asistida:** un comando/operacion explicita que (a) escribe el snapshot content-addressed,
   (b) emite el evento genesis por referencia, (c) deja el estado listo para operar bajo runtime-escritor.
   Reversible (apagar flags) hasta la prohibicion dura.
4. **coordination-tier intacto:** sin `runtime/` no aplica; edicion manual sigue siendo el modo.

## 4. Docs

- `README_INSTANCIACION` / `N_AGENT_RUNTIME`: como migrar de edicion-manual a runtime-escritor, como operar
  (intents en vez de editar JSON), como revertir, y la nota de que el genesis es una referencia (el snapshot
  vive content-addressed fuera del prompt).
- Nota en `AGENTS.md`/`.template` + `TASK_PROTOCOL` (DECISION-0022): en modo autoritativo las transiciones
  pasan por el runtime; edicion manual del estado prohibida.

## 5. Tests (golden determinista, sin red)

1. `write_genesis` por referencia: escribe `snapshots/<hash>.json` + evento con `snapshot_ref` (hash/commit/
   actor/timestamp/schema_version); el evento NO contiene el estado completo.
2. Round-trip: genesis-ref -> replay carga el snapshot por hash -> materializa -> mismo estado canonico.
3. Integridad: snapshot alterado o hash que no coincide => error/bloqueo seguro (no materializa basura).
4. Cold-start liviano: el event log con genesis-ref es mucho mas pequeno que con genesis embebido (asercion
   de tamano/forma: el evento no incluye el blob de estado).
5. Modo autoritativo on + edicion manual simulada => hard-fail (reusa B.3); off => byte-equivalente.
6. Determinismo: replay sin reloj/red (timestamp provisto); negative-replay intacto.
7. Regresion: suite runtime + B.1/B.2/B.3 intactos; coordination-tier sin cambios; fallback N=2 byte-equivalente.

## 6. Fuera de alcance

- Encender el modo autoritativo en el repo vivo (decision/operacion aparte del operador).
- Mecanismos de bloqueo del sistema de archivos (la prohibicion es por gate + proceso, no por permisos de FS).
- Cambiar el contrato del turn schema mas alla de lo necesario para el intent de transicion.

## 7. SemVer

- Lo fija el operador al ratificar DECISION-0022: MINOR-con-migracion (off-by-default, opt-in, coordination
  intacto) o MAJOR si se considera que cambia el contrato operativo de una instancia valida. Genesis-por-
  referencia es aditivo y favorable al cold-start.

## 8. Secuencia

Encolar como TASK-0069 SOLO cuando: B.3 (TASK-0068) este done Y DECISION-0022 este ACCEPTED por el operador.
Promover de a una (DECISION-0020).
