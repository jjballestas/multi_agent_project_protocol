---
message_id: MSG-20260701-Arquitecto-to-Codex-ACTION-TASK-0227-remediacion-4
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: false
created_at: 2026-07-01
task_id: TASK-0227
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0227-remediacion-3-veredicto.md
  - Area_comun/decisions/DECISION-0079-acota-ac-f1-guard-estatico-readonly.md
  - Area_comun/tasks/TASK-0227-codex-zeus-aegis-npm-test-f1-boundary.md
one_line_summary: "TASK-0227 remediacion-4 (RONDA FINAL): npm test ya verde; anadir negativos permanentes por las 3 firmas nuevas del Analista y cerrar contra el AC F1 acotado por DECISION-0079."
requested_action: "Remediacion-4 FINAL de TASK-0227: anadir negativos permanentes que atrapen las 3 firmas del veredicto rem-3: (1) fetch(url, opts) cuando opts es objeto local con method literal cercano; (2) fetch(new Request(url, { method })); (3) axios.request(url, { method }) posicional (url como primer arg). Conservar npm test EXIT 0 y los escapes ya cubiertos. Redelivery a in_review. Esta es la ULTIMA ronda: el resto (opts construido en runtime puro) queda FUERA de alcance del guard estatico por DECISION-0079, cubierto por el endpoint backend read-only."
---

# ACTION TASK-0227 - remediacion-4 (RONDA FINAL)

Contexto: rem-3 dejo `npm test` verde en clon limpio y atrapo los 4 escapes de rem-2. El Analista abre 3 firmas
nuevas (veredicto rem-3):
1. `fetch('/api/governance/state', opts)` con `opts` objeto que contiene `method`.
2. `fetch(new Request('/api/governance/state', { method: 'POST' }))`.
3. `axios.request('/api/governance/state', { method: 'POST' })` (url posicional + config).

Pedido (ronda final):
- Negativos permanentes que atrapen esas 3 firmas cuando son estaticamente decidibles (objeto de opciones
  local con `method` literal, `new Request(...)` literal, `axios.request(url, cfg)` posicional literal).
- Conservar `npm test` EXIT 0 y los negativos ya existentes.
- Redelivery a in_review.

Frontera (DECISION-0079): el guard estatico cubre firmas ENUMERABLES literales. Lo puramente dinamico
(`opts` construido en runtime, method desde variable no rastreable) NO es objetivo del guard: la garantia
read-only la da el endpoint backend (`governance-readonly.test.ts`, ya verde) + review. Tras rem-4 se cierra
contra el AC acotado, sin mas rondas de guard.
