# Connectors

Connectors are read-only adapters for external sources. A connector provides evidence to a caller; it does not grant authority, mutate protocol state, or write to the event log.

This layer is intentionally separate from `protocol.config.json`. The registry is `connectors/connectors.config.json`, defaults to disabled, and is not part of event-log genesis.

Hard rules:

- Read-only, deny-by-default. If an operation is not proven to be a single read or inspection operation, it is denied before any backend call.
- A `trust_boundary` is required per connector and must declare `read_only`, `grants_no_authority`, `persists_outputs`, and an allowlist.
- Live connections are fail-closed while disabled. The fixture backend is the only backend used by the golden tests.
- Outputs stay in memory. Connectors do not import ledger or event-log writers and do not persist result data.
- Live use against an external source requires a later operator GO plus an independent least-privilege verification.
- Action-capable surfaces such as Git stay limited to explicit inspection verbs until a later GO. Mutating verbs remain denied before backend access.
