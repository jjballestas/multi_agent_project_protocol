---
handoff_id: HANDOFF-TASK-0125-codex-to-arquitecto-1
task_id: TASK-0125
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-19
context_refs:
  - Area_comun/specs/SPEC-0087-connector-ci-readonly.md
  - Area_comun/decisions/DECISION-0048-connectors-accion-tool-policy.md
  - connectors/ci_readonly/connector.py
  - examples/connector_ci_cases/run_connector_ci_cases.py
---

# Handoff TASK-0125 - CI read-only connector

## Delivered

- Added `connectors/ci_readonly/` with `classify_ci_operation`, `CiReadOnlyConnector`, and deterministic `FixtureBackend`.
- Added `fixture-ci-ro` to `connectors/connectors.config.json`, outside `protocol.config.json`, with `enabled:false`, explicit read allowlist, and s9/operator-GO live preconditions.
- Added golden `examples/connector_ci_cases/run_connector_ci_cases.py` covering AC1-AC7, including 11 negative vectors rejected before backend access with 0 backend calls.
- Added CI workflow step for the CI connector golden and CHANGELOG capability line without bumping the pinned epoch/config.

## Evidence

- `python examples/connector_ci_cases/run_connector_ci_cases.py` -> pass, 8 cases.
- `python examples/connector_git_cases/run_connector_git_cases.py` -> pass, 8 cases.
- `python examples/connector_sqlserver_readonly_cases/run_connector_sqlserver_readonly_cases.py` -> pass, 7 cases.
- `python scripts/validate_collaboration_state.py --root .` -> OK with warning for non-response FYI still open.
- `python scripts/scan_encoding.py --root .` -> OK.
- `python scripts/scan_domain_neutrality.py --root .` -> OK.
- Drift check -> `has_drift:false`.

## Notes For Checker

- No live CI process or network is invoked. The only backend in tests is `FixtureBackend`.
- Live path remains fail-closed while `enabled:false`.
- Connector modules do not import `runtime.*` writer modules; AC4 also fingerprints event log and state files before/after fixture reads.
