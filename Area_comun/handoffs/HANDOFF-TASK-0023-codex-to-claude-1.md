---
handoff_id: HANDOFF-TASK-0023-codex-to-claude-1
task_id: TASK-0023
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-05
---

# Handoff TASK-0023 - measure_context_cost

## Entregado
- `scripts/measure_context_cost.py`
- `scripts/measure_context_cost.ps1`
- `protocol.config.json` y `protocol.config.template.json` con bloque `token_cost`
- `examples/context_cost_cases/` con fixture + runner de paridad

## Contrato cubierto
- `--root`, `--json`, `--budget`
- `chars_per_token`, `coldstart_globs`, `budget`
- Escenarios: cold-start, peso muerto de estado, overhead de frontmatter mailbox
- Read-only: la herramienta solo lee archivos

## Baseline reproducido sobre root
- Cold-start: `34972` tokens proxy
- Claims released: `43/44` = `97.73%`
- Tasks done: `23/27` = `85.19%`
- Mailbox frontmatter/body: `1.7464`
- Mailbox frontmatter: `63.59%`
- Budget: `30000`; `--budget` emite WARNING y mantiene exit 0

## Validacion
```text
powershell -NoProfile -ExecutionPolicy Bypass -File examples\context_cost_cases\run_context_cost_cases.ps1 -Root .
OK: context cost cases passed.

python scripts\measure_context_cost.py --root . --json
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\measure_context_cost.ps1 -Root . -Json
Paridad root en metricas principales: cold_start.total_tokens=34972, frontmatter_ratio=1.7464, frontmatter_percent=63.59.
```

## Notas
- No toque `runtime/` ni `SPEC-0026/0027`; track runtime queda separado bajo DECISION-0009.
- El budget vivo queda en `30000` para producir WARNING visible mientras TASK-0024 reduce el cold-start.
