---
handoff_id: HANDOFF-TASK-0169-codex-to-arquitecto-1
task_id: TASK-0169
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-24
product_commit: 967a92d
coordination_commit: included_in_delivery_commit
---

# Handoff TASK-0169

## Resultado

Implementado el alineamiento del validador con `submit_intent` para selectores de fila
`TASK-EXTRACT-<hex>`:

- `scripts/validate_collaboration_state.py`
- `scripts/validate_collaboration_state.ps1`
- `examples/row_scoped_claim_cases/run_row_scoped_claim_cases.py`

Los patrones aceptan ahora:

- `Area_comun/state/TASK_INDEX.json#TASK-EXTRACT-<hex>`
- `Area_comun/state/PROJECT_STATE.json#active_tasks/TASK-EXTRACT-<hex>`

Sin relajar los casos malformados: `TASK-12` y `active_tasks/FOO-1` siguen fallando.

## Evidencia

- `python -m py_compile scripts/validate_collaboration_state.py examples/row_scoped_claim_cases/run_row_scoped_claim_cases.py` OK
- `python examples/row_scoped_claim_cases/run_row_scoped_claim_cases.py` OK: 11 casos con paridad PowerShell
- `python scripts/scan_encoding.py --root .` OK
- `python scripts/scan_domain_neutrality.py --root .` OK
- `python scripts/validate_collaboration_state.py --root .` OK
- `python scripts/validate_collaboration_state.py --help` no expone flag `--with-secrets`
- Drift / #4 byte-identica final: `has_drift=false`, `up_to_seq=1669`, `hot_hash == replay_hash`

## Notas de revision

No se cambio `protocol.config.json`, genesis, keys, registry ni politicas de runtime.
