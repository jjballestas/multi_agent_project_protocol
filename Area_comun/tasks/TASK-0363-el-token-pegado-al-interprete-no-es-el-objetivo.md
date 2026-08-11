---
id: TASK-0363
title: La puerta de dependencias descubre el objetivo por el texto del comando, no por lo que el comando ejecuta
status: proposed
owner: Codex
file: Area_comun/tasks/TASK-0363-el-token-pegado-al-interprete-no-es-el-objetivo.md
type: fix
intake:
  type: fix
  goal: "La puerta de dependencias del workflow solo descubre una invocacion si el token inmediatamente posterior a `python` es el propio objetivo (`.py` o `-m modulo`), y solo enrojece si la ruta relativa a la raiz aparece literal en el mismo `run`. Una bandera (`-u`, `-X utf8`, `-W ignore`, `-B`), un `-c`, un envoltorio o un cambio previo de cwd la dejan invisible. Medido en el censo completo del workflow: los **69** pasos `run: python <ruta>.py`, reescritos mecanicamente a `cd <dir> && python -u <base>`, quedan **69 silenciosos y 0 atrapados**, con el runner real muriendo en `ModuleNotFoundError` mientras el gate dice PASS. TASK-0354 cerro lo que podia cerrarse sin cambiar de mecanismo; esta clase exige derivar la invocacion del comando EJECUTADO y no de su texto."
  acceptance:
    - "AC1 (falsacion previa por censo, no por ejemplos): se reproduce que la reescritura mecanica de las invocaciones vivas del workflow las vuelve invisibles a la puerta, reportando el conteo completo sobre la poblacion DERIVADA del workflow y no sobre una lista de formas elegidas a mano. Hoy ese conteo es 69 de 69."
    - "AC2 (el objetivo se deriva de lo EJECUTADO, no del texto): tras el cambio, lo que la puerta identifica como objetivo es el fichero que el comando ejecutaria, no el token que aparece pegado al interprete. Se declara el mecanismo elegido y por que es una propiedad del comando y no un reconocimiento de formas."
    - "AC3 (invariante ante coordenadas incidentales): el veredicto no cambia al insertar banderas, cambiar el cwd antes de invocar, alterar el entrecomillado, el separador, el orden de los flags ni el host del job. Se falsa perturbando cada coordenada por separado Y en composicion -- la composicion es donde vivio el escape de r6: `cd` y bandera se atrapan por separado y juntas no."
    - "AC4 (no enrojece lo legitimo): las invocaciones legitimas de ficheros FUERA del repositorio (`$RUNNER_TEMP`, `/tmp`) no producen rojo. Es el residual que la remediacion de 0354 introdujo y que aqui se cierra: hoy fallan del lado seguro, pero su reparacion ingenua devuelve esas invocaciones a la clase silenciosa."
    - "AC5 (el verde DISCRIMINA): la bateria se corre contra el gate anterior y el nuevo bajo el mismo instrumento. El anterior debe fallar donde el nuevo acierta; un verde que ambos comparten no acredita nada."
    - "AC6 (sin regresion): arbol intacto en EXIT=0 con el conteo de invocaciones y referencias declarado, cero falsos rojos, y las puertas del repo en EXIT=0 en clon limpio CON HISTORIA COMPLETA."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - .github/workflows/validate.yml
  out_of_scope:
    - "G2, la clausura transitiva de imports locales: la superficie termina en el fichero del runner descubierto, como ya declaro TASK-0354."
    - "Acreditar en un run REAL de Actions: la facturacion sigue bloqueada y es decision del operador."
    - "Reabrir el mecanismo de TASK-0354: aquella cerro lo que podia cerrarse sin cambiar de mecanismo y su balance 9+3 esta verificado."
  risk: medium
  estimate: M
---

# TASK-0363 -- el token pegado al interprete no es el objetivo

Sale del veredicto r6 de TASK-0354, donde el checker declaro explicitamente que **no** pedia una
cuarta vuelta de mecanismo -- lo firmo en r5 y lo sostuvo -- y escalo el hecho de fondo como clase
propia.

## La propiedad, medida

    N2   cd <dir> && python <base>       EXIT=1   atrapada
    F1   cd <dir> && python -u <base>    EXIT=0   SILENCIOSA

**Una bandera.** Y no es un caso de laboratorio: aplicando esa reescritura a los **69** pasos
`run: python <ruta>.py` del workflow, quedan **69 silenciosos y 0 atrapados**.

Sobre un runner real con dependencia real, quitandole su `pyyaml` al job que la declara, el gate dice
`PASS invocations=72` mientras el runner muere en `ModuleNotFoundError`. El control sin ocultar
enrojece: **la puerta funciona cuando ve**, y el problema es todo lo que no ve.

## Por que es una tarea y no una remediacion mas

Las tres vueltas de 0354 fueron estrechando la forma reconocida sin cambiar **que** se reconoce: el
texto del comando. Mientras el objetivo se deduzca del token pegado al interprete, cada vuelta cierra
las grafias que alguien enumero y deja abiertas las que no. La unica salida es cambiar la pregunta:
**?que fichero ejecutaria este comando?** en vez de **?que ruta aparece escrita en el?**

El arbol de HOY no esta roto -- cero `working-directory`, cero `cd` en bloques `run`, cero banderas
intermedias -- asi que esto no es una urgencia: es una deuda con nombre y con censo.

## La composicion es el sitio donde vive el escape

`cd` sola se atrapa. Una bandera sola se atrapa. **Juntas, no.** Por eso el AC3 exige perturbar cada
coordenada por separado **y en composicion**: muestrear ejes uno a uno no muestrea el producto, que
es la leccion que esta instancia lleva repitiendo desde el 8 de agosto.
