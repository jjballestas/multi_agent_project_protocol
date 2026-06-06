---
id: TASK-0033
owner: Codex
status: in_progress
type: implementation
priority: normal
created_at: 2026-06-06
updated_at: 2026-06-06
depends_on: [TASK-0032]
relates_to: [TASK-0017, TASK-0018, TASK-0021]
phase: P2
spec_id: Area_comun/specs/SPEC-0032-gate-visibilidad-encoding.md
linked_decisions: [DECISION-0012, DECISION-0013, DECISION-0006, DECISION-0001]
execution_pipeline: [scripts/scan_encoding.py (ASCII canal + mojibake global, --root, exit code), scripts/scan_encoding.ps1 paridad, check handoff-release en validate_collaboration_state .py/.ps1 (in_review/done con claim activo del owner => error), limpieza legacy (TASK-0017/0018/0021), docs liveness en AGENTS.md 7 + TASK_PROTOCOL, CI paso nuevo, golden examples/encoding_gate_cases]
acceptance_criteria: [scan_encoding limpio=0 / no-ASCII en mailbox-state=1 / mojibake=1, repo real verde tras limpiar legacy, validador marca in_review-done con claim activo del owner, paridad py/ps1, CI corre el paso, sin regresion en golden runtime]
test_plan: [golden examples/encoding_gate_cases (limpio/no-ascii/mojibake) + caso handoff-release en golden del validador; validador + scan neutralidad verdes; paridad ps1 atestiguada]
closure_criteria: [scan_encoding py/ps1 + check handoff-release + limpieza legacy + docs liveness + CI, golden verdes, repo real verde, handoff autocontenido, claim liberado al pasar a in_review]
---

# TASK-0033 - Gate de visibilidad y encoding (scan_encoding + handoff-release + liveness)

> `implementation` -> SDD; implementar contra [SPEC-0032](../specs/SPEC-0032-gate-visibilidad-encoding.md)
> bajo DECISION-0012 (ASCII canal) + DECISION-0013 (liveness/handoff-release) + DECISION-0006 (robustez).
> Adaptacion del metodo de coordinacion: vuelve gateable lo que "validador verde" no detectaba.
> **Secuencia: despues de cerrar TASK-0032.** Aditivo, neutral.

## Resumen
`scan_encoding` (.py/.ps1) que falla ante no-ASCII en el canal entre agentes (mailbox/** + state/*.json)
y ante mojibake global; check de **handoff-release** en el validador (una task `in_review`/`done` no
retiene claim activo de su owner); limpieza de los ficheros legacy ya corruptos; documentar la regla de
liveness (senal de progreso por turno) en `AGENTS.md` 7; paso en CI.

## archivos objetivo (previstos)
- `scripts/scan_encoding.py`, `scripts/scan_encoding.ps1`
- `scripts/validate_collaboration_state.py` + `.ps1` (check handoff-release)
- `examples/encoding_gate_cases/`
- `AGENTS.md` (seccion 7), `Area_comun/protocol/TASK_PROTOCOL.md`
- `.github/workflows/` (paso CI)
- limpieza: `Area_comun/tasks/TASK-0017*`, `TASK-0018*`, `TASK-0021*` (mojibake legacy)

## Dogfood
Esta task debe **liberar su claim al pasar a in_review** (la propia regla que implementa).
ASCII-only en mailbox/state desde ya (DECISION-0012).
