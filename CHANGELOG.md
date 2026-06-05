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

[Unreleased]: https://example.invalid/compare/v0.3.0...HEAD
[0.3.0]: https://example.invalid/compare/v0.2.0...v0.3.0
[0.2.0]: https://example.invalid/compare/v0.1.0...v0.2.0
[0.1.0]: https://example.invalid/releases/tag/v0.1.0
