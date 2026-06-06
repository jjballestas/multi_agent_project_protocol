---
spec_id: SPEC-0032-gate-visibilidad-encoding
task_id: TASK-0033
type: implementation
status: ready
linked_decisions: [DECISION-0012, DECISION-0013, DECISION-0006, DECISION-0001]
created_at: 2026-06-06
author: Claude
---

# SPEC-0032 - Gate de visibilidad y encoding (scan_encoding + handoff-release + liveness)

## Contexto
Adaptacion del metodo de coordinacion (DECISION-0012 ASCII + DECISION-0013 liveness/handoff-release).
"Validador verde" no detectaba ni la corrupcion de encoding ni los claims colgados/stalls. Esta spec
convierte esas reglas en un **gate determinista** y documenta la regla de liveness. Bajo DECISION-0006
(robustez operacional), aditivo.

## Alcance
- `scripts/scan_encoding.py` (+ `scripts/scan_encoding.ps1` con paridad): falla si
  (a) hay **bytes no-ASCII** en el canal entre agentes (`Area_comun/mailbox/**`, `Area_comun/state/*.json`),
  (b) hay **firmas de mojibake** (p.ej. secuencias de doble codificacion UTF-8) en cualquier
  `Area_comun/**` o `runtime/**`. Reporta fichero + linea. `--root` y exit code (0 limpio / 1 fallo).
- **Check de handoff-release** en `scripts/validate_collaboration_state.py` (+ `.ps1`): error si una task
  `in_review` o `done` retiene un claim **activo** de su owner implementador (DECISION-0013 punto 3).
- **Limpieza legacy:** normalizar los ficheros ya corruptos por mojibake (TASK-0017/0018/0021 y los que
  detecte el scan) para dejar el gate verde.
- **Docs:** anadir la **regla de liveness** (DECISION-0013 puntos 1-2) a `AGENTS.md` seccion 7
  (Collaboration Protocol) y al `TASK_PROTOCOL`.
- **CI:** anadir `scan_encoding` como paso (junto al scan de neutralidad y el validador).

## No-alcance
- No implementa un stall-detector temporal (no determinista; queda como senal blanda en docs). No toca el
  runtime (`runtime/**`) ni TASK-0032. No cambia el contrato de turno ni el router.

## execution_pipeline
1. `scan_encoding.py`: recorre los globs, detecta no-ASCII (canal duro) y mojibake (global), exit 1 con
   reporte si hay hallazgos.
2. Paridad `.ps1` (mismo contrato, mismos exit codes).
3. Check handoff-release en el validador: cruza TASK_INDEX (status) con CLAIMS (claims activos por owner).
4. Limpieza legacy hasta que `scan_encoding` salga verde.
5. Docs (AGENTS.md 7 + TASK_PROTOCOL) con la regla de liveness y handoff-release.
6. CI: paso nuevo.

## acceptance_criteria
- Fixture limpio => `scan_encoding` exit 0; fixture con no-ASCII en mailbox/state => exit 1 con la ruta;
  fixture con mojibake => exit 1.
- Repo real: `scan_encoding` exit 0 tras limpiar legacy.
- Validador: task `in_review`/`done` con claim activo del owner => error; tras liberar => verde.
- Paridad `.py`/`.ps1` (mismos veredictos). CI corre el nuevo paso. Validador + scan de neutralidad
  siguen verdes; sin regresion en los golden de runtime.

## linked_decisions
- `DECISION-0012` (ASCII canal), `DECISION-0013` (liveness/handoff-release), `DECISION-0006` (robustez),
  `DECISION-0001` (aditivo => MINOR).

## test_plan
- Golden `examples/encoding_gate_cases/` (limpio, no-ASCII, mojibake) + caso de handoff-release en los
  golden del validador; paridad `.ps1` atestiguada (deny-rule PowerShell en sesion arquitecto: Codex/CI).

## closure_criteria
- `scan_encoding` .py/.ps1 + check handoff-release + limpieza legacy + docs de liveness + CI; golden
  verdes; repo real verde; revision del arquitecto OK; claim liberado **al pasar a in_review** (dogfood
  de la propia regla).

## Risks
- **Falsos positivos del detector de mojibake.** Mitigacion: firmas conservadoras (secuencias que solo
  aparecen en doble codificacion, p.ej. "A-tilde" seguido de simbolo); el canal duro es ASCII estricto
  (cero ambiguedad).
- **Legacy ruidoso.** Mitigacion: limpieza incluida en la task; el gate se enciende ya verde.

## Traceability
| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| ASCII en canal entre agentes | TASK-0033 | golden no-ASCII | exit 1 en violacion |
| Sin mojibake global | TASK-0033 | golden mojibake | exit 1 en violacion |
| Handoff-release (no claim colgado) | TASK-0033 | golden validador | error si in_review+claim activo |
| Regla de liveness documentada | TASK-0033 | revision | AGENTS.md 7 actualizado |
