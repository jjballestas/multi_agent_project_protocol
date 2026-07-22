---
artifact_id: Analista-TASK-0261-obstacles-indented-parser-verdict
author: Analista
role: adversarial-checker
task_id: TASK-0261
review_iteration: remediation-iter1
verdict: OK-CLOSABLE
date: 2026-07-22
---

# Analista verdict -- TASK-0261 remediation iter1 (indented obstacle parser)

Local time: 2026-07-22 23:43 (UTC+2). Reviewer: Analista (independent adversarial voice).
Scope: SIN PRODUCTO -- protocol validator only.

## Canonical anchor

- Impl commit under review: `f1d9c30` ("fix(TASK-0261): parse indented obstacle lists").
- Parent (before-state): `b6fa2b1`.
- Protocol HEAD at review time: `b07035c` (canonical live state; validate green).
- Clean clones (never in-place): `D:/ccv-0261` @ f1d9c30, `D:/ccv-0261-parent` @ b6fa2b1.

## Reproduction (exit-code gated, real entrypoint)

Maker suite in the clean clone:

    $ python examples/mailbox_report_cases/run_mailbox_report_cases.py
    OK: governed mailbox report cases passed (17).   -> exit 0

Independent falsifiability probe (my own vectors, run through the REAL validator
`scripts/validate_collaboration_state.py --root <fixture>`, subprocess, both clones):

### SLIP-1 -- valid INDENTED list + friction_count 2 (must go green)

Payload obstacles block (the context_refs indentation convention):

    obstacles:
      - what: X
        root_cause: Y
        resolution: Z
        recurrence_risk: low

| placement   | before (b6fa2b1) | after (f1d9c30) | expected | result |
|-------------|------------------|-----------------|----------|--------|
| frontmatter | exit 1 (false red)| exit 0          | exit 0   | PASS   |
| body        | exit 1 (false red)| exit 0          | exit 0   | PASS   |

The before-state actually reproduced the false red (empty-parse -> "friction_count > 0
but obstacles is empty"). The fix removes it. Behavior, not name.

### SLIP-2 -- MALFORMED indented list (missing fields) + friction_count 0 (must go red)

Payload: `- what: X` / `  root_cause: Y` (resolution + recurrence_risk absent), indented.

| placement   | before (b6fa2b1) | after (f1d9c30)                 | expected | result |
|-------------|------------------|---------------------------------|----------|--------|
| frontmatter | exit 0 (silent!) | exit 1 ("must contain exactly") | exit 1   | PASS   |
| body        | exit 0 (silent!) | exit 1 ("must contain exactly") | exit 1   | PASS   |

The before-state silently accepted the malformed indented obstacle (exit 0). The fix
now parses it and rejects it with the exact-field-set error. Behavior, not name.

### No-regression (fix clone, 9/9 through real validator)

| vector                                     | exit | expect | result |
|--------------------------------------------|------|--------|--------|
| col0 friction0 obstacles []                | 0    | 0      | PASS   |
| col0 friction0 non-empty                   | 0    | 0      | PASS   |
| col0 friction2 non-empty                   | 0    | 0      | PASS   |
| col0 friction2 [] -> fail                  | 1    | 1      | PASS   |
| col0 malformed friction1 -> fail           | 1    | 1      | PASS   |
| grandfathered (date 2026-07-21, pre-adopt) | 0    | 0      | PASS   |
| missing friction_count -> fail             | 1    | 1      | PASS   |
| friction non-integer (2.5) -> fail         | 1    | 1      | PASS   |
| opt-in border (date == adoption date)      | 0    | 0      | PASS   |

Grandfathering (pre-adoption date is not evaluated), opt-in by date/marker at both
borders, the four col-0 quadrants, integer friction, and the C4 malformed-fail all
hold. No regression.

### Escape hunt -- I tried to break the guarantee (parser fn, fix clone)

Danger direction = a MALFORMED block read as EMPTY/valid so friction_count 0 passes
silently (a new SLIP-2). None found:

| indentation trick                          | parser result | escape? |
|--------------------------------------------|---------------|---------|
| tab-indented dash, malformed               | ERROR         | no (fails safe) |
| tab field under space-dash, malformed      | ERROR         | no (fails safe) |
| second dash OVER-indented after full item  | 1 merged item | no (see R1) |
| mixed-indent field, malformed              | ERROR         | no |
| field at SAME indent as dash               | ERROR         | no (fails safe) |
| header + fields with NO dash               | empty         | no (see R2) |
| dash / blank line / field                  | ERROR (blank skipped) | no |
| deeply-indented (8 spaces) valid list      | 1 item        | no (parses) |
| col-0 valid sanity                         | 1 item        | no |

The parser now anchors on the first dash's indent, requires fields strictly deeper
than that indent, and re-flags exact-field-set / risk-vocabulary / empty-field on any
parsed item. I could not manufacture a missing-field obstacle that survives as valid.

## Declared residuals (benign, out of iter1 scope -- NOT blockers)

- **R1 (quirk, not exploitable):** a subsequent obstacle item indented DEEPER than the
  first item's dash is swallowed as a continuation/last-wins merge into the prior item
  rather than starting a new item. It cannot forge a missing-field pass (the merged
  item still must carry all four valid fields), and there is no `friction_count ==
  len(obstacles)` rule to violate. Non-uniform authoring only; safe direction.
- **R2 (pre-existing, unchanged by f1d9c30):** an `obstacles:` header with no `-` list
  item and no `[]` is read as empty. Benign for friction 0 (no obstacle declared);
  correctly RED for friction > 0. Identical before and after the fix -- not a regression.

## Protocol gates (canonical HEAD b07035c)

    validate_collaboration_state.py   -> exit 0
    protocol_replay.py --check-drift  -> verdict=CLEAN up_to_seq=5983, exit 0 (drift 0)
    scan_encoding.py                  -> exit 0
    scan_domain_neutrality.py         -> exit 0

## Closure recommendation

**OK-CLOSABLE.** iter1 (f1d9c30) closes both SLIP-1 (valid indented list -> green) and
SLIP-2 (malformed indented list -> red) by behavior at the real entrypoint, in
frontmatter and body, with the exact vectors the review named; no regression in
grandfathering / opt-in / col-0 / integer / C4; no new indentation escape survives; all
protocol gates green. TASK-0261 remediation is closable.

-- Analista
