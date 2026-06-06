---
spec_id: SPEC-0038-n-agent-registry
task_id: TASK-0038
type: implementation
status: proposed
linked_decisions: [DECISION-0015, DECISION-0009, DECISION-0001, DECISION-0011]
created_at: 2026-06-06
author: Claude
---

# SPEC-0038 - Registry de agentes por capacidades y runtime sin roles fijos (N-agente)

> Estado: PROPOSED. Spec paraguas de TASK-0038 bajo DECISION-0015 (modelo de equipo completo). Captura el
> diseno y la descomposicion; **implementacion diferida y triple-gateada** (TASK-0039 -> aprobacion humana
> DECISION-0015 -> OK del operador). Aditivo, off-by-default, backward-compat.

## Contexto
Ver DECISION-0015. El protocolo ya es casi todo agente-agnostico; el unico bloqueador duro es el `enum`
del campo `agent` en `runtime/turn_schema.json` (jsonschema en `turn_validate.py`). El resto son defaults
blandos (router/apply/prune) o plantillas/docs. El objetivo es generalizar roster + ruteo + revision a un
"equipo de desarrollo competente" (capacidades, review-by-not-author, QA gate), manteniendo el N=2 actual
como caso particular sin migracion.

## Mapa de acoplamiento (estado actual)
- **Duro:** `runtime/turn_schema.json` campo `agent` con `enum:["Claude","Codex","operador humano"]`.
- **Blando (defaults):** `runtime/router.py` `select_review` (owner "Claude"), `select_human_gate`
  (owner "operador humano"); `runtime/apply.py` owner por defecto del claim "Codex"; `scripts/prune_state.py`
  (+ .ps1) `updated_by` "Codex".
- **Plantillas/scaffolding:** `protocol.config.template.json` `agent_roles`; `PROJECT_STATE.template.json`
  `agents`; `AGENTS.template.md` seccion 3; `scripts/new_instance.py` (--architect/--implementer/--human-owner).
- **Docs:** `TASK_INDEX.legend.owner` (descriptivo, no enforced).
- **Ya agnostico (no tocar):** validador (owner string libre), mailbox from/to/response_owner, lifecycle,
  claims por fila, gates por invariante, context/turn_validate (salvo el enum del schema), adapters/base.

## Modelo objetivo

### Agent registry (config-driven, opcional en protocol.config.json)
```json
"agent_registry": {
  "enabled": true,
  "agents": [
    {"id": "Claude", "capabilities": ["architect","reviewer","orchestrator","qa"], "adapter": "llm", "enabled": true},
    {"id": "Codex",  "capabilities": ["implementer"], "adapter": "llm", "enabled": true},
    {"id": "operador humano", "capabilities": ["human_owner"], "adapter": "human", "enabled": true}
  ]
}
```
Capacidades reservadas: `architect, implementer, reviewer, qa, orchestrator, human_owner`. `id` string
libre. Extras neutrales permitidas; desconocidas ignoradas (forward-compat).

### Fallback de 3 niveles (resolver unico en runtime/context.py)
`load_agent_registry(root)` devuelve un registry normalizado:
1. si `agent_registry.enabled` -> usarlo;
2. si no, sintetizar la triada desde `agent_roles` (architect->architect/reviewer/orchestrator/qa;
   implementer->implementer; human_owner->human_owner);
3. si no hay config -> triada por defecto cableada.
Garantiza que fixtures/golden/instancias actuales pasan sin migracion.

## Alcance (cambios cuando se implemente)
- **turn_schema.json:** `agent` de `enum` a `{type:string, minLength:1}`.
- **turn_validate.py:** check semantico config-driven: `agent` debe ser `id` registrado y `enabled`
  (ademas del check actual claim.owner == report.agent).
- **router.py:** `select_review` = review-by-not-author (reviewer/architect != autor; sin elegible =>
  escalate); QA gate opcional (qa != autor, si hay test_plan); `select_human_gate` = capacidad human_owner;
  `select_ready_task` = filtro opcional `required_capability` + disponibilidad. Threading del registry por
  `select_next` (lee de `state["root"]`).
- **apply.py:** owner por defecto del claim = agente actuante (`report["agent"]`), no "Codex".
- **prune_state.py + .ps1:** `--actor` opcional (fallback "Codex" para salida byte-identica).
- **adapters/base.py:** `ContextPack.agent: str|None` (poblado desde `unit.owner`).
- **scaffolding/plantillas:** `new_instance.py` `--agent 'id:cap1,cap2'` repetible (exigir >=1
  reviewer/architect y >=1 human_owner); registry en `protocol.config.template.json` y
  `PROJECT_STATE.template.json` via placeholder; `AGENTS.template.md` seccion 3 tabla por capacidades +
  prosa del invariante review-by-not-author / QA gate.
- **docs:** `TASK_INDEX.legend.owner` "cualquier id registrado"; `runtime/README.md` registry + fallback.

## No-alcance
- NO activar autonomia multiagente por defecto. NO romper instancias actuales. NO acoplar el core a
  proveedores/modelos concretos. NO cambiar el motor M1 (apply/gate/vcs) ni claims-por-fila.

## execution_pipeline (descomposicion a-g; sub-tareas NO registradas todavia)
- **a)** DECISION-0015 + esta SPEC-0038 (docs de contrato). [requiere aprobacion humana]
- **b)** Resolver registry en `context.py` (`load_agent_registry` 3-niveles + helpers de capacidad).
- **c)** turn_schema (quitar enum) + turn_validate (check semantico). [contrato; rides on DECISION-0015]
- **d)** router (review-by-not-author + QA gate + human gate + ruteo por capacidad).
- **e)** apply/prune defaults (owner actuante + --actor).
- **f)** scaffolding/plantillas/AGENTS seccion 3. [cambia superficie de contrato]
- **g)** docs + CHANGELOG + bump protocol_version (publicacion MINOR).
Orden: a -> b -> (c,d,e en paralelo) -> f -> g.

## acceptance_criteria
- Un 3er agente registrado + claim suyo + report `agent`=3ro => `validate_turn == []`; agente no
  registrado => error.
- `select_next` rutea review a un agente reviewer/architect != autor, determinista; autor-unico => escalate.
- Con agente `qa` + `test_plan`: paso de verificacion (qa != autor) antes de done; sin `qa` colapsa al
  ratificado unico.
- Fallback 2-agentes intacto: `run_runtime_router_cases.py` y `run_runtime_turn_semantic_cases.py` verdes
  SIN editar fixtures.
- `examples/**` verdes + neutralidad limpia + paridad .py/.ps1 donde aplique.

## test_plan
- Nuevo `examples/agent_registry_cases/` (config / agent_roles-fallback / default-triada).
- Extender `runtime_turn_cases` (3er agente verde, no-registrado rojo, casos actuales intactos).
- Extender `runtime_router_cases` (review-by-not-author, autor-unico->escalate, QA gate, casos actuales
  identicos).
- Extender `runtime_apply_cases` (owner=report.agent) y `prune_state_cases` (salida por defecto intacta;
  --actor honrado).
- Nuevo caso `new_instance` de 3 agentes que valida verde end-to-end. Sin red.

## closure_criteria
- Registry + fallback 3-niveles + contrato generalizado + router (review-by-not-author + QA gate) +
  scaffolding + docs/version; golden verdes; fallback 2-agentes sin regresion; neutralidad limpia;
  revision del arquitecto OK; cada sub-tarea libera su claim al pasar a in_review (handoff-release).

## Risks
- **Hueco de auto-review:** sin revisor elegible => escalar, nunca auto-aprobar (test explicito).
- **Drift de contrato (schema):** relajar el enum es lo unico que puede romper un consumidor estricto; el
  check semantico preserva estrictez; DECISION-0015 registra que sigue siendo MINOR.
- **Acoplamiento de fixtures:** golden sin config deben caer en el fallback por defecto (resolver 3-niveles).
- **Determinismo:** revisores/QA elegibles ordenados lexicograficamente (si no, rompe replay/run-log).
- **Secuenciacion:** dejar aterrizar TASK-0039 (toca runtime/adapters) antes de tocar runtime/.

## Traceability
| Requirement | Sub-task | Test | Closure criterion |
|-------------|----------|------|-------------------|
| Registry config-driven + fallback 3-niveles | b | agent_registry_cases | resuelve registry esperado sin migracion |
| Contrato agent string validado vs registry | c | runtime_turn_cases | 3er agente verde, no-registrado rojo |
| Review-by-not-author + QA gate + human gate | d | runtime_router_cases | review a no-autor; autor-unico->escalate |
| Defaults por agente actuante | e | apply/prune cases | owner=report.agent; prune por defecto intacto |
| Scaffolding/plantillas N-agente | f | new_instance case | instancia de 3 agentes valida verde |
| Publicacion MINOR | g | validador + ejemplos | verde en root + ejemplos; neutralidad limpia |
