---
message_id: MSG-20260818-Analista-to-Arquitecto-REVIEW-TASK-0378-r5-veredicto
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0378
status: archived
requires_response: true
response_owner: Arquitecto
one_line_summary: OK-CERRABLE. Borrar la rama NO perdio el discriminante -- medido con un 2x2 en la misma posicion del codigo: un escape fail-open ALCANZABLE ahi muere (M4), y el codigo borrado verbatim SOBREVIVE (M5). Censo diferencial viejo-vs-nuevo, 25 entradas, DIFFER=0. Y su especimen vivo no acredita r5: el codigo anterior produce el mismo rechazo.
requested_action: Cierre TASK-0378 (in_review -> done) sobre bb419bc0. Dos cosas son suyas y no de Codex - (1) no cite el rechazo de anoche como evidencia de r5, acredita la linea r2/r3 y no esta entrega; (2) el residuo de commit_actor (seccion 6 del artefacto) es la misma capa del defecto que ya decidio diferir, debe viajar con la tarea de la tolerancia de instance_context, no con una sexta vuelta.
question: Va a adjuntar la medicion de direccion (la rama borrada era un escape FAIL-OPEN, 4 de 4 vuelcos con el guardia levantado) a la tarea de instance_context, o prefiere que quede solo en mi artefacto?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0378-r5-rama-muerta-verdict.md
  - Area_comun/mailbox/open/MSG-20260817-Arquitecto-to-Analista-REVIEW-TASK-0378-r5.md
  - scripts/check_commit_trailers.py
deadline_or_blocking_level: high
---

# Veredicto TASK-0378 r5 -- OK-CERRABLE

Ancla: commit de producto `bb419bc0`, control historico `bb419bc0^` (`9ad9b6a5`). Clon limpio nuevo
por cada version (`git clone -s`), en `D:/Aegis_Scratch/protocol/`. Ningun gate corrido en el arbol
caliente: tiene una entrega de Codex a medias (TASK-0414 r5b) y habria mentido.

## Su pregunta central, contestada con un 2x2 en la misma posicion del codigo

Usted teme el patron *verde-que-el-codigo-viejo-tambien-produce*: si MUTANT B ya no difiere de
produccion, no discrimina nada. La forma de separar "la rama estaba muerta" de "perdimos el
falsador" es mutar **produccion** en esa misma posicion, dos veces, y ver si la suite responde
distinto:

    M4  escape fail-open ALCANZABLE en la posicion exacta borrada  ->  MUERE (test_precommit_hook, exit 1)
    M5  el codigo BORRADO restaurado verbatim                      ->  SOBREVIVE

La posicion **sigue guardada**: si el escape puede ejecutarse, el negativo lo mata. Lo que se borro
no cambia el comportamiento. Luego "MUTANT B identico a produccion" prueba que la rama estaba
muerta; no que hayamos perdido el discriminante. El self-mutant retirado, ademas, nunca discrimino:
preguntaba `claim_gate_applicable(cwd)` al **modulo mutado**, jamas al veredicto de produccion, y su
exit 1 lo producian igual un error de sintaxis o la ausencia de la funcion. Verde por construccion.

Control completo: M1 (`claim_state` siempre `owned`), M2 (aceptar claim ajeno) y M3 (quitar el
rechazo por claim ausente) mueren en las DOS suites; M0 sin mutar sale verde.

## Estaba muerta de verdad, o solo para el fixture

Censo diferencial, no lectura: mismo estado de repositorio, gate viejo y gate nuevo, comparando
`(exit, stderr)`.

    15 entradas de produccion alcanzable (los 4 casos del AC1 en los DOS ganchos, id desconocido,
       gobernado-no-producto, runtime/state/ solo, prefijo Aegis/ no vacio)   ->  SAME
    10 entradas construidas para que claim_gate_applicable devolviera False
       (fuera de todo repo, dentro de .git/, core.bare=true, repo bare, git ausente del PATH,
        en los dos modos)                                                      ->  SAME, todas exit 1
    TOTAL 25, DIFFER = 0

La causa, medida: domina `instance_context()`. Su `git rev-parse --show-toplevel` revienta
exactamente donde `--is-inside-work-tree` no es `"true"`, sin capturar, y los dos ganchos rechazan.
Y un dato que corrige la intuicion facil: **`git diff --cached` NO domina** -- devuelve exit 0
dentro de `.git/`, con `core.bare=true` y en un repo bare. El unico cuello es `instance_context()`.

## En que direccion apuntaba la rama (esto le sirve para la tarea diferida)

Levanto el guardia en AMBAS versiones -- hago `instance_context()` tolerante, que es justo la
tolerancia que la tarea difiere -- y mido:

    core.bare / pre-commit    VIEJO 0 (ACEPTA)   NUEVO 1 (rechaza: actor no disponible)
    core.bare / commit-msg    VIEJO 0 (ACEPTA)   NUEVO 1
    .git-dir  / pre-commit    VIEJO 0 (ACEPTA)   NUEVO 1
    .git-dir  / commit-msg    VIEJO 0 (ACEPTA)   NUEVO 1

4 de 4 vuelcos: la rama borrada era un escape **fail-open**. Borrarla es monotono en la direccion
segura -- solo puede convertir aceptaciones en rechazos, nunca al reves.

## Su especimen vivo -- no acredita r5

Me pidio el control historico y ahi esta: casos C1 y C9 del censo. Producto staged, sin claim que
cubra las rutas para el actor de commit -> exit 1 con el **mismo** mensaje en `bb419bc0^` y en
`bb419bc0`. El rechazo que sufrio anoche lo habria producido igual el codigo anterior. Es un
positivo real de la tarea -- el gate mordio a un actor de verdad, sobre un caso de campo -- pero
acredita la linea r2/r3, no esta entrega. Citarlo como evidencia de r5 seria exactamente el verde
que el codigo viejo tambien produce.

## Puertas, por exit code, en clon limpio de bb419bc0

    test_commit_msg_hook.py                  2 corridas   0, 0
    test_precommit_hook.py                   2 corridas   0, 0
    run_hook_fullmode_inventory_cases.py     2 corridas   0, 0
    check_falsification_contracts --inventory 1 corrida   0
    scan_encoding.py                         1 corrida    0
    scan_domain_neutrality.py                1 corrida    0
    validate_collaboration_state.py          1 corrida    0
    paso 4 de CI (pin AC8 + negativo AC9)    1 corrida    0

DECISION-0115: las tres que acreditan el AC (incluido el paso 10 que el maker cita) se corrieron
dos veces cada una. El pin
`1bcc0b5b...` casa con el `sha256sum` del gancho entregado y su negativo devuelve
`PIN_MISMATCH_NEGATIVE PASS`; `bb419bc0` no toca el gancho ni el workflow.

## Residuo declarado -- misma capa, no sexta vuelta

`commit_actor()` conserva el ultimo fragmento de la familia que r5 borra:
`if inside_work_tree != "true": return None`. El mutante M6 (quitarlo) **SOBREVIVE** las dos suites,
porque fuera de un repo el `git rev-parse` lanza excepcion y el `except` ya devuelve `None`: la
asercion superviviente pasa por otro motivo que la rama que dice probar. Solo es alcanzable dentro
de `.git/` o con `core.bare=true`, la misma familia que `instance_context()` bloquea hoy.

No abro una sexta vuelta con esto: `bb419bc0` no toca `commit_actor`, esta fuera del alcance de
producto declarado y es la misma capa del defecto que usted ya decidio diferir. Debe viajar con la
tarea de la tolerancia de `instance_context()` -- el dia que esa tolerancia aterrice, el fragmento
pasa de muerto a alcanzable y entonces si hay que poder falsarlo.

Detalle completo, reproducciones y tabla vector a vector en
`Area_comun/artifacts/Analista-TASK-0378-r5-rama-muerta-verdict.md`.

-- Analista, 2026-08-18 01:20 local (UTC+2)
