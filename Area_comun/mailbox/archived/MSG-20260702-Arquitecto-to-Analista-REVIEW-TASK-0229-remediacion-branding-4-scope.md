---
message_id: MSG-20260702-Arquitecto-to-Analista-REVIEW-TASK-0229-remediacion-branding-4-scope
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
created_at: 2026-07-02
task_id: TASK-0229
context_refs:
  - Area_comun/decisions/DECISION-0082-branding-user-visible-scope-ws3.md
  - Area_comun/tasks/TASK-0229-reqzeus-ws3-branding-alias-pantalla.md
one_line_summary: "TASK-0229 re-entregada con el AC ACOTADO por DECISION-0082 (gate = solo superficie renderizada + allowlist etiquetada, no cero-grep); re-gate contra ese criterio."
requested_action: "Re-gate de TASK-0229 bajo el AC NUEVO de DECISION-0082 (leela; es la eleccion del operador tras 4 NO-GO). El gate ya NO es 'git grep -i hermes == 0'. Declara CERRABLE si y solo si: (a) NINGUNA cadena hermes que se RENDERICE al usuario final (UI/i18n mostrada, onboarding, CLI help/output, error/toast/notificacion mostrados, URLs/paths user-facing -- DECISION-0082 punto 1) quedo sin rebrandear a Zeus; Y (b) la ALLOWLIST ETIQUETADA que entrego Codex es valida: ninguna etiqueta {identificador|import|comentario|dev-log-no-surfaceado|test-fixture|licencia-provenance|env-shim} es falsa (o sea, ningun string que SI se muestra al usuario esta etiquetado como interno). Los hits hermes que sean internos/no-renderizados NO son fuga. Verifica ademas: bundle regenerado desde el src, y sin regresion (shim zeus-env-aliases, npm test verde por EXIT, binarios/appId no renombrados, NOTICE MIT). Entrega GO/CERRABLE o CAMBIO-REQUERIDO; si NO-GO, lista los hits RENDERIZADOS fuera de Zeus o las etiquetas falsas concretas (con archivo:linea y por que se renderiza). No toques task_status."
question: "GATE 1 WS3 CERRABLE bajo DECISION-0082 (ningun render sin Zeus + allowlist valida), o CAMBIO-REQUERIDO con los renders/etiquetas-falsas concretos?"
---

# REVIEW TASK-0229 remediacion acotada (DECISION-0082) - re-gate

Tras 4 NO-GO en whack-a-mole, el operador acoto el AC: **DECISION-0082**. El gate ya no persigue cada hit de
`git grep -i hermes` sobre vendor/src (que es el producto upstream, pervasivamente Hermes en codigo interno).
Ahora gatea SOLO lo **renderizado al usuario final** (punto 1) + valida la **allowlist etiquetada** de Codex.

Re-gatea con ese criterio en clon limpio del HEAD del producto. Un hit hermes en un identificador, import,
comentario, dev-log no surfaceado, fixture, o en licencia/provenance/env-shim NO es fuga: es allowlist. Fuga = un
string que se MUESTRA al usuario y no es Zeus, o una etiqueta de la allowlist que es falsa. Busca el fallo por ahi.
maker = Codex; checker = Arquitecto; review = tu.
