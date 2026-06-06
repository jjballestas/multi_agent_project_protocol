> **PROMOVIDO** a `Area_comun/specs/SPEC-0038-n-agent-registry.md` (spec de record, 2026-06-06).
> Este artefacto se conserva como origen autoral. La fuente normativa es la copia en `specs/`.

# SPEC-0038 — Runtime de colaboración N-Agente (especificación consolidada e implementable)

**Tipo:** Especificación técnica autocontenida.
**Fecha:** 2026-06-06
**Estado:** Borrador para congelar como `SPEC-0038` + `DECISION-0015`.
**Origen:** consolida la propuesta TASK-0038 con las correcciones críticas (P0/P1/P2) de la revisión independiente, ya incorporadas como decisiones cerradas.
**Autocontenida:** este documento no requiere leer ningún otro para implementarse. Donde una decisión cierra un punto, se marca como **[D-n]** y se recoge en §17.

> Regla rectora: la meta no es "tener más agentes", sino un **runtime de colaboración auditable** donde cada agente actúa bajo capacidad declarada, identidad autenticada, permiso limitado, estado verificable, handoff autocontenido, revisión independiente, QA reproducible y release trazable.

---

## 1. Propósito y alcance

Generalizar el protocolo de 2 agentes (Claude/Codex/humano) a **N agentes configurables**, manteniendo compatibilidad total con el comportamiento actual N=2 sin migración. El sistema debe permitir lanzar y mantener software con agentes, con pruebas, guardrails, handoffs y decisiones auditables.

**En alcance:** modelo de agentes y capacidades, máquina de estados, event log como fuente de verdad, concurrencia, routing, guardrails y seguridad, handoffs, observabilidad, presupuesto de coste, validación de turnos, plan de implementación y tests.

**Fuera de alcance (de este documento):** lógica de dominio/negocio (el núcleo permanece neutral), y la decisión estratégica de *si* conviene ir a N agentes (se asume decidida).

**Invariantes globales** (verificadas por property tests, §15.4):

- I1: ningún `reviewer` es el autor de la tarea revisada.
- I2: ningún `qa` es el autor de la tarea verificada.
- I3: una tarea en `done` tiene evidencia obligatoria completa (§5.2, §10.4).
- I4: no existen dos claims activos para la misma tarea.
- I5: todo evento aplicado incrementa la secuencia global y la versión de su aggregate.
- I6: replay del log reconstruye el mismo snapshot.
- I7: todo evento aplicado es atribuible a una identidad autenticada. **[D-1]**
- I8: ningún intent se aplica dos veces (idempotencia por `idempotency_key`). **[D-2]**

---

## 2. Modelo de agentes y capacidades

### 2.1 Capacidades antes que roles fijos **[D-3]**

El registry modela **capacidades**, no personas ni marcas de modelo. Un agente puede tener varias capacidades; cada acción requiere una capacidad explícita.

Capacidades mínimas: `architect`, `orchestrator`, `implementer`, `reviewer`, `qa`, `security_reviewer`, `release_manager`, `human_owner`.

Opcionales: `docs_writer`, `test_engineer`, `migration_engineer`, `frontend_engineer`, `backend_engineer`, `database_engineer`, `devops_engineer`.

### 2.2 `agent_registry` extendido (fuente de verdad de agentes) **[D-3][D-5]**

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
        "tool_policy_ref": "policy.restricted_write",
        "auth": { "method": "hmac_signed", "key_id": "claude-2026" },
        "review_policy": { "can_review_own_work": false }
      },
      {
        "id": "Codex",
        "capabilities": ["implementer", "test_engineer"],
        "adapter": "llm",
        "enabled": true,
        "max_active_claims": 3,
        "trust_boundary": "internal_llm",
        "tool_policy_ref": "policy.sandboxed_write",
        "auth": { "method": "hmac_signed", "key_id": "codex-2026" }
      },
      {
        "id": "operador humano",
        "capabilities": ["human_owner"],
        "adapter": "human",
        "enabled": true,
        "max_active_claims": 1,
        "trust_boundary": "human",
        "auth": { "method": "session_token" }
      }
    ]
  }
}
```

| Campo | Uso |
|---|---|
| `id` | Identificador estable. |
| `capabilities` | Capacidades disponibles para routing. |
| `adapter` | `llm`, `human`, `cli`, `service`. |
| `enabled` | Retirar un agente sin borrar historial. |
| `max_active_claims` | Límite de concurrencia por agente. |
| `trust_boundary` | Clasifica superficie de riesgo; liga a política efectiva (§8). |
| `tool_policy_ref` | Referencia a una política de herramientas con allowlist (§8.4). |
| `auth` | **[D-1]** Mecanismo de autenticación/firma de los reportes del agente. |
| `review_policy.can_review_own_work` | `false` salvo modo degradado explícito. |

### 2.3 Compatibilidad hacia atrás (fallback de tres niveles) **[D-4]**

Resolución del roster, en orden: (1) `agent_registry` explícito; (2) `agent_roles` existente; (3) tríada por defecto Claude/Codex/humano. N=2 debe producir comportamiento idéntico al actual sin migración.

---

## 3. Máquina de estados

El sistema funciona como una **máquina de estados finita**. Cada transición declara: estado origen, evento, guard conditions, capacidad/actor autorizado, estado destino, evidencia obligatoria, política de reintento, política de escalado.

### 3.1 Estados

```text
proposed  ready  claimed  in_progress  submitted  in_review
changes_requested  review_approved  qa_pending  qa_failed
done  blocked  escalated  cancelled
```

### 3.2 Transiciones

| Origen | Evento | Destino | Actor | Evidencia requerida |
|---|---|---|---|---|
| `proposed` | `approve_scope` | `ready` | `architect` / `human_owner` | DECISION/SPEC aprobada |
| `ready` | `claim` | `claimed` | capacidad requerida | claim con lease + fencing |
| `claimed` | `start` | `in_progress` | owner | turn report |
| `in_progress` | `submit` | `submitted` | owner | artifacts + test evidence |
| `submitted` | `request_review` | `in_review` | orchestrator | reviewer asignado (≠ autor) |
| `in_review` | `approve_review` | `review_approved` | reviewer ≠ autor | review notes |
| `in_review` | `reject_review` | `changes_requested` | reviewer ≠ autor | defect log |
| `review_approved` | `request_qa` | `qa_pending` | orchestrator | test_plan |
| `qa_pending` | `pass_qa` | `done` | qa ≠ autor | QA evidence completa |
| `qa_pending` | `fail_qa` | `qa_failed` | qa ≠ autor | failed checks |
| `qa_failed` | `assign_fix` | `claimed` | orchestrator | defect log + attempt++ |
| `changes_requested` | `assign_fix` | `claimed` | orchestrator | review notes + attempt++ |
| cualquiera | `escalate` | `escalated` | orchestrator/architect | reason + política agotada |

### 3.3 Regla de fallo de QA **[D-9]**

Al fallar QA: (1) emitir `qa.failed` con checks fallidos; (2) crear `defect_log` asociado al `attempt_id`; (3) mover a `qa_failed`; (4) reasignar preferentemente al autor original si sigue habilitado y con capacidad; (5) si no, enrutar a otro implementador elegible; (6) incrementar `qa_attempts`; (7) si `qa_attempts > max_qa_cycles`, escalar al `architect` para rediseño; (8) escalar al humano solo si el arquitecto marca `requires_human_decision`.

**Corte de bucles:** si el mismo check falla 2 veces consecutivas con la **misma firma**, bloquear reasignación automática y enviar a `architect_review`.

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

### 3.4 Escalado humano **[D-10]**

El humano interviene solo ante **decisión real**: cambio incompatible, excepción a política, aprobación de release, aceptación de riesgo técnico, conflicto irresoluble por el arquitecto, acción irreversible/sensible, ambigüedad de requerimiento. **No** interviene por: falta temporal de agente libre, colisión normal de lock, primer fallo de QA, primer fallo de review, retry agotable por runtime.

---

## 4. Event log como fuente de verdad **[D-11]**

El estado actual (`PROJECT_STATE`, `TASK_INDEX`, `CLAIMS`) es un **snapshot derivado**. La fuente de verdad es un **log append-only de eventos**.

### 4.1 Garantías del log **[D-7 (P1)]**

- **Secuencia global monótona:** cada evento lleva `seq` entero estrictamente creciente; el orden total lo define `seq`, no el archivo.
- **Append atómico:** un evento se escribe completo o no se escribe (escritura a tmp + rename, o fsync por línea); el lector ignora líneas truncadas (torn-write safe).
- **Esquema versionado:** cada evento lleva `event_schema_version`; los lectores soportan versiones previas.
- **Snapshot + compactación:** el snapshot se regenera por replay; se persiste un snapshot cada N eventos con `up_to_seq`, y el replay parte del último snapshot válido. El log no se borra; se compacta a archivos por rango de `seq`.

### 4.2 Eventos mínimos

```text
task.created  task.claimed  task.started  artifact.produced
handoff.created  review.requested  review.approved  review.rejected
qa.requested  qa.passed  qa.failed
decision.proposed  decision.approved  decision.rejected
release.candidate_created  release.published
escalation.created  escalation.resolved
state.apply_conflict
```

### 4.3 Forma del evento

```json
{
  "seq": 1043,
  "event_schema_version": "1.0",
  "type": "review.approved",
  "task_id": "TASK-0038-d",
  "aggregate_version": 7,
  "actor": "Claude",
  "actor_auth": { "method": "hmac_signed", "key_id": "claude-2026", "sig": "..." },
  "trace_id": "run-2026-0606-..-001",
  "idempotency_key": "claude:TASK-0038-d:review.approved:attempt-002",
  "payload": { "review_notes_ref": "..." },
  "ts": "2026-06-06T15:10:00Z"
}
```

---

## 5. Concurrencia: escritor único con cola de intents, leases, fencing e idempotencia

### 5.1 Modelo **[D-7]**

Los agentes **no escriben** el snapshot compartido. Emiten **intents append-only** que un orquestador valida y aplica.

```text
Agente -> turn_report/intent (append-only) -> validator -> orchestrator queue -> M2 writer -> snapshot
```

### 5.2 Versión por-aggregate, no global **[D-2 (P0)]**

Cada tarea (aggregate) tiene su propia `aggregate_version`. El check optimista de concurrencia se hace **por tarea**, no contra una versión global del snapshot. Esto evita falsos conflictos entre tareas que no se tocan y permite escalar a N agentes sin contención artificial.

### 5.3 Idempotencia **[D-2 (P0)]**

Todo intent lleva `idempotency_key` (p. ej. `actor:task_id:transition:attempt_id`). El writer mantiene un índice de claves aplicadas; un intent con clave ya aplicada se **ignora silenciosamente y se confirma como éxito** (no se re-aplica). Esto neutraliza la doble-aplicación bajo reintentos con backoff.

### 5.4 Política de colisión

Cuando el writer detecta `aggregate_version` obsoleta: (1) rechazar la aplicación; (2) recargar snapshot de esa tarea; (3) recomputar elegibilidad; (4) reintentar con exponential backoff + jitter determinista; (5) registrar `state.apply_conflict`; (6) si supera `max_apply_retries`, escalar al `orchestrator`, no al humano.

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

### 5.5 Claims con lease y fencing token **[D-8 (P0)]**

Cada claim tiene lease, `aggregate_version` y **fencing token** monótono.

```json
{
  "task_id": "TASK-0038-d",
  "owner": "Codex",
  "capability": "implementer",
  "claim_id": "claim-20260606-0001",
  "attempt_id": "attempt-001",
  "aggregate_version": 42,
  "fencing_token": 8821,
  "claimed_at": "2026-06-06T15:00:00Z",
  "lease_until": "2026-06-06T15:30:00Z",
  "status": "claimed"
}
```

Reglas: un claim vencido no se borra, se marca `expired`; puede ser reclamado por otro agente elegible (con `fencing_token` mayor); el writer **rechaza toda escritura con `fencing_token` menor que el vigente** (protege ante el "proceso pausado"); todo rechazo queda en event log.

---

## 6. Routing determinista balanceado **[D-6]**

### 6.1 Algoritmo

```python
def select_agent(task, transition, registry, state):
    required = required_capability(task, transition)
    candidates = [a for a in registry.agents if a.enabled]
    candidates = [a for a in candidates if required in a.capabilities]
    if transition in ["review", "qa"]:
        candidates = [a for a in candidates if a.id != task.author]   # I1, I2
    candidates = [a for a in candidates
                  if active_claims(a.id, state) < a.max_active_claims]
    if not candidates:
        return route_to_orchestrator_or_architect(task, transition)   # nunca al humano directo
    return min(candidates, key=lambda a: (
        load_score(a.id, state, task),
        stable_hash(task.id + transition + a.id + state.routing_epoch),
        a.id))   # lexicográfico SOLO como último desempate
```

### 6.2 Score de carga (pesos configurables, no constantes en código)

```text
load_score = 10*active_claims + 6*pending_reviews + 6*pending_qa
           + 4*open_fix_cycles + cooldown_penalty - capability_affinity
```

Los pesos viven en config (`routing_weights`), no hardcodeados, para poder calibrarlos. Cada selección emite `routing_decision.explanation` con candidatos, scores y razón.

### 6.3 Fairness como gate de CI **[D-6 (P2)]**

Métrica `routing.fairness_ratio = max_assignments / min_assignments` sobre una ventana. Test obligatorio: distribuir 100 tareas entre 3 agentes idénticos no debe sesgarse por nombre (`fairness_ratio` dentro de umbral). El desempate lexicográfico nunca es criterio principal.

---

## 7. Frontera de determinismo **[D-12 (P1)]**

Distinción explícita y obligatoria:

- **Orquestador determinista:** la lógica de routing, transiciones y aplicación de estado es determinista a partir de `(routing_epoch, estado, registry, eventos)`. Mismo input → mismo snapshot.
- **Actividad de agente NO determinista:** la salida de un LLM, una llamada a herramienta o a red **no** es determinista. Se trata como *actividad* cuyo resultado se **graba como evento** en el log.

Regla: **todo lo que toca el mundo exterior (LLM, herramienta, red, reloj, aleatoriedad) es un evento registrado; el resto es lógica determinista.** En replay, el sistema **reconstruye estado desde los eventos grabados; no re-invoca agentes.** Por tanto "replay determinista" aplica a las transiciones de estado, no a re-correr modelos. Los tests de replay (§15.4) deben verificar exactamente esto y nada más.

---

## 8. Guardrails y seguridad

### 8.1 Autenticación y atribución de eventos **[D-1 (P0)]**

Todo `turn_report`/evento debe ir **firmado o autenticado** según `agent.auth`. La validación semántica:

```text
validate_turn(report):
  registry = load_agent_registry(root)
  verify_signature(report, registry[report.agent].auth)   # [D-1] rechaza si no atribuible
  assert report.agent in registry.enabled_agent_ids
  assert report.idempotency_key not already_applied        # [D-2]
  assert report.transition in allowed_transitions
  assert report.agent has capability required by transition
  assert report.aggregate_version == current(task)         # [D-2] optimista por-tarea
  assert report.artifacts exist when transition requires evidence
  assert report.decision_refs exist when transition changes contract
```

Un evento sin firma válida se **rechaza y se registra** como `security.unauthenticated_event`. La auditoría exige atribución: sin esto, el log inmutable no vale (I7).

### 8.2 Defensa de handoffs contra inyección **[D-1 (P0)]**

Los handoffs y task inputs son **superficie de inyección** (goal/instruction hijacking, OWASP Agentic). Mitigaciones obligatorias: separar instrucciones de datos (el contenido del handoff no se ejecuta como instrucción de sistema); validar/sanear payloads contra patrones de inyección; `trust_boundary` del emisor determina el nivel de confianza aplicado a su contenido; cualquier acción sensible disparada desde contenido de handoff requiere gate de §8.3.

### 8.3 Clasificación por tipo de acción

| Tipo de acción | Ejemplo | Gate |
|---|---|---|
| Lectura | leer archivos, contexto | automático con logging |
| Escritura local | `.md`, tests, código local | sandbox + diff obligatorio |
| Ejecución local | correr tests/scripts | sandbox + allowlist de comandos |
| Cambio de contrato | schema, API pública, migraciones | DECISION + review + QA |
| Acción externa | push, release, deploy | human approval o release manager |
| Acción sensible | credenciales, producción, borrados | human approval obligatorio |

### 8.4 Tool policy con allowlist **[D-13 (P2)]**

`tool_policy_ref` apunta a una política con **allowlist por-herramienta** atada a capacidad + scope de tarea (no un enum grueso). Un agente sin permiso para una herramienta no la ejecuta; queda registrado.

### 8.5 Guardrails mínimos

Validación de entrada de task/handoff; validación de salida del agente antes de aplicar; allowlist de herramientas; revisión de diffs antes de merge; bloqueo de self-review/self-QA; registro de prompts/instrucciones que afecten decisiones técnicas; detección de drift entre SPEC/DECISION/código/tests; validación de artefactos obligatorios antes de cerrar tarea.

---

## 9. Handoffs autocontenidos

```json
{
  "handoff_id": "handoff-0038-d-001",
  "from": "Claude",
  "to": "Codex",
  "task_id": "TASK-0038-d",
  "required_capability": "implementer",
  "objective": "Implement routing by weighted least-loaded deterministic policy",
  "inputs": ["SPEC-0038", "DECISION-0015"],
  "constraints": ["no self-review", "preserve fallback N=2 behavior"],
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

## 10. Observabilidad, presupuesto y auditoría

### 10.1 Identificadores obligatorios

`run_id`, `task_id`, `turn_id`, `agent_id`, `attempt_id`, `claim_id`, `handoff_id`, `artifact_id`, `decision_id`, `trace_id`.

### 10.2 Métricas mínimas

| Métrica | Para qué |
|---|---|
| `agent.active_claims` | saturación |
| `router.assignment_count` / `router.fairness_ratio` | sesgo de routing (gate CI) |
| `state.apply_conflicts` | contención de concurrencia |
| `qa.failure_rate` | calidad de implementación |
| `review.rejection_rate` | drift o instrucciones malas |
| `handoff.missing_context_rate` | calidad de handoffs |
| `human.escalation_count` | embudo humano |
| `release.rollback_count` | estabilidad |
| `run.cost_tokens` / `run.wall_clock` | presupuesto (§10.3) |

### 10.3 Presupuesto de coste y terminación **[D-14 (P1)]**

Cada tarea y cada run tienen presupuesto de coste (tokens) y `deadline`. Al agotarse cualquiera, la tarea se mueve a `escalated` con razón `budget_exhausted` (no se queda en bucle válido consumiendo recursos). Los cortes de ciclo (§3.3) y el presupuesto son límites independientes y complementarios.

### 10.4 Auditoría mínima para cerrar `done`

SPEC/requerimiento fuente; DECISION si hubo cambio de contrato; autor; reviewer ≠ autor; QA ≠ autor cuando hay test plan; evidencia de tests; lista de artefactos; diff/referencia al commit; trazas/run logs; resultado de gates; **todos los eventos atribuibles y firmados** (I7).

---

## 11. Supply chain y release (diferido/condicionado) **[D-15 (sobre-diseño)]**

Estos requisitos aplican **solo cuando una instancia efectivamente publica software** (binarios/artefactos). Para el repo del protocolo (Markdown + JSON, sin publicación de binarios), quedan **diferidos** hasta que exista un pipeline de release real, para no pagar complejidad sin un release que la justifique.

Cuando aplique: SBOM por release (CycloneDX); build provenance por artefacto (SLSA); commit firmado/trazable con autoría; test evidence anexa al release candidate; release checklist con gates; **rollback como pasos de compensación (saga), no solo plan en prosa** [D-16 (P2)]; changelog generado desde eventos/decisiones.

---

## 12. Validación de turnos (schema + semántica)

Schema (`runtime/turn_schema.json`): `agent` pasa de `enum` rígido a:

```json
"agent": { "type": "string", "minLength": 1 }
```

La identidad y capacidad se validan **en runtime** (`turn_validate.py`, §8.1), no en el schema. **SemVer [D-...]:** si el schema no es contrato público consumido por terceros que validen el `enum`, el cambio es MINOR; si algún consumidor externo valida el `enum`, es breaking para ese consumidor y requiere Major o un periodo de doble compatibilidad documentado.

---

## 13. Plan de implementación por fases

**Fase 0 — Congelar diseño.** Entregables: `DECISION-0015`, esta `SPEC-0038`, tabla de estados, políticas (routing, concurrencia, QA failure, escalado, **auth de eventos**, **idempotencia/fencing**, **presupuesto**), test plan cerrado. Salida: aprobación humana; sin código todavía.

**Fase 1 — Registry y validación semántica.** `runtime/context.py: load_agent_registry`; helpers `enabled_agents`, `agents_with_capability`, `has_capability`; schema `agent` enum→string; `turn_validate.py` con verificación de firma (D-1), idempotencia (D-2), capacidad y versión por-tarea. Tests: registry explícito, fallback `agent_roles`, fallback por defecto, agente no registrado/disabled falla, **evento no firmado falla**, golden actuales intactos.

**Fase 2 — Event log, cola, leases, fencing, idempotencia.** Log append-only con `seq` monótono y append atómico; `aggregate_version` por tarea; claim con `lease_until` + `fencing_token`; orquestador aplica transiciones; índice de `idempotency_key`; backoff + jitter determinista; snapshot/compactación. Tests: claim simultáneo de dos agentes; claim vencido reclamado sin borrar historial; reporte tardío con versión/fencing obsoleto se rechaza; **intent reintentado no se aplica dos veces**; replay reconstruye snapshot.

**Fase 3 — Router balanceado.** `runtime/router.py`: capacidad, carga, exclusión de autor, desempate estable; `required_capability` opcional; `max_active_claims`; pesos en config; `routing_decision.explanation`. Tests: review/QA nunca asignan autor; 100 tareas entre 3 agentes sin sesgo por nombre (**fairness gate**); replay con mismo estado → misma asignación; sin candidato → arquitecto/orquestador, no humano.

**Fase 4 — Máquina de estados Review/QA.** Estados `changes_requested`, `qa_failed`, `review_approved`, `qa_pending`; counters `review_attempts`, `qa_attempts`; defect logs; corte de bucles por firma. Tests: QA fail devuelve tarea con defect log; segundo fallo similar dispara revisión arquitectónica; máximo de ciclos escala; no se llega a `done` sin evidencia.

**Fase 5 — Guardrails y permisos (condicionado a necesidad real).** `tool_policy` con allowlist por-herramienta; side-effect gates; diff obligatorio; bloqueo de acciones sensibles sin aprobación; defensa de inyección en handoffs. Tests: agente sin permiso no ejecuta; cambio de contrato sin DECISION falla; acción sensible pausada; payload de handoff malicioso contenido.

**Fase 6 — Observabilidad y presupuesto (condicionado).** trace IDs; spans por transición; métricas de routing/QA/conflicts/escalations/coste; logs JSONL; **presupuesto y deadline** por tarea/run. Tests: todo evento tiene `trace_id`; todo artifact rastreable a task/run/agent; tarea que agota presupuesto escala.

**Fase 7 — Release engineering (diferido hasta release real).** SBOM, provenance/attestation, changelog desde eventos, release checklist, rollback como saga. Tests: release sin SBOM/test evidence/reviewer distinto falla.

---

## 14. Reglas de secuenciación y proporcionalidad

Fases 0–4 son el **núcleo proporcionado**: deben implementarse completas. Fases 5–7 son **condicionadas**: se activan cuando exista superficie real (acciones externas con efecto, publicación de binarios). Todo debe ir **config-gated** y conservar **fallback N=2 intacto** hasta demostrar N=3 y N=5 por simulación. Esto contiene el riesgo de sobre-diseño.

---

## 15. Test plan global

### 15.1 Unit
registry resolver; capability matching; routing score; state transitions; lease expiry; **fencing rejection**; **idempotency dedupe**; **signature verification**; semantic validation.

### 15.2 Contract
`turn_schema` acepta `agent` string; `turn_validate` rechaza agente no registrado, no firmado y con versión obsoleta; fixtures antiguos siguen pasando.

### 15.3 Golden
N=2 reproduce comportamiento anterior; N=3 permite reviewer/QA separados; N=5 balancea carga sin romper replay.

### 15.4 Property-based (invariantes I1–I8)
ningún reviewer es autor; ningún QA es autor; `done` tiene evidencia; no hay dos claims activos por tarea; todo evento aplicado incrementa `seq` y `aggregate_version`; replay reconstruye el mismo snapshot; todo evento aplicado está autenticado; ningún intent se aplica dos veces.

### 15.5 Concurrency simulation
10 implementadores, 100 tareas, colisiones de claim, vencimiento de leases, retries, agentes disabled durante ejecución, QA failures repetidos, **intents duplicados por reintento**. Esperado: conflictos registrados (no silenciosos); sin corrupción del snapshot; distribución de carga dentro de `fairness_ratio`; escalado humano bajo y justificado; cero doble-aplicaciones.

---

## 16. Criterios de aceptación

1. `agent_registry` soporta N agentes configurables.
2. Conserva fallback N=2 sin migración.
3. `turn_schema` sin enum rígido de agentes.
4. `turn_validate` valida agente habilitado, **firma/atribución**, capacidad y **versión por-tarea**.
5. Router asigna por capacidad, disponibilidad y carga, con **fairness gate**.
6. Review y QA excluyen al autor (I1, I2).
7. QA failure tiene transición definida y evita bucles infinitos.
8. Claims con lease, versión y **fencing token**.
9. Conflictos generan retry controlado y evento auditable; **idempotencia garantizada** (I8).
10. El humano no recibe escalados operativos de primer nivel.
11. Existe event log append-only con `seq` monótono, esquema versionado y snapshot/compactación.
12. Trazabilidad por run/task/agent/attempt/artifact; **todos los eventos autenticados** (I7).
13. Presupuesto de coste/deadline por tarea y run con escalado al agotarse.
14. CI ejecuta unit, contract, golden, replay y concurrency tests.
15. Frontera de determinismo documentada y verificada (orquestador vs actividad de agente).
16. Documentación incluye registry, routing, estados, guardrails, seguridad y handoffs.
17. Decisión de SemVer justificada según consumidores reales del schema.

---

## 17. Decisiones cerradas (para `DECISION-0015`)

- **[D-1]** Autenticar/firmar todo `turn_report` y evento; rechazar lo no atribuible (P0).
- **[D-2]** Idempotency key por intent + concurrencia optimista por-aggregate (P0).
- **[D-3]** `agent_registry` modela capacidades; cada acción requiere capacidad explícita.
- **[D-4]** Fallback de tres niveles para compatibilidad N=2.
- **[D-5]** Registry extendido: `max_active_claims`, `trust_boundary`, `tool_policy_ref`, `auth`.
- **[D-6]** Routing weighted least-loaded determinista + hash estable + lexicográfico final + fairness gate.
- **[D-7]** M2 como escritor único que recibe intents append-only; log con `seq`/esquema/compactación.
- **[D-8]** Leases con fencing token monótono; rechazo de escrituras con fencing menor.
- **[D-9]** QA failure como transición formal con corte de bucles por firma.
- **[D-10]** Escalar a humano solo tras arquitecto/orquestador o por decisión sensible.
- **[D-11]** Event log inmutable como fuente de verdad; snapshot derivado.
- **[D-12]** Frontera de determinismo explícita: efecto externo = evento grabado; replay no re-invoca agentes.
- **[D-13]** Tool policy con allowlist por-herramienta atada a capacidad + scope.
- **[D-14]** Presupuesto de coste y deadline por tarea/run.
- **[D-15]** Supply chain (SBOM/SLSA) diferida hasta release real.
- **[D-16]** Rollback de release como pasos de compensación (saga).
- Prohibir self-review y self-QA por defecto.
- Cambiar `agent` de enum a string no vacío; validar identidad y capacidad en runtime.

---

## 18. Riesgos residuales

- **Sobre-diseño** si nunca se supera N=2 → mitigación: config-gated + fallback N=2 + fases 5–7 condicionadas.
- **Complejidad del event log** → mitigación: empezar con JSONL + snapshot regenerable, no infraestructura distribuida.
- **SemVer mal clasificado** → mitigación: documentar consumidores; doble compatibilidad si los hay.
- **Routing opaco** → mitigación: `routing_decision.explanation` + fairness gate.
- **QA lento** → mitigación: QA obligatorio solo con `test_plan`, cambio de contrato, cambio crítico o release candidate.
- **Coste de firma/auth** → mitigación: HMAC simple por agente, no PKI pesada, en la fase inicial.

---

## 19. Referencias técnicas

OpenAI Agents SDK (guardrails, handoffs, human review, tracing); MCP Specification 2025-06-18; A2A (agent cards, capability discovery, task lifecycle, agentes autenticados); OpenTelemetry (trazas, métricas, logs); Temporal Durable Execution (workflows deterministas, replay, event history); event sourcing para agentes autónomos (ESAA); lease + fencing tokens (concurrencia distribuida); Semantic Versioning 2.0.0; JSON Schema; OWASP Top 10 for LLM Applications 2025 y OWASP Top 10 for Agentic Applications (dic-2025); SLSA (provenance); CycloneDX v1.7 (SBOM/ML-BOM/AI-BOM).
