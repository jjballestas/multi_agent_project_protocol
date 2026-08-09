# HANDOFF TASK-0343 REMEDIATION 1

Maker: Codex
Implementation commit: `4cded4c4`

## Delivered behavior

- The exercised rollback path recognizes the conservative `ROLLBACK_DEFER` event class rather than
  two reason literals.
- The permanent property independently rejects event loss, claim change, and an empty prestate.
- mp4 (claims comparison removed) exits 1; mp5 (non-vacuity removed) exits 1; mp6 (production defer
  reason renamed with the same effect) leaves the complete runner at exit 0.
- Production rollback code is unchanged. TASK-0341 remains the partition for dead negative
  invocation. The host-absolute `csc.exe` invocation remains declared residual R5.

## Verification

- Base mailbox retry runner: exit 0.
- Falsification inventory: 69/69.
- Collaboration, encoding, neutrality, drift, compile, and diff gates: exit 0.
- Exact `4cded4c4` passed those gates in a detached clean clone with empty status.
- Actions run 31310469089: `falsification-runners` success and `Execute mailbox retry falsification
  runner` success on exact head `4cded4c4`.
- The unrelated overall red is `Run runtime concurrency simulation cases`, already contracted as
  TASK-0347 for the missing `obstacles` block.

Independent Analista re-review is required. Codex did not review or ratify its own work.
