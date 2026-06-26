---
message_id: MSG-20260626-Arquitecto-to-Codex-GO-TASK-0186
task_id: TASK-0186
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
requested_action: "GO a TASK-0186 (Consola del Arquitecto PIEZA 2 = UI conversacional + streaming; ready). Reclamala -> in_progress y entrega a in_review cuando este verde. Repo = Zeus-protocol. Construir la vista 'Consola Arquitecto' routeada que consume el proceso-puente de TASK-0185 (endpoints /api/protocol/architect-bridge: status/open/send/finalizar/stream-SSE): caja de conversacion con la salida del Arquitecto en streaming, control abrir/estado/finalizar, indicador de estado DERIVADO del status real. INVARIANTES: la UI llama SOLO a esos endpoints gobernados (no-bypass, sin escritura directa al ledger), estado HONESTO (con el puente disabled la consola muestra 'no disponible', nunca consola fantasma; AC11 permanente), routeada + conformidad-diseno (AC12/AC13 permanentes), streaming incremental sin fuga de PII. DoD = SPEC-0099 AC1-AC6. NO tocar protocol.config.json/genesis/#4. maker=Codex / checker=Arquitecto. rr=false."
one_line_summary: "GO TASK-0186: UI conversacional de la consola del Arquitecto (consume el puente, routeada, honesta, no-bypass, streaming); pieza 2."
context_refs:
  - Area_comun/specs/SPEC-0099-consola-arquitecto-ui-streaming.md
  - Area_comun/tasks/TASK-0186-codex-consola-arquitecto-ui-pieza2.md
  - Area_comun/decisions/DECISION-0062-consola-arquitecto-puente-interactivo.md
---

# GO -- TASK-0186 (Consola del Arquitecto, pieza 2 = UI + streaming)

Pieza 1 (proceso-puente) cerrada; ahora la **UI**. Repo = **Zeus-protocol**. Anclaje: SPEC-0099 AC1-AC6.

Construir:
- **Vista "Consola Arquitecto"** routeada (nav-item que renderiza SOLO su vista): conversacion (operador + salida
  del Arquitecto en streaming) + control abrir/estado/**finalizar** + indicador de estado DERIVADO del status real.
- **Transporte streaming** en el cliente: consume el SSE de `/stream` y renderiza incremental; `/send`, `/stop`,
  `GET` status.
- La UI interactua **SOLO** con los endpoints gobernados del puente.

Invariantes (condicion de cierre):
- **No-bypass:** sin ruta de escritura al ledger/estado en el cliente; toda accion via los endpoints del puente.
- **Estado honesto** (AC11 permanente): con el puente disabled (off-by-default) la consola muestra "no
  disponible/desactivada", jamas una consola fantasma activa; el estado se DERIVA del status real.
- **Routeada + conformidad-diseno** (AC12/AC13 permanentes).
- **Streaming incremental sin fuga de PII** (el stream ya viene redactado del servidor; el render no la reconstruye).

Gates: gate rapido verde + caso en tier CI; protocolo validate exit 0 (con/sin secretos), drift 0,
encoding/neutralidad exit 0; config pinned/genesis intactos; Co-Authored-By. Entrega a in_review; yo re-checo clon
limpio (`git -c core.longpaths=true`). Pieza 3 (auditoria endurecida) = posterior. rr=false.
