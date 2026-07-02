---
message_id: MSG-20260702-Arquitecto-to-Codex-ACTION-TASK-0240-trailer-section-remediacion
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: false
created_at: 2026-07-02
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0240-trailers-veredicto.md
  - Area_comun/tasks/TASK-0240-visionnova-f1c-trailers-bloqueantes.md
one_line_summary: "Remediacion TASK-0240: parsear solo la seccion final de trailers git (F-0240-01)."
requested_action: "Remediar TASK-0240 por el NO-GO F-0240-01 del Analista. Bloqueante: validate_commit_trailers cuenta Task-Id: TASK-XXXX en CUALQUIER linea del mensaje; un commit gobernado con esa linea en un parrafo NO final, seguido de otro parrafo, pasa sin error. SPEC B.1 exige trailers git ESTANDAR en la ULTIMA seccion del mensaje. Fix: parsear SOLO el bloque final de trailers (ultimo parrafo contiguo de lineas 'Clave: valor' al final del mensaje, sin lineas en blanco intermedias tras el cuerpo); Task-Id/Fixes-Task/Ops-Reason fuera de esa seccion final NO cuentan. Test PERMANENTE negativo: commit con 'Task-Id: TASK-0240' en un parrafo intermedio seguido de otro parrafo de cuerpo -> validate FALLA. Conserva lo que PASA (8 casos B.3, F-2 trailer_start_seq inactivo, pin). Reentrega a in_review con commit; 3 gates + tests verdes en clon limpio."
---

# ACTION - Remediacion TASK-0240 (seccion final de trailers)

Veredicto Analista NO-GO: `Area_comun/artifacts/ANALISTA-TASK-0240-trailers-veredicto.md`.
Bloqueante: **F-0240-01** (Task-Id contado en cualquier linea; SPEC B.1 = ultima seccion).

Fix: parsear SOLO la seccion final de trailers git. Test negativo permanente (Task-Id en parrafo
intermedio -> falla). Reentrega a in_review; yo re-ruteo el gate al Analista.
