---
id: TASK-0352
title: Los casos de intent flow terminan con drift de estado tras submit_intent
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0352-drift-tras-submit-intent-en-los-casos-de-intent-flow.md
created: 2026-08-10
---

# TASK-0352 -- drift que queda despues de aplicar

Paso 36 (`intent_flow_cases`) del job `validate`, en checkout limpio a HEAD. Medido por mutacion:
**no es la regla de `obstacles`**.

```
case_protocol_prune_removes_terminal_hot_entries
IntentApplyError: protocol state drift remains after submit_intent:
    [{'path': 'Area_comun/state/TASK_INDEX_ARCHIVE.json', 'hot_hash': '8a40378f...'}]
```

Es la capa de ledger, que es la capa para la que existe este protocolo, y el sintoma es que **la
poda deja el archivo caliente y el materializado divergentes**. Determinar si la poda no materializa
el archive, si el detector de drift lo cuenta cuando no debe, o si la fixture arrastra un estado que
la poda ya no produce -- y declararlo antes de tocar nada.

Relacionado de cerca con TASK-0270 (evento perdido / reintento skipeado): misma capa, misma familia
de "exito aparente".

Fuera de alcance: los doce rojos de causa `obstacles` (TASK-0347).
