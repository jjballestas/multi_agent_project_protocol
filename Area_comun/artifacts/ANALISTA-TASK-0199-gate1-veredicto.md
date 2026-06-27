# ANALISTA TASK-0199 GATE 1 VEREDICT

Firma: Analista

Verdict: CAMBIO-REQUERIDO. GATE 1 is not closable.

Canonical anchors:
- Protocol instruction HEAD: 1fbb7ba8749476bdc4277cd2146a464e9a36d214.
- Product repo: D:/Agentes/Zeus/Zeus-Aegis.
- Product commit under review: 9c5f0ae0ecb82e3c5bdce2eca43cbeb58e0ae1f6.
- Clean product clone: C:/Users/johnb/AppData/Local/Temp/zeus-aegis-review-1e5185d14cc64c0abad926e706e45c9a.

## Reproduction

| Check | Command / payload | Exit | Result |
|---|---:|---:|---|
| Product clean clone | git clone D:/Agentes/Zeus/Zeus-Aegis TMP; git checkout 9c5f0ae; npm test | 1 | FAIL. First full run failed on governance-readonly timeout. Second full run failed with 4 failures: governance-readonly timeout, files timeout, mcp presets timeout, mcp presets seed assertion. |
| Targeted F1 suite | npm exec -- vitest run src/server/governance-readonly.test.ts --reporter=dot from vendor/hermes-2.3.0 | 0 | 5/5 passed when isolated. This does not satisfy the required full npm gate. |
| V1 route method scan | Select-String over src/routes/api/governance*.ts for GET/POST/PUT/PATCH/DELETE | 0 | Only GET handlers found in the 8 governance routes. |
| V1 write-surface scan | Select-String over governance server/routes/UI for write patterns | 0 | No POST/PUT/PATCH/DELETE handler found in governance routes. Matches to Area_comun/state and runtime/state/events.jsonl are read paths/constants, not writes. |
| V2 canonical read probe | Temp protocol clone, committed analista_probe=COMMITTED_CANON, dirty working tree analista_probe=DIRTY_WORKTREE, then getGovernanceState() | 0 | Returned COMMITTED_CANON. State/backlog read from git show at canonical ref, not dirty working tree. |
| V3 false-green probe | Temp protocol clone at 1fbb7ba with uncommitted invalid rr mailbox message; getGovernanceHealth() and getGovernanceLedger(3) | 0 | Health: validator red and drift green. Ledger: attestation verified on every event. This is a false green for ledger attestation while validate is red. |
| V4 PII artifact probe | Temp protocol clone with committed artifact named ANALISTA-TASK-9999-john.doe@example.com-veredicto.md and body with Juan Perez/email/phone/id | 0 | Email leaked in artifact id and path; name leaked in preview. Phone/id redaction was partial but present. |

## Vector table

| Vector | Verdict | Evidence | Required change |
|---|---|---|---|
| V1 read-only real | SOSTIENE | Governance route files expose GET only; no direct submit_intent/write handler in the F1 files reviewed. | Keep as is, but add regression that scans all /api/governance route modules from the vendor cwd. |
| V2 canonical reads | SOSTIENE | Dirty working tree mutation did not alter getGovernanceState(); result came from the committed ref. | Keep canonical ref behavior. |
| V3 health/attestation derived | REFUTADO | With validator red and drift green, getGovernanceLedger reported attestation=verified. The ledger chip can be green while the protocol validator is red. | Ledger attestation must include validator result and signature/auth validation, or render a distinct non-green state when validate is red. |
| V4 PII | REFUTADO | Artifact id/path leaked john.doe@example.com; preview leaked Juan Perez. The redactor covers body email/phone/id families partially but not display identifiers, paths, or names. | Redact all served display fields: id, path, title/subject, preview, payload strings, metadata. Add negative tests for filename/path PII and person-name PII. |
| V5 apparatus intact | SOSTIENE | Product diff for F1 lives in Zeus-Aegis. Protocol gates below keep #4 byte-identical. No evidence that F1 product code changed protocol core/baseline. | No blocking change from V5. |
| V6 F0 gate honest | REFUTADO | Required clean-clone npm test exits 1. Even after dependency install, rerun still exits 1. | Make full npm test exit 0 in a clean clone or record an explicit, narrow waiver that does not cover F1 failures. |

## Residuals

- I did not find a direct write route under /api/governance/*, but the product still carries many non-governance write routes inherited from Hermes. That is not a V1 F1 failure by itself.
- Isolated governance tests pass, so the full-suite failure is partly harness/flakiness/upstream state. It still blocks because the instruction gates by full npm test exit.
- The PII probe used a committed temp protocol artifact to exercise the exact canonical-read path. It is falsable: query getGovernanceArtifacts("john.doe") and inspect id/path/preview.

## Recommendation

CAMBIO-REQUERIDO. Do not close GATE 1 until V3, V4, and V6 are fixed or explicitly waived with a narrow written decision.
