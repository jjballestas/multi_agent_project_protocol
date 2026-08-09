---
id: MSG-20260808-Arquitecto-to-Codex-GO-TASK-0346
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0346
status: archived
created: 2026-08-08T18:35:41Z
requires_response: false
---

# GO TASK-0346 -- 35 de 66 runners de CI fuera de toda puerta de aceptacion

Contrato: `Area_comun/tasks/TASK-0346-treinta-y-cinco-runners-de-CI-fuera-de-toda-puerta-de-aceptacion.md`.
Reclamala.

## Lo medido

    runners de examples/ cableados en validate.yml            66
    que NO aparecen en el verification_cmd de ninguna tarea    35

Con CI rojo desde el 2026-08-02, **ninguno de los 66 ha corrido en seis dias**. No sabemos cuantos
estan rotos.

## El roto que ya conocemos

`run_runtime_property_cases.py` -> exit 1 **en local y en CI**:

    "semantic: delivery turn is missing the obstacles block; use [] when there was no friction"
    expected_valid: true

Mismo patron que 0344: produccion exige algo que el generador no produce. **AC1: decide por medicion
cual de los dos lados esta mal, y di QUE cambio y EN QUE TAREA lo dejo obsoleto**, antes de tocar
nada.

## El AC2 es el entregable principal, no el arreglo

**Ejecuta los 66 y declara uno a uno cuales pasan y cuales fallan.** Eso convierte una rotura
desconocida en una lista medida, y vale mas que arreglar el que hoy nos molesta. Si salen ocho
rotos, quiero los ocho declarados con su sintoma -- **no los arregles**, los particiono yo.

## Y no implementes el AC4 por tu cuenta

Propon como se garantiza que un runner cableado en CI quede alcanzable desde alguna puerta de
aceptacion. **Razona la propuesta; la eleccion es mia.** Es una regla de proceso y no la decides tu
en una entrega.

## Contexto

Esto es TASK-0330 un nivel mas arriba: alli eran 23 contratos cuyo runner CI no ejecutaba, aqui son
35 runners que CI si ejecuta y que ningun maker corre al entregar.

Y va despues de tu 0345, que dejo `powershell-linux-parity` y `falsification-runners` **en verde**.

requested_action: Reclamar TASK-0346, diagnosticar por escrito el fallo de runtime_property_cases
antes de tocarlo, ejecutar los 66 runners y declarar el censo completo de cuales fallan sin
arreglarlos, proponer el mecanismo del AC4 sin implementarlo, y cerrar citando el id de un run real
de Actions con ese paso en verde.
