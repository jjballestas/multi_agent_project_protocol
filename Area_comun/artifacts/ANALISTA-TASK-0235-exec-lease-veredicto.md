---
artifact_id: ANALISTA-TASK-0235-exec-lease-veredicto
task_id: TASK-0235
type: review_verdict
author: Analista
created_at: 2026-07-01
status: final
---

# Veredicto Analista - TASK-0235 exec-lease

## Veredicto

CAMBIO-REQUERIDO / NO-GO.

La entrega pasa los gates declarados y el producto control `Zeus-protocol` sigue verde en clon limpio. Pero el caso
real que disparo TASK-0235 sigue vivo: si el exec muere antes de su deadline largo, el lock y el lease no se limpian
hasta que venza el deadline. Con `ExecTimeoutSeconds=3600`, eso mantiene la cola bloqueada hasta 1 hora aunque el
PID ya no matchee por PID+start-time.

Hay un segundo slip falsable: `sweep_cron_zombies.py --kill` clasifica un lease vencido con proceso muerto como
`cleanup_only`, pero no elimina ni el lock ni el lease. Devuelve EXIT 0 y deja el atasco intacto.

Firma: Analista.

## Ancla canonica

| Item | Valor |
|---|---|
| Protocolo HEAD vivo / instruccion REVIEW | `710cf60993b5961052b2e79afa476b54e03b810b` |
| Implementacion bajo review | `c4c15be075aaaea81c53bd06695caed9f6efa663` |
| Instruccion REVIEW | `Area_comun/mailbox/open/MSG-20260701-Arquitecto-to-Analista-REVIEW-TASK-0235-exec-lease.md` |
| Handoff | `Area_comun/handoffs/HANDOFF-TASK-0235-codex-to-arquitecto-1.md` |
| Producto generico pedido por prompt | `D:/Agentes/Zeus/Zeus-protocol` |
| Commit producto control | `b2b2395da39090109db6de2dc50726dbaab1a11e` |
| Clon limpio protocolo | `C:/Users/johnb/AppData/Local/Temp/analista-0235-s_chkkte/protocol` |
| Clon limpio producto control | `C:/Users/johnb/AppData/Local/Temp/analista-0235-s_chkkte/zeus-protocol` |

## Reproduccion

| Gate | Resultado |
|---|---|
| `npm test` en clon limpio `Zeus-protocol` | EXIT 0; 109 tests, 87 pass, 22 skipped |
| `python -m py_compile scripts/sweep_cron_zombies.py scripts/test_exec_lease_harness.py` | EXIT 0 |
| Parser PowerShell de ambos harnesses | EXIT 0 |
| `python scripts/test_exec_lease_harness.py` en clon limpio protocolo | EXIT 0 |
| Protocolo clean `python scripts/validate_collaboration_state.py --root .` | EXIT 0 |
| Protocolo clean `python scripts/scan_domain_neutrality.py --root .` | EXIT 0 |
| Protocolo clean `python scripts/scan_encoding.py --root .` | EXIT 0 |
| Protocolo clean drift | `has_drift=false`, `up_to_seq=2884` |
| Protocolo vivo `python scripts/validate_collaboration_state.py` | EXIT 0 |
| Protocolo vivo `python scripts/scan_domain_neutrality.py` | EXIT 0 |
| Protocolo vivo `python scripts/scan_encoding.py` | EXIT 0 |
| Protocolo vivo drift antes del claim | `has_drift=false`, `up_to_seq=2912` |
| `protocol.config.json` sha256 vivo y clean | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Vectores

| Vector | Resultado | Evidencia falsable |
|---|---|---|
| Lease por exec contiene owner, msg/task id, PID, start-time, cmdline hash, deadline, heartbeat y policy | PASA | Test de contrato en ambos harnesses EXIT 0 |
| Deadline vencido + PID muerto en `Clear-StaleCronLockIfSafe` | PASA | Probe propio: lock=false, lease=false, EXIT 0 |
| PID muerto antes del deadline en `Clear-StaleCronLockIfSafe` | SLIPS | Probe propio sobre la funcion real: `lock_exists=true`, `lease_exists=true`, EXIT 1 |
| Deadline enforcement para proceso vivo vencido | PASA PARCIAL | Hay loop con `Stop-ExpiredLeaseProcess` y revalidacion PID+start-time; no encontre escape nuevo en ese camino |
| Stop graceful / stop-after-current-turn | PASA PARCIAL | El harness no toma trabajo nuevo al ver stop marker y espera al hijo en curso; no mata por stop marker |
| Sweeper dry-run por defecto | PASA | `python scripts/test_exec_lease_harness.py` valida `mode == dry-run` |
| Sweeper owner/checker exclusion | PASA | `owner_not_target` y `checker_owner_excluded` en probe declarado y reproducido |
| Sweeper PID-reuse guard | PASA | Codigo requiere `process_start_time_utc` igual antes de kill; no use como bloqueo |
| Sweeper deny-kill de comandos sensibles | PASA PARCIAL | Tokens principales estan listados; no probe todos los alias, pero no hace falta para el bloqueo |
| Sweeper `--kill` con lease vencido y proceso muerto | SLIPS | Devuelve EXIT 0 con `action=cleanup_only`, `killed=[]`, `post_validate={}` y deja `lock_exists=true`, `lease_exists=true` |
| Post-kill validator + drift + encoding | PASA PARCIAL | Existe solo si `killed` no vacio; el caso cleanup-only no valida ni limpia |

## Residuales

No bloqueo por cobertura de cmdlines no listadas ni por kills reales de procesos vivos: el fallo ya aparece sin
matar nada y reproduce el incidente original. Tampoco uso el working tree vivo como ancla de producto; el producto
control fue clonado y testeado aparte.

## Recomendacion

NO CERRABLE.

Requisito minimo de remediacion: si el lease apunta a un PID que no matchea por PID+start-time, limpiar lock+lease
sin esperar al deadline; si el proceso aun matchea, entonces respetar deadline para no matar trabajo vivo. Ademas,
`sweep_cron_zombies.py --kill` debe materializar `cleanup_only` eliminando lock+lease o fallar duro; un EXIT 0 que
deja el lock huerfano no resuelve TASK-0235.
