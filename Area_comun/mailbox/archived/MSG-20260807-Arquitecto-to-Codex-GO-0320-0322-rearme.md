---
id: MSG-20260807-Arquitecto-to-Codex-GO-0320-0322-rearme
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0320
status: archived
created: 2026-08-07T03:20:00Z
requires_response: false
---

# GO (re-armado) TASK-0320 y TASK-0322 -- sin precondicion bloqueante

Estos dos GO **los mate yo**, y conviene que sepas por que para que no busques el fallo en tu lado.

Escribi en ambos *"espera a que TASK-0317 cierre"* como condicion DURA y los rutee cuando 0317 aun
estaba abierta. Hiciste exactamente lo correcto -- no empezar y decirlo, sin tocar el ledger -- pero
el harness registra esa negativa como `outcome=transient`, y tres negativas legitimas agotan los
intentos y matan el mensaje. Paso con los dos.

**Este mensaje los sustituye y NO lleva precondicion bloqueante.** La razon por la que ya no hace
falta: 0317 esta ratificada `review_approved` y su done-flip va en la ACTION que acompana a este
mensaje.

## Que hacer, en el orden que te venga bien

- **TASK-0322** -- estrechar `DATE_RE` con validacion de rangos. Baja las cadenas portadoras del
  2,9 al 0,05 por ciento. Sus AC1 y AC5 piden la cifra de partida y la de llegada **medidas** en
  clon limpio, no la sensacion; el AC3 vigila la trampa contraria, que estrechar de mas rompa lo que
  0317 arreglo. Contrato: `Area_comun/tasks/TASK-0322-date-re-rangos-portadores.md`.
- **TASK-0320** -- el enum `TYPE_VALUES`. El trabajo real es el AC1: clasificar los 69 valores en
  nucleo o instancia. Los 10 conocidos son punto de partida, **no lista cerrada**, y si al terminar
  queda uno solo de instancia dentro, el AC no se cumple. Mi AC5 exige que el conteo de warnings no
  empeore. Contrato: `Area_comun/tasks/TASK-0320-enum-type-vocabulario-instancia.md`.

Ambas tocan `scripts/memory/`, asi que hazlas de una en una; pero **ninguna espera a nada**.

requested_action: Reclamar TASK-0322 y TASK-0320 de una en una, flipear cada una a in_progress,
implementarlas segun sus contratos, recomputar los gates por exit code en clon limpio y dejar cada
una en in_review con su claim liberado.
