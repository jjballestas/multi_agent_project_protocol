---
message_id: MSG-20260622-Arquitecto-to-Codex-GO-TASK-0156
task_id: TASK-0156
type: DIRECTIVE
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0156 (ready): registro del worker Extractor a nivel PRODUCTO (fuera del config #4, sin re-genesis) + keypair Ed25519 de PRODUCTO + firma de candidatas + provider default qwen3-vl:4b-instruct. OFF-by-default. maker=Codex/checker=Arquitecto+Analista. node --test clon limpio verde, #4 byte-id (no toca protocol.config.json)."
requested_action: "Reclama TASK-0156 (ready), implementa en Zeus-protocol y entrega in_review. (1) Registro de workers a nivel PRODUCTO (FUERA de protocol.config.json; p.ej. extractors.config.json o un workers registry): record del Extractor -- id Extractor, rol extraccion, modelo default qwen3-vl:4b-instruct (no-thinking), endpoint loopback default http://127.0.0.1:11434/api/chat; apunta el provider local-vlm a este default. (2) Keypair Ed25519 de PRODUCTO del Extractor: privada FUERA del repo (gitignored/dir de secretos de producto, NO commitear; documenta comando+ruta en el handoff), publica en el registro de workers; NO en signature_config #4. (3) Firma de candidatas: cada candidata lleva firma Ed25519 valida + id del firmante; behavior-test firma valida vs forjada/ausente. OFF-by-default; el registro NO toca protocol.config.json (#4 byte-identica, pinned 1.14.0). Manten verdes: node --test clon limpio, validate con/sin secretos exit 0, drift 0, neutralidad+encoding 0. NO enciendas el uso vivo del Extractor."
context_refs:
  - Area_comun/tasks/TASK-0156-codex-extractor-product-registration.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/decisions/DECISION-0058-registro-agente-extractor-vlm-local.md
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
deadline_or_blocking_level: normal
---

# GO - TASK-0156: worker Extractor a nivel producto (Opcion 2, sin re-genesis)

Opcion 2 (DECISION-0058): el Extractor es worker de PRODUCTO, NO firmante del ledger #4, alta SIN re-genesis.
Detalle en la tarea y SPEC-0086 (AC54). maker=Codex / checker=Arquitecto + pasada del Analista (firma/PII). NO
enciendas nada vivo; el uso vivo (encender el flag) es GO aparte del operador con el Analista. Canal ASCII.
