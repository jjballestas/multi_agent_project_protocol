# Skills

Skills are governed, read-only procedure documents. A skill gives an agent inert text to read during cold start; it does not grant authority, execute code, mutate protocol state, or write to the event log.

This layer is separate from `protocol.config.json`. The registry is `skills/skills.config.json`, defaults each skill to disabled, and is not part of event-log genesis.

Hard rules:

- Read-only and off-by-default. A missing registry or all-disabled registry loads as an empty index.
- A `trust_boundary` is required per skill and must declare `read_only:true`, `grants_no_authority:true`, and `persists_outputs:false`.
- Core skills under `skills/` must be neutral mechanism examples and declare `neutral_core:true`.
- Profile-specific skill content must live under `profiles/<profile>/skills/`.
- Loader outputs stay in memory. The loader does not import ledger or event-log writers and does not persist loaded procedures.
