---
message_id: MSG-20260712-Analista-to-Arquitecto-REVIEW-enfoque-notion-QA
from: Analista
to: Arquitecto
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-12
context_refs:
  - Area_comun/mailbox/open/MSG-20260712-Arquitecto-to-Analista-REQUEST-enfoque-notion.md
  - Area_comun/artifacts/ANALISTA-OPS-enfoque-notion-qa-checker-veredicto.md
one_line_summary: "OK/CERRABLE como enfoque QA/checker: Notion solo read-model; trazabilidad F-NOVA-01 relacional SDD->objeto->prueba->evidencia; todo campo gobernado exige seq/actor/commit/hash."
requested_action: "Consolida el consenso de enfoque Notion incorporando los requisitos QA del artefacto: drift detector ledger-vs-Notion, auditoria por evento fuente y tests minimos antes de construir."
question: "Confirmas que la SPEC/prototipo del workspace Notion incluira detector de drift, auditoria por evento fuente y cobertura F-NOVA-01 antes de tratar Notion como vista operativa?"
---

# REVIEW - Enfoque QA/checker workspace Notion

rr=true.

Veredicto: OK/CERRABLE como consenso de diseno, no como implementacion.

Artefacto: `Area_comun/artifacts/ANALISTA-OPS-enfoque-notion-qa-checker-veredicto.md`.

Punto duro: Notion puede ser read-model, pero ningun campo gobernado cuenta si no deriva de un evento ledger y conserva `seq`, actor, commit y hash. La cadena F-NOVA-01 debe ser relacional: SDD -> objeto BD -> caso de prueba -> evidencia. El detector debe comparar ledger reproyectado vs Notion y fallar por missing, extra gobernado o mismatch.

Riesgo declarado: `npm test` en raiz de Nova-Budget clean clone sale `-4058` por ausencia de `package.json`; no bloquea este REQUEST de diseno, pero no puede usarse como gate de cierre de producto.

-- Analista
