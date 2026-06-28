# ANALISTA TASK-0211 veredicto

Firma: Analista

Veredicto: CAMBIO-REQUERIDO.

Ancla canonica:
- Protocolo instruccion: e9c59f4e0760abc0417703996f4bcfbcc68a7afa.
- Producto Zeus-Aegis bajo review: 3f8461e31de06fa8ea2720a3ced0b77dcc6224c7.
- Clean clone producto: C:/Users/johnb/AppData/Local/Temp/zeus-aegis-review-0211-dd2e231681f844c79de937b5d925d2b0.

Resumen:
- V1-V4 sustantivos del cache sostienen: no encontre verde hardcodeado, refresh fuerza validacion real, TTL expira a rojo, no hay writer-path nuevo, unknown del render no sale del diff de 0209, e invalidacion por HEAD funciona.
- Bloqueo de cierre: AC3 de TASK-0209 dice `pnpm governance:smoke PASS`; en clean clone, despues de `npm test`, `corepack pnpm --dir vendor/hermes-2.3.0 governance:smoke` sale exit 1 porque falta `dist/server/server.js`. Tras `corepack pnpm --dir vendor/hermes-2.3.0 build`, el mismo smoke sale exit 0. El gate no es reproducible tal como esta escrito en clean clone sin prebuild.

Reproduccion y gates:

| Prueba | Resultado |
|---|---|
| `git checkout 3f8461e`; `npm test` en clean clone | exit 0 |
| Probe propio V1/V4 por funciones `getGovernanceHealth`, `getGovernanceMetrics`, `getGovernanceLedger`, `getGovernanceState` contra protocolo temporal | exit 0; green/green inicial, cache TTL sirve green con checkedAt viejo dentro de ventana, `forceRefresh` con validate roto -> red, metrics -> red, ledger override red/green -> failed, TTL +46s -> red, state cambia al cambiar HEAD |
| Writer scan propio sobre 10 rutas `/api/governance/*` + `governance.tsx` | exit 0; solo GET, sin `submit_intent.py`, `runtime/state/events.jsonl`, `Area_comun/state/`, ni fetch con metodo write |
| `corepack pnpm --dir vendor/hermes-2.3.0 governance:smoke` tras `npm test` | exit 1; `ERR_MODULE_NOT_FOUND ... dist/server/server.js` |
| `corepack pnpm --dir vendor/hermes-2.3.0 build` | exit 0 |
| `corepack pnpm --dir vendor/hermes-2.3.0 governance:smoke` tras build | exit 0 |
| Protocolo `python scripts/validate_collaboration_state.py` | exit 0 |
| Protocolo secretless clone `python scripts/validate_collaboration_state.py --root <clone>` | exit 0 |
| Drift vivo | exit 0; `has_drift=false`, `up_to_seq=2461` antes de release; release posterior dejo drift 0 en `up_to_seq=2464` |
| `python scripts/scan_domain_neutrality.py` | exit 0 |
| `python scripts/scan_encoding.py` | exit 0 |
| `protocol.config.json` | byte-identico, sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

Vector por vector:

| Vector | Veredicto | Evidencia falsable |
|---|---|---|
| V1 honestidad del chip | SOSTIENE con residual TTL | El valor green sale de `validateExitCode=0` real. Al romper validate en protocolo temporal, `forceRefresh` devuelve `validator=red`, `metrics.health=red`, y tras simular +46s de TTL `getGovernanceHealth()` vuelve a calcular y devuelve red. Dentro de TTL se sirve el green cacheado con el mismo `checkedAt`; esto es la ventana honesta declarada por AC1, no un verde hardcodeado. |
| V2 no-regresion read-only | SOSTIENE | Las 10 rutas governance siguen exponiendo solo GET. El UI solo agrega `fetch('/api/governance/health?refresh=1')` y no agrega metodo write ni `submit_intent`. No vi writer-path hacia ledger/state. |
| V3 unknown preexistente | SOSTIENE como no-regresion de 0209 | El diff de 0209 en `governance.tsx` agrega refresh/checkedAt y no cambia la derivacion de `health?.validator`, `health?.drift` ni el `Promise.all` todo-o-nada. Si el render headless queda unknown por endpoints ajenos 503, eso es defecto UX preexistente/candidato TASK-0210, no regresion del cache. |
| V4 cache por HEAD + TTL | SOSTIENE | `healthCacheKey` y `stateCacheKey` incluyen `canonicalHead(repo, ref)`. En protocolo temporal, cambiar y commitear `PROJECT_STATE.slim.json` hizo que `getGovernanceState()` devolviera `updated_at=2099-01-01`, demostrando invalidacion por HEAD. |
| AC3 smoke PASS | SLIPS | En clean clone, el comando literal `corepack pnpm --dir vendor/hermes-2.3.0 governance:smoke` salio exit 1 por falta de `dist/server/server.js`. Solo pasa despues de `pnpm build`. |

Residuales declarados:
- No bloquee por el green cacheado dentro de TTL: el panel muestra `Verified Ns ago` y `refresh=1` revalida. Si el operador exige cero stale aun dentro de TTL, entonces el diseno de TASK-0209 debe cambiar y perderia el objetivo de performance.
- El chip `unknown` en render sigue siendo deuda UX fuera de este cache; no es cierre de V1-V4, pero merece TASK-0210 o equivalente si se quiere que el panel pinte health parcial aunque fallen endpoints no-governance.

Recomendacion de cierre:
- CAMBIO-REQUERIDO: o bien ajustar `governance:smoke` para construir/usar dev server de forma reproducible en clean clone, o registrar explicitamente que el gate es `pnpm build && pnpm governance:smoke` y actualizar AC/evidencia. Con ese punto corregido o waivado, V1-V4 quedan CERRABLES.
