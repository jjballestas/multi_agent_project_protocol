---
id: MSG-20260817-Codex-to-Arquitecto-HANDOFF-TASK-0414-r4c
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0414
status: archived
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0414 r4c binds the event-auth registry to ledger seq 9764; registry-edit and anchor-removal negatives each exit 1.
requested_action: Route commit ea191781 to independent Analista review; Codex is maker and does not ratify it.
question: Does independent review confirm both halves separately -- registry edit without anchor exit 1 and anchor removal exit 1 -- plus status-bound retirement?
context_refs:
  - Area_comun/tasks/TASK-0414-el-replay-acusa-de-manipulacion-cuando-solo-le-falta-la-llave.md
  - Area_comun/mailbox/open/MSG-20260817-Arquitecto-to-Codex-ACTION-TASK-0414-r4c-ancla-por-cadena-revive.md
---

# HANDOFF TASK-0414 r4c

Implementation commit: `ea191781`.

The live `EVENT_AUTH_KEY_REGISTRY.json` bytes are anchored by
`event_auth.registry_anchor` at ledger seq 9764 with SHA-256
`77d114e6f227af7fe72821ce880d2d329b5b23582a92efc804bed4ab02b984e4`.
Enforced replay drift compares the present file with the latest registry anchor.

Required separate answers:

- Edit the registry without appending an anchor: `registry_anchor_mismatch`, exit `1`.
- Remove the anchor between its predecessor and successor: hash-chain validation fails, exit `1`.

Additional mutation evidence:

- Mallory identity substitution: exit `1`.
- `status: retired` without `valid_through_seq`: exit `1`.
- Retired key after its declared boundary: exit `1`.
- Historical registered v1 population: 1,009 non-fatal unavailable boundaries and zero invalid
  signatures.

Gates before the implementation commit:

- focused replay/rotation/anchor cases: exit `0`;
- falsification inventory: 76/76, exit `0`;
- collaboration validator: exit `0`;
- encoding scan: exit `0`;
- domain-neutrality scan: exit `0`.

Codex is maker only. Independent Analista review remains mandatory.
