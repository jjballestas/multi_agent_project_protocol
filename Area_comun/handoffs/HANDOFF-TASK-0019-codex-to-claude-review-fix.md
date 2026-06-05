---
handoff_id: HANDOFF-TASK-0019-codex-to-claude-review-fix
task_id: TASK-0019
from: Codex
to: Claude
date: 2026-06-05
spec_id: Area_comun/specs/SPEC-0019-upgrade-asistido.md
linked_decisions: [DECISION-0006, DECISION-0001]
status: done
requested_action: Review/audit final opcional; TASK-0019 queda cerrado por paridad verificada.
---

# HANDOFF TASK-0019 - Review fix y cierre

## Resumen
Durante review, Codex encontro dos gaps en TASK-0019:
- `upgrade_instance.ps1` fallaba en modo stdout por colision case-insensitive entre parametro
  `-Report` y variable local `$report`.
- `.py/.ps1` no reportaban `eliminado`, aunque `SPEC-0019` lo exige.

Ambos quedaron corregidos y verificados.

## Cambios
- `scripts/upgrade_instance.py`: clasifica `eliminado` comparando union de archivos adoptables
  master+instancia.
- `scripts/upgrade_instance.ps1`: mismo soporte `eliminado`; variable local renombrada a
  `$reportBody`; conteos robustos con `@(...).Count`.
- `examples/upgrade_cases/outdated_instance/core/legacy.md`: fixture de archivo eliminado.

## Evidencia
- `python scripts\upgrade_instance.py --instance examples\upgrade_cases\outdated_instance --master examples\upgrade_cases\master`
  reporta `core/a.md cambiado`, `core/b.md nuevo`, `core/legacy.md eliminado`.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\upgrade_instance.ps1 -Instance examples\upgrade_cases\outdated_instance -Master examples\upgrade_cases\master`
  produce salida normalizada identica.
- Fixture `current_instance` produce salida normalizada identica y sin deltas.
- `--report` y `-Report` escriben a archivo temporal fuera de la instancia.

## Riesgos
No quedan riesgos conocidos para `SPEC-0019`; el enlace CHANGELOG sigue siendo best-effort/omitido,
permitido por la spec.
