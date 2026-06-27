---
message_id: MSG-20260627-Arquitecto-to-Codex-GO-TASK-0197-f1b-views
task_id: TASK-0197
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: true
response_owner: Codex
question: "Confirmas que reclamas TASK-0197 y entregas F1b (vistas Decisiones/Ledger/Handoffs read-only), o hay un bloqueo?"
requested_action: "Reclamar TASK-0197 via submit_intent e implementar SPEC-0107 F1b en Zeus-Aegis: endpoints read-only /api/governance/{decisions,handoffs,ledger} (lee canonico via git show) + vistas Decisiones, Ledger/atestacion (timeline con method+actor por evento, chip atestado DERIVADO de la verificacion real) y Handoffs; PII redactada; prueba negativa de no-escritura; node --test verde; gate F0 sigue exit 0. Handoff a Arquitecto."
one_line_summary: "GO a F1b de Zeus-Aegis (vistas Decisiones/Ledger/Handoffs, read-only). F1a cerrado verde."
context_refs:
  - Area_comun/tasks/TASK-0197-codex-zeus-aegis-f1b-views.md
  - Area_comun/specs/SPEC-0107-zeus-aegis-f1-panel-readonly.md
---

# GO - Zeus-Aegis F1b (Decisiones / Ledger / Handoffs)

F1a cerrado (checker verde, TASK-0196 done, producto 75273cb). Siguiente increment: las 3 vistas restantes de F1.

## Que entregas (SPEC-0107 F1b)

- Endpoints read-only `/api/governance/{decisions,handoffs,ledger}` (lee CANONICO via git show, no working tree).
- Vista Decisiones (indice), Vista Handoffs (indice), Vista Ledger/atestacion (timeline): por evento muestra el
  method de firma (hmac/ed25519/not_enforced) + actor; el chip "atestado" se **DERIVA de validate_chain/firmas
  reales** (tri-estado, fail-safe no-verde, NUNCA hardcoded). PII redactada en payloads.

## Limites

- SOLO LECTURA (F2 sigue gateado post-TFM). Sin nueva superficie de escritura (la denylist debe seguir cubriendo
  submit_intent/state). NO tocar core protocolo, #4, baseline. Producto Zeus-Aegis. Pin v2.3.0.
- Commit como Arquitecto con Co-Authored-By Codex. Minimal narration. Bloqueo -> blocked + una pregunta.

Esto genera dataset elegible (seq>=2221). Tras cerrar (checker verde) actualizo el pipeline.html (control).
