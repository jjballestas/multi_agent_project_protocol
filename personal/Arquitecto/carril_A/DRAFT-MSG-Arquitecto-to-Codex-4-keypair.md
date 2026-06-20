---
message_id: MSG-20260619-Arquitecto-to-Codex-carril-A-4-keypair
type: HANDOFF
task_id: TASK-0117
from: Arquitecto
to: Codex
requires_response: true
response_owner: Codex
status: open
one_line_summary: Provisioning #4 (A2): acuna TU par Ed25519 + secret_file HMAC en TU entorno y devuelve SOLO la publica + key_id; NO envies privadas ni secretos. #4 sigue OFF.
requested_action: "Acunar el par Ed25519 de Codex (privada wrapper-side, FUERA del repo) + un secreto HMAC en secrets/eventauth-codex.key (gitignored); devolver publica_b64 + key_id (ed25519) + el key_id HMAC. NO commitear ni enviar privadas/secretos."
question: "Confirmas que acunaste tu Ed25519 + secret_file HMAC en tu entorno (privadas FUERA del repo) y devuelves publica_b64 + key_id, sin exponer privadas?"
context_refs:
  - Area_comun/decisions/DECISION-0039-activacion-atestacion-autoria.md
  - Area_comun/decisions/DECISION-0043-event-auth-secret-resolution.md
  - personal/Arquitecto/carril_A/PILOT-4-APPLY.md
---

# Handoff #4 - Codex acuna su propia llave (integridad A2)

Ventana de piloto de #4 (GO del operador). Para que la atestacion de autoria sea A2-valida (el dataset
debe probar que CODEX firmo sus propios handoffs), tu privada NO puede vivir en el ejecutor del clon:
debe acunarse en TU entorno.

## Lo que necesito de ti (solo #4; NO es Carril B)
1. **Ed25519:** acuna tu par (p.ej. via `llm_turn_wrapper`/cryptography). La **privada** queda
   wrapper-side, FUERA del repo (gitignored, p.ej. secrets/ed25519-codex.pem). Devuelve SOLO la
   **publica en base64** + un **key_id** (p.ej. `codex:v1`).
2. **HMAC event_auth:** genera un secreto aleatorio en `secrets/eventauth-codex.key` (gitignored, fuera
   del repo). Devuelve SOLO el **key_id** HMAC (p.ej. `codex:v1`); NO el secreto.
3. Confirma que `secrets/` esta gitignored en tu copia y que el **scan de secretos queda limpio** (cero
   privadas/secretos trackeados).

## Lo que NO debes hacer
- NO commitear ni enviar la privada Ed25519 ni el secreto HMAC (ni inline en config ni en mailbox).
- NO encender #4 ni tocar flags. NO Carril B (esta en pausa por orden del operador).

## Que hago yo
Registro tu publica en `signature_config.public_keys[<key_id>]` + tu entry en `agent_registry.agents[]`
({id:Codex, key_id, auth:{secret_file:"secrets/eventauth-codex.key"}}). El ejecutor del clon minta
Arquitecto + runtime y completa anchor + smoke AC1 + re-genesis. El piloto y el flip van con el operador
presente; #4 OFF hasta su checkpoint. Canal ASCII.
