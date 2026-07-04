---
skill_id: codegen-triage
title: Codegen triage
version: 0.1.0
neutral_core: true
---

# Codegen Triage

Use this skill before coding when a task looks repetitive, template-shaped, or
derived from a structured source. The accountable signer applies the decision and
keeps responsibility for the result.

This skill decides only between deterministic code generation and boundary
signer work. It does not authorize an assistant worker, extra agent, reviewer, or
judgment-bearing delegation.

## Decision

Return this shape:

```json
{
  "camino": "codegen | frontera",
  "razon": "",
  "gate": "",
  "banderas": []
}
```

Choose `codegen` only when all required conditions are true.

## Required Conditions

1. Deterministic source.

   The output is a total mechanical function of one explicit source. Literal
   test: for each source item, emit a known set of files or blocks by filling
   fixed placeholders.

2. Deterministic oracle.

   Correctness is accepted by an automatic gate, not by human judgment. The gate
   must be named before generation and must cover build, behavior, structure,
   parity, lint, or formatting as relevant to the generated surface.

If either condition is absent, choose `frontera`.

## Red Flags

Choose `frontera` when the change:

- composes more than one state mutation;
- calls procedures or services in a required sequence;
- crosses a module boundary;
- touches request context, identity context, ownership context, balances, or
  reconciliations;
- depends on a known gap between a view and the source of truth;
- changes business rules, authorization, privacy, migration, audit, or recovery
  behavior;
- needs a reviewer to decide whether the result is semantically correct.

## Rules

- The signer remains accountable for the generated output.
- Generation is valid only for surfaces whose review is cheaper than manual
  authoring.
- A broad surface is still mechanical only when it has one source, one output
  pattern, no ordered mutation sequence, and no known source gap.
- When in doubt, choose `frontera`.

## Study Integrity

Deterministic generation is standard single-developer practice. It is
zero-token, repeatable, and does not add an agent or judgment-bearing delegate.
It is not the measured treatment in any comparison that distinguishes solo work
from assisted work.

For paired comparisons, deterministic generation must be available and applied
symmetrically within the pair when its conditions are met. Any formal study-arm
wording is an input to the sealing step, not part of this skill's authority.
