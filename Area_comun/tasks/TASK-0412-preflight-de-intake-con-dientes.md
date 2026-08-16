---
id: TASK-0412
title: Pre-vuelo de intake CON DIENTES -- el item mecanizable falla cerrado, y el auto-atestado queda prohibido
status: ready
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0412-preflight-de-intake-con-dientes.md
created: 2026-08-16
reviewer: Analista
intake:
  type: infra
  goal: >
    P1 de la v3 aprobada (D-A, semana 0). El coordinador redacta intakes con defectos que ya estan
    codificados como lecciones en su propia memoria y los repite igual: en TASK-0396 dos de los seis
    commits de coordinacion fueron enmiendas a defectos del propio encargo, y el alcance que excluye
    la costura del defecto va por su TERCERA reincidencia -- la ultima el 2026-08-16 en TASK-0378,
    donde el out_of_scope dejaba fuera el unico fichero donde vivia el defecto. Un checklist que
    reenuncia una leccion que ya no freno no es un instrumento distinto: es la misma leccion con
    otro formato. Por eso esta tarea NO entrega un documento, entrega un GATE que puede decir que no.
  acceptance:
    - "AC1 (el item 1 en forma NEGATIVA y fail-closed): preflight_intake toma el sintoma nombrado en
      el goal de la tarea, lo busca en el arbol, y FALLA CERRADO si algun fichero donde aparece esta
      dentro de out_of_scope. Se acredita con los DOS casos por exit code: intake con la costura
      excluida -> exit distinto de 0 nombrando el fichero; intake correcto -> exit 0."
    - "AC2 (lo demas mecanizable): verification_cmd parsea y sus rutas existen; los residuos
      esperados apuntan a rutas escribibles; el tier declarado esta en el enum. Cada uno con su caso
      negativo."
    - "AC3 (PROHIBIDO el auto-atestado): el GO no admite una linea preflight 7/7 escrita a mano.
      Lleva el EXIT CODE del script. Los items de juicio -- AC falsable y satisfacible con senal
      propia, criterio de pertenencia en vez de enumeracion, autosuficiencia del encargo -- llevan
      UNA linea de justificacion auditable cada uno, no un tick."
    - "AC4 (el negativo, por MUTACION): desdentar el guard del AC1 debe hacer FALLAR su caso. Si
      sobrevive a su propia mutacion no es un negativo -- exactamente lo que le paso al AC9 del pin
      de TASK-0378, que el checker desdento y siguio imprimiendo PASS."
    - "AC5 (la leccion entra al gate, no solo a la memoria): cada defecto de intake residual anade su
      item -- mecanizado si se puede -- en el MISMO commit que corrige el intake. Sin excepcion: es
      la regla que convierte memoria en freno."
  verification_cmd:
    - "python scripts/preflight_intake.py --help"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory"
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/preflight_intake.py
  out_of_scope:
    - "Mecanizar los items de JUICIO (AC falsable, criterio de pertenencia, autosuficiencia): se
      acreditan con justificacion de una linea, y forzarlos a tick seria checklist-teatro."
    - "El panel de metricas M7/M8: tarea hermana de la misma semana 0, via propia."
  risk: low
  estimate: M
---

# TASK-0412 -- el pre-vuelo que puede decir que no

## Por que un checklist no basta

Los items 1 y 2 del pre-vuelo son lecciones que el coordinador **ya tenia escritas y violo igual**:
el alcance que excluye la costura, tres veces; el AC atado a un instrumento compartido, dos. La
diferencia entre una leccion y un gate es que **el gate falla**.

## El item que si es mecanizable, y por que es el que vale

    tomar el sintoma nombrado en el goal, buscarlo en el arbol,
    y FALLAR CERRADO si aparece en un fichero que out_of_scope excluye

Habria frenado las tres reincidencias. Las demas comprobaciones (AC2) son higiene; esta es la que
ataca el defecto caro.

## El limite, declarado

El gate **solo puede ver lo que el goal nombra**. Un goal sin sintoma buscable lo esquiva. No tiene
mitigacion completa y por eso se declara **en el propio script**, no en la nota de una tarea.
