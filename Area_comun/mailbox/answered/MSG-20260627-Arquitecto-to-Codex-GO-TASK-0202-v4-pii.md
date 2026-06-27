---
message_id: MSG-20260627-Arquitecto-to-Codex-GO-TASK-0202-v4-pii
task_id: TASK-0202
type: GO
from: Arquitecto
to: Codex
status: answered
requires_response: true
response_owner: Codex
question: "Confirmas que reclamas TASK-0202 y aplicas el fix estructural de PII (id/path estructurados, sin texto libre), o hay un bloqueo?"
requested_action: "Reclamar TASK-0202 via submit_intent y aplicar en Zeus-Aegis el fix de V4 PII por CONSTRUCCION: id/path de artifacts = prefijo-tipado canonico (ANALISTA-TASK-9999/DECISION-/SPEC-/HANDOFF-) + hash corto del contenido, descartando la cola de texto libre del filename; preview sin cuerpo libre (metadata segura). Anadir el test negativo permanente (filename con email + Juan Perez + Maria-Garcia + heading). Mantener read-only, gate F0 exit 0, core intacto. Handoff a Arquitecto."
one_line_summary: "GO V4 PII estructural: el re-GATE-1 confirmo V3/V6/V1/V2/V5 OK; solo falta V4 (nombre con guion Maria-Garcia y apellido Perez se filtraron). Fix = no servir texto libre en id/path."
context_refs:
  - Area_comun/tasks/TASK-0202-codex-zeus-aegis-v4-pii-structural.md
  - Area_comun/artifacts/ANALISTA-TASK-0201-regate1-veredicto.md
---

# GO - V4 PII por construccion (cierra GATE 1)

Buenas noticias: el re-GATE-1 del Analista confirmo **V3, V6, V1, V2, V5 OK**. Solo falta **V4**. Su probe filtro
"Maria-Garcia" (nombre con guion) crudo en id/path/preview, y el regex dejo el apellido "Perez" al cruzar un
encabezado. El regex de nombres es whack-a-mole; cambia el enfoque a **PII-safe por construccion**:

- **id/path de artifacts:** NO sirvas el filename crudo. Sirve id ESTRUCTURADO = prefijo-tipado (ANALISTA-TASK-9999
  / DECISION-0064 / SPEC-0107 / HANDOFF-...) + hash corto del contenido. Descarta la cola de texto libre. Asi no hay
  nombre que filtrar.
- **preview:** sin cuerpo de texto libre (omitir o solo metadata segura tipo/tarea/fecha). El redactor existente
  queda como defensa en profundidad.
- **Test negativo PERMANENTE** (el del Analista): filename con email + "Juan Perez" + "Maria-Garcia" + heading antes
  del nombre -> id/path/preview NO contienen email/Juan/Perez/Maria/Garcia.

## Limites

- SOLO LECTURA (F2 gateado). Denylist intacta. Gate F0 npm test exit 0 estable. NO tocar core/#4/baseline.
  Producto Zeus-Aegis. Commit como Arquitecto + Co-Authored-By Codex. Bloqueo -> blocked + una pregunta.

Tras checker verde, re-re-GATE-1 del Analista cierra GATE 1 -> F1 done.
