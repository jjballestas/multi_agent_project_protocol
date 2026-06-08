---
spec_id: SPEC-0066-next-actions-intent-y-prune-submit-intent
task_id: TASK-0085
type: design
status: ready
created_at: 2026-06-08
author: Claude (arquitecto)
linked_decisions: [DECISION-0022, DECISION-0017, DECISION-0014, DECISION-0020]
relates_to: [TASK-0084, TASK-0065, SPEC-0063]
---

> PROMOVIDA por Claude (2026-06-08) bajo enforce=true (authoritative OFF). Cierra el GAP que congelamos al
> encender enforce: `PROJECT_STATE.next_actions` (y narrativa) no tiene intent en submit_intent, y el prune
> editaba `*.json` a mano (incompatible con enforce -> lo congelamos con maintenance.enabled=false).

# Diseno - Intent de next_actions/narrativa + prune via submit_intent

## 1. Objetivo

Bajo `event_state.enforce=true`, TODA mutacion del ledger debe pasar por `submit_intent` o hard-failea. Hoy
faltan dos caminos: (a) actualizar campos narrativos de `PROJECT_STATE` (`next_actions`, y por extension
`risks`/`open_questions`) y (b) el prune (`scripts/prune_state.py --apply`), que reescribe
`PROJECT_STATE`/`TASK_INDEX` y condensa `next_actions` por edicion directa. Este spec agrega un intent propio
para la narrativa y reencauza el prune por submit_intent, para poder **descongelar** el prune sin romper enforce.

## 2. Estado actual (punto de partida)

- `submit_intent` soporta intents: `task_status`, `task_upsert`, `claim`, `decision` (ver `validate_intent`).
  NINGUNO toca `next_actions`. Por eso lo dejamos materializado/congelado al encender enforce (DECISION-0026
  no autoriza edicion manual de `state/*.json`).
- `scripts/prune_state.py --apply` (DECISION-0014/TASK-0065) condensa `next_actions` y archiva entradas
  terminales (`active_tasks` done, claims released) escribiendo los `*.json` a mano. CONGELADO con
  `maintenance.enabled=false` SOLO en la instancia viva; el template queda intacto.
- La materializacion (`materialize_protocol_state`) preserva `next_actions` y demas campos no-task desde el
  snapshot de genesis (verificado en TASK-0084: tras el cutover, decisions/next_actions intactos).

## 3. Alcance

### 3.1 Intent nuevo de narrativa
- Nuevo `kind` (p.ej. `project_narrative`) en `submit_intent` que actualiza campos narrativos de
  `PROJECT_STATE` de forma **idempotente** y **determinista**: al menos `next_actions` (append y/o set);
  considerar `risks`/`open_questions` si es barato y simetrico.
- **Capability**: `orchestrator` (analogo a `task_upsert`). **required_scopes**: `Area_comun/state/PROJECT_STATE.json`
  (o selector `#next_actions`). Cubierto por claim activo del actor.
- La materializacion debe aplicar el intent sobre el estado replayed sin romper la identidad replay==hot
  (drift 0). El evento se registra como `intent.applied` igual que los demas.

### 3.2 Prune via submit_intent (descongelar)
- `prune_state.py --apply` deja de editar `*.json` a mano: arma y emite sus cambios como transaccion(es)
  `submit_intent --intents`:
  - condensado de `next_actions` -> via el intent de narrativa (3.1) con el centinela determinista existente.
  - archivado de entradas terminales (`active_tasks` done, claims released) -> via los intents existentes
    apropiados (o un mecanismo de archivado que respete el event-sourcing; no por edicion directa).
- `maintenance.enabled` se **re-habilita en la instancia viva** SOLO despues de verificar en vivo que el prune
  emite por submit_intent con drift 0. El **template queda intacto** (no cambia el default del master).
- `--check` sigue read-only (inocuo bajo enforce).

### 3.3 Verificacion
- **EN VIVO (no solo golden)**: ejecutar el intent de narrativa y un prune real sobre la instancia viva (o un
  clon fiel) y confirmar `drift 0` tras cada transaccion + validador verde bajo enforce.
- **Golden de replay-identidad**: una secuencia (narrativa + prune) aplicada por submit_intent sobre un fixture
  drift-0 -> replay(log) materializa identico al hot state (round-trip = identidad), idempotente.
- Regresiones existentes verdes (cutover/enforce/materialize/cross-FS). Paridad `.ps1` donde aplique + CI.

## 4. Invariantes
1. Off/sin enforce => comportamiento previo; template byte-equivalente (master intacto).
2. submit_intent exige drift 0 antes y deja drift 0 despues (heredado).
3. Determinista, idempotente, neutral, ASCII, sin secretos.
4. El intent de narrativa NO habilita edicion manual; es el unico camino para next_actions bajo enforce.

## 5. Cierre (DoD)
- Intent de narrativa implementado + prune reencauzado por submit_intent + `maintenance.enabled` re-habilitado
  en la instancia viva (template intacto).
- Verificado EN VIVO con drift 0 (narrativa + prune) + golden de replay-identidad + regresiones verdes.
- El intent nuevo validado **aparte como deliverable** (su golden/uso documentado).
- Handoff autocontenido; release atomico; TODO por submit_intent (enforce ON).

## 6. Fuera de alcance
- `authoritative=true` (escritor-unico real), SA.4, Capa C del bridge: cada uno en su ventana posterior.
- Cambiar el default del template (queda intacto).
