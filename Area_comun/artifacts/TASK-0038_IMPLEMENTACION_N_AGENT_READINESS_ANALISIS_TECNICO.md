> **UNIFICADO** en `Area_comun/artifacts/ANALISIS-TASK-0038-n-agent-consolidado.md` (analisis de record, 2026-06-06). Este documento se conserva como fuente autoral.

# TASK-0038 — Implementación N-Agent Readiness

**Documento nuevo para implementación**  
**Fecha:** 2026-06-06  
**Alcance:** análisis técnico crítico de la propuesta original y de las enmiendas propuestas.  
**Excluido:** evaluación legal, financiera, operativa comercial y reputacional.  
**Objetivo:** convertir la propuesta en una especificación implementable para lanzar y mantener software con agentes, pruebas, guardrails, handoffs y decisiones auditables.

---

## 1. Veredicto técnico honesto

La propuesta original está bien encaminada porque identifica correctamente que el problema no es “añadir más agentes”, sino generalizar el protocolo alrededor de capacidades, ownership, routing, revisión independiente y gates. El diseño también acierta al tratar `owner`, `from`, `to` y `response_owner` como identificadores libres, y al localizar el bloqueo duro en el `enum` estático de `runtime/turn_schema.json`.

Sin embargo, la propuesta original no está lista para implementación robusta en N agentes reales. Está demasiado centrada en compatibilidad y generalización del roster, pero no cierra suficientemente la semántica de concurrencia, fairness, fallos de QA, reintentos, colas, límites de autonomía, observabilidad, seguridad de herramientas ni auditoría de artefactos. En un sistema repetible de lanzamiento y mantenimiento de software con agentes, esos huecos no son accesorios: son el núcleo de confiabilidad.

Las enmiendas propuestas son técnicamente pertinentes. Señalan los cuatro puntos que realmente podrían romper el sistema en producción: cuello de botella del escritor único, sesgo de routing lexicográfico, ausencia de máquina de estados para fallos de QA y saturación del operador humano. Mi evaluación es que esas enmiendas deben incorporarse, pero no como “temas de debate”; deben transformarse en decisiones de diseño cerradas, verificables y testeables.

**Decisión recomendada:** aprobar la dirección general de TASK-0038, pero bloquear la implementación hasta que `SPEC-0038` y `DECISION-0015` incluyan explícitamente los algoritmos de concurrencia, routing, QA failure, escalado humano, observabilidad, trazabilidad, guardrails y supply chain.

---

## 2. Diagnóstico de la propuesta original

### 2.1 Puntos sólidos

La propuesta original tiene una base correcta por estas razones:

1. **Define agentes por capacidades, no por nombres.** Esto evita que el protocolo quede acoplado a `Claude`, `Codex` u otro agente concreto.
2. **Mantiene compatibilidad hacia atrás.** El fallback de tres niveles permite usar `agent_registry`, `agent_roles` existente o la tríada por defecto.
3. **Introduce revisión independiente.** El principio `review-by-not-author` es obligatorio si se pretende que un sistema multiagente tenga valor real y no sea autoaprobación automatizada.
4. **Propone QA como gate de primera clase.** Esto corrige el error típico de confundir “review” con “verificación de aceptación”.
5. **Descompone la implementación en subtareas pequeñas.** El orden `registry → schema/validate/router/apply → scaffolding/docs` es razonable.
6. **Reconoce que el cambio del `enum` debe moverse a validación semántica.** Esto es correcto: el esquema debe validar forma; el runtime debe validar identidad contra el registry.

### 2.2 Huecos técnicos críticos

Los huecos principales son estos:

1. **El escritor único M2 se trata como garantía suficiente.** Un lock evita corrupción de estado, pero no garantiza throughput, fairness ni recuperación ante colisiones.
2. **El desempate lexicográfico es determinista, pero operacionalmente injusto.** En N agentes, asignará carga de forma sesgada y puede convertir a un agente en cuello de botella permanente.
3. **El QA gate no define transición de fallo.** Sin una tabla de estados explícita, aparecerán bucles entre implementación, review y QA.
4. **El escalado humano está sobredimensionado.** Un humano debe intervenir en decisiones de política, riesgo o ambigüedad de producto, no en cada imposibilidad temporal de routing.
5. **No se define un event log canónico.** Sin historial inmutable de turnos, decisiones, artefactos y transiciones, la auditoría queda incompleta.
6. **No hay modelo explícito de observabilidad.** Para operar agentes se necesita trazabilidad por `run_id`, `task_id`, `agent_id`, `attempt_id`, `handoff_id` y `artifact_id`.
7. **No se definen guardrails por tipo de acción.** No es igual redactar un archivo, ejecutar tests, tocar configuración, abrir un PR, modificar producción o lanzar una acción con efectos laterales.
8. **No se define supply chain del software generado por agentes.** Si el sistema lanza software, debe producir evidencias: SBOM, provenance, test evidence, commit metadata y release notes.

---

## 3. Principios técnicos que deben regir la implementación

### 3.1 Capacidades antes que roles fijos

El registry debe modelar capacidades, no personas ni marcas de modelo. Un agente puede tener varias capacidades, pero cada acción debe requerir una capacidad explícita.

Capacidades mínimas:

- `architect`
- `orchestrator`
- `implementer`
- `reviewer`
- `qa`
- `security_reviewer`
- `release_manager`
- `human_owner`

Capacidades opcionales útiles:

- `docs_writer`
- `test_engineer`
- `migration_engineer`
- `frontend_engineer`
- `backend_engineer`
- `database_engineer`
- `devops_engineer`

### 3.2 Estado como contrato, no como texto libre

El sistema debe funcionar como una máquina de estados finita. Cada transición debe tener:

- estado origen;
- evento;
- guard conditions;
- agente autorizado;
- estado destino;
- evidencia obligatoria;
- política de reintento;
- política de escalado.

### 3.3 Event log inmutable + snapshot derivado

El estado actual (`PROJECT_STATE`, `TASK_INDEX` o equivalente) debe tratarse como snapshot derivado. La fuente de verdad debe ser un log append-only de eventos.

Eventos mínimos:

- `task.created`
- `task.claimed`
- `task.started`
- `artifact.produced`
- `handoff.created`
- `review.requested`
- `review.approved`
- `review.rejected`
- `qa.requested`
- `qa.passed`
- `qa.failed`
- `decision.proposed`
- `decision.approved`
- `decision.rejected`
- `release.candidate_created`
- `release.published`
- `escalation.created`
- `escalation.resolved`

### 3.4 Determinismo reproducible, no determinismo simplista

El sistema debe ser reproducible, pero no por orden lexicográfico puro. La selección debe ser determinista a partir del estado, pero balanceada.

Regla recomendada:

```text
score(agent, task) =
  active_claims(agent) * 10
+ pending_reviews(agent) * 6
+ pending_qa(agent) * 6
+ cooldown_penalty(agent)
- capability_affinity(agent, task)
- priority_bonus(task)
```

Criterio de selección:

1. filtrar agentes `enabled`;
2. filtrar por capacidad requerida;
3. excluir autores cuando aplique revisión o QA;
4. excluir agentes con `active_claims >= max_active_claims`;
5. ordenar por `score` ascendente;
6. desempatar por `stable_hash(task_id + transition + agent_id + routing_epoch)`;
7. usar lexicográfico solo como último desempate estable.

Esto conserva replay determinista si `routing_epoch`, estado y registry son iguales, pero evita que `Claude`, `Agent_Alpha` u otro identificador inicial absorba siempre la carga.

### 3.5 Humano como gate de decisión, no como catch-all operativo

El operador humano debe intervenir cuando existe una decisión real:

- cambio incompatible;
- excepción a política;
- aprobación de release;
- aceptación de riesgo técnico;
- conflicto entre agentes que el arquitecto no puede resolver;
- acción irreversible o sensible;
- ambigüedad de requerimiento.

No debe intervenir por:

- falta temporal de agente libre;
- colisión normal de lock;
- primer fallo de QA;
- primer fallo de review;
- retry agotable por runtime.

---

## 4. Diseño objetivo recomendado

### 4.1 `agent_registry` extendido

La propuesta original de registry debe ampliarse con límites de concurrencia, afinidad, confianza y política de herramientas.

```json
{
  "agent_registry": {
    "enabled": true,
    "routing_policy": "weighted_least_loaded_deterministic",
    "agents": [
      {
        "id": "Claude",
        "capabilities": ["architect", "reviewer", "orchestrator", "qa"],
        "adapter": "llm",
        "enabled": true,
        "max_active_claims": 2,
        "trust_boundary": "internal_llm",
        "tool_policy": "restricted_write",
        "review_policy": {
          "can_review_own_work": false
        }
      },
      {
        "id": "Codex",
        "capabilities": ["implementer", "test_engineer"],
        "adapter": "llm",
        "enabled": true,
        "max_active_claims": 3,
        "trust_boundary": "internal_llm",
        "tool_policy": "sandboxed_write"
      },
      {
        "id": "operador humano",
        "capabilities": ["human_owner"],
        "adapter": "human",
        "enabled": true,
        "max_active_claims": 1,
        "trust_boundary": "human"
      }
    ]
  }
}
```

Campos recomendados:

| Campo | Uso |
|---|---|
| `id` | Identificador estable del agente. |
| `capabilities` | Capacidades disponibles para routing. |
| `adapter` | Tipo de integración: `llm`, `human`, `cli`, `service`. |
| `enabled` | Permite retirar un agente sin borrar historial. |
| `max_active_claims` | Límite de concurrencia por agente. |
| `trust_boundary` | Clasifica superficie de riesgo. |
| `tool_policy` | Define permisos de lectura/escritura/ejecución. |
| `review_policy.can_review_own_work` | Debe ser `false` salvo modo degradado explícito. |

### 4.2 Validación de turnos

La modificación del schema debe hacerse así:

```json
"agent": {
  "type": "string",
  "minLength": 1
}
```

Y la validación semántica debe ejecutarse en `turn_validate.py`:

```text
validate_turn(report):
  registry = load_agent_registry(root)
  assert report.agent in registry.enabled_agent_ids
  assert report.transition in allowed_transitions
  assert report.agent has capability required by transition
  assert report.artifacts exist when transition requires evidence
  assert report.decision_refs exist when transition changes contract
```

El cambio puede ser SemVer MINOR si el schema no se considera contrato público consumido por terceros estrictos. Si algún consumidor externo validaba explícitamente el `enum`, entonces el cambio puede ser breaking para ese consumidor y debería registrarse como Major o como Minor con periodo de compatibilidad doble.

### 4.3 Concurrencia: M2 no debe ser el punto de entrada de todos los agentes

El escritor único debe mantenerse, pero los agentes no deberían escribir directamente el snapshot compartido. Deben emitir reportes/intentions append-only y dejar que el orquestador aplique transiciones.

Modelo recomendado:

```text
Agente -> turn_report append-only -> validator -> orchestrator queue -> M2 writer -> snapshot
```

Esto reduce colisiones porque los agentes no compiten directamente por el archivo/estado central.

#### Política de colisión

Cuando M2 detecte versión obsoleta:

1. rechazar la aplicación de la transición;
2. recargar snapshot actual;
3. recomputar elegibilidad;
4. reintentar con exponential backoff + jitter determinista;
5. registrar evento `state.apply_conflict`;
6. si supera `max_apply_retries`, escalar al `orchestrator`, no al humano.

Parámetros iniciales:

```json
{
  "concurrency": {
    "state_apply_mode": "single_writer_with_intent_queue",
    "max_apply_retries": 5,
    "base_backoff_ms": 250,
    "max_backoff_ms": 5000,
    "jitter": "deterministic_seeded",
    "lease_seconds": 1800,
    "stale_claim_policy": "reclaim_after_lease_expired"
  }
}
```

### 4.4 Claims con lease

Cada claim debe tener lease y versión.

```json
{
  "task_id": "TASK-0038-d",
  "owner": "Codex",
  "capability": "implementer",
  "claim_id": "claim-20260606-0001",
  "attempt_id": "attempt-001",
  "state_version": 42,
  "claimed_at": "2026-06-06T15:00:00Z",
  "lease_until": "2026-06-06T15:30:00Z",
  "status": "claimed"
}
```

Reglas:

- Un claim vencido no se borra; se marca `expired`.
- Un claim vencido puede ser reclamado por otro agente elegible.
- Si el agente original vuelve tarde, su reporte se rechaza por `state_version` obsoleta.
- Todo rechazo debe quedar en event log.

---

## 5. Máquina de estados recomendada

### 5.1 Estados mínimos

```text
proposed
ready
claimed
in_progress
submitted
in_review
changes_requested
review_approved
qa_pending
qa_failed
done
blocked
escalated
cancelled
```

### 5.2 Transiciones principales

| Origen | Evento | Destino | Actor | Evidencia requerida |
|---|---|---|---|---|
| `proposed` | `approve_scope` | `ready` | `architect` / `human_owner` | DECISION/SPEC aprobada |
| `ready` | `claim` | `claimed` | capacidad requerida | claim con lease |
| `claimed` | `start` | `in_progress` | owner | turn report |
| `in_progress` | `submit` | `submitted` | owner | artifacts + test evidence |
| `submitted` | `request_review` | `in_review` | orchestrator | reviewer asignado |
| `in_review` | `approve_review` | `review_approved` | reviewer ≠ author | review notes |
| `in_review` | `reject_review` | `changes_requested` | reviewer ≠ author | defect log |
| `review_approved` | `request_qa` | `qa_pending` | orchestrator | test_plan |
| `qa_pending` | `pass_qa` | `done` | qa ≠ author | QA evidence |
| `qa_pending` | `fail_qa` | `qa_failed` | qa ≠ author | failed checks |
| `qa_failed` | `assign_fix` | `claimed` | orchestrator | defect log + attempt++ |
| `changes_requested` | `assign_fix` | `claimed` | orchestrator | review notes + attempt++ |
| cualquier | `escalate` | `escalated` | orchestrator/architect | reason + exhausted policy |

### 5.3 Regla para fallo de QA

Cuando QA falla:

1. generar evento `qa.failed` con checks fallidos;
2. crear `defect_log` asociado al `attempt_id`;
3. mover tarea a `qa_failed`;
4. reasignar preferentemente al autor original si sigue habilitado y tiene capacidad;
5. si el autor original no está disponible, enrutar a otro implementador elegible;
6. incrementar `qa_attempts`;
7. si `qa_attempts > max_qa_attempts`, escalar al `architect` para rediseño;
8. solo escalar al humano si el arquitecto marca `requires_human_decision`.

Parámetros iniciales:

```json
{
  "quality_policy": {
    "max_review_cycles": 3,
    "max_qa_cycles": 3,
    "escalate_to_architect_before_human": true,
    "allow_self_review": false,
    "allow_self_qa": false
  }
}
```

### 5.4 Evitar bucles infinitos

El sistema debe cortar bucles por contador de ciclos y por firma del fallo.

Regla adicional:

```text
Si el mismo check falla 2 veces consecutivas con la misma firma, bloquear reasignación automática y enviar a architect_review.
```

Esto evita que un implementador y QA repitan el mismo ciclo sin rediseñar la solución.

---

## 6. Routing recomendado

### 6.1 Algoritmo

```python
def select_agent(task, transition, registry, state):
    required = required_capability(task, transition)
    candidates = [a for a in registry.agents if a.enabled]
    candidates = [a for a in candidates if required in a.capabilities]

    if transition in ["review", "qa"]:
        candidates = [a for a in candidates if a.id != task.author]

    candidates = [a for a in candidates if active_claims(a.id, state) < a.max_active_claims]

    if not candidates:
        return route_to_orchestrator_or_architect(task, transition)

    return min(
        candidates,
        key=lambda a: (
            load_score(a.id, state, task),
            stable_hash(task.id + transition + a.id + state.routing_epoch),
            a.id
        )
    )
```

### 6.2 Criterios de carga

`active_claims` no basta. Hay que sumar trabajo pendiente por tipo:

```text
load_score =
  10 * active_claims
+ 6  * pending_reviews
+ 6  * pending_qa
+ 4  * open_fix_cycles
+ cooldown_penalty
- capability_affinity
```

### 6.3 Desempate lexicográfico

El desempate lexicográfico debe quedar solo como último recurso. Usarlo como criterio principal es técnicamente pobre porque produce sesgo permanente.

---

## 7. Guardrails técnicos

### 7.1 Clasificación por tipo de acción

| Tipo de acción | Ejemplo | Gate recomendado |
|---|---|---|
| Lectura | leer archivos, consultar contexto | automático con logging |
| Escritura local | modificar `.md`, tests, código local | sandbox + diff obligatorio |
| Ejecución local | correr tests/scripts | sandbox + allowlist de comandos |
| Cambio de contrato | schema, API pública, migraciones | DECISION + review + QA |
| Acción externa | push, release, deploy | human approval o release manager |
| Acción sensible | credenciales, producción, borrados | human approval obligatorio |

### 7.2 Guardrails mínimos

- Validación de entrada del task/handoff.
- Validación de salida del agente antes de aplicar cambios.
- Validación de herramientas por allowlist.
- Revisión de diffs antes de merge.
- Bloqueo de self-review y self-QA.
- Registro de prompts/instrucciones relevantes cuando afecten decisiones técnicas.
- Detección de drift entre SPEC, DECISION, código y tests.
- Validación de artefactos obligatorios antes de cerrar tarea.

---

## 8. Handoffs

Un handoff debe ser autocontenido, verificable y trazable.

Formato mínimo:

```json
{
  "handoff_id": "handoff-0038-d-001",
  "from": "Claude",
  "to": "Codex",
  "task_id": "TASK-0038-d",
  "required_capability": "implementer",
  "objective": "Implement routing by weighted least-loaded deterministic policy",
  "inputs": ["SPEC-0038", "DECISION-0015"],
  "constraints": ["no self-review", "preserve fallback 2-agent behavior"],
  "acceptance_criteria": [
    "existing router golden tests pass unchanged",
    "new fairness tests pass",
    "reviewer never equals author"
  ],
  "expected_artifacts": ["code diff", "tests", "test evidence"],
  "return_to": "orchestrator"
}
```

Regla: ningún handoff puede depender de memoria implícita del agente anterior.

---

## 9. Observabilidad y auditoría técnica

### 9.1 Identificadores obligatorios

Cada ejecución debe propagar:

- `run_id`
- `task_id`
- `turn_id`
- `agent_id`
- `attempt_id`
- `claim_id`
- `handoff_id`
- `artifact_id`
- `decision_id`
- `trace_id`

### 9.2 Spans recomendados

- `agent.plan`
- `agent.handoff`
- `agent.tool_call`
- `state.validate_turn`
- `state.apply_transition`
- `router.select_agent`
- `review.evaluate`
- `qa.execute_test_plan`
- `release.build`
- `release.attest`

### 9.3 Métricas mínimas

| Métrica | Para qué sirve |
|---|---|
| `agent.active_claims` | detectar saturación |
| `router.assignment_count` | detectar sesgo de routing |
| `state.apply_conflicts` | medir cuello de botella M2 |
| `qa.failure_rate` | detectar baja calidad de implementación |
| `review.rejection_rate` | detectar drift o instrucciones malas |
| `handoff.missing_context_rate` | medir calidad de handoffs |
| `human.escalation_count` | detectar embudo humano |
| `release.rollback_count` | medir estabilidad |

### 9.4 Auditoría mínima por tarea cerrada

Para cerrar una tarea como `done`, deben existir:

- SPEC o requerimiento fuente;
- DECISION si hubo cambio de contrato;
- autor;
- reviewer distinto del autor;
- QA distinto del autor cuando exista test plan;
- evidencia de tests;
- lista de artefactos generados;
- diff o referencia al commit;
- trazas o run logs;
- resultado de gates.

---

## 10. Supply chain y release engineering

Si el sistema va a lanzar y mantener software, debe producir evidencias de cadena de suministro.

Requisitos mínimos:

1. **SBOM** por release, preferiblemente CycloneDX.
2. **Build provenance** por artefacto, alineado con SLSA.
3. **Commit firmado o trazable** con autoría del agente/humano que generó el cambio.
4. **Test evidence** anexada al release candidate.
5. **Release checklist** con gates cumplidos.
6. **Rollback plan** por release.
7. **Changelog** generado desde eventos/decisiones, no redactado manualmente desde memoria.

---

## 11. Plan de implementación recomendado

### Fase 0 — Congelamiento de diseño

Entregables:

- `DECISION-0015-n-agent-registry-y-capacidades.md`
- `SPEC-0038-n-agent-registry.md`
- tabla de estados;
- política de routing;
- política de concurrencia;
- política de QA failure;
- política de escalado humano;
- test plan cerrado.

Condición de salida:

- aprobación humana del diseño;
- sin cambios de código todavía.

### Fase 1 — Registry y validación semántica

Cambios:

- `runtime/context.py`: `load_agent_registry(root)`;
- helpers: `enabled_agents`, `agents_with_capability`, `has_capability`;
- `runtime/turn_schema.json`: `agent` pasa de `enum` a `string` con `minLength`;
- `runtime/turn_validate.py`: validación contra registry.

Tests:

- registry explícito;
- fallback desde `agent_roles`;
- fallback por defecto;
- agente no registrado falla;
- agente disabled falla;
- golden actuales intactos.

### Fase 2 — Event log, queue y leases

Cambios:

- directorio append-only para `turn_reports` o `events`;
- `state_version` en snapshot;
- claim con `lease_until`;
- orquestador aplica transiciones;
- política de reintentos con backoff + jitter determinista.

Tests:

- dos agentes intentan claim simultáneo;
- un claim vencido se reclama sin borrar historial;
- reporte tardío con versión antigua se rechaza;
- replay reconstruye snapshot.

### Fase 3 — Router balanceado y determinista

Cambios:

- `runtime/router.py`: selección por capacidad, carga, exclusión de autor y desempate estable;
- soporte de `required_capability` opcional;
- límites `max_active_claims`.

Tests:

- review nunca asigna autor;
- QA nunca asigna autor;
- distribución de 100 tareas entre 3 agentes no queda sesgada por nombre;
- replay con mismo estado produce misma asignación;
- sin candidato elegible escala a arquitecto/orquestador, no directamente al humano.

### Fase 4 — Máquina de estados Review/QA

Cambios:

- estados `changes_requested`, `qa_failed`, `review_approved`, `qa_pending`;
- counters `review_attempts`, `qa_attempts`;
- defect logs;
- corte de bucles repetidos.

Tests:

- QA fail devuelve tarea con defect log;
- segundo fallo similar dispara revisión arquitectónica;
- máximo de ciclos escala correctamente;
- tarea no puede pasar a `done` sin evidencia obligatoria.

### Fase 5 — Guardrails y permisos de herramientas

Cambios:

- `tool_policy` por agente;
- allowlist de comandos;
- side-effect gates;
- diff obligatorio antes de aplicar cambios;
- bloqueo de acciones sensibles sin aprobación.

Tests:

- agente sin permiso no ejecuta herramienta;
- cambio de contrato sin DECISION falla;
- acción sensible queda pausada.

### Fase 6 — Observabilidad

Cambios:

- trace IDs;
- spans por transición;
- métricas de routing, QA, conflicts y escalations;
- logs estructurados JSONL.

Tests:

- todo evento tiene `trace_id`;
- todo artifact puede rastrearse a task/run/agent;
- dashboard o reporte de métricas básico.

### Fase 7 — Release engineering

Cambios:

- SBOM;
- provenance/attestation;
- changelog desde eventos;
- release checklist;
- rollback plan.

Tests:

- release candidate sin SBOM falla;
- release candidate sin test evidence falla;
- release candidate sin reviewer distinto falla.

---

## 12. Test plan global

### 12.1 Unit tests

- registry resolver;
- capability matching;
- routing score;
- state transitions;
- lease expiry;
- semantic validation.

### 12.2 Contract tests

- `turn_schema` acepta agente string;
- `turn_validate` rechaza agente no registrado;
- fixtures antiguos siguen pasando.

### 12.3 Golden tests

- N=2 produce comportamiento anterior;
- N=3 permite reviewer/QA separados;
- N=5 balancea carga sin romper replay.

### 12.4 Property-based tests

Invariantes:

- ningún reviewer es autor;
- ningún QA es autor;
- una tarea `done` tiene evidencia;
- no hay dos claims activos para la misma tarea;
- todo evento aplicado incrementa `state_version`;
- replay produce el mismo snapshot.

### 12.5 Concurrency simulation

Simular:

- 10 implementadores;
- 100 tareas;
- colisiones de claim;
- vencimiento de leases;
- retries;
- agentes disabled durante ejecución;
- QA failures repetidos.

Métricas esperadas:

- conflictos registrados, no silenciosos;
- ninguna corrupción del snapshot;
- distribución de carga razonable;
- escalado humano bajo y justificado.

---

## 13. Criterios de aceptación de TASK-0038

TASK-0038 solo debe cerrarse cuando se cumpla todo lo siguiente:

1. `agent_registry` soporta N agentes configurables.
2. El sistema conserva fallback N=2 sin migración.
3. `turn_schema` ya no contiene enum rígido de agentes.
4. `turn_validate` valida agente habilitado y capacidad requerida.
5. El router asigna por capacidad, disponibilidad y carga.
6. Review y QA excluyen al autor.
7. QA failure tiene transición definida y evita bucles infinitos.
8. Los claims tienen lease y versionado.
9. Los conflictos M2 generan retry controlado y evento auditable.
10. El humano no recibe escalados operativos de primer nivel.
11. Existe event log o equivalente append-only.
12. Existe trazabilidad por run/task/agent/attempt/artifact.
13. CI ejecuta unit, contract, golden, replay y concurrency tests.
14. La documentación incluye registry, routing, estados, guardrails y handoffs.
15. La decisión de SemVer está justificada según consumidores reales del schema.

---

## 14. Cambios concretos sobre la propuesta original

| Tema | Propuesta original | Recomendación final |
|---|---|---|
| Registry | Capacidades básicas | Añadir concurrencia, tool_policy, trust_boundary y límites |
| Schema | `agent` string + validación registry | Correcto; añadir validación por capacidad de transición |
| Routing | Capacidad + lexicográfico | Weighted least-loaded determinista + hash estable + lexicográfico final |
| QA | Gate independiente | Añadir estados `qa_failed`, counters y defect logs |
| Humano | Escalado si no hay revisor | Escalar primero a orchestrator/architect; humano solo por decisión real |
| Concurrencia | Claim lock + escritor único | Intent queue + single writer + leases + retry/backoff |
| Auditoría | Gates y reportes | Event log inmutable + snapshot derivado |
| Observabilidad | No suficientemente definido | OpenTelemetry-style traces, metrics y logs estructurados |
| Release | No suficientemente definido | SBOM, provenance, release checklist, rollback |

---

## 15. Decisiones que deben quedar en `DECISION-0015`

1. Adoptar `agent_registry` como fuente de verdad de agentes y capacidades.
2. Mantener fallback de tres niveles para compatibilidad.
3. Cambiar `agent` en JSON Schema de enum a string no vacío.
4. Validar identidad y capacidad en runtime.
5. Prohibir self-review y self-QA por defecto.
6. Implementar routing weighted least-loaded determinista.
7. Mantener M2 como escritor único, pero recibir intents append-only.
8. Incorporar leases a claims.
9. Definir QA failure como transición formal.
10. Escalar a humano solo tras arquitecto/orquestador o por decisión sensible.
11. Registrar todos los cambios en event log auditable.
12. Exigir trazabilidad de artefactos y evidencia de tests.
13. Alinear release con SBOM/provenance cuando exista publicación de software.

---

## 16. Riesgos técnicos residuales

### 16.1 Riesgo: demasiada arquitectura para un protocolo pequeño

Existe riesgo de sobrediseño si el proyecto nunca supera 2 agentes. Mitigación: implementar todo config-gated y mantener fallback N=2 intacto.

### 16.2 Riesgo: complejidad del event log

Un event log añade complejidad. Mitigación: empezar con JSONL append-only y snapshot regenerable, no con infraestructura distribuida pesada.

### 16.3 Riesgo: SemVer mal clasificado

Si el schema es contrato público, quitar un enum puede romper validadores externos. Mitigación: documentar consumidores conocidos y, si existen, introducir periodo de doble compatibilidad.

### 16.4 Riesgo: routing justo pero difícil de explicar

Un score compuesto puede volverse opaco. Mitigación: registrar `routing_decision.explanation` con candidatos, scores y razón de selección.

### 16.5 Riesgo: QA gate lento

QA independiente aumenta latencia. Mitigación: activar QA obligatorio solo cuando hay `test_plan`, cambio de contrato, cambio crítico o release candidate.

---

## 17. Recomendación final

No implementaría TASK-0038 tal como está en la propuesta original. Sí implementaría una versión enmendada con las decisiones de este documento.

El camino correcto es:

1. convertir la propuesta original en `SPEC-0038`;
2. incorporar las enmiendas como decisiones cerradas, no como debate abierto;
3. aprobar `DECISION-0015`;
4. implementar en fases pequeñas;
5. validar cada fase con golden tests y replay;
6. mantener N=2 intacto hasta demostrar N=3 y N=5 con simulaciones.

La meta no debe ser “tener más agentes”. La meta debe ser tener un runtime de colaboración auditable donde cada agente actúa bajo capacidad declarada, permiso limitado, estado verificable, handoff autocontenido, revisión independiente, QA reproducible y release trazable.

---

## 18. Referencias técnicas consultadas

Estas referencias se usaron como base metodológica y técnica para el diseño:

- OpenAI Agents SDK: guardrails, handoffs, human review, tracing y observabilidad de runs.
- Model Context Protocol Specification 2025-06-18: integración estandarizada con herramientas, recursos y contexto.
- Agent2Agent Protocol: agent cards, capability discovery, task lifecycle, messages y artifacts.
- OpenTelemetry Documentation: trazas, métricas y logs como señales de observabilidad.
- Temporal Durable Execution: workflows deterministas, replay y event history.
- Semantic Versioning 2.0.0: clasificación de cambios backward-compatible y breaking changes.
- JSON Schema: uso de `enum` para conjuntos cerrados y validación estructural.
- OWASP Top 10 for LLM Applications 2025 y OWASP Agentic AI Threats and Mitigations: amenazas técnicas en aplicaciones LLM/agénticas.
- SLSA: controles de integridad y provenance para cadena de suministro de software.
- CycloneDX: estándar BOM/SBOM/AI-BOM para transparencia de componentes.
