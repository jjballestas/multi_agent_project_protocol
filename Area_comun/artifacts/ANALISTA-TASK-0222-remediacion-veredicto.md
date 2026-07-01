# ANALISTA TASK-0222 remediacion veredicto

Firma: Analista
Fecha: 2026-07-01
Veredicto: CAMBIO-REQUERIDO / NO-GO

## Ancla canonica

- Protocolo instruccion/HEAD: `b942389b0243ab7a4085689af6b157bdeb1bbaa8`.
- Producto bajo review: `D:/Agentes/Zeus/Zeus-Aegis` commit `a68eb34297d81a77a92c0d8fb378933f3f2796f6`.
- Clon limpio producto: `C:/Users/johnb/AppData/Local/Temp/analista-0222-remed-zeus-aegis-52ac4b8230a944329a51e0eb6c1dd714`.
- Clon limpio protocolo sin secretos: `C:/Users/johnb/AppData/Local/Temp/analista-0222-remed-protocol-clean-ca1990b4a2884b34a04470af694feb35`.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| `npm test` en clon limpio producto `a68eb34` | EXIT 1. El test de stats ya no hace timeout (`exposes token stats...` visible en 943 ms), pero la corrida full termina con `Unhandled Rejection: Error: Channel closed` / `ERR_IPC_CHANNEL_CLOSED`; por contrato el gate full sigue rojo por exit-code. |
| Targeted `corepack pnpm exec vitest run src/server/governance-readonly.test.ts --testNamePattern "token stats"` | EXIT 0. 1/1 passed, stats AC en 1142 ms, duration 2.74 s. |
| Targeted F1/stats/read-only family | EXIT 0. 3 tests passed, 12 skipped; stats AC en 1147 ms. |
| Payload propio de token scanner sobre protocolo clonado | EXIT 0. Log grande con token viejo fuera de los ultimos 128 KiB no suma; token de cola `1,234` suma a Codex; multilinea a 2 lineas suma `1.111` a Arquitecto; multilinea a 5 lineas se ignora; doble linea suma `777` a agente `Bad`. Dataset sigue `500/500`, `minSeq=2221`. |
| Protocolo vivo: `validate_collaboration_state.py` | EXIT 0. |
| Protocolo vivo: `scan_domain_neutrality.py` | EXIT 0. |
| Protocolo vivo: `scan_encoding.py` | EXIT 0. |
| Protocolo vivo drift | `has_drift=false`, `up_to_seq=2869` antes de mi claim. |
| Protocolo clean clone `b942389`: validate / neutrality / encoding / drift | EXIT 0 / EXIT 0 / EXIT 0 / `has_drift=false`, `up_to_seq=2869`. |
| `protocol.config.json` sha256 vivo/clean | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`, byte-identico. |

## Vectores

| Vector / AC | Estado | Evidencia falsable |
| --- | --- | --- |
| Full clean-clone gate | SLIPS | `npm test` obligatorio salio EXIT 1 en clon limpio de `a68eb34`. La causa observada ya no es timeout de stats, pero el cierre pedido gatea por exit-code full. |
| Stats endpoint: costo acotado, no timeout | PASA focal | Test targeted en 1142 ms y prueba propia confirma lectura de cola de 128 KiB, sin sumar tokens fuera de la cola. |
| Tokens por agente + total | PASA focal | Payload propio produjo Codex `1234`, Arquitecto `1111`, Bad `777`, total `3122`, runs `3`; el caso fuera de ventana no incremento Analista. |
| Dataset chip 500/500 | PASA | Endpoint bajo payload propio conserva `current=500`, `target=500`, `minSeq=2221`, `frozenTag=TFM-dataset-N500`; breakdown canonico suma 500. |
| Render/contrato UI de Estadisticas | PASA por test focal | El test focal comprueba presencia de `/api/governance/agent-metrics`, `Dataset:`, `Progreso dataset TFM` y `formatDatasetBreakdown`; no probe screenshot nuevo porque el gate full ya bloqueo. |
| F1 read-only estricto | PASA focal | Diff de `a68eb34^..a68eb34` toca solo `governance-readonly.ts`; no agrega rutas de escritura. Targeted F1/read-only exit 0; la superficie declarada sigue GET-only y sin `submit_intent` en rutas F1. |

## Residuales

- El blocker anterior de timeout del test de stats parece corregido.
- El producto todavia no es cerrable porque la reproduccion obligatoria en clon limpio no obtiene `npm test` EXIT 0. La falla observada es de runner IPC (`ERR_IPC_CHANNEL_CLOSED`) tras una corrida parcial, no de asercion funcional de stats.
- No encontre un escape nuevo en el scanner acotado con las familias probadas; el residuo bloqueante es estrictamente el gate full rojo.

## Recomendacion

CAMBIO-REQUERIDO. Devolver a Codex: entregar una remediacion que haga `npm test` EXIT 0 en clon limpio de HEAD, o aislar y corregir la causa reproducible del `ERR_IPC_CHANNEL_CLOSED` en la suite full. Mientras ese gate salga 1, TASK-0222 no es cerrable aunque stats/dataset/F1 pasen focalmente.
