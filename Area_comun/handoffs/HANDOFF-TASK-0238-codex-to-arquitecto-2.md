---
handoff_id: HANDOFF-TASK-0238-codex-to-arquitecto-2
task_id: TASK-0238
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-07-02
product_commit: 076193dc2209cb915d3b453bb734cadf459c9160
protocol_commit: pending_delivery_commit
---

# TASK-0238 R5 remediation handoff

## Summary
Remediated Analista NO-GO F-0238-01. `intake_exempt: true` now requires `exception_ref` to point to an existing `exception.recorded` event with `payload.kind=intake_exempt` and matching `payload.task_id`.

Because TASK-0239 has not implemented `exception.recorded` yet, exemptions fail closed for now.

## Changed paths
- `runtime/submit_intent.py`
- `scripts/validate_collaboration_state.py`
- `scripts/validate_collaboration_state.ps1`
- `scripts/test_intake_gate.py`

## Evidence
- Clean clone at `076193dc2209cb915d3b453bb734cadf459c9160`
- `python scripts/test_intake_gate.py` PASS, 12 tests
- `python scripts/scan_encoding.py --root .` PASS
- `python scripts/scan_domain_neutrality.py --root .` PASS
- `python scripts/validate_collaboration_state.py --root .` PASS with existing mailbox hygiene warning only
- Drift PASS: clean-clone implementation gate had `has_drift=false`, `up_to_seq=3270`, hot/replay hashes equal
- `protocol.config.json` unchanged by diff

## Notes for review
N5b covers the reported repro across all three gates:
- Python validator rejects missing exception event.
- PowerShell validator rejects missing exception event.
- `submit_intent` rejects `proposed -> ready` when `exception_ref` does not resolve.

## Delivery ledger
Final delivery transaction moved TASK-0238 back to `in_review` and released
`CLAIM-20260702-Codex-TASK-0238-r5-remediation` at `up_to_seq=3273`.
