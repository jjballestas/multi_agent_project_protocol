# Codex Memory

Last updated: 2026-06-23 Europe/Madrid, after TASK-0160 intake extraction acceptanceIntent/PII label delivery.

## Latest Session Note

- TASK-0160 product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `a3c5f26 fix(intake): allow empty extraction acceptance intent`. File extraction upload no longer requires
  `acceptanceIntent` in `sanitizeFileExtractionUpload`, while candidate approval still rejects an empty
  `acceptanceIntent` through the governed intake path. The PII acknowledgement label is associated with its
  checkbox, rewritten in plain language, and aligned for clean wrapping. Evidence: `node --check src/server.js
  public/app.js tests/staticContract.test.js`, product `git diff --check`, product `npm test` PASS 52/52,
  clean-clone Zeus `npm test` PASS 52/52, and local smoke on port 4192 for `/healthz` plus
  `/api/protocol/observe`. Protocol evidence before delivery artifacts: encoding OK, neutrality OK,
  `validate_collaboration_state.py` OK, drift false up_to_seq 1318; after acquiring the delivery claim,
  drift false up_to_seq 1319. The current validator has no `--with-secrets` flag. No live canonical pilot was
  run.
- TASK-0159 product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `bc8346d fix(intake): surface file extraction candidates`. File-mode Intake now hides the direct
  `EXECUTE SUBMIT_INTENT` button, places `Proyecto destino` first inside the file section, shows a processing
  state while extraction runs, renders extraction/write/0-candidate errors in red, and derives the ingestion note
  and file accept list from the loaded config instead of hardcoded `.md/.txt`. The server now honors
  `file-ingestion.runtime.json` local-vlm endpoint/model fields at the extractor top level and records
  `completed-empty` with an explicit no-candidates reason. Evidence so far: `node --check public/app.js
  src/server.js tests/staticContract.test.js`, product `git diff --check`, product `npm test` PASS 52/52, and
  local smoke on port 4190 confirmed the live server reads gitignored `file-ingestion.runtime.json` with
  extractor enabled/local-vlm/loopback and real allowed extensions.
  Protocol delivery commit `28effe9 coord(TASK-0159): deliver intake UX fixes` moved TASK-0159 to
  `in_review`, released `CLAIM-20260623-Codex-TASK-0159`, wrote
  `Area_comun/handoffs/HANDOFF-TASK-0159-codex-to-arquitecto-1.md`, and opened
  `Area_comun/mailbox/open/MSG-20260623-Codex-to-Arquitecto-TASK-0159-in-review.md`. Final protocol evidence
  before the delivery commit: encoding OK, neutrality OK, `validate_collaboration_state.py` OK, drift false
  up_to_seq 1304. The original GO remains open because `mailbox_archive` requires `orchestrator`.
- TASK-0158 CAMBIO3 neutrality fix landed in `D:/Agentes/multi_agent_project_protocol`:
  `91f7a0b fix(connectors): remove SQL Server s9 instance env default`. The live s9 verifier no longer hardcodes an
  instance-specific env file path under `connectors/`; it accepts `--env` or `SQLSERVER_S9_ENV_FILE` and fails closed
  with a clear error if neither is provided. The refreshed sanitized artifact records live SELECT row_count=1, DML
  `DELETE ordinary_user_table_zero_rows` rejected with 229, and DDL `CREATE TABLE` rejected with 262, both
  `permission_denied_on_principal`. Evidence before delivery commit: connectors token grep for
  `nova|budget|treasury|paycontrol|accounting` no matches, py_compile OK, golden
  `connector_sqlserver_readonly_cases` PASS, live s9 PASS via gitignored operator env, encoding OK, neutrality OK,
  `validate_collaboration_state.py` OK, drift false up_to_seq 1278, and no active claims. Delivery wrote
  `Area_comun/handoffs/HANDOFF-TASK-0158-codex-to-arquitecto-4.md`, opened
  `Area_comun/mailbox/open/MSG-20260623-Codex-to-Arquitecto-TASK-0158-fix3-in-review.md`, moved TASK-0158 back to
  `in_review`, and released the fix3 Codex claims. No live-use flip was made; `connectors.config.json` remains
  `enabled:false`.
- TASK-0158 CAMBIO2 rework implementation commit landed in `D:/Agentes/multi_agent_project_protocol`:
  `a4b4b3d fix(connectors): discover SQL Server s9 DML table`. The live s9 verifier now discovers a readable
  ordinary base table at runtime via `INFORMATION_SCHEMA.TABLES`, validates `SELECT TOP 0`, executes the DML
  negative vector against that real table, and persists only the generic operation label
  `DELETE ordinary_user_table_zero_rows`. `208` remains an invalid/other server rejection and does not satisfy the
  s9; DML must prove error `229`, and DDL must prove error `262`, both classified as
  `permission_denied_on_principal`. The refreshed sanitized artifact
  `Area_comun/artifacts/S9-TASK-0158-sqlserver-readonly-live.json` records the real reproducible 229/262 evidence
  without credentials or real schema/table names. Evidence before delivery: py_compile for connector/verifier/golden
  OK, `python examples/connector_sqlserver_readonly_cases/run_connector_sqlserver_readonly_cases.py` PASS, live s9
  PASS using a temporary gitignored `connectors.runtime.json`, encoding OK, neutrality OK,
  `validate_collaboration_state.py` OK, and drift false up_to_seq 1267. Delivery commit
  `coord(TASK-0158): deliver SQL Server s9 rework v2` moved TASK-0158 to `in_review`, released
  `CLAIM-20260623-Codex-TASK-0158-fix2-s9`, wrote
  `Area_comun/handoffs/HANDOFF-TASK-0158-codex-to-arquitecto-3.md`, and opened
  `Area_comun/mailbox/open/MSG-20260623-Codex-to-Arquitecto-TASK-0158-fix2-in-review.md`. No live-use flip was made;
  `connectors.config.json` remains `enabled:false`.
- TASK-0158 changes_requested rework implementation commit landed in `D:/Agentes/multi_agent_project_protocol`:
  `31e0f23 fix(connectors): prove SQL Server DML permission denial`. The live s9 verifier no longer uses system
  catalog DML as its default negative vector; it records each write vector with `type`, `operation`,
  `error_code`, `error_class`, and `rejection_kind`, and hard-fails unless both DML and DDL prove
  `permission_denied_on_principal`. The refreshed sanitized artifact
  `Area_comun/artifacts/S9-TASK-0158-sqlserver-readonly-live.json` now records DML `DELETE ordinary_table_zero_rows`
  rejected server-side with error `229` and DDL `CREATE TABLE` rejected with error `262`, both classified as
  principal permission denial; no credentials or sensitive table names are in the artifact. Evidence before this
  memory update: live s9 PASS using a one-shot process env override for the real ordinary table DML, `python -m
  py_compile` for connector/verifier/golden OK, `python examples/connector_sqlserver_readonly_cases/run_connector_sqlserver_readonly_cases.py`
  PASS, encoding OK, neutrality OK, `validate_collaboration_state.py` OK, and drift false up_to_seq 1260. Delivery
  commit `coord(TASK-0158): deliver SQL Server s9 rework` wrote
  `Area_comun/handoffs/HANDOFF-TASK-0158-codex-to-arquitecto-2.md`, opened
  `Area_comun/mailbox/open/MSG-20260623-Codex-to-Arquitecto-TASK-0158-fix-in-review.md`, moved TASK-0158 back to
  `in_review`, and released `CLAIM-20260623-Codex-TASK-0158-fix-s9`. Final protocol evidence before this memory
  amendment: encoding OK, neutrality OK, `validate_collaboration_state.py` OK, drift false up_to_seq 1262, and
  golden `connector_sqlserver_readonly_cases` PASS.
- TASK-0158 protocol implementation commit landed in `D:/Agentes/multi_agent_project_protocol`:
  `e61f0ae feat(connectors): add SQL Server live readonly backend`. The SQL Server connector now has a
  real `pymssql` live backend loaded from gitignored `SQLSERVER_*` env values, keeps
  `classify_readonly_sql` in front of normal reads, resolves `connectors.runtime.json` before the versioned
  off-by-default config, and ships a non-CI s9 verifier. `connectors/connectors.config.json` includes
  `sqlserver_readonly` with `enabled:false`; `.gitignore` excludes `connectors/*.runtime.json`. The live s9
  verifier installed `pymssql` with `python -m pip install pymssql`, used a temporary runtime override for
  the run, then removed it. Sanitized artifact:
  `Area_comun/artifacts/S9-TASK-0158-sqlserver-readonly-live.json` records SELECT row_count=1 and server-side
  rejection of DML/DDL vectors with `OperationalError` codes 259/262, without credentials or schema/table
  names. Evidence before this memory update: `python -m py_compile` for connector/verifier/golden OK,
  `python examples/connector_sqlserver_readonly_cases/run_connector_sqlserver_readonly_cases.py` PASS,
  encoding OK, neutrality OK, `validate_collaboration_state.py` OK, drift false up_to_seq 1249. The validator
  still does not support `--with-secrets`. Delivery commit `coord(TASK-0158): deliver SQL Server connector s9`
  moved TASK-0158 to `in_review`, released the Codex claim, opened
  `Area_comun/mailbox/open/MSG-20260623-Codex-to-Arquitecto-TASK-0158-in-review.md`, and wrote
  `Area_comun/handoffs/HANDOFF-TASK-0158-codex-to-arquitecto-1.md`. Final protocol evidence before this
  memory follow-up: encoding OK, neutrality OK, `validate_collaboration_state.py` OK, drift false up_to_seq
  1255, and golden `connector_sqlserver_readonly_cases` PASS. Codex could not archive the original GO because
  `mailbox_archive` requires `orchestrator`; the original GO remains open with `requires_response:false`.
- TASK-0157 product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `2afc944 feat(intake): streamline file extraction flow`. File-mode Intake now opens a dedicated section with
  the file selector and `Extraer requisito` action before typed fields, runs the existing governed extraction
  path, renders candidates as selectable cards, and lets a card populate title/narrative/acceptance while
  preserving PII review and submit_intent approval. The server now resolves gitignored runtime overrides
  (`commit-push.runtime.json`, `file-ingestion.runtime.json`) before versioned off-by-default configs when no
  test/operator env path is injected. Evidence after commit: `node --check public/app.js src/server.js
  tests/staticContract.test.js`, product `npm test` PASS 50/50, clean-clone Zeus `npm test` PASS 50/50.
  During startup Codex corrected an initial invalid claim row selector via runtime events; drift stayed false
  after the correction. Protocol delivery commit `d41e75b coord(TASK-0157): deliver intake v3 flow` moved
  TASK-0157 to `in_review`, moved `TASK-EXTRACT-DC0E283672` to `done`, released the Codex claim, opened
  `Area_comun/mailbox/open/MSG-20260623-Codex-to-Arquitecto-TASK-0157-in-review.md`, and wrote
  `Area_comun/handoffs/HANDOFF-TASK-0157-codex-to-arquitecto-1.md`. Final protocol evidence before memory
  follow-up: encoding OK, neutrality OK, drift false up_to_seq 1233, `validate_collaboration_state.py` OK;
  `--with-secrets` is still not a supported validator flag.
- TASK-0156 product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `560a226 feat(intake): sign extractor candidates`. The product now has `extractors.config.json` as a
  product-level worker registry for `Extractor` (role `extraccion`, default model `qwen3-vl:4b-instruct`,
  default loopback endpoint `http://127.0.0.1:11434/api/chat`, public Ed25519 key) outside `protocol.config.json`.
  The matching private key was generated at `D:/Agentes/Zeus/Zeus-protocol/.secrets/extractor_ed25519_private.pem`
  and remains gitignored; rotate/regenerate with `node -e`/Ed25519 and update only the public key in the registry.
  Extracted candidates now carry `extractor_worker_id` plus an Ed25519 signature over canonical candidate
  provenance/content, and candidate approval rejects absent or forged signatures before governed intake. Local-vlm
  now defaults to the registry model when no per-runtime model is configured. Evidence before memory update:
  `node --check src/server.js tests/staticContract.test.js`, product `git diff --check`, product `npm test` PASS
  48/48, local smoke on port 4184 OK for `/healthz` + `/api/protocol/observe`, and clean-clone Zeus `npm test`
  PASS 48/48. Protocol delivery moved TASK-0156 to `in_review`, released all Codex TASK-0156 claims, opened
  `Area_comun/mailbox/open/MSG-20260622-Codex-to-Arquitecto-TASK-0156-in-review.md`, and wrote
  `Area_comun/handoffs/HANDOFF-TASK-0156-codex-to-arquitecto-1.md`. Final protocol evidence: encoding OK,
  neutrality OK, drift false up_to_seq 1213, and `validate_collaboration_state.py` OK with one unrelated warning
  for `MSG-20260622-Arquitecto-to-Operador-ESTADO-cola-vacia.md`.
- TASK-0155 AC52 rework product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `6369b5c fix(intake): enforce strict loopback host syntax`. The local-vlm endpoint guard now validates the raw
  URL host before WHATWG URL canonicalization and accepts only `localhost`, dotted-decimal IPv4 in `127.0.0.0/8`
  without ambiguous octal/hex/integer notation, and `::1`/`[::1]`; decimal `2130706433`, octal, hex,
  `0.0.0.0`, external IPs, hostnames, suffix tricks, IPv4-mapped IPv6, and leading-zero ambiguous IPv4 are
  rejected before any extractor call. Product evidence before this memory update: `node --check src/server.js
  tests/staticContract.test.js public/app.js`, product `git diff --check`, and product `npm test` PASS 48/48.
  Protocol delivery commit `coord(TASK-0155): deliver AC52 loopback rework` moved TASK-0155 back to
  `in_review`, released Codex claims, opened
  `Area_comun/mailbox/open/MSG-20260622-Codex-to-Arquitecto-TASK-0155-AC52-in-review.md`, and wrote
  `Area_comun/handoffs/HANDOFF-TASK-0155-AC52-codex-to-arquitecto-2.md`. Final evidence: clean-clone Zeus
  `npm test` PASS 48/48; protocol encoding OK, neutrality OK, drift false up_to_seq 1197, and
  `validate_collaboration_state.py` OK with one unrelated warning for
  `MSG-20260622-Arquitecto-to-Operador-ESTADO-cola-vacia.md`. Codex could not archive the original AC52
  directive because `mailbox_archive` requires `orchestrator`; the original message remains open with
  `requires_response:false`.
- TASK-0155 product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `79be511 feat(intake): add local vlm extractor provider`. The extractor keeps `deterministic-local` as the
  default and adds off-by-default `local-vlm` with loopback-only endpoint validation, bounded per-chunk/per-image
  calls, robust JSON extraction from noisy model responses, candidate dedupe, and no-ledger candidate storage
  behind the existing human PII review gate. Evidence before this memory update: `node --check src/server.js
  tests/staticContract.test.js public/app.js`, product `git diff --check`, product `npm test` PASS 48/48, and
  clean-clone Zeus `npm test` PASS 48/48. Protocol delivery moved TASK-0155 to `in_review`, released Codex
  claims, and opened `Area_comun/mailbox/open/MSG-20260622-Codex-to-Arquitecto-TASK-0155-in-review.md` with
  handoff `Area_comun/handoffs/HANDOFF-TASK-0155-codex-to-arquitecto-1.md`. Codex could not archive the
  original GO through `mailbox_archive` because that intent requires `orchestrator`; the GO remains open with
  `requires_response:false`.
- TASK-0154 product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `da5825d test(intake): lock UX regression behavior`. The suite now has permanent behavior coverage for
  AC48/AC49/AC50: the Intake "Nueva historia/requisito" button must keep the `governed-button` design-system
  class and CSS token surface, compose/new-story behavior preserves typed drafts while reset remains tied to
  successful `status.variant === "ok"`, and a live server fixture proves `/api/protocol/snapshot` reflects a new
  canonical HEAD across two requests without restart. Evidence before memory update: `node --check
  tests/staticContract.test.js public/app.js src/server.js`, product `git diff --check`, product `npm test` PASS
  47/47, and clean-clone Zeus `npm test` PASS 47/47. Protocol delivery commit
  `7088be4 coord(TASK-0154): deliver UX behavior tests` moved TASK-0154 to `in_review`, released Codex claims,
  answered the GO, and opened `Area_comun/mailbox/open/MSG-20260622-Codex-to-Arquitecto-TASK-0154-in-review.md`
  with handoff `Area_comun/handoffs/HANDOFF-TASK-0154-codex-to-arquitecto-1.md`. Protocol evidence before commit:
  encoding OK, neutrality OK, drift false up_to_seq 1176, `validate_collaboration_state.py` OK; the requested
  `--with-secrets` validator flag is not supported by the current script.
- TASK-0153 exec/execSync import rework product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `8751051 test(intake): flag child process exec imports`. The guard now flags named imports/destructured
  requires of `exec` or `execSync` from `node:child_process` / `child_process` with reason `cli-exec-import`,
  without matching bare `exec(` so legitimate `RegExp.exec(...)` remains clean. Positive controls cover named
  ESM imports, aliases, destructured CommonJS requires, allowed `execFile`/`spawn`, and real `src/**` as clean.
  Evidence after commit: `node --check tests/staticContract.test.js`, product `git diff --check`, product
  `npm test` PASS 44/44, and clean-clone Zeus `npm test` PASS 44/44. Protocol delivery moves TASK-0153 back to
  `in_review`, answers `MSG-20260622-Arquitecto-to-Codex-CAMBIO-TASK-0153-exec-import`, releases Codex claims,
  and opens `Area_comun/mailbox/open/MSG-20260622-Codex-to-Arquitecto-TASK-0153-exec-import-in-review.md` with
  handoff `Area_comun/handoffs/HANDOFF-TASK-0153-exec-import-codex-to-arquitecto-3.md`.
- TASK-0153 external-cli rework product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `5cb8910 test(intake): allowlist spawned egress commands`. The `external-cli` guard now uses an explicit
  allowlist for spawned binaries (`git`, `python`) across `execFile`, `execFileAsync`, `execFileSync`, `spawn`
  and `spawnSync`, flagging shell/network binaries such as `powershell`, `sh`, `bash`, `cmd`, `curl` and `wget`.
  Positive controls cover the blocked binaries and call families, while allowed `git`/`python` calls and real
  `src/**` stay clean. Evidence after commit: `node --check tests/staticContract.test.js`, product
  `git diff --check`, product `npm test` PASS 44/44, and clean-clone Zeus `npm test` PASS 44/44. Protocol
  delivery moves TASK-0153 back to `in_review`, answers
  `MSG-20260622-Arquitecto-to-Codex-CAMBIO-TASK-0153-external-cli`, releases Codex claims, and opens
  `Area_comun/mailbox/open/MSG-20260622-Codex-to-Arquitecto-TASK-0153-external-cli-in-review.md` with handoff
  `Area_comun/handoffs/HANDOFF-TASK-0153-external-cli-codex-to-arquitecto-2.md`.
- TASK-0153 product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `ac2e308 test(intake): enforce egress allowlist isolation`. The `src/**` egress guard flipped to an
  explicit import/require allowlist with deny-by-default behavior, keeps governed `git push` wrapper usage
  allowed, flags unlisted HTTP/model clients such as `phin`/`axios`/`openai`, and now marks `eval(` plus
  `new Function(`. The test harness creates its own OFF runtime config fixtures and `startServer` injects them
  by default, so operator shell env values for `AUTO_COMMIT_PUSH_CONFIG_PATH` or `FILE_INGESTION_CONFIG_PATH`
  cannot turn tests live unless a test explicitly overrides them. Local product evidence after commit:
  `node --check tests/staticContract.test.js`, `git diff --check`, product `npm test` PASS 44/44, and clean-clone
  Zeus `npm test` PASS 44/44. Protocol delivery moves TASK-0153 to `in_review`, answers the GO, releases Codex
  claims, and opens `Area_comun/mailbox/open/MSG-20260622-Codex-to-Arquitecto-TASK-0153-in-review.md` with
  handoff `Area_comun/handoffs/HANDOFF-TASK-0153-codex-to-arquitecto-1.md`.
- TASK-0152 AC45 guard rework product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `3d94f11 test(intake): harden egress guard patterns`. `sourceEgressViolations` now marks dynamic
  `import(`, dynamic/static/require model SDKs, bare network imports, network call sites
  `.connect/.request/.get/.createConnection`, and common HTTP clients (`undici`, `axios`, `got`,
  `node-fetch`, `superagent`, `request`). Positive controls cover each new pattern, including the falsable
  `await import("openai")` case requested by Arquitecto. Evidence before delivery: `node --check
  tests/staticContract.test.js`, product `npm test` PASS 43/43, and clean-clone Zeus `npm test` PASS 43/43.
  Protocol delivery moved TASK-0152 back through `in_progress` to `in_review`, released the AC45 guard claim,
  answered `MSG-20260622-Arquitecto-to-Codex-CAMBIO-TASK-0152-guard-AC45`, opened
  `Area_comun/mailbox/open/MSG-20260622-Codex-to-Arquitecto-TASK-0152-AC45-guard-in-review.md`, and wrote
  handoff `Area_comun/handoffs/HANDOFF-TASK-0152-AC45-guard-codex-to-arquitecto-2.md`.
- TASK-0152 product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `63a80ee feat(intake): add extractor loop and raw purge`. File intake v2 Phase C now has a gated/off-by-default
  extraction loop endpoint (`/api/protocol/intake-extractions/run`) with explicit `FILE_EXTRACTION_AGENT` consent,
  deterministic-local provider, labelled agent egress boundary and no network egress; AC45 expands the static
  egress guard to all `src/**`, adds raw upload TTL sweeping, and purges raw uploads when a candidate reaches
  terminal status. Evidence before delivery: `node --check src/server.js public/app.js tests/staticContract.test.js`,
  product `npm test` PASS 43/43, clean-clone Zeus `npm test` PASS 43/43, and healthz/actions smoke OK. Protocol
  delivery moved TASK-0152 to `in_review`, released `CLAIM-20260622-Codex-TASK-0152`, answered the GO, and opened
  `Area_comun/mailbox/open/MSG-20260622-Codex-to-Arquitecto-TASK-0152-in-review.md` with handoff
  `Area_comun/handoffs/HANDOFF-TASK-0152-codex-to-arquitecto-1.md`.
- Codex cron executor prompt was hardened per
  `MSG-20260622-Arquitecto-to-Codex-CONFIG-CRON-EJECUTOR`: `personal/Codex/codex_mailbox_cron.ps1` now treats
  DECISION messages to Codex as processable and reinjects an executor prompt that must claim ready Codex GO tasks,
  move them to `in_progress`, implement in `D:/Agentes/Zeus/Zeus-protocol`, run product/protocol gates, deliver
  `in_review`, release the claim via `runtime/submit_intent.py`, and avoid self-closing to `done`. The CONFIG
  message was moved to answered and `CLAIM-20260622-Codex-cron-executor-config` was released. No live cron was
  started by this change.
- TASK-0151 product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `0a5e737 feat(intake): add candidate review gate`. File intake v2 Phase B now keeps candidates in an OS temp
  store outside the attested dataset, exposes a review panel for pending candidates, blocks approval without
  per-candidate human PII acknowledgement, rejects active edited content, re-screens/redacts candidate text through
  governed `requirement-intake`, derives requirement ids from edited content, preserves PII-free provenance
  (`source_file_sha256`, `extraction_task_id`, `candidate_pre_edit_hash`), and keeps discard/approval lifecycle
  outside `task_status`. Evidence before commit: `node --check src/server.js public/app.js
  tests/staticContract.test.js`, product `npm test` PASS 43/43, and clean-clone Zeus `npm test` PASS 43/43.
  Protocol delivery commit moved TASK-0151 to `in_review`, released
  `CLAIM-20260622-Codex-TASK-0151`, answered the GO, and opened
  `Area_comun/mailbox/open/MSG-20260622-Codex-to-Arquitecto-TASK-0151-in-review.md` with handoff
  `Area_comun/handoffs/HANDOFF-TASK-0151-codex-to-arquitecto-1.md`.
- TASK-0150 product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `5121335 feat(intake): emit file extraction tasks`. File intake v2 Phase A now keeps upload ingestion
  OFF-by-default, hashes raw upload bytes with SHA-256, performs honest best-effort ASCII PII screening, stores
  raw uploads in OS temp outside the attested dataset, emits idempotent `TASK-EXTRACT-*` extraction tasks via
  governed `task_upsert`, and adds the typed/file intake mode selector with execute-time required-field checks.
  Evidence before commit: `node --check src/server.js public/app.js tests/staticContract.test.js`, product
  `npm test` PASS 42/42, and clean-clone Zeus `npm test` PASS 42/42. Protocol delivery moved TASK-0150 to
  `in_review`, released `CLAIM-20260622-Codex-TASK-0150`, answered the GO, and opened
  `Area_comun/mailbox/open/MSG-20260622-Codex-to-Arquitecto-TASK-0150-in-review.md` with handoff
  `Area_comun/handoffs/HANDOFF-TASK-0150-codex-to-arquitecto-1.md`.
- TASK-0149 product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `03991cd fix(intake): reject phantom requirements`. The Intake no longer preloads example narrative,
  acceptance, or project values; server-side `requirement-intake` rejects empty/placeholder narrative and
  acceptance, and requires an explicit project instead of defaulting to `Zeus-protocol`. The front keeps failed
  submissions as real errors, without reset-as-success. Evidence: `node --check public/app.js src/server.js
  tests/staticContract.test.js`, product `npm test` PASS 41/41, and clean-clone Zeus `npm test` PASS 41/41.
  Handoff prepared at `Area_comun/handoffs/HANDOFF-TASK-0149-codex-to-arquitecto-1.md`.
- TASK-0148 CRLF determinism fix landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `2f760a6 test(front): make mermaid fixture CRLF stable`. The product repo now has `.gitattributes` enforcing
  LF checkout for text/code files, and the Mermaid code-fence test accepts `\r?\n`, fixing the clean-clone
  Windows red reported by Analista. No ingestion logic changed. Evidence: `node --check public/app.js
  tests/staticContract.test.js src/server.js`, product `npm test` PASS 41/41, and clean-clone Zeus `npm test`
  PASS 41/41. Handoff prepared at
  `Area_comun/handoffs/HANDOFF-TASK-0148-CRLF-codex-to-arquitecto-1.md`.
- TASK-0148 product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `0eaf602 feat(intake): gate file requirement ingestion`. The Intake now has an OFF-by-default file ingestion
  config (`file-ingestion.config.json` with runtime/local overrides ignored), server-side bounded `.md/.txt`
  validation, safe basename checks, inert active-content rejection, PII/ASCII redaction, idempotent relay into the
  existing `requirement-intake` path, and permanent anti-abuse coverage. Evidence before commit: `node --check
  public/app.js tests/staticContract.test.js src/server.js`, `npm test` PASS 41/41, healthz smoke OK with
  `fileIngestion.enabled=false`. Handoff prepared for Arquitecto at
  `Area_comun/handoffs/HANDOFF-TASK-0148-codex-to-arquitecto-1.md`.
- TASK-0147 product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `7daf70e feat(front): filter ledger events`. The Ledger #4 view now exposes read-only actor/type filters,
  paginates the timeline at 40 events by default, supports progressive "Show more", and keeps payload previews
  redacted. The observe reader now sends the full ledger event list to the client while the DOM render remains
  bounded by pagination. Evidence before commit: `node --check public/app.js tests/staticContract.test.js
  src/server.js`, `npm test` PASS 39/39, healthz smoke OK. Handoff prepared for Arquitecto at
  `Area_comun/handoffs/HANDOFF-TASK-0147-codex-to-arquitecto-1.md`.
- TASK-0146 product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `90ea26b feat(front): compact empty backlog lanes`. The Backlog kanban now builds its board from
  `tasks.byStatus` so `done` content is visible, marks empty lanes as compact header-only columns, adapts lane
  widths to populated content, and shows an overflow summary after the first 12 cards. The change is read-only
  and does not add any `submit_intent` surface. Evidence before commit: `node --check public/app.js
  tests/staticContract.test.js src/server.js`, `npm test` PASS 38/38, healthz smoke OK. Handoff prepared for
  Arquitecto at `Area_comun/handoffs/HANDOFF-TASK-0146-codex-to-arquitecto-1.md`.
- TASK-0145 product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `5f53224 feat(front): improve mailbox and backlog hierarchy`. The Mailbox cards now prioritize the human
  subject as `.mailbox-subject` and demote `MSG-...` plus route metadata to secondary monospace text; Backlog
  cards now show the task title before the technical id, with ids visually secondary. The change is read-only
  and preserves the existing front surface. Evidence before commit: `node --check public/app.js
  tests/staticContract.test.js src/server.js`, `npm test` PASS 37/37, healthz smoke OK. Handoff prepared for
  Arquitecto at `Area_comun/handoffs/HANDOFF-TASK-0145-codex-to-arquitecto-1.md`.
- TASK-0144 product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `4ee322b feat(front): render help mermaid diagrams`. The Help view now renders Mermaid `flowchart` and
  `sequenceDiagram` code fences as client-side SVG diagrams instead of raw code, while keeping `package.json`
  free of npm/server dependencies. The change is read-only and does not add any `submit_intent` surface.
  Evidence before commit: `node --check public/app.js tests/staticContract.test.js src/server.js`, `npm test`
  PASS 36/36, healthz smoke OK. Handoff prepared for Arquitecto at
  `Area_comun/handoffs/HANDOFF-TASK-0144-codex-to-arquitecto-1.md`.
- TASK-0143 product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `8e41461 feat(front): explain RF and glossary terms`. The front now uses one shared
  `HELP_GLOSSARY_TERMS` dictionary for RF-N/acronym tooltips and the Help-rendered surface, annotates matching
  terms with `title`, `aria-label`, `role="button"`, focusability and pointer cursor, and covers RF-5/RF-14,
  SDD, T0, HMAC and PII. The integration test fixture now selects a claim-free and drift-free protocol ref
  before write-real tests, preventing false reds when live protocol HEAD is mid-ledger. Evidence before commit:
  `node --check public/app.js tests/staticContract.test.js src/server.js`, `npm test` PASS 35/35, healthz smoke
  OK. Handoff prepared for Arquitecto at
  `Area_comun/handoffs/HANDOFF-TASK-0143-codex-to-arquitecto-1.md`.
- TASK-0142 product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `cb4c0b1 feat(front): explain integrity badges`. The front now gives each integrity-band indicator
  (epoch, drift, attestation, canonical source, validator) a short accessible tooltip via `title` and
  `aria-label`, covering normal value, what change means, and when to worry. Change is read-only and does
  not add a `submit_intent` surface. Evidence before commit: `node --check public/app.js
  tests/staticContract.test.js src/server.js`, `npm test` PASS 34/34, healthz smoke OK. Handoff prepared for
  Arquitecto at `Area_comun/handoffs/HANDOFF-TASK-0142-codex-to-arquitecto-1.md`.
- TASK-0141 product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `88b4604 feat(front): show data freshness state`. The front now derives `actualizado hace Ns` from the
  real timestamp of the last successful fetch, shows a subtle loading spinner through the status dot, and
  marks the integrity note `STALE` after the configured freshness threshold. Fetch failures do not update
  `lastRefreshAt`, preserving no-stale-as-fresh behavior. Evidence before commit:
  `node --check public/app.js tests/staticContract.test.js src/server.js`, `npm test` PASS 33/33, healthz
  smoke OK. Handoff prepared for Arquitecto at
  `Area_comun/handoffs/HANDOFF-TASK-0141-codex-to-arquitecto-1.md`.
- TASK-0140 product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `60fdb97 feat(front): refresh data on navigation`. The front now fetches fresh observe/actions/help data and
  re-renders when navigating between views, exposes a read-only refresh button per panel, and has an opt-in
  interval refresh control. The exported refresh controller has behavior coverage for navigation fetch,
  manual refresh, configured interval, and fetch-failure no-stale-as-fresh. Evidence before commit:
  `node --check public/app.js tests/staticContract.test.js src/server.js`, `npm test` PASS 31/31, healthz
  smoke OK. The Codex mailbox monitor script was updated for 5-minute cadence, executable Codex-message
  dispatch, and 7-round no-Arquitecto-response stop logic.
- TASK-0139 product commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `9d0a586 feat(intake): add governed auto commit push`. The server now has an OFF-by-default
  `commit-push.config.json` transport: after successful governed `submit_intent`, when enabled, it stages
  exactly runtime-reported outputs plus seed files and runtime state, commits with `commit --only` and a
  templated ASCII message, pushes without force to configured remote/branch, verifies landed HEAD, redacts
  remote credentials, and reports HEAD+seq only on push OK. Client `paths`/`commitMessage` remain rejected.
  Product evidence before commit: `node --check` for server/app/tests, `npm test` PASS 29/29, healthz smoke OK.
  Protocol handoff is `Area_comun/handoffs/HANDOFF-TASK-0139-codex-to-arquitecto-1.md`; GO was moved to
  answered, TASK-0139 moved to `in_review`, and `CLAIM-20260621-Codex-TASK-0139` was released via
  `runtime/submit_intent.py` (drift 0, up_to_seq 900). `design/front_pipeline.html` remains dirty and
  untouched.
- TASK-0138 AC26 product fix landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `7619fd2 fix(mailbox): derive archive attribution in server builder`. `mailbox-archive` now sends
  `author`/`relayed_by`/`endorsement` from the server-side action builder, keeps rejecting client
  `actorId`/`intents`, and rejects `:` in `messageId` for the NTFS ADS guard. Evidence before commit:
  `npm test` PASS 26/26 and `node --check src/server.js tests/staticContract.test.js` OK. Protocol-side AC26
  landed as `eee35c7 fix(runtime): make mailbox archive attribution caller-derived`: `mailbox_archive` now
  requires caller-derived `author`/`relayed_by`, message ids are limited to `MSG-[A-Za-z0-9._-]+`,
  `scan_domain_neutrality` has an identity-literal golden, RE-GO is answered, TASK-0138 is back in
  `in_review`, and Codex claim is released.
- TASK-0138 product implementation commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `6afefe7 feat(mailbox): add governed archive relay`. The front now exposes `mailbox-archive` as the second
  executable RF-14 action, builds its transaction server-side, rejects client actor/intents and unsafe
  message ids, and moves open mailbox messages to archived in the UI only after a real `submit_intent`
  response with id/seq. Product evidence before commit: `npm test` PASS 26 tests; `node --check` OK for
  `public/app.js`, `src/server.js`, and `tests/staticContract.test.js`. `design/front_pipeline.html`
  remains dirty and untouched. Protocol side is delivered in the current protocol commit: core
  `mailbox_archive` intent, golden cases, handoff, GO answered, TASK-0138 moved to `in_review`, and Codex
  claim released through `runtime/submit_intent.py`.
- TASK-0132 implementation commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `a4acb68 feat(front): align selector and backlog with design`. The front now aligns the remaining stage 6.1
  design gaps: Backlog is a read-only kanban with agent filter and active-claim badges; Projects consumes
  project entities (`id/name/kind/source/state`) and includes the selector add-project card wired to the
  existing governed RF-10 kickoff; PII preview redaction is enforced at render; styles now expose the design
  token families. Product evidence before commit: `npm test` PASS 19 tests, `node --check public/app.js
  src/server.js` OK, server smoke on port 4176 OK (`/healthz`, `/api/protocol/observe`, 7 panels). Protocol
  encoding, neutrality, and validator were green before product commit. `design/front_pipeline.html` remains
  dirty and untouched.
- TASK-0130 implementation commit landed in `D:/Agentes/Zeus/Zeus-protocol`:
  `661ed8d feat(front): add multiproject selector and governed kickoff`. The front now has a read-only
  hub-centric product selector for `D:/Agentes/Zeus`, RF-10 governed kickoff preparation via
  `runtime/submit_intent.py`, behavior coverage for selector indicator honesty, and negative no-bypass checks
  (no repo creation / no `git init` route). Product evidence before commit: `npm test` PASS 15 tests,
  `node --check public/app.js src/server.js src/canonicalReader.js` OK, server smoke on port 4174 OK
  (`/healthz`, `/api/protocol/projects`, dry-run `project-kickoff-t0`). `design/front_pipeline.html` remains
  dirty and untouched. Protocol task is still in progress until handoff/status close is completed.
- TASK-0129 is delivered to `in_review`: `D:/Agentes/Zeus/Zeus-protocol` now has behavior tests for
  attestation badge honesty. `public/app.js` exports pure derivation helpers while preserving browser render;
  `tests/staticContract.test.js` verifies false-green prevention for chain, agent signatures, anchor,
  event-auth, drift, validator, source-state, and indeterminate cases. Evidence: product `npm test`
  (13 tests), `node --check public/app.js`, encoding, neutrality, and drift green. The protocol validator is
  blocked by unrelated mailbox anomaly `MSG-20260620-Operador-to-Arquitecto-GO-etapa6.md` (marked as requiring
  response without `question`); Codex notified Arquitecto in
  `Area_comun/mailbox/open/MSG-20260620-Codex-to-Arquitecto-validator-anomaly-etapa6.md`. Handoff:
  `Area_comun/handoffs/HANDOFF-TASK-0129-codex-to-arquitecto-1.md`. `personal/Codex/STARTUP_PROMPT.md` was
  refreshed for the next session with v1.14.0/#4 ON, TASK-0129 in_review, cron PID 141272, and the validator
  anomaly caveat.
- TASK-0128 is delivered to `in_review`: `D:/Agentes/Zeus/Zeus-protocol` now deepens RF-4 with a read-only
  #4 attestation view. The observe API exposes runtime-derived chain, event-auth, agent-signature, anchor,
  drift, and source-state checks, plus boundary T0 / pre-T0 seal / `chain_manifest.json`; event payload
  previews are redacted as `[redacted - PII de tercero]`. Evidence: product `npm test` (11 tests), `node
  --check` for server/reader/app, server smoke on `http://127.0.0.1:4173` PID 137252, protocol validator,
  encoding, neutrality, and drift green. Handoff:
  `Area_comun/handoffs/HANDOFF-TASK-0128-codex-to-arquitecto-1.md`.
- TASK-0127 is delivered to `in_review`: `D:/Agentes/Zeus/Zeus-protocol` now exposes the governed operate
  surface for RF-5..RF-8. `/api/protocol/actions` lists SDD, GO/response, agent-run, and validation actions;
  `/api/protocol/actions/submit` prepares transactions and executes only through `runtime/submit_intent.py`
  with explicit `SUBMIT_INTENT` confirmation. Direct ledger/state/mailbox write surfaces are absent and
  rejected by contract. Evidence: product `npm test` (10 tests), server smoke on `http://127.0.0.1:4173`
  PID 137196, protocol validator, encoding, neutrality, and drift green. Handoff:
  `Area_comun/handoffs/HANDOFF-TASK-0127-codex-to-arquitecto-1.md`.
- TASK-0126 is delivered to `in_review`: product code lives in `D:/Agentes/Zeus/Zeus-protocol` and now
  implements front stage 2 observe with RF-1 dashboard, RF-2 mailbox, RF-3 artifacts, and RF-4 #4 ledger
  timeline. The server exposes read-only `/api/protocol/observe`; canonical data is read from the protocol
  repo through allowlisted `git show <ref>:<path>` and `git ls-tree`, with no direct write APIs or ledger
  mutation routes. Evidence: product `npm test` (8 tests), protocol validator, encoding, neutrality, and
  drift green. Handoff: `Area_comun/handoffs/HANDOFF-TASK-0126-codex-to-arquitecto-1.md`.
- TASK-0125 is delivered to `in_review`: `connectors/ci_readonly/` implements a deny-by-default CI read
  connector with fixture backend; `examples/connector_ci_cases` covers AC1-AC7, including 11 negative
  vectors with 0 backend calls; CI includes the golden. `connectors.config.json` records `fixture-ci-ro`
  outside `protocol.config.json`, `enabled:false`; live use remains gated by s9 + operator GO. Handoff:
  `Area_comun/handoffs/HANDOFF-TASK-0125-codex-to-arquitecto-1.md`.
- TASK-0124 stage 1 is delivered to `in_review`: product code lives in `D:/Agentes/Zeus/Zeus-protocol`;
  dependency-free Node scaffold adds static UI shell, local `/api/protocol/snapshot`, and a canonical
  reader using `git show <ref>:<path>` against the protocol repo rather than the working tree. Product
  tests pass (`npm test`, 4 tests). Handoff:
  `Area_comun/handoffs/HANDOFF-TASK-0124-codex-to-arquitecto-1.md`.
- TASK-0123 is delivered to `in_review`: `connectors/git_readonly/` implements a deny-by-default Git
  inspection connector with fixture backend; `examples/connector_git_cases` covers AC1-AC7, including 10
  negative vectors with 0 backend calls; CI includes the golden. `connectors.config.json` records
  `fixture-git-ro` outside `protocol.config.json`, `enabled:false`; live use remains gated by s9 + operator
  GO. Handoff: `Area_comun/handoffs/HANDOFF-TASK-0123-codex-to-arquitecto-1.md`.

## Current Repository State

- Latest observed HEAD before this refresh: `823b5b9 chore(personal): renombra areas a la identidad nueva (personal/Claude->Arquitecto, personal/Claude-analista->Analista)`.
- v1.9.3 is published and the OFF-PILOT trio is closed: TASK-0100, TASK-0095, and TASK-0096 are done.
- Identity reform is live: use `Arquitecto` for the architect/orchestrator and `Analista` for the independent
  analyst voice. The ledger actor was renamed from `Claude` to `Arquitecto` through coordinated re-genesis
  (`c9a5dd6 chore(identity): renombra actor del ledger Claude -> Arquitecto (re-genesis)`).
- `personal/Claude/` and `personal/Claude-analista/` were renamed to `personal/Arquitecto/` and
  `personal/Analista/`. Do not edit those areas unless the operator explicitly asks.
- Claude's stand-down FYI was archived after explicit operator request to hygiene Codex mailbox:
  `Area_comun/mailbox/archived/MSG-20260614-Claude-to-Codex-stand-down-cron.md`.
- Expected Codex mailbox after hygiene: no open messages addressed to Codex unless new messages arrive.
- Coordination after operator request:
  - Codex sent `Area_comun/mailbox/open/MSG-20260614-Codex-to-Claude-coord-next-work.md` asking Claude
    whether there is a new GO or Codex remains in stand-down.
  - Codex answered `Area_comun/mailbox/answered/MSG-20260614-Claude-to-Codex-gate-coupling-readonly-s9.md`.
    ACK: Codex owns the future read-only invariant verification for `protocol_research` coupling/exporters
    post-GATE-DATASET, before any live Core read. No action now; current work remains gate-only/stub-only.
- Operator reactivated Codex for the OFF-PILOT trio and asked for a 5-minute coordination cron with Claude.
  That process is now closed; the local coordination cron was stopped and `personal/Codex/coord_cron.stop`
  may exist. Do not restart it without explicit operator reactivation.
- TASK-0100 is implemented and in `in_review` under DECISION-0037 option A. Scope is future releases:
  `.gitattributes` added for LF checkouts, `dist/v1.1.0/KNOWN_LIMITATIONS.md` documents v1.1.0 as
  pre-normalization with 616 LF / 127 CRLF / 14 no-EOL, `SPEC-0075` has a rescope amendment, and
  `scripts/verify_release.py` emits a visible `release_scope` note for v1.1.0 without suppressing failures.
  Handoff: `Area_comun/handoffs/HANDOFF-TASK-0100-codex-to-claude-1.md`.
  Evidence: release verify harness OK (7 cases), clean HEAD renormalize guard staged only `.gitattributes`,
  validator/encoding/neutrality/drift green. v1.1.0 manifest/signature were not regenerated or edited.
- TASK-0100 was later closed by Claude in v1.9.1. TASK-0095 is now implemented and in `in_review`:
  `runtime/apply.py` derives task markdown paths mutated by turn transitions and includes them in
  `commit_turn`; `examples/runtime_apply_cases` now proves the task `.md` is committed even when omitted
  from `changed_paths`. Handoff:
  `Area_comun/handoffs/HANDOFF-TASK-0095-codex-to-claude-1.md`. Evidence: runtime_apply OK (4),
  runtime_loop OK (15), runtime_real_adapter OK (4), intent_flow OK (11), validator/encoding/neutrality/drift
  green. No active Codex claims expected.
- DECISION-0038 is accepted by operator order: minimal narration is now a primordial rule. AGENTS.md,
  AGENTS.template.md, personal/Codex/STARTUP_PROMPT.md, and personal/Claude/STARTUP_PROMPT.md were hardened:
  no visible process narration, no step announcements/recaps, no non-actionable periodic progress. Only final
  report/handoff, real blocking question, actionable coordination result, or substantive reasoning-as-deliverable.
- TASK-0096 is implemented and in `in_review`: real subprocess invoker runs require an explicit fresh
  `--run-id`; existing `runtime/runs/<run_id>.jsonl` is rejected before invoker execution to avoid run-log
  accumulation and cross-run metrics. Handoff: `Area_comun/handoffs/HANDOFF-TASK-0096-codex-to-claude-1.md`.
  Evidence: llm_adapter OK (6), runtime_real_adapter OK (5), supervised_autonomy OK (10), runtime_loop OK
  (15), runtime_budget OK (5), runtime_observability OK (5), runtime_cost_attribution OK (11),
  validator/encoding/neutrality/drift green. No active Codex claims expected.
- Delivery coordination for TASK-0096 was sent to Claude:
  `Area_comun/mailbox/open/MSG-20260615-Codex-to-Claude-TASK0096-delivery-coordination.md`.
  Commit `3add1c9` remains the implementation commit. Drift stayed 0; no active Codex claims. Validator is
  blocked in the live working tree by an unrelated peer mailbox anomaly:
  `Area_comun/mailbox/open/MSG-20260615-Claude-analista-to-Claude-sync-coordinacion.md` has `status:
  answered` while sitting in `open/`.
- The peer mailbox anomaly was notified to Claude in
  `Area_comun/mailbox/open/MSG-20260615-Codex-to-Claude-mailbox-anomaly-sync-coordinacion.md`. Codex did not
  edit the peer-owned anomalous message.
- Codex mailbox hygiene archived the non-response TASK-0096 delivery FYI:
  `Area_comun/mailbox/archived/MSG-20260615-Codex-to-Claude-TASK0096-delivery-coordination.md`. Validator
  is OK with one unrelated warning for `MSG-20260615-Claude-to-ClaudeAnalista-sync-reply.md`; drift 0 and
  no active Codex claims.
- Arquitecto closed the OFF-PILOT trio and sent Codex stand-down:
  `Area_comun/mailbox/archived/MSG-20260615-Claude-to-Codex-trio-cerrado-standdown.md`. Codex mailbox is
  clean for Codex; only non-Codex open mailbox remains. Local coordination cron was stopped (PID 80672) and
  `personal/Codex/coord_cron.stop` was created locally. Do not take new tasks until operator reactivation.
- Expected active claims: none for Codex.
- No remaining Codex-relevant trio tasks are active after review. Do not claim new work without a fresh GO and
  a mailbox/claims check.
- Runtime flags to preserve: `chain_enabled=false`, `agent_signatures_enabled=false`, `anchor_enabled=false`,
  subagents off, SA.4 not fired. Do not enable #4/chain/auth/anchor without the TASK-0113/#4 gate sequence and
  explicit operator/architect GO.

## Personal Area Hygiene

- `personal/Codex/` is the only Codex private area. Do not use legacy `Codex/`.
- Old root-level intent/claim JSON envelopes were moved to `personal/Codex/archive/intents/` during this refresh.
  They are retained for traceability but should not clutter cold-start reading.
- Root of `personal/Codex/` should stay small: `README.md`, `Memory.md`, `STARTUP_PROMPT.md`, durable reports, and
  archive folders.
- Do not touch `personal/Arquitecto/`, `personal/Analista/` or `personal/operador/` unless the operator explicitly asks.

## Operating Rules

- Read `AGENTS.md` first on every cold start, then this memory and `personal/Codex/STARTUP_PROMPT.md`.
- Shared state is runtime-authoritative. Never edit `Area_comun/state/*.json` by hand; use `runtime/submit_intent.py`
  or `runtime/ledger_ops.py --submit`.
- Before editing shared routes, including mailbox, create or update an active claim that covers the route.
- Release a claim when moving work to `in_review`/`done` or when a hygiene step is finished.
- After every Codex commit, update this memory so the next cold start reflects the committed state.
- Stage explicit paths only. Leave unrelated dirty worktree changes alone.

## Known Dirty-Tree Caution

- The worktree may contain unrelated edits under `personal/Arquitecto/`, `personal/Analista/` and `personal/operador/`.
  Treat them as peer/operator state and do not revert or stage them.
- Latest Codex mailbox hygiene: archived `MSG-20260615-Claude-to-Codex-trio-cerrado-standdown.md`, stopped the
  coordination cron via `personal/Codex/coord_cron.stop`, released `CLAIM-20260615-Codex-standdown`, and left no
  active Codex claims. Commit: `c0efaaf chore(mailbox): archive Codex stand-down`.
- Startup files were refreshed so the next Codex session reads both `personal/Codex/STARTUP_PROMPT.md` and
  this memory before acting.

## Useful Fresh-Session Commands

```powershell
git status --short
git log -5 --oneline
Get-ChildItem -File Area_comun\mailbox\open | Select-Object -ExpandProperty Name
python scripts\validate_collaboration_state.py --root .
python -c "from pathlib import Path; from runtime.protocol_replay import protocol_state_drift; import json; print(json.dumps(protocol_state_drift(Path('.')), indent=2, ensure_ascii=False))"
```

If a Windows sandbox tempfile test fails with `WinError 5` / `PermissionError`, remember the known inherited-ACL
issue. Re-run only the necessary evidence path and record the caveat.
