---
task_id: TASK-0169
title: "Validador: alinear los regex de selectores de fila con submit_intent (aceptar ids TASK-EXTRACT-* en TASK_INDEX y active_tasks) + golden"
type: implementation
status: in_review
owner: Codex
phase: P2
priority: normal
created_at: 2026-06-24
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/multi_agent_project_protocol
linked_reports: [Area_comun/reports/REPORTE-20260624-front-completo-y-hardening-0166.md]
linked_decisions: [DECISION-0022]
file: Area_comun/tasks/TASK-0169-codex-validator-selector-task-extract.md
---

# TASK-0169 - Alinear regex del validador con el escritor autoritativo (submit_intent)

> Bug-fix de tooling del protocolo-core (NO producto). maker=Codex / checker=Arquitecto. Bajo #4 enforce ON.
> Aditivo (acepta selectores validos que hoy rechaza); no cambia boundary -> sin DECISION. Origen: hallazgo del
> REPORTE-20260624 (cerrar TASK-EXTRACT-* con selector de fila dejaba el canonico rojo).

## Contexto

`runtime/submit_intent.py::required_scopes` CONSTRUYE los selectores de fila
`Area_comun/state/TASK_INDEX.json#<task_id>` y `Area_comun/state/PROJECT_STATE.json#active_tasks/<task_id>`
para CUALQUIER `task_id` que exista en el indice -- incluidos los ids `TASK-EXTRACT-<hex>` que produce el
file-intake. Es el **escritor autoritativo** (DECISION-0022). Pero
`scripts/validate_collaboration_state.py` rechaza esos selectores porque sus regex solo aceptan `TASK-\d{4}` y
`REQ-*`:

```
TASK_ROW_SELECTOR_PATTERN     = re.compile(r"^(TASK-\d{4}|REQ-[0-9A-Fa-f]+)$")
PROJECT_STATE_SELECTOR_PATTERN = re.compile(r"^(active_tasks/(TASK-\d{4}|REQ-[0-9A-Fa-f]+)|[A-Za-z_][A-Za-z0-9_]*)$")
```

Efecto: un claim que scope-a `TASK_INDEX#TASK-EXTRACT-...` o `active_tasks/TASK-EXTRACT-...` (selector fino,
legitimo y aceptado por submit_intent) deja el validador en exit 1 ("invalid row selector"). Inconsistencia
escritor-autoritativo vs validador.

## Alcance del fix

- En `scripts/validate_collaboration_state.py`, extender la porcion de id de tarea para aceptar la familia
  `TASK-EXTRACT-<hex>` ademas de `TASK-\d{4}` y `REQ-<hex>`, en AMBOS patrones:
  - `TASK_ROW_SELECTOR_PATTERN`  -> `^(TASK-(\d{4}|EXTRACT-[0-9A-Fa-f]+)|REQ-[0-9A-Fa-f]+)$`
  - `PROJECT_STATE_SELECTOR_PATTERN` -> `^(active_tasks/(TASK-(\d{4}|EXTRACT-[0-9A-Fa-f]+)|REQ-[0-9A-Fa-f]+)|[A-Za-z_][A-Za-z0-9_]*)$`
  (mantener el caso `[A-Za-z_]...` para selectores top-level no-fila como `decisions`/contadores).
- Revisar el equivalente PowerShell si el validador `.ps1` tiene la misma regla, y alinearlo igual (paridad
  cross-platform), si aplica.
- **Golden/behavior-test determinista** (extender el set de validador, p.ej. `examples/*validation*` o un caso
  nuevo): un claim que scope-a `TASK_INDEX#TASK-EXTRACT-<hex>` y `active_tasks/TASK-EXTRACT-<hex>` PASA; un
  selector de fila malformado (p.ej. `active_tasks/FOO-1`, `TASK-12` de 2 digitos) sigue FALLANDO. Cubrir que
  `TASK-\d{4}` y `REQ-*` siguen aceptados (sin regresion).

## DoD

- Aditivo (solo acepta selectores validos antes rechazados); sin aceptar ids malformados nuevos. validate con/sin
  secretos exit 0; drift 0; neutralidad+encoding 0; #4 byte-identica (NO toca protocol.config.json; version
  PINNED, DECISION-0047). Golden verde; sin regresion del resto de la validacion de claims.
- Reproducido por el checker (Arquitecto) desde clon limpio; maker!=checker.
- REPRO objetivo: con el fix, un claim con scope `Area_comun/state/PROJECT_STATE.json#active_tasks/TASK-EXTRACT-X`
  y `Area_comun/state/TASK_INDEX.json#TASK-EXTRACT-X` valida exit 0; un selector de fila malformado sigue exit 1.

## Notas

- Versionado por epoca (DECISION-0047): si Codex bumpea, se reconcilia en CHANGELOG/manifest fuera del config.
- No es necesario re-introducir el claim podado del cierre de TASK-EXTRACT-1F5C13A7B5; basta con que el patron
  acepte la familia para futuros closes con selector fino.
