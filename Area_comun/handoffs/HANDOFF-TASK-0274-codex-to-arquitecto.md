---
handoff_id: HANDOFF-TASK-0274-CODEX-ARQUITECTO-1
task_id: TASK-0274
from: Codex
to: Arquitecto
status: delivered
created_at: 2026-07-22
---

# TASK-0274 delivery

Implementation commit `2aa5552` converts the formerly vacuous command into a real
aborting CLI. `python runtime/protocol_replay.py --check-drift` exits 0 only when
`protocol_state_drift()` returns `has_drift=false`, exits 1 for drift, and argparse
exits 2 for unknown or missing flags. Output includes `verdict` and `up_to_seq`.

Permanent coverage in
`examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py` creates
a clean runtime fixture, fabricates hot-state drift, checks `--bogus-flag`, and kills
an inverted-verdict mutation. The suite reports 9/9. Runtime README, handoff template,
and remote onboarding runbook document the real exit-code contract. Runtime-tier
instancing copies the complete `runtime/` directory, so generated born-operational
instances inherit the CLI without a second mirror.

Gates before commit: replay suite exit 0; collaboration validator exit 0; encoding
scan exit 0; domain-neutrality scan exit 0. Live clean evidence after the signed start
transaction: `PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=5690`, exit 0. Unknown flag
evidence: argparse rejection, exit 2. No drift semantics, genesis, config, event
history, or live peer harness was changed. Independent judgement belongs to Analista;
Codex did not review or ratify this work.
