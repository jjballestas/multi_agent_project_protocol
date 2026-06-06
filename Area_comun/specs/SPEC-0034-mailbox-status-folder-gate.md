---
spec_id: SPEC-0034-mailbox-status-folder-gate
task_id: TASK-0035
type: implementation
status: ready
linked_decisions: [DECISION-0013, DECISION-0006, DECISION-0005, DECISION-0001]
created_at: 2026-06-06
author: Claude
priority: high
---

# SPEC-0034 - Gate de consistencia mailbox status<->carpeta

## Contexto
La coordinacion es el nucleo del proyecto. Se detecto deriva silenciosa: 10 mensajes movidos a
`answered/`/`archived/` conservaban `status: open` en el frontmatter, por lo que aparecian como
pendientes para siempre. `validate_mailbox` solo revisa `open/` (warn si un mensaje resuelto sigue ahi)
y NO el caso inverso (archivado con `status: open`); ademas es warning, no falla. En produccion (loop
autonomo M2) un mensaje atascado en "open" haria que el router lo re-procese o mal-enrute => desastre.
Causa raiz: mover-a-answered es un paso manual no verificado (convencion sin gate).

## Alcance
- Extender `scripts/validate_collaboration_state.py` (+ `.ps1` con paridad), funcion `validate_mailbox`:
  recorrer **las tres carpetas** (`open`/`answered`/`archived`) y verificar que el campo frontmatter
  `status` **coincide con la carpeta**. Mismatch => **error** (no solo warn), con ruta + valor esperado.
- Conservar el check existente (mensaje resuelto en `open/`) como subcaso del mismo invariante.
- **Arreglar `scripts/prune_state.py`/`.ps1`**: al MOVER un mensaje a `archived/` (o a `answered/`), debe
  **actualizar el frontmatter `status` a la carpeta destino**. (Se descubrio que la poda de TASK-0034
  movio 41 mensajes a `archived/` dejando `status: answered` -> reintrodujo el bug que este gate cierra.)
- **Normalizacion one-time:** sincronizar los mensajes ya desfasados (los 41 + cualquiera) para que el
  gate quede verde sobre el repo real.
- Golden `examples/mailbox_status_cases/`: limpio (3 carpetas consistentes) pasa; `answered/` con
  `status: open` falla; `open/` con `status: answered` falla; **caso prune que mueve a archived/ y deja
  status correcto**.
- CI: ya corre el validador; el nuevo error entra en el gate existente.

## No-alcance
- No cambia el ciclo de vida de tareas ni el contrato de turno. No mueve mensajes automaticamente (eso es
  mailbox automation de M2); aqui solo se VERIFICA la consistencia. No toca runtime ni poda.

## execution_pipeline
1. En `validate_mailbox`, iterar las tres carpetas; por cada `MSG-*.md` leer `status` y compararlo con el
   nombre de carpeta; `fail` en mismatch.
2. Paridad `.ps1` (mismos veredictos/exit codes).
3. Golden con los tres casos.

## acceptance_criteria
- Mensaje en `answered/` con `status: open` => validador **falla** con la ruta. Igual para `archived/`.
- Mensaje en `open/` con `status: answered`/`archived` => falla (endurece el warn actual a error, o lo
  mantiene como error coherente con el invariante).
- Repo real verde tras la limpieza de los 10 mensajes (ya aplicada).
- Paridad `.py`/`.ps1`; golden verdes; sin regresion en los demas golden/validador.

## linked_decisions
- `DECISION-0013` (visibilidad/integridad de coordinacion), `DECISION-0006` (robustez), `DECISION-0005`
  (mailbox), `DECISION-0001` (aditivo => MINOR). Sin decision nueva: enforcement de un invariante existente.

## test_plan
- Golden `examples/mailbox_status_cases/` (consistente / answered-con-open / open-con-answered) + paridad
  `.ps1` atestiguada; validador + scan verdes en el repo real.

## closure_criteria
- Check folder<->status en `validate_mailbox` (.py/.ps1) como error + golden verdes + repo real verde +
  revision del arquitecto OK; claim liberado al pasar a in_review (dogfood DECISION-0013).

## Risks
- **Falsos positivos por plantillas/ejemplos.** Mitigacion: limitar el check a `Area_comun/mailbox/**`
  (no a fixtures de ejemplos que prueban estados a proposito); los golden usan su propio root.

## Traceability
| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| status coincide con carpeta | TASK-0035 | golden mismatch | validador falla en mismatch |
| Paridad py/ps1 | TASK-0035 | golden + ps1 | mismos veredictos |
| Repo real consistente | TASK-0035 | validador repo | verde tras limpieza |
