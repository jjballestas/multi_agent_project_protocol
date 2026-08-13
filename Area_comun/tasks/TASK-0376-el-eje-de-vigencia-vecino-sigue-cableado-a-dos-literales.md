---
id: TASK-0376
title: El eje de vigencia vecino sigue cableado a dos literales, a doscientas lineas de la correccion que existia para matarlos
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0376-el-eje-de-vigencia-vecino-sigue-cableado-a-dos-literales.md
created: 2026-08-14
reviewer: Analista
intake:
  type: fix
  goal: >
    Residual R2 del veredicto r1 de TASK-0368, declarado por el checker como NO perteneciente a esa
    tarea. Mientras 0368 sustituia el literal de vigencia por una propiedad con superficie atestada,
    `build_memory_db.py:1365` conserva otro: `agent_memory.is_current` se calcula como
    `int(metadata.get("status") not in {"superseded", "archived"})`. Es un conjunto de DOS elementos
    escrito a mano, en el eje de vigencia vecino, que no lee la lista atestada y que por tanto
    discrepa de ella: la lista de politica tiene seis miembros y este cableado reconoce dos. Una
    memoria de agente cuyo `status` sea `proposed`, `rejected`, `draft` o `cancelled` se marca
    CORRIENTE. Es la familia exacta de defecto que TASK-0368 existe para matar, viva a doscientas
    lineas de la correccion.
  acceptance:
    - "AC1 (una sola fuente para el eje de vigencia): `agent_memory.is_current` deriva su respuesta
      del MISMO mecanismo atestado que decide la vigencia de una decision, no de un conjunto propio.
      Se acredita cambiando la lista atestada y observando que ESTE campo cambia en consecuencia. Si
      no se mueve al mover la lista, sigue siendo un cableado con otra ropa."
    - "AC2 (el negativo lee la lista EMBARCADA, no una copia): el test que ate esta invariante tiene
      que leer la politica que viaja en el arbol. Un test que escriba su propia copia en el fixture
      no puede detectar que la embarcada cambie -- es el defecto B4 del mismo veredicto y no se
      repite aqui."
    - "AC3 (el par, en las dos direcciones): un estado de la frontera marca no-corriente, y un estado
      vigente sigue marcando corriente. Se mide con los dos, no con uno."
    - "AC4 (barrido del eje, derivado): se reporta si quedan MAS sitios que decidan vigencia por su
      cuenta, derivando la busqueda de la propiedad `compara status contra un conjunto literal` y no
      de esta linea concreta. Si aparecen mas, entran o se declaran con su razon."
  verification_cmd:
    - "python scripts/memory/test_memory_db.py"
    - "python scripts/memory/check_memory_db_drift.py --root . --fast"
    - "python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory"
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - scripts/memory/build_memory_db.py
    - scripts/memory/test_memory_db.py
  out_of_scope:
    - "El eje de vigencia de DECISIONES: es TASK-0368, en remediacion. Aqui se trata el de
      `agent_memory`."
    - "El `.casefold()` inalcanzable de `decision_policy_state`: es TASK-0377."
  risk: low
  estimate: S
---

# TASK-0376 -- el mismo defecto, doscientas lineas mas abajo

## Lo que el checker midio

    build_memory_db.py:1365
    is_current = int(metadata.get("status") not in {"superseded", "archived"})

Dos literales escritos a mano donde la politica atestada tiene seis miembros. El resultado es que
`proposed`, `rejected`, `draft` y `cancelled` cuentan como CORRIENTES en este eje.

## Por que merece tarea y no una linea de paso

Porque es la prueba de que matar un literal no mata la costumbre. TASK-0368 sustituyo el suyo por
una propiedad con superficie configurable, y este sobrevivio intacto **en el mismo fichero**. Una
correccion que no barre su propia familia deja el siguiente caso esperando.

De ahi el AC4: el barrido se deriva de la propiedad -- *comparar `status` contra un conjunto
literal* -- y no de la linea que el checker cito.
