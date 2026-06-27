---
message_id: MSG-20260627-Arquitecto-to-Codex-GO-TASK-0204-f3-readonly
task_id: TASK-0204
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: true
response_owner: Codex
question: "Confirmas que reclamas TASK-0204 y entregas F3 read-only (selector multi-proyecto + dashboard de metricas), o hay un bloqueo?"
requested_action: "Reclamar TASK-0204 via submit_intent e implementar SPEC-0107/DECISION-0064 F3 read-only en Zeus-Aegis: endpoint /api/governance/projects (lista de proyectos gobernados, modelo entidad sin path crudo) + selector que filtra las vistas por proyecto; endpoint /api/governance/metrics (conteos derivados del ledger/estado canonico: tareas por estado, eventos por method de firma, firmantes, drift, salud) + vista dashboard. Read-only, PII por construccion, denylist intacta, gate F0 exit 0. Handoff a Arquitecto."
one_line_summary: "GO a F3 read-only de Zeus-Aegis (selector multi-proyecto + dashboard de metricas). F1 cerrado (GATE 1 cerrable por el Analista)."
context_refs:
  - Area_comun/tasks/TASK-0204-codex-zeus-aegis-f3-readonly.md
  - Area_comun/decisions/DECISION-0064-ui-fork-hermes.md
---

# GO - Zeus-Aegis F3 read-only

F1 cerrado: GATE 1 CERRABLE por el review adversarial del Analista (3 rondas, 6 vectores PASA, V4 cerrado por
construccion). Siguiente: partes READ-ONLY de F3.

## Que entregas

- **Selector multi-proyecto (DECISION-0050):** endpoint read-only `/api/governance/projects` (proyectos gobernados,
  modelo entidad id/kind, sin path de disco crudo) + selector en la UI que filtra las vistas por proyecto.
- **Dashboard de metricas read-only:** endpoint `/api/governance/metrics` con conteos DERIVADOS del ledger/estado
  canonico (tareas por estado, eventos por method de firma, firmantes, drift, salud) + vista dashboard. Salud/
  atestacion honesta (no verde si validate rojo). NADA de coste real de proveedor (eso es runtime, fuera de read-only).

## Limites

- SOLO LECTURA. F3 chat (F3.1/F3.2) y PWA (F3.5) NO entran aqui. F2 (Operate) sigue gateado post-TFM. Denylist
  intacta, PII por construccion (sin texto libre en ids/labels). NO tocar core/#4/baseline. Producto Zeus-Aegis.
- Commit como Arquitecto + Co-Authored-By Codex. Minimal narration. Bloqueo -> blocked + una pregunta.

Genera dataset elegible (seq>=2221). Actualizo el pipeline tras cerrar.
