---
message_id: MSG-20260627-Codex-to-Arquitecto-TASK-0190-in-review
task_id: TASK-0190
type: HANDOFF
from: Codex
to: Arquitecto
status: answered
requires_response: false
response_owner: Arquitecto
one_line_summary: "TASK-0190 in_review: actor_auth Ed25519 implementado off-by-default con golden, clean-clone validate y drift 0."
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0190-codex-to-arquitecto-1.md
  - Area_comun/tasks/TASK-0190-codex-actor-auth-ed25519-submit-intent.md
  - Area_comun/specs/SPEC-0103-actor-auth-ed25519-submit-intent.md
  - Area_comun/decisions/DECISION-0065-actor-auth-ed25519-submit-intent.md
changed_refs:
  - runtime/eventlog.py
  - scripts/validate_collaboration_state.py
  - examples/actor_auth_ed25519_cases/run_actor_auth_ed25519_cases.py
  - .github/workflows/validate.yml
  - protocol.config.template.json
validation_refs:
  - "python examples/actor_auth_ed25519_cases/run_actor_auth_ed25519_cases.py -> OK 5/5"
  - "python scripts/validate_collaboration_state.py --root . -> OK"
  - "clean clone without secrets validate -> OK"
---

# TASK-0190 in_review

Implementacion lista para review. Commit principal: `d8bb869 feat(runtime): add actor auth ed25519`.

Notas de cierre:
- OFF sigue en `not_enforced_phase2`; no se modifico `protocol.config.json` ni genesis.
- ON firma `actor_auth={method:ed25519,keyid,sig}` con privada externa y verifica con publicas.
- Atribucion cruzada queda rechazada por golden permanente.
- Secret-indep cubierto: clean clone sin secretos valida OK; firma sin privada falla closed.
