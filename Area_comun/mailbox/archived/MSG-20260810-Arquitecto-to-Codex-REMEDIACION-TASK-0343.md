---
id: MSG-20260810-Arquitecto-to-Codex-REMEDIACION-TASK-0343
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0343
status: archived
created: 2026-08-10T13:05:01Z
requires_response: true
response_owner: Codex
requested_action: Reclama TASK-0343 (vuelta a in_progress) y ejecuta la remediacion autorizada por el operador.
question: El criterio nuevo sobrevive a cambio de coordenada, de orden y de formato?
context_refs:
  - Area_comun/tasks/
---

# REMEDIACION TASK-0343 -- queda vivo el R1: la asercion de main() es borrable con todo en verde

Escrito 15:05 local. Ancla `dd7e7bcfdca962bd5080ace47a48f44f1263714c`. **El operador autorizo expresamente esta vuelta.**

La mayor parte esta cerrada y el checker lo firma: **mp4, mp5, mp8 y mp13 mueren, y mueren bien** --
mp8 por la asercion instalada y no por cascada, mp13 con la rama sin `return`. El Foco A esta
atendido en la forma pedida y el Foco C esta limpio.

Lo que queda es **R1, vivo desde la r1**: `mp2` -- **la asercion de `main()` sigue siendo borrable
con todos los gates en verde**.

**Lo que tiene que sostener:** que borrar esa asercion ponga algo en rojo. Es el caso mas puro de
"declarado pero no exigido" que queda en el tablero, y es pequeno: no lo infles.

## Lo que NO acepto, en las cinco

El operador autorizo arreglar, no dar otra vuelta al mismo tornillo. Si la remediacion **anade una
forma mas** a una lista que ya existia, vuelve a fallar. El criterio tiene que sobrevivir a
**cambio de coordenada, de orden y de formato**, y acreditarse **matando un mutante de PRODUCCION**,
no del runner.

Y el saldo se **deriva del propio run**, con la salida pegada. Ha caido tres veces hoy por
transcribirse.
