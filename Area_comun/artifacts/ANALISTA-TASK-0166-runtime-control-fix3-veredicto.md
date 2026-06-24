# ANALISTA TASK-0166 fix3 - veredicto adversarial

Firma: Analista

## Veredicto

CAMBIO-REQUERIDO. El escape original `agentId: ["Codex"]` quedo cerrado en el commit producto
`a1d4491fc00f86ffdb3c3fce73de0d6ca9d366ae`, pero queda un escape hermano en el mismo endpoint:
`action: ["activate"]` se acepta por coercion y muta el runtime (`200`, heartbeat creado). Tambien
`action: { "toString": "activate" }` devuelve `500` con un TypeError publico en vez de rechazo controlado.

Recomendacion de cierre: NO CERRABLE hasta exigir `typeof input.action === "string"` antes de coercion,
rechazar tipos no-string con `400`, y dejar tests negativos permanentes para `action: ["activate"]` y
`action: { ... }`.

## Ancla canonica

| Repo | Ref |
|---|---|
| Producto `D:/Agentes/Zeus/Zeus-protocol` | `a1d4491fc00f86ffdb3c3fce73de0d6ca9d366ae` |
| Protocolo, instruccion REVIEW procesada | `07c3ad622cbefe04120cd897513af3b8113123ec` contiene `Area_comun/mailbox/open/MSG-20260624-Arquitecto-to-Analista-REVIEW-TASK-0166-fix3.md` |
| Protocolo citado por la instruccion | `9f3cded58e9305bd7926a46c54092f85286d3c0a` |

## Reproduccion

| Gate / prueba | Resultado |
|---|---|
| Clon limpio producto, checkout `a1d4491`, `npm test` corrida 1 | exit 1, 63/64; fallo local de readiness: el servidor imprimio `listening` pero el harness no recibio `/healthz` a tiempo |
| Mismo clon limpio, `npm test` corrida 2 | exit 0, 64/64 |
| Payloads propios contra servidor temporal sobre producto `a1d4491` + protocolo clonado en `9f3cded` | exit 0 del harness propio |
| `python scripts/validate_collaboration_state.py` con secretos, repo vivo | exit 0 |
| `python scripts/validate_collaboration_state.py --root <clone sin secrets>` | exit 0 |
| Drift repo vivo | `has_drift=false`, `up_to_seq=1617` |
| `python scripts/scan_domain_neutrality.py` | exit 0 |
| `python scripts/scan_encoding.py` | exit 0 |
| `protocol.config.json` #4 | byte-identico durante la pasada, SHA256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Tabla vector por vector

| Vector | Resultado | Veredicto |
|---|---:|---|
| `agentId: ["Codex"], action: "activate"` | `400`, sin heartbeat | PASA |
| `agentId: { "toString": "Codex" }, action: "activate"` | `400`, sin heartbeat | PASA |
| `agentId: 0`, `true`, `null`, `[["Codex"]]` | `400`, sin heartbeat | PASA |
| `agentId: " Codex"` | `400`, sin heartbeat | PASA |
| `agentId: "Co\\u200ddex"` | `400`, sin heartbeat | PASA |
| `agentId: "Codex\\u0000"` | `400`, sin heartbeat | PASA |
| JSON raw con duplicate key ultimo `Bad` | `400`, sin heartbeat | PASA |
| Extra key `__proto_polluted` | `400`, sin heartbeat | PASA |
| Heartbeat ausente | `dormant` | PASA |
| Heartbeat stale 10 min | `dormant` | PASA |
| Heartbeat futuro +10y | `dormant`, `ageMs=null` | PASA |
| Heartbeat fresco | `alive` | PASA |
| Control positivo `agentId: "Codex", action: "activate"` | `200`, heartbeat creado | PASA |
| `agentId: "Codex", action: ["activate"]` | `200`, heartbeat creado | SLIPS |
| `agentId: "Codex", action: { "toString": "activate" }` | `500`, sin heartbeat, TypeError publico | SLIPS |

## Hallazgo falsable

En `src/server.js`, `sanitizeRuntimeControlAgentId` ya hace el type-check estricto para `agentId`, pero
`applyRuntimeControlAction` sigue calculando:

```js
const action = ascii(stripControl(input?.action || "")).trim();
```

Como `stripControl` llama a `String(value)`, un array JSON de un solo elemento coerciona a la accion valida:
`String(["activate"]) === "activate"`. El endpoint acepta el payload, escribe `Codex.heartbeat` y devuelve
estado `alive`.

Payload minimo:

```json
{"agentId":"Codex","action":["activate"]}
```

Resultado observado:

```json
{"status":200,"body":{"ok":true,"action":"activate","agentId":"Codex","status":"alive"},"heartbeat":true}
```

## Residuales

- El primer `npm test` tuvo el flake de readiness ya observado en esta suite; la repeticion completa fue verde.
- No probe interaccion visual pixel-perfect del boton; la pasada se centro en el contrato de runtime server-side.
- El hallazgo no permite comando arbitrario ni agente fuera de allowlist, pero si permite mutacion de runtime con un
  tipo JSON malformado. Para este gate, eso basta para devolver a maker porque reproduce el mismo patron de coercion
  que se acaba de corregir en `agentId`.
