---
id: TASK-0350
title: El port del motor de memoria mete un fichero con marcadores sin resolver en la instancia generada
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0350-el-port-del-motor-de-memoria-deja-marcadores-sin-resolver.md
created: 2026-08-09
---

# TASK-0350 -- marcadores sin resolver en la instancia generada

Paso 50 del job `validate` (`examples/runtime_instantiation_cases`), en checkout limpio a HEAD:

    case_coordination_default_and_flag
    ERROR: Unresolved placeholders remain in generated instance: scripts/memory/test_memory_db.py

El instanciador copia el motor de memoria a la instancia nueva sin resolver sus marcadores. Toca
justo el trabajo de memoria hibrida de esta jornada (TASK-0327/0328), asi que importa doble: una
instancia recien nacida arrastraria el fichero roto.

Determinar si el fichero debe resolverse como plantilla, excluirse del copiado, o si el motor de
memoria no deberia viajar en el instanciador. Declarar cual y por que.

Fuera de alcance: los quince rojos de causa `obstacles` (TASK-0347).
