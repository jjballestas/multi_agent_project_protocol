# TASK-0368 remediation r4

- Maker: Codex.
- Implementation commit: `95584c3a`.
- Decision status is normalized exactly once at the decision-load boundary, after raw PII
  validation and before storage in metadata. The vocabulary gate and policy classifier consume
  that same stored value without further normalization.
- The behavioral fixture proves `Proposed` is classified exactly like `proposed` without adding a
  case variant to the attested allowlist.
- The falsification inventory replaces the tautological set inequality with two direct assertions
  over `DECISION-OLD` in the production and pointer-mutant populations.
- All six TASK-0368 gates exited 0 before the implementation commit. Independent review remains
  required; Codex did not review or ratify the change.
