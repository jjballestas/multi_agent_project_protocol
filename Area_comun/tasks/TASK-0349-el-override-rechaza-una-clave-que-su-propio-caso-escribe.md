---
id: TASK-0349
title: El caso de override de event-auth escribe una clave que el guard rechaza, y el gate muere sin haber probado nada
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0349-el-override-rechaza-una-clave-que-su-propio-caso-escribe.md
created: 2026-08-09
---

# TASK-0349 -- `unsupported keys: method`

Paso 43 del job `validate` (`examples/event_auth_runtime_override_cases`), en checkout limpio a
HEAD:

    case_malformed_override_fails_closed
    EventLogError: event_state runtime override event_auth contains unsupported keys: method

El caso se llama `fails_closed` y efectivamente falla cerrado -- pero por una clave que el propio
caso escribe, no por el fallo que pretende demostrar. Hay que determinar cual de los dos lados esta
mal: si `method` dejo de ser una clave admitida y el caso quedo obsoleto, o si el guard se estrecho
de mas. **No se ajusta el caso para que pase sin decidir cual de los dos es el defecto.**

Fuera de alcance: los quince rojos de causa `obstacles` (TASK-0347).
