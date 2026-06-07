---
message_id: MSG-20260607-Claude-to-Codex-task0066-GO-faseB1
type: TASK_ASSIGNMENT
task_id: TASK-0066
from: Claude
to: Codex
status: open
requires_response: false
response_owner: none
one_line_summary: GO TASK-0066 (Fase B.1, ready): replay/materializacion del estado de protocolo read-only + drift WARNING gateado (off=byte-equivalente). Primera rebanada de Fase B post-v1.0.
requested_action: Reclama TASK-0066 cuando estes libre e implementala segun SPEC-0052 (B.1). Release atomico (DECISION-0018) + anti-colision (DECISION-0020).
context_refs:
  - Area_comun/specs/SPEC-0052-faseB-replay-estado-protocolo.md
  - Area_comun/tasks/TASK-0066-codex-faseB1-replay-estado-protocolo.md
  - Area_comun/specs/SPEC-0039-event-log-writer-vivo.md
---

# GO - TASK-0066 (Fase B.1)

v1.0.0 ya esta publicado (tag v1.0.0). El operador ordeno arrancar **Fase B** (event log como writer del
ESTADO DE PROTOCOLO, SPEC-0039 sec.4) y el paraguas **TASK-0038**. La decompuse en SPEC-0052 (B.1..B.4) y
te encolo la primera, **TASK-0066 (Fase B.1)** = `ready`.

ETA sugerida: tu ritmo autonomo habitual (~1 ciclo de implementacion + golden). Sin prisa dura.

Alcance B.1 (acotado, ver SPEC-0052 sec.3):
- `replay_protocol_state` / `materialize_protocol_state` / `build_genesis_snapshot` / `protocol_state_drift`
  deterministas y canonicos (sin reloj/red).
- Config `event_state.enabled` (live + template, **default false**).
- Validador py/.ps1: drift como **WARNING** solo con `runtime/state/` presente Y `event_state.enabled`;
  con la feature off => **byte-equivalente** (sin warning, sin hard-fail).
- Golden `examples/runtime_protocol_replay_cases` + CI.

Limites duros (NO en B.1, son B.2-B.4 gateadas):
- NO materializar los `*.json` como verdad. NO tocar apply/orchestrator write-path. NO prohibir/migrar la
  edicion manual. Si la reconstruccion exige tocar eso => `blocked` + pregunta.

Recordatorio DECISION-0020 (recien formalizada): ventana segura, archivos-antes-de-claim, staging explicito,
el FYI/in-review DESPUES del flip. Promuevo de a una; cuando cierres B.1 te encolo B.2.
