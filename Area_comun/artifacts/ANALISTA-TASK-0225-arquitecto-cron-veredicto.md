# ANALISTA TASK-0225 -- Arquitecto-cron headless

Firma: Analista

## Veredicto

CAMBIO-REQUERIDO / NO-GO. No recomiendo cierre de TASK-0225.

Motivo bloqueante falsable: el dry-run canonico no detecta tareas in_review reales de la familia WS/TASK-02 cuando las filas de TASK_INDEX no tienen campo `project`. En el commit de entrega `15c02b2`, `TASK-0225` y `TASK-0226` estan `in_review` en `Area_comun/state/TASK_INDEX.json`, pero `personal/Arquitecto/arquitecto_cron.ps1 -DryRunOnce` devuelve `ws_snapshot.in_review=[]` y decide `promote_one_ready_task`. Eso incumple el DoD: "Dry-run documentado (un ciclo en seco que muestre: lee estado, detecta WS, decide promover/revisar)".

## Ancla canonica

- Protocolo HEAD observado: `4e9fd4dcefc6eb67da8b35323e81866dca59e14c` (`origin/main` igual).
- Implementacion bajo review: `a1cecb275d853f64cdaa4701d65cc50dc8e685af`.
- Handoff/delivery bajo review: `15c02b2787850b81e8835c7a3d02481e0fda39d7`.
- Producto Zeus-protocol: la instruccion no cita commit de producto especifico; use clon limpio de control en `b2b2395da39090109db6de2dc50726dbaab1a11e`.

## Reproduccion

| Gate | Resultado |
|---|---|
| `git fetch origin` + `git status --short` | Exit 0; arbol vivo tenia cambios ajenos sin tocar. |
| JSON state con `utf-8-sig` | Exit 0; todos los `Area_comun/state/*.json` parsean. |
| `python scripts/validate_collaboration_state.py` vivo | Exit 0; solo warnings preexistentes de mailbox FYI. |
| Producto limpio `npm test` en `C:/Users/johnb/AppData/Local/Temp/zeus-protocol-review-0225-1af028626b324a7eac6517dba5772f3a` | Exit 0; 109 tests, 87 pass, 22 skipped. |
| Protocolo limpio `15c02b2`, parser PowerShell de `arquitecto_cron.ps1` | Exit 0; `PARSE_OK`. |
| Protocolo limpio `15c02b2`, `powershell ... arquitecto_cron.ps1 -DryRunOnce` | Exit 0; `ledger_write=false`, pero `in_review=[]` y `decision=promote_one_ready_task` pese a TASK-0225/TASK-0226 `in_review` en TASK_INDEX. |
| `git diff --check a1cecb2^ a1cecb2 -- personal/Arquitecto/arquitecto_cron.ps1 personal/Arquitecto/ARQUITECTO_CRON_RUNBOOK.md Area_comun/tasks/TASK-0225-codex-construir-arquitecto-cron.md` | Exit 0. |
| Gates protocolo vivo: validate, scan_domain_neutrality, scan_encoding | Exit 0. Drift: `has_drift=false`, `up_to_seq=2752`. |
| Gates protocolo clean clone `4e9fd4d`: validate, scan_domain_neutrality, scan_encoding | Exit 0. Drift: `has_drift=false`, `up_to_seq=2746`. |
| `protocol.config.json` byte-identica | SHA256 `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354` vivo y clean clone. |

## Vectores

| Vector / AC | Resultado | Evidencia falsable |
|---|---|---|
| Harness presente, parseable y con pid/log/seen/lock/stop/runs | PASA | Parser PowerShell exit 0; estructura presente en `a1cecb2`. |
| Prompt cableado por STDIN | PASA | `Start-Process` usa `-RedirectStandardInput $PromptRuntimePath`; prompt fuente existe en `personal/Arquitecto/arquitecto_cron.prompt.txt`. |
| El script no escribe ledger por si mismo | PASA con residual | Static check encuentra escrituras solo en `.protocol-tmp` (`WriteAllText`, `Set-Content` pid, lock/log/seen/prompt); la unica lectura de `Area_comun/state` esta en `Get-WsSnapshot`. Residual: el runtime invocado puede escribir si el prompt lo ordena; eso queda fuera del dry-run y bajo rieles de Arquitecto. |
| Dry-run no escribe ledger | PASA | `-DryRunOnce` exit 0 y `ledger_write=false`; no invoca `Invoke-ArquitectoCycle`. |
| Dry-run detecta WS en revision y decide revisar/ratificar | SLIP BLOQUEANTE | En `15c02b2`, `TASK-0225` y `TASK-0226` estan `in_review` en TASK_INDEX, pero dry-run devuelve `in_review=[]` y `decision=promote_one_ready_task`. |
| Familia adversarial del clasificador `Get-WsSnapshot` | SLIP BLOQUEANTE | Payload propio con una tarea `TASK-0299`, titulo `REQ-ZEUS WS review candidate`, `status=in_review`, sin `project`: `decision=no_action`, `in_review=0`. El mismo payload con `project=multi_agent_project_protocol` o `project=Zeus-protocol` da `decision=review_or_ratify`, `in_review=1`. El filtro `($_.project -in ...) -and (...)` descarta filas canonicas sin `project`. |
| Stop-order / lock / seen espejo estructural | PASA parcial | El patron y archivos existen y son consistentes en forma con los crons de Codex/Analista. No cierro semantica viva de parada porque no lance loop real, por restriccion de operador. |

## Residuales

- No ejecute el loop vivo ni invoque runtime de Arquitecto; revise el dry-run y la estructura del harness.
- No hay commit de producto citado por la instruccion; el gate de producto fue control sobre Zeus-protocol `b2b2395`.
- El hallazgo no depende de nombres de test: sale de ejecutar el harness contra el estado canonico de `15c02b2` y de payloads propios sobre la familia `in_review` con/sin `project`.

## Recomendacion

CAMBIO-REQUERIDO. No cerrar TASK-0225 hasta que `Get-WsSnapshot` deje de depender de `project` como filtro obligatorio o el ledger garantice ese campo para todas las filas relevantes, y exista prueba negativa permanente que cubra al menos: tarea `TASK-02xx` `in_review` sin `project`, tarea WS/REQ-ZEUS `in_review` sin `project`, y tarea `ready` que no debe promoverse cuando existe cualquier `in_review` relevante.
