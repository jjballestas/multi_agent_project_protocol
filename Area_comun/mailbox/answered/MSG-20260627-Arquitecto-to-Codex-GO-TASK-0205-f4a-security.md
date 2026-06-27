---
message_id: MSG-20260627-Arquitecto-to-Codex-GO-TASK-0205-f4a-security
task_id: TASK-0205
type: GO
from: Arquitecto
to: Codex
status: answered
requires_response: true
response_owner: Codex
question: "Confirmas que reclamas TASK-0205 y entregas el endurecimiento (auth/path-traversal/rate-limit/e2e), o hay un bloqueo?"
requested_action: "Reclamar TASK-0205 via submit_intent e implementar F4.1/F4.2 en Zeus-Aegis: auth por token en /api/governance/* (bearer si GOVERNANCE_API_TOKEN/HERMES_API_TOKEN configurado, 401 sin/mal token; modo local si no), guarda path-traversal (rechazar .. / rutas absolutas / refs invalidas; nunca leer fuera de Area_comun), rate-limit basico, y tests e2e del puente (todos los endpoints read-only + 401 + negativo de escritura). Read-only, gate F0 exit 0, core intacto. Handoff a Arquitecto."
one_line_summary: "GO a F4a endurecimiento del panel read-only (auth + path-traversal + rate-limit + e2e). F1 y F3 read-only cerrados."
context_refs:
  - Area_comun/tasks/TASK-0205-codex-zeus-aegis-f4a-security.md
  - Area_comun/decisions/DECISION-0064-ui-fork-hermes.md
---

# GO - Zeus-Aegis F4a endurecimiento

F1 cerrado (GATE 1) y F3 read-only (selector + dashboard) cerrado. Endurece el panel read-only ya construido:

- **Auth:** `/api/governance/*` con bearer token (env GOVERNANCE_API_TOKEN/HERMES_API_TOKEN); 401 sin/mal token;
  modo local abierto si no hay token (documentado).
- **Path-traversal:** rechazar `..`, rutas absolutas y refs invalidas en todo parametro; nunca leer fuera de
  Area_comun (los reads ya van por git show; blindalo).
- **Rate-limit:** basico por IP/token en governance.
- **e2e del puente:** prueba que arranca el server y verifica los 11 endpoints read-only + 401 sin token +
  negativo de escritura.

## Limites

- SOLO LECTURA (F2 gateado post-TFM). PII por construccion intacta. Denylist intacta. NO tocar core/#4/baseline.
  Producto Zeus-Aegis. Commit como Arquitecto + Co-Authored-By Codex. Bloqueo -> blocked + una pregunta.

Genera dataset elegible. Actualizo el pipeline tras cerrar. F4.3 (versionado) y F4.4 (DECISION final) van con F2.
