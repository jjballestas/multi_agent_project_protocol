---
id: TASK-0384
title: El aviso afirma un desenlace que no computa -- el canal de reporte cablea el resultado en vez de leerlo del clasificador
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0384-el-aviso-afirma-un-desenlace-que-no-computa.md
created: 2026-08-14
reviewer: Analista
intake:
  type: fix
  goal: >
    Sucesora declarada al cierre de TASK-0368, por arbitraje del checker (veredicto r5, seccion 9,
    residual R1). El aviso de `build_memory_db.py:985-987` afirma "attested policy treats it as
    current" para TODO artefacto con `status` ausente -- incluido el caso que r5 clasifica
    `superseded`. Clase del defecto: **un mensaje que afirma un desenlace que no computa**. Vive en
    la frontera de carga, donde el clasificador todavia no ha corrido, y por eso solo puede hablar
    del resultado CABLEANDOLO. Es la misma familia que TASK-0368 existio para cerrar -- derivar una
    propiedad de un literal -- mudada un piso arriba, al canal de reporte. Por eso el arreglo NO es
    cambiar la frase: es que el aviso por artefacto reporte el estado que el clasificador produjo
    para ESE artefacto. Hoy hay CERO instancias vivas (el unico fichero del corpus sin `status`,
    DECISION-0059, no lleva puntero), asi que no bloqueaba el cierre de 0368; el defecto es real
    igual y se declara aqui para que no se redescubra como hallazgo.
  acceptance:
    - "AC1 (el criterio, tal como lo formulo el checker): el aviso por artefacto reporta el estado
      que el clasificador produjo para ESE artefacto. Se acredita con el caso que hoy miente --
      `status` ausente MAS `superseded_by` -- comprobando que el aviso nombra `superseded` y no
      `current`, y con el caso que hoy dice verdad -- `status` ausente SIN puntero -- comprobando
      que sigue diciendo `current`. Por exit code, no por inspeccion visual del texto."
    - "AC2 (no es un parche de cadena): el aviso deja de contener un desenlace literal. Si tras el
      cambio se invierte la rama del clasificador, el TEXTO del aviso cambia con ella sin tocar el
      mensaje. Se acredita con ese mutante: invertir la clasificacion y comprobar que el aviso lo
      sigue."
    - "AC3 (R2, mismo canal, residuo PRE-EXISTENTE): un `superseded_by` que no case `ID_RE` lo
      descarta `validate_metadata` y la decision sale `active`. NO lo introduce r5 -- la rama
      `status: accepted` hace lo mismo (medido por el checker en P06/P07/P08/P10) -- y yerra hacia
      MAS visibilidad (`hot_required=1`), que es la cara fail-closed. Se acredita dejando el
      descarte RUIDOSO y trazable al artefacto concreto, no silencioso."
    - "AC4 (el censo no se mueve): antes y despues, censo A/B sobre el corpus real dentro del mismo
      commit. Cero filas movidas en las dos direcciones. Este cambio es de canal de reporte; si
      mueve una clasificacion, esta mal."
    - "AC5 (el verde discrimina): revertir el cambio pone en exit 1 el runner declarado, con el
      control en 0. Un verde que el codigo previo tambien produce no acredita nada."
  verification_cmd:
    - "python scripts/memory/test_memory_db.py"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory"
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/memory/build_memory_db.py
    - scripts/memory/test_memory_db.py
  out_of_scope:
    - "RENOMBRAR el campo atestado `missing_status: current_with_warning`. Respuesta del Arquitecto a
      la pregunta del checker al cerrar 0368: NO entra. El literal que carga el CONTRATO es
      `non_current_when: superseded_by_present_or_status_declared_non_current`, es correcto y r5 puso
      a produccion a obedecerlo; `missing_status` solo nombra el DEFECTO del caso SIN puntero, que
      sigue siendo exactamente lo que dice. Una vez el aviso reporte el estado computado, la
      imprecision del nombre deja de tener consecuencia operativa. Renombrarlo arrastra el blob de
      politica atestado y su guard de forma que lo PINEA como literal (`build_memory_db.py:588`), es
      decir acopla un arreglo de conducta a un cambio de artefacto atestado -- el acoplamiento que ha
      mordido a esta cadena repetidamente. Si algun dia se renombra, va en tarea propia con su
      re-atestacion coordinada."
    - "R3 del veredicto (asimetria de `value_list` con espacios en blanco): simetrica en las dos
      ramas e INALCANZABLE por el camino real. Declarada para que nadie la redescubra, no para
      arreglarla."
    - "R4 del veredicto (el corpus real no ejercita el cambio de r5): es una limitacion de la puerta
      de inventario, que ata la declaracion por PRESENCIA y no por poder de matar mutantes. Va con
      la familia del inventario, no aqui."
    - "Cualquier cambio de clasificacion. Esta tarea toca el canal de reporte."
  risk: low
  estimate: S
---

# TASK-0384 -- el aviso afirma un desenlace que no computa

## Origen

Hallazgo del Arquitecto durante la verificacion independiente de TASK-0368 r5, medido en clon limpio
con una sonda commiteada:

    CLASSIFY DECISION-PROBE  -> superseded | status= None | superseded_by= ['DECISION-0081']
    WARN:    DECISION-PROBE.md : decision currentness status is missing;
                                 attested policy treats it as current

Ruteado al checker como **arbitraje** en vez de como sexta iteracion de remediacion: el operador
habia acotado el lazo a UNA propiedad tras el escalado del checker, y un coordinador que se
autoconcede otra vuelta sobre su propia cadena es el maker haciendo de checker.

## Dictamen del checker (veredicto r5, seccion 7)

**No bloquea AC4 de 0368.** AC4 condiciona su exigencia a una CLASIFICACION ERRONEA, y no la hay:
17/17 formas bien clasificadas, censo correcto. Las tres condiciones de bloqueo, medidas y ausentes:

    C1  una decision real HOY con status ausente Y puntero  -> ninguna (DECISION-0059 no lleva puntero)
    C2  clasificacion erronea en cualquier direccion        -> ninguna
    C3  el aviso como unica senal decidiendo una puerta     -> ninguna puerta lo consume

Sale como tarea propia, con el criterio de la seccion 9 y no como "arreglar el texto".
