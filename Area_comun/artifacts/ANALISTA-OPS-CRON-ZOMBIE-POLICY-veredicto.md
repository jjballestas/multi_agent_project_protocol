# ANALISTA - OPS-CRON-ZOMBIE-POLICY - Veredicto

Firma: Analista
Fecha: 2026-07-01
Veredicto: CAMBIO-REQUERIDO / NO-GO para convertir la propuesta en politica o tarea ejecutable tal como esta.

## Ancla canonica

- Instruccion REVIEW materializada en protocolo: `ba617c6` (`coord(OPS-CRON-ZOMBIE-POLICY): rutea al Analista revision adversarial de la politica de execs colgados`).
- Documento bajo revision: `personal/Arquitecto/DISCUSSION-cron-zombie-policy.md` en `ba617c6`.
- Protocolo vivo observado durante la review: `7c65448967f9e4253eec234945d48660ae371a92`.
- Producto: la instruccion no cita commit de producto. Control limpio ejecutado sobre `D:/Agentes/Zeus/Zeus-protocol` HEAD local `b2b2395da39090109db6de2dc50726dbaab1a11e`.

## Veredicto corto

La separacion conceptual A/B/C es correcta como direccion: zombie, runtime sano y causa raiz no son el mismo problema. Pero el barrido quirurgico de s.3 no es cerrable como politica porque su criterio operativo central sigue indefinido: "excluir el exec legitimamente en curso" no tiene una senal robusta, verificable y serializada. Sin esa senal, Restart Manager solo prueba posesion de handle, no prueba que el proceso sea zombie. Eso permite matar trabajo vivo, incluido el trabajo del checker.

Recomendacion: NO-GO para automatizar o normalizar el barrido. Aceptable solo como intervencion manual de emergencia con confirmacion humana, lista explicita de PIDs, start-time, command line, holder path, exclusion de la propia sesion y evidencia de lease vencido. Antes de convertirlo en tarea, especificar y testear un contrato de leases/heartbeats por exec.

## Reproduccion y gates

| Gate | Resultado |
|---|---|
| `git fetch origin` + `git status --short` | Exit 0. Arbol vivo tenia cambios ajenos no tocados; se stagearon rutas explicitas solamente. |
| `python scripts/validate_collaboration_state.py` vivo | Exit 0. Warning no bloqueante: mensaje FYI antiguo sin respuesta pendiente. |
| Drift vivo | Exit 0. `has_drift=False`, `up_to_seq=2806`. |
| `python scripts/scan_domain_neutrality.py` vivo | Exit 0. |
| `python scripts/scan_encoding.py` vivo | Exit 0. |
| `protocol.config.json` vivo | SHA256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. |
| Clean clone protocolo `ba617c6`, validate sin secretos | Exit 0. |
| Clean clone protocolo `ba617c6`, drift | Exit 0. `has_drift=False`, `up_to_seq=2804`. |
| Clean clone protocolo `ba617c6`, neutrality | Exit 0. |
| Clean clone protocolo `ba617c6`, encoding | Exit 0. |
| Clean clone protocolo `ba617c6`, `protocol.config.json` | SHA256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. |
| Clean clone producto `b2b2395`, `npm test` | Exit 0. 109 tests, 87 pass, 22 skipped. Temp: `C:/Users/johnb/AppData/Local/Temp/analista-zombie-zeus-f76f22515a884b2aaf71d9076427ff34`. |

## Tabla adversarial vector por vector

| Vector | Resultado | Evidencia falsable |
|---|---|---|
| 1. Falso positivo: lento pero vivo | SLIPS | Restart Manager identifica holders, no liveness. Un `npm test` o build silencioso puede retener handles sin escribir logs durante minutos. La propuesta no define lease renovado por el exec, start-time, deadline firmado, ni estado atomico "exec_active". "Excluyendo el exec legitimamente en curso" es una intencion, no un guard. |
| 2. PID reuse en TTL de lock | SLIPS | La propuesta menciona el riesgo, pero no lo convierte en requisito duro. Un lock viejo con solo PID permite limpiar o matar contra un PID reciclado. Cierre minimo: comparar PID + process start-time + executable path + command line + token de lease. |
| 3. Restart Manager incompleto o iterativo | RIESGO DECLARADO | El incidente ya exige iterar hasta `HOLDERS: none`. Si un holder aparece despues del snapshot, el sweep puede declarar limpieza parcial. No bloquea el diagnostico manual, pero bloquea una politica automatica sin re-scan bajo lock y limite de intentos. |
| 4. Parada graceful mid-exec | RIESGO DECLARADO | La parada graceful es preferible a force-kill, pero debe ser "stop after current turn", no matar hijo en curso. Falta contrato observable: el cron debe dejar de tomar trabajo nuevo, esperar hijo, liberar lock en finally y reportar salida. |
| 5. 24/7 vs costo | PASA con residual | Mantener crones arriba mientras REQ-ZEUS esta activo es defendible si no dispara execs sin cola. Residual: falta punto de corte explicito para stand-down tras cierre real del proceso de coordinacion. |
| 6. Carreras entre barredores | SLIPS | Dos sweepers pueden observar holders en ventanas distintas y matar procesos que el otro acaba de legitimar. Falta lock global de mantenimiento, owner unico, dry-run obligatorio y compare-and-kill contra start-time justo antes de matar. |
| 7. Auto-dano al Analista | SLIPS | La propuesta excluye cron vivo y exec en curso, pero no define como identifica el exec de review del checker ni sesiones de peers. Si el Analista esta revisando y toca un prompt/lock observado por RM, el sweep lo clasifica igual que el zombie. Necesita exclusion por session id, parent tree, start-time y lease de "review_active". |
| 8. Ledger tras kill | SLIPS | Esta vez no hubo claim huerfano, pero no hay invariante que lo garantice si se mata mid-submit_intent, mid-commit, mid-test o mid-write. Antes de matar debe probarse: no writer lock de runtime, no git operation, no process command line de submit_intent/git/npm test, y post-kill debe correr validate + drift. |

## Cambio requerido antes de volverlo politica

1. Definir un contrato de `exec lease`: cada exec escribe un lease separado con PID, process start-time, command line hash, owner, task/message id, started_at, deadline, heartbeat monotono y shutdown policy.
2. El sweep solo puede matar si el holder coincide con PID + start-time del lease, el lease esta vencido, el cron owner no reporta exec activo, y un re-check inmediato bajo lock devuelve el mismo holder.
3. Excluir por defecto la sesion del checker y cualquier owner distinto al target. El barrido de un peer no debe inspeccionar ni matar procesos de otro peer salvo orden humana explicita.
4. Serializar barredores con un lock global de mantenimiento y modo dry-run obligatorio que imprima PID, start-time, command line, holder path, lease, razon y comando de kill.
5. Antes del kill, negar si command line contiene `submit_intent`, `git`, `npm test`, `vitest`, `node --test`, `python scripts/validate_collaboration_state.py`, o si hay cambios no commiteados en rutas cubiertas por claims activas del owner.
6. Despues del kill, ejecutar validate, drift y scan_encoding; si falla, dejar mensaje DECISION-0018 y no continuar con la cola.

## Residuales

- No revise una implementacion de `sweep_cron_zombies.py` porque el documento describe una propuesta, no un patch bajo review.
- Restart Manager puede seguir siendo una buena herramienta forense manual. El NO-GO es contra convertir el barrido descrito en politica/tarea sin el contrato de liveness y serializacion anterior.
