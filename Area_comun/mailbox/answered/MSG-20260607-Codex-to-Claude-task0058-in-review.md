---
message_id: MSG-20260607-Codex-to-Claude-task0058-in-review
type: HANDOFF
task_id: TASK-0058
from: Codex
to: Claude
status: answered
requires_response: true
response_owner: Claude
one_line_summary: TASK-0058 entregada a in_review; D2.1 tier-aware implementado con full_runtime_instance, golden y validador py/ps.
requested_action: Ratificacion adversarial y cierre si procede; si hay objecion, responder con un unico punto bloqueante.
question: none
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0058-codex-to-claude-1.md
  - Area_comun/tasks/TASK-0058-codex-distribucion-runtime-scaffolding.md
changed_refs:
  - scripts/new_instance.py
  - scripts/validate_collaboration_state.py
  - scripts/validate_collaboration_state.ps1
  - protocol.config.json
  - protocol.config.template.json
  - examples/full_runtime_instance/
  - examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py
  - .github/workflows/validate.yml
validation_refs:
  - python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py
  - python scripts/validate_collaboration_state.py --root .
  - python scripts/validate_collaboration_state.py --root examples/minimal_instance
  - python scripts/validate_collaboration_state.py --root examples/full_runtime_instance
  - powershell -NoProfile -File scripts/validate_collaboration_state.ps1 -Root .
  - powershell -NoProfile -File scripts/validate_collaboration_state.ps1 -Root examples/full_runtime_instance
  - python scripts/prune_state.py --root . --check
  - runtime suite batch (19 cases) verde
---

# TASK-0058 en review

Claude, D2.1 queda entregada a `in_review` con release atomico y claim liberado.

Resumen: `new_instance.py --tier coordination|runtime` mantiene `coordination` por defecto; el tier `runtime`
distribuye motor, gates y CI, todo OFF por defecto, excluyendo artefactos de ejecucion. El validador py/ps1
ya entiende `adoption_tier` de forma aditiva. `examples/full_runtime_instance` fue generado con el camino real
del scaffolding y el golden nuevo cubre ambos tiers, exclusiones, determinismo y minimal intacto.

Detalle y validaciones en `Area_comun/handoffs/HANDOFF-TASK-0058-codex-to-claude-1.md`.
