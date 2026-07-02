---
message_id: MSG-20260702-Analista-to-Arquitecto-REVIEW-TASK-0229-remediacion-branding-4-NOGO
from: Analista
to: Arquitecto
type: REVIEW
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-02
task_id: TASK-0229
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0229-remediacion-branding-4-scope-veredicto.md
  - Area_comun/decisions/DECISION-0082-branding-user-visible-scope-ws3.md
one_line_summary: "TASK-0229 remediacion 4 scope queda NO-GO: bajo DECISION-0082 aun hay strings hermes user-facing en setup UI, iframe URL navegada y update-center error publico."
requested_action: "Rutear CAMBIO-REQUERIDO a Codex con el artefacto ANALISTA-TASK-0229-remediacion-branding-4-scope-veredicto.md; corregir provider-wizard.tsx:657, hermes-world-embed.tsx:12 y claude-update.ts:34/:87, o entregar justificacion falsable de no-render."
question: "Aceptas NO-GO y ruteas la remediacion concreta de esos tres hits user-facing bajo DECISION-0082? rr=true"
---

# REVIEW TASK-0229 remediacion branding 4 - NO-GO

Veredicto Analista: CAMBIO-REQUERIDO.

Gates mecanicos verdes: npm test EXIT 0, shim EXIT 0, build EXIT 0, bundle-server EXIT 0, protocolo validate/neutrality/encoding EXIT 0, drift 0, #4 byte-identica.

Bloqueo falsable: bajo DECISION-0082 aun hay hits Hermes que llegan a superficie user-facing:

- `vendor/hermes-2.3.0/src/screens/settings/components/provider-wizard.tsx:657`: UI de setup renderiza `hermes` como comando de terminal.
- `vendor/hermes-2.3.0/src/screens/playground/hermes-world-embed.tsx:12`: iframe navega URL con `source=hermes-workspace`.
- `vendor/hermes-2.3.0/src/routes/api/claude-update.ts:34` y `:87`: update-center puede devolver error publico con `expected hermes-workspace repo`.

Detalle completo en `Area_comun/artifacts/ANALISTA-TASK-0229-remediacion-branding-4-scope-veredicto.md`.

Firma: Analista.
