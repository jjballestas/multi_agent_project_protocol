---
artifact_id: ANALISTA-TASK-0223-vista-instanciar-veredicto
task_id: TASK-0223
author: Analista
created_at: 2026-07-01
verdict: GO-CERRABLE
product_repo: D:/Agentes/Zeus/Zeus-Aegis
product_commit: 4ff95d929e41c13c04750c2ebed1947978724896
protocol_instruction_commit: 7c65448967f9e4253eec234945d48660ae371a92
protocol_live_head: d88f5f2
---

# Veredicto Analista - TASK-0223 vista Instanciar proyecto

## Veredicto

GO/CERRABLE.

No encontre escape bloqueante en el alcance pedido: la vista Instanciar proyecto se sostiene como F1 read-only en modo preparar-comando, genera texto para copiar, no ejecuta `new_instance.py`, no expone write-path de governance, y el texto de comando contiene el guard visible "El panel NO escribe el ledger".

Firma: Analista.

## Ancla canonica

| Elemento | Valor |
| --- | --- |
| Instruccion REVIEW | `Area_comun/mailbox/open/MSG-20260701-Arquitecto-to-Analista-REVIEW-TASK-0223-vista-instanciar.md` |
| Commit protocolo que introdujo la instruccion | `7c65448967f9e4253eec234945d48660ae371a92` |
| HEAD protocolo vivo durante review | `d88f5f2` |
| Producto bajo review | `D:/Agentes/Zeus/Zeus-Aegis` |
| Commit producto bajo review | `4ff95d929e41c13c04750c2ebed1947978724896` |
| Clean clone producto | `C:/Users/johnb/AppData/Local/Temp/analista-0223-zeus-aegis-9b29a374d46a4b03be4800b25584cf01` |
| Clean clone protocolo | `C:/Users/johnb/AppData/Local/Temp/analista-0223-protocol-3bd9adae194940e6aba48a9c669f57f0` |

## Reproduccion

| Gate | Resultado |
| --- | --- |
| `git clone D:/Agentes/Zeus/Zeus-Aegis <tmp>; git checkout 4ff95d9` | exit 0, HEAD `4ff95d929e41c13c04750c2ebed1947978724896` |
| `npm test` en clean clone producto | exit 0; `governance-readonly.test.ts` 15 tests; suite completa verde |
| Payloads propios sobre `buildInstancePlan`/guard | exit 0; 5 payloads; guard presente; sin superficie de ejecucion de `new_instance.py` |
| Render local `/governance` via Vite + Chrome headless | exit 0; dialog `Instanciar proyecto` renderiza; screenshot `C:/Users/johnb/AppData/Local/Temp/task0223-analista-instancing-render.png` |
| Render: requests de escritura a `/api/governance` | 0 requests `POST/PUT/PATCH/DELETE` |
| Protocolo vivo: `python scripts/validate_collaboration_state.py` | exit 0 |
| Protocolo vivo: `python scripts/scan_domain_neutrality.py` | exit 0 |
| Protocolo vivo: `python scripts/scan_encoding.py` | exit 0 |
| Protocolo vivo: drift por `runtime.protocol_replay.protocol_state_drift(Path("."))` | `has_drift=false`, `up_to_seq=2811` |
| Clean protocolo `7c65448`: validate/neutrality/encoding | exit 0 / exit 0 / exit 0 |
| Clean protocolo `7c65448`: drift | `has_drift=false`, `up_to_seq=2804` |
| `protocol.config.json` sha256 vivo y clean | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Vector por vector

| Vector / AC | Veredicto | Evidencia falsable |
| --- | --- | --- |
| F1 read-only estricto en la vista | PASA | En `governance.tsx`, los `fetch` de la pantalla son GET/read-only (`cache: no-store`) hacia `/api/governance/*`; el test permanente verifica que las rutas `GOVERNANCE_READONLY_ENDPOINTS` solo exponen `GET:` y que no hay `POST/PUT/PATCH/DELETE` en rutas governance. La prueba de render capturo 0 requests de escritura a `/api/governance`. |
| Modo preparar-comando no ejecuta | PASA | `buildInstancePlan` devuelve JSON/string con `mode: "prepare-command-only"` y comando textual; el boton solo llama `setInstancePlan(buildInstancePlan(...))`. No hay `spawn`, `exec`, `execFile` ni `fetch` asociado a `new_instance.py` en la vista. |
| Guard visible junto a `new_instance.py` | PASA | Las ocurrencias de `new_instance.py` quedan cerca de `NO escribe el ledger` / `no ejecuta`; el modal renderizado contiene `El panel NO escribe el ledger` y `no ejecuta new_instance.py`. |
| Guard visible junto a `submit_intent` heredado de archivado | PASA | Las ocurrencias de `submit_intent` en la misma pantalla quedan cercanas a `NO escribe el ledger` o a comentario read-only; no hay endpoint de escritura asociado. |
| Inputs adversariales de proyecto/ruta | PASA | Payloads `../Bad;$(calc)`, `../outside`, `C:\\tmp\\ACME; rm -rf x`, vacios y con espacios/unicode fueron normalizados por `projectEntityId`/`sanitizeInstanceRoot`; no sobreviven `..` ni metacaracteres peligrosos en `project_id`; el plan sigue incluyendo guard y modo copy-only. |
| Render en clon limpio | PASA | Vite local renderizo `/governance`, se abrio la seccion Instanciar proyecto, se genero el dialogo y se tomo screenshot. |
| `npm test` en clon limpio | PASA | exit 0 en el commit producto citado. |

## Residuales declarados

- La prueba de render uso Chrome del sistema (`channel: chrome`) porque el browser empaquetado de Playwright no estaba instalado en el clean clone. No afecta el gate de producto: `npm test` salio exit 0 y el render fue funcional.
- La vista sigue siendo copy-only: si un operador copia y ejecuta el comando fuera del panel, eso pertenece a F2/ceremonia externa y no a este cierre F1.

## Recomendacion de cierre

OK->CERRABLE para TASK-0223.
