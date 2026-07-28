---
task_id: TASK-0300
title: "Endurecer el harness de los crons de mailbox para ciclos de tareas del bridge de Zeus: timeout de cross-atestacion (no colgar al deadline) + TREE_KILL que limpia el arbol completo (cero procesos huerfanos)"
type: infra
status: in_review
owner: Codex
maker: Codex
checker: Analista
reviewer: Analista
phase: P2
priority: high
created_at: 2026-07-28
origin: incidente 2026-07-28 durante TASK-0298 (goal Aegis Front); directiva operador "tarea de fix ahora"
project: multi_agent_project_protocol
relates_to: [TASK-0236, TASK-0237, TASK-0298, DECISION-0095, DECISION-0018]
linked_decisions: [DECISION-0095, DECISION-0018]
file: Area_comun/tasks/TASK-0300-harden-cron-harness-zeus-bridge.md
intake:
  type: infra
  goal: Endurecer el harness de los crons de mailbox (personal/<agente>/<agente>_mailbox_cron.ps1 + personal/codex_cron_recover.ps1) para que un ciclo de tarea del BRIDGE de Zeus no (a) cuelgue el exec hasta el deadline ni (b) deje procesos huerfanos. INCIDENTE 2026-07-28 (durante TASK-0298): el exec de Codex (pid 89340) hizo la entrega core (Zeus bf0d477 + flip ledger + HANDOFF) en ~20min y luego se COLGO ~40min en la CROSS-ATESTACION (DECISION-0095); el harness lo TREE_KILLED por DEADLINE de 1h (EXEC_EXIT transient) SIN completar. Ademas el TREE_KILL NO limpio el arbol: 7 procesos node quedaron HUERFANOS ~1h (node --test + architect-runtime-launcher.mjs + architect-runtime-stub.mjs), contribuyendo al bloqueo del exec de review de la Analista. Dos fixes al HARNESS: (A) la CROSS-ATESTACION (o cualquier paso post-entrega que corre en el exec del cron) debe tener un TIMEOUT ACOTADO -> al vencer, sale/defiere LIMPIO con diagnostico, en vez de colgar hasta el deadline de 1h; (B) el TREE_KILL debe matar el ARBOL COMPLETO (hijos + nietos, incluidos node --test y las fixtures que spawnea) -> cero huerfanos tras el kill. FUERA de alcance: los hangs de PROVEEDOR del LLM (err.log 0-byte; el hang de la Analista en este incidente fue de proveedor, NO del harness) no son arreglables en el harness mas alla del deadline/retry.
  acceptance:
    - AC1 TIMEOUT DE CROSS-ATEST - el paso de cross-atestacion / post-entrega que corre dentro del exec del cron tiene un timeout acotado y configurable; al vencer, el exec SALE o DEFIERE con un diagnostico claro (no cuelga hasta el deadline de 1h). Reproducible con un cross-atest simulado lento -> el exec termina en <=timeout, no en 1h.
    - AC2 TREE_KILL LIMPIA EL ARBOL - al matar un exec (por deadline o manual), el harness mata el ARBOL COMPLETO de procesos (hijos + nietos), incluidos node --test y las fixtures spawneadas (launcher/stub). Test: spawnear un arbol de procesos hijos, disparar el kill, ASEVERAR cero procesos huerfanos del arbol despues.
    - AC3 SIN REGRESION - los execs normales (no colgados) siguen funcionando; la logica de RETRY (RETRY_SCHEDULED/backoff) y el flujo de entrega gobernada quedan intactos; no se altera el pre-gate ni el flujo maker/checker.
    - AC4 DESPLIEGUE COORDINADO (nota, no codigo de esta unidad) - el fix se aplica al harness canonico; PROPAGARLO a los 3 harnesses (personal/Codex, personal/Analista, personal/Arquitecto) y REINICIAR los crons para que tome efecto es un paso COORDINADO POSTERIOR (tras cerrar los reviews en vuelo 0297/0298), no parte del codigo de esta unidad. El maker entrega el fix; el despliegue lo coordina el Arquitecto con el operador.
  verification_cmd:
    - (test del harness: repro del cross-atest lento -> exec termina en <=timeout; repro del arbol de procesos -> TREE_KILL deja cero huerfanos. Comando exacto lo define el maker segun como se testea el .ps1.)
    - python scripts/scan_encoding.py
  scope_routes:
    - scripts/harness/peer_mailbox_cron.ps1
    - examples/mailbox_retry_cases/
    - personal/Codex/codex_mailbox_cron.ps1
    - personal/codex_cron_recover.ps1
  out_of_scope:
    - Hangs de PROVEEDOR del LLM (err.log 0-byte) -- no arreglables en el harness; el deadline/retry ya los cubre.
    - El REINICIO/despliegue de los crons -- paso coordinado posterior (tras cerrar 0297/0298), no codigo de esta unidad.
    - Los harnesses de OTROS agentes (personal/Analista, personal/Arquitecto) -- se actualizan en el despliegue coordinado, no editando el area personal de otro agente en esta unidad.
    - El codigo de producto de Zeus (el bridge en si) -- FUERA; esto es el HARNESS del cron, no el producto.
  risk: medium
  estimate: M
---

# TASK-0300 - Endurecer el harness de crons para ciclos del bridge de Zeus

> maker=Codex (autor del harness, TASK-0236/0237) / checker=Analista. Prioridad ALTA: el pipeline del
> Aegis (0298/0299 y siguientes tocan el mismo bridge) se cuelga sin este fix. Origen: incidente
> 2026-07-28 durante TASK-0298; directiva del operador "tarea de fix ahora".

## El incidente (evidencia)
- 22:28 EXEC_START (Codex, 0298). Entrega core (~20min): Zeus bf0d477 + flip ledger a in_review + HANDOFF.
- Luego ~40min COLGADO en la cross-atestacion (DECISION-0095).
- 23:28 TREE_KILL por DEADLINE de 1h; EXEC_EXIT transient (NO completo). El TREE_KILL NO limpio el arbol:
  7 node procs huerfanos (node --test + architect-runtime-launcher/stub) sobrevivieron ~1h.
- El exec de review de la Analista quedo bloqueado (contribuyo el estado sucio + su propio fallo de proveedor).
- Destrabe manual: el Arquitecto (con autorizacion del operador) mato los huerfanos + el exec colgado.

## Los 2 fixes del harness (confirmados)
1. **Timeout de cross-atest:** el paso que colgo el exec de Codex ~40min debe tener un timeout acotado ->
   salir/deferir limpio, no colgar hasta el deadline de 1h.
2. **TREE_KILL completo:** matar el arbol entero (hijos + nietos + fixtures node) -> cero huerfanos.

## Nota de despliegue
El maker entrega el fix del harness. PROPAGARLO a los 3 harnesses + REINICIAR los crons es un paso
COORDINADO posterior (tras cerrar 0297/0298), no de esta unidad. El hang de PROVEEDOR de la Analista es
un fallo separado (err.log 0-byte del LLM), fuera del alcance del harness.
