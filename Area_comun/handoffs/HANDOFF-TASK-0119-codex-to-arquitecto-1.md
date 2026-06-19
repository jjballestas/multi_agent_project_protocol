---
handoff_id: HANDOFF-TASK-0119-codex-to-arquitecto-1
task_id: TASK-0119
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-19T02:45:00Z
---

# TASK-0119 - Handoff Codex -> Arquitecto

## Summary

Guard de DECISION-0042 implementado: un `claim acquire` con scope de directorio bajo
`Area_comun/mailbox/` ahora falla con `mailbox claim must be file-scoped: <entry>`. Los archivos
`MSG-*.md` concretos siguen permitidos. El validador Python y PowerShell aplican el guard solo a claims
activos, por lo que no rompen claims historicos released.

## Changed

- `runtime/submit_intent.py`
- `scripts/validate_collaboration_state.py`
- `scripts/validate_collaboration_state.ps1`
- `examples/mailbox_claim_scope_cases/run_mailbox_claim_scope_cases.py`
- `.github/workflows/validate.yml`
- `CHANGELOG.md`
- `protocol.config.json`
- `Area_comun/tasks/TASK-0119-codex-guard-mailbox-claims.md`

## Verification

- OK: `python examples\mailbox_claim_scope_cases\run_mailbox_claim_scope_cases.py`
- OK: `python -m py_compile runtime\submit_intent.py scripts\validate_collaboration_state.py examples\mailbox_claim_scope_cases\run_mailbox_claim_scope_cases.py`
- OK with existing warning: `python scripts\validate_collaboration_state.py --root .`
- OK with existing warning: `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .`
- OK: `python scripts\scan_encoding.py --root .`
- OK: `python scripts\scan_domain_neutrality.py --root .`

## Review Notes

- `protocol.config.json` was bumped to `1.11.0` and `CHANGELOG.md` has the 1.11.0 entry.
- `PROJECT_STATE.version` remains `1.10.0` because `project_narrative.version` requires an orchestrator
  capability; Codex attempted no manual ledger edit under authoritative mode.
- The only validator warning observed is pre-existing mailbox hygiene:
  `MSG-20260619-Arquitecto-to-Operador-carril-A-promocion-done.md` does not require response.
