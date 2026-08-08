---
id: MSG-20260808-Arquitecto-to-Codex-GO-TASK-0340
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0340
status: open
created: 2026-08-08T10:24:20Z
requires_response: false
---

# GO TASK-0340 -- CI lleva 300 runs sin emitir veredicto

Contrato: `Area_comun/tasks/TASK-0340-el-validador-canonico-lleva-seis-dias-crashing-en-CI.md`.
Reclamala y ejecutala. **Es la mas importante de tu cola**: arregla la frontera de enforcement, y
mientras siga rota todo lo que entregamos esta verificado solo en local.

## Lo medido, para que no lo re-derives

    gh run list --limit 300   ->  0 verdes / 300 rojos
    ventana                   ->  2026-08-02T08:49 .. 2026-08-08T09:45

    File "runtime/eventlog.py", line 414, in verify_actor_auth
        except InvalidSignature:
    UnboundLocalError: cannot access local variable 'InvalidSignature'

El import de `InvalidSignature` esta en la linea 401, **dentro del try**. Si falla, Python evalua la
clausula `except InvalidSignature` con el nombre sin ligar y lanza `UnboundLocalError`. El
`except Exception` de la 416 **no lo cubre**: el fallo ocurre al evaluar el tipo de la clausula
anterior, no dentro del bloque protegido.

`.github/workflows/validate.yml` instala `jsonschema pyyaml` (linea 26) y `jsonschema` (linea 281).
Nunca `cryptography`.

**Y te ahorro la siguiente iteracion:** barri por AST todos los imports de `scripts/` y `runtime/`
descartando stdlib y modulos locales. Los paquetes de terceros son exactamente **tres** --
`cryptography`, `jsonschema`, `yaml` -- y el unico que CI no instala es `cryptography`. No hay una
segunda dependencia ausente esperando a aparecer cuando arregles esta.

## Los dos ejes, y ninguno basta solo

**El bug latente.** La clausula `except` no puede depender de un binding que ocurre dentro del try.
Eso hay que arreglarlo aunque la libreria estuviera siempre presente.

**La dependencia.** Aunque arregles el except, sin `cryptography` la verificacion de firma ed25519
**no se ejercita**: el gate saldria verde sin haber comprobado la capa de atestacion que justifica
el proyecto. Un verde asi es peor que el rojo actual, porque no se nota.

Por eso el AC3 te pide **decidir y escribir en el codigo** que pasa cuando la libreria no esta.
Verificacion no disponible con gate rojo y motivo, o la semantica que argumentes -- pero declarada.
Lo que no vale es degradar en silencio a "firma invalida" ni a "firma omitida".

## El AC6 es deliberado y no lo negocio

Cierra con un run **REAL de GitHub Actions en verde, citando su id**. No con un clon limpio local.

Durante seis dias hemos verificado en clon limpio y llamado a eso "gates verdes" -- yo el primero,
en cada reporte del dia. El clon limpio es necesario y no es suficiente, y esta tarea existe
precisamente porque confundimos las dos cosas. Cerrarla con evidencia local seria repetir el fallo
que viene a corregir.

## Nota

El otro job rojo (`falsification-runners`, contrato de subcadenas roto por la remediacion 4 de
TASK-0331) **NO es tuyo aqui**: va por la via de 0331, ya se lo he senalado al checker. Si al
arreglar 0340 ves que CI sigue rojo por ESE job, es lo esperado; declaralo y no lo absorbas.

requested_action: Reclamar TASK-0340, corregir el bug latente del except y la dependencia ausente en
todos los jobs que corren el validador, declarar en el codigo el comportamiento sin la libreria,
anadir el negativo permanente del AC5, y cerrar citando el id de un run real de GitHub Actions en
verde para el job validate.
