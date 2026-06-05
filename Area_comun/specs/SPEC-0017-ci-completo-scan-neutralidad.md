---
spec_id: SPEC-0017-ci-completo-scan-neutralidad
task_id: TASK-0017
type: implementation
status: ready
linked_decisions: [DECISION-0006, DECISION-0001]
created_at: 2026-06-05
author: Claude
---

# SPEC-0017 — CI completo + scan de neutralidad de dominio

## Contexto
`AGENTS.md` §5 declara como quality gates `validador_verde` y `neutralidad_de_dominio`, pero CI
solo corre `validate_collaboration_state.py` x2 y el scan de neutralidad **no existe** como script.
DECISION-0006 §2-§3 cierra esa grieta. Ver
[DISENO-robustez-operacional.md](../artifacts/DISENO-robustez-operacional.md) §3.

## Alcance
- `.github/workflows/validate.yml`: añadir pasos (ver execution_pipeline).
- `scripts/scan_domain_neutrality.py` y `scripts/scan_domain_neutrality.ps1` (paridad).
- Bloque `domain_neutrality` en `protocol.config.template.json` y `protocol.config.json`.
- Golden cases en `examples/neutrality_scan_cases/`.

## No-alcance
- No cambiar la lógica de `validate_collaboration_state.*`.
- No escanear `profiles/` ni `examples/` ni el área viva del dogfood (exentos por diseño §1.2).
- No convertir WARNINGs existentes en errores; no tocar formatos obligatorios.

## execution_pipeline
1. Implementar `scan_domain_neutrality.py`: leer `protocol.config.json` → `domain_neutrality`
   (`enabled`, `denylist`, `scan_globs`, `exempt_globs`). Si ausente o `enabled:false` ⇒ exit 0.
2. Matching case-insensitive con límite de palabra (`\bterm\b`); `scan_globs` − `exempt_globs`.
   Términos multi-palabra soportados. Salida `ruta:linea: término`; exit 1 si hay hallazgos.
3. Espejar la lógica en `scan_domain_neutrality.ps1` (mismos mensajes y exits → paridad).
4. Añadir `domain_neutrality` a `protocol.config.template.json` (`enabled:true`, denylist mínima
   neutral, `scan_globs/exempt_globs` del diseño §3.2) y a `protocol.config.json` dogfood
   (denylist del piloto: `trading`, `spot`, `binance`, `backtest`, …).
5. Golden cases en `examples/neutrality_scan_cases/`: fixture **limpio** (exit 0) y fixture con un
   término de denylist en una ruta escaneada (exit 1); harness que verifica paridad `.py`/`.ps1`.
6. Extender `validate.yml` (un job ubuntu, setup-python + pwsh): añadir
   `validate_collaboration_state.ps1` (dogfood + minimal vía pwsh), `run_sdd_cases.ps1`,
   `run_compact_comms_cases.ps1`, y `scan_domain_neutrality.py --root .`.
7. Verificar build verde; handoff con criterios + pruebas.

## acceptance_criteria
- `validate.yml` ejecuta: validate.py x2, validate.ps1 (pwsh) x2, harness SDD, harness compacto,
  y scan de neutralidad.
- `scan_domain_neutrality.*` falla (exit 1) ante un término de denylist en zona escaneada y pasa
  (exit 0) sobre el repo actual (área viva exenta).
- Paridad `.py`↔`.ps1` del scan (mismos hallazgos, exits y mensajes).
- `domain_neutrality` configurable (denylist + globs) en `protocol.config*.json`; ausente/`false`
  ⇒ sin scan (no rompe instancias existentes).
- Sin términos de dominio introducidos en la superficie neutral (§1.1); core neutral intacto.

## linked_decisions
- `DECISION-0006`: §2 (CI completo) y §3 (scan ejecutable) son la fuente de esta spec.
- `DECISION-0001`: cambio aditivo ⇒ MINOR v0.6.0; endurecer gates sería MAJOR.

## test_plan
- Golden harness de neutralidad (exit 0/1 + paridad `.py` vs `.ps1`) sobre
  `examples/neutrality_scan_cases/`.
- `scan_domain_neutrality.py --root .` y `.ps1 -Root .` ⇒ exit 0 en este repo.
- CI: el workflow corre en ubuntu con ambos runtimes; todos los pasos verdes.
- `validate.py`/`.ps1` sobre dogfood + ejemplos siguen verdes.

## closure_criteria
- Todos los gates de `AGENTS.md` §5 corren en CI y verdes.
- Scan integrado con golden cases y paridad; config documentada.
- Handoff mapea cada acceptance/closure a evidencia; revisión cruzada del arquitecto OK; claim liberado.

## Risks
- Denylist demasiado amplia ⇒ falsos positivos. Mitigación: límite de palabra, denylist base
  mínima, `exempt_globs` explícitos, extensible por instancia.
- `pwsh` ausente en algún runner. Mitigación: `ubuntu-latest` trae `pwsh`; el job lo asume y, si
  faltara, los harness de SPEC-0018 degradan a `SKIPPED (WARNING)` sin romper (pero CI debe tener
  ambos para ejercer paridad).

## Traceability
| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| CI corre validador .ps1 + ambos harness + scan | TASK-0017 | CI verde en ubuntu | §5 AGENTS verificado en CI |
| Scan de neutralidad ejecutable y configurable | TASK-0017 | golden cases + scan repo exit 0 | scan integrado con paridad |
| Aditividad (no rompe instancias sin config) | TASK-0017 | validate.* ejemplos verdes | instancias existentes verdes |
