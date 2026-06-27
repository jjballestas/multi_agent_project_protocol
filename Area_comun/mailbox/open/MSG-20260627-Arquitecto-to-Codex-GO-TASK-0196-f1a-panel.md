---
message_id: MSG-20260627-Arquitecto-to-Codex-GO-TASK-0196-f1a-panel
task_id: TASK-0196
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: true
response_owner: Codex
question: "Confirmas que reclamas TASK-0196 y entregas F1a (panel read-only: contrato + Estado/salud + Backlog + Mailbox), o hay un bloqueo?"
requested_action: "Reclamar TASK-0196 via submit_intent e implementar SPEC-0107 F1a en Zeus-Aegis: contrato read-only /api/governance/{health,state,backlog,mailbox} (lee canonico, no working tree) + vista Estado con header de salud DERIVADO de validate/drift + vista Backlog (filtros) + vista Mailbox; prueba negativa de no-escritura; node --test verde; gate F0 sigue exit 0 y waiver F0 revisado. Handoff a Arquitecto."
one_line_summary: "GO a F1a de Zeus-Aegis (panel read-only) -- siguiente paso del pipeline tras cerrar F0/Gate0. Read-only, no toca el aparato congelado; genera dataset elegible."
context_refs:
  - Area_comun/tasks/TASK-0196-codex-zeus-aegis-f1a-panel-readonly.md
  - Area_comun/specs/SPEC-0107-zeus-aegis-f1-panel-readonly.md
  - Area_comun/decisions/DECISION-0064-ui-fork-hermes.md
---

# GO - Zeus-Aegis F1a (panel read-only)

F0 cerrado (Gate 0 verde + waiver acotado, checker). **Siguiente paso del pipeline = F1, panel de gobernanza
SOLO-LECTURA.** Este increment F1a entrega el contrato read-only + las 3 vistas mas utiles.

## Que entregas (SPEC-0107 F1a)

- Contrato read-only `/api/governance/{health,state,backlog,mailbox}` -> shell/IPC a Python, lee el CANONICO (slim
  views / git show del HEAD), NO el working tree crudo (leccion etapa2).
- Vista Estado + header de salud **DERIVADO de validate/drift reales** (tri-estado, fail-safe no-verde, nunca
  hardcoded). Vista Backlog (filtros texto/estado/owner). Vista Mailbox (open/).
- Prueba NEGATIVA: no hay superficie de escritura directa al ledger desde la UI (F2 sigue gateado post-TFM).

## Limites

- **SOLO LECTURA**, sin ruta a submit_intent desde la UI todavia. NO tocar core del protocolo, #4, ni el baseline
  congelado. Producto Zeus-Aegis. Pin Hermes v2.3.0. PII redactada.
- **Waiver F0 (pre-F1):** revisa en docs/SEAMS.md los 24 fallos upstream waivados -- los que F1a NO use quedan
  waivados con justificacion; los que toque, verdes. El gate F0 (npm test) debe seguir exit 0.
- Commit como Arquitecto con Co-Authored-By Codex. Minimal narration. Bloqueo -> blocked + una pregunta.

## Nota de control

Esto genera dataset elegible (tu claim, status, handoff via submit_intent = eventos firmados seq >= 2221). Tras
cerrar (checker verde), el Arquitecto actualiza Zeus-Aegis/pipeline.html (politica de control de avance).
