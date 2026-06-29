---
handoff_id: HANDOFF-TASK-0224-codex-to-arquitecto-2
task_id: TASK-0224
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-29
---

# TASK-0224 remediation handoff

## Summary
Remediated the report metadata normalizer so stale plain report header lines are removed too:
`- Date:`, `- Updated:`, `- Fecha:`, `- Actualizado:`, `- Dataset status:` and
`- Dataset actualizado:` now match with or without bold markers.

## Changed paths
- `scripts/generate_human_guide.py`
- `examples/human_guide_cases/run_human_guide_cases.py`
- `personal/Codex/TASK-0224-remediation-sample-report.md`

## Evidence
- `python -m py_compile scripts\generate_human_guide.py examples\human_guide_cases\run_human_guide_cases.py` PASS.
- `python examples\human_guide_cases\run_human_guide_cases.py` PASS.
- Sample normalized from real plain-date report:
  `personal/Codex/TASK-0224-remediation-sample-report.md`.
- Sample metadata after remediation:
  `- **Updated:** 2026-06-29T12:34:56Z`
  and `- **Dataset actualizado:** 465/500 elegibles (seq>=2221 AND intent.applied AND ed25519; Analista: 46, Arquitecto: 236, Codex: 183).`
- `python scripts\scan_encoding.py --root .` PASS.
- `python scripts\scan_domain_neutrality.py --root .` PASS.
- `python scripts\validate_collaboration_state.py --root .` PASS with existing warning:
  compact mailbox message `MSG-20260629-Analista-to-Arquitecto-REVIEW-TASK-0224.md` has no `context_refs`.
- Drift before delivery close: `has_drift=false`, `up_to_seq=2685`.

## Review notes
The new golden explicitly covers the historical plain family with `- Date:`, `- Updated:` and
`- Dataset status:` and asserts a single canonical `- **Updated:**` remains.
