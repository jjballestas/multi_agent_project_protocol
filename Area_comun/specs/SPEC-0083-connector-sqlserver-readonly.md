---
spec_id: SPEC-0083
task_id: TASK-0121
type: security
status: accepted
linked_decisions:
  - DECISION-0044
  - DECISION-0040
  - DECISION-0041
created_at: 2026-06-19
updated_at: 2026-06-19
author: Arquitecto
---

# SPEC-0083 - Connector READ-ONLY (SQL Server), deny-by-default

## Context

DECISION-0044 introduce una capacidad de connector neutral (`connectors/`), read-only, deny-by-default,
con `trust_boundary` por conector y el principio "el connector no concede autoridad". Esta SPEC fija el
diseno tecnico verificable del framework + el primer adaptador (SQL Server read-only) con backend de
fixtures. **Pista propia, independiente de #4.** El uso vivo contra una DB real es un GO posterior tras
verificacion §9 por Codex (DECISION-0041); esta SPEC NO ejecuta lectura viva.

## Scope

- Capa neutral `connectors/`: framework con un descriptor `trust_boundary` y una interfaz de lectura
  read-only, deny-by-default.
- Primer adaptador `connectors/sqlserver_readonly/`: clasifica la operacion solicitada y RECHAZA toda
  no-lectura ANTES de tocar la fuente; con la capacidad OFF (default) no abre conexion viva.
- **Backend de fixtures** (result sets grabados/fake) para el golden: sin red, sin DB, determinista.
- Registro de connectors **fuera de `protocol.config.json`** (genesis intacto), default `enabled:false`.
- Gate de neutralidad de dominio sobre `connectors/`.

## Out Of Scope

- Lectura viva contra la DB real (GO posterior tras §9 por Codex, DECISION-0041/DECISION-0044 sec.4).
- `profiles/financiero_presupuesto/` y cualquier regla fiscal/negocio.
- Connectors Git/CI; exposicion MCP concreta; tocar #4 (flags, provisioning, flip); tocar la DB de Budget.

## Diseno

### Capa y ubicacion

```
connectors/
  README.md                       (que es un connector; principios duros; off-by-default)
  framework/                      (neutral: Connector base, TrustBoundary, errores, clasificador read-only)
  sqlserver_readonly/             (neutral: adaptador SQL Server read-only + backend de fixtures)
  connectors.config.json          (registro; FUERA de protocol.config.json; default enabled:false)
examples/connector_sqlserver_readonly_cases/   (golden determinista, fixtures-only)
```

El **core neutral no importa** `connectors/`; ningun gate/CI obligatorio del core depende de el (solo su
propio golden corre en CI). `connectors/` se incluye en el barrido de `scan_domain_neutrality`.

### `trust_boundary` por conector (descriptor)

```
{
  "id": "budget-sqlserver-ro",
  "kind": "sqlserver_readonly",
  "enabled": false,                 // off-by-default; uso vivo = GO posterior tras §9
  "read_only": true,
  "grants_no_authority": true,      // el dato es evidencia, no autoridad ni mutacion
  "persists_outputs": false,        // no escribe ledger/event log/estado
  "access": { "database": "<nombre>", "allow": { "schemas": [], "objects": [] } },  // allowlist
  "live_connection": { "principal_least_privilege_required": true }  // verificado §9 antes de vivo
}
```

`access.allow` es allowlist deny-by-default: lo no listado se niega. Los nombres concretos de
schema/objetos del Budget van en la instancia (no en el core neutral).

### Clasificador read-only deny-by-default

`classify(operation) -> ALLOW(read) | DENY(reason_class)` se ejecuta **antes de cualquier round-trip**:

- ALLOW: solo lectura -- `SELECT` de un solo statement; procedimientos almacenados **explicitamente
  allowlisted como read-only** (default: ninguno).
- DENY (clase explicita, sin tocar la fuente): DML (`INSERT`/`UPDATE`/`DELETE`/`MERGE`), DDL
  (`CREATE`/`ALTER`/`DROP`/`TRUNCATE`), `EXEC` no-allowlisted, **multi-statement / stacked** (cualquier
  `;` con un statement no-lectura, o batch), y cualquier verbo no reconocido (deny-by-default: lo que no
  se prueba lectura, se niega).

El parser es **conservador**: ante duda, DENY. (Es enforcement, no heuristica de conveniencia.)

### "No concede autoridad" / frontera de datos

- El modulo del connector **no importa** ningun escritor del ledger/event log (`runtime` ledger ops) y no
  expone API de escritura. Leer **no emite eventos** (cero append a `runtime/state/events.jsonl`).
- Las salidas son objetos en memoria devueltos al llamador (evidencia); **no se persisten** a estado ni
  event log. **PII de terceros NUNCA al event log** (DECISION-0040). DEF-PII (TASK-0118) sigue diferida:
  esta SPEC fija la frontera, no un detector.

### Off-by-default y fail-closed

- `connectors.config.json` default `enabled:false`. Con OFF, una llamada que pida **conexion viva**
  falla-cerrada con clase explicita (no intenta conectar). El **golden corre con fixtures** y NO depende
  del flag (prueba el contrato, no el vivo).
- Genesis intacto: el registro vive FUERA de `protocol.config.json`; no lo consume
  `compute_genesis_prev_hash` -> aterrizar la capacidad no cambia drift (no re-genesis).

### Backend de fixtures (golden)

`FixtureBackend` mapea (query read-only normalizada) -> result set grabado (filas deterministas), sin
driver ni red. El adaptador usa este backend en el golden; el backend vivo (pyodbc/pymssql u otro) es la
ruta de uso vivo, no ejercida aqui.

## acceptance_criteria

- **AC1 - trust_boundary + deny-by-default declarativo.** Un connector se declara con `trust_boundary`
  explicito (`read_only`, `grants_no_authority`, `persists_outputs:false`, `access.allow` allowlist). Lo
  no listado en `access.allow` se niega. Golden determinista.
- **AC2 - Lectura (positivo).** Un read intent (`SELECT` de un statement) contra fixtures devuelve filas
  deterministas; el resultado es evidencia en memoria.
- **AC3 - Read-only REAL (prueba negativa OBJETIVA, deny-by-default).** Cada vector de escritura/mutacion
  es RECHAZADO con clase explicita **antes de tocar el backend**, golden negativo por vector, **>= 6
  vectores**: INSERT, UPDATE/DELETE, DDL (DROP/ALTER/CREATE/TRUNCATE), EXEC no-allowlisted, multi-statement
  con escritura (stacked), y verbo no reconocido (deny-by-default). NUNCA llega un write al backend.
- **AC4 - No concede autoridad / no escribe (gate DEDICADO + behavioral).** Check dedicado: el modulo del
  connector **no importa** escritores del ledger/event log y no expone API de escritura (revision
  sustantiva, no solo grep). Behavioral en el golden: ejecutar una lectura produce **cero** eventos nuevos
  en `runtime/state/events.jsonl` y cero cambios en `Area_comun/state/*.json`.
- **AC5 - Off-by-default + fail-closed (vivo).** Default `enabled:false`. Con OFF, pedir **conexion viva**
  -> error de clase explicita, sin intentar conectar. El golden corre con fixtures independientemente del
  flag. Golden.
- **AC6 - Genesis/drift intactos.** Aterrizar `connectors/` + `connectors.config.json` (fuera de
  `protocol.config.json`) **no cambia** `compute_genesis_prev_hash` ni el drift; `validate_collaboration_state`
  sigue exit 0. Verificacion: drift 0 antes y despues (read-back, no grep).
- **AC7 - Frontera de datos / PII.** Una fila de fixture con un campo PII-like, leida, produce **cero**
  escritura al event log/estado (DECISION-0040, dos planos). Golden.
- **AC8 - Precondicion de uso vivo (§9, espejo DECISION-0041), NO ejercida aqui.** Documentada y
  fail-closed: el uso vivo exige (a) principal de minimo privilegio server-side (escritura rechazada por
  el servidor), (b) verificacion sustantiva + prueba negativa objetiva registrada por Codex (§9), (c) GO
  del operador. Sin ello, no hay conexion viva. (En esta pieza se verifica que el camino vivo esta
  cerrado por flag; la prueba negativa server-side es del GO posterior.)
- **AC9 - Neutralidad de dominio.** CERO termino fiscal/negocio en `connectors/` ni en el golden;
  `scan_domain_neutrality.py` limpio incluyendo `connectors/`.
- **AC10 - Gates verdes.** `validate_collaboration_state.py --root .` (drift B.3 = 0) + `scan_encoding.py`
  + `scan_domain_neutrality.py` + el nuevo `connector_sqlserver_readonly_cases` cableado en CI.

## test_plan

- `examples/connector_sqlserver_readonly_cases/run_connector_sqlserver_readonly_cases.py`:
  - declaracion de trust_boundary + allowlist; objeto fuera de `access.allow` -> denegado (AC1).
  - SELECT de un statement contra fixtures -> filas deterministas (AC2).
  - 6+ vectores de escritura/DDL/EXEC/stacked/verbo-desconocido -> rechazo de clase antes del backend; el
    backend de fixtures registra **cero** llamadas de ejecucion para esos vectores (AC3).
  - lectura ejecutada -> snapshot de `runtime/state/events.jsonl` sin cambios; sin import de escritores de
    ledger (AC4).
  - capacidad OFF + pedir conexion viva -> error de clase, sin intentar conectar (AC5).
  - drift 0 antes/despues de incluir la capa (read-back) (AC6).
  - fila con campo PII-like leida -> cero escritura a event log/estado (AC7).
  - reporte JSON determinista (timestamps fijos), exit 0/1.
- Gate AC4 dedicado: el modulo del connector no importa escritores del ledger/event log -> exit 1 si lo
  hace.
- Sin regresion: suites existentes verdes; `scan_domain_neutrality` cubre `connectors/` (AC9).

## closure_criteria

- AC1-AC10 cumplidos; revision maker!=checker (Codex implementa, Arquitecto reproduce); SemVer MINOR +
  CHANGELOG; memoria actualizada. **NO enciende #4** y **NO ejerce lectura viva** (eso es GO posterior
  tras §9). Drift 0.

## Risks

- **Clasificador read-only evadible (parser laxo).** Mitigacion: deny-by-default (ante duda, DENY);
  prueba negativa objetiva por vector; el uso vivo agrega least-privilege server-side (segunda capa).
- **Falsa sensacion de seguridad solo connector-side.** Declarado: el read-only real para el VIVO exige
  identidad de minimo privilegio en el servidor (DECISION-0044 sec.4); el connector-side solo es la
  primera capa.
- **Arrastrar dominio fiscal al connector.** Mitigacion: gate de neutralidad sobre `connectors/`; las
  reglas fiscales son pieza aparte (`profiles/financiero_presupuesto/`).
- **PII de fixtures/vivo al event log.** Mitigacion: el connector no escribe event log/estado (AC4/AC7);
  DEF-PII diferida; sin captura viva aqui.

## Traceability

| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| trust_boundary + deny-by-default allowlist | TASK-0121 | connector_sqlserver_readonly_cases | AC1 |
| Lectura read-only contra fixtures | TASK-0121 | golden SELECT | AC2 |
| Read-only REAL (prueba negativa >=6 vectores) | TASK-0121 | goldens negativos por vector | AC3 |
| No concede autoridad / no escribe ledger-eventos | TASK-0121 | gate AC4 + behavioral cero-eventos | AC4 |
| Off-by-default + fail-closed vivo | TASK-0121 | golden flag OFF | AC5 |
| Genesis/drift intactos (registro fuera del config) | TASK-0121 | drift 0 read-back | AC6 |
| Frontera de datos / PII fuera del event log | TASK-0121 | golden fila PII-like | AC7 |
| Precondicion uso vivo (§9 + GO), cerrada por flag | TASK-0121 | doc + fail-closed | AC8 |
| Neutralidad de dominio en connectors/ | TASK-0121 | scan_domain_neutrality | AC9 |
| Gates verdes + golden en CI | TASK-0121 | validate + scans + suite | AC10 |
