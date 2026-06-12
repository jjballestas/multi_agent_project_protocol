# MSG 2026-06-13 - Operador -> Codex - TASK-0101 promovido a ready + GO

- **De:** Operador humano (john.ballestas@gmail.com)
- **Para:** Codex (implementer)
- **Asunto:** TASK-0101 (prev_hash encadenado) promovido a `ready`; GO de inicio
- **Requiere respuesta:** No (GO terminal; reclama y comienza cuando esté listo)

---

## Mensaje

**TASK-0101** (`Area_comun/tasks/TASK-0101-codex-eventlog-prev-hash.md`) ha sido promovido de
`proposed` a `ready`.

**SPEC:** [SPEC-0070](Area_comun/specs/SPEC-0070-prev-hash-encadenado.md) (clausura 561 líneas,
acceptance criteria + test plan + 10 golden cases)

### Siguiente paso

- **Reclama TASK-0101** cuando esté listo (claim en `Area_comun/state/CLAIMS.json` con owner Codex)
- **Status:** `ready → claimed → in_progress`
- **Entregas esperadas:** runtime/eventlog.py (prev_hash bajo flag off-by-default), protocol_replay.py
  (validador integrado), protocol.config.json (nuevo flag event_state.chain_enabled), ejemplos/casos
  golden
- **Handoff:** Autocontenido con evidencia (versiones, hashes, reproducibilidad)

### Contexto

- DECISION-0029 aprobada (firmantes cruzados sin consenso: prev_hash encadenado base; luego
  firma por agente + anclaje externo)
- Las otras dos tareas (TASK-0102/TASK-0103) dependen de esta; pueden prepararse en paralelo
- SPEC-0070 responde Q1 (genesis) y Q2 (prune/archive); interacción formalizada
- Modo legacy completamente preservado (flag off-by-default)

¡Adelante!

---

*GO terminal. No requiere ACK.*
