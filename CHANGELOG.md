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

## [Unreleased] — target v0.3.0 (profiles)

### Added
- **Core / profiles / examples architecture**
  ([DECISION-0002](Area_comun/decisions/DECISION-0002-core-perfiles-profesionales.md), TASK-0005):
  the `profiles/` layer with `profiles/README.md`, a neutral `PROFILE_TEMPLATE/`
  (`profile.manifest.template.json` + README + `docs/`/`templates/`/`prompts/`), the
  `profile.manifest` contract, and `Area_comun/artifacts/ARQUITECTURA-core-profiles.md`.
  This is an **additive (MINOR)** capability — the core stays domain-neutral.

### Pending
- TASK-0006 (Codex): `profiles/dotnet_enterprise/` built from the enterprise .NET practices.
- TASK-0007 (Codex): optional `adopted_profiles` in state + profile-aware validator (additive,
  `.py` ↔ `.ps1` parity).

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

[Unreleased]: https://example.invalid/compare/v0.2.0...HEAD
[0.2.0]: https://example.invalid/compare/v0.1.0...v0.2.0
[0.1.0]: https://example.invalid/releases/tag/v0.1.0
