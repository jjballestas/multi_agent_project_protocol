---
id: TASK-0363
title: La puerta de dependencias descubre el objetivo por el texto del comando, no por lo que el comando ejecuta
status: proposed
owner: Codex
file: Area_comun/tasks/TASK-0363-el-token-pegado-al-interprete-no-es-el-objetivo.md
type: fix
intake:
  type: fix
  goal: "La puerta de dependencias del workflow descubre una invocacion solo si se cumplen **dos** condiciones a la vez: (1) el token inmediatamente posterior a `python` es el propio objetivo -- una ruta terminada en `.py`, o `-m <modulo>`; y (2) ese objetivo, tal como esta escrito, resuelve a un fichero existente relativo a la raiz del repositorio. Si falla (1) -- una bandera (`-u`, `-X utf8`, `-W ignore`, `-B`), un `-c`, un envoltorio o un cambio previo de cwd -- la invocacion queda invisible y solo enrojece si la ruta relativa a la raiz aparece escrita en el mismo `run`. Si falla (2), las dos formas fallan en direcciones **opuestas**: una forma script queda fail-closed y enrojece; una forma `-m <modulo>` se descarta en silencio y el bloque queda verde. Medido sobre la poblacion DERIVADA -- las **73** invocaciones que la propia puerta cuenta (`invocations=73`) -- reescrita mecanicamente a `cd <dir> && python -u <base>`: **73 silenciosas y 0 atrapadas**, con el runner real muriendo en `ModuleNotFoundError` mientras el gate dice PASS. La cobertura se cuenta por fichero y son **72** (`referenced=72`), porque `scripts/validate_collaboration_state.py` se invoca dos veces: son dos unidades distintas, no el mismo conjunto. (Los cardinales 69 y 72 de las dos primeras redacciones se retiraron en r7 y r8: no por irre-derivables -- se re-derivan --, sino por contar la unidad equivocada bajo un criterio anclado a la forma del texto.) TASK-0354 cerro lo que podia cerrarse sin cambiar de mecanismo; esta clase exige derivar la invocacion del comando EJECUTADO y no de su texto."
  acceptance:
    - "AC1 (falsacion previa por censo, no por ejemplos): se reproduce que la reescritura mecanica de las invocaciones vivas del workflow las vuelve invisibles a la puerta, reportando el conteo completo sobre la poblacion DERIVADA del workflow y no sobre una lista de formas elegidas a mano. El conteo declara QUE UNIDAD cuenta -- invocaciones o ficheros -- y su criterio de pertenencia no ancla en la forma de la linea. Hoy son **73** invocaciones descubiertas por la puerta y **73 de 73** quedan silenciosas tras la reescritura; los **72** ficheros cubiertos (`referenced=72`) son otra unidad y no valen como corroboracion del conteo de invocaciones. Un cardinal no vale por re-derivarse: vale si declara su unidad y un criterio de pertenencia que no ancle en la forma del texto. El 69 y el 72 de las dos primeras redacciones **se re-derivan** -- son celdas de la tabla forma-por-unidad de TASK-0354 -- y aun asi eran falsos, porque contaban la unidad equivocada."
    - "AC2 (el objetivo se deriva de lo EJECUTADO, no del texto): tras el cambio, lo que la puerta identifica como objetivo es el fichero que el comando ejecutaria, no el token que aparece pegado al interprete. Se declara el mecanismo elegido y por que es una propiedad del comando y no un reconocimiento de formas."
    - "AC3 (invariante ante coordenadas incidentales): el veredicto no cambia al insertar banderas, cambiar el cwd antes de invocar, alterar el entrecomillado, el separador, el orden de los flags ni el host del job. Se falsa perturbando cada coordenada por separado Y en composicion -- la composicion es donde vivio el escape de r6: `cd` y bandera se atrapan por separado y juntas no."
    - "AC4 (no enrojece lo legitimo): las invocaciones legitimas de ficheros FUERA del repositorio (`$RUNNER_TEMP`, `/tmp`) no producen rojo. Es el residual que la remediacion de 0354 introdujo y que aqui se cierra: hoy fallan del lado seguro, pero su reparacion ingenua devuelve esas invocaciones a la clase silenciosa."
    - "AC5 (la mitad de MODULO no se traga en silencio): cuando el objetivo no resuelve contra la raiz, las dos formas fallan hoy en direcciones OPUESTAS -- una forma script queda fail-closed y enrojece, una forma `-m <modulo>` se descarta en silencio y el bloque queda verde. Tras el cambio, ninguna de las dos puede quedar silenciosa. Se falsa con `python -m generated` (hoy verde) contra `python \"$RUNNER_TEMP/generated.py\"` (hoy rojo): el mismo hecho -- el objetivo no existe en el repo -- no puede producir veredictos opuestos segun la grafia."
    - "AC6 (el verde DISCRIMINA): la bateria se corre contra el gate anterior y el nuevo bajo el mismo instrumento. El anterior debe fallar donde el nuevo acierta; un verde que ambos comparten no acredita nada."
    - "AC7 (sin regresion): arbol intacto en EXIT=0 con el conteo de invocaciones y referencias declarado, cero falsos rojos, y las puertas del repo en EXIT=0 en clon limpio CON HISTORIA COMPLETA."
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

    N2   cd <dir> && python <base>       EXIT=1   (rechaza el token: no resuelve; no es que viera el runner)
    F1   cd <dir> && python -u <base>    EXIT=0   SILENCIOSA

**Una bandera.** Y no es un caso de laboratorio: aplicando esa reescritura a la poblacion derivada del
workflow -- las **73** invocaciones que la propia puerta cuenta -- quedan **73 silenciosas y 0
atrapadas**. La cobertura es otra unidad: **72** ficheros distintos, porque
`scripts/validate_collaboration_state.py` se invoca dos veces.

Sobre un runner real con dependencia real, quitandole su `pyyaml` al job que la declara, el gate dice
`PASS` mientras el runner muere en `ModuleNotFoundError`. El control sin ocultar
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
