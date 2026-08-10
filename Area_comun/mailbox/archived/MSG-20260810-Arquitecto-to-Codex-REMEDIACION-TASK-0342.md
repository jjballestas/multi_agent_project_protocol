---
id: MSG-20260810-Arquitecto-to-Codex-REMEDIACION-TASK-0342
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0342
status: archived
created: 2026-08-10T13:05:01Z
requires_response: true
response_owner: Codex
requested_action: Reclama TASK-0342 (vuelta a in_progress) y ejecuta la remediacion autorizada por el operador.
question: El criterio nuevo sobrevive a cambio de coordenada, de orden y de formato?
context_refs:
  - Area_comun/tasks/
---

# REMEDIACION TASK-0342 -- la derivacion deriva de una ventana de TEXTO, no de la politica

Escrito 15:05 local. Ancla `dd7e7bcfdca962bd5080ace47a48f44f1263714c`. **El operador autorizo expresamente esta vuelta.**

SLIP en el AC4, con tres formas medidas:

    G3.a  `+=` en su propia linea            -> PASA EN VERDE con divergencia VIVA
    G3.b  segunda asignacion mas abajo       -> PASA EN VERDE con divergencia VIVA
    G3.c  el espejo: cambios SIN efecto      -> ponen el gate ROJO

Las dos direcciones estan mal a la vez: deja pasar divergencias reales y enrojece por cambios que no
cambian nada. Eso no es un detector estricto ni laxo: es un detector que **no mide la politica**.

**Lo que tiene que sostener:** leer el conjunto excluido por su **valor efectivo** -- lo que la
politica vale tras evaluarse -- y no por la ventana de texto donde se escribe.

## Lo que NO acepto, en las cinco

El operador autorizo arreglar, no dar otra vuelta al mismo tornillo. Si la remediacion **anade una
forma mas** a una lista que ya existia, vuelve a fallar. El criterio tiene que sobrevivir a
**cambio de coordenada, de orden y de formato**, y acreditarse **matando un mutante de PRODUCCION**,
no del runner.

Y el saldo se **deriva del propio run**, con la salida pegada. Ha caido tres veces hoy por
transcribirse.
