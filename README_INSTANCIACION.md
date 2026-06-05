# Guia de instanciacion del protocolo multiagente

> **Propietario — All Rights Reserved.** Ver [`LICENSE`](LICENSE) y
> [`DECISION-0010`](Area_comun/decisions/DECISION-0010-licenciamiento-propietario.md). La
> instanciacion descrita aqui es para **uso autorizado del titular**; no es una invitacion a copiar
> o reutilizar el protocolo.

Esta carpeta empaqueta una metodologia generica para coordinar proyectos de software con
varios agentes. El protocolo define como se trabaja: tareas, claims, mailbox, decisiones,
handoffs y validacion de estado. El dominio de cada proyecto se declara en la instancia.

## 1. Crear un proyecto nuevo con script

Desde la raiz de `multi_agent_project_protocol`, genera una instancia nueva con:

```powershell
python scripts\new_instance.py `
  --source-template . `
  --target D:\Agentes\mi_nuevo_proyecto `
  --project-name mi_nuevo_proyecto `
  --project-goal "Objetivo operativo del proyecto." `
  --project-description "Descripcion breve del proyecto." `
  --architect Claude `
  --implementer Codex `
  --human-owner "operador humano" `
  --phase-id P0 `
  --phase-name "Bootstrap" `
  --phase-goal "Dejar una instancia inicial valida."
```

El script usa solo Python stdlib, copia los masters `*.template.*` a sus archivos canonicos,
crea la estructura necesaria de `Area_comun/` y sustituye todos los placeholders `{{...}}`.
Si queda un placeholder sin resolver, falla. Si el `--target` existe y no esta vacio, falla salvo
que se pase `--force`.

Parametros minimos obligatorios:

- `--source-template`
- `--target`
- `--project-name`
- `--project-goal`
- `--project-description`
- `--architect`
- `--implementer`
- `--human-owner`
- `--phase-id`
- `--phase-name`
- `--phase-goal`

Parametros utiles opcionales:

- `--protocol-version`: declara la version del protocolo que sigue la instancia. Si se omite, el
  script toma la version del `protocol.config.json` o `PROJECT_STATE.json` del template fuente.
- `--domain-critical-boundaries`: fronteras duras del proyecto.
- `--stack-decisions`: decisiones de stack iniciales.
- `--quality-gates`: gates de calidad iniciales.
- `--human-approval-points`: puntos de aprobacion humana.
- `--in-scope` / `--out-of-scope`: alcance inicial.
- `--phase-exit-criteria`: criterio inicial de salida de fase.
- `--force`: permite regenerar un target no vacio.

La instancia generada deja `TASK_INDEX.json` vacio pero valido. La primera tarea real se crea
despues copiando `Area_comun/protocol/TASK_TEMPLATE.md` dentro de `Area_comun/tasks/` y
registrandola en `Area_comun/state/TASK_INDEX.json`.

## 2. Validar la instancia generada

Valida la nueva instancia desde la raiz de este repo:

```powershell
python scripts\validate_collaboration_state.py --root D:\Agentes\mi_nuevo_proyecto
```

Tambien puedes usar el validador PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root D:\Agentes\mi_nuevo_proyecto
```

Para comprobar que no quedan placeholders sin resolver:

```powershell
rg "\{\{[A-Z0-9_]+\}\}" D:\Agentes\mi_nuevo_proyecto
```

## 3. Arrancar un proyecto con SDD

SDD es opcional y esta apagado por defecto. Para iniciar una instancia con SDD activado:

1. Crea la instancia con el script o de forma manual.
2. Activa el bloque `sdd` en `protocol.config.json`:

```json
{
  "sdd": {
    "enabled": true,
    "enforcement": "new_implementable_tasks",
    "adopted_at": "2026-06-05"
  }
}
```

3. Crea una spec en `Area_comun/specs/` usando `Area_comun/specs/SPEC_TEMPLATE.md`.
4. Declara la tarea implementable con estos seis campos:
   - `spec_id`
   - `execution_pipeline`
   - `acceptance_criteria`
   - `linked_decisions`
   - `test_plan`
   - `closure_criteria`
5. Verifica que `spec_id` apunta a un archivo existente dentro de la instancia.
6. Ejecuta ambos validadores antes del handoff.

Ejemplo minimo de tarea implementable con SDD:

```yaml
---
id: TASK-0001
owner: Codex
status: ready
type: implementation
spec_id: Area_comun/specs/SPEC-0001-example.md
execution_pipeline: [Create artifact, Run validator]
acceptance_criteria: [Artifact exists, Validator passes]
linked_decisions: [DECISION-0001]
test_plan: [python validator, powershell validator]
closure_criteria: [Handoff created, Review requested]
---
```

Para tareas de `discovery`, `analysis`, `review`, `documentation` o `triage`, usa los cuatro
campos minimos: `objective`, `expected_output`, `question_to_resolve` y `closure_criterion`.

La instancia `examples/minimal_sdd_instance/` muestra el caso minimo completo: `sdd.enabled:true`,
una spec resoluble y una tarea `implementation` conforme a SDD.

## 4. Crear un proyecto nuevo manualmente

1. Copia el contenido de `protocol_template/` a la raiz del nuevo repo.
2. Copia estos archivos master para crear los archivos vivos de la instancia:
   - `AGENTS.template.md` -> `AGENTS.md`
   - `protocol.config.template.json` -> `protocol.config.json`
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
8. Declara `protocol_version` (placeholder `{{PROTOCOL_VERSION}}`) con la version del protocolo
   que sigue la instancia (p.ej. `0.1.0`); ver `CHANGELOG.md` y
   `Area_comun/decisions/DECISION-0001-versionado.md`.

## 5. Archivos a completar primero

1. `AGENTS.md`: contrato superior del proyecto.
2. `Area_comun/state/PROJECT_STATE.json`: fase inicial, objetivo, agentes, decisiones y riesgos.
3. `protocol.config.json`: parametros que usa el validador.
4. `Area_comun/state/TASK_INDEX.json`: backlog inicial.
5. `Area_comun/tasks/TASK-0001-*.md`: primera tarea ejecutable.

## 6. Generar backlog inicial

1. Crea tareas pequenas, verificables y con un solo owner.
2. Cada tarea debe tener objetivo, entradas, archivos relevantes, entregables, DoD, riesgos y
   preguntas abiertas.
3. Registra cada tarea en `Area_comun/state/TASK_INDEX.json`.
4. Si una tarea depende de una decision, enlaza `Area_comun/decisions/DECISION-XXXX-*.md`.
5. Si hay una ambiguedad bloqueante, usa status `blocked` y una pregunta concreta.

## 7. Reclamar tareas

1. Lee `AGENTS.md`, `Area_comun/README.md`, `TASK_PROTOCOL.md`, `PROJECT_STATE.json`,
   `TASK_INDEX.json`, `CLAIMS.json`, `mailbox/open/` y el archivo de tarea.
2. Verifica que la tarea esta `ready` y que no existe claim activo de otro owner sobre sus rutas.
3. Actualiza el archivo de tarea y `TASK_INDEX.json` a `claimed` o `in_progress`.
4. Crea o actualiza una entrada en `Area_comun/state/CLAIMS.json` con scope explicito.
5. Al cerrar, libera el claim con `status: released`.

## 8. Cerrar una fase

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

## 9. Validar una instancia minima de ejemplo

Desde la raiz de esta plantilla:

```powershell
powershell -NoProfile -File scripts\validate_collaboration_state.ps1 -Root examples\minimal_instance
```

Para validar el ejemplo con SDD activado:

```powershell
python scripts\validate_collaboration_state.py --root examples\minimal_sdd_instance
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root examples\minimal_sdd_instance
```

## 10. Convencion de archivos template

Los archivos con sufijo `.template.*` son los unicos masters para contenido que se rellena por
proyecto. Para un proyecto NUEVO, los canonicos sin sufijo (`AGENTS.md`, `protocol.config.json`,
`PROJECT_STATE.json`, etc.) se crean en la instancia, no se mantienen como copia duplicada de la
plantilla.

**Excepcion — dogfooding de este repo:** `multi_agent_project_protocol` aplica su propio
protocolo a su desarrollo, por lo que aqui SI conviven los `.template.*` (masters publicados) con
los canonicos vivos (la instancia de este repo) y `examples/minimal_instance/` (instancia de
ejemplo). No es drift: cada par tiene un proposito distinto (master publicado vs estado vivo).
