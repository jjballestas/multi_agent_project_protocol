---
task_id: TASK-0290
title: "[DECISION-0103][R-A1/follow-up] prune --check: anadir *_ARCHIVE.json al preflight para NOMBRAR un archive malformado (hoy da exit 0 not-due sin nombrarlo)"
type: infra
status: ready
owner: Codex
phase: P2
priority: normal
created_at: 2026-07-23
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0103, TASK-0288, TASK-0287]
linked_decisions: [DECISION-0103]
file: Area_comun/tasks/TASK-0290-ra1-prune-preflight-name-archives.md
intake:
  type: infra
  goal: "Residual R-A1 del veredicto del checker en TASK-0288. El preflight de run_check en scripts/prune_state.py lista solo 4 JSON hot (protocol.config.json, PROJECT_STATE.json, TASK_INDEX.json, CLAIMS.json); un TASK_INDEX_ARCHIVE.json o CLAIMS_ARCHIVE.json MALFORMADO en el camino 'not due' da exit 0 'prune not due' SIN nombrar el archivo (sigue graceful, sin traceback, y en el camino due/apply si lo caza via read_json -> InvalidJsonError -> exit 2). Anadir los 2 *_ARCHIVE.json al tuple del preflight para que --check tambien los NOMBRE gracefulmente. Cambio minimo de higiene; NO cambia semantica ni umbrales."
  acceptance:
    - "prune_state.py --check sobre un TASK_INDEX_ARCHIVE.json (y CLAIMS_ARCHIVE.json) MALFORMADO -> exit no-cero graceful que NOMBRA el archivo, SIN traceback (hoy da exit 0 sin nombrarlo)."
    - "NO-REGRESION: estado valido -> --check funciona igual (prune due/not-due segun corresponda); un hot malformado sigue nombrado y graceful; ningun umbral (recent_done_tasks, recent_released_claims, token threshold) cambia."
    - "Neutralidad de dominio en el script del nucleo."
  verification_cmd:
    - "estado con TASK_INDEX_ARCHIVE.json malformado -> prune_state.py --check -> exit no-cero graceful nombrando el archivo, sin traceback (evidencia)"
    - "idem CLAIMS_ARCHIVE.json (evidencia)"
    - "estado valido limpio -> prune_state.py --check -> comportamiento normal (evidencia)"
    - "python scripts/validate_collaboration_state.py -> 0 ; python scripts/scan_encoding.py -> 0"
  scope_routes:
    - scripts/prune_state.py
    - examples/
  out_of_scope:
    - "Cambiar semantica/umbrales de la poda -- FUERA (solo anadir los 2 archives al preflight)."
    - "El camino due/apply (ya cubierto por read_json -> InvalidJsonError -> exit 2) -- FUERA."
    - "Fondo intocable (protocol.config.json 2E35F26E epoch 1.14.0, dataset N=500, reservadas N=6) -- FUERA."
  risk: low
  estimate: S
---

# TASK-0290 - [DECISION-0103][R-A1] prune --check nombra archives malformados

Origen: residual R-A1 del veredicto de TASK-0288. El preflight de `run_check` omite los
`*_ARCHIVE.json`; un archive malformado en el camino not-due da exit 0 sin nombrarlo. Anadir los 2
al tuple del preflight. Higiene menor, no bloqueante, no cambia semantica.
