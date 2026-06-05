---
id: TASK-0016
owner: Claude
status: done
type: analysis
priority: high
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: []
relates_to: [TASK-0017, TASK-0018, TASK-0019]
phase: P2
linked_decisions: [DECISION-0006, DECISION-0001]
objective: Diseñar la robustez operacional (CI completo, harness tolerantes a runtime, scan de neutralidad, upgrade asistido) y emitir las specs que desbloquean a Codex.
expected_output: DISENO-robustez-operacional.md + SPEC-0017 (CI+scan), SPEC-0018 (harness runtime), SPEC-0019 (upgrade asistido), con spec_id resoluble para TASK-0017/0018/0019.
question_to_resolve: ¿Cuál es el contrato exacto de detección/fallback de runtime, la denylist base de neutralidad y el formato del reporte de upgrade, de forma neutral de dominio?
closure_criterion: Specs publicadas y referenciadas; TASK-0017/0018/0019 pasan a SDD-elegibles (spec_id fijado); validadores verdes.
---

# TASK-0016 — Diseño de robustez operacional + specs

> `analysis` → exige objective/expected_output/question_to_resolve/closure_criterion (ya en
> frontmatter). Ejecuta DECISION-0006: produce el diseño y las specs que descomponen los §1–§4 en
> tareas de implementación neutrales para Codex.

## Alcance
- **SPEC-0017 (CI completo + scan de neutralidad):** qué jobs/pasos añade `validate.yml` (validador
  `.ps1` vía `pwsh`, harness SDD, harness compacto, scan); contrato del script
  `scan_domain_neutrality.(py/ps1)` (denylist + rutas escaneadas/exentas en `protocol.config`);
  casos golden del scan.
- **SPEC-0018 (harness tolerantes a runtime):** contrato de detección con fallback
  (`python`→`py -3`→`python3`; `pwsh`→`powershell`), semántica de `SKIPPED (WARNING)`, cuándo falla
  (lógica o ningún runtime), formato del resumen final. Aditivo: no cambia los exits esperados de
  los casos existentes cuando ambos runtimes están.
- **SPEC-0019 (upgrade asistido):** entradas (protocol_version instancia vs master), salida
  (reporte de adopción con deltas y acciones recomendadas), garantía de **no aplicar sin
  confirmación**, neutralidad de dominio.

## riesgos
- Denylist de neutralidad demasiado agresiva ⇒ falsos positivos en core legítimo. Mitigar:
  denylist base mínima + extensible por instancia; rutas exentas explícitas.
- Detección de runtime en CI vs local divergente. Mitigar: misma lógica de detección en harness y
  documentada en la spec.

## notas_de_ejecucion
- Diseño: `Area_comun/artifacts/DISENO-robustez-operacional.md` (fuente de verdad; define los dos
  conjuntos de archivos —superficie neutral §1.1 y conjunto adoptable §1.2— reutilizados por scan y
  upgrade).
- Specs emitidas: `SPEC-0017-ci-completo-scan-neutralidad.md`, `SPEC-0018-harness-tolerante-runtime.md`,
  `SPEC-0019-upgrade-asistido.md` (todas `status: ready`, `spec_id` resoluble).
- TASK-0017/0018/0019 promovidas `proposed → ready` (SDD-elegibles). Orden sugerido: 0018 → 0017 → 0019.
- Validador de estado verde tras los cambios.
