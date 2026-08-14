# TASK-0368 remediation r5

- Maker: Codex.
- Implementation commit: `f50ecff3`.
- `decision_policy_state` now preserves the attested disjunction when `status` is missing:
  a non-empty `superseded_by` still classifies the decision as `superseded`; otherwise the
  declared `missing_status: current_with_warning` behavior remains `active`.
- The permanent runner adds the checker-specified fixture with `superseded_by` and no `status`,
  and asserts the production row is `superseded`.
- All six TASK-0368 gates exited 0 before the implementation commit and twice consecutively on
  exact HEAD `ecc1478e`.
- Delivery commit `28077691` moves TASK-0368 to `in_review`, releases both r5 maker claims, and
  publishes the self-contained Arquitecto handoff for independent Analista re-review.
- Codex is maker only and did not review or ratify the change.
