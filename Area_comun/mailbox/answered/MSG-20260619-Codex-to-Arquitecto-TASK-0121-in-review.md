---
message_id: MSG-20260619-Codex-to-Arquitecto-TASK-0121-in-review
type: HANDOFF
task_id: TASK-0121
from: Codex
to: Arquitecto
requires_response: true
response_owner: Arquitecto
status: answered
one_line_summary: "TASK-0121 implementada y en in_review: connectors/ neutral read-only deny-by-default + SQL Server fixture backend + golden AC1-AC7 + CI + neutrality scan sobre connectors/."
question: "Puedes reproducir TASK-0121 como checker maker!=checker y cerrar si AC1-AC10 te salen verdes?"
requested_action: "Reproducir: python examples/connector_sqlserver_readonly_cases/run_connector_sqlserver_readonly_cases.py; python scripts/validate_collaboration_state.py --root .; python scripts/scan_encoding.py --root .; python scripts/scan_domain_neutrality.py --root .; revisar AC4 gate no imports de escritores en connectors/."
context_refs:
  - Area_comun/tasks/TASK-0121-codex-connector-sqlserver-readonly.md
  - Area_comun/specs/SPEC-0083-connector-sqlserver-readonly.md
  - Area_comun/decisions/DECISION-0044-connector-readonly-deny-by-default.md
  - connectors/README.md
  - connectors/connectors.config.json
  - examples/connector_sqlserver_readonly_cases/run_connector_sqlserver_readonly_cases.py
deadline_or_blocking_level: normal
---

# Handoff TASK-0121

Implementacion lista para review.

Cambios:

- `connectors/` neutral con framework (`Connector`, `TrustBoundary`, errores, clasificador read-only deny-by-default).
- `connectors/sqlserver_readonly/` con `SqlServerReadOnlyConnector` y `FixtureBackend`.
- `connectors/connectors.config.json` fuera de `protocol.config.json`, default `enabled:false`.
- Golden `examples/connector_sqlserver_readonly_cases/` para AC1-AC7: trust boundary, lectura fixture, 7 vectores negativos, gate AC4 sin imports de escritores, cero cambios en estado/event log, live fail-closed, registro fuera del config, dato PII-like solo en memoria.
- CI cableado y `scan_domain_neutrality.py` ahora incluye `connectors/**` si existe la capa.
- `CHANGELOG.md` documenta 1.15.0. No toque `protocol.config.json` para preservar la invariante de genesis/T0.

Evidencia local verde:

- `python examples\connector_sqlserver_readonly_cases\run_connector_sqlserver_readonly_cases.py`
- `python -m compileall -q connectors examples\connector_sqlserver_readonly_cases`
- `python examples\readonly_enforcement_cases\run_readonly_enforcement_cases.py`
- `python examples\event_auth_secret_resolution_cases\run_event_auth_secret_resolution_cases.py`
- `python examples\chain_auth_combined_cases\run_chain_auth_combined_cases.py`
- `python scripts\validate_collaboration_state.py --root .`
- `python scripts\scan_encoding.py --root .`
- `python scripts\scan_domain_neutrality.py --root .`

Notas:

- No hay lectura viva ni driver DB.
- No se tocan flags de #4.
- La ruta viva queda fail-closed hasta GO posterior del operador y verificacion server-side de minimo privilegio.
