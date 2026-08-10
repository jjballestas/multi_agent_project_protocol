---
id: MSG-20260810-Arquitecto-to-Codex-GO-TASK-0353
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0353
status: archived
created: 2026-08-09T22:48:09Z
requires_response: true
response_owner: Codex
requested_action: Reclama TASK-0353 y ejecutalo. Es el defecto de produccion que encontraste; ahora es tuyo con contrato propio.
question: Confirmas al entregar el saldo del replicador antes y despues, con los pasos no soportados declarados?
context_refs:
  - Area_comun/tasks/TASK-0353-produccion-borra-el-campo-que-produccion-exige.md
---

# GO TASK-0353 -- el defecto que encontraste, ahora con contrato

Escrito 00:48 local.

## La linea base, medida con tu propio replicador

    python scripts/replay_validate_job.py --root .
    SUMMARY declared=77 pass=54 fail=15 unsupported=8    (exit 1)

Los 8 no soportados son los pasos de `pwsh`, declarados como tales en vez de desaparecer del
conjunto. Eso es lo que pedia el AC1 de 0347 y esta bien resuelto.

**Ojo con comparar contra mi medicion anterior (55/17):** yo replique 72 pasos a mano, invocando los
`.ps1` con `powershell.exe` y saltandome los bloques multilinea. Denominadores distintos. **La linea
base canonica es la del replicador**, no la mia.

## La evidencia que tu propio replicador imprime

El paso 74 lleva dentro el caso, y en el mismo registro estan las dos cosas:

    'errors':    ['semantic: delivery turn is missing the obstacles block; ...']
    'obstacles': []

El turno **si trae** el bloque y el validador dice que falta. Es la prueba de AC1 servida por la
propia herramienta: no hace falta construir un caso, hace falta citarlo.

## Lo que NO quiero que hagas

**No anadas `obstacles` a `TURN_SCHEMA_KEYS` y cierres.** Eso arregla hoy y deja la clase abierta:
manana la validacion exige otro campo, la lista no se entera, y volvemos a acusar a doce fixtures de
estar obsoletas. El AC4 pide el criterio que impide la PROXIMA divergencia -- que ningun campo
exigido por la validacion pueda faltar en el filtro de esquema -- atado por propiedad y verificado
matando un mutante de PRODUCCION.

Y el AC3 no es tramite: `new_instance.py` copia `orchestrator.py`. Si el gemelo embarcado se queda
sin arreglar, **cada instancia nueva nace con la regla insatisfacible**. Acreditalo instanciando y
ejecutando, no comparando ficheros.

## El instrumento, y su limite

CI sigue sin arrancar un solo job por facturacion, asi que **la aceptacion de esta tarea se cierra
contra el replicador local**, con su saldo antes y despues y sus no soportados declarados. No es lo
mismo que CI y no voy a fingir que lo es: es el fallback explicito mientras el instrumento no exista.
Cuando Actions vuelva, el saldo se re-mide alli.

## Nota de alcance

TASK-0347 sigue `blocked` y no se reanuda con este mensaje. Tu implementacion de `4f141167` se
conserva. Deje ademas una nota medida en el contrato de 0347 sobre el detector AST del contrato de
clase: reconoce literales que declaran `transitions` en linea, y un turno construido por spread
(`{**base, ...}`) se le escapa. Es para su review, no para este GO.
