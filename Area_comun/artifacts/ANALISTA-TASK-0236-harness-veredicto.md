# Veredicto Analista - TASK-0236 harness

Firma: Analista
Fecha: 2026-07-02

## Veredicto

OK/CERRABLE para TASK-0236 en la ancla canonica revisada. No encontre escape nuevo bloqueante contra los cinco vectores pedidos ni regresion de lo verde de TASK-0235.

## Ancla canonica

- Protocolo bajo review: `3523ecb` (`coord(TASK-0236): commitea entrega de Codex...`).
- Producto de control: `D:/Agentes/Zeus/Zeus-protocol` clean clone en commit `b2b2395da39090109db6de2dc50726dbaab1a11e` (la instruccion no cito commit de producto distinto).
- Clean clone usado: `C:/Users/johnb/AppData/Local/Temp/analista-0236-d785e14512aa4be79a1708a33b45c55c`.
- #4 `protocol.config.json` sha256: `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.

## Reproduccion y gates

| Gate | Resultado |
| --- | --- |
| `git fetch origin` + `git status --short` vivo | EXIT 0; hay cambios ajenos/untracked no tocados, principalmente TASK-0237/Codex y areas personales. |
| `python scripts/validate_collaboration_state.py` vivo | EXIT 0. |
| Clean clone protocolo `3523ecb`: `python scripts/validate_collaboration_state.py` | EXIT 0. |
| Clean clone protocolo `3523ecb`: `python scripts/scan_domain_neutrality.py` | EXIT 0. |
| Clean clone protocolo `3523ecb`: `python scripts/scan_encoding.py` | EXIT 0. |
| Clean clone protocolo `3523ecb`: drift via `runtime.protocol_replay.protocol_state_drift` | EXIT 0; `has_drift=false`, `up_to_seq=3041`. |
| Vivo: neutrality / encoding / drift | EXIT 0 / EXIT 0 / EXIT 0; vivo `has_drift=false`, `up_to_seq=3043`. |
| Producto clean clone `Zeus-protocol` `npm test` | EXIT 0; 109 tests, 87 pass, 22 skipped. |
| `python -m py_compile scripts/sweep_cron_zombies.py scripts/test_exec_lease_harness.py` | EXIT 0. |
| Parser PowerShell de los tres harnesses | EXIT 0; Codex, Analista y Arquitecto parsean sin errores. |
| `python scripts/test_exec_lease_harness.py` | EXIT 0; 9/9 PASS. |

## Tabla vector por vector

| Vector / AC | Estado | Evidencia adversarial |
| --- | --- | --- |
| V1 prompt por exec en `runs/` | PASA | Los tres harnesses escriben prompt runtime bajo `RunsDir` con sufijo `.prompt.txt` y redirigen stdin a ese path por ejecucion. El test permanente `test_harnesses_use_per_exec_prompt_files` pasa. No queda prompt compartido activo para Codex/Analista; Arquitecto conserva `arquitecto_cron.prompt.txt` solo como fuente de plantilla y genera prompt runtime por ciclo. |
| V2 deadline kill de arbol completo | PASA | Los tres harnesses usan `taskkill.exe /PID <pid> /T /F` en `Stop-LeaseProcessTree`; parser verde. El test permanente `test_harnesses_use_tree_kill_and_single_instance_guard` pasa. |
| V2 deny-kill de 0235 conservado | PASA | `Stop-LeaseProcessTree` conserva deny por cmdline para `submit_intent`, `git`, `npm test`, `vitest` y `validate_collaboration_state`; `sweep_cron_zombies.py` conserva deny tokens, dry-run default y recheck. Tests `test_owner_and_checker_exclusions`, `test_dry_run_is_default` y cleanup dead PID pasan. |
| V3 instancia unica | PASA | Los tres harnesses tienen `Test-ExistingCronInstance`, persisten pid + `process_start_time_utc` con `Write-CronPid`, y salen con `INSTANCE_ALREADY_RUNNING` si el pid vivo matchea. Test permanente pasa. |
| V4 lease huerfana vencida | PASA | `Clear-StaleCronLockIfSafe` valida pid+start-time, limpia PID muerto sin esperar deadline, y para lease vivo vencido invoca tree-kill antes de borrar lock+lease. En Arquitecto se invoca una vez al arranque antes del guard de instancia unica; en Codex/Analista tambien antes de procesar mensajes. Test `test_self_heal_does_not_wait_for_deadline_before_dead_pid_cleanup` pasa. |
| V5 orden de corte exacta | PASA | Los tres detectores comparan `requested_action` o `one_line_summary` con igualdad exacta `-ceq "STOP_JOB"` y no escanean el cuerpo. Test `test_stop_order_requires_exact_line_not_contains` pasa; un mensaje que solo menciona el token en prosa no dispara stop. |
| Regresion TASK-0235 self-heal PID muerto | PASA | `test_dead_process_cleans_only` y `test_kill_mode_cleanup_only_removes_lock_and_lease` pasan. |
| Regresion TASK-0235 dry-run sweeper | PASA | `test_dry_run_is_default` pasa y `sweep_cron_zombies.py` requiere `--kill` para matar/limpiar. |

## Residuales declarados

- La instruccion generica exigia `npm test` en `Zeus-protocol`; no cito un commit de producto concreto. Use el HEAD local clonado `b2b2395da39090109db6de2dc50726dbaab1a11e`, verde.
- Los tests permanentes de TASK-0236 son mayoritariamente estructurales sobre los harnesses, no una ejecucion end-to-end del cron real con `codex exec` colgado. Aun asi, cubren los contratos que causaron el jam: prompt por ejecucion, tree-kill, instancia unica, lease vencida y stop exacto.
- El deny-kill por cmdline sigue siendo una heuristica textual; no encontre regresion respecto a TASK-0235, pero no lo convierto en garantia criptografica.

## Recomendacion

CERRABLE. Arquitecto puede ratificar review_approved y coordinar el redespliegue de los harnesses de TASK-0236.
