# SCHEMA_VERSIONING.md - Runtime Turn Schema SemVer

Source of truth: `runtime/turn_schema.json`.

The runtime turn schema is the contract for a single agent turn report. Its explicit
`schema_version` field is the SemVer version of that contract, independent from the repository
release version.

Current version: `1.1.0`.

## Consumers

The policy is based on the real consumers of the schema:

- `runtime/turn_validate.py` loads `runtime/turn_schema.json`, validates report shape and then checks
  semantic rules against project state.
- `runtime/apply.py` consumes validated transitions and applies task, claim, mailbox and handoff state
  changes.
- Runtime adapters produce turn reports that must satisfy the schema before any state mutation.
- Golden cases in `examples/runtime_turn_cases/` and higher-level runtime suites protect compatibility.

## Version Policy

Use `PATCH` when the change does not alter the report contract:

- descriptions, examples, comments or metadata only;
- typo fixes in non-normative text;
- validation or documentation fixes that do not change accepted or rejected report payloads.

Use `MINOR` when the schema accepts additional compatible payloads and existing valid reports remain valid:

- new optional top-level fields;
- new optional nested fields;
- new optional transition payload sections;
- relaxing a constraint in a way that the runtime consumers already handle;
- adding enum values only when `turn_validate.py`, `apply.py` and adapters can process or safely ignore
  them without changing existing producer behavior.

Use `MAJOR` when existing valid reports may become invalid, or when existing consumers must change behavior:

- removing or renaming a field;
- making an optional field required;
- tightening an enum, pattern, minimum, maximum or `additionalProperties` boundary;
- changing the meaning of a field, transition, idempotency key, fencing token or outcome;
- changing state-transition semantics in a way that affects `turn_validate.py`, `apply.py` or adapters.

## Capa A Justification

The N-agent Fases 1-4 changes to the turn schema are `MINOR`:

- `agent` moved from a fixed role enum to an open string validated semantically against `agent_registry`.
  This accepts additional registered agents while preserving existing `Claude`, `Codex` and human-owner
  reports.
- `attempt_id`, `idempotency_key`, `aggregate_version` and `fencing_token` are optional top-level fields
  for idempotency and concurrency. Existing reports remain valid when those fields are absent.
- `transitions.review_qa` is an optional nested payload. Reports without Review/QA transitions remain valid.
- Review/QA states and events were added so the runtime can model review failures, QA failures and
  architect review. Existing lifecycle reports remain valid.

Because these changes extend accepted payloads and preserve existing producers, the current schema is
declared as `1.1.0` rather than a new major version.
