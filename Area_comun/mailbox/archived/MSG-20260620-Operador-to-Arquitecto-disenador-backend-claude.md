---
message_id: MSG-20260620-Operador-to-Arquitecto-disenador-backend-claude
type: DECISION
task_id: none
from: Operador
to: Arquitecto
requires_response: false
status: archived
one_line_summary: Dato que faltaba para el onboard del Disenador: backend = claude (llm_cli_preset "claude"). Capacidades segun el prompt de rol (15_Asistente_PROMPT-disenador) + el GO front-completo-disenador. Con esto puedes correr la ceremonia de re-genesis cuando yo este presente.
requested_action: "Onboardear al agente DISENADOR con backend claude (llm_cli_presets.claude). Identidad propia (id Disenador) + su keypair (publica al agent_registry pinned; privada wrapper-side via llm_turn_wrapper). tool_policy: leer SPECs/requisitos (Area_comun + design/), ESCRIBIR artefactos de diseno en el repo de producto Zeus-protocol/design/interface/, NO escribir codigo ni ledger/estado directo, NO submit_intent. Ejecutar la re-genesis-boundary GOBERNADA en copia limpia, con el operador PRESENTE, su propia ventana de riesgo. Su rol en el prompt: personal/operador/15_Asistente_PROMPT-disenador.md (handover)."
question: none
context_refs:
  - personal/operador/15_Asistente_PROMPT-disenador.md
  - Area_comun/mailbox/open/MSG-20260620-Operador-to-Arquitecto-GO-front-completo-disenador.md
  - Area_comun/decisions/DECISION-0045-boundary-t0-sello-pre-t0.md
deadline_or_blocking_level: normal
---

# Onboard del Disenador: backend = claude

CLIs disponibles: **claude** y **codex**. El Disenador usa **backend `claude`** (codex sigue siendo el
implementador). Identidad/claves distinguen al agente, no el modelo: Arquitecto (claude) y Disenador
(claude) conviven sin problema.

## Parametros del onboard
- **id:** Disenador. **backend:** `llm_cli_presets.claude`. **keypair propio** (publica al `agent_registry`
  pinned por el genesis; privada wrapper-side, fuera del repo).
- **tool_policy (deny-by-default):** leer SPECs/requisitos (`Area_comun` + `design/`); **escribir solo
  artefactos de diseno** en `D:\Agentes\Zeus\Zeus-protocol\design\interface\`; **NO** codigo, **NO** ledger/
  estado directo, **NO** `submit_intent`. El handoff del diseno a Codex lo registras tu (gobernado/atestado).
- **rol/prompt de arranque:** `personal/operador/15_Asistente_PROMPT-disenador.md`.

## Ceremonia (recordatorio)
Es **re-genesis-boundary gobernado** (cambia el conjunto de firmantes): copia limpia (DECISION-0045: nunca
contra el log vivo), **operador PRESENTE**, su **propia ventana de riesgo** (no combinar). #4 epoca pasa a
nueva epoca al re-genesis (batcheado/gobernado, DECISION-0047). Reporta el resultado (nuevo firmante en el
registry, validate exit 0, drift 0) en canonico. Canal ASCII.
