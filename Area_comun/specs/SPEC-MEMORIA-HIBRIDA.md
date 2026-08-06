---
spec_id: SPEC-MEMORIA-HIBRIDA
title: "Memoria hibrida: repo caliente + archivo frio verificable + DB derivada reconstruible (implementacion del REQ v0.3.0)"
status: draft-reviewed-informal
version: 0.3.0
date: 2026-08-06
author: Arquitecto
review: "adversarial informal (subagent anti-rubber-stamp) 2026-07-14: 2 BLOCKER + 7 MAJOR + 5 MINOR, TODOS reales e INCORPORADOS en esta version (registro en s.15); review FORMAL del Analista pendiente de reactivacion de su harness. v0.2.1 (2026-07-17): provision F1 del adversarial extracted-vs-inferred (veredicto Analista 476ceac, aceptado por Operador en GO Fase A): contrato de mapeo frontmatter->edge_type (s.5.1b) + invariante I9 F1-no-infiere (s.4) + DoD F1 (s.13); patron epistemico DIFERIDO-LIMPIO a F4. v0.3.0 (2026-08-06): s.16 contrato del F1-PORT al hub -- medicion del motor de la instancia contra el corpus REAL del hub (viabilidad demostrada) + 12 hallazgos de neutralidad/calibracion/escala con su accion requerida + 3 defectos de higiene del corpus (remediacion separada) + DoD del port"
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

## 16. F1-PORT AL HUB - contrato de neutralizacion y calibracion (2026-08-06)

### 16.1 Precondicion y alcance

DECISION-0100 s.2 agendo la promocion del motor probado (`scripts/memory/` de la instancia
Nova-Payroll) a master neutral del hub para "Fase 3+, POST-ventana-medida (post-30-jul)". La
ventana medida CERRO con el estudio pre-registrado H1-H3 ejecutado y cerrado el 2026-08-02
(TASK-0308 done). El operador dio GO explicito el 2026-08-06 con alcance **F1 SOLO** y ejecucion
por **Codex (maker) + Analista (checker)**, la cadena de s.13. Esta seccion es el contrato que el
maker implementa; no reabre metricas, DDL ni invariantes (s.3/s.4 mandan tal cual).

### 16.2 Evidencia de viabilidad (medida, no supuesta)

El Arquitecto clono el hub a scratch (`D:/Aegis_Scratch/protocol/memhib/hub`, DECISION-0104),
copio los 6 archivos del motor de la instancia (fuente: Nova-Payroll HEAD 0a33fed) y los corrio
contra el **corpus real del hub**. Resultado:

| Prueba | Resultado sobre el corpus del hub |
|---|---|
| build normal | 4150 artefactos, 197 eventos, 15 tablas, `schema_version` 1, `foreign_keys` 1, ~90 s |
| build `--rebuild` | mismos 4150 artefactos, ~128 s |
| round-trip AC5 (s.6) | **PASS byte a byte** (dump canonico de 7 346 333 bytes identico entre build A y build B) |
| `check_memory_db_drift --fast` | `result: pass`, `database_read: false` (I5 respetado: el gate rapido no abre la DB) |
| `check_memory_db_drift --full` | `result: pass`, `round_trip: pass`, `sweep: bidirectional-pass`, `database_written: false`, exit 0 |
| I2 read-only | tras correr el indexador, `git status --porcelain` no reporta NINGUN archivo trackeado modificado |
| query (FTS5-metadata) | recupera `SPEC-MEMORIA-HIBRIDA` y `DECISION-0100` con su grafo de aristas real (`decision_for`, `mentions`) |
| retrieve por id | emite el blob de `DECISION-0100` con verificacion sha + fila en `retrieval_log` |
| revive_pack | compone las 5 secciones + atestacion de fuentes, deterministico; **1 535 306 bytes** para el Arquitecto (ver P11) |
| suite de tests | 42 tests: 40 verdes, 1 FAIL y 1 ERROR, ambos por gaps REALES del hub (P10 y el entregable de `scan_encoding`) |

Lectura: el motor **funciona sobre nuestro corpus** y sus gates fallan cerrado donde deben. Lo que
falta es neutralidad de dominio y calibracion al vocabulario del hub, no arquitectura.

### 16.3 Hallazgos del port (P1-P12) y accion requerida

Clasificacion: **NEU** = neutralidad de dominio (frontera dura AGENTS.md s.4 / CLAUDE.md regla 1);
**CAL** = calibracion al corpus del hub; **ESC** = escala.

| Id | Clase | Hallazgo (evidencia medida) | Accion requerida en el master del hub |
|---|---|---|---|
| P1 | NEU | `PII_TITLE_PATTERNS[2]` = `\b(?:salario\|salary\|iban\|empleado\|employee\|nombre)\b` y la funcion `contains_payroll_pii()` meten lexico de NOMINA en el nucleo. Ademas `nombre` es palabra corriente en espanol: `contains_payroll_pii("nombre del agente")` -> True | El nucleo conserva SOLO patrones ESTRUCTURALES (email, patron IBAN-like, palabras clave de id fiscal, telefono). El lexico de dominio pasa a lista CONFIGURABLE por instancia (archivo fuera del config pineado, patron `COMMIT_TRAILERS.json`), **vacia por defecto**. Renombrar la funcion a nombre neutro (`contains_pii`) |
| P2 | NEU | `build_memory_db.py:881` escribe la columna `project` con el literal `"Nova-Payroll"` | Derivar `project` del `protocol.config.json` de la instancia; jamas literal |
| P3 | NEU | `DUMP_FORMAT = "nova-memory-derived-v1"` (el nombre del formato es parte del contrato de round-trip) | Nombre neutro del protocolo; documentar que cambiarlo invalida dumps previos |
| P4 | NEU | Docstrings citan "this Aegis instance" y "Zeus-protocol-Aegis/scripts/memdb.py" | Reescribir en terminos del protocolo; conservar el registro del supersede M6 como nota, sin marca de producto |
| P5 | CAL | El patron de telefono `(?:\+?\d[\d .()-]{7,}\d)` da FALSO POSITIVO sobre los ids con fecha-hora del protocolo: `contains_payroll_pii("MSG-20260619-092823-Codex-to-Arquitecto-...")` -> True | Excluir del patron de telefono los ids que casan `ID_RE`, o exigir separadores/longitud que no case una marca de tiempo `YYYYMMDD-HHMMSS` |
| P6 | CAL | `ID_RE = ^[A-Z]+-[0-9A-Za-z-]+$` no admite punto: rechaza 24 ids reales del hub (`...GO-front-etapa6.1-...`, `...TASK-0253-P4.1-baseline`, `...release-v0.10.0`) | Ampliar el juego de caracteres del id a `[0-9A-Za-z._-]` manteniendo el ancla de prefijo en mayusculas |
| P7 | CAL | `ASCII_TITLE_RE` rechaza titulos legitimos con tilde (`"...basados en evaluacion SOTA..."` con `o` acentuada) y titulos de mas de 200 caracteres: 49 rechazos | Aceptar UTF-8 imprimible en `title` (el gate de bytes del repo es `scan_encoding`, no el indexador) y elevar/declarar el tope de longitud. La validacion PII por VALOR se mantiene |
| P8 | CAL | `owner`/`from`/`to` se validan SOLO contra `agent_registry` = {Arquitecto, Codex, Analista}: 935 rechazos por participantes reales del hub (`Operador` 493, `Claude` 405 -- id historico del Arquitecto --, `Claude-analista` 24, `operador humano` 5) | Contrato explicito de identidades validas = `agent_registry` UNION `agents.human_owner` del config UNION alias historicos declarados en un archivo versionado fuera del config pineado. NUNCA texto libre (la validacion por VALOR de s.7 se conserva) |
| P9 | CAL | `TYPE_VALUES`/`STATUS_VALUES` no cubren el vocabulario real del hub: 982 rechazos de `type` (`HANDOFF` 429, `product` 72, `DECISION` 67, `requirement` 51, `DIRECTIVA` 35, `DIRECTIVE` 34) y 189 de `status` (`ready_for_review` 144, `final` 18, `delivered` 4, `submitted` 4, `cambio-requerido` 2) | Ampliar ambos enums al vocabulario efectivo del protocolo, documentando la fuente de cada valor. Los enums siguen siendo FINITOS (no texto libre) |
| P10 | CAL | La exclusion de plantillas solo cubre `*.template.*`; el hub usa ademas `*_TEMPLATE.md` -> colision dura `duplicate artifact_id SPEC-XXXX-short-name` entre `SPEC_TEMPLATE.md` y `ACCEPTANCE_CRITERIA_TEMPLATE.md`, que **aborta el build entero** | Anadir la convencion `*_TEMPLATE.*` a `is_excluded()`. Recomendado ademas: ignorar ids-placeholder (`XXXX`) como defensa en profundidad |
| P11 | ESC | `revive_pack.py` no tiene tope: inlinea el cuerpo integro de todo `personal/<id>/**` -> **1,5 MB** para el Arquitecto del hub (inutilizable como pack de arranque). No surgio en la instancia porque sus areas personales son pequenas | Acotar el pack: presupuesto declarado (bytes/tokens), seleccion por `is_current` + recencia, y resumen determinista (s.7: derivado de metadata, jamas del cuerpo por LLM) cuando el cuerpo no entra. Emitir `token_estimate` como pide s.5.5 y declarar en el pack lo que quedo fuera |
| P12 | CAL | `supersedes: []` (lista vacia declarada) se RECHAZA en vez de aceptarse como vacia: 116 rechazos | Aceptar la lista vacia como valor valido sin arista; el rechazo se reserva para valores malformados |

Regla del port: **ningun hallazgo se resuelve relajando una garantia**. P5-P9 y P12 amplian el
dominio de valores ACEPTADOS pero conservan la validacion por VALOR de s.7 (enums finitos, regex
ancladas, PII por valor); ninguno introduce texto libre en el indice.

### 16.4 Defectos del corpus del hub que el indexador caza (remediacion SEPARADA)

No son trabajo del port; se registran aqui porque bloquean o degradan el build y su correccion es
higiene gobernada del hub (DECISION-0018). El indexador falla CERRADO en H1: eso es correcto.

- **H1 (bloqueante):** 3 mensajes existen a la vez en `mailbox/answered/` y `mailbox/archived/`
  con blobs DIVERGENTES -> `duplicate artifact_id` aborta el build:
  `MSG-20260619-Arquitecto-to-Operador-carril-A-mirror-stall`,
  `MSG-20260628-Arquitecto-to-Analista-REPASS2-TASK-0208`,
  `MSG-20260706-Arquitecto-to-Codex-ACTION-TASK-1102-remediacion-nogo`.
- **H2 (degrada):** frontmatter malformado en el corpus historico: `task_id`/`spec_id` con valor
  `none` (82 + 16), `null`, RUTAS en vez de ids (`Area_comun/specs/SPEC-0038-...`), y listas por
  coma en un campo escalar (`TASK-0102,TASK-0103`). El rechazo del indexador es correcto.
- **H3 (menor):** 3 archivos del arbol contienen un byte NUL literal, entre ellos
  `personal/Arquitecto/MEMORY.md` -- lo que vuelve "binario" cualquier pack que los inlinee.

### 16.5 DoD del F1-PORT

1. `scripts/memory/{build_memory_db,query_memory_db,dump_memory_db,check_memory_db_drift,revive_pack,test_memory_db}.py`
   en el hub, con P1-P12 resueltos segun s.16.3.
2. `python scripts/scan_domain_neutrality.py --root .` exit 0 y `python scripts/scan_encoding.py --root .`
   exit 0 con los scripts nuevos dentro del arbol.
3. Suite de tests VERDE COMPLETA en clon limpio, incluidos los 2 casos que hoy fallan
   (`test_scan_encoding_excludes_runtime_memory`, `test_current_tree_build_does_not_change_tracked_status`),
   mas tests NUEVOS que cubran cada hallazgo P1-P12 (uno por hallazgo, incluido un negativo que
   demuestre que el lexico de dominio ya no vive en el nucleo).
4. `.gitignore` += `runtime/memory/`; `scripts/scan_encoding.py` (y su `.ps1`) excluyen esa ruta.
5. Sobre el corpus del hub en clon limpio: build sin error duro; round-trip AC5 byte a byte;
   `--fast` y `--full` verdes por EXIT CODE. Los warnings restantes deben ser SOLO H2 (frontmatter
   realmente malformado), no metadata bien formada del hub.
6. I2 verificado: `git status --porcelain` vacio tras correr el indexador sobre un arbol limpio.
7. `revive_pack` acotado (P11) con presupuesto declarado y `token_estimate` en el pack.
8. Export a instancias (DECISION-0096, born-operational): `scripts/new_instance.py` publica
   `scripts/memory/` en la instancia nueva, con test que lo demuestre.
9. NO se modifican `validate_collaboration_state.*` ni `submit_intent.py` (s.1 fuera de alcance de
   F1); los comandos nuevos se corren APARTE, en el checkpoint de higiene.

### 16.7 Ledger de residuales del port (C1 del veredicto r2 de TASK-0316; 2026-08-06)

Registro trazable de lo que el port dejo abierto o movio despues de cerrar. Existe para que quien
recompute TASK-0314 manana no lea una regresion silenciosa sin poder explicarla.

**Delta declarado sobre el AC5 de TASK-0314: warnings del build 219 -> 227.**
- Causa: TASK-0316 AC4 saco del enum `STATUS_VALUES` los dos valores de vocabulario de instancia
  (`DRAFT-PENDIENTE-DE-FIRMA-DEL-OPERADOR`, `draft (pendiente GO operador)`) por ser fuga de dominio
  hacia el nucleo neutral. 8 artefactos TRACKEADOS los usan y pasan a emitir warning.
- Medicion A/B del checker sobre el mismo commit: delta **+8**; **0** sobre corpus gobernado (los 8
  son borradores de `personal/Arquitecto/`); **1** solo archivo estaba antes limpio (7 de los 8 ya
  warneaban por otras claves ad-hoc del mismo frontmatter); **0** warnings eliminados.
- Efecto semantico: perdida del campo `status` en el indice para esos 8 borradores.
- **No bloqueo el cierre de 0316** por decision del checker, con tres razones: (a) ningun gate por
  exit code regresa -- build, round-trip y drift `--fast`/`--full` verdes en clon pristino, y CI no
  ejecuta la base de memoria en ningun paso; (b) la clausula del AC5 protege *metadata bien formada
  del hub*, y estos son borradores personales con vocabulario que no esta en el ciclo de vida de
  AGENTS.md s.6 -- leerla de otro modo la convierte en un veto a purgar el enum, lo contrario de su
  proposito; (c) conservar los dos valores para proteger un conteo seria comprar una metrica
  cosmetica apagando un defecto real, la misma inversion que el checker reporto en r1 de 0316.
- **Cierre esperado:** TASK-0318 debe devolver el conteo a 219 **sin** reintroducir vocabulario de
  instancia en el nucleo, y dejarlo escrito.

**Hecho estructural declarado: el enum queda MEDIO purgado.** Salieron 2 valores y quedan 6 del
mismo vocabulario de instancia (`GO-PROMOVER-OFF`, `OK-CERRABLE`, `OK_CERRABLE`, `cambio-requerido`,
`hallazgo-confirmado`, `draft-reviewed-informal`), que sobreviven solo porque no son nombres de
agente y la regla de identidad no los ve. El nucleo neutral no queda neutral: queda **arbitrario**.
Se adjudica a TASK-0318 con el alcance de los 6, no de los 2.

**Residuales abiertos del motor** (de los veredictos r1/r2 de TASK-0314 y r1/r2 de TASK-0316):
R1 patron de telefono demasiado ancho por el lado de la exencion (valores con forma de id lo saltan;
opcion autorizada por P5) -- R2 IBAN solo en forma contigua -- R3 el barrido de plano publico del
`--full` no recibe los terminos de dominio de la instancia -- R5-0314 falso positivo de timestamps con
offset negativo (**adjudicado a TASK-0317**) -- R6 suelo no degradable del revive pack al 37-47 pct del
techo -- R5-0316 la allowlist de archivo completo sobre `peer_mailbox_cron.ps1` ciega el defecto de
identidad que se acaba de corregir en el.

**Regla vigente:** el motor NO se declara listo para exportar a instancias mientras TASK-0317 y
TASK-0320 sigan abiertas (TASK-0318 cerro el vocabulario de `status`; TASK-0320 cierra el de `type`).

**Anadido 2026-08-06 tras el veredicto OK-CERRABLE de TASK-0318 (encargos C1 y C3 del checker):**

- **Linea base del vocabulario declarado (C3), para que una deriva futura sea visible:**
  `extra_status_values` = **8 declarados / 8 en uso / 0 muertos**. Si un recuento futuro encuentra
  declarados que ya nadie usa, eso es vocabulario muerto acumulandose en la politica de la instancia
  y toca purgarlo; el mecanismo no lo detecta solo.
- **Propiedad verificada que conviene no perder (medida por el checker sobre el corpus real):** la
  declaracion **solo surte efecto ATESTADA**. Editar `MEMORY_INDEX_POLICY.json` sin commitear no
  concede nada -- el indexador lee el blob de git, asi que el conteo se queda en 219. Quitar las 8
  declaraciones y commitear lo lleva a 234, con exactamente 15 warnings de `status`, los 15
  artefactos que las usan. Es lo que hace del mecanismo una validacion y no documentacion.
- **R2 heredado, declarado (C2):** la politica admite latitud no-ASCII en sus valores, igual que
  `domain_pii_terms` e `identity_aliases`, porque esa ruta queda fuera del alcance de
  `scan_encoding`. No lo introdujo TASK-0318; se registra para que no se descubra como sorpresa.
- **R1 adjudicado a TASK-0320:** el enum hermano `TYPE_VALUES` conserva 10 fichas de ceremonia de
  instancia (6 en castellano), el mismo defecto que `status` acaba de cerrar y con el mecanismo
  curativo ya probado.

### 16.6 Fuera de alcance del port

F2 (stubs/manifests, `--propose-cold`), F3 (enfriado real: exige DECISION de activacion +
`MEMORY_HOT_COLD_RULES.json` + regla anti-B1 de s.5.3), F4 (FTS de contenido, embeddings,
contradicciones) y la remediacion H1-H3 de s.16.4. El fondo intocable del hub (config `2E35F26E`,
epoch `1.14.0`, dataset N=500) no se toca: el indexador es read-only y no escribe el ledger.
