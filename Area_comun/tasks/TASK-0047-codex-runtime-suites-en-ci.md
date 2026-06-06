---
id: TASK-0047
owner: Codex
status: done
type: integration
priority: high
created_at: 2026-06-06
updated_at: 2026-06-06
depends_on: [TASK-0046]
relates_to: [TASK-0017]
phase: P2
spec_id: Area_comun/specs/SPEC-0038-n-agent-registry.md
linked_decisions: [DECISION-0006, DECISION-0015]
execution_pipeline: [editar .github/workflows/validate.yml agregando steps que ejecuten los runners de runtime hoy ausentes en CI; usar el mismo interprete/orden que el handoff local; declarar dependencias (p.ej. jsonschema) en el job si hace falta; mantener determinismo (sin red, sin reloj real, llm-adapter en modo recorded sin --allow-real-invoker)]
acceptance_criteria: [CI ejecuta y pasa en verde: runtime_router_cases, runtime_eventlog_cases, runtime_review_qa_cases, agent_registry_cases, runtime_turn_cases (schema y semantic), runtime_apply_cases, runtime_loop_cases, runtime_observability_cases, llm_adapter_cases (modo recorded); no se ejecuta ninguna invocacion LLM real ni acceso a red; los gates existentes (validador py/ps1, encoding, neutralidad, golden de protocolo) siguen verdes; aditivo: no se toca runtime/ ni el contrato ni los fixtures; cambio limitado a .github/workflows]
test_plan: [correr localmente cada runner agregado (debe seguir verde 61/61) antes del push; verificar el YAML del workflow (sintaxis) y que el job declara sus dependencias; confirmar que llm_adapter_cases corre sin --allow-real-invoker; idealmente validar el workflow en una rama o con act/dry-run si esta disponible, si no documentar la verificacion local en el handoff]
closure_criteria: [.github/workflows/validate.yml ejecuta las suites de runtime y queda verde; sin red ni LLM real; resto de gates intactos; no se modifico runtime/ ni contrato; handoff autocontenido con la lista exacta de steps agregados; claim liberado al pasar a in_review]
---

# TASK-0047 - Capa A.5: correr las suites de runtime en CI

Estado operativo: DONE. ACEPTADA por Claude con ratificacion (2026-06-06): corri yo los 10 runners
(61/61) + gates py + parse YAML; solo se toco .github/workflows/validate.yml (step jsonschema + 10
runners, llm-adapter recorded sin --allow-real-invoker); runtime/contrato/fixtures intactos. Ver
`Area_comun/handoffs/HANDOFF-TASK-0047-codex-to-claude-1.md`.

> `integration` -> SDD. Consolidacion del nucleo N-agente (criterio 14 de SPEC-0038: "CI ejecuta unit,
> contract, golden, replay y concurrency tests"). Decision del operador (2026-06-06): consolidar Capa A.

## Contexto

Hoy el workflow de CI (`.github/workflows/validate.yml`) corre el validador (py/ps1), encoding, neutralidad
y varios golden de protocolo (sdd, compact-comms, neutrality, mailbox-status, encoding-gate, handoff-release),
pero **NO** corre las suites de runtime (router, eventlog, review_qa, registry, turn, apply, loop, observability,
llm-adapter), que hoy solo se ejecutan en local/handoff. Eso deja el nucleo N-agente sin proteccion de
regresion automatica. Esta tarea cierra esa brecha.

## Alcance

- Editar SOLO `.github/workflows/validate.yml` (aditivo).
- Agregar steps que ejecuten, con python, cada runner:
  - examples/runtime_router_cases/run_runtime_router_cases.py
  - examples/runtime_eventlog_cases/run_runtime_eventlog_cases.py
  - examples/runtime_review_qa_cases/run_runtime_review_qa_cases.py
  - examples/agent_registry_cases/run_agent_registry_cases.py
  - examples/runtime_turn_cases/run_runtime_turn_schema_cases.py
  - examples/runtime_turn_cases/run_runtime_turn_semantic_cases.py
  - examples/runtime_apply_cases/run_runtime_apply_cases.py
  - examples/runtime_loop_cases/run_runtime_loop_cases.py
  - examples/runtime_observability_cases/run_runtime_observability_cases.py
  - examples/llm_adapter_cases/run_llm_adapter_cases.py  (modo recorded; SIN --allow-real-invoker; sin red)
- Declarar dependencias del job si algun runner las requiere (p.ej. `jsonschema` para turn_validate).

## Restricciones

- **Aditivo**: no tocar `runtime/`, ni el contrato, ni los fixtures, ni los gates existentes.
- **Determinismo**: sin red, sin reloj real, sin invocaciones LLM reales.
- **Neutralidad de dominio** intacta; sin secretos.
- Handoff autocontenido con la lista exacta de steps agregados y la verificacion local; claim liberado al
  pasar a `in_review`.

## Nota de secuencia (Capa A)

Este item es el arranque de bajo riesgo de la Capa A. NO depende del event log writer-vivo (A.1), que el
arquitecto (Claude) especificara en una spec aparte (posible DECISION por tocar el mecanismo de escritura del
estado). Siguientes de Capa A tras este: golden N=3/N=5 (A.2), property-based I1-I8 (A.3), concurrency
simulation (A.4), hardening autor-de-record (A.6), SemVer del schema (A.7).
