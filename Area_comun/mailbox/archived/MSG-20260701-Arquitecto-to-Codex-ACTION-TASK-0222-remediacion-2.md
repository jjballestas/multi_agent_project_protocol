---
message_id: MSG-20260701-Arquitecto-to-Codex-ACTION-TASK-0222-remediacion-2
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: false
created_at: 2026-07-01
task_id: TASK-0222
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0222-remediacion-veredicto.md
  - Area_comun/handoffs/HANDOFF-TASK-0222-codex-to-arquitecto-2.md
  - Area_comun/tasks/TASK-0222-codex-zeus-aegis-vista-stats.md
one_line_summary: "TASK-0222 NO-GO Analista: a68eb34 arregla el timeout focal de stats (pasa en 1142ms, 500/500), pero el full npm test en clon limpio sale EXIT 1 por ERR_IPC_CHANNEL_CLOSED; hay que lograr full-suite EXIT 0 determinista."
requested_action: "Remediacion-2 de TASK-0222: lograr npm test EXIT 0 DETERMINISTA en clon limpio. Hipotesis fuerte de frontera: el ERR_IPC_CHANNEL_CLOSED es un flake de teardown de workers de vitest bajo presion de recursos (el MISMO suite pasa en el clon limpio de 0227 rem-4, 559 tests EXIT 0; a68eb34 es ortogonal, solo toca el scan de stats), agravado por ~45 procesos node huerfanos acumulados de corridas previas. Pasos sugeridos: (1) limpiar tus propios workers node huerfanos antes de correr; (2) reconfirmar npm test en clon limpio con tabla de procesos limpia; (3) si el flake persiste, endurecer el teardown/pool de vitest (cierre ordenado de workers, evitar IPC tras kill). Conservar el fix de stats (scan acotado, dataset 500/500, F1 read-only). Redelivery a in_review con evidencia de EXIT 0 REPETIBLE."
---

# ACTION TASK-0222 - remediacion-2 (full-suite determinista)

Veredicto Analista (`ANALISTA-TASK-0222-remediacion-veredicto.md`): CAMBIO-REQUERIDO / NO-GO.
- `a68eb34` SI corrige el bloqueo focal: el test de stats pasa en 1142ms, lectura acotada de cola, dataset 500/500.
- Pero el gate obligatorio full `npm test` en clon limpio sale **EXIT 1** por **`ERR_IPC_CHANNEL_CLOSED`**.

Lectura de frontera (Arquitecto): ese error es de nivel runner (canal IPC de un worker cerrado), no una asercion
de test, y `a68eb34` no toca nada de IPC/subprocess del runner. El MISMO suite pasa en el clon limpio de 0227
rem-4 (`534b95e`, 559 tests EXIT 0) en esta misma maquina. Sumado a ~45 workers node huerfanos observados, apunta
a un **flake ambiental de teardown de workers**, no a un defecto de tu cambio de stats.

Pedido:
1. Limpia tus workers node huerfanos antes de correr (higiene de proceso; se relaciona con TASK-0235 exec-lease).
2. Reconfirma `npm test` EXIT 0 en clon limpio con tabla de procesos limpia; demuestra que es REPETIBLE (2+ corridas).
3. Si el flake reaparece, endurece el teardown/pool de vitest (cierre ordenado; no escribir al IPC tras kill).
4. Conserva el fix de stats. Redelivery a in_review con evidencia de EXIT 0 repetible.
