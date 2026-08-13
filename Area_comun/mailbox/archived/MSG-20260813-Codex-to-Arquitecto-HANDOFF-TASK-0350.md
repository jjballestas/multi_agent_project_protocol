---
id: MSG-20260813-Codex-to-Arquitecto-HANDOFF-TASK-0350
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0350
status: archived
created: 2026-08-13T07:35:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0350 implementation 192c5dea is ready for independent review under amended AC5; the remaining generated-instance neutrality failure is pre-existing and owned by TASK-0367.
requested_action: Route commit 192c5dea for independent Analista review; do not treat the TASK-0367 residual as a TASK-0350 failure.
question: Can you route commit 192c5dea for independent Analista review under the amended AC5?
context_refs:
  - Area_comun/tasks/TASK-0350-el-port-del-motor-de-memoria-deja-marcadores-sin-resolver.md
  - Area_comun/tasks/TASK-0367-el-nucleo-neutral-trae-la-identidad-de-esta-instancia-cableada.md
  - scripts/new_instance.py
  - examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py
---

# HANDOFF -- TASK-0350

## Delivered implementation

Implementation commit: `192c5deabfef481b0f4db558da24afa679bfd2e9`.

The instantiator now recognizes only doubled-brace identifiers beginning with an uppercase letter:
`^[A-Z][A-Z0-9_]*$`. A doubled numeric regex quantifier such as `{{40}}` is product text, not an
instantiator-owned placeholder. The memory motor remains copied and executable in generated runtime
instances; neither its file nor its content is excluded.

## Acceptance evidence

- AC1: the criterion is identifier grammar, not a route or literal exception. Resolving the memory
  test as a template would assign product regex syntax to the instantiator; excluding the file or
  motor would remove executable product behavior to silence a false positive.
- AC2: the runner injects `{{PROJECT_NAME}}` into the generated instance. The dirty generation exits
  1 while the clean generation passes the placeholder gate: `clean_exit=0`, `dirty_exit=1`.
- AC3: `rf"[0-9a-f]{{128}}"` is moved to `product_regex.py`; it remains accepted without any path,
  line, or literal allowlist.
- AC4: the real generated-instance sets are exactly `before=[scripts/memory/test_memory_db.py]` and
  `after=[]`. The only removed hit is the false positive explained by the identifier criterion; no
  new hit appears. All 28 keys produced by `build_replacements` begin with an uppercase letter and
  remain inside the recognized grammar.
- AC5: the failure signature moved. Generation no longer aborts on
  `Unresolved placeholders remain in generated instance: scripts/memory/test_memory_db.py`; the run
  reaches later neutrality checks and reports the instance identity in `runtime/context.py`,
  `runtime/router.py`, `scripts/prune_state.py`, and, for runtime tier only,
  `scripts/harness/peer_mailbox_cron.ps1`. `git diff 192c5dea^ 192c5dea --name-only` contains only
  governed state/task materialization, `scripts/new_instance.py`, and the runtime-instantiation
  runner; none of those four residual source routes changed. The residual is therefore
  pre-existing relative to this implementation and is accepted by TASK-0367.
- AC6: the memory motor still travels in generated instances and remains executable there.

## Measured commands

- `python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py`: exit 1 only on
  the two later TASK-0367 neutrality cases; the placeholder evidence prints
  `before=[scripts/memory/test_memory_db.py]`, `after=[]`, `clean_exit=0`, `dirty_exit=1`.
- `python scripts/validate_collaboration_state.py --root .`: exit 0.
- `python scripts/scan_encoding.py --root .`: exit 0.
- `python scripts/scan_domain_neutrality.py --root .`: exit 0.

Codex is the maker and has not reviewed or ratified this work.
