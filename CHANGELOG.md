# Changelog

All notable changes to the **multi_agent_project_protocol** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
as scoped for a *protocol* (not a library): see
[`Area_comun/decisions/DECISION-0001-versionado.md`](Area_comun/decisions/DECISION-0001-versionado.md)
for what counts as MAJOR / MINOR / PATCH here.

> **Scope note.** Versions in this file describe **the protocol itself** (its structure,
> lifecycle, required fields, templates and validator). Each *instance* declares which protocol
> version it follows via `protocol_version` in its `protocol.config.json`. The protocol is **not**
> pushed automatically to instances; an instance adopts a new version through a decision of its own.

## [Unreleased]

_No changes yet._

## [0.10.0] — 2026-06-06

N-agent **core consolidation** release. Packages the N-agent runtime phases 1-4 and the full
**Layer A** consolidation, plus three protocol decisions. **MINOR** — additive, domain-neutral,
back-compatible (the legacy N=2 path stays byte-equivalent; every previously valid turn report stays
valid; runtime stays gated/off-by-default in templates).

### Added
- **N-agent runtime core (phases 1-4)** against [SPEC-0038](Area_comun/specs/SPEC-0038-n-agent-registry.md):
  - Phase 1 — agent registry + capability resolution + semantic turn validation (TASK-0043).
  - Phase 2 — append-only event log: writer-only `seq`, per-aggregate `aggregate_version`/idempotency +
    leases/fencing, snapshot/compaction, negative replay (TASK-0044).
  - Phase 3 — deterministic weighted-least-loaded router with author exclusion and fairness gate
    (TASK-0045).
  - Phase 4 — Review/QA state machine: defect logs, canonical `failure_signature`, loop-cut to
    `architect_review`, evidence-gated `done` (TASK-0046).
- **Layer A — core consolidation**:
  - A.5 runtime suites wired into CI (TASK-0047).
  - A.1 event log as **live writer of the control-plane** (Phase A): `assert_snapshot_matches` hard-gate
    in `apply` and in the global validator when `runtime/state` exists; fallback intact
    (TASK-0048, [SPEC-0039](Area_comun/specs/SPEC-0039-event-log-writer-vivo.md), DECISION-0017 scope A->B).
  - A.6 author-of-record hardening (I1/I2 read from state, not payload) (TASK-0049).
  - A.2 golden N=3/N=5 (reviewer/QA separation + deterministic load balancing) (TASK-0050).
  - A.3 property-based invariants I1-I8 (TASK-0051).
  - A.4 concurrency simulation (10 implementers / 100 tasks: conflicts recorded, no snapshot
    corruption, fairness, zero double-applications) (TASK-0052).
  - A.7 explicit turn-schema SemVer (`schema_version 1.1.0` + `Area_comun/protocol/SCHEMA_VERSIONING.md`)
    (TASK-0053).
- **`turn_schema` is now versioned** (`schema_version: 1.1.0`, additive metadata).

### Decisions
- [DECISION-0016](Area_comun/decisions/DECISION-0016-areas-personales-onboarding.md) — personal areas under
  `personal/<id>/` + onboarding rule.
- [DECISION-0017](Area_comun/decisions/DECISION-0017-event-log-writer-vivo.md) — event-log-as-live-writer
  scope: A->B incremental (Phase A done; Phase B gated).
- [DECISION-0018](Area_comun/decisions/DECISION-0018-notificacion-de-anomalias.md) — anomaly notification
  between agents via mailbox.

### Notes
- The full global test plan (SPEC-0038 sec.15.3-15.5: N=3/N=5 golden, property-based, concurrency) is covered.
- Phase B (event log as live writer of the **protocol state**) and Phases 5-7 remain **gated**.

## [0.9.0] — 2026-06-06

Runtime **M2 hito 2** release: the orchestration runtime gains its **first real (non-replay) agent
invoker**, vendor-neutral and gated, all **additively and off-by-default** (`runtime.enabled:false`,
default adapter still `replay`). Running a real agent requires explicit opt-in flags
(`--adapter llm --llm-invoker subprocess --allow-real-invoker --llm-command <cmd> --once`) and a human
gate for the first live run. **MINOR** — additive, domain-neutral, back-compatible (every previously
valid turn report stays valid).

### Added
- **Real LLM adapter** (TASK-0036, [SPEC-0035](Area_comun/specs/SPEC-0035-adapter-llm-real.md)):
  `runtime/adapters/llm_adapter.py` — `LLMAdapter(AgentAdapter)` driven by a **pluggable `Invoker`**.
  `RecordedInvoker` (transcript `recorded_invoker.v1`, no network) keeps golden cases deterministic;
  `SubprocessInvoker` runs a **generic external command** (vendor-neutral: Claude SDK / Codex CLI are
  configurations of this invoker, not the base). Orchestrator flags `--adapter llm`,
  `--llm-invoker recorded|subprocess`, `--llm-command`, `--allow-real-invoker`. Limits reuse M1: the real
  invoker requires `enabled` + `--allow-real-invoker` + `--llm-command` + `--once`; `changed_paths`
  outside the active claim are rejected; per-turn budget aborts before mutating state. Default stays
  `replay`; CI never uses the real invoker. Golden `examples/llm_adapter_cases/` (once, replay-comparative
  `llm==replay`, allowlist rejection, budget abort, `enabled:false` abort).
- **Windows-safe subprocess command parsing** (TASK-0039,
  [SPEC-0036](Area_comun/specs/SPEC-0036-subprocess-invoker-windows-safe.md)):
  `SubprocessInvoker.from_command` tokenizes via `CommandLineToArgvW` on Windows (and `shlex` on POSIX),
  so a real `--llm-command` with native backslash paths and quoted spaces works instead of failing with
  `WinError 2`. Golden subprocess case runs end-to-end with the host-native separator.

### Notes
- First **real run on the live repo** executed under human approval (DECISION-0009 decision #2): the
  runtime closed a task with one gated M1 commit via the real subprocess invoker. Run-logs
  (`runtime/runs/`) are local audit traces and are git-ignored.
- Autonomous multi-turn loop, mailbox automation and a real LLM wrapper remain **M2 (later milestones)**
  and gated.

## [0.8.0] — 2026-06-06

Runtime **M1** release: the orchestration runtime gains its **first safe writer** and closes the
turn loop **deterministically**, all **additively and off-by-default** (`runtime.enabled:false`).
Nothing runs real agents yet — M1 proves the apply/gate/commit engine and the loop via a **replay
adapter**; real LLM adapters and autonomous multi-agent operation are M2 (and turning the runtime on
requires human approval). **MINOR** — additive, domain-neutral, back-compatible.

### Added
- **Turn apply + gate + commit/revert** (TASK-0030, [SPEC-0029](Area_comun/specs/SPEC-0029-turn-apply-gate.md)):
  `runtime/apply.py` (writes only if `validate_turn` passes), `runtime/gate.py` (validator + neutrality
  scan) and `runtime/vcs.py` (one commit per green turn; `git restore` + task `blocked` on a red gate).
  Honors the write-allowlist and row-scoped claims. Golden `examples/runtime_apply_cases/` (repo-fixture, 4/4).
- **Vendor-neutral agent adapter + replay + run loop** (TASK-0031,
  [SPEC-0030](Area_comun/specs/SPEC-0030-adapter-replay-loop.md)): `runtime/adapters/base.py`
  (`AgentAdapter` Protocol + `ContextPack`/`TurnReport`), `runtime/adapters/replay.py` (deterministic
  report replay), `runtime/runlog.py` (JSONL run-log with injectable `--run-id` + deterministic
  `RUN-<sha256>` default), and `runtime/orchestrator.py` `--run/--once/--max-iter` reusing the
  apply+gate+commit engine. `--plan` stays read-only. Golden `examples/runtime_loop_cases/` (5/5):
  `--once`=1 turn/1 commit, deterministic sequence cut by `--max-iter`, `human_required` hard-stop
  (no commit), `--plan` no-regression, `runtime.enabled:false` aborts `--run`.
- **M1 design + specs** (TASK-0029): `Area_comun/artifacts/DISENO-runtime-m1.md` + SPEC-0029/0030,
  refining the M1/M2 boundary (M1 deterministic via replay; real agents = M2).

### Notes
- Off-by-default and vendor-neutral: swapping the replay adapter for a future real adapter does **not**
  touch the loop. Activating `runtime.enabled:true` is a human-owner decision (DECISION-0009).

## [0.7.0] — 2026-06-05

Token-efficiency release: the protocol now **measures** its own context cost and trims the biggest
sources of cold-start bloat, cutting cold-start ~**75%** (≈37k → ≈9k proxy tokens) with no loss of
traceability. Also lands, **additively and off-by-default**, the runtime control-plane foundation (M0)
and a row-scoped state-claim model that lets two agents work in parallel without serializing on the
shared state files. **MINOR** — additive, domain-neutral, back-compatible.

### Added
- **Token-efficiency decision + design** ([DECISION-0008](Area_comun/decisions/DECISION-0008-eficiencia-de-tokens.md),
  TASK-0022): `Area_comun/artifacts/DISENO-eficiencia-de-tokens.md` + SPEC-0023/0024/0025 with a measured baseline.
- **Context-cost meter** `scripts/measure_context_cost.py`/`.ps1` (TASK-0023, SPEC-0023): deterministic
  chars/token proxy over cold-start globs + state dead-weight + mailbox frontmatter overhead; `--json`
  and `--budget` (warning); configurable `token_cost` block in `protocol.config(.template).json`;
  read-only. Golden `examples/context_cost_cases/`.
- **State pruning to history** (TASK-0024, SPEC-0024): `Area_comun/state/CLAIMS_ARCHIVE.json` /
  `TASK_INDEX_ARCHIVE.json` (+ templates); the validator reads **hot ∪ archive** (cross-ref duplicate
  detection). Cold-start **37 391 → ≈9k tokens (-75%)**; nothing deleted (archive ≠ delete).
- **Minimal mailbox frontmatter** (TASK-0025, SPEC-0025): a minimal variant + omission rule in
  `MAILBOX_MESSAGE_TEMPLATE.md`; the validator already tolerates omitted optional fields (back-compat).
  Golden `examples/compact_comms_validation_cases/minimal_frontmatter/` (-61% frontmatter chars on the example).
- **Runtime control-plane M0** ([DECISION-0009](Area_comun/decisions/DECISION-0009-runtime-orquestacion.md),
  TASK-0026/0027): `runtime/turn_schema.json` (strict turn contract), deterministic router, turn
  validator (schema + write-allowlist + race detection) and `orchestrator --plan` dry-run;
  `runtime.enabled:false` by default (`runtime/**` added to the neutrality scan). Golden
  `examples/runtime_turn_cases/`, `examples/runtime_router_cases/`.
- **Row-scoped state claims** ([DECISION-0011](Area_comun/decisions/DECISION-0011-claims-por-fila-estado.md),
  TASK-0028, SPEC-0028): claim scopes may target `TASK_INDEX.json#TASK-XXXX` /
  `PROJECT_STATE.json#active_tasks/TASK-XXXX`; same-row conflicts still caught, distinct rows no longer
  collide. Bare paths keep whole-file semantics (back-compat). Golden `examples/row_scoped_claim_cases/`.
- **Runtime M1/M2 design** (TASK-0029): `DISENO-runtime-m1.md` + SPEC-0029/0030 (apply+gate+commit/revert,
  adapter interface + replay loop) and `DISENO-runtime-m2.md` (real adapters + autonomous loop) — design
  only; implementation tracked as TASK-0030/0031 and later.

## [0.6.0] — 2026-06-05

Operational robustness: the protocol's own quality gates now run in CI, validation harnesses no
longer fail just because a runtime is missing, and instances get assisted version-adoption tooling.
**MINOR** release — additive, domain-neutral, no breaking changes. Closes the audit findings
(weak Python portability, incomplete CI, manual adoption/migration).

### Added
- **Operational robustness decision**
  ([DECISION-0006](Area_comun/decisions/DECISION-0006-robustez-operacional.md), TASK-0016): design
  (`Area_comun/artifacts/DISENO-robustez-operacional.md`) + specs SPEC-0017/0018/0019; defines the
  *neutral surface* and *adoptable set* reused by the scan and upgrade tools.
- **Complete CI** (TASK-0017): `.github/workflows/validate.yml` now also runs the PowerShell
  validator (dogfood + minimal), the SDD/compact/neutrality harnesses and the domain-neutrality
  scan — every gate promised in `AGENTS.md` §5 actually runs.
- **Domain-neutrality scan** `scripts/scan_domain_neutrality.py`/`.ps1` (TASK-0017): configurable via
  a `domain_neutrality` block in `protocol.config(.template).json` (denylist + scan/exempt globs,
  word-boundary match); `enabled:false`/absent ⇒ no-op. Golden cases in
  `examples/neutrality_scan_cases/`, `.py`↔`.ps1` parity.
- **Runtime-tolerant harnesses** (TASK-0018, DECISION-0006 §1): `run_sdd_cases.ps1` and
  `run_compact_comms_cases.ps1` resolve runtimes with fallback (`python`/`py -3`/`python3`,
  `pwsh`/`powershell`), mark the absent half `SKIPPED (WARNING)`, check parity only when both run,
  fail only on logic or no runtime, and always print a summary.
- **Assisted version upgrade** `scripts/upgrade_instance.py`/`.ps1` (TASK-0019, DECISION-0006 §4):
  read-only adoption report of deltas (`nuevo`/`cambiado`/`igual`/`eliminado`) between an instance
  and the master; does **not** modify the instance (adoption stays a per-instance decision,
  DECISION-0001). Fixtures in `examples/upgrade_cases/`, `.py`↔`.ps1` parity.
- **Claim-before-shared-draft rule**
  ([DECISION-0007](Area_comun/decisions/DECISION-0007-claim-before-shared-draft.md), TASK-0020):
  an agent must hold an active claim before creating/editing any draft on shared paths; unclaimed
  work is not overwritten — ask via one concrete mailbox question. Propagated to `AGENTS.md`,
  templates and protocol docs.

### Notes
- MINOR per DECISION-0001 §4 (additive, neutral). Hardening (require both runtimes, WARNING→build
  error, auto-apply upgrades) would be MAJOR (out of scope).
- Validator and domain-neutrality scan green (Python) on root; `.ps1` halves and CI verified by
  Codex/CI (PowerShell run blocked in the architect session by an environment deny-rule).
- Backlog opened, not in this release: TASK-0021 (mailbox-hygiene soft-checks).

## [0.5.0] — 2026-06-05

Compact, token-efficient agent communication: reference canonical artifacts instead of
reconstructing context in long conversations. **MINOR** release — additive, neutral, no length
limits, historical messages and handoffs remain valid.

### Added
- **Compact communication policy**
  ([DECISION-0005](Area_comun/decisions/DECISION-0005-comunicacion-compacta-token-efficient.md)):
  reference by ID/path, one intention (and one question) per message, send deltas, close the loop
  with standard codes (`ACK`/`FYI`/`OK`/`REVIEW`/`CHANGES`/`BLOCKED`/`DONE`/`DECISION_REQUIRED`/
  `HUMAN_REQUIRED`), move long content to artifacts/specs/reports/decisions.
- New `Area_comun/protocol/MAILBOX_MESSAGE_TEMPLATE.md` and a "Compact / token-efficient
  communication" section in `COMMUNICATION_PROTOCOL.md`.
- `HANDOFF_TEMPLATE.md` (compact note), `TASK_PROTOCOL.md` (one concrete question before blocking),
  `TASK_TEMPLATE.md` (`communication_budget`), `HUMAN_REPORT_TEMPLATE.md` (communication status).
- **Soft mailbox validations** (TASK-0014) in `validate_collaboration_state.py`/`.ps1`:
  `open`+`requires_response:true` ⇒ `requested_action` and `question` (ERROR); missing `context_refs`
  when referencing existing work (WARNING). Additive, `.py`↔`.ps1` parity, **no length checks**,
  historical/legacy messages exempt. Golden cases in `examples/compact_comms_validation_cases/`.
- **Reference instance** `examples/compact_communication_case/` (TASK-0015): compact mailbox
  (REVIEW→OK) + compact handoff, validates green.

### Notes
- MINOR per DECISION-0001 §4 (additive). Hardening (length limits, mandatory codes everywhere) would
  be MAJOR (out of scope). Validators green on root + all examples + SDD and compact-comms golden cases.

## [0.4.0] — 2026-06-05

Spec-Driven Development (SDD): clarity before execution. Implementable tasks must declare a spec,
execution pipeline, acceptance criteria, linked decisions, test plan and closure criteria before
they can start. **MINOR** release — additive, config-gated (off by default), no retroactive
migration of historical tasks.

### Added
- **SDD policy** ([DECISION-0004](Area_comun/decisions/DECISION-0004-sdd-pipeline-y-cierre.md),
  TASK-0008): the six SDD fields (`spec_id`, `execution_pipeline`, `acceptance_criteria`,
  `linked_decisions`, `test_plan`, `closure_criteria`) for implementable task types and four
  lightweight fields for discovery/analysis/review/documentation/triage; ambiguity ⇒ ask, never
  invent steps; design + rollout specs in `Area_comun/artifacts/DISENO-SDD.md` and
  `Area_comun/specs/SPEC-0009..0013`.
- **Protocol templates updated for SDD** (TASK-0009): `TASK_PROTOCOL.md` (SDD gate +
  clarity-before-execution + task `type`), `TASK_TEMPLATE.md`, `HANDOFF_TEMPLATE.md` (criteria +
  tests + spec deviations), `HUMAN_REPORT_TEMPLATE.md`.
- **Reusable spec templates** in `Area_comun/specs/` (TASK-0010): `SPEC_TEMPLATE`,
  `PROJECT_BRIEF_TEMPLATE`, `REQUIREMENTS_TEMPLATE`, `ACCEPTANCE_CRITERIA_TEMPLATE`,
  `TEST_PLAN_TEMPLATE`, `TRACEABILITY_MATRIX_TEMPLATE`.
- **Profile-aware → SDD-aware validators** (TASK-0011): config-gated SDD checks in
  `validate_collaboration_state.py`/`.ps1` (block `sdd` in `protocol.config.template.json`,
  default `enabled:false`), pre-SDD exemption, ERROR/WARNING rules, golden cases in
  `examples/sdd_validation_cases/` with `.py`↔`.ps1` parity.
- **Reference instance** `examples/minimal_sdd_instance/` (TASK-0012, `sdd.enabled:true`, validates
  green) and **SDD onboarding** section in `README_INSTANCIACION.md` (TASK-0013).

### Notes
- MINOR per DECISION-0001 §4 (additive, config-gated). `enabled:false`/absent ⇒ validators behave
  exactly as before. Retroactive enforcement to all tasks would be MAJOR (out of scope); TASK-0001..0007
  remain pre-SDD with no migration.
- Validators green on root and all examples (`minimal_instance`, `generated_minimal_instance`,
  `dotnet_enterprise_instance`, `minimal_sdd_instance`) plus SDD and profile golden cases.

## [0.3.0] — 2026-06-05

Professional profiles: the protocol becomes layered (core / profiles / examples) and can be
composed with optional, stack-specific profiles — the core stays domain-neutral. **MINOR** release
(backward-compatible, additive).

### Added
- **Core / profiles / examples architecture**
  ([DECISION-0002](Area_comun/decisions/DECISION-0002-core-perfiles-profesionales.md), TASK-0005):
  the `profiles/` layer with `profiles/README.md`, a neutral `PROFILE_TEMPLATE/`
  (`profile.manifest.template.json` + README + `docs/`/`templates/`/`prompts/`), the
  `profile.manifest` contract, and `Area_comun/artifacts/ARQUITECTURA-core-profiles.md`.
- **First professional profile** `profiles/dotnet_enterprise/` (TASK-0006): ADRs, branching,
  artifact model, SQL Server governance, template versioning, secure AI use, secret handling,
  container-network security, Azure DevOps pipelines, Dev Container / Docker SQL Server / DB
  bootstrap templates, onboarding and a .NET master prompt — all packaged as an **optional**
  extension with a `profile.manifest.json`. Source traceability in `docs/SOURCE_MAP.md`; secrets
  sanitized to placeholders.
- **`adopted_profiles` contract**
  ([DECISION-0003](Area_comun/decisions/DECISION-0003-adopted-profiles-contract.md)) and
  **profile-aware validators** (TASK-0007): optional `adopted_profiles` in
  `PROJECT_STATE.template.json` and additive checks in both `validate_collaboration_state.py` and
  `.ps1` (schema, id/version match against the manifest, `requires_protocol_version` compatibility,
  dependencies, duplicates) with `.py` ↔ `.ps1` parity and golden cases in
  `examples/profile_validation_cases/`.
- Reference instance `examples/dotnet_enterprise_instance/` (core + `dotnet_enterprise`, validates
  green, declares `adopted_profiles` + an instance adoption decision).

### Notes
- MINOR release per DECISION-0001 §4 (additive, no human approval required). Instances **without**
  `adopted_profiles` validate exactly as before (backward compatible).
- Validators green on root, `examples/minimal_instance/`, `examples/generated_minimal_instance/`,
  `examples/dotnet_enterprise_instance/` and all `examples/profile_validation_cases/`.

## [0.2.0] — 2026-06-05

Protocol enrichment: more portable, versioned and easier to instantiate. Domain-neutral core.

### Added
- **Versioning policy** ([DECISION-0001](Area_comun/decisions/DECISION-0001-versionado.md)) and
  this `CHANGELOG.md`: SemVer adapted to a file-based protocol (MAJOR/MINOR/PATCH with concrete
  examples), the release procedure, and human approval required for MAJOR releases.
- **`protocol_version`** declaration: new field in `protocol.config.template.json`
  (placeholder `{{PROTOCOL_VERSION}}`) and in this repo's live `protocol.config.json` and
  `examples/minimal_instance/`, so every instance records the protocol version it follows.
- **Cross-platform Python validator** `scripts/validate_collaboration_state.py` plus CI workflow
  `.github/workflows/validate.yml` (TASK-0002), complementing the PowerShell validator.
- **Scaffolding script** `scripts/new_instance.py` (TASK-0004): stdlib-only, renders the
  `*.template.*` masters into a valid instance, populates `protocol_version`, and fails on any
  unresolved `{{...}}` placeholder. Documented in `README_INSTANCIACION.md`.
- Roadmap to v0.2.0 in `Area_comun/artifacts/ROADMAP-v0.2.0.md` (TASK-0001).

### Notes
- v0.2.0 is a **MINOR** release (backward-compatible additions); no human approval required per
  DECISION-0001 §4. Validators green on root, `examples/minimal_instance/` and
  `examples/generated_minimal_instance/`.

## [0.1.0] — 2026-06-05

Initial extraction and bootstrap of the reusable, domain-neutral multi-agent protocol.

### Added
- Shared contract `AGENTS.md` and Claude-specific rules `CLAUDE.md`.
- `Area_comun/` protocol docs: `TASK_PROTOCOL.md`, `COMMUNICATION_PROTOCOL.md`,
  `HANDOFF_TEMPLATE.md`, `TASK_TEMPLATE.md`, human report template.
- Live state artifacts: `PROJECT_STATE.json`, `TASK_INDEX.json`, `CLAIMS.json`, mailbox,
  handoffs, decisions and reports folders.
- Shipped masters: `*.template.*` files and `protocol.config.template.json`.
- Reference instance `examples/minimal_instance/` (validates green).
- PowerShell validator `scripts/validate_collaboration_state.ps1`.

[Unreleased]: https://example.invalid/compare/v0.6.0...HEAD
[0.6.0]: https://example.invalid/compare/v0.5.0...v0.6.0
[0.5.0]: https://example.invalid/compare/v0.4.0...v0.5.0
[0.4.0]: https://example.invalid/compare/v0.3.0...v0.4.0
[0.3.0]: https://example.invalid/compare/v0.2.0...v0.3.0
[0.2.0]: https://example.invalid/compare/v0.1.0...v0.2.0
[0.1.0]: https://example.invalid/releases/tag/v0.1.0
