---
id: TASK-0043
owner: Codex
status: in_review
type: implementation
priority: high
created_at: 2026-06-06
updated_at: 2026-06-06
depends_on: [TASK-0038]
relates_to: [TASK-0042]
phase: P2
spec_id: Area_comun/specs/SPEC-0038-n-agent-registry.md
linked_decisions: [DECISION-0015, DECISION-0001]
execution_pipeline: [runtime/context.py load_agent_registry(root) con fallback de 3 niveles (agent_registry -> agent_roles -> triada por defecto) + helpers enabled_agents/agents_with_capability/has_capability, runtime/turn_schema.json campo agent de enum a {type string minLength 1}, runtime/turn_validate.py validacion semantica config-driven (agent registrado y enabled + capacidad requerida por la transicion) sin romper el check de claim.owner==agent, golden examples/agent_registry_cases + extender runtime_turn_cases]
acceptance_criteria: [load_agent_registry resuelve los 3 niveles (config explicito / agent_roles / triada por defecto), schema agent acepta string no vacio y rechaza vacio, turn_validate rechaza agente no registrado o disabled y agente sin capacidad de la transicion, registrado+enabled+capaz pasa, fallback N=2 byte-equivalente (run_runtime_turn_semantic_cases + router cases sin editar fixtures siguen verdes), un 3er agente registrado valida, golden deterministas sin red, paridad .py/.ps1 si se toca un validador con .ps1]
test_plan: [nuevo examples/agent_registry_cases (config/agent_roles/default + agente no registrado/disabled/sin-capacidad); extender runtime_turn_cases (3er agente valido + no-registrado rojo, 7 actuales intactos); regresion runtime suite verde]
closure_criteria: [registry resolver + fallback 3 niveles + helpers + schema agent->string + turn_validate semantico, golden verdes, fallback N=2 sin regresion, neutralidad limpia, handoff autocontenido, claim liberado al pasar a in_review]
---

# TASK-0043 - N-agente Fase 1: registry resolver + schema + validacion semantica

> `implementation` -> SDD; implementar contra **SPEC-0038 (congelada)** Fase 1 (sec.13) + addenda sec.20.
> Primera fase de implementacion del runtime N-agente tras congelar la Fase 0 (DECISION-0015 ACCEPTED).
> Aditivo, config-gated, **fallback N=2 intacto**.

## Alcance (Fase 1, minimo desbloqueo N-agente)
- `runtime/context.py`: `load_agent_registry(root)` con **fallback de 3 niveles** (D-4): (1) `agent_registry`
  de protocol.config; (2) sintetizar desde `agent_roles`; (3) triada por defecto cableada
  (Claude=architect/reviewer/orchestrator/qa, Codex=implementer, operador humano=human_owner). Helpers:
  `enabled_agents`, `agents_with_capability(cap)`, `has_capability(agent, cap)`.
- `runtime/turn_schema.json`: campo `agent` de `enum` a `{ "type": "string", "minLength": 1 }` (D-3, sec.12).
- `runtime/turn_validate.py`: validacion **semantica** config-driven (sec.8.1): `agent` debe ser id
  registrado y `enabled`; debe tener la **capacidad** requerida por la transicion; conservar el check actual
  `claim.owner == report.agent`. Estructurar el punto de validacion para que en Fase 2 se enchufen
  **firma/atribucion (A1/D-1)** e **idempotencia (A3/D-2)** sin reescribir (ahora NO se exige firma).

## No-alcance (fases posteriores)
- NO event log / leases / fencing / idempotencia (Fase 2). NO router por capacidad/fairness (Fase 3). NO
  maquina de estados Review/QA (Fase 4). NO firma de eventos todavia (se deja el hook, A1 aterriza en Fase 2).
- NO romper instancias N=2: el fallback debe dar comportamiento byte-equivalente sin migracion.

## Tests
- Nuevo `examples/agent_registry_cases/`: resolver en los 3 niveles; agente no registrado / disabled /
  sin-capacidad => error; registrado+enabled+capaz => ok.
- Extender `runtime_turn_cases`: un 3er agente registrado valida (verde); agente no registrado (rojo); los
  casos actuales (schema 4 + semantic 3) intactos.
- Regresion: suite runtime verde; `run_runtime_router_cases` y `run_runtime_turn_semantic_cases` SIN editar
  fixtures siguen verdes (prueba del fallback N=2). Sin red.

## Dogfood
Liveness + handoff-release. ASCII-only en mailbox/state (DECISION-0012). Paridad .py/.ps1 solo si tocas un
validador con contraparte .ps1. Te ratifico adversarialmente (foco: fallback N=2 byte-equivalente + rechazo
de agente no registrado/sin-capacidad). Si un punto exige decision, `blocked` + 1 pregunta.
