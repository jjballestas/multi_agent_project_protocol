# AUTODRIVE v2 - progreso de la carga por archivo v2 (Fases B->C)

> Tracker del drive. Cron Arquitecto 9954b818 cada ~5 min (session-only, 7-dias). Counter de rondas-sin-respuesta
> de Codex (parar a 7). De a UNA tarea (anti-colision). Checker DESDE CLON LIMPIO. Fase B/C exigen Analista al cierre.

## Cron
- job_id: 9954b818. Stand-down = CronDelete 9954b818 (o CronList).

## Counter
- rounds_without_codex_response: 5 (CAMBIO-REQUERIDO guard AC45 devuelto a Codex a3c75a9; aun no re-reclama; a 7 -> stand-down)
- ultima actividad Codex: entrega Fase C (d1eb0cf). Pendiente rework guard AC45. HEAD==origin tras este round.

## Orden y estado
| Fase | TASK | AC | estado |
|------|------|----|--------|
| A | TASK-0150 | AC40/AC42 | DONE (Analista OK 10/10; checker clon limpio npm 42/42) |
| B | TASK-0151 | AC41/AC43/AC45c | **DONE** (5d5d1ad). Checker Arquitecto verde + Analista OK 6/6 (0bca9fb). Cierre via submit_intent seq 1106. LECCION: clasificador denego el cierre porque el veredicto del Analista estaba UNTRACKED (no en canonico); aterrizarlo primero (commit 0bca9fb) satisface genuinamente la precondicion -> cierre OK. |
| C | TASK-0152 | AC41-loop/AC45 | **CAMBIO REQUERIDO** (Analista, vector 1). Guard AC45 SLIPS por COMPORTAMIENTO en `await import("openai")`, `await import("undici")` (ejemplo del operador), `net.connect` por import bare, `axios/got` -- los must-catch del operador; control positivo solo ejercita fetch. Vectores 2-6 PASAN (purga/TTL, loop off+consent+cero-egress, fuera-ledger, carry, #4 byte-id). Sin breach vivo (extractor deterministic-local) pero la teeth de AC45 no cierra `await import(...)`. DEVUELTO a Codex (MSG CAMBIO-guard-AC45): ampliar familia (import dinamico + bare net/tls/dgram/http/https/dns + clientes undici/axios/got) o FLIP a allowlist + control positivo POR patron; re-entrega in_review -> checker -> Analista re-verifica -> cierro. |

## Notas
- Uso vivo v2 OFF (versionado enabled:false; activacion por env FILE_INGESTION_CONFIG_PATH/FILE_UPLOAD_STORE_ROOT;
  GO aparte del operador). Rama 'por carga de archivo' del selector GATEADA tras B/C.
- DECISION-0056 + SPEC-0086 ext10 (AC40-AC45). Red-team REDTEAM-ingestion-v2-OPCION4-veredicto.md.
