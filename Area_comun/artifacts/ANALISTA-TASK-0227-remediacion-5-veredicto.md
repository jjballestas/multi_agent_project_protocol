# ANALISTA TASK-0227 remediacion-5 - veredicto

Firma: Analista

## Veredicto

CAMBIO-REQUERIDO / NO-GO.

El cierre no es ratificable contra la familia enumerable de DECISION-0079. El caso exacto de rem-4 queda corregido y `npm test` sale EXIT 0 en clon limpio, pero el guard F1 sigue dejando pasar write-paths estaticamente decidibles con claves de objeto entre comillas (`"method"` / `"url"`). Eso es JavaScript/TypeScript normal y pertenece a la misma familia enumerable de objeto literal local/config literal, no a runtime dinamico ni alias opaco.

## Ancla canonica

| Elemento | Valor |
|---|---|
| Protocolo REVIEW HEAD | `7953df12150c69d7f48c417252303c45ba4cc405` |
| Instruccion REVIEW | `Area_comun/mailbox/open/MSG-20260701-Arquitecto-to-Analista-REVIEW-TASK-0227-remediacion-5.md` |
| Handoff | `Area_comun/handoffs/HANDOFF-TASK-0227-codex-to-arquitecto-5.md` |
| Decision de frontera | `Area_comun/decisions/DECISION-0079-acota-ac-f1-guard-estatico-readonly.md` |
| Producto citado | `bbf84e714e2bff4b29fba325fa0e7a20192a1df6` |
| Repo efectivo | `D:/Agentes/Zeus/Zeus-Aegis` (`D:/Agentes/Zeus/Zeus-protocol` no contiene `bbf84e7`) |
| Clon limpio producto | `C:/Users/johnb/AppData/Local/Temp/analista-0227-rem5-c0552dd117574b13865b1e18159c7c5b/zeus-aegis` |

## Reproduccion

| Gate | Resultado |
|---|---|
| `git clone D:/Agentes/Zeus/Zeus-Aegis ...; git checkout bbf84e714e2bff4b29fba325fa0e7a20192a1df6` | EXIT 0 |
| `corepack pnpm --dir vendor/hermes-2.3.0 test` en clon limpio | EXIT 0, `governance-readonly.test.ts` 16 tests; suite full verde |
| Probe propio del guard F1, familia DECISION-0079 | EXIT 1 por slips falsables |
| Protocolo vivo `python scripts/validate_collaboration_state.py` | EXIT 0 |
| Protocolo vivo `python scripts/scan_domain_neutrality.py` | EXIT 0 |
| Protocolo vivo `python scripts/scan_encoding.py` | EXIT 0 |
| Protocolo clean clone `7953df1` validate/neutrality/encoding | EXIT 0 / 0 / 0 |
| Drift protocolo vivo y clean | `has_drift=false`, `up_to_seq=2898` antes de mi claim; `up_to_seq=2900` tras claim/release |
| `protocol.config.json` sha256 vivo/clean | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Vector por vector

| Vector probado | Resultado | Evidencia falsable |
|---|---|---|
| Caso rem-4 literal: `const opts: RequestInit = { method: 'POST' }; fetch('/api/governance/state', opts)` | PASA | `matched=true` |
| Texto pedido en REVIEW: `const method = 'POST'; const opts: RequestInit = { method }; fetch('/api/governance/state', opts)` | PASA | `matched=true` |
| Previos rem-3/rem-4: objeto local sin tipo, `new Request`, `axios.request(url,cfg)`, `axios.post`, shorthand, computed | PASA | Todos `matched=true` |
| Control display-only `submit_intent.py` sin fetch/write | PASA | `matched=false` |
| `fetch('/api/governance/state', { "method": "POST" })` | SLIPS | `matched=false` |
| `const opts: RequestInit = { "method": "POST" }; fetch('/api/governance/state', opts)` | SLIPS | `matched=false` |
| `fetch(new Request('/api/governance/state', { "method": "POST" }))` | SLIPS | `matched=false` |
| `axios.request('/api/governance/state', { "method": "POST" })` | SLIPS | `matched=false` |
| `axios({ "url": "/api/governance/state", method: "POST" })` | SLIPS | `matched=false` |

Probe minimo reproducible:

```js
const patterns = GOVERNANCE_FORBIDDEN_WRITE_PATTERNS
patterns.some((p) => p.test('void fetch("/api/governance/state", { "method": "POST" })')) // false
patterns.some((p) => p.test('const opts: RequestInit = { "method": "POST" }; void fetch("/api/governance/state", opts)')) // false
patterns.some((p) => p.test('void axios.request("/api/governance/state", { "method": "POST" })')) // false
```

## Residuales

No uso como bloqueo los write-paths expresamente fuera de DECISION-0079: metodo construido en runtime puro, helpers opacos, alias multinivel. El bloqueo se limita a claves literales entre comillas dentro de objetos literales locales/config literal, que son enumerables estaticamente.

## Recomendacion

CAMBIO-REQUERIDO. No cerrar TASK-0227 hasta que el guard cubra claves string-literal `"method"` y `"url"` en las mismas firmas ya prometidas/cubiertas, o hasta que DECISION-0079 acote explicitamente que solo cubre property identifiers sin comillas.
