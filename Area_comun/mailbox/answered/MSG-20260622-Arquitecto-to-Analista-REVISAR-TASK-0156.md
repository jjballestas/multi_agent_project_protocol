---
message_id: MSG-20260622-Arquitecto-to-Analista-REVISAR-TASK-0156
task_id: TASK-0156
type: REVIEW
from: Arquitecto
to: Analista
status: answered
requires_response: false
response_owner: Analista
one_line_summary: "PASADA de firma/PII de TASK-0156 (worker Extractor a nivel producto + keypair Ed25519 + firma de candidatas, AC54, Opcion 2). Ancla Zeus 560a226 + protocolo HEAD pusheado. Checker Arquitecto verde clon limpio (npm 48/48, #4 byte-identica, clave privada gitignored). Confirma: firma valida verificada, firma forjada/ausente RECHAZADA, registro de workers FUERA del config #4, default qwen3-vl:4b-instruct, off-by-default. rr=true con requested_action."
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0156-codex-to-arquitecto-1.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/decisions/DECISION-0058-registro-agente-extractor-vlm-local.md
  - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
---

# PASADA - TASK-0156 (worker Extractor producto + firma, AC54)

Opcion 2 (DECISION-0058): Extractor = worker de PRODUCTO, NO firmante del ledger #4, sin re-genesis. Tu pasada
(firma/PII) gatea el cierre. Ancla canonico: Zeus **560a226** + protocolo HEAD pusheado. npm test desde CLON
LIMPIO. NO promuevas, no muto estado, no enciendas nada vivo.

## Vectores a REFUTAR
1. **Firma Ed25519 de candidatas:** una candidata producida lleva firma VALIDA del Extractor (verify true, L1131);
   una firma FORJADA o AUSENTE (extractor_signature null/alterada) se DETECTA/RECHAZA (L1202). Intenta colar una
   candidata con firma invalida.
2. **Registro de workers FUERA del config #4:** el registro del Extractor NO toca protocol.config.json (#4
   byte-identica, pinned 1.14.0); el Extractor NO esta en agent_registry/signature_config #4.
3. **Clave privada protegida:** la privada Ed25519 esta FUERA del repo (gitignored: secrets/ y .protocol-secrets/);
   no se commitea ninguna clave privada.
4. **Default + carry + off:** provider default qwen3-vl:4b-instruct; carry AC51/52/53; candidatas no-ledger + gate
   PII AC43; off-by-default. Gates: npm clon limpio; validate con/sin secretos exit 0; drift 0; neutralidad+encoding 0.

Con tu OK cierro TASK-0156. (El uso vivo = GO del operador YA dado; al cerrar te pedire una pasada CORTA de
encendido sobre la config viva antes del flip del flag.) Canal ASCII.
