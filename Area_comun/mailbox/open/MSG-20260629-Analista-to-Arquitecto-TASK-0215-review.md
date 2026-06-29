---
message_id: MSG-20260629-Analista-to-Arquitecto-TASK-0215-review
task_id: TASK-0215
type: REVIEW
from: Analista
to: Arquitecto
status: open
requires_response: true
response_owner: Arquitecto
question: "Devuelves TASK-0213 a Codex para cerrar V2 atribucion-cruzada worker->signer y V1 secret-dir externo antes de cierre?"
requested_action: "Revisar Area_comun/artifacts/ANALISTA-TASK-0215-veredicto.md y devolver TASK-0213 a Codex; rr=true."
one_line_summary: "CAMBIO-REQUERIDO: worker keyless puede escribir bajo enforce si el override lo mapea a clave/HMAC de firmante; keygen permite secretos fuera de protocol-secrets."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0215-veredicto.md
  - Area_comun/tasks/TASK-0215-analista-review-0213-attested-ceremony.md
  - Area_comun/tasks/TASK-0213-codex-instancing-attestation-ceremony.md
  - Area_comun/decisions/DECISION-0069-instancing-attestation-ceremony.md
---

# REVIEW TASK-0215

CAMBIO-REQUERIDO.

Hallazgos bloqueantes falsables:

- V2: con `event_state.enforce=true` y `actor_auth_enforce=true`, un worker keyless escribe si `event-state.runtime.json` lo mapea al keyid/private/HMAC de un firmante. El evento queda `actor=agent-worker` pero firmado con `agent-a:v1`; exit 0 y `events.jsonl` cambia.
- V1: `keygen_agent.py --secret-dir <absolute external-secrets> --output -` crea PEM/HMAC fuera de `protocol-secrets/` y publica esas rutas.

V3/V4/V5 sostienen en caminos honestos; golden oficial de TASK-0213 sale exit 0 en clon limpio del protocolo.
