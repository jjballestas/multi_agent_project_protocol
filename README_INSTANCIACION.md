# Guia de instanciacion del protocolo multiagente

Esta carpeta empaqueta una metodologia generica para coordinar proyectos de software con
varios agentes. El protocolo define como se trabaja: tareas, claims, mailbox, decisiones,
handoffs y validacion de estado. El dominio de cada proyecto se declara en la instancia.

## 1. Crear un proyecto nuevo

1. Copia el contenido de `protocol_template/` a la raiz del nuevo repo.
2. Copia estos archivos master para crear los archivos vivos de la instancia:
   - `AGENTS.template.md` -> `AGENTS.md`
   - `Area_comun/README.template.md` -> `Area_comun/README.md`
   - `Area_comun/state/PROJECT_STATE.template.json` -> `Area_comun/state/PROJECT_STATE.json`
   - `Area_comun/state/TASK_INDEX.template.json` -> `Area_comun/state/TASK_INDEX.json`
   - `Area_comun/state/CLAIMS.template.json` -> `Area_comun/state/CLAIMS.json`
3. Rellena todos los placeholders `{{...}}`.
4. Declara las fronteras duras del proyecto en `{{DOMAIN_CRITICAL_BOUNDARIES}}`.
5. Declara decisiones de stack en `{{STACK_DECISIONS}}`.
6. Declara puntos de aprobacion humana en `{{HUMAN_APPROVAL_POINTS}}`.
7. Ajusta `protocol.config.json` con `project_name`, `agent_roles`, `quality_gates` y
   `state_invariants`.

## 2. Archivos a completar primero

1. `AGENTS.md`: contrato superior del proyecto.
2. `Area_comun/state/PROJECT_STATE.json`: fase inicial, objetivo, agentes, decisiones y riesgos.
3. `protocol.config.json`: parametros que usa el validador.
4. `Area_comun/state/TASK_INDEX.json`: backlog inicial.
5. `Area_comun/tasks/TASK-0001-*.md`: primera tarea ejecutable.

## 3. Generar backlog inicial

1. Crea tareas pequenas, verificables y con un solo owner.
2. Cada tarea debe tener objetivo, entradas, archivos relevantes, entregables, DoD, riesgos y
   preguntas abiertas.
3. Registra cada tarea en `Area_comun/state/TASK_INDEX.json`.
4. Si una tarea depende de una decision, enlaza `Area_comun/decisions/DECISION-XXXX-*.md`.
5. Si hay una ambiguedad bloqueante, usa status `blocked` y una pregunta concreta.

## 4. Reclamar tareas

1. Lee `AGENTS.md`, `Area_comun/README.md`, `TASK_PROTOCOL.md`, `PROJECT_STATE.json`,
   `TASK_INDEX.json`, `CLAIMS.json`, `mailbox/open/` y el archivo de tarea.
2. Verifica que la tarea esta `ready` y que no existe claim activo de otro owner sobre sus rutas.
3. Actualiza el archivo de tarea y `TASK_INDEX.json` a `claimed` o `in_progress`.
4. Crea o actualiza una entrada en `Area_comun/state/CLAIMS.json` con scope explicito.
5. Al cerrar, libera el claim con `status: released`.

## 5. Cerrar una fase

1. Todas las tareas de salida de fase deben estar `done` o tener bloqueo aceptado.
2. Debe existir handoff autocontenido para lo que otro agente deba revisar.
3. Debe existir reporte humano en `Area_comun/reports/`.
4. `PROJECT_STATE.json` debe reflejar fase, riesgos, preguntas y proximas acciones.
5. Ejecuta el validador. Variante recomendada:

```powershell
powershell -NoProfile -File scripts\validate_collaboration_state.ps1
```

Si tu entorno local requiere una anulacion temporal de politica de ejecucion, tambien puede
funcionar:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1
```

## 6. Validar una instancia minima de ejemplo

Desde la raiz de esta plantilla:

```powershell
powershell -NoProfile -File scripts\validate_collaboration_state.ps1 -Root examples\minimal_instance
```

## 7. Convencion de archivos template

En la raiz de `protocol_template/`, los archivos con sufijo `.template.*` son los unicos masters
para contenido que debe rellenarse por proyecto. Los archivos canonicos sin sufijo (`AGENTS.md`,
`PROJECT_STATE.json`, etc.) solo viven dentro de instancias reales, como
`examples/minimal_instance/`, para evitar drift entre dos fuentes equivalentes.
