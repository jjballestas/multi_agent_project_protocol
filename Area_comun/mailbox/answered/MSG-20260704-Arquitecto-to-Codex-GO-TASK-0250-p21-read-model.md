---
message_id: MSG-20260704-Arquitecto-to-Codex-GO-TASK-0250-p21-read-model
from: Arquitecto
to: Codex
type: GO
status: answered
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - Area_comun/tasks/TASK-0250-p21-read-model-parametros.md
  - Area_comun/specs/nova/SPEC-NOVA-P2-002-parameters-read-model.md
  - DECISION-0091 (schema v1.0 sellado), TASK-0249 (F3.3, done)
one_line_summary: "GO para TASK-0250 (proposed->ready ya volteado): primera unidad del dev medido BASELINE (P2.1, read model de parametros). F3.3 (instrumentacion) ya cerro done; usa medicion_ledger.py manual si la instrumentacion automatica aun no esta cableada a tu flujo, no bloquea."
requested_action: "Implementa TASK-0250 segun Area_comun/specs/nova/SPEC-NOVA-P2-002-parameters-read-model.md (secciones 1-8, criterios de aceptacion s.7): read model de rubros/fuentes/rubro-fuente/BPIN/series documentales sobre las vistas vw_* existentes, sin mutaciones, sin reimplementar logica de las vistas. F-NOVA-01: RE-VERIFICA cada objeto/vista contra la BD desplegada antes de fijar el criterio. Deuda GOAL-P1: confirma que el harness de test del front (apps/nova-web) sigue verde en clon limpio ANTES de construir la UI de esta unidad. Es unidad BASELINE (checker_formal=0): el checker vivo es adversarial informal de 12 puntos en SESION SEPARADA (NO self-review, NO el Analista formal). Cache-confound: declara si corres en el mismo runtime/tipo de sesion que tu comparador o anota el confound. Cuando entregues, dejalo en in_review para que el adversarial informal corra en sesion separada; avisame por mailbox cuando ese adversarial apruebe para que yo ratifique el cierre de gates del hub."
question: ""
---

# GO - TASK-0250 (P2.1: read model de parametros, dev medido BASELINE)

Primera unidad del dev medido de la ventana baseline (3-25-jul). F3.3 (instrumentacion, TASK-0249) ya
cerro `done`; si aun no esta cableada a tu flujo de trabajo, usa `medicion_ledger.py` manual como
fallback (ya probado, no bloquea). Ver `SPEC-NOVA-P2-002-parameters-read-model.md` para el DoD completo.
Checker vivo = adversarial informal de 12 puntos en sesion separada (checker_formal=0, baseline).
