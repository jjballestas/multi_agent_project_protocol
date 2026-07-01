# ANALISTA TASK-0227 remediacion-4 veredicto

Firma: Analista

Veredicto: CAMBIO-REQUERIDO / NO-GO.

Ancla canonica:
- Protocolo HEAD vivo al adquirir claim de review: `c4c15be075aaaea81c53bd06695caed9f6efa663`
- Instruccion REVIEW materializada en: `2a881e6db3e1e9910ee747525494053676fc08db`
- Producto citado por la instruccion: `534b95eaaf952be81c635aedab528e6663041e1e`
- Nota de ancla: `D:/Agentes/Zeus/Zeus-protocol` no contiene `534b95e`; el commit citado existe en `D:/Agentes/Zeus/Zeus-Aegis`, que coincide con el handoff de Codex.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| `git clone D:/Agentes/Zeus/Zeus-protocol` + `git checkout 534b95e` | EXIT 1: commit no existe en ese repo |
| `git clone D:/Agentes/Zeus/Zeus-Aegis` + `git checkout 534b95e` | EXIT 0, HEAD `534b95eaaf952be81c635aedab528e6663041e1e` |
| Producto clean clone `npm test` | EXIT 0, incluye `src/server/governance-readonly.test.ts` 16 tests |
| Probe propio de guard F1 acotado | EXIT 1 por un slip nuevo dentro del AC acotado |
| Protocolo vivo `python scripts/validate_collaboration_state.py` | EXIT 0 |
| Protocolo limpio `python scripts/validate_collaboration_state.py` | EXIT 0 |
| Protocolo vivo `python scripts/scan_domain_neutrality.py` | EXIT 0 |
| Protocolo limpio `python scripts/scan_domain_neutrality.py` | EXIT 0 |
| Protocolo vivo `python scripts/scan_encoding.py` | EXIT 0 |
| Protocolo limpio `python scripts/scan_encoding.py` | EXIT 0 |
| Drift protocolo vivo | `has_drift=false`, `up_to_seq=2886` tras release del claim de review |
| Drift protocolo limpio | `has_drift=false`, `up_to_seq=2877` |
| `protocol.config.json` sha256 | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

Clean clones usados:
- Producto: `C:/Users/johnb/AppData/Local/Temp/analista-0227-rem4-0977876a2d4e48c89be806b704728d22/zeus-aegis`
- Control producto pedido: `C:/Users/johnb/AppData/Local/Temp/analista-0227-rem4-0977876a2d4e48c89be806b704728d22/zeus-protocol`
- Protocolo: `C:/Users/johnb/AppData/Local/Temp/analista-0227-rem4-0977876a2d4e48c89be806b704728d22/protocol-clean`

## Vector por vector

| Vector | Resultado | Evidencia falsable |
| --- | --- | --- |
| `npm test` en clon limpio producto | PASA | EXIT 0 en `534b95e`; 82 files / 559 tests reportados por la suite |
| `governance-readonly.test.ts` | PASA | Integrado en `npm test`; 16 tests pasan |
| `const opts = { method: 'POST' }; fetch('/api/governance/state', opts)` | PASA | Probe propio: matched=true |
| `fetch(new Request('/api/governance/state', { method: 'POST' }))` | PASA | Probe propio: matched=true |
| `axios.request('/api/governance/state', { method: 'POST' })` | PASA | Probe propio: matched=true |
| Display-only `submit_intent.py` | PASA | Probe propio: matched=false |
| `const opts: RequestInit = { method: 'POST' }; fetch('/api/governance/state', opts)` | SLIPS | Probe propio: matched=false |

## Residuales

DECISION-0079 acota el lint a firmas enumerables literales y deja fuera los write-paths puramente dinamicos. El slip reportado no es una construccion dinamica: es el mismo objeto local con `method` literal pasado a `fetch`, solo con anotacion TypeScript `RequestInit`, una forma normal y estaticamente enumerable en este codigo base.

La garantia backend read-only sigue siendo el control duro y el `npm test` ya esta verde. Aun asi, contra el AC acotado escrito en DECISION-0079, el guard estatico no atrapa toda la familia prometida de "objeto de opciones local con method literal".

Recomendacion: CAMBIO-REQUERIDO. Anadir negativo permanente para objeto local tipado (`const opts: RequestInit = { method: 'POST' }`) o acotar DECISION-0079 todavia mas para excluir objetos locales con anotacion TypeScript. Con el AC actual, TASK-0227 remediacion-4 no es cerrable.
