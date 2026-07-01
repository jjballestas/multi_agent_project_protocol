# ANALISTA TASK-0227 F1 Boundary Verdict

Firma: Analista
Fecha: 2026-07-01

## Veredicto

CAMBIO-REQUERIDO / NO-GO.

El commit producto `15c52fb134ee21cc9d716af8f9d8a9c7aba0e741` deja `npm test` verde en clon limpio, y el timeout de lectura canonica ya no reproduce fallo. Pero el boundary F1 no queda cerrado por comportamiento: el test solo detecta algunos `fetch` de escritura literales y deja pasar variantes reales de escritura HTTP en la UI.

Recomendacion de cierre: CAMBIO-REQUERIDO. Endurecer el guard F1 para cubrir toda la familia de write methods en UI, no solo `method: 'POST|PUT|PATCH|DELETE'` con comillas simples/dobles y `axios(...)`.

## Ancla Canonica

| Elemento | Valor |
|---|---|
| Instruccion REVIEW | `Area_comun/mailbox/open/MSG-20260630-Arquitecto-to-Analista-REVIEW-TASK-0227-f1-boundary.md` |
| Protocolo citado por instruccion | `9e0206e48b66227a9165a2970d9f717d51b0953f` |
| Protocolo vivo durante review | `245e521f1420f87614a59bc640ca219a87899a44` |
| Producto | `D:/Agentes/Zeus/Zeus-Aegis` |
| Producto bajo review | `15c52fb134ee21cc9d716af8f9d8a9c7aba0e741` |
| Clon limpio producto | `C:/Users/johnb/AppData/Local/Temp/analista-0227-zeus-aegis-31a2123de8544283adf546a486497d3e` |
| Clon limpio protocolo citado | `C:/Users/johnb/AppData/Local/Temp/analista-0227-protocol-2b4d798a09bd46f79f1999aa79d04351` |
| `protocol.config.json` sha256 | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` vivo y limpio |

## Reproduccion

| Gate | Resultado |
|---|---|
| `git clone D:/Agentes/Zeus/Zeus-Aegis <tmp>; git checkout 15c52fb; npm test` | exit 0, 82 files / 556 tests |
| Target canonico `governance-readonly.test.ts`, test F1 | exit 0 |
| `python scripts/validate_collaboration_state.py` vivo con secretos | exit 0 |
| `python scripts/validate_collaboration_state.py --root <clean-protocol-9e0206e>` sin secretos | exit 0 |
| `python scripts/scan_domain_neutrality.py` vivo/limpio | exit 0 |
| `python scripts/scan_encoding.py` vivo/limpio | exit 0 |
| Drift vivo | `has_drift=false`, `up_to_seq=2791` |
| Drift limpio `9e0206e` | `has_drift=false`, `up_to_seq=2758` |

## Vectores

| Vector / AC | Resultado | Evidencia falsable |
|---|---|---|
| Full suite producto en clon limpio | PASA | `npm test` exit 0 en `15c52fb`; `governance-readonly.test.ts` tarda 26976 ms total y el caso de artifacts/decisions/handoffs/ledger 9822 ms bajo timeout 30000. |
| Texto display-only `submit_intent` con guard local | PASA | El test canonico acepta las menciones existentes cuando hay guard cercano `NO escribe el ledger` / `does NOT write the ledger` / `Pure client-side, no fetch, no writer-path`. |
| `submit_intent` sin guard local | PASA | Payload propio `const analistaUnguardedSubmitIntent = 'submit_intent should fail without local guard'` hace fallar el test F1 con exit 1. |
| `fetch(..., { method: 'POST' })` literal | PASA | Payload propio `fetch('/api/governance/state', { method: 'POST' })` hace fallar el test F1 con exit 1. |
| `fetch(..., { method: \`POST\` })` | SLIPS | Payload propio compila como patron real de escritura, pero el test F1 sale exit 0 porque el regex solo acepta comillas simples/dobles. |
| `const m = 'POST'; fetch(..., { method: m })` | SLIPS | Payload propio sale exit 0; el guard no resuelve valores de metodo aunque la llamada escribe. |
| `fetch(..., { method: 'post' })` | SLIPS | Payload propio sale exit 0; Fetch normaliza metodos case-insensitive de uso real, pero el regex solo cubre mayusculas. |
| `axios.post('/api/governance/state')` | SLIPS | Payload propio sale exit 0; el guard cubre `axios(...)` con `method:` pero no los shorthand `axios.post/put/patch/delete`. |
| `GOVERNANCE_FORBIDDEN_WRITE_PATTERNS` | PASA PARCIAL | La lista conserva `submit_intent.py`, `Area_comun/state/`, `runtime/state/events.jsonl`, pero no cubre los slips UI anteriores. |

## Hallazgo Bloqueante

El AC pedido no era solo "el ejemplo literal falla"; era confirmar que F1 sigue rojo ante un write-path real. Hay escapes nuevos y triviales que conservan semantica de escritura:

```ts
const m = 'POST'
void fetch('/api/governance/state', { method: m })
void fetch('/api/governance/state', { method: `POST` })
void fetch('/api/governance/state', { method: 'post' })
void axios.post('/api/governance/state')
```

Todos pasaron el test F1 dirigido con exit 0 en el clon limpio mutado. Por tanto el test ya no es sobre-amplio para texto inerte, pero quedo sub-amplio para la familia de write-paths que promete bloquear.

## Residuales

- No encontre fuga F1 real en el `15c52fb` canonico sin mutar: los `fetch` presentes son GET/read-only y las menciones de `submit_intent` son preparar-comando display-only.
- El timeout parece mitigado para esta corrida, pero el cierre no es recomendable mientras el guard F1 acepta variantes HTTP de escritura reales.

