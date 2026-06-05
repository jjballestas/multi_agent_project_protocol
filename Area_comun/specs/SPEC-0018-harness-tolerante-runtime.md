---
spec_id: SPEC-0018-harness-tolerante-runtime
task_id: TASK-0018
type: implementation
status: ready
linked_decisions: [DECISION-0006, DECISION-0001]
created_at: 2026-06-05
author: Claude
---

# SPEC-0018 — Harness de validación tolerantes a runtime (skip con aviso)

## Contexto
`run_sdd_cases.ps1` y `run_compact_comms_cases.ps1` invocan `& python` **y** `& powershell` y
comparan salidas; si falta cualquiera de los dos runtimes, el harness cae por **entorno**, no por
lógica (fragilidad reportada en la auditoría). DECISION-0006 §1 fija la política **skip con aviso**.
Ver [DISENO-robustez-operacional.md](../artifacts/DISENO-robustez-operacional.md) §2.

## Alcance
- `examples/sdd_validation_cases/run_sdd_cases.ps1`
- `examples/compact_comms_validation_cases/run_compact_comms_cases.ps1`
- (Opcional, recomendado) una función de resolución compartida documentada para futuros harness.

## No-alcance
- No cambiar los casos golden ni sus exits esperados.
- No cambiar la lógica de los validadores `.py`/`.ps1`.
- No exigir ambos runtimes (eso sería MAJOR).

## execution_pipeline
1. Resolver Python: primer comando con `--version` exit 0 en orden `python`, `py -3`, `python3`;
   si ninguno ⇒ `none`.
2. Resolver PowerShell: `pwsh` → `powershell`; si ninguno ⇒ `none`.
3. Por cada caso: ejecutar la mitad de cada runtime **disponible** contra su exit esperado; la mitad
   del runtime ausente ⇒ `SKIPPED (WARNING)` con mensaje explícito.
4. Comparar paridad (salida normalizada `.py`↔`.ps1`) **solo si ambos** ejecutaron.
5. Exit 1 si: (a) un runtime presente da exit inesperado, (b) ambos presentes y difieren, o
   (c) ningún runtime disponible. En otro caso exit 0 (incluso con skips).
6. Imprimir resumen final: `RESUMEN: py[ok/skip/fail] ps[ok/skip/fail] paridad[checked/skipped]`.
7. Aplicar el mismo patrón a ambos harness.

## acceptance_criteria
- Falta un runtime ⇒ su mitad `SKIPPED (WARNING)` y el harness **no** falla por ello.
- Un runtime presente con exit inesperado ⇒ exit 1.
- Ambos presentes con salidas distintas ⇒ exit 1 (paridad rota).
- Ningún runtime ⇒ exit 1 con mensaje claro.
- Con **ambos** runtimes, exits esperados y comparación de paridad **no cambian** vs hoy.
- Resumen final impreso siempre (sin truncado silencioso).

## linked_decisions
- `DECISION-0006`: §1 es la fuente de esta spec.
- `DECISION-0001`: aditivo (más tolerante) ⇒ MINOR; exigir ambos runtimes sería MAJOR.

## test_plan
- Ejecutar ambos harness con ambos runtimes presentes ⇒ comportamiento idéntico al actual (verde).
- Simular ausencia de python (PATH sin python/py/python3) ⇒ mitad python `SKIPPED`, harness verde.
- Simular ausencia de powershell ⇒ simétrico.
- Forzar un exit inesperado en un caso (fixture) ⇒ exit 1.

## closure_criteria
- Harness no fallan por entorno; paridad intacta con ambos runtimes; resumen final presente.
- Handoff mapea cada acceptance/closure a evidencia; revisión cruzada del arquitecto OK; claim liberado.

## Risks
- Detección divergente CI vs local. Mitigación: misma lógica de resolución en ambos harness,
  documentada; CI mantiene ambos runtimes para ejercer paridad real.
- `py -3` inexistente fuera de Windows. Mitigación: es solo un eslabón del fallback; en Linux
  resuelve `python3`.

## Traceability
| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| Skip con aviso si falta un runtime | TASK-0018 | simular ausencia py/ps | harness verde con SKIPPED |
| Falla solo por lógica o sin runtime | TASK-0018 | fixture exit inesperado; sin runtime | exit 1 en ambos |
| No-regresión con ambos runtimes | TASK-0018 | run con py+ps | exits/paridad iguales a hoy |
