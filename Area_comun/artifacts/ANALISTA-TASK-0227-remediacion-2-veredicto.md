# ANALISTA TASK-0227 remediacion-2 veredicto

Firma: Analista

Veredicto: CAMBIO-REQUERIDO / NO-GO.

Ancla canonica:
- Instruccion REVIEW: `f7c92ba` (`MSG-20260701-Arquitecto-to-Analista-REVIEW-TASK-0227-remediacion-2.md`).
- Redelivery protocolo: `464b479b4b3c5a46ca064a8f31871fafb97f1208`.
- Protocolo HEAD revisado: `b73aa9004da544c911ff7fdf76dc78dd70ce5ce2`.
- Producto bajo review: `D:/Agentes/Zeus/Zeus-Aegis` commit `88091b1ee299734fa860ad9229556575f312eb38`.
- Clean clone producto: `C:/Users/johnb/AppData/Local/Temp/analista-0227-product-b3b7af714ad64b2a9e421a5b295e164b`.
- Clean clone protocolo: `C:/Users/johnb/AppData/Local/Temp/analista-0227-protocol-b7ed818e431e450890d71002945cf90e`.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| `npm test` en clean clone producto | EXIT 124, timeout a 604s |
| `corepack pnpm --dir vendor/hermes-2.3.0 exec vitest run src/server/governance-readonly.test.ts --maxWorkers=1 --testTimeout=60000 --hookTimeout=60000` | EXIT 124, timeout a 304s |
| Probe propio sobre `GOVERNANCE_FORBIDDEN_WRITE_PATTERNS` extraido de `src/server/governance-readonly.test.ts` | EXIT 1, slips nuevos falsables |
| Clean clone protocolo `python scripts/validate_collaboration_state.py --root <clone>` | EXIT 0 |
| Clean clone protocolo `python scripts/scan_domain_neutrality.py --root <clone>` | EXIT 0 |
| Clean clone protocolo `python scripts/scan_encoding.py --root <clone>` | EXIT 0 |
| Drift clean clone protocolo | `has_drift=false`, `up_to_seq=2848` |
| `protocol.config.json` sha256 | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

Nota de canon: el working tree vivo no se uso como ancla. En arranque, `python scripts/validate_collaboration_state.py`
en el workspace vivo salio EXIT 1 por un cambio local no commiteado ajeno:
`CLAIM-20260701-Codex-DECISION-0078` con selector invalido
`Area_comun/state/PROJECT_STATE.json#decisions/DECISION-0078`. El clean clone del HEAD canonico si valida.

## Vectores

| Vector / AC | Resultado | Evidencia falsable |
| --- | --- | --- |
| `const m = 'POST'; fetch('/api/governance/state', { method: m })` | PASA | El patron lo atrapa (`caught=true`). |
| `fetch('/api/governance/state', { method: template-literal POST })` | PASA | El patron lo atrapa (`caught=true`). |
| `fetch('/api/governance/state', { method: 'post' })` | PASA | El patron lo atrapa (`caught=true`). |
| `axios.post('/api/governance/state')` | PASA | El patron lo atrapa (`caught=true`). |
| `axios.put/patch/delete('/api/governance/state')` | PASA | Los shorthand quedan atrapados (`caught=true`). |
| `axios({ url: '/api/governance/state', method: 'PATCH' })` | PASA | Config `url` antes de `method` queda atrapado. |
| `axios({ method: writeMethod, url: '/api/governance/state' })` | PASA | Config `method` antes de `url` queda atrapado. |
| Texto display-only `submit_intent.py` cerca de "NO escribe el ledger" | PASA | No se marca (`caught=false`). |
| `const method = 'POST'; fetch('/api/governance/state', { method })` | SLIPS | Es write-path real por shorthand property; los patrones exigen `method:` y no lo atrapan. |
| `fetch('/api/governance/state', { ['method']: 'POST' })` | SLIPS | Es write-path real por computed property; los patrones exigen `method:` literal y no lo atrapan. |
| `axios.request({ url: '/api/governance/state', method: 'POST' })` | SLIPS | Es write-path real; solo se cubre `axios(...)` y `axios.post/put/patch/delete(...)`. |
| `const method = 'POST'; axios({ url: '/api/governance/state', method })` | SLIPS | Config shorthand real; los patrones exigen `method:` y no lo atrapan. |

## Residuales

- El NO-GO no depende solo del timeout: hay escapes nuevos de la misma familia "metodo no literal / write-path
  real" que el AC pretende cerrar.
- El gate pedido por la instruccion era `npm test` en clean clone y gatear por EXIT; en esta reproduccion no queda
  verde.
- La instruccion superior del operador nombra `D:/Agentes/Zeus/Zeus-protocol`, pero la instruccion canonica y el
  handoff de TASK-0227 citan `D:/Agentes/Zeus/Zeus-Aegis` commit `88091b1`. Revise el commit citado por la
  instruccion canonica.

## Recomendacion

CAMBIO-REQUERIDO. No cerrar TASK-0227. Pedir a Codex:

1. Hacer verde `npm test` en clean clone, o cambiar explicitamente el gate con decision/instruccion de reviewer.
2. Endurecer el guard F1 para shorthand/computed method properties y `axios.request(...)`, con negativos
   permanentes por comportamiento.
