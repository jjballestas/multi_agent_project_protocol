# TASK-0378 remediation iteration 2 blocked

- Commit `85ebb1f6` records TASK-0378 as `blocked`, publishes one concrete question to Arquitecto,
  and releases both Codex claims.
- The amended AC2 permits pre-commit to discriminate only by staged route class: PRODUCT staged
  requires an own active claim; no PRODUCT staged requires none.
- P-COORD H4 simultaneously requires a `scripts/` commit to pass without a claim, although
  `scripts/` is currently PRODUCT. Pre-commit cannot see `Task-Id: none` or `Ops-Reason`, so both
  requirements cannot hold without an explicit boundary decision.
- The unresolved question is whether `scripts/` remains PRODUCT (H4 must reject) or is excluded
  (H4 may accept). No product perimeter was weakened while awaiting Arquitecto.
- Collaboration and encoding gates exited 0; runtime drift was false through seq 9262. Codex is
  maker only and performed no review or ratification.
