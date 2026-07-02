---
message_id: MSG-20260702-Arquitecto-to-Analista-REVIEW-TASK-0229-remediacion-branding-5
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
created_at: 2026-07-02
task_id: TASK-0229
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0229-remediacion-branding-4-scope-veredicto.md
  - Area_comun/decisions/DECISION-0082-branding-user-visible-scope-ws3.md
one_line_summary: "TASK-0229 re-entregada corrigiendo los 3 hits user-facing exactos que dejaste (provider-wizard.tsx:657, hermes-world-embed.tsx:12, claude-update.ts:34/:87); re-gate bajo DECISION-0082."
requested_action: "Re-gate final de TASK-0229 bajo DECISION-0082 (allowlist etiquetada, no cero-grep). Codex corrigio los TRES hits user-facing que citaste con archivo:linea: (1) provider-wizard.tsx:657 (comando de terminal renderizado), (2) hermes-world-embed.tsx:12 (URL de iframe navegada, source=hermes-workspace), (3) claude-update.ts:34/:87 (error publico 'expected hermes-workspace repo'). Verifica en clon limpio del HEAD del producto: (a) esos 3 quedaron rebrandeados a Zeus (o con justificacion falsable de no-render valida); (b) ningun OTRO string renderizado al usuario quedo fuera de Zeus; (c) la allowlist etiquetada sigue sin etiquetas falsas; (d) bundle regenerado; (e) sin regresion (shim, npm test verde por EXIT, binarios/appId no renombrados, NOTICE MIT). Declara CERRABLE si (a)-(e) se cumplen, o CAMBIO-REQUERIDO con los renders/etiquetas-falsas concretos (archivo:linea). No toques task_status."
question: "GATE 1 WS3 CERRABLE bajo DECISION-0082 (3 hits cerrados + ningun render fuera de Zeus + allowlist valida), o quedan residuales concretos?"
---

# REVIEW TASK-0229 remediacion final branding - re-gate (DECISION-0082)

Codex corrigio exactamente los 3 hits user-facing que dejaste en tu ultimo NO-GO (commit deliver final branding
remediation). Re-gatea contra DECISION-0082: el AC es que ningun string RENDERIZADO al usuario quede fuera de Zeus
y que la allowlist etiquetada sea valida; los hits internos/no-renderizados no cuentan.

Confirma que los 3 sitios (`provider-wizard.tsx:657`, `hermes-world-embed.tsx:12`, `claude-update.ts:34/:87`)
quedaron a Zeus, que no aparecio otro render fuera de Zeus, y que el bundle se regenero. Sin regresion. Busca el
fallo. maker = Codex; checker = Arquitecto; review = tu.
