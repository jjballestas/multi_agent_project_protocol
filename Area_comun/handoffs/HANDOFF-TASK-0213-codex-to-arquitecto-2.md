---
task_id: TASK-0213
from: Codex
to: Arquitecto
date: 2026-06-29
status: in_review
type: handoff
claim: CLAIM-20260629-Codex-TASK-0213-review-fix
---

# HANDOFF TASK-0213 review fix

## Scope
- Fixed V1 by constraining `scripts/keygen_agent.py --secret-dir` to resolve under `<root>/protocol-secrets/`.
- Fixed V2 with a write-time guard in `runtime/submit_intent.py` for attested instances: when actor auth is enforced, only `tier=signer` actors may bind signing material; signer key ids must match the generated actor-owned convention.
- Added permanent regressions in `scripts/test_attested_instancing.py`:
  - external `--secret-dir` exits non-zero and writes nothing outside `protocol-secrets`;
  - worker mapped to signer key/HMAC exits non-zero and leaves `runtime/state/events.jsonl` byte-identical.

## Guardrail
Touched files:
- `scripts/keygen_agent.py`
- `runtime/submit_intent.py`
- `scripts/test_attested_instancing.py`

Pinned files left byte-identical:
- `runtime/eventlog.py`: `59A8AE8764AC327598BA2DA4759E7CBC75EA46B0CDE214A636518A3A9A70DEDD`
- `scripts/validate_collaboration_state.py`: `EB04799F266DEBAFB13A61F7F5E673F5D831683B18532BB8807F12DAFD65C5AB`
- `protocol.config.json`: `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`
- `event-state.runtime.json`: `B9706842F32E30B4A3054C65BF5F26A7A327567BDDB885438ED7FEDFA05111CF`
- `personal/operador/TFM/PRE-REGISTRO-H1-H3-v2.md`: `E8277CC7D52F015C6F9396F3D4261CB8C3F0F7A331B3E865CD76F418028A5E6D`

## Evidence
- `python -m py_compile scripts\keygen_agent.py runtime\submit_intent.py scripts\test_attested_instancing.py` PASS.
- `python scripts\test_attested_instancing.py --work C:\t\att0213-reviewfix` PASS.
- `python scripts\scan_encoding.py --root .` PASS.
- `python scripts\scan_domain_neutrality.py --root .` PASS.
- `python scripts\validate_collaboration_state.py --root .` PASS with pre-existing mailbox warnings only.
- `git diff --check -- scripts/keygen_agent.py runtime/submit_intent.py scripts/test_attested_instancing.py` PASS.

## Review notes
- The binding guard is intentionally write-time only and does not touch `runtime/eventlog.py` or the validator.
- `event_state.enforce` still ships OFF by default in generated attested instances; the new guard applies when actor auth enforcement is later enabled.
