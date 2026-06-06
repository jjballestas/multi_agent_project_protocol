---
handoff_id: HANDOFF-TASK-0055-codex-to-claude-1
task_id: TASK-0055
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-07
context_refs:
  - Area_comun/tasks/TASK-0055-codex-prune-requires-response.md
  - Area_comun/specs/SPEC-0041-prune-requires-response.md
  - scripts/prune_state.py
  - scripts/prune_state.ps1
  - examples/runtime_prune_cases/run_runtime_prune_cases.py
  - .github/workflows/validate.yml
---

# Handoff TASK-0055 - Prune response-required messages

## Entrega

- `scripts/prune_state.py`:
  - parsea frontmatter de mailbox de forma determinista;
  - exime mensajes que requieren respuesta y siguen sin resolver;
  - si detecta uno en `answered/` con `status: open`, lo devuelve a `open/` con status reconciliado;
  - garantiza `status: archived` antes de mover mensajes elegibles a `archived/`.
- `scripts/prune_state.ps1` documenta que la paridad se conserva delegando `-Check` y `-Apply` al Python.
- Nuevo golden `examples/runtime_prune_cases/run_runtime_prune_cases.py`.
- CI actualizado con `Run runtime prune cases`.

## Validacion ejecutada

- `python examples/runtime_prune_cases/run_runtime_prune_cases.py`.
- `python examples/prune_state_cases/run_prune_state_cases.py`.
- `python examples/mailbox_status_cases/run_mailbox_status_cases.py`.
- Runtime completo: 110/110.
- `python scripts/validate_collaboration_state.py --root .` verde con warning FYI no bloqueante.
- `./scripts/validate_collaboration_state.ps1 -Root .` verde con el mismo warning.
- `python scripts/scan_encoding.py --root .` verde.
- `./scripts/scan_encoding.ps1 -Root .` verde.
- `python scripts/scan_domain_neutrality.py --root .` verde.
- `./scripts/scan_domain_neutrality.ps1 -Root .` verde.
- `python scripts/prune_state.py --root . --check` verde.
- `./scripts/prune_state.ps1 -Root . -Check` verde.

## Limites respetados

- No cambie umbrales ni la poda de tasks/claims.
- No toque Fase 5.2/5.3, Fase B ni runtime guardrails.
- Sin red, sin secretos, neutralidad limpia.
- Release atomico aplicado: status `in_review` + claim liberado en el mismo paso.
