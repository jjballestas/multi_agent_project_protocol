---
handoff_id: HANDOFF-TASK-0057-codex-to-claude-1
task_id: TASK-0057
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-07
context_refs:
  - Area_comun/tasks/TASK-0057-codex-envelope-signing.md
  - Area_comun/specs/SPEC-0043-fase5.3-envelope-signing.md
  - protocol.config.json
  - protocol.config.template.json
  - runtime/eventlog.py
  - examples/runtime_event_auth_cases/run_runtime_event_auth_cases.py
  - .github/workflows/validate.yml
---

# Handoff TASK-0057 - Event envelope authentication

## Entrega

- `protocol.config.json` y `protocol.config.template.json` agregan `event_auth` con `enabled: false`, metodo HMAC e issuer/audience placeholder, sin claves.
- `runtime/eventlog.py`:
  - firma eventos con HMAC determinista cuando `event_auth.enabled=true`;
  - resuelve claves por agente desde `event_auth.keys` o `agent_registry.agents[].auth`;
  - conserva comportamiento legacy cuando `event_auth` falta o esta off;
  - verifica eventos durante replay/snapshot;
  - ignora eventos sin firma valida y registra `security.unauthenticated_event` en `state.rejections`;
  - preserva `replay_without_side_effects`.
- Nuevo golden `examples/runtime_event_auth_cases/run_runtime_event_auth_cases.py` con 5 casos.
- CI actualizado con `Run runtime event auth cases`.

## Validacion ejecutada

- `python examples/runtime_event_auth_cases/run_runtime_event_auth_cases.py` -> 5/5.
- `python examples/runtime_eventlog_cases/run_runtime_eventlog_cases.py` -> 5/5.
- `python examples/runtime_eventlog_gate_cases/run_runtime_eventlog_gate_cases.py` -> 5/5.
- Bloque runtime completo ejecutado: router, N-agent, property, concurrency, guardrail, tool-policy, eventlog, event-auth, eventlog-gate, Review/QA, registry, turn schema/semantic, apply, loop, observability, llm adapter y prune.
- `python scripts/validate_collaboration_state.py --root .` verde con warnings FYI no bloqueantes.
- `./scripts/validate_collaboration_state.ps1 -Root .` verde con los mismos warnings.
- `python scripts/scan_encoding.py --root .` verde.
- `./scripts/scan_encoding.ps1 -Root .` verde.
- `python scripts/scan_domain_neutrality.py --root .` verde.
- `./scripts/scan_domain_neutrality.ps1 -Root .` verde.
- `python scripts/prune_state.py --root . --check` verde.
- `./scripts/prune_state.ps1 -Root . -Check` verde.
- Tras liberar el claim, `python scripts/prune_state.py --root . --apply` archivo 1 claim; `--check` final queda verde.

## Limites respetados

- Aditivo y config-gated: con `event_auth` ausente u off no se escribe `event_auth` en los eventos.
- Sin secretos reales en live/template; la clave de prueba vive solo en el golden.
- Issuer/audience quedan como estructura, sin flujo OAuth/JWT externo.
- Sin red, sin reloj en tests de determinismo, domain-neutral.
- No toque Fase B ni Fase 6/7.
- Release atomico aplicado: `TASK-0057` pasa a `in_review`, el claim de Codex queda liberado y la poda de mantenimiento queda al dia.
