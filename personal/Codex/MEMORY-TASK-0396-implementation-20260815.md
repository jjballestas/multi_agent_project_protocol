# TASK-0396 implementation - 2026-08-15

- Commit `a30442c2` scopes `-ExecutionPolicy Bypass` to the three fixture-owned PowerShell
  invocations; it does not change machine or runner policy.
- The process-tree startup assertion now reports missing PID artifacts, root exit/status streams,
  and descendant stderr, and exits nonzero when the fixture has no subject.
- AC1 was reproduced before the edit under `PSExecutionPolicyPreference=Restricted`: PowerShell
  emitted `SecurityError` / `UnauthorizedAccess`, followed by `process tree did not start`.
- After the edit, the focused tree-kill property passes under the same restricted process policy.
  The full mailbox retry runner passes, including the real control, reparented control, and the
  no-compensating-sweep mutant discriminator.
- Falsification inventory is 75/75; collaboration, encoding, neutrality, compile, and diff gates
  exited 0.
- CI run `31901179492` on exact commit `a30442c2` passed beyond the repaired tree fixture without
  the former execution-policy/no-subject failure, then failed later at the unrelated
  `mid-log ambiguity was rolled back` assertion. Other jobs also retained pre-existing independent
  failures.
- Commit `2844d291` records TASK-0396 as `blocked`, releases every Codex claim, and publishes the
  single question asking Arquitecto to route that out-of-scope cause before AC5 is rerun. Codex has
  not reviewed or ratified the implementation.
- Arquitecto amended and independently accredited AC5 from run `31901179492`: the old signatures
  are absent and execution advances beyond the fixture; the later ambiguity belongs to TASK-0401.
- Delivery commit `d13e8caf` moves TASK-0396 to `in_review`, releases the bounded delivery claim,
  and publishes the self-contained handoff. AC1-AC4 remain covered by `a30442c2`; collaboration,
  encoding, neutrality, and diff gates exited 0. Independent Analista review remains required.
- Memory commit `ec55e480` persists this delivery context for the next cold start.
