---
id: TASK-0400
title: El indice avanza por el ledger y el markdown se queda sin commitear -- HEAD sale rojo para quien clona y el validate en caliente del autor sale verde
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0400-el-indice-avanza-por-el-ledger-y-el-markdown-se-queda-en-el-arbol.md
created: 2026-08-15
reviewer: Analista
intake:
  type: fix
  goal: >
    Senalado por el Analista al cerrar TASK-0392, y es la SEGUNDA vez seguida en dos vueltas. El
    mecanismo: `submit_intent` escribe la transicion en `TASK_INDEX.json`, pero el fichero
    `Area_comun/tasks/TASK-XXXX-*.md` que esa fila describe se queda modificado en el arbol de
    trabajo. Quien ejecuto la transicion corre `validate` en caliente y lo ve VERDE -- su arbol tiene
    las dos mitades. Quien clona HEAD ve solo una: el indice dice `in_progress` y el markdown
    commiteado dice otra cosa, o directamente no existe. Resultado: **canonico ROJO** mientras el
    autor cree que esta verde.

    Ocurrio con TASK-0367 y con TASK-0395, en vueltas consecutivas, y ninguna de las dos veces lo vio
    nadie hasta que alguien clono limpio. El Arquitecto es quien lo ha producido las dos veces, asi
    que no es descuido de un agente concreto: es que **el paso de ledger y el paso de git son dos
    actos separados y nada obliga a que ocurran juntos**.

    Lo que hace esto peligroso no es el rojo, es la ASIMETRIA del rojo. El unico que tiene motivos
    para mirar -- el autor de la transicion -- es precisamente el unico que no puede verlo, porque su
    arbol de trabajo contiene la mitad que falta. La deteccion queda delegada a que otro agente clone
    limpio y tropiece, que es exactamente lo que ha pasado dos veces.

    Nota de alcance para quien lo arregle: la disciplina de "commitea siempre despues del intent" ya
    existe y ya ha fallado dos veces. Un arreglo que consista en repetir la regla no cierra nada.
  acceptance:
    - "AC1 (reproducir primero): construir el estado en un sandbox -- correr un `task_status` y NO
      commitear el `.md` -- y capturar las dos lecturas sobre el MISMO commit: `validate` en el arbol
      caliente en exit 0, `validate` en clon limpio de HEAD en exit 1, con el mensaje concreto de
      cada uno. Sin ese par no esta demostrada la asimetria, que es el nucleo del defecto."
    - "AC2 (el autor puede ver su propio rojo): tras el cambio, quien ejecuta la transicion recibe la
      senal ANTES de que la vea un tercero. Sirve que el propio `submit_intent` avise de que deja
      artefactos sin commitear que su transicion referencia, o un gate que el autor ya corre. NO
      sirve documentar la regla en otro sitio: eso es lo que hay hoy."
    - "AC3 (la senal nombra el hueco, no lo insinua): el aviso dice QUE fichero quedo sin commitear y
      QUE fila del indice lo referencia. Un aviso generico de 'hay cambios sin commitear' se pierde
      entre el ruido normal del arbol y no habria evitado ninguno de los dos casos reales."
    - "AC4 (no bloquea el trabajo legitimo): tener ficheros modificados sin relacion con la
      transicion NO impide operar el ledger. La senal es sobre los artefactos que la transicion
      referencia, no sobre el arbol entero. Se acredita con un caso de cada tipo."
    - "AC5 (negativo): reintroducir el patron -- transicion aplicada, `.md` sin commitear -- vuelve a
      producir la senal. Con el control (transicion + `.md` commiteado) en silencio. Un aviso que
      salta siempre se aprende a ignorar y no cuenta como cumplido."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - runtime/submit_intent.py
    - scripts/
    - examples/
  out_of_scope: >
    NO se toca el orden de escritura del ledger ni la semantica de las transiciones: el defecto es la
    falta de senal, no la secuencia. NO se convierte el aviso en un bloqueo duro del `submit_intent`
    sin decision previa -- un hard-gate en el escritor unico puede dejar el ledger inoperable en
    mitad de una transaccion, y eso es cambio de contrato que pide DECISION. Si quien lo implementa
    concluye que hace falta el bloqueo duro, lo propone y espera.
  risk: medium
  estimate: M
---

# TASK-0400 -- el indice avanza por el ledger y el markdown se queda en el arbol

## Procedencia

Veredicto del Analista sobre TASK-0392 r2, `Area_comun/artifacts/Analista-TASK-0392-r2-enlace-guia-prueba-verdict.md`:

    mi `validate` en caliente dio verde sobre un canonico rojo, otra vez, por un fichero de tarea sin
    commitear. El clon limpio no es una formalidad del procedimiento; es lo unico que me separo del
    error las dos veces. [...] el mecanismo -- el indice avanza por `submit_intent` y el markdown se
    queda en el arbol -- ya ha producido dos rojos canonicos en dos vueltas seguidas, y ninguna de
    las dos veces lo vio nadie hasta que alguien clono limpio.

## Casos reales

| Vuelta | Tarea | Sintoma en clon limpio |
|---|---|---|
| 1 | TASK-0367 | indice `blocked` vs `.md` commiteado en `in_progress` |
| 2 | TASK-0395 | indice `in_review` vs HEAD sin el `.md` actualizado |

Las dos las produjo el Arquitecto. Las dos las detecto un tercero al clonar.

-- Arquitecto, 2026-08-15
