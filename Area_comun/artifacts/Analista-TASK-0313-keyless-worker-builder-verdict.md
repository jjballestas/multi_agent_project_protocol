---
artifact: Analista-TASK-0313-keyless-worker-builder-verdict
task_id: TASK-0313
reviewer: Analista
role: adversarial-checker
verdict: OK-CLOSABLE
iteration: r1-FINAL
created: 2026-08-02T18:30:00Z
local_time: 2026-08-02 20:30 CEST (UTC+2)
spec: SPEC-0115
decision: DECISION-0109
---

# Analista verdict -- TASK-0313: keyless product-worker builder (front Zeus-protocol, P4a / Nivel 1)

## Verdict: OK-CLOSABLE

The product-worker builder is off-by-default (403 inert), composes the roster entry SERVER-SIDE
from a strict allow-list (client cannot inject raw entry / actor / signature / ledger capability),
persists a KEYLESS entry (ledger denied, no ledger capabilities, not a governance agent, not
enabled), keeps the Nivel 2 boundary (a governance-signer request records only a `pending` marker;
no signer is registered, no agent_registry write), and leaves the hub #4 (config / events /
snapshot) byte-identical. Independent clean-clone gate green and an independent behavioral harness
(59/59) found NO escape. Three non-blocking residuals declared below.

## Canonical anchor (never a hot working tree)

- Product repo: D:/Agentes/Zeus/Zeus-protocol -- commit `8ba0155` (== origin/main HEAD; cited by handoff).
- Hub HEAD (protocol): `35cf295`.
- Review executed in a CLEAN CLONE checked out at `8ba0155` (D:/Aegis_Scratch/z0313), gated by
  EXIT CODE, not in-place.
- Commit `8ba0155` touches ONLY product routes: public/app.js, public/index.html, public/styles.css,
  src/server.js (+113/-1), tests/staticContract.test.js. It does not touch the hub, the #4 chain,
  protocol.config.json, agent_registry, or genesis.

## Reproduction (exit codes)

Product gate (clean clone @8ba0155):
- `npm install` -> up to date; `npm test` -> tests 144 / pass 124 / fail 0 / skipped 20 (slow tier).
  EXIT 0. Matches maker report (144/124/20/0).

Protocol gates (hub @35cf295):
- `python scripts/validate_collaboration_state.py` -> OK (1 benign WARNING: this REVIEW msg has no
  context_refs). EXIT 0.
- `python runtime/protocol_replay.py --check-drift` -> PROTOCOL_STATE_DRIFT verdict=CLEAN
  up_to_seq=7013. EXIT 0.
- `python runtime/gate.py` (enforce hard-gate) -> EXIT 0.
- `python scripts/scan_encoding.py` -> clean. EXIT 0.
- `python scripts/scan_domain_neutrality.py` -> EXIT 0.

Independent adversarial harness (my own payloads, not the maker's tests): spun the server as a
subprocess against a temp roster, exercised the WHOLE family per criterion (not the single given
example), fingerprinted the hub before/after. Result: 59/59 PASS, 0 FAIL.

## Vector-by-vector (PASS / SLIPS)

| AC | Criterion | How I tried to break it | Result |
|----|-----------|-------------------------|--------|
| AC6 | off-by-default 403 | env unset AND "0" AND "true" AND "1x" AND "" -> POST builder / GET / POST register | PASS: all 403 inert (only exact "1" enables); capabilities.productWorkerBuilder.enabled reflects flag |
| AC1 | form + confirm | execute upsert with NO confirm; with WRONG confirm; dry_run persist check | PASS: 409 both; dry_run returns 200 and does NOT write roster |
| AC2 | server-side compose + anti-injection | top-level `actor`/`signature`/`rawEntry`/foreign key; inner `ledgerCapabilities`/`governanceAgent`/`signing`/`enabled`/`publicKeyPem`/`role`/`defaultEndpoint`; `__proto__` pollution | PASS: all 400, none persisted; server hard-codes signing.ledger=denied, ledgerCapabilities=[], governanceAgent=false; GET (publicProductWorker) does NOT leak publicKeyPem |
| AC3 | keyless (DECISION-0069 / guard TASK-0213) | inspect persisted entry + dry_run authority + submit_intent surface | PASS: persisted ledgerCapabilities=[], governanceAgent=false, signing.ledger=denied, enabled=false; response authority={ledgerSigning:false,ledgerWrites:false,governanceRegistration:false}, submitIntentEmitted=false, protocolLedgerTouched=false. Path never calls submit_intent |
| AC4 | LLM link (provider/endpoint/model in roster outside pinned config) | create -> edit model -> remove | PASS: entry stores provider/defaultEndpoint/defaultModel/capabilities in extractors.runtime.json (outside protocol.config.json); edit updates model keeping enabled=false; remove empties roster; remove of unknown id -> 404 |
| AC5 | Nivel 2 boundary (no governance signer via form) | `governanceRequested:true` on create | PASS: only records governanceCeremony="pending"; persisted governanceAgent stays false; no agent_registry / signer set write |
| AC6 | fondo intocable (#4 drift 0) | sha256 hub config/events/snapshot before/after full run | PASS: protocol.config.json (2E35F26E...), events.jsonl, snapshot.json byte-identical; drift verdict=CLEAN |

Additional negatives probed (all PASS): bad `operation` (delete) -> 400; bad `mode` (commit) -> 400;
traversal id `../../etc` on remove -> 400; traversal id `../evil` on upsert -> 400.

No SLIPS. No new escape found.

## Residuals (non-blocking; declared, not gating)

1. **Endpoint validation asymmetry (informational).** The builder's
   `sanitizeProductWorkerBuilderFields` accepts any HTTP(S) URL (no credentials) as the worker
   endpoint, whereas the pre-existing `register` path forces `provider === "local-vlm"` +
   loopback-only. In the builder this is inert stored roster data: the entry is keyless,
   `enabled:false`, and this path never EXECUTES the worker (execution is explicitly out of scope).
   Recommendation for a future runtime task: the EXECUTION boundary (when/if a roster worker is
   actually run) must re-validate endpoint against a loopback/allow-list, so an external endpoint in
   the roster never becomes an SSRF surface at run time. Not a TASK-0313 defect.

2. **Builder cannot make a worker live (stronger than required).** A net-new worker created via
   the builder is always `enabled:false` and carries no keypair (`publicKeyPem` stays undefined on
   the mutate path; keypair generation lives only in the separate `register` path). This is a
   stronger keyless posture than the ACs demand and confirms the builder confers neither liveness
   nor signing authority. Noted for traceability.

3. **`governanceRequested` marker is display-only.** The `pending` ceremony marker is inert data;
   nothing in this code acts on it. Correct per DECISION-0109 (Nivel 2 = re-genesis ceremony,
   runbook P4b, not a front toggle). If a later phase wires the ceremony intake, the checker must
   re-confirm the flip stays out-of-band.

## Closure recommendation

**OK-CLOSABLE.** AC1-AC6 verified independently by behavior in a clean clone; keyless + server-side
compose + Nivel 2 boundary hold; hub #4 byte-identical and drift CLEAN; all protocol gates green.
No change required.

-- Analista (adversarial checker)
