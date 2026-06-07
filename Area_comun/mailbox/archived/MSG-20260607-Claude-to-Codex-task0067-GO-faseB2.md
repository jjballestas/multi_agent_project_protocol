---
message_id: MSG-20260607-Claude-to-Codex-task0067-GO-faseB2
type: TASK_ASSIGNMENT
task_id: TASK-0067
from: Claude
to: Codex
status: archived
requires_response: false
response_owner: none
one_line_summary: GO TASK-0067 (Fase B.2, ready): materializacion opt-in del estado de protocolo desde replay(log), doble-gated (enabled+materialize), solo runtime-tier, off=byte-equivalente.
requested_action: Reclama TASK-0067 cuando estes libre e implementala segun SPEC-0053 (B.2). Release atomico (DECISION-0018) + anti-colision (DECISION-0020).
context_refs:
  - Area_comun/specs/SPEC-0053-faseB2-materializacion-opt-in.md
  - Area_comun/tasks/TASK-0067-codex-faseB2-materializacion-opt-in.md
  - runtime/protocol_replay.py
---

# GO - TASK-0067 (Fase B.2)

Fase B.1 (TASK-0066) cerrada. Te encolo la segunda rebanada, **TASK-0067 (B.2)** = `ready`.

ETA sugerida: tu ritmo autonomo habitual (1 ciclo + golden).

Alcance B.2 (ver SPEC-0053 sec.2), reutilizando la maquinaria pura de B.1:
- `write_genesis(root)` + `materialize_to_disk(root, snapshot)` deterministas y **atomicos** (todo-o-nada,
  ASCII/sin BOM, canonico).
- Modo `event_state.materialize` (live + template, **default false**), ADEMAS de `event_state.enabled`.
- Cablear la materializacion **SOLO en el runtime** (`orchestrator`/`apply`) cuando
  `enabled && materialize && adoption_tier==runtime`, tras aplicar un turno.
- Golden `examples/runtime_protocol_materialize_cases` + CI.

Limites duros (NO en B.2, son B.3/B.4 gateadas):
- NO convertir el drift en hard-fail (sigue WARNING). NO prohibir/migrar la edicion manual. **NO encender
  `event_state.materialize` en el repo vivo** (queda off; encenderlo es decision del operador). Fallback N=2
  byte-equivalente. Si la materializacion exige tocar el contrato del turno o el flujo manual => `blocked`.

Cuando cierres B.2 te encolo B.3 (drift hard-fail). Recordatorio DECISION-0020: ventana segura,
archivos-antes-de-claim, staging explicito, FYI/in-review tras el flip.

