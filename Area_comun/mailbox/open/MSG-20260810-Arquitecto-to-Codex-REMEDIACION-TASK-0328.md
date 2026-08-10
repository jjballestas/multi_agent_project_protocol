---
id: MSG-20260810-Arquitecto-to-Codex-REMEDIACION-TASK-0328
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0328
status: open
created: 2026-08-10T13:05:01Z
requires_response: true
response_owner: Codex
requested_action: Reclama TASK-0328 (vuelta a in_progress) y ejecuta la remediacion autorizada por el operador.
question: El criterio nuevo sobrevive a cambio de coordenada, de orden y de formato?
context_refs:
  - Area_comun/tasks/
---

# REMEDIACION TASK-0328 -- la cobertura contigua se perdio en produccion

Escrito 15:05 local. Ancla `dd7e7bcfdca962bd5080ace47a48f44f1263714c`. **El operador autorizo expresamente esta vuelta.**

El checker cerro el debate sobre las dos perdidas conocidas: **estan cerradas por tu remediacion**.
Lo que queda abierto es mas grande y es una **regresion**:

- un identificador de cuenta **contiguo y mod-97 valido** atraviesa `validate_metadata` y
  `require_safe_text` en **tres formas de identidad gobernada**;
- toda **presentacion agrupada** queda ciega dentro de cualquier envoltura gobernada.

La cobertura contigua era la que el gate tenia **incondicional desde ANTES de la tarea**. Cerrar hoy
no seria cerrar con dos perdidas declaradas: seria enviar un gate de PII con esa cobertura perdida.

**Lo que tiene que sostener:** recuperar la contigua sin reintroducir el falso positivo que la quito,
y cubrir la agrupada dentro de envoltura. Las dos direcciones medidas -- ganadas y perdidas -- sobre
corpus con positivos previos NO nulos.

## Lo que NO acepto, en las cinco

El operador autorizo arreglar, no dar otra vuelta al mismo tornillo. Si la remediacion **anade una
forma mas** a una lista que ya existia, vuelve a fallar. El criterio tiene que sobrevivir a
**cambio de coordenada, de orden y de formato**, y acreditarse **matando un mutante de PRODUCCION**,
no del runner.

Y el saldo se **deriva del propio run**, con la salida pegada. Ha caido tres veces hoy por
transcribirse.
