---
message_id: MSG-20260723-Arquitecto-to-Codex-ACTION-GO-TASK-0290
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "GO TASK-0290 (R-A1/follow-up de DECISION-0103, residual del veredicto de TASK-0288, type=infra, maker=Codex, checker=Analista, risk=low, estimate=S). El preflight de run_check en scripts/prune_state.py lista solo 4 JSON hot (protocol.config.json, PROJECT_STATE.json, TASK_INDEX.json, CLAIMS.json); un TASK_INDEX_ARCHIVE.json o CLAIMS_ARCHIVE.json MALFORMADO en el camino 'not due' da exit 0 'prune not due' SIN nombrar el archivo. Anade los 2 *_ARCHIVE.json al tuple del preflight para que --check tambien los NOMBRE gracefulmente (exit no-cero, sin traceback). Cambio minimo de higiene; NO cambia semantica ni umbrales. Acceptance: (1) prune_state.py --check sobre TASK_INDEX_ARCHIVE.json (y CLAIMS_ARCHIVE.json) MALFORMADO -> exit no-cero graceful que NOMBRA el archivo, sin traceback (hoy exit 0 sin nombrarlo); (2) NO-REGRESION: estado valido -> --check igual (due/not-due segun corresponda); un hot malformado sigue nombrado y graceful; ningun umbral cambia; (3) neutralidad de dominio en el nucleo. verification_cmd: estado con TASK_INDEX_ARCHIVE.json malformado -> --check -> exit no-cero graceful nombrando el archivo sin traceback (evidencia) + idem CLAIMS_ARCHIVE.json + estado valido limpio -> --check normal + python scripts/validate_collaboration_state.py -> 0 + python scripts/scan_encoding.py -> 0. Scope: scripts/prune_state.py + examples/. FUERA: cambiar semantica/umbrales de la poda (solo anadir los 2 archives al preflight), el camino due/apply (ya cubierto por read_json -> InvalidJsonError -> exit 2), el fondo (protocol.config.json pineado 2E35F26E epoch 1.14.0, dataset N=500, reservadas N=6). Entrega TASK-0290 in_review + handoff bien formado (gates con exit code) + release."
question: "Confirmas ETA para TASK-0290 y que SOLO anades los 2 *_ARCHIVE.json al tuple del preflight (para nombrar el archive malformado en --check) SIN cambiar semantica/umbrales de la poda, con evidencia por el entrypoint real (sin traceback)?"
created_at: 2026-07-23
context_refs:
  - Area_comun/tasks/TASK-0290-ra1-prune-preflight-name-archives.md
  - Area_comun/artifacts/Analista-TASK-0288-graceful-malformed-json-verdict.md
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
one_line_summary: "GO TASK-0290 (R-A1): anadir TASK_INDEX_ARCHIVE.json + CLAIMS_ARCHIVE.json al preflight de prune --check para nombrar un archive malformado; sin cambio de semantica; evidencia por entrypoint real."
---

# ACTION - GO TASK-0290 (R-A1: prune --check nombra archives malformados)

Hora local: 2026-07-23 19:18 (UTC+2). Origen: residual R-A1 del veredicto del checker en TASK-0288.
Follow-up de mantenimiento autorizado por el Operador (directiva "terminas R1-A1"). Ficha completa en
`Area_comun/tasks/TASK-0290-ra1-prune-preflight-name-archives.md`.

## El defecto

`run_check` (scripts/prune_state.py) hace preflight de 4 JSON hot pero NO de los `*_ARCHIVE.json`. Un
`TASK_INDEX_ARCHIVE.json`/`CLAIMS_ARCHIVE.json` malformado en el camino not-due da exit 0 sin nombrar
el archivo (sigue graceful; el camino due/apply si lo caza via read_json -> InvalidJsonError -> exit 2).

## LA GUARDA (no cambiar semantica)

SOLO anade los 2 `*_ARCHIVE.json` al tuple del preflight. NO cambies umbrales ni la logica de la poda.
El resultado: --check tambien nombra un archive malformado (graceful, sin traceback). Evidencia por el
entrypoint real.

## Entrega esperada

TASK-0290 a `in_review` + handoff con `verification_cmd` y exit codes (archive malformado -> no-cero
graceful nombrando; estado valido -> normal; validate/scan_encoding -> 0) + release. ASCII puro.
Fix-loop tope 2 iteraciones.
