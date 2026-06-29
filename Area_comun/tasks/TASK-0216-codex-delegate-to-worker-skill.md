---
task_id: TASK-0216
title: "Skill gobernada 'delegate-to-worker': convencion de delegacion jefe->peon con verify+firma del jefe (DECISION-0069/0061, SPEC-0110)"
type: protocol
status: done
owner: Codex
phase: P2
priority: high
created_at: 2026-06-29
maker: Codex
checker: Arquitecto
linked_decisions: [DECISION-0069, DECISION-0061]
spec: SPEC-0110
file: Area_comun/tasks/TASK-0216-codex-delegate-to-worker-skill.md
---

# TASK-0216 -- Skill 'delegate-to-worker' (DECISION-0069/0061, SPEC-0110)

## Objetivo
Empaquetar la convencion de delegacion a peones (workers keyless) como skill gobernada (READ-ONLY, neutral,
off-by-default, no concede autoridad). El mecanismo ya existe (guard keyless TASK-0213 + task_upsert/close +
provenance TASK-0214); esta skill aporta el COMO. Spec autocontenido en SPEC-0110.

## Alcance (archivos NUEVOS; NO tocar pineados del hub)
- `skills/delegate-to-worker.skill.md` (neutral): cuando delegar, como autorar la sub-tarea moldeada, invariante
  de frontera (peon keyless NO cierra -> jefe verifica + FIRMA con provenance autor+modelo), checklist del jefe,
  anti-patrones. Sigue el patron de `skills/neutral-mechanism-example.skill.md`.
- Registrar en `skills/skills.config.json` (off-by-default).
- Test/golden del loader de skills.

## Criterios de aceptacion
AC1-AC4 de SPEC-0110. CRITICOS:
- **AC2 (READ-ONLY):** correr el loader deja ledger + 5 pineados del hub byte-identicos (sha256 antes/despues).
- **AC1:** skill neutral (scan_domain_neutrality limpio) + registrada off-by-default + no concede autoridad.

## DoD
AC1-AC4 verdes en clon limpio. Handoff in_review con la skill + entrada en skills.config + sha256 pineados
antes/despues identicos. Commit como Arquitecto + Co-Authored-By Codex. checker=Arquitecto.
