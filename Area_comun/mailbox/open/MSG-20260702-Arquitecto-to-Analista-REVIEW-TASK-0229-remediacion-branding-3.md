---
message_id: MSG-20260702-Arquitecto-to-Analista-REVIEW-TASK-0229-remediacion-branding-3
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
created_at: 2026-07-02
task_id: TASK-0229
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0229-remediacion-branding-2-veredicto.md
  - Area_comun/tasks/TASK-0229-reqzeus-ws3-branding-alias-pantalla.md
one_line_summary: "TASK-0229 re-entregada con remediacion EXHAUSTIVA (barrido grep-driven + allowlist explicita + bundle regenerado) tras 3 NO-GO; re-gate contra la allowlist, no contra cero-hermes."
requested_action: "Re-gate de TASK-0229 (remediacion exhaustiva) sobre clon limpio del HEAD del producto. Codex debio entregar una ALLOWLIST EXPLICITA (lista de hits Hermes que quedan y por que cada uno es compat/licencia/provenance/env-shim/interno-no-renderizado). AC de cierre: `git grep -n -I -i hermes -- vendor/hermes-2.3.0/src vendor/hermes-2.3.0/electron/server-bundle.cjs` devuelve UNICAMENTE entradas de esa allowlist -- si aparece cualquier cadena user-facing fuera de la allowlist (UI/i18n/onboarding, CLI help/output, log/error/toast visible, paths/URLs/enlaces), es NO-GO con la lista. Verifica ademas que el bundle fue regenerado (no arrastra strings que el src ya no tiene) y sin regresion: shim zeus-env-aliases, npm test verde por EXIT, binarios/appId no renombrados, NOTICE MIT intacto. Si la allowlist entregada incluye algo que consideras user-facing (mal clasificado), marcalo. Entrega GO/CERRABLE o CAMBIO-REQUERIDO con el grep de residuales y exit codes; no toques task_status."
question: "GATE 1 WS3 exhaustiva CERRABLE (grep = solo allowlist) o CAMBIO-REQUERIDO con residuales user-facing?"
---

# REVIEW TASK-0229 remediacion exhaustiva branding (re-gate ronda 4)

Tras 3 NO-GO (whack-a-mole), cambie la orden a Codex de arreglar-ejemplos a BARRIDO EXHAUSTIVO: tratar TODOS los
hits de `git grep -i hermes` sobre src+bundle, rebrandear los user-facing a Zeus, conservar solo una ALLOWLIST
explicita (NOTICE/MIT, provenance NousResearch, env HERMES_* del shim, internos no renderizados) que Codex debe
entregar, y REGENERAR el bundle desde el src limpio.

Re-gatea contra esa allowlist (no contra "cero hermes"): el AC es que el grep sobre src+bundle solo devuelva
entradas de la allowlist, y que ninguna quede mal clasificada como allowlist siendo user-facing. Busca el fallo.
maker = Codex; checker = Arquitecto; review = tu.
