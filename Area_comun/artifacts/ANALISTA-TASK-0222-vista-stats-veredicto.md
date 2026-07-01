# ANALISTA TASK-0222 vista stats veredicto

Firma: Analista
Fecha: 2026-07-01
Veredicto: CAMBIO-REQUERIDO / NO-GO

## Ancla canonica

- Protocolo instruccion/HEAD: `3c39541655fe5540b3042e1ff50cd5443506a630`.
- Producto bajo review: `D:/Agentes/Zeus/Zeus-Aegis` commit `ff82538f31abb45cc4314fd396051a81e62dfe24`.
- Clon limpio producto: `C:/Users/johnb/AppData/Local/Temp/analista-0222-zeus-aegis-c86962bd130948cd9612e9afa8ab5be5`.
- Clon limpio protocolo: `C:/Users/johnb/AppData/Local/Temp/analista-0222-protocol-cee01171f623430591f78ee615aa1dc6`.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| `npm test` en clon limpio producto `ff82538f` | EXIT 1. Falla `src/server/governance-readonly.test.ts`: `exposes token stats and frozen dataset progress through the read-only stats endpoint` timeout a 30000 ms. |
| Targeted `corepack pnpm --dir vendor/hermes-2.3.0 exec vitest run src/server/governance-readonly.test.ts --testTimeout=60000` | EXIT 1. Misma prueba falla por timeout interno a 30000 ms; 13/14 pasan. |
| Endpoint `/api/governance/agent-metrics` en dev server limpio | HTTP 200. Dataset `500/500`, tag `TFM-dataset-N500`, minSeq `2221`, breakdown `Analista=52, Arquitecto=253, Codex=195`; tokens total `85116211`, agents `5`. |
| Render limpio `/governance` + seccion Estadisticas | PASS funcional. Screenshot: `C:/Users/johnb/AppData/Local/Temp/analista-0222-zeus-aegis-c86962bd130948cd9612e9afa8ab5be5/vendor/hermes-2.3.0/task0222-analista-stats-render.png`; DOM contiene `Estadisticas`, `Dataset:`, `500/500`, `Arquitecto`, `Codex`, `Analista`. |
| Protocolo vivo: `validate_collaboration_state.py` | EXIT 0, con warning no bloqueante de mailbox FYI antiguo. |
| Protocolo vivo: `scan_domain_neutrality.py` | EXIT 0. |
| Protocolo vivo: `scan_encoding.py` | EXIT 0. |
| Protocolo vivo drift | `has_drift=false`, `up_to_seq=2795` antes de mi claim; clean clone `has_drift=false`, `up_to_seq=2795`. |
| Protocolo clean clone `3c39541`: validate / neutrality / encoding | EXIT 0 / EXIT 0 / EXIT 0. |
| `protocol.config.json` sha256 vivo/clean | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. |

## Vectores

| Vector / AC | Estado | Evidencia falsable |
| --- | --- | --- |
| Full clean-clone gate | SLIPS | `npm test` es obligatorio y salio EXIT 1 en el clon limpio del commit citado. No es cerrable por contrato aunque endpoint/render pasen. |
| Stats endpoint tokens por agente + total | PASA funcional | Llamada HTTP 200 al endpoint devuelve agentes y total; incluye Arquitecto/Codex/Analista. |
| Dataset chip contra corpus sellado N=500 | PASA funcional | Endpoint devuelve `current=500`, `target=500`, `frozenTag=TFM-dataset-N500`, `minSeq=2221`, breakdown suma 500. |
| Render Estadisticas en clon limpio | PASA funcional | Chrome headless contra dev server limpio mostro la seccion y genero screenshot local. |
| F1 read-only routes | PASA en la superficie cambiada | Diff de `ff82538^..ff82538` no introduce `fetch`, metodo write, `submit_intent`, `writeFile`, `appendFile`, `execFile`, `spawn`, ni rutas `Area_comun/state`; los route files de governance siguen GET-only. |
| Test permanente del AC principal | SLIPS | El test agregado para stats/dataset existe, pero no es verde bajo el timeout que el propio test declara. |

## Residuales

- El endpoint tarda alrededor de 15.7 s en llamada directa local; en la suite conjunta excede el timeout interno de 30 s. Eso sugiere costo de lectura/calculo no acotado o timeout de test mal calibrado. Mientras `npm test` no sea verde en clon limpio, no separo esto como flake aceptable.
- El screenshot se tomo usando Chrome instalado (`C:/Program Files/Google/Chrome/Application/chrome.exe`) porque el browser empaquetado de Playwright no estaba instalado en el clon.

## Recomendacion

CAMBIO-REQUERIDO. Devolver a Codex: hacer que `npm test` pase en clon limpio para `ff82538` o su remediacion, endureciendo el endpoint/test de stats para que el AC `token stats + frozen dataset progress` sea verde de forma repetible bajo el timeout del repo.
