# VERDICT - TASK-0264 (DECISION-0103 C1 written start-up rule): OK-CLOSABLE

Reviewer: Analista (independent adversarial checker). Signature: Analista.
Date: 2026-07-23. Scope: NO PRODUCT (protocol-only, hub).

## Canonical anchor

- Impl commit: `a079bca` ("docs(TASK-0264): publish governed plan approval rule").
- Protocol HEAD at review: `1b075a4`.
- Clean clone: `/d/ccv-0264`, checked out at `a079bca`, gates run THERE by exit code
  (not in a hot working tree).
- Doc drift a079bca..HEAD for the two published docs: EMPTY (`git diff a079bca..HEAD --
  Area_comun/protocol/TASK_PROTOCOL.md AGENTS.template.md` returned no output), so the text
  reviewed at a079bca is byte-identical to the text now in canonical state.

## Reproduction (clean clone a079bca, by exit code)

| Gate | Command | Exit |
|---|---|---|
| Collaboration state | `python scripts/validate_collaboration_state.py` | 0 (OK; one benign WARNING: FYI does not require response, consider archiving) |
| Encoding scan | `python scripts/scan_encoding.py` | 0 |
| Domain-neutrality scan | `python scripts/scan_domain_neutrality.py` | 0 |

Drift: canonical state valid at HEAD; snapshot canonical_hash consistent; no manual-edit drift.

## What was published (the WRITTEN rule, not the enforcement)

- `Area_comun/protocol/TASK_PROTOCOL.md`: new section "## Governed Plan Approval Before
  Execution (DECISION-0103 C1)" (file lines 38-65).
- `AGENTS.template.md`: mirror "#### Governed plan approval before execution (DECISION-0103 C1)"
  placed under "## 6. Task Lifecycle" / "### 6.1 Intake gate" (born-operational lifecycle), so
  new instances are born carrying it.
- `Area_comun/mailbox/open/MSG-20260723-Codex-to-Asesor-FYI-TASK-0264-regla-C1-publicada.md`:
  FYI to Asesor announcing the publication.

## Vector-by-vector (tested by content against DECISION-0103 C1, not by test name)

| # | Vector | Verdict | Evidence |
|---|---|---|---|
| 1 | Rule in TASK_PROTOCOL.md cites C1; 7-field plan table; recorded approval; re-approval on material change; E1 carve-out preserved | PASS | 7 fields present, exact names/order: `id, goal, acceptance, verification_cmd, required_capability, risk, estimate` (matches DECISION-0103 C1 line 63). "Approval must be durable and attributable ... signed event log or ... signed mailbox message. An ephemeral chat acknowledgement is not sufficient" (matches C1 recorded-approval). "Adding a unit or materially changing a unit's acceptance criteria or risk ... requires human re-approval" (all 3 material-change triggers: new unit / acceptance / risk). E1 carve-out present with the exact conditions: same acceptance, same scope, same risk, references parent unit. |
| 2 | Mirror in AGENTS.template.md (born-operational), no NORMATIVE content divergence | PASS | Same trigger, same 7-field table, same durable/attributable-approval + chat-not-sufficient, same re-approval on new-unit/acceptance/risk, same E1 carve-out conditions (same acceptance/scope/risk + parent ref). Placed in the lifecycle/intake section. See residual R-1 (cosmetic wording delta, non-normative). |
| 3 | Written rule, not enforcement: coherent with TASK-0260, does not duplicate it as code nor contradict it | PASS | Both texts end with an explicit disclaimer that mechanical turn-zero enforcement is a SEPARATE concern and "does not replace the recorded human approval". No gate logic embedded as code; no statement that contradicts the 0260 gate. The unit documents; 0260 enforces. |
| 4 | FYI to Asesor does not edit personal/asesor/ nor any foreign private area | PASS | Full commit a079bca touches only: AGENTS.template.md, the FYI mailbox message, TASK_PROTOCOL.md, governed state JSON, the two task .md files, runtime/state. ZERO edits under personal/. The FYI body itself states each participant updates only their own private startup prompt/memory. |
| 5 | ASCII purity + domain neutrality on everything published | PASS | scan_encoding exit 0; scan_domain_neutrality exit 0. Independent check: the newly-published C1 section (TASK_PROTOCOL.md lines 38-65), the AGENTS.template mirror, and the FYI are all pure ASCII (0 non-ASCII bytes in the mirror and FYI; the only 2 non-ASCII locations in TASK_PROTOCOL.md are at lines 110 and 285, both PRE-EXISTING and OUTSIDE the new section). No business/trading terms in the new content. |

No SLIPS found. I attempted to break each guarantee (searched for an invented requirement, a
dropped E1 condition, a divergent carve-out between the two texts, a private-area edit, and a
non-ASCII byte inside the new content). None held up as a defect.

## Declared residuals (NON-blocking; do not gate closure)

- R-1 (cosmetic, non-normative): TASK_PROTOCOL.md says "A checker-requested remediation ..."
  while AGENTS.template.md says "A remediation ...". DECISION-0103 E1 is specifically about a
  remediation born from a checker rejection, so TASK_PROTOCOL.md is marginally more precise.
  Both texts anchor to "DECISION-0103 E1 carve-out" and the OPERATIVE conditions (same
  acceptance/scope/risk + parent reference) are identical in both, so there is no divergence in
  the carve-out's effect - only the origin qualifier is dropped in the mirror. Optional polish,
  not a blocker.
- R-2 (context, not a requirement): neither text restates C1's explanatory note that this is a
  "turn-0 checkpoint, distinct from supervised_autonomy.human_checkpoint_every_k". That is
  contextual framing in the DECISION, not a normative requirement; the operative timing ("must
  not start the first execution turn before that approval is recorded") IS captured in both.
  Not an omission of a requirement.
- Benign validator WARNING: the FYI (requires_response:false) triggers "consider archiving".
  That is correct for an FYI and is the Arquitecto's to archive at closure; not a defect.

## Closure recommendation

OK-CLOSABLE (GO). The written rule is faithful to DECISION-0103 C1 (7 fields + recorded/
attributable approval + re-approval on material change + E1 carve-out preserved), mirrored in
AGENTS.template.md without normative divergence, coherent with (and not duplicating) the
TASK-0260 mechanical enforcement, and the FYI touches no foreign private area. All gates exit 0
in a clean clone at a079bca. Maker != checker preserved: implementation by Codex, review by
Analista.

-- Analista
