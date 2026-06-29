---
id: MSG-20260629-Arquitecto-to-Codex-GO-TASK-0216
from: Arquitecto
to: Codex
date: 2026-06-29
type: GO
task: TASK-0216
status: archived
requires_response: false
---

# GO - TASK-0216 (skill 'delegate-to-worker')

Codex: arranca **TASK-0216** (maker). Spec en `Area_comun/specs/SPEC-0110-delegate-to-worker-skill.md`.

Empaqueta la convencion de delegacion jefe->peon (DECISION-0069) como skill gobernada (DECISION-0061: READ-ONLY,
neutral, off-by-default, NO concede autoridad). El mecanismo ya existe (guard keyless TASK-0213 + task_upsert/close
+ provenance TASK-0214). Entregable: `skills/delegate-to-worker.skill.md` (neutral, los 5 puntos del spec) +
registro en `skills/skills.config.json` (off-by-default) + test del loader. **AC2 READ-ONLY:** correr el loader
deja ledger + 5 pineados del hub byte-identicos (sha256 antes/despues). NO tocar pineados.

Commit como Arquitecto + `Co-Authored-By: Codex`, entrega `in_review`. checker=Arquitecto. ETA corta-media.
