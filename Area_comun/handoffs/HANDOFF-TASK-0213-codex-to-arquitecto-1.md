---
id: HANDOFF-TASK-0213-codex-to-arquitecto-1
task: TASK-0213
from: Codex
to: Arquitecto
date: 2026-06-29
status: in_review
---

# HANDOFF TASK-0213 - attested instancing ceremony

## Delivered
- Added `scripts/keygen_agent.py`: per-signer Ed25519 private PEM + HMAC secret under instance-local
  `protocol-secrets/`, portable public metadata JSON, idempotent no-overwrite default, no secret stdout.
- Extended `scripts/new_instance.py` with `--tier attested` and `--roster` JSON:
  - copies runtime + scripts;
  - creates signer keys and runtime override references;
  - registers signer/worker roster with `llm_preset`;
  - keeps workers keyless;
  - writes signer public keys to instance `event_state.signature_config.public_keys`;
  - writes provenance convention under `attested_instancing.provenance_metadata`;
  - creates `personal/<id>/` for every roster agent;
  - signs the genesis boundary, then leaves `event_state.enforce=false` and `actor_auth_enforce=false`.
- Added `scripts/test_attested_instancing.py` golden coverage for keygen, ceremony, clone-without-secrets
  verification, and keyless-worker negative write.

Implementation note: the CLI tier is `attested`, but generated `protocol.config.json` keeps
`adoption_tier: "runtime"` plus `attested_instancing.enabled: true` so existing validator accepts the instance
without touching the pinned validator during the measurement guardrail.

## Evidence
- `python -m py_compile scripts\keygen_agent.py scripts\new_instance.py scripts\test_attested_instancing.py` OK.
- `python scripts\test_attested_instancing.py --work C:\t\att0213-golden` OK.
- Disposable instance: `python scripts\new_instance.py --source-template . --target C:\t\att0213 ... --tier attested --roster C:\t\att0213-roster.json` OK.
- Generated instance validate: `python scripts\validate_collaboration_state.py --root C:\t\att0213` OK.
- Third-party clone without secrets: `python scripts\validate_collaboration_state.py --root C:\t\att0213clone` OK.
- Worker keyless negative: `submit_intent.py --actor-id Peon` with `actor_auth_enforce=true` failed before ledger write: `actor_auth private key path outside allowed roots`.
- `python scripts\scan_encoding.py --root .` OK.
- `python scripts\scan_domain_neutrality.py --root .` OK.
- `python scripts\validate_collaboration_state.py --root .` OK with pre-existing warnings:
  - compact mailbox context_refs warning for `MSG-20260627-Codex-to-Arquitecto-TASK-0193-in-review.md`;
  - non-response archive suggestion for `MSG-20260628-Arquitecto-to-Codex-ANOMALY-delivery-format.md`.
- Drift: `has_drift=false`, `up_to_seq=2502`, hot/replay hash
  `4a22252ba5468fa85e579a19b8a751380b174817554726b26d92ec890a2e3610`.
- `git diff --check` OK; only known CRLF warning for `runtime/state/snapshot.json`.

## Pinned Hub Hashes
Before and after implementation are identical:
- `runtime/eventlog.py`:
  `59A8AE8764AC327598BA2DA4759E7CBC75EA46B0CDE214A636518A3A9A70DEDD`
- `scripts/validate_collaboration_state.py`:
  `EB04799F266DEBAFB13A61F7F5E673F5D831683B18532BB8807F12DAFD65C5AB`
- `protocol.config.json`:
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`
- `event-state.runtime.json`:
  `B9706842F32E30B4A3054C65BF5F26A7A327567BDDB885438ED7FEDFA05111CF`

Pre-registro v2.0 path was not present as a concrete file in this checkout; no pre-registro file was modified.

## Review Focus
- Confirm that preserving generated `adoption_tier: "runtime"` while exposing the `attested` ceremony satisfies
  DECISION-0069 under the no-pinned-validator-edit guardrail.
- Re-run the golden on a clean short path and inspect that `protocol-secrets/` is absent from the clone.
