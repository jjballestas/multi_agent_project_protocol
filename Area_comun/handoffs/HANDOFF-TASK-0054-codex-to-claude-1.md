---
handoff_id: HANDOFF-TASK-0054-codex-to-claude-1
task_id: TASK-0054
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-07
context_refs:
  - Area_comun/tasks/TASK-0054-codex-guardrails-anti-inyeccion-handoffs.md
  - Area_comun/specs/SPEC-0040-fase5-guardrails.md
  - runtime/guardrails.py
  - runtime/turn_validate.py
  - examples/runtime_guardrail_cases/run_runtime_guardrail_cases.py
  - .github/workflows/validate.yml
---

# Handoff TASK-0054 - Guardrails 5.1

## Entrega

- Nuevo `runtime/guardrails.py` con:
  - `classify_provenance`: `registry`/`state`/`config` trusted; fuentes desconocidas, handoff, task_input y tool_output untrusted por defecto.
  - `scan_injection`: patrones deterministas, domain-neutral, para override de protocolo, scope, autoridad, escalado y review/QA.
  - `contain_untrusted`: preserva contenido como dato, emite `security.handoff_injection_contained` y rechaza escalado sostenido solo por contenido untrusted.
- Cableado aditivo en `runtime/turn_validate.py`: lee el handoff referenciado por el turn report, aplica guardrails y convierte errores de seguridad en errores semanticos.
- Nuevo golden `examples/runtime_guardrail_cases/run_runtime_guardrail_cases.py` con los 5 casos de SPEC-0040 sec.4.4.
- CI actualizado con el step `Run runtime guardrail cases`.

## Validacion ejecutada

- Guardrails: 5/5.
- Runtime previo completo: 105/105.
- Total runtime con TASK-0054: 110/110.
- `python scripts/validate_collaboration_state.py --root .` verde con warning no bloqueante de FYI antiguo sin archivar.
- `./scripts/validate_collaboration_state.ps1 -Root .` verde con el mismo warning no bloqueante.
- `python scripts/scan_encoding.py --root .` verde.
- `./scripts/scan_encoding.ps1 -Root .` verde.
- `python scripts/scan_domain_neutrality.py --root .` verde.
- `./scripts/scan_domain_neutrality.ps1 -Root .` verde.
- `python scripts/prune_state.py --root . --check` verde.

## Limites respetados

- No toque tool-policy/allowlist (5.2), firma del envelope (5.3), Fase B ni Fase 6/7.
- No cambie `runtime/turn_schema.json`; el cableado es aditivo sobre reportes existentes.
- Fallback N=2 preservado por las suites runtime existentes.
- Sin red, sin secretos y neutralidad de dominio limpia.
- Claim liberado en el mismo paso que el paso a `in_review` (DECISION-0018).
