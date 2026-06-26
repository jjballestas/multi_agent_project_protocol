---
skill_id: business-rule-vs-legacy
title: Business rule vs legacy behavior
profile: financiero_presupuesto
version: 0.1.0
neutral_core: false
---

# Procedure

Use this checklist when changing inherited behavior:

1. State the observed behavior separately from the intended rule. Do not treat existing behavior as authoritative
   until a source of intent confirms it.
2. Trace callers, stored data, tests, documentation, and operator workflows that depend on the behavior.
3. Classify each dependency as intentional rule, compatibility requirement, accidental coupling, or unknown.
4. Preserve intentional rules with direct tests and explicit wording in the task or handoff.
5. Isolate accidental coupling behind a compatibility layer or migration step when immediate removal would create
   avoidable risk.
6. For unknown cases, keep the behavior stable, record the question, and request a decision before changing the
   externally visible contract.
7. In the final handoff, name which behaviors were preserved by design and which were left unchanged only for
   compatibility.
