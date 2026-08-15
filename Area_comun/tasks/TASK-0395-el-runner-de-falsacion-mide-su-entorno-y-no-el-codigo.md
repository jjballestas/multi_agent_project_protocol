---
id: TASK-0395
title: El runner de falsacion mide su ENTORNO y no el codigo -- lee el arbol de trabajo vivo, y por eso da verde en clon limpio y rojo en CI sobre el MISMO commit
status: in_progress
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0395-el-runner-de-falsacion-mide-su-entorno-y-no-el-codigo.md
created: 2026-08-15
reviewer: Analista
intake:
  type: fix
  goal: >
    PRIORIDAD DECLARADA POR EL OPERADOR. `examples/mailbox_retry_cases/run_mailbox_retry_cases.py`
    NO es hermetico: consulta el estado del arbol de trabajo donde se ejecuta. Por eso el mismo
    commit da resultados distintos segun quien lo corra, y por eso la CI del protocolo lleva 60 runs
    sin un solo verde. Medido por el Arquitecto el 2026-08-15 sobre el commit `47cc9184`, tres brazos
    con el MISMO codigo: (1) CLON LIMPIO recien clonado -> `TASK0343_MAIN_ASSERTION_EXECUTION
    baseline=3/3 short_circuit=3/3 tautology=3/3 unreachable=3/3`, `PASS`, **exit 0**; (2) ARBOL VIVO
    con un exec de peon escribiendo encima -> **exit 1** en `run_nul_residue_path_cases`, con
    `AssertionError: stale UTF-8 residue did not age: 'live'`; (3) CI en runner propio -> **exit 1**
    con `baseline caught_runs=0`. La prueba directa de la causa es el brazo (2): ese caso LEE el
    residuo real del working tree y comprueba si ha envejecido; con otro proceso escribiendo, sale
    `live` en vez de `aborted`. Consecuencia en cadena, ya pagada: el gate rojo impidio entregar
    TASK-0367, su claim no se libero, y eso bloqueo TASK-0337 y TASK-0391 -- las correcciones
    comprometidas con la instancia NOVA. Y lo mas grave del caso: **esto es un runner de FALSACION**,
    cuyo trabajo es demostrar que los controles saben decir que no. Un verificador cuyo veredicto
    depende de quien mas este escribiendo en el disco no verifica de forma reproducible, que es
    exactamente lo que DECISION-0115 clausula 4 obliga a declarar y excluir.
  acceptance:
    - "AC1 (hermetico o excluido, y se elige con la medicion delante): el runner deja de leer el
      arbol de trabajo donde corre -- monta su propio sandbox y consulta SOLO ese -- o se DECLARA no
      idempotente y se EXCLUYE del gate, como manda DECISION-0115 clausula 4. Las dos salidas son
      aceptables; lo que no lo es es dejarlo como esta. Se acredita con el par: mismo commit, arbol
      LIMPIO y arbol SUCIO A PROPOSITO, MISMO exit code."
    - "AC2 (concurrencia): mismo commit, misma corrida, con un proceso escribiendo ficheros en el
      arbol durante la ejecucion -> mismo exit code que sin el. Es el brazo (2) de la medicion, que
      hoy diverge."
    - "AC3 (dos corridas, DECISION-0115): dos ejecuciones consecutivas sobre el mismo commit dan el
      mismo resultado. Si no lo dan tras el arreglo, se declara no idempotente y se excluye,
      documentando que deja de cubrir."
    - "AC4 (prueba de que sigue RECHAZANDO): los mutantes que hoy si caza -- short_circuit,
      tautology, unreachable -- siguen muriendo tras el cambio. Un runner hermetico que deje de
      matar mutantes es peor que uno irreproducible: se acredita con los tres en exit 1 y el control
      en 0."
    - "AC5 (CI vuelve a verde por esta via): tras el arreglo, el job `falsification-runners` pasa en
      el runner propio. Se acredita con el run de CI, no con una corrida local -- el clon limpio
      local YA daba verde y es justamente lo que oculto el problema durante semanas."
  verification_cmd:
    - "python examples/mailbox_retry_cases/run_mailbox_retry_cases.py"
    - "python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
  out_of_scope:
    - "El segundo job rojo de CI, `falsification-runners-python` (`semantic: agent not registered:
      Codex` y `prune_state.py not found` en el runner de turnos). Es otro fallo, probablemente de
      entorno de la instancia sintetica, y va en tarea propia si persiste tras este."
    - "TASK-0343, que esta archivada como done. Su asercion no se re-abre: lo que se arregla es el
      ARNES que la ejecuta, no la propiedad que ella acredito."
    - "Cambiar el contenido de los casos de residuo. Se puede cambiar DE DONDE leen; que compruebe
      envejecimiento de residuo sigue siendo legitimo."
  risk: high
  estimate: M
---

# TASK-0395 -- el verificador que mide el disco

## Los tres brazos, mismo commit `47cc9184`

    CLON LIMPIO   baseline=3/3 short_circuit=3/3 tautology=3/3 unreachable=3/3   exit 0
    ARBOL VIVO    AssertionError: stale UTF-8 residue did not age: 'live'        exit 1
    CI (runner)   baseline caught_runs=0                                          exit 1

No habia contradiccion entre instrumentos. Habia **una suite que mide su entorno**, y cada uno la
corrio en un entorno distinto. El checker tenia razon, Codex tenia razon y CI tiene razon: sobre
arboles diferentes.

## La causa, directa

`run_nul_residue_path_cases` lee el residuo REAL del working tree y comprueba si ha envejecido. Con
un exec de peon escribiendo, el residuo esta `live` y el caso falla. El runner no distingue su
sandbox del arbol donde vive.

## Por que es prioridad y no una molestia

Porque ya cobro su precio, y en cadena:

    rojo del gate -> TASK-0367 no pudo entregar -> su claim no se libero
                  -> TASK-0337 y TASK-0391 bloqueadas
                  -> la instancia NOVA sin las correcciones que reporto

Y porque el objeto averiado es **el runner de falsacion**: el instrumento que existe para demostrar
que los controles saben decir que no. Si su veredicto depende de quien mas escriba en el disco, todo
lo que acredita es una coincidencia. Es la misma familia que el hub lleva una semana cazando, en el
sitio donde mas duele: **el que mide a los que miden**.

## Blocked evidence - 2026-08-15

The hermetic residue-path probe passed twice from an intentionally dirty live tree, but the required
falsification gate still exits 1 before delivery. Its TASK-0343 execution matrix is stable across the
attempted isolated-root repair: `baseline=0/3`, while `short_circuit=3/3`, `tautology=3/3`, and
`unreachable=3/3`. The baseline child exits 0 with `mailbox retry cases: PASS`, so the declared
ledger-destruction stimulus is not reaching the production assertion. The claim is released and the
changes remain uncommitted. Arquitecto must decide whether TASK-0395 may repair that stale TASK-0343
stimulus despite the explicit out-of-scope rule that TASK-0343 is not reopened.
