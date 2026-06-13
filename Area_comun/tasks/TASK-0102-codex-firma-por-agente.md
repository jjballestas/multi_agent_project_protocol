---
id: TASK-0102
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-12
updated_at: 2026-06-13
depends_on: [TASK-0101]
relates_to: [DECISION-0029, DECISION-0015, DECISION-0023]
phase: P2
spec_id: SPEC-0071
linked_decisions: [DECISION-0029, DECISION-0015, DECISION-0021, DECISION-0023]
deliverables:
  - atestacion de turno firmada por agente (formato compatible in-toto), off-by-default
  - integracion con agent_registry (material de firma por agente; claves privadas FUERA del repo)
  - atestacion de revision maker!=checker firmada por el revisor
relevant_files:
  - runtime/eventlog.py
  - runtime/llm_turn_wrapper.py
  - runtime/team_bridge.py
  - protocol.config.json
blocked_by_questions: []
objective: (DECISION-0029 pieza 2b) Cada agente del agent_registry posee material de firma propio (Ed25519 local o identidad keyless; backend configurable, vendor-neutral). Los turnos/handoffs relevantes para autoria llevan atestacion firmada por el agente productor - sujeto: hash del artefacto; predicado: agente, modelo-version, tarea, decision habilitante, trust_boundary de insumos. El runtime almacena y encadena pero NO puede producir atestaciones (no posee claves de agente).
expected_output: (1) Esquema de atestacion (JSON, compatible in-toto statement) versionado. (2) Firma en el wrapper del agente, no en el orquestador; claves publicas/identidades registradas en agent_registry; privadas fuera del repo (boundary sin cambio). (3) Verificador - una atestacion sin firma valida del agente declarado NO verifica (cubre A2 y A3-fabricacion del modelo de amenaza de DECISION-0029). (4) Revision maker!=checker emite atestacion del revisor que referencia el hash del turno revisado (deteccion parcial de omision via atestaciones huerfanas). (5) Golden cases: suplantacion de autoria detectada; fabricacion por runtime detectada; flujo legitimo verifica. (6) Off-by-default; overhead medido (bytes/atestacion, tokens si aplica) reportado en el handoff.
question_to_resolve: Q1 backend de firma por defecto (Ed25519 local vs keyless) y rotacion/expiracion de claves por sesion. Q2 que turnos atestan (todos vs solo los que producen artefactos rastreables) - coste vs cobertura. Q3 representacion de trust_boundary de insumos (enum cerrado, coherente con esquema de dos planos del caso de estudio).
closure_criterion: atestaciones firmadas por agente bajo flag; verificador rechaza suplantacion y fabricacion (golden cases verdes); claves privadas fuera del repo; atestacion de revisor operativa; overhead reportado; validador/neutralidad/encoding verdes; handoff con evidencia.
sdd_required: true
---

# TASK-0102 - Firma por agente: atestacion de autoria (DECISION-0029 pieza 2b)

> PROPOSED (Claude 2026-06-12, habilitada por DECISION-0029). Depende de TASK-0101 (encadenado). Es la
> pieza central: convierte la autoria de string anotado por el runtime en afirmacion criptografica del
> agente. Promover a ready+GO cuando el operador lo indique y la SPEC este cerrada.

## Contexto

Ver DECISION-0029 (decision 2b y modelo de amenaza en la seccion 3). Hoy la identidad del agente en cada
evento es un string que escribe el runtime: ningun actor distinto del runtime sostiene la afirmacion de
autoria. Con esta pieza, el runtime pasa de testigo unico a archivero - almacena y ordena, pero no puede
fabricar lo que los agentes no firmaron.
