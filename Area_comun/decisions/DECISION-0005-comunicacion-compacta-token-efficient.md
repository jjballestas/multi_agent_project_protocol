---
decision_id: DECISION-0005
title: Comunicación compacta y token-efficient entre agentes
status: accepted
date: 2026-06-05
ratified_at: 2026-06-05
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0001, DECISION-0004, TASK-0014, TASK-0015]
phase: P2
---

# DECISION-0005 — Comunicación compacta y token-efficient

## Contexto

Cuando dos agentes dialogan como humanos tienden a repetir contexto ya disponible, pegar contenido
que ya vive en archivos, reexplicar y reconstruir la historia. Eso gasta tokens, duplica contexto y
aumenta el riesgo de inconsistencias. El protocolo ya tiene artefactos canónicos (AGENTS,
PROJECT_STATE, TASK_INDEX, decisions, specs, tasks, handoffs) que hacen innecesaria esa repetición.

## Principio

**No conversar para reconstruir contexto.** Referenciar artefactos existentes por **ID y ruta** y
enviar solo **delta, decisión, bloqueo o solicitud concreta**.

## Decisión

### 1. Reglas de comunicación compacta
- Los agentes **no repiten** contexto ya contenido en `AGENTS.md`, `PROJECT_STATE.json`,
  `TASK_INDEX.json`, `decisions/`, `specs/`, `tasks/` o `handoffs/`. Lo **referencian** por ID+ruta.
- **Una intención principal por mensaje.** Si requiere respuesta, **una sola pregunta concreta**.
- Enviar **deltas**, no recapitular todo.
- **Mailbox** = comunicación breve. **Handoff** = cierre formal de tarea o revisión.
- El **contenido largo** vive en `artifacts/`, `specs/`, `reports/` o `decisions/`, **no** en
  mensajes. Si un mensaje supera un umbral razonable, se convierte en artifact/handoff/report y el
  mailbox solo lo **enlaza**.
- Agrupar respuestas **solo** si pertenecen al mismo `task_id`.
- Evitar conversaciones narrativas entre agentes.
- La compacidad **no puede sacrificar trazabilidad ni claridad**: ante la duda, referenciar de más,
  no de menos.

### 2. Códigos estándar de comunicación
El `type` de un mensaje de mailbox usa uno de:

| Código | Significado |
|--------|-------------|
| `ACK` | Recibido, sin acción adicional. |
| `FYI` | Nota informativa, no requiere respuesta. |
| `OK` | Aceptado / correcto. |
| `REVIEW` | Solicita revisión. |
| `CHANGES` | Requiere cambios accionables. |
| `BLOCKED` | Bloqueado por una pregunta concreta. |
| `DONE` | Tarea cerrada o entregable listo. |
| `DECISION_REQUIRED` | Requiere una decisión formal. |
| `HUMAN_REQUIRED` | Requiere intervención del operador humano. |

El receptor responde con uno de estos códigos (típicamente `OK`/`CHANGES`/`BLOCKED`/`ACK`/`FYI`)
salvo que haga falta una revisión detallada (entonces, handoff).

### 3. Formato de mensaje (mailbox compacto)
Definido en `Area_comun/protocol/MAILBOX_MESSAGE_TEMPLATE.md`. Campos:
`message_id`, `type`, `task_id`, `from`, `to`, `requires_response`, `response_owner`, `subject`,
`one_line_summary`, `requested_action`, `question`, `context_refs`, `changed_refs`,
`validation_refs`, `deadline_or_blocking_level`, `status`.

### 4. Handoff compacto
`HANDOFF_TEMPLATE.md` recomienda: resumen breve; rutas exactas; decisiones/specs referenciadas;
validaciones ejecutadas; riesgos residuales; `requested_action`. **No** copiar contenido largo si
ya está en archivos.

### 5. Pregunta concreta antes de bloquear (TASK_PROTOCOL)
Antes de bloquear o pedir aclaración, el agente formula **una pregunta concreta y mínima**. Si hay
más de una pregunta, las separa en mensajes distintos o las convierte en una tarea `discovery`.

### 6. communication_budget en tareas (TASK_TEMPLATE)
Cada tarea puede declarar `## communication_budget`: `expected_messages`, `required_handoffs`,
`escalation_owner`, `compact_refs`. Orienta el coste de coordinación esperado.

### 7. Reporte humano
`HUMAN_REPORT_TEMPLATE.md` resume mensajes abiertos, bloqueos activos y decisiones requeridas, sin
incluir conversaciones largas.

### 8. Validación (suave, aditiva — TASK-0014)
Chequeos **suaves**, compatibles con mensajes históricos:
- `open` + `requires_response: true` ⇒ debe tener `requested_action` **y** `question` (ERROR).
- Si el mensaje referencia trabajo existente, debe declarar `context_refs` (WARNING).
- **No** validar longitud todavía (frágil).
- Mensajes sin los campos nuevos (históricos) **no** se invalidan.

### 9. Versionado y compatibilidad (DECISION-0001)
Aditivo ⇒ **MINOR (target v0.5.0)**. No cambia formatos obligatorios existentes ni invalida
mensajes/handoffs históricos. Endurecer (p.ej. validar longitud o exigir códigos a todo mensaje)
sería **MAJOR** y requeriría aprobación humana. Neutral de dominio.

## Consecuencias
- **Positivas:** menos tokens, menos duplicación, colaboración por referencias canónicas, menor
  riesgo de inconsistencia.
- **Costo:** disciplina de redacción; un template nuevo y campos adicionales (opcionales).
- **Seguimiento:** TASK-0014 (validador soft-checks, Codex, con spec) y TASK-0015 (ejemplo
  `compact_communication_case`, Codex). La capa se publica como **v0.5.0** al cerrarlos.

## Alternativas consideradas
- **Límites rígidos de longitud:** descartado ahora (frágil, rompería históricos) → posible MAJOR futuro.
- **Solo guía sin template/códigos:** insuficiente; no da estructura accionable ni validable.
