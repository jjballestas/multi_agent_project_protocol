---
handoff_id: HANDOFF-TASK-0105-codex-to-claude-1
task_id: TASK-0105
from: Codex
to: Claude
status: in_review
created_at: 2026-06-13T12:15:00Z
---

# HANDOFF TASK-0105 - Slim-views cold-start

## Summary

Implemented SPEC-0077 slim-views as derived, off-by-default runtime artifacts:

- `runtime/protocol_replay.py`
  - Added `SLIM_VIEW_PATHS`, `HOT_TASK_STATUSES`, `slim_views_enabled`.
  - Added `build_slim_views(snapshot_or_state, config)` for:
    - `Area_comun/state/TASK_INDEX.slim.json`
    - `Area_comun/state/PROJECT_STATE.slim.json`
    - `Area_comun/state/CLAIMS.slim.json`
  - Extended `materialize_to_disk` so slim-views join the same staged/backup/replace batch when `event_state.slim_views_enabled=true`.
  - Added `slim_view_drift(root)` and integrated its entries into `protocol_state_drift(root)` under the flag.
- `protocol.config.json` and `protocol.config.template.json`
  - Added `event_state.slim_views_enabled: false`.
- Added neutral masters:
  - `Area_comun/state/TASK_INDEX.slim.template.json`
  - `Area_comun/state/PROJECT_STATE.slim.template.json`
  - `Area_comun/state/CLAIMS.slim.template.json`
- Extended context measurement:
  - `scripts/measure_context_cost.py`
  - `scripts/measure_context_cost.ps1`
- Added golden suite:
  - `examples/slim_view_cases/run_tests.py`

## Measurement

Command:

```powershell
python scripts\measure_context_cost.py --root . --json
```

Result, canonical Python measurement:

- Full cold-start: `17,225` tokens.
- Slim cold-start estimate: `9,232` tokens.
- Delta: `7,993` tokens saved.
- Target check: `slim_within_target=true`.

Post-hygiene open mailbox contains only:

- `MSG-20260613-Operador-GO-DECISION-0014-0030.md`: `852` tokens.

I archived the executed TASK-0105 GO message after the handoff-release. I still did not promote live `coldstart_globs`; GC-7 verifies the promoted shape in a fixture, and the actual config flip can be done as the gated follow-up once Claude ratifies the implementation.

## Verification

```powershell
python -m py_compile runtime\protocol_replay.py scripts\measure_context_cost.py examples\slim_view_cases\run_tests.py
python examples\slim_view_cases\run_tests.py
python scripts\validate_collaboration_state.py --root .
python -c "from pathlib import Path; from runtime.protocol_replay import protocol_state_drift; import json; print(json.dumps(protocol_state_drift(Path('.')), indent=2, ensure_ascii=False))"
powershell -ExecutionPolicy Bypass -File scripts\measure_context_cost.ps1 -Root . -Budget
```

Observed:

- `examples/slim_view_cases`: `7/7` passed.
- Validator: `OK: collaboration state is valid.`
- Runtime drift: `has_drift=false`, `up_to_seq=375` before the handoff measurement correction claim.
- PowerShell measurement reports the same full mode and a slim delta; its virtual JSON formatting is more verbose (`9,741` slim tokens), still below the 10k target. The canonical Python number above is the handoff measurement.

## Notes For Review

- `slim_views_enabled` remains `false` in both live and template config.
- No live `*.slim.json` files are materialized while the flag is off.
- GC-3 manipulates a slim file and verifies both `slim_view_drift` and the `submit_intent.py` CLI abort path.
- GC-7 verifies the promoted-globs shape in a fixture only; live `coldstart_globs` are intentionally unchanged pending the measured gate.
