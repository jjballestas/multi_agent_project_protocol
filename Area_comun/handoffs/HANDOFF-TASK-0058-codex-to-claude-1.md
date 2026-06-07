---
handoff_id: HANDOFF-TASK-0058-codex-to-claude-1
task_id: TASK-0058
from: Codex
to: Claude
status: in_review
requires_response: true
response_owner: Claude
requested_action: Ratificacion adversarial de TASK-0058 y cierre si procede.
context_refs:
  - Area_comun/tasks/TASK-0058-codex-distribucion-runtime-scaffolding.md
  - Area_comun/specs/SPEC-0044-distribucion-runtime.md
  - Area_comun/decisions/DECISION-0019-distribucion-runtime.md
changed_refs:
  - scripts/new_instance.py
  - scripts/validate_collaboration_state.py
  - scripts/validate_collaboration_state.ps1
  - protocol.config.json
  - protocol.config.template.json
  - examples/full_runtime_instance/
  - examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py
  - .github/workflows/validate.yml
validation_refs:
  - python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py
  - python scripts/validate_collaboration_state.py --root .
  - python scripts/validate_collaboration_state.py --root examples/minimal_instance
  - python scripts/validate_collaboration_state.py --root examples/full_runtime_instance
  - powershell -NoProfile -File scripts/validate_collaboration_state.ps1 -Root .
  - powershell -NoProfile -File scripts/validate_collaboration_state.ps1 -Root examples/full_runtime_instance
  - python scripts/scan_encoding.py --root .
  - powershell -NoProfile -File scripts/scan_encoding.ps1 -Root .
  - python scripts/scan_domain_neutrality.py --root .
  - powershell -NoProfile -File scripts/scan_domain_neutrality.ps1 -Root .
  - python scripts/prune_state.py --root . --check
  - powershell -NoProfile -File scripts/prune_state.ps1 -Root . -Check
  - runtime suite batch (19 cases) verde
---

# TASK-0058 Handoff

## Resultado

Implementado D2.1 como distribucion por tiers:

- `protocol.config.json` declara `adoption_tier: runtime` para este repo vivo.
- `protocol.config.template.json` declara `{{ADOPTION_TIER}}` y deja `runtime.enabled`, `tool_policy.enabled` y `event_auth.enabled` en `false` para instancias nuevas.
- `scripts/new_instance.py` acepta `--tier coordination|runtime`, con default `coordination`.
- El tier `coordination` conserva el comportamiento ligero actual.
- El tier `runtime` copia `runtime/`, scripts de gates y workflow CI; excluye `runtime/state`, `runtime/runs` y cualquier `__pycache__`.
- Se copia `measure_context_cost.py` porque `prune_state.py` lo necesita para que el tier runtime sea autocontenido.
- `scripts/validate_collaboration_state.py` y `.ps1` son tier-aware: ausencia de `adoption_tier` equivale a `coordination`; `runtime` exige motor/gates/CI presentes.
- `examples/full_runtime_instance/` fue generado con `--tier runtime` y valida verde.
- `examples/runtime_instantiation_cases/` genera ambos tiers en tmp, comprueba OFF-by-default, exclusiones, determinismo, minimal intacto y paridad ps1 cuando hay PowerShell.

## Validacion ejecutada

- Golden nuevo: `OK: runtime instantiation cases passed (5 + ps1 parity when available).`
- Validador Python: repo vivo verde con warnings preexistentes de mailbox ACK/FYI abiertos; `minimal_instance` verde; `full_runtime_instance` verde.
- Validador PowerShell: repo vivo verde con los mismos warnings preexistentes; `full_runtime_instance` verde.
- Encoding py/ps: verde.
- Neutralidad py/ps: verde.
- Prune py/ps: tras aplicar poda de mantenimiento (`claims_archived=1`), `OK: prune not due (cold_start_tokens=16383).`
- Suite runtime completa: 19 runners verdes, incluyendo router, N-agent, property, concurrency, guardrails, tool-policy, eventlog, event-auth, instantiation, apply, loop, observability y adapter recorded.
- Suites auxiliares ejecutadas: encoding_gate, handoff_release, mailbox_status, SDD, compact_comms, neutrality_scan, prune_state.

## Notas de revision

- No se activo el motor en instancias nuevas; el tier runtime solo distribuye el motor presente y apagado.
- `examples/minimal_instance` no fue modificado y valida verde.
- `pwsh` no estaba disponible en esta maquina; la paridad PowerShell se ejecuto con `powershell` 5.1.
- Queda fuera de alcance D2.2: `upgrade_instance.py` tier-aware + `runtime_version`.
