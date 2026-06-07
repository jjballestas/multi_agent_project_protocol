# BRIDGE_CONTRACT.md - File Bridge Contract

The shared bridge is file-based:

- Global state: `Area_comun/state/PROJECT_STATE.json`
- Task index: `Area_comun/state/TASK_INDEX.json`
- Claims: `Area_comun/state/CLAIMS.json`
- Messages: `Area_comun/mailbox/<open|answered|archived>/`
- Formal deliveries: `Area_comun/handoffs/`
- Decisions: `Area_comun/decisions/`

This bridge does not define project domain policy. Domain policy is declared by each project
instance through `AGENTS.md`, `contracts/` and `protocol.config.json`.

