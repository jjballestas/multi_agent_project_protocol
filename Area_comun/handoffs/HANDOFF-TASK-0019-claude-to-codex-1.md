---
handoff_id: HANDOFF-TASK-0019-claude-to-codex-1
task_id: TASK-0019
from: Claude
to: Codex
date: 2026-06-05
spec_id: Area_comun/specs/SPEC-0019-upgrade-asistido.md
linked_decisions: [DECISION-0006, DECISION-0001]
status: in_review
requested_action: Revisar contra SPEC-0019 y, con PowerShell disponible, ejecutar la paridad .py/.ps1 pendiente.
---

# HANDOFF TASK-0019 — Upgrade asistido entre versiones

## Resumen (delta)
Implementada la herramienta de migración/upgrade **asistida** (DECISION-0006 §4): reporta deltas del
conjunto adoptable entre la versión de una instancia y el master, **sin modificar la instancia**.
Reasignada a Claude por el operador humano; Codex cedió el claim vía mailbox (sin colisión).

## Entregables (rutas exactas)
- `scripts/upgrade_instance.py` — CLI `--instance <ruta> [--master <ruta>] [--report <archivo>]`.
- `scripts/upgrade_instance.ps1` — espejo PowerShell (misma salida normalizada).
- `examples/upgrade_cases/` — `master/` (v0.6.0, `upgrade.adoptable_globs=["core/*.md"]`),
  `outdated_instance/` (v0.5.0), `current_instance/` (v0.6.0).

## Criterios cumplidos (SPEC-0019 acceptance/closure)
| Criterio | Evidencia |
|----------|-----------|
| Reporta `nuevo/cambiado/igual` del conjunto adoptable | outdated → `core/a.md` cambiado, `core/b.md` nuevo |
| No modifica la instancia (read-only) | `git status` sin cambios en la instancia tras la corrida |
| Reporte neutral de dominio | salida solo rutas/versiones/deltas |
| Conjunto adoptable configurable | `master/protocol.config.json` → `upgrade.adoptable_globs` |
| Normaliza BOM/EOL (sin falsos `cambiado`) | lectura `utf-8-sig` (.py) / `ReadAllText` (.ps1) + EOL→`\n` |
| **Paridad `.py`/`.ps1`** | **PENDIENTE** — corrida PowerShell bloqueada en esta sesión (deny-rule) |

## Pruebas ejecutadas
- `python scripts/upgrade_instance.py --instance examples/upgrade_cases/outdated_instance --master examples/upgrade_cases/master` → exit 0; a.md cambiado, b.md nuevo (0.5.0→0.6.0).
- `python scripts/upgrade_instance.py --instance examples/upgrade_cases/current_instance --master examples/upgrade_cases/master` → exit 0; "la instancia esta al dia".
- `git status --short examples/upgrade_cases/` tras correr → instancia intacta (read-only).
- `python scripts/validate_collaboration_state.py --root .` → verde.

## Riesgos residuales / pendientes
- **Paridad `.py`/`.ps1` no ejecutada** aquí (PowerShell denegado por el entorno). El `.ps1` está
  escrito para producir salida idéntica, pero **debe verificarse** con una corrida real (CI con
  ambos runtimes, o Codex, o aprobación puntual). No afirmo paridad hasta esa corrida.
- Falta (opcional) un harness `examples/upgrade_cases/run_upgrade_cases.*` estilo SPEC-0018
  (skip-con-aviso) para automatizar la comparación py↔ps; lo dejo como follow-up menor.

## requested_action
Revisión cruzada contra SPEC-0019 y ejecución de la paridad `.py`/`.ps1` pendiente. Si todo OK,
TASK-0019 pasa a `done`; con TASK-0017/0018 cierra el alcance de **v0.6.0**.
