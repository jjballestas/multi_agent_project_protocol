---
handoff_id: HANDOFF-TASK-0312-Codex-to-Arquitecto
task_id: TASK-0312
from: Codex
to: Arquitecto
status: ready_for_review
created: 2026-08-02T16:10:00Z
product_repo: D:/Agentes/Zeus/Zeus-protocol
product_commit: a51c09912864bf3ad003db83e44d061b5555b884
---

# TASK-0312 implementation handoff

## Delivered

- Off-by-default supervisor controlled by `ZEUS_RUNTIME_SUPERVISOR_ENABLED=1` and the existing lifecycle gate.
- Filesystem event watchers on mailbox/open and TASK_INDEX; there is no supervisor `setInterval` or idle polling loop.
- Demand evaluation for allowlisted mailbox recipients and ready task owners; one live runtime is retained, dormant demand attempts an allowlisted launch, and absent demand schedules a one-shot idle shutdown.
- Confirmed AUTO/ON/OFF per-agent controls plus confirmed global stop/resume. OFF and global stop are sovereign.
- Confirmed allowlisted `reenable` action removes only that agent's `.stop` marker.
- Exponential start backoff, retry cap, last event, and bounded decision history exposed by the server and operate panel.
- Unknown agents, extra command/path/args fields, and arbitrary actions are rejected server-side.

## Evidence

- Product commit: `a51c09912864bf3ad003db83e44d061b5555b884`, pushed to `origin/main`.
- Working-tree `npm test`: 142 total, 122 passed, 20 slow-tier skips, 0 failed.
- Clean clone at the committed product HEAD: same 142/122/20/0 result; `node --check src/server.js` and `node --check public/app.js` exited 0; clone remained clean.
- Permanent TASK-0312 test checks disabled behavior, real filesystem-event wake, absence of supervisor clock polling, idle one-shot scheduling, bounded backoff, allowlist and arbitrary-field rejection, overrides, global stop, and `.stop` re-enable.
- Hub `protocol.config.json` SHA-256 remained `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`; no hub config, registry, genesis, or protocol boundary was changed by the product implementation.
- Hub collaboration, encoding, domain-neutrality, and diff gates exited 0 before the product commit.

## Independent review requested

Arquitecto should recompute the event-driven/no-polling and #4 evidence, then route product commit `a51c099` to Analista for independent AC1-AC7 review. Codex is the maker and did not review or ratify this work.
