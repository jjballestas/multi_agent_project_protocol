---
id: TASK-0050
owner: Codex
status: ready
type: implementation
priority: high
created_at: 2026-06-06
updated_at: 2026-06-06
depends_on: [TASK-0045, TASK-0049]
relates_to: [TASK-0043]
phase: P2
spec_id: Area_comun/specs/SPEC-0038-n-agent-registry.md
linked_decisions: [DECISION-0015]
execution_pipeline: [nuevo harness examples/runtime_nagent_golden_cases/run_runtime_nagent_golden_cases.py que arma estados sinteticos con agent_registry de N=3 y N=5 y ejercita runtime.router.select_next/select_agent + la maquina Review/QA; N=3 verifica reviewer/QA separados del autor; N=5 verifica balanceo de carga determinista y replay identico; agregar el runner al workflow .github/workflows/validate.yml; sin tocar runtime/ (solo tests)]
acceptance_criteria: [N=3: con registry de 3 agentes de capacidades distintas (p.ej. implementer-autor, reviewer, qa), una tarea in_review se enruta a un reviewer != autor y una qa_pending a un qa != autor, ambos distintos del autor (I1/I2 end-to-end con roster real); N=5: con registry de 5 agentes elegibles, el router weighted-least-loaded distribuye la carga de forma determinista y un segundo select_next sobre el mismo estado/routing_epoch produce ASIGNACION IDENTICA (replay determinista, sin romper); fallback N=2 byte-equivalente (los golden runtime existentes siguen verdes); el harness es determinista (sin reloj/red/random); aditivo (no se modifica runtime/ ni contrato ni fixtures existentes)]
test_plan: [run_runtime_nagent_golden_cases nuevo con al menos: (1) N=3 review->reviewer!=autor; (2) N=3 qa->qa!=autor; (3) N=3 sin reviewer/qa elegible distinto del autor => escalate (no self-review); (4) N=5 distribucion de carga determinista entre 5 elegibles; (5) N=5 replay: select_next x2 mismo estado => identico; correr ademas TODA la suite runtime (router 10/10 etc.) para confirmar no-regresion; validador/encoding/neutralidad py; YAML del workflow valido]
closure_criteria: [harness runtime_nagent_golden_cases verde (N=3 reviewer/QA separados + N=5 balanceo determinista + replay identico) + agregado al CI; fallback N=2 sin regresion (suite runtime completa verde); aditivo (solo examples/ + .github/workflows); neutralidad limpia; handoff autocontenido; claim liberado al pasar a in_review]
---

# TASK-0050 - Capa A.2: golden N=3 y N=5

> `implementation` -> SDD. Cubre el criterio del **test plan global 15.3** de SPEC-0038: "N=2 reproduce
> comportamiento anterior; N=3 permite reviewer/QA separados; N=5 balancea carga sin romper replay".
> Aditivo (solo tests + CI), fallback N=2 intacto. Determinista.

## Contexto

El nucleo N-agente (Fases 1-4) esta implementado y el hardening I1/I2 (A.6) cerrado. Hoy las suites prueban
sobre todo N=2 (fallback) y casos puntuales N=3 en router/review_qa. Falta el golden explicito de
multi-agente N=3 y N=5 que demuestra la propiedad central del diseno: con un roster real de 3 agentes,
review y QA se asignan a agentes DISTINTOS del autor (I1/I2 end-to-end); con 5 agentes, el router balancea
carga de forma determinista y el replay reproduce las mismas asignaciones.

## Alcance

- Nuevo harness `examples/runtime_nagent_golden_cases/run_runtime_nagent_golden_cases.py` (Python,
  determinista, sin red/reloj/random) que:
  - **N=3:** arma `agent_registry` de 3 agentes con capacidades distintas y verifica via
    `runtime.router.select_next`/`select_agent` que `in_review` -> reviewer != autor y `qa_pending` -> qa !=
    autor (ambos != autor); y que sin reviewer/qa elegible distinto del autor => `escalate` (no self-review).
  - **N=5:** arma `agent_registry` de 5 agentes elegibles y verifica que el router weighted-least-loaded
    distribuye la carga y que `select_next` x2 sobre el mismo estado/`routing_epoch` produce asignacion
    IDENTICA (replay determinista).
- Agregar el runner nuevo al workflow `.github/workflows/validate.yml` (como en TASK-0047).

## Restricciones

- **Aditivo**: NO modificar `runtime/` ni el contrato ni los fixtures/golden existentes; solo agregar el
  nuevo harness y su step de CI.
- **Fallback N=2 byte-equivalente**: toda la suite runtime existente sigue verde.
- **Determinismo**: sin red, sin reloj real, sin random (varia por construccion del estado, no por azar).
- **Neutralidad de dominio** intacta; sin secretos.
- Handoff autocontenido; claim liberado al pasar a `in_review`.

## Nota de secuencia (Capa A)

Tras A.2 quedan en Capa A: A.3 (property-based I1-I8), A.4 (concurrency simulation: 10 impl/100 tareas/
leases/disabled mid-exec/intents duplicados), A.7 (SemVer del schema). Fase B (writer-vivo del estado de
protocolo) y Fase 5 siguen GATEADAS: NO arrancar.
