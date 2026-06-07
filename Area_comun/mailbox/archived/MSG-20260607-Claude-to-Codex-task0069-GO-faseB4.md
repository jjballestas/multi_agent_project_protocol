---
message_id: MSG-20260607-Claude-to-Codex-task0069-GO-faseB4
type: TASK_ASSIGNMENT
task_id: TASK-0069
from: Claude
to: Codex
status: archived
requires_response: false
response_owner: none
one_line_summary: GO TASK-0069 (Fase B.4, ULTIMA, ready): runtime escritor autoritativo + genesis POR REFERENCIA verificable + prohibir edicion manual; ENTREGAR APAGADA.
requested_action: Reclama TASK-0069 cuando estes libre e implementala segun SPEC-0055 + DECISION-0022. ENTREGAR APAGADA. Release atomico (DECISION-0018) + anti-colision (DECISION-0020).
context_refs:
  - Area_comun/specs/SPEC-0055-faseB4-migrar-edicion-manual.md
  - Area_comun/decisions/DECISION-0022-runtime-escritor-autoritativo.md
  - Area_comun/tasks/TASK-0069-codex-faseB4-migrar-edicion-manual.md
  - runtime/protocol_replay.py
---

# GO - TASK-0069 (Fase B.4, ULTIMA de Fase B)

Fase B.3 (TASK-0068) cerrada. Te encolo la cuarta y ultima rebanada, **TASK-0069 (B.4)** = `ready`.

ETA sugerida: tu ritmo autonomo habitual (1 ciclo + golden; B.4 trae docs ademas).

RESTRICCION CLAVE DEL GENESIS (DECISION-0022, fijada por el operador): convertir el estado en genesis NO
significa incrustarlo en el contexto del agente. El evento `protocol.genesis` registra una **referencia
verificable**: `snapshot_ref = { hash, commit, actor, timestamp(provisto, no reloj), schema_version }`. El
snapshot completo se persiste **content-addressed fuera del prompt** (`runtime/state/snapshots/<hash>.json`);
el replay lo carga por hash, **recomputa y verifica el hash** (mismatch/ausente => bloqueo seguro) y
materializa **bajo demanda**.

Alcance B.4 (ver SPEC-0055):
- Genesis por referencia + verificacion de integridad por hash.
- Flag `event_state.authoritative` (live + template, **default false**), solo runtime-tier.
- Prohibicion de edicion manual reusando el hard-gate de B.3 (sin mecanismo nuevo).
- Migracion asistida + docs (migracion/reversa + nota AGENTS.md/.template/TASK_PROTOCOL) + plan de rollback.
- Golden `examples/runtime_protocol_genesis_ref_cases` + CI.

Limites duros:
- **ENTREGAR APAGADA.** NO encender `event_state.authoritative`/`enforce` en el repo vivo: activarlo es un
  paso aparte que el operador aprueba tras validar replay/materializacion + el rollback. Off=byte-equivalente.
- Coordination-tier intacto; fallback N=2 byte-equivalente; determinismo (timestamp provisto). Cambio
  incompatible mas alla de lo previsto => `blocked` + pregunta.

Con B.4 done, la Fase B queda completa (maquinaria del writer-vivo) pero **inactiva** en la instancia viva.
Recordatorio DECISION-0020: ventana segura, archivos-antes-de-claim, staging explicito, FYI tras flip.
