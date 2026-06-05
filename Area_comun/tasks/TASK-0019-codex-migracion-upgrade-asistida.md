---
id: TASK-0019
owner: Claude
status: in_review
type: implementation
priority: normal
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0016]
relates_to: [TASK-0017, TASK-0018]
phase: P2
spec_id: Area_comun/specs/SPEC-0019-upgrade-asistido.md
linked_decisions: [DECISION-0006, DECISION-0001]
execution_pipeline: [Leer protocol_version instancia vs master, Calcular deltas de core y *.template.* entre versiones, Emitir reporte de adopción con acciones recomendadas, Garantizar no-aplicar-sin-confirmación, Paridad .py/.ps1 y golden cases]
acceptance_criteria: [Reporta deltas core/template entre versión de instancia y master, No modifica archivos sin confirmación explícita, Reporte neutral de dominio, Paridad .py/.ps1, Casos golden (instancia desactualizada vs al día)]
test_plan: [Fixtures de instancia en versión previa vs actual, verificar reporte de deltas y ausencia de escritura sin confirmación]
closure_criteria: [Herramienta de upgrade asistida funcional con reporte, preserva gobernanza por-decisión (DECISION-0001), handoff documenta uso, claim liberado]
---

# TASK-0019 — Migración/upgrade asistida entre versiones

> `implementation` → SDD obligatorio; implementar contra
> [SPEC-0019](../specs/SPEC-0019-upgrade-asistido.md) y DECISION-0006 §4. `ready` (spec emitida por
> TASK-0016). Asiste, **no impone**: la adopción sigue siendo por decisión de la instancia
> (preserva DECISION-0001 y el risk de drift).

## Resumen
Baja el costo operativo de detectar y razonar el delta entre versiones del protocolo sin
automatizar la política de adopción. Ver DECISION-0006 §4.

## entregable previsto
- `scripts/upgrade_instance.py` + `scripts/upgrade_instance.ps1` (paridad) + golden fixtures.

## notas_de_ejecucion
- Reasignada a Claude por el operador humano (Codex la cedió vía mailbox
  `MSG-20260605-Codex-to-Claude-task0019-collision-audit` → `...-ownership-confirmed`).
- Entregado: `scripts/upgrade_instance.py` (CLI `--instance/--master/--report`, conjunto adoptable
  configurable vía `upgrade.adoptable_globs`, normaliza BOM/EOL, **read-only** sobre la instancia),
  `scripts/upgrade_instance.ps1` (espejo), fixtures `examples/upgrade_cases/` (master + outdated +
  current).
- **Verificado (.py):** outdated → `core/a.md` cambiado + `core/b.md` nuevo (0.5.0→0.6.0);
  current → "al dia"; `git status` confirma instancia intacta tras la corrida (read-only).
- **PENDIENTE:** paridad `.py`/`.ps1` no ejecutada en esta sesión (corrida PowerShell bloqueada por
  deny-rule del entorno). Verificar en CI / por Codex / con aprobación puntual del operador.
- Handoff: `Area_comun/handoffs/HANDOFF-TASK-0019-claude-to-codex-1.md`.
