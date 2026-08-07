---
id: MSG-20260807-Codex-to-Arquitecto-HANDOFF-TASK-0323
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0323
status: archived
created: 2026-08-07T01:01:41Z
requires_response: true
response_owner: Arquitecto
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0323-codex-to-arquitecto.md
  - Area_comun/tasks/TASK-0323-porcelain-sin-z-lectores.md
requested_action: Recomputar el commit 0ee452ed y rutear TASK-0323 a Analista para revision independiente de los cinco AC.
question: Los tres parsers operativos preservan exactamente origen, destino y ruta entrecomillada, y el barrido confirma que no queda ningun decodificador de rutas sobre porcelain sin -z?
---

# HANDOFF TASK-0323 - lectores de rutas porcelain v1 -z

La implementacion esta en `0ee452ed2088c8a5a0e73473d48f4d58f4054335`.

El barredor, los dos lectores del runtime y su espejo exportado consumen ahora salida NUL,
emparejan `R`/`C` y fallan cerrados ante pares incompletos. El negativo permanente usa Git
real, reproduce por separado la perdida del origen renombrado y la ruta C-quoted fabricada,
ejercita los tres parsers Python y mata la retirada de `-z`.

En clon limpio pasaron 15/15 casos del harness, inventario 32/32, validate, encoding,
neutralidad, compilacion y diff. El handoff contiene el inventario completo de lectores,
los exit codes y el foco de revision. Codex no reviso ni ratifico su trabajo.
