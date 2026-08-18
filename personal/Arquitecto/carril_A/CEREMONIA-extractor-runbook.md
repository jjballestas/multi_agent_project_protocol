# Runbook: alta del agente Extractor -- analisis + opciones (DRAFT para el operador)

> Autor: Arquitecto. Fecha: 2026-06-22. Estado: DRAFT para ratificacion. NO ejecutado.
> Relacionado: DECISION-0058, DECISION-0022/0028 (#4), regenesis.py.

## Mecanica real (lo que toca un re-genesis)

El re-genesis afecta `protocol.config.json`, que esta PINNED bajo #4 (chain.genesis = canonical_hash del config):
- `agent_registry.agents`: lista de agentes con `id`/`enabled`/`capabilities`. Hoy: Arquitecto, Codex, Analista.
- `event_state.signature_config.public_keys`: mapa `<id>:v1` -> clave Ed25519 publica. Es el registro de quien
  FIRMA los eventos del ledger atestado (submit_intent). Hoy: arquitecto:v1, codex:v1, analista:v1.
- `tool_policy.policies`: policy.architect, policy.implementer.
- `regenesis.py` (runtime): re-escribe el genesis desde el hot state actual (nuevo config hash), re-snapshot,
  verifica drift_after==0. Es el mecanismo para re-basar la cadena tras cambiar el config.

Agregar un agente al `agent_registry`/`signature_config` cambia el config -> invalida `chain.genesis` ->
**exige re-genesis-boundary**: la operacion MAS delicada del sistema (toca la cadena de atestacion viva, con
enforce+authoritative ON).

## La pregunta de diseno (clave)

El `agent_registry` + `signature_config` es el registro de **firmantes del ledger atestado**. **El Extractor NO
escribe el ledger** (DECISION-0058: sin submit_intent; candidatas al store NO-ledger; gate humano + aprobacion
antes del intake). Por tanto:

- **NO necesita una clave Ed25519 en `signature_config`** (nunca firma eventos del ledger).
- Su "autoria honesta" (firmar sus candidatas) es a nivel PRODUCTO (el store de candidatas en Zeus), con una
  clave de producto -- NO la cadena #4 del protocolo.
- Registrarlo en el `agent_registry` #4 (con re-genesis) da reconocimiento FORMAL, pero NO es funcionalmente
  necesario para que el provider corra ni para la autoria honesta.

## Opcion 1 -- Ceremonia completa de re-genesis (como contemplaba DECISION-0058)

Registrar el Extractor en `protocol.config.json` (agent_registry + capability + keypair) via re-genesis-boundary.
- Pasos: (a) generar keypair Ed25519 del Extractor (privada en D:/Agentes/protocol-secrets/); (b) agregar
  `{"id":"Extractor","enabled":true,"capabilities":["extractor"]}` a agent_registry.agents + `extractor:v1` ->
  pubkey en signature_config.public_keys + policy.extractor minima en tool_policy; (c) en COPIA LIMPIA, con el
  operador presente: editar config + `python runtime/regenesis.py --actor-id Arquitecto --timestamp <ISO>
  --commit <short>`; (d) verificar drift 0 + validate con/sin secretos exit 0 + chain/firmas validas; (e) commit;
  (f) rollback armado (flags #4 -> false) si algo falla.
- RIESGO: ALTO (toca la cadena #4 viva). Beneficio: el Extractor queda como firmante #4 (util SOLO si algun dia
  escribe el ledger).

## Opcion 2 -- Extractor como worker de PRODUCTO, SIN re-genesis (RECOMENDADA)

Distincion limpia:
- **Agentes de GOBERNANZA** (escriben el ledger atestado, en agent_registry #4, alta=re-genesis): Arquitecto,
  Codex, Analista.
- **Workers de PRODUCTO** (proponen candidatas al intake con gate humano, NUNCA escriben el ledger): el Extractor
  -> registrado a nivel PRODUCTO (Zeus), firma sus candidatas con una clave de PRODUCTO, **SIN entrada en el
  agent_registry #4, SIN re-genesis**.
- La autoria honesta se cumple (el Extractor firma sus candidatas; el dataset muestra su firma de producto), y
  EVITAMOS la operacion mas peligrosa (re-genesis sobre la cadena #4 viva) para un agente que ni siquiera escribe
  el ledger.
- El `agent_registry` #4 se reserva para quienes realmente atestan el ledger. El config sigue pinned 1.14.0, sin
  re-genesis.

RIESGO: BAJO (no toca #4). Requiere: una clave de producto para el Extractor (en Zeus/secrets de producto) +
registrar al Extractor en la capa de producto (un registro de workers fuera del config #4).

## Recomendacion

**Opcion 2.** No hacer la operacion mas peligrosa (re-genesis #4 viva) para un agente que no escribe el ledger.
Si el operador quiere igualmente el reconocimiento formal en #4, hacemos Opcion 1 con todas las guardas. Esto
AMENDA la suposicion de DECISION-0058 ("alta = re-genesis"): el alta del Extractor NO requiere re-genesis porque
no es firmante del ledger; se registra a nivel producto.

## Pendiente antes de uso vivo (cualquier opcion)

- TASK-0155 (provider) cerrada (Analista verificando).
- Apuntar el provider a `qwen3-vl:4b-instruct` (config; import ya hecho).
- Clave de firma del Extractor (producto en Opcion 2; #4 en Opcion 1).
- GO de uso vivo del operador + pasada del Analista al encender (ventana de modelo real).
