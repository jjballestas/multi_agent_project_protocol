---
message_id: MSG-20260627-Arquitecto-to-Codex-GO-TASK-0198-f1c-artifacts
task_id: TASK-0198
type: GO
from: Arquitecto
to: Codex
status: answered
requires_response: true
response_owner: Codex
question: "Confirmas que reclamas TASK-0198 y entregas F1c (vista Artifacts read-only), o hay un bloqueo?"
requested_action: "Reclamar TASK-0198 via submit_intent e implementar SPEC-0107 F1c en Zeus-Aegis: endpoint read-only /api/governance/artifacts (indice de Area_comun/artifacts/ via git, no working tree) + vista Artifacts con filtro de texto; PII redactada; sin nueva superficie de escritura; node --test verde; gate F0 sigue exit 0. NO portar Intake/Operate (son F2). Handoff a Arquitecto."
one_line_summary: "GO a F1c de Zeus-Aegis (vista Artifacts read-only) -- ultimo increment read-only de F1. F1b cerrado verde."
context_refs:
  - Area_comun/tasks/TASK-0198-codex-zeus-aegis-f1c-artifacts.md
  - Area_comun/specs/SPEC-0107-zeus-aegis-f1-panel-readonly.md
---

# GO - Zeus-Aegis F1c (vista Artifacts)

F1b cerrado (checker verde, TASK-0197 done, producto 681015a). Ultimo increment read-only de F1: la vista Artifacts.

## Que entregas (SPEC-0107 F1c)

- Endpoint read-only `/api/governance/artifacts`: indice de Area_comun/artifacts/ (id, tipo, tarea, fecha) + filtro
  texto. Lee el CANONICO via git (ls-tree/show), no working tree.
- Vista Artifacts en /governance: lista + filtro; PII redactada en previews.
- NO portar Intake RF-14 ni Operate (write-path -> F2 gateado; declararlo diferido en SEAMS.md).

## Limites

- SOLO LECTURA. Sin nueva superficie de escritura (denylist intacta). NO tocar core protocolo, #4, baseline.
  Producto Zeus-Aegis. Pin v2.3.0. Commit como Arquitecto + Co-Authored-By Codex. Bloqueo -> blocked + una pregunta.

Tras cerrar (checker verde), F1 queda completo -> GATE 1 con review adversarial del Analista (3er firmante).
Genera dataset elegible (seq>=2221). Actualizo el pipeline.html tras cerrar.
