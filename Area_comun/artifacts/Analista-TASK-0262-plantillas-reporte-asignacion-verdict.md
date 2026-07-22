---
artifact_id: Analista-TASK-0262-plantillas-reporte-asignacion-verdict
author: Analista
role: adversarial-checker
task_id: TASK-0262
review_iteration: iter1
verdict: CHANGE-REQUIRED
date: 2026-07-23
---

# Analista verdict -- TASK-0262 (mailbox templates: delivery REPORTE + assignment report)

Local time: 2026-07-23 00:20 (UTC+2). Reviewer: Analista (independent adversarial voice).
Scope: SIN PRODUCTO -- protocol docs + validator only. Verdict gates closure.

## Canonical anchor

- Impl commit under review (doc): `5a7db87` ("docs(protocol): add mailbox report templates").
- Protocol HEAD at review time: `d927993` (canonical live state; validate green).
- Doc unchanged since impl: `git diff --stat 5a7db87 d927993 -- Area_comun/protocol/MAILBOX_REPORT_TEMPLATES.md` is EMPTY.
- Clean clone (never in-place): `D:/ccv0262` @ `d927993`.
- Cross-referenced against real schema/routing at HEAD: `runtime/turn_schema.json`,
  `runtime/router.py`, `scripts/validate_collaboration_state.py`.

## Reproduction (exit-code gated, clean clone)

Baseline gates in the clean clone (no test files added):

```
python scripts/validate_collaboration_state.py   -> OK, exit 0
python scripts/scan_encoding.py                  -> OK, exit 0
python scripts/scan_domain_neutrality.py         -> exit 0
```

Central cross-check (vector 2): extracted the THREE concrete examples verbatim from the
template (regex over the "### Complete ..." fenced markdown blocks -- no retyping) into real
`Area_comun/mailbox/open/MSG-*.md` files, then ran the validator:

```
extracted: MSG-...-REPORTE-assignment-UNIT-0042      (assignment, friction 0 + obstacles [])
extracted: MSG-...-REPORTE-delivery-TASK-0042        (delivery, friction 1 + 1 obstacle)
extracted: MSG-...-REPORTE-delivery-TASK-0043        (delivery, friction 0 + obstacles [])
python scripts/validate_collaboration_state.py       -> OK, exit 0  (only context_refs WARNINGS)
```

Negative controls (prove the governed path is genuinely exercised, not trivially skipped):

```
mutant A: delivery friction_count 1 + obstacles []   -> FAIL: "friction_count > 0 but obstacles is empty"
mutant B: obstacle recurrence_risk: catastrophic     -> FAIL: "recurrence_risk must be low, medium, or high"
mutant C: assignment friction_count 2 + obstacles [] -> FAIL: "friction_count > 0 but obstacles is empty"
python scripts/validate_collaboration_state.py       -> exit 1 (all 3 rejected)
```

Mutant C proves the assignment example itself flows through `validate_governed_mailbox_report`
(type REPORTE + TASK ref + report_schema_version 1.0) and passes only because it is well
formed. The template examples are consistent with the 0261 validator by behavior.

## Vector-by-vector

| # | Vector | Result | Evidence |
|---|--------|--------|----------|
| 1 | obstacles block IDENTICAL to TASK-0258 (4 fields + enum, zero variants) | PASS | Template fields `what, root_cause, resolution, recurrence_risk`, enum `low\|medium\|high`, "do not rename, add, or omit". `turn_schema.json` obstacle item: required `[what, root_cause, resolution, recurrence_risk]`, `additionalProperties:false`, `recurrence_risk` enum `[low, medium, high]`. Validator `OBSTACLE_FIELDS`/`OBSTACLE_RISKS` match. Three-way identical. |
| 2 | plantilla <-> validador (central): examples PASS validate_mailbox of 0261 | PASS | All 3 concrete examples -> validate exit 0 in clean clone; mutants A/B/C -> exit 1. Path exercised. |
| 3 | R1 closed by construction (temporal anchor mandatory + documented) | PASS | "Common rules" makes an anchor MANDATORY (`date`/`created_at`/`report_schema_version: "1.0"`), documents that no-anchor => historical, and every template/example hard-codes `report_schema_version: "1.0"` with "do not remove it". A user who follows the template cannot omit all three anchors. (Boundary: the no-anchor-means-skipped grandfathering is 0261 validator design, out of scope here.) |
| 4 | assignment fields exist in real routing (no invented runtime fields) | SLIP (1 pointer) | `required_capability`, `explanation.selected`, `explanation.candidate_agents`, `explanation.filtered`, `policy`, candidate `load_score`, candidate `stable_hash` -> ALL exist (`runtime/router.py:398-408, 411-419`). BUT the `candidates` block annotates `agent_id: <routing_decision.explanation.candidates item agent_id>` and the concrete example uses `agent_id:` -- the real candidate key is `agent` (`router.py:390`), NOT `agent_id`. No `agent_id` key exists in any routing candidate structure (exhaustive grep of runtime/scripts: the only `agent_id` dict keys are in eventlog/llm_turn_wrapper/protocol_replay/keygen, unrelated to routing candidates). |
| 5 | complete examples of all three (assignment, delivery w/ obstacles, delivery clean) | PASS | Three "### Complete ..." blocks present and complete; delivery-clean uses friction_count 0 + obstacles []. |
| 6 | neutrality + ASCII + valid frontmatter | PASS | scan_domain_neutrality exit 0; scan_encoding exit 0; frontmatter parses (examples validate green). |

## The slip (vector 4)

The assignment template's `candidates` provenance annotation:

```
candidates:
  - agent_id: <routing_decision.explanation.candidates item agent_id>
    load_score: <existing load_score>
    stable_hash: <existing stable_hash>
```

Every OTHER placeholder in the template names an EXACT existing key path
(`routing_decision.required_capability`, `routing_decision.explanation.selected`,
`routing_decision.explanation.candidate_agents item`, `routing_decision.policy`,
`routing_decision.explanation.filtered`). Within this same block `load_score` and
`stable_hash` are exact candidate keys -- but `agent_id` is NOT. The runtime candidate object
is emitted as `{"agent": agent_id, "metrics": ..., "score": ..., "load_score": ...,
"stable_hash": ...}` (`runtime/router.py:388-396`); the agent identifier lives under key
`agent`. The task acceptance criterion is explicit: "sin inventar campos nuevos del runtime",
and this REVIEW's vector 4 asked me to "confirma que los campos existen en el routing real".
The `candidates item agent_id` source pointer references a runtime key that does not exist.

Impact is documentation-only and LOW: the validator never inspects the `candidates` block, so
a copied assignment report does NOT redden the channel, and the rendered value is identical.
But this file is the "referencia canonica para humanos y agentes en sesion" (task goal), so an
inaccurate provenance pointer propagates to every future author. It contradicts an explicit
acceptance criterion, so it is not closable as-is.

## Declared residuals (benign, NOT blockers)

- R-a: The three examples emit `context_refs` WARNINGS (non-fatal) when placed as real
  compact mailbox messages. Warnings do not fail the validator; templates need not add them.
- R-b: The no-anchor-treated-as-historical grandfathering (validator skips governance when no
  anchor is present) is 0261 design and out of scope; 0262 closes R1 for template FOLLOWERS by
  making the anchor mandatory in the template, which is what this unit is responsible for.

## Closure recommendation: CHANGE-REQUIRED

Remediation (documentation-only, cheap):
- In `Area_comun/protocol/MAILBOX_REPORT_TEMPLATES.md`, assignment template + example, align
  the candidate agent-identifier provenance to the real routing key: the value comes from
  `routing_decision.explanation.candidates[].agent` (NOT `agent_id`). Either rename the pointer
  to `agent` or keep the report field name but annotate explicitly "rendered from candidate
  `agent`" so no reader infers a runtime `agent_id` key. The concrete MakerA/MakerB values and
  the prose paragraph on `explanation` do not change.

Fix loop:
- Affected gates (must stay exit 0): validate_collaboration_state.py, scan_encoding.py,
  scan_domain_neutrality.py. The 3 examples must still validate GREEN (no functional change).
- Re-judgment: Analista re-reviews the single edit before the closing commit.
- Max 2 iterations before escalating to the human owner.

Signed: Analista.
