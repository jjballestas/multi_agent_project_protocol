---
message_id: MSG-20260622-Arquitecto-to-Operador-CIERRE-carga-archivo-v2
task_id: TASK-0152
type: FYI
from: Arquitecto
to: Operador
status: open
requires_response: false
response_owner: Operador
one_line_summary: "CARGA POR ARCHIVO v2 (OPCION 4) COMPLETA: Fase A (TASK-0150) + Fase B (TASK-0151) + Fase C (TASK-0152) DONE. Todo checker Arquitecto + Analista. Off-by-default; canonico verde HEAD 6d1ca65; #4 byte-identica epoca 1.14.0. PENDIENTE TUYO antes del USO VIVO del extractor (GO aparte): el Analista recomienda endurecer el guard a ALLOWLIST + marcar eval/new Function (cierra clientes HTTP no listados y ofuscacion; residual inherente del scan estatico, NO bloqueo el cierre). Cron de monitoreo detenido."
context_refs:
  - Area_comun/tasks/TASK-0152-codex-file-intake-v2-faseC.md
  - Area_comun/artifacts/ANALISTA-TASK-0152-guard-AC45-reverificacion.md
  - Area_comun/decisions/DECISION-0056-file-ingestion-v2.md
deadline_or_blocking_level: normal
---

# CIERRE - carga por archivo v2 (OPCION 4) COMPLETA

Las tres fases de la carga por archivo v2 estan **done**, cada una con checker Arquitecto (clon limpio) +
pasada del Analista (DECISION-0056):

| Fase | Tarea | Que entrega | Estado |
|------|-------|-------------|--------|
| A | TASK-0150 | upload no-extractivo + screening de ingest (no-MODELO-egress, SHA-256, store os-tmp) | DONE |
| B | TASK-0151 | panel de candidatas no-ledger + GATE HUMANO DURO de PII (aprobar sin declarar -> 409) + re-screen | DONE |
| C | TASK-0152 | agente extractor (AC41, off-by-default, consent, deterministic-local, cero egress) + guard de red AC45 a TODO src/** + purga/TTL del raw | DONE |

## Garantias verificadas
- **Cero MODELO-egress vivo:** el extractor entregado es `deterministic-local` (no abre SDK/socket); `networkEgress:false`.
- **Gate humano de PII duro:** ninguna candidata entra al intake sin que declares PII revisada (409); el texto
  editado se re-screenea con los mismos guards.
- **Fuera del dataset atestado:** candidatas/estados de extraccion viven en os-tmp, NO en el ledger; #4 byte-identica
  (epoca 1.14.0); drift 0.
- **Guard AC45:** scan estatico sobre TODO `src/**` que marca fetch/import dinamico/SDKs/clientes
  HTTP (undici/axios/got/node-fetch)/sockets bare; control positivo por familia; el git push gobernado allowlisted.

## PENDIENTE TUYO antes del USO VIVO del extractor (GO aparte; sigue OFF-by-default)
El Analista declaro un **residual no bloqueante** (limite inherente del scan estatico denylist): aun escaparian
clientes HTTP **no listados** (phin/needle/bent/ky) y **ofuscacion deliberada** (eval/computed-global). No es
regresion ni material para el cierre (la ruta realista `await import("openai")` SI queda cerrada), pero **antes
de encender el agente contra archivos reales** conviene el follow-up que recomienda:
- **Flip del guard a ALLOWLIST** (marcar cualquier import/require fuera de una lista permitida) + marcar
  `eval(`/`new Function(`. Cierra de raiz los clientes-no-listados y la ofuscacion.

Cuando quieras, autoro ese endurecimiento como pieza SDD (maker=Codex/checker=Arquitecto+Analista) y lo dejamos
listo como precondicion del GO de uso vivo.

## Estado
Canonico verde: HEAD==origin **6d1ca65**, validate con/sin secretos exit 0, drift 0, #4 byte-identica. Cron de
monitoreo detenido; Codex en stand-down (sin cola). Puedo re-armar el cron / reactivar a Codex cuando lo indiques.
Canal ASCII.
