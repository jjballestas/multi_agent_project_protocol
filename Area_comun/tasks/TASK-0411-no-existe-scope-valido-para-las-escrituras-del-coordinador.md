---
id: TASK-0411
title: No existe scope valido para las escrituras del coordinador -- el fragmento cae fuera y el fichero entero solapa
status: ready
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0411-no-existe-scope-valido-para-las-escrituras-del-coordinador.md
created: 2026-08-16
reviewer: Analista
intake:
  type: infra
  goal: >
    Fusiona el D-6 del hub (scope_routes a nivel de DIRECTORIO serializa la instancia entera) con el
    D-10 medido por NOVA, que lo generaliza y es la formulacion correcta: NO EXISTE un scope valido
    para NINGUNA escritura del coordinador sobre el estado compartido. Declarar el FRAGMENTO falla
    por fuera-de-scope; declarar el FICHERO ENTERO falla por solape con cualquier fragmento que otro
    actor ya tenga. El coordinador queda sin forma legal de escribir mientras un peon tenga
    cualquier claim. Medido en el hub el 2026-08-16, TRES bloqueos propios en una jornada -- 12:29 y
    13:43 la poda contra `CLAIMS.json` (claim de Codex sobre 0378-r4 y sobre 0409), y 13:01 el alta
    de TASK-0409 contra `runtime/state/events.jsonl`; el registro solo entro al RETIRAR esa ruta del
    scope, no por resolver el conflicto. En NOVA costo una hora registrar una tarea que desbloqueaba
    otras diez. Consecuencia sistemica: la ventana de escritura del coordinador dura SEGUNDOS (el
    hueco entre que un peon cierra un exec y toma el siguiente) y la poda, que reclama el ledger
    entero, es practicamente inejecutable con dos peones activos.
  acceptance:
    - "AC1 (nombrar la propiedad, no el caso): declarar por que un fragmento cae fuera de scope y un
      fichero entero solapa -- es decir, cual es la regla de contencion que hoy hace vacio el
      conjunto de scopes validos para el coordinador. Se acredita con los DOS rechazos reproducidos
      por exit code, no con la descripcion."
    - "AC2 (el conjunto deja de ser vacio): existe al menos un scope declarable con el que el
      coordinador PUEDE escribir estado compartido mientras un peon tiene un claim sobre OTRA fila
      del mismo fichero. Se acredita ejecutando ambas escrituras concurrentes por exit code."
    - "AC3 (el negativo, por MUTACION): dos actores que reclaman LA MISMA fila siguen colisionando.
      Si tras el arreglo dos claims sobre la misma fila conviven, se ha quitado la exclusion en vez
      de afinarla -- y eso es peor que el defecto. Se acredita con el rechazo ejecutado."
    - "AC4 (la poda vuelve a ser ejecutable): `prune_state.py --apply` entra con un claim de peon
      activo sobre filas que la poda no toca. Es el caso que hoy obliga a cazar una ventana de
      segundos, y el unico que prueba que el arreglo sirve para la operacion real."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/prune_state.py --root . --check"
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - runtime/submit_intent.py
  out_of_scope:
    - "El gate de poda cuyo disparador y remedio son disjuntos (`cold_start_tokens` mide el backlog
      abierto y el mailbox, no lo que la poda archiva): defecto distinto, tarea aparte."
    - "La barrera de quiesce (marca de estado consultada en Acquire-ExecReservation): es la
      alternativa de COORDINACION a este defecto de SCOPE, y va a DECISION aparte. Si este arreglo
      entra, la barrera deja de ser necesaria para la poda."
    - "TASK-0407 (el marcador de parada no respeta el lote) y D-11 de NOVA (el rollback pone en
      cuarentena ficheros de otro actor): misma familia de arnes, vias propias."
  risk: medium
  estimate: M
---

# TASK-0411 -- el coordinador no tiene forma legal de escribir

## Las dos mitades del mismo muro

    scope = fragmento          ->  "write outside active claim scope"
    scope = fichero entero     ->  "claim acquire overlaps active claim ...: X / X#fila"

No es que un scope sea demasiado ancho: es que **el conjunto de scopes validos esta VACIO** mientras
otro actor tenga cualquier fila del mismo fichero.

## Evidencia propia del 2026-08-16 (tres bloqueos en una jornada)

    12:29  poda   vs CLAIM-20260816-Codex-TASK-0378-r4        (CLAIMS.json)
    13:43  poda   vs CLAIM-20260816-Codex-TASK-0409           (CLAIMS.json)
    13:01  alta de TASK-0409 vs el mismo claim                (runtime/state/events.jsonl)

El alta de 0409 **solo entro al RETIRAR `events.jsonl` de mi scope** -- es decir, evitando el
conflicto, no resolviendolo. Y la poda solo entro al intento 22 de un comando que esperaba
`claims == 0`, cazando un hueco de segundos.

## Por que se registra fusionado con el D-10 de NOVA

El D-6 del hub decia "scope a nivel de directorio serializa la instancia". El D-10 de NOVA lo mide
mas general y mejor: **ninguna escritura del coordinador tiene scope legal**, no solo las anchas.
Alli costo una hora registrar una tarea que desbloqueaba otras diez. La formulacion de NOVA es la
que se adopta.

## El AC que impide la salida comoda

**AC3.** Quitar la exclusion haria pasar los dos casos y romperia lo unico que el claim aporta. Por
eso el negativo exige que **dos actores sobre LA MISMA fila sigan colisionando**: si tras el arreglo
conviven, se ha desactivado el mutex en vez de afinarlo.
