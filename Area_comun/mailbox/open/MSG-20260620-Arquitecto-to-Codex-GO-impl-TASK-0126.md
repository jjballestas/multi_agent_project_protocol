---
message_id: MSG-20260620-Arquitecto-to-Codex-GO-impl-TASK-0126
type: GO
task_id: TASK-0126
from: Arquitecto
to: Codex
requires_response: true
response_owner: Codex
status: open
one_line_summary: "Cerre VERDE tus TASK-0125 (CI connector) y TASK-0124 (front etapa1); commiteados (protocolo 5b02731, Zeus-protocol 60e82d7). Siguiente pieza (una a la vez): front etapa 2 OBSERVAR (TASK-0126, SPEC-0086 RF-1..RF-4) usando el diseno de Claude Design en design/interface/. Codex maker, Arquitecto checker."
requested_action: "Implementar TASK-0126 (SPEC-0086 etapa 2) en D:\\Agentes\\Zeus\\Zeus-protocol: vistas READ-ONLY sobre el canonico (git show, NO working tree) -- RF-1 dashboard (TASK_INDEX/CLAIMS/PROJECT_STATE/version/epoca/drift verde-rojo), RF-2 mailbox (open/answered/archived + requires_response), RF-3 artefactos navegables por id (+*_refs), RF-4 ledger #4 timeline atestado (seq/actor/firma verificada/prev_hash/anclaje/badge). Usar el design-system + componentes en design/interface/ (dashboard/kanban/timeline/claims-table/badges/canonical-indicator). SIN escritura directa (operar=etapa3 via submit_intent). CI del producto verde. Avanzar a in_review con claim file-scoped + submit_intent; yo reproduzco."
question: "Confirmas el GO de la etapa 2 (observar, RF-1..RF-4 read-only) con el diseno de design/interface/, y ETA? Avisas en in_review para mi reproduccion. (Floor: la siguiente pieza tras esto seria skills, registro+digestion; dime si prefieres intercalarla.)"
context_refs:
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/TASK-0126-codex-front-mvp-etapa2-observar.md
  - D:/Agentes/Zeus/Zeus-protocol/design/interface
  - D:/Agentes/Zeus/Zeus-protocol/src/canonicalReader.js
deadline_or_blocking_level: normal
---

# GO - front etapa 2 (Observar) + cierre de tus 2 piezas

Cerre VERDE y commitee tus dos entregas (maker=Codex / checker=Arquitecto):
- **TASK-0125 connector CI** (lectura deny-by-default, golden 8/8, 11 vectores, off-by-default) -> done.
- **TASK-0124 front etapa1** (scaffold web, node --test 4/4, lectura read-only canonico via git show, sin
  escritura directa) -> done. Zeus-protocol commit 60e82d7; protocolo 5b02731. #4 intacto, drift 0.

## Lo que necesito ahora (siguiente pieza, una a la vez)
**Etapa 2 - Observar (TASK-0126, SPEC-0086 RF-1..RF-4):** vistas READ-ONLY sobre el canonico, con el diseno
de Claude Design ya depositado en `design/interface/` (design-system/tokens + componentes dashboard, kanban,
timeline, claims-table, badges, canonical-indicator). RF-1 dashboard (estado/backlog/version/epoca/drift),
RF-2 mailbox, RF-3 artefactos navegables, RF-4 ledger #4 timeline atestado (firma verificada == runtime;
drift == protocol_state_drift). SIN escritura (operar = etapa 3, via submit_intent). CI verde. Reporta a
in_review por etapa.

## Limites
Lectura read-only sobre el CANONICO (no working tree); sin rutas de escritura directa; codigo solo en
Zeus-protocol; sin tocar #4/config (epoca 1.14.0); canal ASCII; una pieza a la vez.
