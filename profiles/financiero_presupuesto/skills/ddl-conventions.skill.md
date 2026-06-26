---
skill_id: ddl-conventions
title: DDL conventions
profile: financiero_presupuesto
version: 0.1.0
neutral_core: false
---

# Procedure

Use this checklist when proposing or reviewing data definition changes:

1. Name objects consistently before writing statements. Prefer stable, descriptive names for tables, columns,
   constraints, indexes, and migration files. Avoid names that encode temporary implementation details.
2. Choose data types from the smallest clear semantic contract. Record precision, scale, length, nullability, and
   default behavior explicitly when they affect consumers.
3. Declare constraints close to the data invariant. Include primary keys, foreign keys, uniqueness, checks, and
   default values only when they express an intentional rule.
4. Make the change repeatable. Split create, alter, backfill, verify, and cleanup steps so a failed run can be
   diagnosed and resumed without hidden side effects.
5. Keep compatibility visible. For every destructive or narrowing change, document the expected reader/writer
   impact and the reversible step that precedes it.
6. Verify the resulting shape with schema inspection and a small set of representative data checks before handoff.
