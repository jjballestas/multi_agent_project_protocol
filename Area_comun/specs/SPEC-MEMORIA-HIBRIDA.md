---
spec_id: SPEC-MEMORIA-HIBRIDA
title: "Memoria hibrida: repo caliente + archivo frio verificable + DB derivada reconstruible (implementacion del REQ v0.3.0)"
status: draft-reviewed-informal
version: 0.2.1
date: 2026-07-17
author: Arquitecto
review: "adversarial informal (subagent anti-rubber-stamp) 2026-07-14: 2 BLOCKER + 7 MAJOR + 5 MINOR, TODOS reales e INCORPORADOS en esta version (registro en s.15); review FORMAL del Analista pendiente de reactivacion de su harness. v0.2.1 (2026-07-17): provision F1 del adversarial extracted-vs-inferred (veredicto Analista 476ceac, aceptado por Operador en GO Fase A): contrato de mapeo frontmatter->edge_type (s.5.1b) + invariante I9 F1-no-infiere (s.4) + DoD F1 (s.13); patron epistemico DIFERIDO-LIMPIO a F4"
derives_from: "personal/operador/requerimientos-futuros/memoria-hibrida-db-archivo-frio/REQ-MEMORIA-HIBRIDA-DB-ARCHIVO-FRIO.md (v0.3.0, RUTA UNICA por DECISION-0081)"
linked_decisions: [DECISION-0081, DECISION-0026, DECISION-0016, DECISION-0020, DECISION-0022, DECISION-0040, DECISION-0061, DECISION-0096]
authority: "SPEC de diseno (papel). NO autoriza mover historia canonica ni activar el archivado: eso exige la DECISION de activacion que el REQ s.0.4 requiere. El build no arranca antes del cierre de la ventana medida (compromiso audit-first) salvo GO explicito del operador por fase."
---

# SPEC-MEMORIA-HIBRIDA - arquitectura implementable de la memoria hibrida

> Cumple el backlog s.17.2 del REQ (owner Arquitecto, review Analista). Convierte el REQ en
> contratos implementables: rutas concretas, DDL concreto, comandos, gates, fases con DoD y
> trazabilidad AC1-AC15. Cada garantia lleva etiqueta de la matriz de honestidad (REQ s.26.6):
> ESTRUCTURAL | ESTRUCTURAL-PENDIENTE-IMPL+TESTS | ESTRUCTURAL-SI-PRECONDICION(x) |
> DISCIPLINARIO | ABIERTO-DIFERIDO. Nada se declara cerrado sin codigo merged y test verde.

## 1. Alcance y no-alcance

EN ALCANCE (por fases, s.13): indexador read-only + DB SQLite derivada; importador canon->DB con
round-trip; stubs y cold-packs con manifest; gates rapido/completo + check de drift; revive-pack
por agente; FTS; deteccion de contradicciones; runbook.

FUERA DE ALCANCE (hereda REQ s.20, sin excepciones): reemplazar `runtime/state/events.jsonl` o
`Area_comun/state/*.json`; mover el ledger a DB; DB como writer autoritativo; cloud obligatorio;
embeddings de contenido sensible; archivar decisiones activas sin stub. ADEMAS: esta SPEC no
modifica `validate_collaboration_state.*` ni `submit_intent.py` en Fase 0-2 (los comandos nuevos
son ejecutables APARTE; la integracion al gate canonico es Fase 3+ con su propia review).

VENTANA: Fase 0 (discovery, read-only puro) puede correr en cualquier momento. Fases 1+ tocan
`scripts/` del hub -> post-cierre de la ventana medida o en instancia (Aegis/) con GO del operador.

## 2. Arquitectura de 3 planos aterrizada a rutas del protocolo

### 2.1 Plano caliente (hot) - que se lee en cold-start
Mapa concreto del subset REQ s.5.1 sobre el arbol real:

| Categoria | Ruta(s) | Regla hot |
|---|---|---|
| Contrato | `AGENTS.md`, `Area_comun/README.md`, `Area_comun/protocol/*.md`, `protocol.config.json` | siempre |
| Estado | `Area_comun/state/*.json` + `*.slim.json` | siempre (ya podados por DECISION-0014/prune) |
| Mailbox vivo | `Area_comun/mailbox/open/` | siempre |
| Tareas vivas | `Area_comun/tasks/` con status != done/cancelled | siempre |
| Tareas done recientes | ultimas `window_count` o `window_days` (s.8 Q1) | ventana |
| Handoffs | enlazados por tareas vivas + ultimos N | ventana |
| Specs | enlazadas por tareas vivas + plantillas | ventana |
| Decisiones | TODAS las activas COMPLETAS (s.8 Q3) + stubs de superseded si se enfrian | politica |
| Memoria personal | `personal/<id>/` acotada por el propio agente (DECISION-0026) | disciplina del agente |
| Manifests frios | `Area_comun/archive/manifest-*.json` | siempre (es el indice para encontrar el frio) |

### 2.2 Plano frio (cold) - donde vive la historia enfriada
Decision de ubicacion (responde REQ s.18.4): **carpeta `Area_comun/archive/` EN LA MISMA RAMA**,
con packs por lote:

```text
Area_comun/archive/
  cold-packs/
    CP-YYYYMMDD-<slug>/            (un lote de archivado = un pack)
      <artefactos movidos, ruta relativa original preservada bajo el pack>
      pack.manifest.json           (cabecera del pack: pack_id, pack_type, path, git_ref,
                                    created_at; y por artefacto: artifact_id, original_path,
                                    cold_path, sha256, git_commit_at_freeze, artifact_type,
                                    status, closed_at)
  manifest-index.json              (indice de packs: pack_id, path, sha256_manifest, artifact_count)
```

El manifest lleva TODOS los campos que `cold_packs` necesita: la tabla se reconstruye 1:1 desde
los manifests (requisito del round-trip s.6; hallazgo M1 de la review adversarial).

Razones contra las alternativas: (a) rama historica / repo satelite rompen la verificabilidad en
clon limpio con UN solo fetch (los gates y el Analista clonan main; leccion operativa repetida) y
complican la atestacion; (b) storage local no versionado pierde la garantia git. La misma-rama
conserva TODO auditable en el mismo main; el ahorro de cold-start viene de que los AGENTES no leen
`archive/` (esta fuera del hot map s.2.1), no de que los bytes desaparezcan del repo. Cuando el
TAMANO del repo (no el cold-start) sea el problema, migrar a repo satelite sera una DECISION
separada con su propia ceremonia (ABIERTO-DIFERIDO). `git sparse-checkout set --no-cone
'/*' '!Area_comun/archive'` queda documentado como OPT-IN por maquina (s.18.5), jamas requisito.

Movimiento hot->cold = `git mv` del artefacto a su pack + stub en la ruta original cuando la
politica lo exige (s.8) + fila en manifest. SIEMPRE via tarea gobernada con claim (REQ s.13).

### 2.3 DB derivada - SQLite local, gitignored, reconstruible
- Archivo: `runtime/memory/index.db`. **OJO (hallazgo M5): el `.gitignore` del HUB hoy NO cubre
  `runtime/memory/`** (el precedente de esa ruta gitignored esta en la INSTANCIA
  Zeus-protocol-Aegis, no aqui). Entregable explicito de F1: `.gitignore` += `runtime/memory/` +
  exclusion de esa ruta en `scan_encoding` (leccion conocida: un index.db a medio build pone el
  scan rojo). La DB JAMAS se commitea: es cache (REQ s.26.1). Lo commiteable son manifests, stubs
  y el archivo canonico de reglas (s.8 Q1).
- Motor: SQLite + FTS5 (verificado disponible en el sqlite3 embebido de Python 3.12 local).
  Fallback estructural: si FTS5 no esta compilado, `search_terms` + LIKE cubre busqueda basica
  (degradacion declarada, no fallo).
- Escritor UNICO de la DB: `scripts/memory/build_memory_db.py` (el "indexador"). Ningun agente
  escribe la DB a mano; ningun proceso del protocolo LEE la DB para decidir estado gobernado.

## 3. Modelo de datos (DDL objetivo v1)

Columnas = REQ s.6 verbatim; tipos y claves concretados aqui. `schema_version` global en
`PRAGMA user_version = 1`. La conexion SIEMPRE abre con `PRAGMA foreign_keys = ON` (SQLite las
ignora sin el; hallazgo MIN1) y toda clausula `REFERENCES` de este DDL es `ON DELETE CASCADE`
(el implementador la escribe explicita). Tablas SIN FK a proposito (declarado): `artifact_edges.
to_artifact_id` (edge pendiente a id aun no indexado), `artifact_versions`, `retrieval_log`,
`embeddings`, `task_context_cache` (registran historia/operacion que puede referir ids ya
purgados del indice vivo).

**Derivacion y unicidad de `artifact_id` (hallazgo MIN2):** tipos con id intrinseco (task/
decision/spec/mailbox/handoff/requirement) usan el id del frontmatter; tipos SIN id (memory/
report/artifact/runlog) usan `<type>:<relpath>`. El scan EXCLUYE `examples/**`, `**/*.template.*`
y `.protocol-tmp/**` (hoy existe colision real de TASK-0001 entre el arbol vivo y
examples/minimal_instance: sin exclusion, el upsert last-writer-wins pisaria la fila viva).

```sql
CREATE TABLE artifacts (
  artifact_id        TEXT PRIMARY KEY,          -- p.ej. TASK-0231, DECISION-0081, MSG-..., HANDOFF-...
  artifact_type      TEXT NOT NULL CHECK (artifact_type IN
    ('decision','task','spec','handoff','mailbox','report','artifact','memory',
     'state_snapshot','eventlog','runlog','requirement')),
  title              TEXT,
  status             TEXT,
  original_path      TEXT NOT NULL,
  hot_path           TEXT,
  cold_path          TEXT,
  git_commit         TEXT NOT NULL,             -- commit del blob indexado (hash por BLOB, nunca working copy)
  sha256             TEXT NOT NULL,
  created_at         TEXT, updated_at TEXT, closed_at TEXT,
  owner              TEXT, project TEXT,
  is_active_policy   INTEGER NOT NULL DEFAULT 0,
  is_hot             INTEGER NOT NULL DEFAULT 1,
  is_pii_safe        INTEGER,                   -- NULL = sin clasificar (nunca se asume safe)
  summary_short      TEXT, summary_long TEXT,
  canonicality       TEXT NOT NULL CHECK (canonicality IN
    ('canonical_file','stub','derived_index','cold_copy','external_pointer')),
  retention_class    TEXT NOT NULL CHECK (retention_class IN
    ('hot','warm','cold','sealed','do_not_archive')),
  cold_reason        TEXT,
  last_verified_at   TEXT,
  schema_version     INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX idx_artifacts_type_status ON artifacts(artifact_type, status);
CREATE INDEX idx_artifacts_hot ON artifacts(is_hot, retention_class);

CREATE TABLE artifact_edges (
  from_artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id),
  to_artifact_id   TEXT NOT NULL,               -- puede apuntar a id aun no indexado (edge pendiente)
  edge_type        TEXT NOT NULL CHECK (edge_type IN
    ('implements','reviews','supersedes','contradicts','depends_on','mentions',
     'handoff_for','mailbox_for','decision_for','spec_for')),
  source_path      TEXT NOT NULL,
  source_commit    TEXT NOT NULL,
  PRIMARY KEY (from_artifact_id, to_artifact_id, edge_type)
);

CREATE TABLE agent_memory (
  memory_id     TEXT PRIMARY KEY,
  agent_id      TEXT NOT NULL,                  -- DERIVADO del path fuente personal/<id>/ (s.26.3), jamas input libre
  scope         TEXT NOT NULL CHECK (scope IN ('personal','compartido')),
  summary       TEXT,
  source_path   TEXT NOT NULL,
  source_commit TEXT NOT NULL,
  event_seq     INTEGER,
  sha256        TEXT NOT NULL,
  valid_from    TEXT, valid_until TEXT,
  is_current    INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX idx_agent_memory_current ON agent_memory(agent_id, is_current);

CREATE TABLE cold_packs (
  pack_id         TEXT PRIMARY KEY,             -- CP-YYYYMMDD-<slug>
  pack_type       TEXT NOT NULL,
  path            TEXT NOT NULL,
  git_ref         TEXT NOT NULL,
  created_at      TEXT NOT NULL,
  sha256_manifest TEXT NOT NULL,
  artifact_count  INTEGER NOT NULL,
  validated_at    TEXT, validator_result TEXT
);

CREATE TABLE retrieval_log (
  retrieval_id   INTEGER PRIMARY KEY AUTOINCREMENT,
  requested_by   TEXT NOT NULL,
  task_id        TEXT,
  artifact_id    TEXT NOT NULL,
  reason         TEXT,
  retrieved_at   TEXT NOT NULL,
  source_commit  TEXT NOT NULL,
  sha256_verified INTEGER NOT NULL
);

CREATE TABLE artifact_versions (
  artifact_id    TEXT NOT NULL,
  version_id     INTEGER NOT NULL,
  git_commit     TEXT NOT NULL,
  event_seq      INTEGER,
  path_at_commit TEXT NOT NULL,
  sha256         TEXT NOT NULL,
  changed_at     TEXT, changed_by TEXT, change_kind TEXT, status_at_version TEXT,
  PRIMARY KEY (artifact_id, version_id)
);

CREATE TABLE artifact_content_index (
  artifact_id       TEXT PRIMARY KEY REFERENCES artifacts(artifact_id),
  content_sha256    TEXT NOT NULL,
  indexed_at        TEXT NOT NULL,
  language          TEXT,
  token_estimate    INTEGER,
  line_count        INTEGER,
  has_frontmatter   INTEGER,
  frontmatter_json  TEXT,                       -- SOLO claves de la allowlist s.7 (por VALOR)
  plain_text_excerpt TEXT,                      -- NULL salvo pii_classification.public_plane_allowed=1
  redaction_state   TEXT NOT NULL DEFAULT 'unclassified'
    CHECK (redaction_state IN ('unclassified','raw_private','redacted','public_ok'))
);

CREATE TABLE policy_status (
  decision_id   TEXT PRIMARY KEY,
  policy_state  TEXT NOT NULL CHECK (policy_state IN ('active','superseded','historical')),
  superseded_by TEXT, supersedes TEXT,
  active_from   TEXT, active_until TEXT,
  applies_to    TEXT,
  hot_required  INTEGER NOT NULL DEFAULT 0,
  reason        TEXT
);

CREATE TABLE hot_cold_rules (
  -- TABLA DERIVADA (hallazgo B2): la fuente CANONICA y VERSIONADA de las reglas es el archivo
  -- Area_comun/protocol/MEMORY_HOT_COLD_RULES.json (fuera del config pineado; mismo patron que
  -- COMMIT_TRAILERS.json / INTAKE_GATE.json). El indexador DERIVA esta tabla de ese archivo en
  -- cada build; una fila sin respaldo en el archivo = drift (--full falla). Crear/cambiar el
  -- archivo = DECISION (la de activacion del REQ s.0.4 lo anexa).
  rule_id                     TEXT PRIMARY KEY,
  artifact_type               TEXT NOT NULL,
  selector                    TEXT NOT NULL,    -- expresion documentada (status/glob), evaluada por el indexador
  target_retention_class      TEXT NOT NULL,
  window_days                 INTEGER,
  window_count                INTEGER,
  requires_stub               INTEGER NOT NULL DEFAULT 0,
  requires_active_policy_check INTEGER NOT NULL DEFAULT 0,
  enabled                     INTEGER NOT NULL DEFAULT 0,   -- OFF por defecto: activar regla = DECISION
  created_by_decision         TEXT
);

CREATE TABLE stubs (
  stub_id            TEXT PRIMARY KEY,
  artifact_id        TEXT NOT NULL REFERENCES artifacts(artifact_id),
  stub_path          TEXT NOT NULL,
  original_path      TEXT NOT NULL,
  cold_path          TEXT NOT NULL,
  git_commit         TEXT NOT NULL,
  sha256             TEXT NOT NULL,             -- sha del artefacto FRIO al que apunta
  summary            TEXT,
  rehydration_command TEXT NOT NULL,
  created_at         TEXT NOT NULL,
  validated_at       TEXT
);

CREATE TABLE validation_runs (
  validation_id   INTEGER PRIMARY KEY AUTOINCREMENT,
  run_type        TEXT NOT NULL CHECK (run_type IN ('hot_fast','full_rebuild','drift_check')),
  started_at      TEXT NOT NULL, finished_at TEXT,
  actor           TEXT NOT NULL,
  git_commit      TEXT NOT NULL,
  event_seq       INTEGER,
  result          TEXT NOT NULL CHECK (result IN ('pass','fail')),
  errors_json     TEXT, warnings_json TEXT,
  checked_artifact_count INTEGER,
  db_hash         TEXT, manifest_hash TEXT
);

CREATE TABLE pii_classification (
  artifact_id          TEXT PRIMARY KEY REFERENCES artifacts(artifact_id),
  classifier_version   TEXT NOT NULL,
  classified_at        TEXT NOT NULL,
  pii_state            TEXT NOT NULL CHECK (pii_state IN ('clean','findings','not_scanned')),
  finding_count        INTEGER NOT NULL DEFAULT 0,
  finding_types_json   TEXT,
  public_plane_allowed INTEGER NOT NULL DEFAULT 0,   -- default CERRADO
  redaction_required   INTEGER NOT NULL DEFAULT 0,
  redaction_artifact_id TEXT
);

CREATE TABLE search_terms (
  artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id),
  term        TEXT NOT NULL,
  field       TEXT NOT NULL,
  weight      REAL NOT NULL DEFAULT 1.0,
  source      TEXT NOT NULL,
  PRIMARY KEY (artifact_id, term, field)
);
-- FTS5 (si disponible): tabla virtual sobre title/summary/plain_text_excerpt SOLO public_ok.
-- CREATE VIRTUAL TABLE artifacts_fts USING fts5(artifact_id UNINDEXED, title, summary, excerpt);

CREATE TABLE embeddings (            -- Fase 4+; NO se crea antes de la politica PII de embeddings
  artifact_id  TEXT NOT NULL,
  chunk_id     TEXT NOT NULL,
  model        TEXT NOT NULL,
  dimension    INTEGER NOT NULL,
  embedding    BLOB NOT NULL,
  source_sha256 TEXT NOT NULL,
  created_at   TEXT NOT NULL,
  pii_safe     INTEGER NOT NULL,
  PRIMARY KEY (artifact_id, chunk_id, model)
);

CREATE TABLE task_context_cache (
  task_id                  TEXT NOT NULL,
  context_hash             TEXT NOT NULL,
  generated_at             TEXT NOT NULL,
  included_artifacts_json  TEXT NOT NULL,
  excluded_artifacts_json  TEXT,
  summary                  TEXT,
  token_estimate           INTEGER,
  valid_until_event_seq    INTEGER,
  PRIMARY KEY (task_id, context_hash)
);
```

## 4. Invariantes (etiquetados, matriz REQ s.26.6)

- **I1 - La DB es cache; el canon (git + events.jsonl + packs) gana siempre.** Reconstruibilidad
  se DEMUESTRA con round-trip (s.6). Etiqueta: ESTRUCTURAL-PENDIENTE-IMPL+TESTS.
- **I2 - Cero writers paralelos al estado gobernado.** El indexador es read-only sobre el repo:
  no importa `submit_intent`, no abre `events.jsonl` en escritura, no toca `Area_comun/state/`.
  Su unico output es `runtime/memory/index.db` (gitignored). Etiqueta:
  ESTRUCTURAL-PENDIENTE-IMPL+TESTS (test: correr indexador + `git status --porcelain` limpio +
  validate exit 0 antes/despues).
- **I3 - PII default-cerrado.** `plain_text_excerpt` y FTS de contenido SOLO se pueblan si
  `pii_classification.public_plane_allowed=1`; sin clasificar = sin excerpt (NULL) y
  `redaction_state='unclassified'`. Frontmatter indexado por ALLOWLIST DE CLAVES con validacion
  por VALOR (s.7). Etiqueta: ESTRUCTURAL-PENDIENTE-IMPL+TESTS (test negativo: PII plantada ->
  excerpt NULL + drift-check falla si aparece en tabla publicable).
- **I4 - Historia no se mueve sin decision.** Las reglas viven CANONICAS en
  `Area_comun/protocol/MEMORY_HOT_COLD_RULES.json` (versionado, auditable; B2); `enabled=0` por
  defecto; activar una regla exige `created_by_decision` no-nulo y la DECISION de activacion del
  REQ s.0.4. El movimiento fisico es una tarea gobernada con claim (DECISION-0020). Etiqueta:
  DISCIPLINARIO en Fase 0-1; ESTRUCTURAL-PENDIENTE-IMPL+TESTS desde Fase 2 (`check_memory_db_drift`
  falla si `archive/` contiene artefactos sin fila de manifest o sin regla habilitada EN EL
  ARCHIVO CANONICO que los cubra).
- **I5 - Fallo seguro sin DB.** Ningun flujo vivo del protocolo (validate, submit_intent, crons,
  gates) LEE la DB. Borrarla degrada busqueda, no la cola. Etiqueta (corregida por hallazgo M2:
  sin codigo merged nada es ESTRUCTURAL, y el cableado F3+ de `--fast` al pipeline podria
  hacer que un gate leyera la DB): **ESTRUCTURAL-SI-PRECONDICION(el `--fast` que se cablee a un
  gate deriva sus checks de ARCHIVOS canonicos -- decisiones + stubs + manifests -- nunca de la
  DB, y degrada a verde si la DB no existe) + PENDIENTE-IMPL+TESTS** (test: gates verdes con
  index.db borrado).
- **I6 - Identidad de memoria derivada del chokepoint.** `agent_memory.agent_id` se deriva del
  path fuente `personal/<id>/...` (espejo DECISION-0016); `scope='compartido'` solo para fuentes
  bajo `Area_comun/`. No existe parametro de CLI que fuerce agent_id sobre una fuente personal
  ajena. Etiqueta: ESTRUCTURAL-PENDIENTE-IMPL+TESTS (test: intentar indexar personal/X como
  agente Y -> rechazo).
- **I7 - Decision activa jamas invisible.** `policy_status.hot_required=1` => o el .md completo
  esta hot, o existe stub hot verificado. `check_memory_db_drift` falla si no. Etiqueta:
  ESTRUCTURAL-PENDIENTE-IMPL+TESTS.
- **I8 - Hashes por BLOB de git.** Todo sha256 de atestacion/manifest se computa sobre
  `git show <commit>:<path>`, nunca working copy (leccion CRLF, cross-atest Entrada 1).
  Etiqueta: DISCIPLINARIO (regla de implementacion) + test golden con CRLF plantado.
- **I9 - F1 no infiere (provision del adversarial extracted-vs-inferred, 2026-07-17).** TODA arista
  que el indexador F1 escribe en `artifact_edges` deriva 1:1 de una clave de frontmatter allowlisted
  (s.7) segun la tabla de mapeo de s.5.1b -- el indexador F1 NO computa aristas por heuristica
  (relatedness, cercania, texto del cuerpo). Los edge_type sin clave productora en la tabla son
  enums RESERVADOS que F1 no produce. Si al implementar F1 algun edge_type resultara requerir
  heuristica, se DETIENE y se re-evalua el patron epistemico diferido a F4 (etiquetado
  EXTRACTED-vs-INFERRED + procedencia fail-closed) ANTES de producirlo. Etiqueta:
  ESTRUCTURAL-PENDIENTE-IMPL+TESTS (tests: fixture sin claves de relacion -> 0 aristas; cada arista
  producida trazable a su clave fuente; enum reservado producido -> fallo del test).

## 5. Flujos

### 5.1 Escritura (indexacion) - read-only, post-commit
1. El agente escribe el artefacto canonico como HOY (archivo + submit_intent si toca estado).
2. `build_memory_db.py` corre bajo demanda o post-commit (hook OPCIONAL por maquina, jamas
   requisito del gate): recorre el arbol por tipos (s.2.1), computa sha256 del blob, extrae
   frontmatter allowlisted, upserta `artifacts`/`artifact_edges`/`agent_memory`/`search_terms`,
   registra `validation_runs(run_type='hot_fast')`.
3. Acople con DECISION-0026 (commit-then-memory): el paso de memoria del agente NO cambia (sigue
   escribiendo su markdown en `personal/<id>/`); el indexador lo recoge en la proxima pasada.
   La DB nunca es el lugar donde el agente "escribe memoria": es donde se INDEXA.

### 5.1b Contrato de mapeo frontmatter -> edge_type (provision F1; nota gobernada 2026-07-17)

Tabla v1 del contrato (cada arista F1 nace EXACTAMENTE de una de estas claves allowlisted de s.7;
invariante I9). `from` = el artefacto cuyo frontmatter contiene la clave, salvo normalizacion
declarada:

| Clave frontmatter (s.7) | edge_type | Nota |
|---|---|---|
| `relates_to` | `mentions` | referencia declarada generica |
| `linked_decisions` | `decision_for` | from=artefacto, to=decision |
| `supersedes` | `supersedes` | from=el que supersede |
| `superseded_by` | `supersedes` | NORMALIZADA: from=to declarado (el superseder), to=el declarante; dedup con la anterior por PK |
| `file` (en tasks del indice) | `implements` | from=task, to=artefacto entregable |

Edge_type RESERVADOS SIN productor en F1 (el enum del DDL los admite; el indexador F1 NO los
escribe): `contradicts`, `reviews`, `depends_on`, `handoff_for`, `mailbox_for`, `spec_for`.
Se activan en fases posteriores, cada uno con su clave/mecanismo productor declarado en su fase
(p.ej. `contradicts` = F4 con el patron epistemico diferido). Cambiar esta tabla = edicion
gobernada de esta SPEC, nunca decision del implementador.

### 5.2 Lectura / cold-start
1. El agente arranca leyendo el plano hot (s.2.1) - identico a hoy.
2. Historia bajo demanda: `query_memory_db.py "<pregunta>"` (FTS + edges + policy_status) devuelve
   ids + paths + resumenes; si el resumen no basta, rehidrata (s.5.4) y registra `retrieval_log`.
3. Sin DB (I5): `git grep` + manifests siguen funcionando; el agente pierde velocidad, no acceso.

### 5.3 Promocion hot->cold (Fase 2+, tras DECISION de activacion)
1. Seleccion: `build_memory_db.py --propose-cold` lista candidatos segun las reglas habilitadas
   del archivo canonico (dry-run SIEMPRE disponible). Excluye rutas bajo claim activo.
2. Ejecucion: tarea gobernada (task_id real) + claim con scope sobre las rutas origen y destino;
   `git mv` a `Area_comun/archive/cold-packs/CP-.../` + stub si aplica + fila en
   `pack.manifest.json` + actualizacion de `manifest-index.json`; commit con pathspec explicito.
3. **REGLA DE ORO anti-B1 (el hallazgo BLOCKER de la review): ningun `git mv` puede dejar
   colgando un puntero del indice fusionado.** `validate_collaboration_state` valida las tareas
   sobre TASK_INDEX + TASK_INDEX_ARCHIVE y FALLA si el `file` de una tarea no existe o si falta
   un deliverable de una tarea done (hoy: 276 tareas archivadas, 92 con deliverables). Por tanto:
   TODO artefacto referenciado por `file` o `deliverables` del indice fusionado tiene
   `requires_stub=1` OBLIGATORIO, y el stub se crea EN LA RUTA ORIGINAL EXACTA (mismo nombre),
   conservando en su frontmatter el `status` espejo y el puntero verificable (cold_path + sha256
   + rehydration_command) -- asi el puntero del indice sigue resolviendo a un archivo real y el
   gate canonico queda VERDE sin tocar el validador. La alternativa (validador archive-aware) es
   una tarea F3+ separada con su propia DECISION y review; NO precondicion del piloto.
4. Post: `check_memory_db_drift` verde + `validate_collaboration_state` verde EN CLON LIMPIO
   obligatorios antes del push (stub->sha, manifest->fila DB, punteros del indice resolviendo).

### 5.4 Rehidratacion (runbook AC15)
- Con DB: `query_memory_db.py --retrieve <artifact_id>` -> localiza cold_path + sha esperado,
  extrae `git show <freeze_commit>:<cold_path>` (o lee el working tree), verifica sha256, emite a
  stdout o a un tmp, registra `retrieval_log`.
- Sin DB (manual): abrir `manifest-index.json` -> pack -> `pack.manifest.json` -> cold_path + sha;
  `git show` + `sha256sum`. Documentado en el runbook de Fase 5.

### 5.5 Revive de agente / peon (employee-ready)
`revive_pack.py <agent_id>` compone, SOLO leyendo canon + DB: (a) memoria vigente del agente
(`agent_memory.is_current=1`, en orden), (b) sus tareas vivas + claims, (c) mailbox open dirigido
a el, (d) decisiones activas que le aplican (`policy_status.applies_to`), (e) `task_context_cache`
fresco de su tarea en vuelo si existe. Output = un markdown de arranque (token_estimate incluido).
Es la materializacion de "peones REVIVEN": un worker keyless nuevo recibe ese pack como prompt de
arranque sin releer el repo entero. El pack NO otorga autoridad (las capabilities siguen en el
config/registry; DECISION-0061 aplica igual a skills).

## 6. Importador canon->DB + round-trip (el gap que mato a Engram)

`build_memory_db.py --rebuild` reconstruye la DB COMPLETA desde cero con SOLO estas fuentes:
arbol git (HEAD o `--at <commit>`), `runtime/state/events.jsonl`, y los packs/manifests de
`Area_comun/archive/`. El test round-trip (AC5, obligatorio para llamar "reconstruible" a la DB):

```text
build A: indexado incremental normal -> dump canonico (dump_memory_db.py: filas ordenadas,
         sin autoincrement ni timestamps de corrida)
build B: --rebuild desde cero en DB nueva -> mismo dump canonico
PASS sii dump(A) == dump(B) byte a byte.
```

**Particion derivado-vs-operacional (hallazgo M1; el dump SOLO cubre lo derivado):**

- DERIVADO DEL CANON (entra al dump; reconstruible siempre): `artifacts` (campos de identidad/
  contenido; excluidos los operacionales de abajo), `artifact_edges`, `agent_memory`,
  `policy_status`, `stubs` (campos de identidad), `cold_packs` (campos de identidad, 1:1 del
  manifest), `search_terms`, `hot_cold_rules` (derivada del archivo canonico B2),
  `artifact_versions`, `artifact_content_index` (campos deterministas; excerpt ver abajo).
- OPERACIONAL (EXCLUIDO del dump; se DECLARA como estado que se pierde en un rebuild -- por eso
  la DB es cache y no canon): `retrieval_log`, `validation_runs`, `task_context_cache`,
  `pii_classification` (runs de clasificador), y las columnas `*.validated_at`,
  `artifacts.last_verified_at`, `artifacts.is_pii_safe`, `artifact_content_index.
  plain_text_excerpt` + `redaction_state`.
- Consecuencia honesta: tras `--rebuild`, los excerpts quedan NULL y `redaction_state=
  'unclassified'` hasta re-correr la clasificacion (determinista bajo `classifier_version`
  pineada); la perdida de logs operacionales es aceptada y declarada. "Reconstruible" (AC5)
  aplica a la particion DERIVADA -- que es la unica con valor de canon.

El dump canonico tambien sirve de `db_hash` para `validation_runs`.

## 7. PII y seguridad (REQ s.12 + s.26.2)

- Allowlist de claves de frontmatter indexables (v1): `task_id, decision_id, spec_id, message_id,
  title, status, type, owner, from, to, created_at, updated_at, closed_at, phase, priority,
  relates_to, linked_decisions, supersedes, superseded_by, file`. Cada clave con validacion por
  VALOR -- SIN excepciones (hallazgo M4a): ids por regex `^[A-Z]+-[0-9A-Za-z-]+$`; fechas ISO;
  status/type por enum; `owner/from/to` por enum contra el agent_registry del config + ids de
  participantes conocidos; `title` = ASCII imprimible + longitud <= 200 + pasa el scan PII basico
  (patrones email/telefono/id-fiscal) -- si no valida, la clave NO se indexa (warning registrado),
  jamas "se guarda igual".
- **Summaries (hallazgo M4b):** en F1-F3 TODA columna `summary*` (`artifacts.summary_short/long`,
  `agent_memory.summary`, `stubs.summary`, `task_context_cache.summary`) se deriva
  DETERMINISTICAMENTE de campos ya allowlisted (title + status + type + ids relacionados) --
  NUNCA del cuerpo, NUNCA por LLM (el LLM romperia el round-trip determinista de s.6). Summaries
  ricos desde el cuerpo = Fase 4, gateados por `pii_classification` y con `redaction_state`
  propio en `artifact_content_index` (el summary rico ES un excerpt y se rige por su misma
  puerta).
- **search_terms (hallazgo M4c):** en v1 `source` se restringe a metadata allowlisted (title
  validado, ids, type/status); terminos derivados de CONTENIDO solo entran en Fase 4 y solo de
  artefactos `public_plane_allowed=1`.
- Texto libre de cuerpos: entra SOLO a `plain_text_excerpt` (columna no-publicable-por-defecto
  con `redaction_state`); el plano publicable (excerpt/FTS de contenido/embeddings) exige
  `public_plane_allowed=1` de un run de clasificacion registrado.
- Secretos: el indexador EXCLUYE por patron de ruta `protocol-secrets/`, `*.key`, `*.pem`,
  `.env*`, `event-state.runtime.json` de cualquier maquina, y corre el mismo scan de secretos del
  repo antes de poblar excerpts. Test negativo obligatorio (s.10).
- Embeddings: tabla definida, creacion DIFERIDA a Fase 4 con politica PII propia (RFC del REQ
  s.24). Nada de embeddings de fuentes con `pii_state != 'clean'`.

## 8. Politica hot/cold inicial (responde REQ s.18)

- **Q1 umbral done->frio:** AMBOS criterios, gana el que MAS conserva: `window_days=45` O
  `window_count=20` ultimas done por tipo. Config en el archivo canonico versionado
  `Area_comun/protocol/MEMORY_HOT_COLD_RULES.json` (B2) del que la tabla se deriva; no hardcode.
- **Q2 motor:** SQLite + FTS5 desde el inicio (verificado disponible); `search_terms` existe
  igual como fallback estructural.
- **Q3 decisiones activas:** COMPLETAS en hot mientras `policy_state='active'`
  (`hot_required=1`); stub solo para superseded/historical. Razon: una decision activa es
  contrato vivo; el ahorro de tokens no justifica indireccion sobre reglas vigentes.
- **Q4 ubicacion frio:** misma rama, `Area_comun/archive/cold-packs/` (razonado en s.2.2).
- **Q5 sparse checkout:** opt-in por maquina, documentado; jamas precondicion de gates.
- **Q6 split protocolo/producto:** indexador+gates+stubs+revive = scripts NEUTRALES del protocolo
  (`scripts/memory/`); UI de busqueda/paneles = producto (panel Zeus); embeddings = opt-in de
  instancia. La capa neutral se exporta a instancias via new_instance (patron DECISION-0096).
  **Reconciliacion OBLIGATORIA con el memdb existente (hallazgo M6):** la instancia
  Zeus-protocol-Aegis YA tiene merged `scripts/memdb.py` + `test_memdb.py` (TASK-1203/1204/1208/
  1209) con las mismas 15 tablas pero DDL DIVERGENTE (artifacts sin summary_long/cold_reason/
  schema_version, git_commit NULLABLE, is_pii_safe NOT NULL DEFAULT 0 con semantica OPUESTA al
  NULL=sin-clasificar de esta SPEC, agent_memory de 6 columnas que ni cumple el REQ s.6, sin
  CHECKs). F1 NO es greenfield: es PORT/SUPERSEDE de ese memdb hacia UN master neutral en el hub
  (con diff DDL documentado y plan de migracion de la instancia); dos capas "neutrales"
  divergentes violan el propio Q6 y el REQ s.6 ("evitar migraciones estructurales obvias").

## 9. Gates y drift (REQ s.10-11)

- **Gate rapido hot** (`check_memory_db_drift --fast`): valida stubs hot (sha apunta a frio
  existente), manifests parseables, ninguna decision con `hot_required` sin presencia hot.
  No requiere rehidratar packs. Deriva sus checks de ARCHIVOS (decisiones + stubs + manifests +
  reglas canonicas), NUNCA de la DB (precondicion de I5); sin DB presente = verde. El "gate
  rapido" del REQ s.10 completo = `validate_collaboration_state` canonico (estado caliente,
  claims, mailbox) COMPUESTO con este `--fast` (hallazgo MIN3).
- **Gate completo** (`check_memory_db_drift --full`): rebuild round-trip (s.6) + sweep en AMBAS
  direcciones (MIN3): (a) por cada fila `artifacts`: fuente existe (hot o cold) y sha coincide;
  (b) por cada artefacto HOT del scan y cada artefacto de archive/: fila DB presente; (c) fila
  manifest por artefacto frio; (d) stub->sha correcto; (e) CERO filas publicables con
  `pii_state != 'clean'`; (f) regla habilitada en el archivo canonico por cada artefacto frio.
  Falla CERRADO en cualquiera de las condiciones del REQ s.11.
- Integracion con el gate canonico: Fase 0-2 = comandos APARTE (se corren en el checkpoint de
  higiene, junto a prune). Fase 3+ = se PROPONE anadir `--fast` al pipeline de validate como paso
  opt-in de instancia; ese cableado es su propia tarea con review (no se toca el validador antes).
- Concurrencia (REQ s.13; corregido por hallazgo M7, verificado contra runtime/eventlog.py):
  el indexador abre events.jsonl SOLO lectura sin lock (el reader torn-safe del runtime tolera
  colas a medio append). **El archivo `.ledger.lock` PERSISTE tras soltarse** (ledger_file_lock
  bloquea 1 byte via msvcrt/fcntl y no borra el archivo): presencia/antiguedad NO son senal de
  actividad. La deteccion correcta es un PROBE NO-BLOQUEANTE (msvcrt LK_NBLCK / flock LOCK_NB)
  con backoff; y submit_intent retiene el lock durante TODA su transaccion (validacion + append +
  materializacion + snapshot), asi que el indexador solo espera/reintenta, jamas compite.
  La promocion cold respeta claims activos (verificacion pre-git-mv contra CLAIMS.json).
- Exec-lease (REQ s.13 pide considerarlo; hallazgo MIN4): en F0-F2 el indexador es un proceso
  read-only bajo demanda con abort-on-lock -- el aparato exec-lease (TASK-0235) NO se necesita.
  Se RE-EVALUA si el indexador se vuelve daemon/hook concurrente permanente (F3+).

## 10. Test plan concreto (REQ s.16 -> comandos)

| Test | Comando/criterio |
|---|---|
| metadata extraction | unit: frontmatter allowlist + validacion por VALOR (casos validos/invalidos/inyectados) |
| hot/cold classify | unit: hot_cold_rules selector sobre fixture-tree |
| stubs golden | golden: stub generado byte-estable (LF) |
| manifest golden | golden: pack.manifest.json byte-estable, orden canonico |
| rebuild round-trip | s.6: dump(A)==dump(B) |
| drift DB vs files | mutar un sha -> --full exit!=0 |
| retrieve por id | rehidratar + sha verificado + retrieval_log +1 |
| decision activa stub | hot_required=1 sin hot -> --fast exit!=0 |
| NEG sha frio corrupto | tamper en pack -> --full exit!=0 |
| NEG path inexistente | fila artifacts a path borrado -> --full exit!=0 |
| NEG PII publicable | plantar email/NIT en excerpt-candidato sin clasificar -> excerpt NULL; forzar fila publicable -> --full exit!=0 |
| concurrencia claims | ruta bajo claim activo -> --propose-cold la excluye; mover con claim ajeno -> rechazo |
| rollback | rm index.db -> --rebuild -> round-trip verde |
| performance | baseline del HOT MAP REAL de s.2.1 antes/despues de F3 (ver nota AC10 en s.11) |
| I2 read-only | indexador sobre repo limpio -> git status --porcelain vacio + validate 0 |
| I6 identidad | indexar personal/X declarando agente Y -> rechazo |
| reglas canonicas | fila en hot_cold_rules sin respaldo en MEMORY_HOT_COLD_RULES.json -> --full exit!=0 |
| title PII | title con email/NIT -> clave no indexada + warning |

## 11. Trazabilidad AC1-AC15 (REQ s.15)

AC1->gate rapido (s.9, sin rehidratar). AC2->gate completo. AC3->s.5.3+5.4+test retrieve.
AC4->I7+Q3. AC5->s.6 round-trip (particion DERIVADA; lo operacional declarado como perdible).
AC6->I5. AC7->s.5.2 query (FTS+edges). AC8->retrieval_log.
AC9->s.7 (default-cerrado + tests NEG). **AC10 (corregido por hallazgo M3):**
`measure_context_cost.py` HOY solo mide los `coldstart_globs` del config pineado (AGENTS.md,
README, TASK_PROTOCOL, slims, mailbox/open) -- NINGUNA superficie que F3 enfria entra en esa
metrica, asi que su delta seria ~0 por construccion (evidencia vacua). El baseline AC10 se define
sobre el HOT MAP REAL de s.2.1: en F0 se computa con una herramienta desechable de area personal
(read-only, sin tocar core ni config); el modo oficial del medidor (extension del script) es
entregable de F1 (post-ventana, declarado). AC11->I2 (read-only, cero submit_intent).
AC12->s.9 concurrencia + test claims. AC13->SQLite local, cero red. AC14->paths relativos POSIX
en DB/manifests + LF forzado en artefactos generados (.gitattributes ya cubre Area_comun/**).
AC15->s.5.4 runbook manual.

Nota (hallazgo MIN5): el REQ s.5.3 pide indexar metricas "tokens, agente, peon, reviewer,
ciclos, resultado" pero su propio modelo s.6 no las tabula (inconsistencia interna del REQ).
Esta SPEC lo declara **ABIERTO-DIFERIDO**: el candidato natural es una VISTA sobre el schema de
medicion v1.0 del estudio (52 cols, ya instrumentado), no una tabla nueva aqui; se adjudica en
la DECISION de activacion.

## 12. Deteccion de contradicciones (Fase 4; REQ s.26.4-26.5)

`report_memory_conflicts.py`: (a) pares con edge `contradicts`; (b) memorias `is_current=1` del
mismo agente cuyo scope se solapa y cuyos summaries chocan (heuristica textual v1: negacion del
mismo term set; el juicio semantico fino queda para el humano); (c) memoria vigente que referencia
un artefacto `superseded`. Output = reporte, JAMAS merge automatico: resuelve un humano o una
DECISION dejando edge `supersedes` como rastro (arbitraje explicito).

## 13. Fases -> tareas (owner/checker sugeridos; ventana audit-first)

| Fase | Tarea(s) | Owner/Checker | DoD resumido | Ventana |
|---|---|---|---|---|
| F0 discovery | inventario por tipo/estado/tamano + baseline del HOT MAP s.2.1 (herramienta desechable en area personal, s.11-AC10) + borrador de MEMORY_HOT_COLD_RULES.json | Arquitecto / Analista read-only | inventario commiteado + baseline atestado | YA (read-only puro) |
| F1 DB read-only | PORT/SUPERSEDE del memdb.py de Zeus-protocol-Aegis (M6: diff DDL + plan de migracion) -> `scripts/memory/{build_memory_db,query_memory_db,dump_memory_db,check_memory_db_drift}.py` + `.gitignore` += runtime/memory/ + exclusion en scan_encoding (M5) + modo hot-map del medidor (M3) + tests s.10 (round-trip, I2, I6, PII NEG) + **contrato de mapeo s.5.1b implementado tal cual + declaracion cero-inferencias I9 con sus tests** | Codex / Analista | tests verdes en clon limpio; I1/I2/I3/I6/I9 pasan a ESTRUCTURAL; ninguna arista fuera de la tabla s.5.1b | post-ventana o instancia, GO operador |
| F2 stubs+manifests | formato stub/manifest + goldens + `--propose-cold` dry-run | Codex / Analista | goldens estables; dry-run correcto sobre fixture | idem |
| F3 frio real (piloto) | DECISION de activacion (REQ s.0.4, anexa MEMORY_HOT_COLD_RULES.json) + lote piloto tasks done antiguas CON stub-espejo obligatorio para todo lo referenciado por el indice (regla anti-B1 s.5.3) + rehidratacion + medicion AC10 | Arquitecto decide, Codex ejecuta / Analista | piloto archivado+rehidratado verde; `validate` canonico VERDE en clon limpio; AC10 medido | post-30-jul |
| F4 busqueda avanzada | FTS5 contenido public_ok + conflictos (s.12) + evaluacion embeddings (RFC PII) | Codex / Analista | FTS util; reporte conflictos corre | post-F3 |
| F5 operacion | runbook + archive periodico + export/import | Arquitecto / Analista | runbook probado por tercero | post-F3 |

Regla de arranque por fase: cada fase F1+ abre con GO explicito del operador (el REQ s.0.4 exige
ademas la DECISION formal para lo que cambia comportamiento: F3 la requiere si o si; F1-F2 son
read-only/aditivas y van con GO + tarea gobernada normal).

## 14. Riesgos especificos de esta SPEC (delta sobre REQ s.19)

1. **Doble fuente de "que es memoria" durante F0-F2** (markdown vivo + DB index): mitigado por I1
   (DB=cache) + s.12 (conflictos superficiados, no mergeados).
2. **Crecimiento del repo por archive/ misma-rama:** aceptado y declarado (s.2.2); el trigger de
   re-evaluacion (repo-size, no cold-start) queda ABIERTO-DIFERIDO con criterio: si `archive/`
   supera al hot en clone-time significativo, DECISION de repo satelite.
3. **FTS5 ausente en algun sqlite embebido:** fallback estructural search_terms (degradacion
   declarada).
4. **El indexador como proceso paralelo en arbol compartido:** solo lectura + probe no-bloqueante
   (s.9); jamas corre durante una promocion cold (misma tarea lo secuencia).
5. **Fork de esquema con el memdb ya merged en la instancia (M6):** mientras F1 no ejecute el
   port/supersede, existen DOS DDL divergentes; ninguna instancia nueva debe heredar el viejo
   (el export DECISION-0096 tomara el master del hub cuando exista).

## 15. Registro de la revision adversarial (2026-07-14, pre-commit)

Checker informal anti-rubber-stamp (subagent; checker formal apagado). Ataco SPEC-vs-REQ columna
por columna, etiquetas de la matriz s.26.6, DDL, reconstruibilidad, PII, concurrencia contra el
runtime REAL (eventlog.py/submit_intent.py/validate) y la ventana audit-first. Resultado:
**2 BLOCKER + 7 MAJOR + 5 MINOR, todos verificados como reales e INCORPORADOS en esta version:**

- B1 (F3 rompia el validador canonico: punteros file/deliverables del indice fusionado a rutas
  movidas) -> regla de oro anti-B1 en s.5.3 (stub-espejo obligatorio en la ruta original para
  todo lo referenciado) + DoD F3 con validate verde en clon limpio.
- B2 (reglas hot/cold solo en DB gitignored = no versionadas, rompia AC5/I4) -> fuente canonica
  `Area_comun/protocol/MEMORY_HOT_COLD_RULES.json`; la tabla es DERIVADA.
- M1 (dump del round-trip perdia estado en silencio) -> particion derivado-vs-operacional
  explicita en s.6 + manifests completados.
- M2 (I5 sobre-etiquetado ESTRUCTURAL) -> reetiquetado con precondicion explicita en s.4.
- M3 (AC10 vacuo: el medidor actual no cubre la superficie que F3 enfria) -> baseline sobre el
  hot map real (s.11) + modo oficial como entregable F1.
- M4 (PII: title/owner sin regla por valor; summaries libres sin redaction; search_terms sin
  gate) -> s.7 reescrita: validacion por VALOR sin excepciones, summaries deterministas de
  metadata en F1-F3, search_terms restringidas.
- M5 (afirmacion falsa de gitignore/precedente en el hub) -> corregida en s.2.3 + entregable F1.
- M6 (memdb.py YA merged en Zeus-protocol-Aegis con DDL divergente, no reconciliado) -> F1 =
  port/supersede con diff DDL (s.8 Q6, s.13, riesgo 5).
- M7 (deteccion de lock irrealizable: .ledger.lock persiste tras soltarse) -> probe no-bloqueante
  con backoff en s.9 (verificado contra ledger_file_lock del runtime).
- MIN1-MIN5 -> PRAGMA foreign_keys + cascadas explicitas + FKs omitidas declaradas (s.3);
  derivacion/unicidad de artifact_id + exclusiones de scan (s.3, colision TASK-0001 real);
  sweep bidireccional del --full + composicion del gate rapido (s.9); nota exec-lease (s.9);
  metricas del REQ s.5.3 declaradas ABIERTO-DIFERIDO (s.11).

Lo verificado SIN hallazgo por el checker (fidelidad de las 15 tablas columna-por-columna,
trazabilidad AC1-AC15 y tests s.16, FTS5 disponible, torn-safe read del events.jsonl, herencia
completa del fuera-de-alcance) queda como evidencia de cobertura, no como garantia.
