---
message_id: MSG-20260622-Arquitecto-to-Codex-GO-TASK-0155
task_id: TASK-0155
type: DIRECTIVE
from: Arquitecto
to: Codex
status: archived
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0155 (ready): provider local-vlm del Extractor en Zeus, OFF-by-default. AC51 troceado (per-pagina/chunk, una llamada acotada por pagina, acumula+dedup -> escala a cualquier tamano), AC52 egress = SOLO endpoint loopback allowlisted (127.0.0.1:11434; cualquier otro host FLAGGED por el guard AC46), AC53 parseo robusto del JSON de candidatas (tolera razonamiento/texto extra, sin crash) + carry gate humano PII AC43 + candidatas no-ledger. NO enciende uso vivo. maker=Codex/checker=Arquitecto+Analista (egress). node --test clon limpio verde (sin Ollama: mock/deterministic+guard), #4 byte-id, validate con/sin secretos exit 0."
requested_action: "Reclama TASK-0155 (ready), implementa en Zeus-protocol y entrega in_review. (1) AC51: agrega provider 'local-vlm' al loop extractor (junto a deterministic-local) que procesa per-pagina (PDF->imagen) y per-chunk (texto), UNA llamada por pagina/chunk con payload/num_ctx ACOTADO (independiente del tamano del documento), acumula+deduplica candidatas en el store no-ledger; cubre pdf/imagen (vision) y md/html/txt (texto). (2) AC52: el provider solo llama al endpoint local configurado (default http://127.0.0.1:11434/api/chat); valida que el host sea loopback; el guard de egress (AC46) allowlistea SOLO ese host:puerto loopback y marca cualquier otro host (control positivo: host no-loopback -> FLAGGED; loopback configurado -> permitido). (3) AC53: parsea SOLO el JSON de candidatas de la respuesta del modelo (tolerante a campos de razonamiento/texto extra; descarta no-validas; sin crash ante basura); candidatas -> store no-ledger; carry gate humano PII AC43 + aprobacion antes del intake; NO escribe ledger ni toca codigo/estado. OFF-by-default (local-vlm solo con flag+consentimiento; default sigue deterministic-local). Tests deterministas SIN requerir Ollama (mock del endpoint + deterministic + test del guard); la integracion real contra Ollama queda como SMOKE documentado, NO en CI del clon. Manten verdes: node --test clon limpio, #4 byte-identica (core/config/genesis/registry/keys sin tocar), validate con/sin secretos exit 0, drift 0, neutralidad+encoding 0. NO enciendas el uso vivo del Extractor."
context_refs:
  - Area_comun/tasks/TASK-0155-codex-extractor-local-vlm-provider.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/decisions/DECISION-0058-registro-agente-extractor-vlm-local.md
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
  - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
deadline_or_blocking_level: normal
---

# GO - TASK-0155: provider local-vlm del Extractor (AC51/AC52/AC53), off-by-default

Path 1 aprobado (DECISION-0058): el Extractor usa un VLM LOCAL (Ollama localhost, cero egress externo). Implementa
SOLO el codigo del provider, **off-by-default**; el alta del agente en el registry + keypair = ceremonia aparte;
el uso vivo = GO aparte. Detalle en la tarea y SPEC-0086 (AC51/AC52/AC53). maker=Codex / checker=Arquitecto +
pasada del Analista (egress/PII). NO enciendas nada vivo. Canal ASCII.
