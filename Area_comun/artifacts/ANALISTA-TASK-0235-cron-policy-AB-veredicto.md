# ANALISTA - TASK-0235 cron policy A/B - Veredicto

Firma: Analista
Fecha: 2026-07-02
Veredicto: CAMBIO-REQUERIDO / NO-GO de cierre canonico.

## Ancla canonica

- Instruccion REVIEW: `Area_comun/mailbox/open/MSG-20260702-Arquitecto-to-Analista-REVIEW-cron-policy-AB.md`.
- HEAD de protocolo que materializa la instruccion: `cc1dac4a411217d5e0291e73d27fefe37c7b9f3e`.
- Documento bajo review: `personal/Arquitecto/DISCUSSION-cron-zombie-policy.md` en ese HEAD.
- Tarea de implementacion cerrada citada: `Area_comun/tasks/TASK-0235-exec-lease-cron-harness-hardening.md`.
- Producto: la instruccion no cita commit de producto; use control limpio `D:/Agentes/Zeus/Zeus-protocol` HEAD local
  `b2b2395da39090109db6de2dc50726dbaab1a11e`.

## Veredicto corto

La politica A/B, tomada junto con el contrato ya cerrado en TASK-0235, corrige los dos riesgos que bloquearon mi
primer dictamen: el barrido ya no se basa en Restart Manager como prueba de zombie, sino en lease vencido con
PID + start-time, re-check, dry-run por defecto, exclusions y deny-list; y la baja de runtime sano queda como
stop-after-current-turn, no force-kill.

Sustantivamente A/B es cerrable como politica si la decision conserva esas condiciones duras. Pero NO recomiendo
cierre canonico en este disparo porque el protocolo anclado `cc1dac4` falla el gate secretless de validacion en
clon limpio: `TASK-0229` y `TASK-0237` tienen mismatch entre TASK_INDEX y task file. El workspace vivo valida por
cambios locales ajenos no commiteados; eso no sirve como ancla canonica.

## Reproduccion y gates

| Gate | Resultado |
|---|---|
| `git fetch origin` + `git status --short` vivo | Exit 0. Habia cambios ajenos en `TASK-0229`, `TASK-0237` y `personal/Codex/Memory.md`; no los toque. |
| `python scripts/validate_collaboration_state.py` vivo | Exit 0. |
| Drift vivo | Exit 0. `has_drift=false`, `up_to_seq=3032`. |
| `python scripts/scan_domain_neutrality.py` vivo | Exit 0. |
| `python scripts/scan_encoding.py --root .` vivo | Exit 0. |
| `protocol.config.json` vivo | SHA256 `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`. |
| Clean clone protocolo `cc1dac4`, validate sin secretos | Exit 1. `TASK-0229 status mismatch: index='blocked' file='ready'`; `TASK-0237 status mismatch: index='in_progress' file='ready'`. |
| Clean clone protocolo `cc1dac4`, drift | Exit 0. `has_drift=false`, `up_to_seq=3028`. |
| Clean clone protocolo `cc1dac4`, neutrality | Exit 0. |
| Clean clone protocolo `cc1dac4`, encoding | Exit 0. |
| Clean clone protocolo `cc1dac4`, `protocol.config.json` | SHA256 `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`. |
| Clean clone producto `b2b2395`, `npm test` | Exit 0. 109 tests, 87 pass, 22 skipped. Temp: `C:/Users/johnb/AppData/Local/Temp/analista-cron-policy-ab-6956b96b35364048adb38eaba696d770`. |

## Tabla adversarial

| Vector | Resultado | Evidencia falsable |
|---|---|---|
| A/#1 falso positivo: exec lento pero vivo | PASA sustantivo | Probe propio sobre `scripts/sweep_cron_zombies.py`: lease de `Codex` con proceso vivo y deadline futuro devuelve `action=skip`, `reason=lease_not_expired`, exit 0. La politica ya no permite matar solo porque un holder existe. |
| A/#1 falso positivo: trabajo vivo pero peligroso | PASA con condicion | TASK-0235 agrega deny-list antes del kill (`submit_intent`, `git`, `npm test`, `vitest`, `node --test`, `validate_collaboration_state.py`) y dirty claimed route. Condicion de cierre: la decision debe copiar esa lista como requisito, no dejarlo como implementacion accidental. |
| A/#2 PID reuse | PASA | El sweep exige match de PID + `process_start_time_utc`; si no coincide, devuelve `pid_reuse_start_time_mismatch`. El self-heal de los harnesses tambien usa PID + start-time antes de limpiar. |
| A/#3 Restart Manager incompleto | PASA con residual | La implementacion bajo 0235 no usa Restart Manager como autorizacion suficiente para matar; el kill depende del lease vencido y re-check. Residual: Restart Manager puede seguir siendo forense manual, no criterio unico de verdad. |
| B/#4 baja graceful mid-exec | PASA | Los harnesses implementan `shutdown_policy=stop_after_current_turn`: stop marker deja de tomar trabajo nuevo, espera el exec en curso y limpia lock/lease en `finally`. No hay force-kill de runtime sano. |
| #5 24/7 vs costo | PASA con residual | Mantener crones headless mientras REQ-ZEUS esta activo no ejecuta trabajo por si solo; el corte queda ligado a cierre real de coordinacion u orden del operador. Residual: la decision debe nombrar explicitamente ese punto de corte. |
| #6 carreras entre barredores | PASA | `sweep_cron_zombies.py` usa lock global `.protocol-tmp/cron_zombie_sweeper.lock` y re-check antes de kill/cleanup. |
| #7 auto-dano al Analista | PASA sustantivo | Probe propio: al barrer `--owner Codex --checker-owner Analista`, una lease `owner=Analista` devuelve `owner_not_target`; al barrer `--owner Analista --checker-owner Analista`, devuelve `checker_owner_excluded`. Esto protege el exec del checker si se invoca con checker-owner correcto. |
| #7 configuracion erronea del checker | RIESGO DECLARADO | El default del script es `checker-owner=Arquitecto`. Para una decision de politica, la invocacion operativa debe fijar el checker real de la ventana; si se barre `Analista` desde un contexto donde el checker tambien es Analista sin pasar ese flag, el default no lo protege. |
| #8 ledger tras kill | PASA con condicion | El sweep valida despues de matar (`validate`, drift, encoding) y niega comandos de ledger/git/test antes del kill. Condicion: si post-kill falla, la politica debe exigir DECISION-0018 y frenar cola, no seguir. |

## Residuales

- El producto `Zeus-protocol` no participa materialmente en A/B; se corrio `npm test` por el contrato de review.
- Mi NO-GO es de cierre canonico por gate secretless rojo en `cc1dac4`, no por la seguridad sustantiva de A/B.
- No toque ni arregle los mismatches de `TASK-0229`/`TASK-0237` porque pertenecen a cambios ajenos en curso.

## Recomendacion

CAMBIO-REQUERIDO antes de convertir A/B en DECISION: commitear o reanclar un HEAD donde el gate secretless
`python scripts/validate_collaboration_state.py` sea exit 0. Con ese reanclaje, A/B es CERRABLE si la decision
incluye como texto normativo: lease vencido PID+start-time, dry-run por defecto, re-check bajo lock, owner target
unico, checker-owner explicito, deny-list, dirty-claimed-route guard y post-kill validate/drift/encoding.
