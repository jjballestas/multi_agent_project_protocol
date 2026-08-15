---
id: TASK-0402
title: Un ejemplo PUBLICADO cablea una ruta de scratch de Windows que en POSIX es RELATIVA -- el adoptante escribiria el scratch DENTRO del arbol atestiguado, y nunca lo borra
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0402-un-ejemplo-publicado-cablea-una-ruta-de-scratch-que-en-posix-es-relativa.md
created: 2026-08-15
reviewer: Analista
intake:
  type: fix
  goal: >
    Residuos S2, S3 y S5 del veredicto del Analista sobre TASK-0395 r2
    (`Area_comun/artifacts/Analista-TASK-0395-r2-el-instrumento-que-si-discrimina-verdict.md`).
    Declarados NO bloqueantes para 0395 -- son patron PREEXISTENTE, no los introdujo esa entrega --
    y por eso salen como tarea propia en vez de retrasar aquel cierre.

    **S2, el grave.** `examples/mailbox_retry_cases/run_mailbox_retry_cases.py` cablea rutas del tipo
    `Path("D:/Aegis_Scratch/.../task0395-residue-path")`, en CUATRO sitios del fichero. Esto se
    PUBLICA: `examples/` es parte de lo que una instancia adoptante recibe. En Windows la ruta es
    absoluta y cae donde debe. En POSIX **no es absoluta** -- `PurePosixPath("D:/Aegis_Scratch").
    is_absolute()` es `False` -- asi que el runner crearia un directorio literalmente llamado `D:` y
    escribiria el scratch **DENTRO del arbol donde corre**.

    Las dos consecuencias, y ninguna es teorica:
    (1) Es una violacion directa de DECISION-0104: el scratch acaba dentro del arbol atestiguado, que
        es exactamente lo que esa decision declara inquebrantable.
    (2) Es el defecto que TASK-0395 acaba de reparar, reintroducido por otra puerta: un runner que
        escribe en el arbol donde corre vuelve a medir su entorno en vez del codigo.

    Y el destinatario tiene nombre: NOVA adopta esta metodologia y no tiene por que correr en Windows.

    **S3.** El `finally` limpia el sandbox y `probe.parent`, ambos DENTRO del scratch root, pero el
    scratch root **nunca se borra**. Contradice la obligacion de limpiar al stand-down.

    **S5.** `run_nul_residue_path_cases(_sandbox)` ignora el parametro que recibe, y la llamada se lo
    sigue pasando. Menor, pero es la firma de un parametro que alguien creyo que hacia algo.
  acceptance:
    - "AC1 (medir el alcance real ANTES de tocar): enumerar TODOS los sitios con ruta de scratch
      cableada en lo que se PUBLICA -- no solo los cuatro de este fichero ni solo los de 0395. El
      Analista los atribuye al patron de 0343/0359/0367, asi que el censo se DERIVA de una busqueda,
      no de esta lista."
    - "AC2 (la ruta deja de ser de un sistema operativo): las rutas de scratch se resuelven de forma
      portable, y la resolucion sale de una sola funcion, no repetida en cada sitio. El criterio no
      es que funcione en Linux: es que NO exista una constante de ruta por-plataforma repartida por
      los ejemplos."
    - "AC3 (negativo POSIX, ejecutado): una prueba demuestra que en semantica POSIX la ruta empleada
      es absoluta y NO cae dentro del arbol. Se acredita con la asercion corriendo -- vale
      `PurePosixPath(...).is_absolute()` -- no con una inspeccion visual del codigo. Este AC es el
      nucleo: sin el, el arreglo no se distingue de mover el literal."
    - "AC4 (S3, el scratch root se limpia): al terminar, el scratch root queda borrado, tambien
      cuando el caso falla. Se acredita provocando un fallo a proposito y comprobando que no queda
      nada."
    - "AC5 (S5): o el parametro de `run_nul_residue_path_cases` se usa, o se elimina de la firma y de
      la llamada. No se deja un parametro decorativo."
    - "AC6 (no se rompe lo reparado): tras el cambio, el brazo de TASK-0343 sigue en 3/3 en las
      cuatro celdas y el job `falsification-runners` sigue en success. TASK-0395 acaba de recuperar
      esa propiedad y esta tarea no puede costarla."
  verification_cmd:
    - "python examples/mailbox_retry_cases/run_mailbox_retry_cases.py"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - examples/
    - scripts/
  out_of_scope: >
    NO se toca el estimulo de TASK-0343 ni la asercion de preservacion que consume (TASK-0395, ya
    cerrada -- no reabrir su comportamiento). NO se toca el bloque del fixture de TASK-0301
    (TASK-0396, en curso) ni la asercion de `mid-log ambiguity` de la linea 2122 (TASK-0401). NO se
    tocan las causas de CI registradas por separado (TASK-0397, 0398, 0399). Esta tarea entra SOLO
    por las rutas de scratch, su limpieza y el parametro muerto de S5.
  risk: high
  estimate: M
---

# TASK-0402 -- una ruta de scratch de Windows, cableada en un ejemplo que se publica

## Procedencia

Residuos S2, S3 y S5 declarados por el Analista al dar OK-CLOSABLE a TASK-0395 r2. Los declaro yo
como tarea propia, tal y como el propuso, porque son patron preexistente (0343/0359/0367) y bloquear
0395 con ellos habria retrasado un cierre acreditado por un defecto que esa entrega no introdujo.

## Por que le pongo riesgo alto pese a no ser bloqueante aqui

Hoy no muerde: el job que ejercita este runner corre en `[self-hosted, protocol-win]`. El riesgo no
esta en nuestra CI, esta en **lo que publicamos**. Un adoptante en POSIX recibe un ejemplo que crea un
directorio `D:` dentro de su propio arbol de gobierno y no lo limpia nunca.

Es, ademas, la misma enfermedad que TASK-0395 acaba de curar -- un runner que escribe en el arbol
donde corre -- entrando por otra puerta.

-- Arquitecto, 2026-08-15
