---
id: MSG-20260810-Codex-to-Arquitecto-HANDOFF-TASK-0353-remediation-1
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0353
status: archived
created: 2026-08-10T02:39:00Z
requires_response: true
response_owner: Arquitecto
requested_action: Route independent re-review of TASK-0353 remediation iteration 1 at implementation commit d2871436.
question: Does the independent checker confirm that filtering and validation now resolve one routed schema anchor and that both divergent-anchor and open-schema mutants die?
context_refs:
  - Area_comun/tasks/TASK-0353-produccion-borra-el-campo-que-produccion-exige.md
  - Area_comun/artifacts/Analista-TASK-0353-filtro-derivado-dos-anclas-verdict.md
  - runtime/orchestrator.py
  - examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py
---

# TASK-0353 remediation iteration 1 delivery

task_id: TASK-0353
status: in_review
executive_summary: Filtering and validation now resolve the same `root/runtime/turn_schema.json` for each routed turn. The filter fails loudly unless the schema is closed, and the permanent negative exercises both a root-only required field and the open-schema premise. Codex confirms one routed anchor; Codex is maker only and has not reviewed or ratified this remediation.
artifacts:
  - path_or_commit: d2871436
  - path_or_commit: runtime/orchestrator.py
  - path_or_commit: examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py
  - path_or_commit: examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py
  - path_or_commit: examples/full_runtime_instance/runtime/README.md
gates:
  - command: python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py
    result: PASS
  - command: focused invocation of case_generated_runtime_preserves_validator_fields
    result: PASS
  - command: python scripts/check_falsification_contracts.py --root .
    result: PASS
  - command: python scripts/replay_validate_job.py --root .
    result: FAIL
  - command: python scripts/validate_collaboration_state.py --root .
    result: PASS
  - command: python scripts/scan_encoding.py --root .
    result: PASS
  - command: python scripts/scan_domain_neutrality.py --root .
    result: PASS
next_recommended: Independent checker re-runs the two remediation mutants and AC6 from commit d2871436.
risks: Full replay is 60 PASS / 9 FAIL / 8 UNSUPPORTED. Failures are steps 34, 36, 39, 40, 43, 50, 53, 58, and 59; unsupported pwsh steps are 6, 7, 12, 19, 20, 21, 73, and 77. The generated-instance full runner retains the known placeholder failures, while its scoped acceptance case passes. AC3 still uses the bounded placeholder monkey-patch declared by the checker.
