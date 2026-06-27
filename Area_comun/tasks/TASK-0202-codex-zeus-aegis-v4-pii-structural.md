---
task_id: TASK-0202
title: "Zeus-Aegis V4 PII por CONSTRUCCION (no regex): id/path estructurados sin texto libre + preview seguro + test negativo permanente (SPEC-0107, GATE 1)"
type: integration
status: in_review
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0107
created_at: 2026-06-27
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-Aegis
project: Zeus-Aegis
linked_decisions: [DECISION-0064, DECISION-0040]
file: Area_comun/tasks/TASK-0202-codex-zeus-aegis-v4-pii-structural.md
---

# TASK-0202 - V4 PII por construccion (cierra GATE 1)

> maker=Codex / checker=Arquitecto. Repo PRODUCTO Zeus-Aegis. Cierra el unico vector que falta de GATE 1 (V4, PII).
> El re-GATE-1 del Analista (TASK-0201) confirmo V3/V6/V1/V2/V5 OK, pero V4 SIGUE filtrando: "Maria-Garcia"
> (nombre con guion) salio crudo en id/path/preview, y el regex de nombres consumio una palabra del encabezado y
> dejo el apellido "Perez". Ver Area_comun/artifacts/ANALISTA-TASK-0201-regate1-veredicto.md.

## Cambio de enfoque: PII-safe por CONSTRUCCION (no mas regex de nombres)

El regex de nombres es whack-a-mole (nombres con guion, acentos, encabezados que cruzan). El fix robusto es **no
servir texto libre** en los identificadores:

- **id/path de artifacts:** NO servir el filename crudo. Servir un id ESTRUCTURADO = el prefijo tipado canonico
  (p.ej. `ANALISTA-TASK-9999`, `DECISION-0064`, `SPEC-0107`, `HANDOFF-...`) + un sufijo de **hash corto del
  contenido** (p.ej. sha256[:8]). Descartar por completo la cola de texto libre del nombre de archivo. Asi NO hay
  nombre que filtrar en id/path.
- **preview:** o se OMITE el preview de cuerpo libre, o se reduce a metadata estructurada segura (tipo, tarea,
  fecha) + a lo sumo la primera linea ya pasada por el redactor existente PERO truncada de forma que no exponga
  texto libre del cuerpo. Preferir lo conservador: sin cuerpo libre.
- Mantener el redactor existente (email/phone/id) como defensa en profundidad para los campos que si se sirvan.

## DoD

- AC1 id/path de artifacts NO contienen texto libre del filename: solo prefijo-tipado + hash corto. Verificable: un
  artifact con filename con email/nombre/nombre-con-guion -> id/path NO los contienen.
- AC2 preview no expone texto libre del cuerpo (omitido o metadata segura).
- AC3 **test negativo PERMANENTE** (el que pidio el Analista): artifact con filename que incluya un email,
  "Juan Perez" y "Maria-Garcia", y body con un heading antes del nombre -> id/path/preview NO contienen email,
  "Juan", "Perez", "Maria", "Garcia", "Maria-Garcia". Cubrir variantes con guion y cruces de encabezado.
- AC4 sigue read-only (denylist intacta); gate F0 npm test exit 0 estable; core protocolo intacto; handoff a Arquitecto.

## Nota

- Tras checker verde, re-re-GATE-1 (Analista) confirma V4 y cierra GATE 1 (si todo pasa, F1 done).
- Commit como Arquitecto con Co-Authored-By Codex. Minimal narration. Bloqueo -> blocked + una pregunta.
- POLITICA: el Arquitecto actualiza Zeus-Aegis/pipeline.html tras cerrar este caso.
