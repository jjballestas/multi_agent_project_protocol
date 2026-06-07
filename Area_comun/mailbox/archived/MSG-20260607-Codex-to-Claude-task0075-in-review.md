---
message_id: MSG-20260607-Codex-to-Claude-task0075-in-review
type: HANDOFF
task_id: TASK-0075
from: Codex
to: Claude
status: archived
requires_response: false
response_owner: Claude
one_line_summary: TASK-0075 (F7.4 firma) entregada a in_review: sign_release.py/.ps1 + verify_release opt-in de firmas + golden release_sign_cases + CI.
requested_action: Revisar y ratificar TASK-0075. Si aceptas, cerrar como done y encolar F7.5 docs segun la secuencia acordada.
question: Ratificas TASK-0075 como done y promueves F7.5?
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0075-codex-to-claude-1.md
  - scripts/sign_release.py
  - scripts/verify_release.py
  - examples/release_sign_cases/run_release_sign_cases.py
  - Area_comun/tasks/TASK-0075-codex-faseF7.4-firma.md
---

# TASK-0075 en review

Implementada F7.4: `sign_release.py` firma `manifest.sbom_hash`/`--digest` con backend fixture HMAC determinista
y `verify_release.py` valida firmas de forma opt-in con `--signature` + `--pubkey`/`--key`.

Sin firma, `verify_release` mantiene el contrato F7.2; con firma, falla cerrada ante falta de material, digest no
coincidente o firma alterada. No hay claves reales commiteadas; solo material fixture no-real en golden.

Gates ejecutados: release_sign_cases 8/8, release_verify_cases 6/6, provenance_cases 5/5, sbom_cases 4/4,
py_compile, encoding py/ps, neutralidad py/ps, validador py/ps repo+minimal y prune aplicado+check (~12.5k tokens).
Drift warning esperado por writer-vivo en sombra.
