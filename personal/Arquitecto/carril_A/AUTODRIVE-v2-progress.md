# AUTODRIVE v2 - progreso de la carga por archivo v2 (Fases B->C)

> Tracker del drive. Cron Arquitecto 9954b818 cada ~5 min (session-only, 7-dias). Counter de rondas-sin-respuesta
> de Codex (parar a 7). De a UNA tarea (anti-colision). Checker DESDE CLON LIMPIO. Fase B/C exigen Analista al cierre.

## Cron Arquitecto
- job_id rota; regla adaptativa: ~30min ("11,41 * * * *") cuando Codex in_progress, */5 cuando idle.

## RUNBOOK ACTIVACION 3-WAY (DECISION-0057; permiso Bash(powershell:*) en .claude/settings.json L57)
Relanzar un cron caido (cold-start o stop stale). Verificar vivo: `cat .protocol-tmp/<name>/<name>.pid` + `powershell -NoProfile -Command "Get-Process -Id <pid> -ErrorAction SilentlyContinue"`.
- Codex:   `rm -f .protocol-tmp/codex_mailbox_cron/codex_mailbox_cron.stop` ; `powershell -NoProfile -Command "Start-Process -WindowStyle Hidden -FilePath powershell -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','D:\Agentes\multi_agent_project_protocol\personal\Codex\codex_mailbox_cron.ps1'"`
- Analista: `rm -f .protocol-tmp/analista_mailbox_cron/analista_mailbox_cron.stop` ; idem con `personal\Analista\analista_mailbox_cron.ps1`
- Ambos auto-salen a 7 rondas sin mensaje mio (costo). Relanzar cuando haya cola para ellos. NO mandarles MSG con stop/standdown+cron (se auto-detienen). Detener: crear el .stop o CronDelete + matar PID.

## Counter
- rounds_without_codex_response: 1 (CAMBIO external-cli devuelto a Codex 0d42587; aun no reclama el rework)

## RECONCILIACION (hold)
- 9 REQ listos (draft RECONCILE-reqs-intents.json) -> aplicar en ventana LIMPIA tras cerrar TASK-0153 (task_upsert done + protocol_prune + claim, gateado validate). Codex con CAMBIO blocking pendiente = NO es ventana limpia ahora.

## TASK-0153 (GO operador, precondicion uso vivo)
- Guard ALLOWLIST deny-all + eval/new Function (AC46) + aislamiento de suite del runtime del operador (AC47). SPEC-0086 +AC46/AC47. ready/Codex. maker=Codex/checker=Arquitecto+Analista. NO enciende uso vivo (OFF; GO de encendido aparte). Cierra el residual del Analista del cierre de Fase C.
- ultima actividad Codex: entrega Fase C (d1eb0cf). Pendiente rework guard AC45. HEAD==origin tras este round.

## Orden y estado
| Fase | TASK | AC | estado |
|------|------|----|--------|
| A | TASK-0150 | AC40/AC42 | DONE (Analista OK 10/10; checker clon limpio npm 42/42) |
| B | TASK-0151 | AC41/AC43/AC45c | **DONE** (5d5d1ad). Checker Arquitecto verde + Analista OK 6/6 (0bca9fb). Cierre via submit_intent seq 1106. LECCION: clasificador denego el cierre porque el veredicto del Analista estaba UNTRACKED (no en canonico); aterrizarlo primero (commit 0bca9fb) satisface genuinamente la precondicion -> cierre OK. |
| C | TASK-0152 | AC41-loop/AC45 | **DONE** (6d1ca65). Rework guard AC45 checker-verde (Zeus 3d94f11) + Analista OK->CERRABLE reverificacion (5 huecos cierran, control positivo por familia, src real [], sin regresion). Cierre submit_intent. RESIDUAL no bloqueante (clientes HTTP no listados + ofuscacion = limite scan estatico) -> FOLLOW-UP del GO de uso vivo: flip a ALLOWLIST + marcar eval/new Function. |

## CIERRE
- **Carga por archivo v2 (A+B+C) COMPLETA** (HEAD 6d1ca65). Off-by-default. Codex en stand-down (sin cola); cron detenido.
- PENDIENTE OPERADOR (GO aparte): uso vivo del extractor + follow-up allowlist (precondicion recomendada por Analista). Si lo pide, autoro pieza SDD (maker=Codex/checker=Arquitecto+Analista).

## Notas
- Uso vivo v2 OFF (versionado enabled:false; activacion por env FILE_INGESTION_CONFIG_PATH/FILE_UPLOAD_STORE_ROOT;
  GO aparte del operador). Rama 'por carga de archivo' del selector GATEADA tras B/C.
- DECISION-0056 + SPEC-0086 ext10 (AC40-AC45). Red-team REDTEAM-ingestion-v2-OPCION4-veredicto.md.
