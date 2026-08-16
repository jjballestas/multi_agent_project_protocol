---
id: TASK-0409
title: Un test se ancla a un ID de tarea concreto y la poda, que es el propio protocolo, se lo lleva
status: review_approved
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0409-un-test-anclado-a-un-id-que-la-poda-archiva.md
created: 2026-08-16
reviewer: Analista
intake:
  type: infra
  goal: >
    Medido en CI el 2026-08-16 (run 31941857538, job `validate`, paso 14 "Validate falsification
    contracts and guardian controls"): `scripts/memory/test_memory_db.py` falla con
    `StopIteration` en `test_f2_stub_at_original_task_path_keeps_canonical_validator_green`,
    porque en las lineas 3286 y 3296 busca literalmente `TASK-0350` en el indice CALIENTE y esa
    tarea ya no esta: la poda del 2026-08-16 05:25 la archivo, que es exactamente lo que la poda
    existe para hacer. El test asume que una tarea concreta vive para siempre en el indice
    caliente, cuando el propio protocolo la mueve a `TASK_INDEX_ARCHIVE.json` al cerrarse. No es
    un defecto de la poda ni de la entrega que lo destapo: es un control anclado a una coordenada
    que el sistema cambia por diseno. Es la CUARTA variante del mismo patron en 24h -- 353
    fronteras declaradas por texto literal (0397), 164 exenciones indexadas por numero de linea
    (0388, censo medido), el pin del gancho como literal (0378), y ahora un ID de tarea clavado.
    El rojo estuvo LATENTE siete horas y solo se hizo visible al desbloquear los pasos 4 y 10.
  acceptance:
    - "AC1 (la propiedad, no el ejemplar): el test DERIVA el sujeto que necesita en vez de nombrarlo.
      Toma cualquier fila que cumpla la propiedad que el caso quiere probar -- tarea `done` con
      deliverable personal ausente -- o construye su propia fixture. Se acredita midiendo que el
      test pasa con el indice caliente ACTUAL y seguiria pasando si esa fila se archivara."
    - "AC2 (el negativo, por MUTACION): archivar (o retirar del indice caliente) la fila que el test
      acabe usando NO debe romperlo. Se acredita ejecutando esa mutacion y ensenando el exit code:
      con la fila fuera del caliente, el test sigue verde. Si se rompe, el AC1 no esta cumplido --
      solo se ha cambiado un ancla por otra."
    - "AC3 (el censo, porque el patron es de CLASE): cuantas referencias a IDs LITERALES de tarea,
      claim o decision existen en las suites bajo `scripts/` y `examples/`, y cuantas de ellas
      apuntan hoy a filas que ya viven en un `*_ARCHIVE.json`. Da los dos numeros medidos. No se
      pide arreglarlas todas: se pide saber si esto es un caso o una familia."
  verification_cmd:
    - "python scripts/memory/test_memory_db.py"
    - "python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/memory/test_memory_db.py
  out_of_scope:
    - "El gate de poda cuyo disparador y remedio son disjuntos (`cold_start_tokens` mide el backlog
      ABIERTO y la poda solo archiva lo TERMINAL): defecto real y medido, pero es tarea aparte."
    - "Las otras tres variantes del patron de coordenada fragil (fronteras literales de 0397,
      exenciones por linea de 0388, pin literal de 0378): cada una tiene su via. Aqui solo entra el
      ancla por ID de tarea."
    - "Reintroducir TASK-0350 en el indice caliente para que el test pase: esa salida esta
      EXPLICITAMENTE descartada -- pondria el estado al servicio del test."
  risk: low
  estimate: S
---

# TASK-0409 -- el test que ancla en un ID que el sistema archiva

## Lo medido

Run `31941857538`, job `validate`, paso 14:

    ERROR: test_f2_stub_at_original_task_path_keeps_canonical_validator_green
      task_row = next(row for row in canonical_index["tasks"] if row["id"] == "TASK-0350")
    StopIteration
    Ran 82 tests in 92.410s -- FAILED (errors=1)

Coordenadas: `scripts/memory/test_memory_db.py:3286` y `:3296`.

## Por que no es culpa de la poda

La poda hizo su trabajo: archivar entradas terminales. El test asumia que `TASK-0350` seguiria en
el indice caliente indefinidamente. **La suposicion es del test, no del estado.** Reintroducir la
fila para que el test pase seria poner el estado al servicio del verificador -- justo la inversion
que este protocolo existe para impedir.

## Por que importa mas que su tamano

El arreglo es pequeno; el patron no. En 24 horas hemos encontrado la misma patologia cuatro veces,
y cada aparicion costo un rojo que parecia de otra cosa:

    controles anclados a una coordenada que el sistema cambia por diseno,
    y que se desincronizan en SILENCIO del efecto que dicen vigilar

El AC3 pide el censo precisamente para saber si esto se cierra con un parche o pide una DECISION
sobre como se declaran las fronteras de los controles.
