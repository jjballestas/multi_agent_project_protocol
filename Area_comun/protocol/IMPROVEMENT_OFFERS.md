# Improvement offers

`runtime/improvement_offers.py` closes the DECISION-0103 learning loop for runtime
turn reports and mailbox `REPORTE` messages. It produces a human-facing offer; it does
not create or edit a skill, rule, decision, task, or protocol file.

## Deterministic candidate rule

Each obstacle root cause is normalized with Unicode NFKC, Unicode case-folding,
leading/trailing whitespace removal, and internal whitespace collapse. Two obstacles
have the same root cause only when those normalized keys are byte-for-byte equal.
There is no similarity model or fuzzy matching. A candidate exists when any obstacle
has `recurrence_risk: high`, or one normalized key occurs in at least two distinct
delivery ids.

The generated offer contains concrete proposed rule text, a regression requirement,
and citations in `source#delivery:evidence` form. Runtime JSON/JSONL and mailbox
`REPORTE` files are explicit inputs, so both carriers use the same evaluator.

## Durable registry and response flow

The canonical registry is `Area_comun/protocol/improvement_offer_registry.json`.
Each proposal id is a stable hash of its normalized root-cause key. Generate with
`--record-offers` to persist an offered row. Record a human response with `--respond
accepted|rejected|parked --proposal-id ID --response-ref REF`.

Accepted proposals are never offered again. Rejected or parked proposals are not
re-offered unless their evidence set changed and the caller explicitly declares that
proposal id with `--new-evidence`. An unchanged offered proposal is also suppressed.
All registry writes remain normal claimed, reviewed repository changes.

## No auto-application invariant

The module reads delivery evidence and writes only its explicit registry path. Its
output states the only application path: human acceptance, then a recorded DECISION,
then a governed implementation task. It exposes no skill/protocol mutation, task
creation, decision creation, or `submit_intent` integration.
