---
handoff_id: HANDOFF-TASK-0061-codex-to-claude-1
task_id: TASK-0061
from: Codex
to: Claude
status: in_review
requires_response: true
response_owner: Claude
requested_action: Ratificacion adversarial de TASK-0061 y cierre si procede.
context_refs:
  - Area_comun/tasks/TASK-0061-codex-upgrade-tier-aware.md
  - Area_comun/specs/SPEC-0047-d2.2-upgrade-tier-aware.md
changed_refs:
  - protocol.config.json
  - protocol.config.template.json
  - scripts/upgrade_instance.py
  - scripts/upgrade_instance.ps1
  - examples/runtime_upgrade_cases/run_runtime_upgrade_cases.py
  - .github/workflows/validate.yml
validation_refs:
  - python examples/runtime_upgrade_cases/run_runtime_upgrade_cases.py
  - python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py
  - python scripts/upgrade_instance.py --instance examples/upgrade_cases/outdated_instance --master examples/upgrade_cases/master
  - powershell -NoProfile -File scripts/upgrade_instance.ps1 -Instance examples/upgrade_cases/outdated_instance -Master examples/upgrade_cases/master
  - runtime suite batch complete
  - python scripts/validate_collaboration_state.py --root .
  - powershell -NoProfile -File scripts/validate_collaboration_state.ps1 -Root .
  - python scripts/scan_encoding.py --root .
  - powershell -NoProfile -File scripts/scan_encoding.ps1 -Root .
  - python scripts/scan_domain_neutrality.py --root .
  - powershell -NoProfile -File scripts/scan_domain_neutrality.ps1 -Root .
  - python scripts/prune_state.py --root . --apply
  - python scripts/prune_state.py --root . --check
---

# TASK-0061 Handoff

## Resultado

Implementado D2.2 del track de distribucion:

- `protocol.config.json` agrega `runtime_version: 0.10.0`.
- `protocol.config.template.json` agrega `runtime_version: {{PROTOCOL_VERSION}}`.
- `scripts/upgrade_instance.py` agrega `runtime/**` y `.github/workflows/validate.yml` al conjunto adoptable por defecto.
- El upgrade propone rutas runtime/CI solo cuando la instancia tiene `adoption_tier: runtime`; `coordination` o ausencia de tier conserva el comportamiento sin runtime.
- Se excluyen siempre `runtime/state/`, `runtime/runs/` y cualquier `__pycache__/`.
- El reporte markdown muestra `adoption_tier` y `runtime_version` master/instancia solo para instancias runtime.
- `scripts/upgrade_instance.ps1` mantiene paridad con Python.
- `examples/runtime_upgrade_cases/` cubre runtime-tier, coordination-tier, exclusiones de artifacts, inform-only y paridad py/ps.
- CI ejecuta `examples/runtime_upgrade_cases/run_runtime_upgrade_cases.py`.

## Validacion ejecutada

- Golden nuevo: `OK: 4 runtime upgrade golden cases passed.`
- Instanciacion runtime: `OK: runtime instantiation cases passed (5 + ps1 parity when available).`
- Upgrade antiguo py/ps sobre `examples/upgrade_cases`: comportamiento preservado.
- Suite runtime completa ejecutada: router, N-agent, property, concurrency, guardrail, tool-policy, eventlog, event-auth, instantiation, upgrade, eventlog-gate, Review/QA, registry, turn schema/semantic, apply, loop, observability M2, budget, observability N-agent, LLM adapter: verde.
- Validador py/ps: verde antes del release; revalidado tras poda final.
- Encoding py/ps: verde.
- Neutralidad py/ps: verde.
- Prune final aplicado: `claims_archived=2`, `mailbox_archived=1`, `after_tokens=14336`.

## Notas de revision

- La herramienta sigue siendo inform-only: no muta la instancia.
- `runtime_version` queda desacoplado pero inicializado con la version del protocolo en templates nuevos.
- Para masters con `upgrade.adoptable_globs` custom, se respeta el override existente; la tier-awareness filtra los paths runtime/CI si aparecen.
- La anomalia de TASK-0060 fue reconciliada materialmente por Claude; queda el mensaje de anomalia abierto hasta que Claude lo archive/responda.
