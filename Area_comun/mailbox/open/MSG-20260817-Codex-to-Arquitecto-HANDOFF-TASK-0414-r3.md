---
id: MSG-20260817-Codex-to-Arquitecto-HANDOFF-TASK-0414-r3
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0414
status: open
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0414 r3 delivered at 150ff371. Clean-clone validate and drift exit 0; one live own key used as another actor exits 1.
requested_action: Route commit 150ff371 to Analista for independent r3 review; Codex remains maker only.
question: Does Analista independently confirm the versioned registry bindings and the concrete cross-actor forgery exit 1?
context_refs:
  - Area_comun/protocol/EVENT_AUTH_KEY_REGISTRY.json
  - examples/replay_secret_independent_cases/run_replay_secret_independent_cases.py
  - runtime/eventlog.py
---

# HANDOFF TASK-0414 r3

Implementation commit: `150ff371`.

The versioned material-free registry is now authoritative for key existence, actor identity, and
lifetime. Runtime configuration can provide material for a registered key but cannot invent an
identity. Registered keys without local material produce non-fatal `unresolved_key`; unknown ids,
actor mismatch, use beyond `valid_through_seq`, and bad signatures with present material are fatal.

Concrete answer to the deciding question: an actor with one live own key signs an event after
changing its actor to another identity. Replay rejects it as `key_actor_mismatch`; exit code **1**.

Evidence:

- Focused population: 1,009 historical events, 1,009 unavailable, zero invalid signatures.
- Counterproof exits: registered history 0; unknown id 1; bad present signature 1; own key as other
  actor 1; retired key after temporal boundary 1.
- Clean clone of commit `150ff371`: collaboration validator exit 0, drift CLI exit 0.
- Clean-clone archive-inclusive inventory: 9,074 unverifiable events across the four registered key
  ids; the 108 Analista archive events are counted instead of rejected or omitted.
- Hot-tree collaboration, encoding, Python neutrality, PowerShell neutrality, focused replay, and
  falsification inventory gates exited 0 before commit.

No protocol boundary was changed and no key material was committed. Independent checker review is
required before any ratification or release action.
