---
spec_id: SPEC-0023-medidor-context-cost
task_id: TASK-0023
type: implementation
status: ready
linked_decisions: [DECISION-0008, DECISION-0001]
created_at: 2026-06-05
author: Claude
---

# SPEC-0023 — Medidor de costo de contexto

## Contexto
DECISION-0008 §1/§4: hace falta una medición reproducible (gate antes/después). Ver
[DISENO-eficiencia-de-tokens.md](../artifacts/DISENO-eficiencia-de-tokens.md) §4. Es el primer
entregable: sin medidor no hay before/after para las demás tareas.

## Alcance
- `scripts/measure_context_cost.py` y `scripts/measure_context_cost.ps1` (paridad).
- Bloque `token_cost` en `protocol.config(.template).json`.
- (Opcional) paso en `validate.yml` con `--budget` (WARNING).

## No-alcance
- No poda ni cambia estado (solo mide). No factura tokens reales (es proxy chars/divisor).

## execution_pipeline
1. `measure_context_cost.py --root . [--json] [--budget]`. Leer `protocol.config` → `token_cost`
   (`chars_per_token` def 4; `coldstart_globs` con default = lista AGENTS §0; `budget` opcional).
2. Calcular 3 escenarios deterministas: (A) cold-start = suma de tokens de `coldstart_globs` +
   mailbox/open; (B) peso muerto = % `released` en CLAIMS, % `done` en TASK_INDEX; (C) overhead
   frontmatter mailbox (ratio frontmatter/cuerpo). tokens = chars(utf-8-sig)//divisor.
3. Salida humana (tabla) y `--json` (máquina). Exit 0 normal; con `--budget` y cold-start>budget ⇒
   WARNING (exit 0 por defecto; endurecer es decisión aparte).
4. Espejo `.ps1` con misma salida normalizada. Golden case en `examples/context_cost_cases/`.

## acceptance_criteria
- Reporta cold-start, peso muerto (claims/tasks) y overhead frontmatter, determinista.
- `chars_per_token` y `coldstart_globs` configurables; ausentes ⇒ defaults.
- `--json` produce salida parseable; `--budget` avisa sin romper.
- Paridad `.py`↔`.ps1` (mismo reporte para el mismo root).
- No modifica ningún archivo del repo.

## linked_decisions
- `DECISION-0008`: §1/§4 fuente de esta spec.
- `DECISION-0001`: aditivo ⇒ MINOR.

## test_plan
- Correr sobre root: cold-start ≈ baseline del diseño (±, por evolución del estado).
- Golden case con fixture de tamaño conocido ⇒ números esperados; paridad `.py`/`.ps1`.

## closure_criteria
- Medidor funcional con `--json`/`--budget`; paridad; golden case; handoff con baseline reproducido;
  revisión del arquitecto OK; claim liberado.

## Risks
- Divisor proxy ≠ tokenizador real. Mitigación: configurable y documentado como proxy; lo que importa
  es el **delta** consistente, no el absoluto.

## Traceability
| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| Mide 3 escenarios determinista | TASK-0023 | golden case + root | reporte estable |
| Configurable y read-only | TASK-0023 | config ausente/presente; árbol intacto | defaults + sin escritura |
| Paridad .py/.ps1 | TASK-0023 | mismo reporte | paridad confirmada |
