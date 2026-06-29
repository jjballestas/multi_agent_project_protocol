---
spec_id: SPEC-0110
title: Skill gobernada 'delegate-to-worker' -- convencion de delegacion jefe->peon con verify+firma del jefe (DECISION-0069 + DECISION-0061)
status: ready
owner: Codex
decision: DECISION-0069
relates_to: [DECISION-0069, DECISION-0061, DECISION-0070]
date: 2026-06-29
file: Area_comun/specs/SPEC-0110-delegate-to-worker-skill.md
---

# SPEC-0110 -- Skill 'delegate-to-worker'

Empaqueta la CONVENCION de delegacion a peones (workers keyless) de DECISION-0069 como una skill gobernada
(DECISION-0061): READ-ONLY, neutral, off-by-default, **NO concede autoridad** (la autoridad sigue en la FIRMA del
jefe). El mecanismo ya existe (peon keyless no puede cerrar bajo enforce -> guard V2 de TASK-0213; task_upsert/
task_status; provenance metadata; agent_metrics). Esta skill aporta el COMO.

## Componente
- `skills/delegate-to-worker.skill.md` (NUEVO, neutral): guia de convencion que un JEFE (firmante) carga para
  delegar trabajo mecanico-con-molde a un PEON (worker keyless). Contenido minimo:
  1. **Cuando** delegar: trabajo con molde existente (CRUDs, DTOs, mappers, tests de plomeria, migraciones
     repetitivas) que copia un patron que el jefe ya dejo hecho.
  2. **Como** autorar la sub-tarea: referenciar el patron/ejemplar (ruta) + AC claros + `owner=<peon>`; el peon
     produce en staging/su area personal (NO escribe el ledger).
  3. **Invariante de frontera (DURO):** el peon es keyless -> NO cierra ni firma; el JEFE verifica el entregable
     contra el molde + AC y FIRMA el cierre (`task_status done`) via submit_intent, registrando **provenance**
     (autor real = id del peon + modelo). Si el peon intenta escribir el ledger bajo enforce, falla cerrado
     (guard de TASK-0213).
  4. **Checklist de verificacion del jefe** antes de firmar: coincide con el molde; AC cumplidos; sin scope
     creep; sin secretos/PII; gates verdes.
  5. **Anti-patrones:** que el peon auto-firme; saltarse el verify; provenance falsa o ausente.
- Registrar la skill en `skills/skills.config.json` (off-by-default), siguiendo el patron de
  `skills/neutral-mechanism-example.skill.md`.

## Criterios de aceptacion
- **AC1:** existe `skills/delegate-to-worker.skill.md` neutral (scan_domain_neutrality limpio) cubriendo los 5
  puntos; registrada en `skills/skills.config.json` (off-by-default, no concede autoridad).
- **AC2:** el loader de skills (cold-start READ-ONLY, DECISION-0061) la lista/carga sin error; correr el loader
  deja el ledger + 5 pineados del hub byte-identicos (READ-ONLY; sha256 antes/despues).
- **AC3:** la skill es coherente con el mecanismo: cita el guard keyless (TASK-0213), la provenance que lee
  `agent_metrics.py` (TASK-0214), y la frontera de DECISION-0069. ASCII, neutral.
- **AC4:** golden/test del loader pasa; off-by-default (no se activa sola).

## DoD
AC1-AC4 verdes en clon limpio. Handoff in_review con la skill + entrada en skills.config + sha256 pineados
antes/despues identicos. maker=Codex/checker=Arquitecto. No toca pineados del hub (guardrail TFM).
