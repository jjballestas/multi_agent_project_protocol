---
handoff_id: HANDOFF-TASK-0099-codex-to-claude-1
task_id: TASK-0099
spec_id: Area_comun/specs/SPEC-0073-backend-firma-externo-configurable.md
from: Codex
to: Claude
date: 2026-06-10
status: for_review
requires_response: no
response_owner: none
acceptance_criteria_verified: yes
tests_run:
  - python -m py_compile scripts\sign_release.py scripts\verify_release.py examples\release_sign_cases\run_release_sign_cases.py
  - python examples\release_sign_cases\run_release_sign_cases.py
  - python examples\release_verify_cases\run_release_verify_cases.py
  - python scripts\validate_collaboration_state.py --root .
  - powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .
  - python scripts\scan_encoding.py --root .
  - powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_encoding.ps1 -Root .
  - python scripts\scan_domain_neutrality.py --root .
  - powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_domain_neutrality.ps1 -Root .
  - python scripts\prune_state.py --root . --check
  - protocol_state_drift(Path('.'))
spec_deviations:
  - none
decisions_referenced:
  - DECISION-0023
  - DECISION-0021
  - DECISION-0001
  - DECISION-0006
---

# Handoff: TASK-0099 external-command release signing backend

## 1. Minimal Context

SPEC-0073 asked for a real, configurable, vendor-neutral release signing path while preserving the
deterministic fixture backend. The implementation keeps `fixture-hmac-sha256` byte-equivalent and adds
`external-command` as an opt-in backend configured only by CLI flags.

Operational note: after the first implementation handoff, one transient `prune --check` run reported
`released_ratio 90.91 >= 90`. Codex briefly recorded a blocker instead of running `protocol_prune`; after the
blocked-claim audit state, the final prune check returned green (`cold_start_tokens=16652`). The blocker message
was withdrawn and TASK-0099 returned to review.

## 2. What Was Done

- `scripts/sign_release.py`
  - Added `external-command`.
  - Added `--sign-command`, `--identity`, `--issuer`, and `--signature-field signature|bundle`.
  - Supports `{digest}` and `{manifest}` placeholders; if no placeholder is used, the digest is sent on stdin.
  - Does not persist command text or signing material in the signature payload.
- `scripts/verify_release.py`
  - Added `--verify-command` for `external-command`.
  - Verifies `subject_digest == manifest.sbom_hash` before backend execution.
  - Rejects backend mismatch before backend execution.
  - Supports `{digest}`, `{manifest}`, `{signature}`, `{bundle}`, `{signature_file}`, `{identity}`, `{issuer}`,
    and `{key_id}` placeholders; if no placeholder is used, signature JSON is sent on stdin.
- `scripts/sign_release.ps1` and `scripts/verify_release.ps1`
  - Delegate the new flags to Python while preserving fixture behavior.
- `examples/release_sign_cases/run_release_sign_cases.py`
  - Uses repo-local inherited-ACL temp dirs for sandbox compatibility.
  - Adds deterministic fake/recorded external backend cases.
  - Now covers 13 cases: existing fixture cases plus external round-trip, backend mismatch, subject mismatch,
    missing verify command, and PowerShell parity when available.
- `README_INSTANCIACION.md`
  - Documents the external signing/verifying recipe and the release-report fields to publish.

## 3. What Was Not Done

- No real provider command is hardcoded.
- No keys, identities, bundles, or real signatures were committed.
- No runtime flip, SA.4 re-arm, or pilot was run.
- No release was signed; this only enables the mechanism.

## 4. Acceptance Criteria Verified

| Criterion | Evidence | Status |
|-----------|----------|--------|
| Fixture HMAC unchanged | `case_signature_expected_payload` compares exact canonical JSON; release signing suite passed | met |
| External-command backend works | `case_external_command_round_trip_ok` signs and verifies with fake/recorded backend | met |
| subject_digest binding | `case_external_command_fails_for_subject_mismatch` rejects mismatched digest | met |
| Backend mismatch rejects | `case_external_command_fails_for_backend_mismatch` rejects requested backend mismatch | met |
| Off-by-default integrity-only verify | `case_verify_without_signature_keeps_integrity_contract` remains green | met |
| Fails closed without material/command | Fixture no-material case and external missing-verify-command case both reject | met |
| Parity .py/.ps1 | Release signing suite includes wrapper parity when PowerShell is available | met |
| No secrets / neutral | encoding + neutrality scans passed; no real material added | met |
| Prune gate | Final `python scripts\prune_state.py --root . --check` -> OK, prune not due (`cold_start_tokens=16652`) | met |

## 5. Tests Run

- `python -m py_compile scripts\sign_release.py scripts\verify_release.py examples\release_sign_cases\run_release_sign_cases.py`
  - OK.
- `python examples\release_sign_cases\run_release_sign_cases.py`
  - OK: 13 release signature golden cases passed.
- `python examples\release_verify_cases\run_release_verify_cases.py`
  - OK: 6 release verify golden cases passed. This suite was rerun outside the sandbox because the first run hit
    the known Windows sandbox `%TEMP%` ACL issue before test assertions.
- `python scripts\validate_collaboration_state.py --root .`
  - OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .`
  - OK.
- `python scripts\scan_encoding.py --root .`
  - OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_encoding.ps1 -Root .`
  - OK.
- `python scripts\scan_domain_neutrality.py --root .`
  - OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_domain_neutrality.ps1 -Root .`
  - OK.
- `python scripts\prune_state.py --root . --check`
  - OK: prune not due, `cold_start_tokens=16652`.
- `protocol_state_drift(Path('.'))`
  - OK: `has_drift=false`, `up_to_seq=275`.

## 6. Spec Deviations

none

Implementation choices for SPEC-0073 questions:

- Q1: chose explicit CLI flags, not persisted presets.
- Q2: chose placeholders first (`{digest}`, `{manifest}`, etc.) with stdin fallback. This keeps commands
  neutral and lets an emitter wrap any provider-specific CLI without core code knowing the provider.

## 7. Requested Action

Claude: ratify adversarially for vendor-neutrality, no secrets, deterministic fixture preservation, and
`subject_digest == manifest.sbom_hash` binding; then close TASK-0099 to `done` if accepted.

## 8. Risks and Assumptions

- External real-provider commands are intentionally not exercised in CI; only fake/recorded deterministic
  backend is in golden.
- If a provider needs a bundle file rather than bundle content, the emitter should provide a local wrapper
  command and publish that exact verification command in the release report.

## 9. Open Questions / BLOCKED

none

## 10. Pointers

- Task: `Area_comun/tasks/TASK-0099-codex-backend-firma-externo-configurable.md`
- Spec: `Area_comun/specs/SPEC-0073-backend-firma-externo-configurable.md`
- Decision: `Area_comun/decisions/DECISION-0023-firma-release.md`
- Deliverables:
  - `scripts/sign_release.py`
  - `scripts/verify_release.py`
  - `scripts/sign_release.ps1`
  - `scripts/verify_release.ps1`
  - `examples/release_sign_cases/run_release_sign_cases.py`
  - `README_INSTANCIACION.md`
