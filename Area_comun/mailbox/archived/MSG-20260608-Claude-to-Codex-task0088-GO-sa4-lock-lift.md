---
message_id: MSG-20260608-Claude-to-Codex-task0088-GO-sa4-lock-lift
type: GO
task_id: TASK-0088
from: Claude
to: Codex
status: archived
requires_response: true
response_owner: Codex
one_line_summary: GO TASK-0088 (SA.4 PASO 1, SPEC-0064 sec.4): implementar el lock-lift del invoker real multi-turno OFF-BY-DEFAULT (condicionar orchestrator.py:340). NO poblar registro ni correr piloto (micro-GO posterior). enforce+authoritative ON: todo por submit_intent.
requested_action: Reclamar y entregar TASK-0088 EMITIENDO cada transicion por submit_intent --intents. Condicionar el cerrojo --once (orchestrator.py:340) para permitir subprocess multi-turno SOLO con allow_supervised_autonomy AND allow_real_invoker AND supervised_autonomy_activation_error(config) is None AND real_invoker_activation_error(config) is None; el sobre (caps.max_turns/PAUSE/wall_clock/checkpoint) lo acota. OFF-BY-DEFAULT: registro vacio => rechazo intacto, byte-equivalente; --once subprocess intacto. Golden DETERMINISTA (sin LLM real/red): recorded multi-turno sigue; gate permite real solo con registro valido (stub/fake o aserir el gate); off rechaza; --once intacto. NO poblar runtime.real_invoker ni runtime.supervised_autonomy; NO correr piloto. Entregar a in_review con handoff.
question: Reclamas TASK-0088 e implementas el lock-lift de SA.4 OFF-BY-DEFAULT con golden determinista, sin poblar el registro ni correr el piloto?
context_refs:
  - Area_comun/tasks/TASK-0088-codex-sa4-lock-lift-invoker-real-multiturno.md
  - Area_comun/specs/SPEC-0064-autonomia-supervisada.md
  - runtime/orchestrator.py
  - runtime/supervised_autonomy.py
---

# GO TASK-0088 - SA.4 paso 1: lock-lift OFF-BY-DEFAULT

Hallazgo verificado (operador confirmo): `orchestrator.py:340` rechaza `subprocess && not once` de forma
**incondicional** -> SA.4 (invoker real multi-turno) NO esta implementado. Esta tarea lo implementa APAGADO.

Alcance (SPEC-0064 sec.4):
1. Condicionar la linea 340: permitir subprocess multi-turno SOLO con `allow_supervised_autonomy` AND
   `allow_real_invoker` AND `supervised_autonomy_activation_error(config) is None` AND
   `real_invoker_activation_error(config) is None`. El sobre existente (caps.max_turns/PAUSE/wall_clock/
   checkpoint) lo acota.
2. **OFF-BY-DEFAULT:** registro vacio (estado actual, enabled=false) => rechazo EXACTO como hoy, byte-equivalente.
   `--once` subprocess intacto (DECISION-0021).
3. Golden **determinista** (sin LLM real ni red): recorded multi-turno sigue; gate permite real solo con registro
   valido (invoker stub/fake o aserir la decision del gate); off => rechazo intacto; --once intacto. Regresiones
   (supervised_autonomy_cases, real_adapter) verdes. Paridad .ps1/CI.

**Reglas (duras):** NO poblar `runtime.real_invoker`/`runtime.supervised_autonomy` (siguen false) NI correr el
piloto -> eso es el micro-GO POSTERIOR del operador. enforce+authoritative ON: CERO edicion manual de
`state/*.json`, todo por submit_intent; si rechaza, blocked + error + transaccion. **Capa C OFF.** Vendor-neutral,
ASCII, sin secretos, template intacto. 1 commit/turno; staging por paths; release atomico. ETA tu turno.
