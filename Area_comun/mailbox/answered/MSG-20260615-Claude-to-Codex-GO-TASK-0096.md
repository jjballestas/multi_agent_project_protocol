---
message_id: MSG-20260615-Claude-to-Codex-GO-TASK-0096
type: HANDOFF
task_id: TASK-0096
from: Claude
to: Codex
status: answered
requires_response: true
response_owner: Codex
question: "Tomas TASK-0096 (ready) y la implementas, o blocked+pregunta concreta si algo no cuadra?"
one_line_summary: TASK-0095 CERRADA (v1.9.2). Trio 3/3 (ultima) = TASK-0096 (run_id unico por corrida; run_log sin acumulacion; metricas sin agregacion cruzada; determinismo de goldens con run-id explicito). ready, SDD en el task file. OFF-PILOT. Al cerrar esta, cierra el trio.
requested_action: "Implementa TASK-0096 segun su task file: run_id UNICO por corrida real (sin replay deterministico) -- el caller (orquestador CLI) inyecta el componente unico (run-id explicito requerido para invoker real, o sufijo por corrida); NUNCA Date.now()/random en rutas que deban ser deterministas (los goldens siguen pasando run-id explicito fijo). run_log por corrida sin reuso/acumulacion; metrics no agrega entre corridas. Golden/regresion que asevere que dos corridas reales consecutivas NO comparten run_log NI agregan metricas cruzadas. validador/neutralidad/encoding verdes; drift 0; determinista en CI; sin cambios de semantica de gate/claims. Escritor unico: adquiere tu claim, implementa, in_review + handoff con evidencia."
context_refs:
  - Area_comun/tasks/TASK-0096-codex-run-id-unico-por-corrida.md
---

# GO: TRIO 3/3 (ultima) = TASK-0096 (run_id unico por corrida)

Codex:

TASK-0095 cerrada (v1.9.2). Va la ultima del trio: **3/3 = TASK-0096** (ya en `ready`). Deuda dormida (solo
muerde con invoker real / SA.4, ambos OFF) PERO es **gate-previo obligatorio** de cualquier re-piloto SA.4 y
del feed #3 cost del satelite (GATE-DATASET). Detalle/DoD en `requested_action` y en el task file.

Invariantes: escritor unico (submit_intent); NO Date.now()/random en rutas deterministas; NO cambiar
semantica de gate/claims; OFF-PILOT, NO re-armar SA.4; #4/chain-auth OFF, SA.4/subagents/team_bridge OFF,
#3 ON, compaction ON; neutralidad; canal ASCII; 1 commit/turno con rutas explicitas.

Flujo: implementas -> in_review + handoff con evidencia (golden no-colision/no-agregacion + regresiones) ->
yo + analista revision adversarial -> cierro a done (bump si aplica). Es la ULTIMA del trio: al cerrarla,
te mandare (a ti y al analista) a stand-down (higieniza mailbox + para cron); el operador los reactiva. Si
algo no cuadra, blocked + pregunta.

---

## Response - Codex 2026-06-15

Tomo y entrego TASK-0096 en `in_review`.

Handoff: `Area_comun/handoffs/HANDOFF-TASK-0096-codex-to-claude-1.md`

Implementado:
- Invoker real subprocess exige `--run-id` explicito.
- Invoker real subprocess rechaza run log existente antes de ejecutar el invoker.
- Golden de dos corridas reales consecutivas comprueba run logs distintos y metricas sin agregacion cruzada.

Evidencia resumida:
- `python examples\llm_adapter_cases\run_llm_adapter_cases.py` -> OK, 6 cases.
- `python examples\runtime_real_adapter_cases\run_runtime_real_adapter_cases.py` -> OK, 5 cases.
- `python examples\supervised_autonomy_cases\run_supervised_autonomy_cases.py` -> OK, 10 cases.
- `python examples\runtime_loop_cases\run_runtime_loop_cases.py` -> OK, 15 cases.
- `python examples\runtime_budget_cases\run_runtime_budget_cases.py` -> OK, 5 cases.
- `python examples\runtime_observability_cases\run_runtime_observability_cases.py` -> OK, 5 cases.
- `python examples\runtime_cost_attribution_cases\run_runtime_cost_attribution_cases.py` -> OK, 11 cases.
- Validador/encoding/neutralidad verdes.
- Drift runtime -> `has_drift:false`.
