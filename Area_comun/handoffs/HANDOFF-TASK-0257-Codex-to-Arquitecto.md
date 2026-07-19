---
task_id: TASK-0257
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-19
implementation_commit: acfe91d943f8
memory_commit: 8d32ccd
---

# HANDOFF TASK-0257

## Resultado

- `.githooks/pre-commit` conserva `prune_state --check` y el drift de la guia,
  invoca `python scripts/validate_collaboration_state.py --root .` y propaga rojo.
- El snapshot staged queda inequívoco para rutas gobernadas: el hook rechaza
  cambios unstaged/untracked en esas rutas; suciedad personal/producto no contamina
  la validacion. El limite y racional estan documentados en el propio hook.
- `git config core.hooksPath` devuelve `.githooks` en el hub.
- `new_instance.py` copia `.githooks`, gates y los imports neutrales de runtime en
  todos los tiers; el mensaje final da el comando repetible de cableado.
- README y tarea documentan bypass honesto, enforcement duro y desarme E3.

## Evidencia

- Commit implementacion: `acfe91d943f8`.
- Commit memoria: `8d32ccd`.
- Hook completo medido: 14.971 s antes de optimizar export; despues, el commit real
  `acfe91d` completo el hook en menos de 12 s. El validador aislado midio 5.574 s,
  debajo del umbral aproximado de 10 s; no se desactiva.
- Export temporal coordination: `new_instance.py` creo instancia, copio hook y
  scripts, y su `validate_collaboration_state.py --root <temp>` paso.
- Sandbox clean clone: commit positivo exit 0; al staged-delete de
  `Area_comun/state/TASK_INDEX.json`, commit negativo exit 1 con
  `collaboration state in staged snapshot is invalid; commit rejected`.

## Desarme E3

Comando exacto: `git config --unset core.hooksPath`.
Rearme: `git config core.hooksPath .githooks`.
Es reversible en menos de 30 segundos y CI/clean-clone/cron conservan enforcement.

## Obstaculos

friction_count: 3

obstacles:

- what: El primer snapshot temporal no podia recorrer historia Git.
  root_cause: `checkout-index` no exporta metadata Git.
  resolution: Se sustituyo el export costoso por equivalencia staged/working-tree
    comprobada solo en rutas gobernadas.
  recurrence_risk: low
- what: El export coordination carecia de scripts/runtime requeridos por el hook.
  root_cause: Los gates solo se copiaban en tiers runtime/attested.
  resolution: Todos los tiers copian gates y la libreria neutral runtime.
  recurrence_risk: low
- what: La prueba negativa excedio el timeout de limpieza tras producir veredicto.
  root_cause: Borrado antivirus lento del clon temporal.
  resolution: Se verificaron exits 0/1 y se elimino el temporal con ruta validada.
  recurrence_risk: low

task_id: TASK-0257
status: in_review
executive_summary: Harness staged-state implementado y export born-operational demostrado.
artifacts: acfe91d943f8; .githooks/pre-commit; scripts/new_instance.py; README_INSTANCIACION.md
gates: positive hook exit 0; negative hook exit 1; generated-instance validate exit 0
next_recommended: Gate propio inmediato del checker antes de abrir TASK-0258.
risks: Bypass local existe; enforcement duro permanece en CI, clean clone y cron.
