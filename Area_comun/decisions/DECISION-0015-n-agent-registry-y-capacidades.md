---
decision_id: DECISION-0015
title: Registry de agentes por capacidades y runtime sin roles fijos (N-agente, modelo de equipo)
status: proposed
date: 2026-06-06
ratified_at: null
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0009, DECISION-0001, DECISION-0011, DECISION-0007, DECISION-0006]
phase: P2
---

# DECISION-0015 - Registry de agentes por capacidades y runtime sin roles fijos (N-agente)

> Estado: PROPOSED (2026-06-06). Diseno pedido por el operador (analisis de la tarea futura TASK-0038,
> modelo objetivo = "equipo de desarrollo competente"). **Requiere aprobacion humana** antes de
> implementar. Aditivo, off-by-default, backward-compat; se deriva SPEC-0038 + sub-tareas. NO se toca
> codigo con esta decision; solo fija el contrato objetivo y los invariantes.

## Contexto
El protocolo se autogestiona (dogfooding) y hoy esta cableado a **2 agentes** (`Claude`=arquitecto,
`Codex`=implementador, `operador humano`=dueno). Los fallos que el dogfooding a 2 agentes expuso
(colisiones en estado compartido, drift de status, stalls, mensajes olvidados) escalan
combinatoriamente con 3+. Hallazgo que acota el alcance: el grueso del protocolo **ya es
agente-agnostico** -el validador trata `owner` como string libre (sin enum), el mailbox `from`/`to`/
`response_owner` son strings libres, lifecycle/claims-por-fila/gates validan invariantes de estado, no
nombres. El **unico bloqueador duro** es el `enum` del campo `agent` en `runtime/turn_schema.json`
(lo aplica jsonschema en `turn_validate.py`). El resto son defaults blandos (router/apply/prune) o
plantillas/docs.

Escalar a N agentes por tanto NO es repensar el protocolo: es **terminar los rieles estructurales** (claim
= lock + escritor unico del orquestador, ya en su sitio tras M1/M2, DECISION-0009/0011) y **generalizar
roster + ruteo + revision**.

## Modelo conceptual (equipo de desarrollo competente)
Un equipo competente se define por **capacidades, ownership y gates**, no por nombres fijos:
- **Arquitecto/tech lead** (direccion, descomposicion, coherencia, neutralidad; SDD).
- **Implementadores (N, especializados)** (1 work item = 1 owner; trabajo pequeno verificable).
- **Revisor peer** -> invariante **review-by-not-author** (el revisor nunca es el autor).
- **QA/test** -> gate de calidad **independiente** de quien implemento (verifica acceptance/test_plan).
- **Orquestador** (asigna por capacidad + disponibilidad; ruteo determinista; escritor unico).
- **Dueno humano** (prioridades, aprobaciones, breaking changes; gate humano explicito).

El protocolo actual es el **caso degenerado N=2**: arquitecto+revisor+QA+orquestador colapsados en
`Claude`, implementador = `Codex`. El diseno generaliza ese colapso a un equipo configurable.

## Decision (nucleo)
Se adopta el **modelo de equipo completo** para N agentes, aditivo y backward-compat:

1. **Capacidades, no nombres.** Un **agent registry** config-driven describe el equipo: cada agente =
   `{id, capabilities[], adapter, enabled}`. Capacidades reservadas que el runtime entiende:
   `architect, implementer, reviewer, qa, orchestrator, human_owner`. `id` sigue siendo string libre
   (mismo convenio que `owner`/`agent`/`from`/`to`). Capacidades extra neutrales permitidas; las
   desconocidas se ignoran (forward-compat).
2. **Fallback de 3 niveles (corazon de la compatibilidad):** (a) usar `agent_registry` si esta presente;
   (b) si no, sintetizar la triada desde el `agent_roles` existente; (c) si no hay config (fixtures/
   golden), triada por defecto cableada. Instancias y golden actuales pasan **sin migracion**.
3. **Contrato de turno generalizado.** El campo `agent` de `turn_schema.json` deja de ser `enum` y pasa a
   `string` validado **semanticamente** contra el registry en `turn_validate.py` (debe ser un `id`
   registrado y `enabled`). Relajar un enum a string-validado-contra-registry es backward-compatible (todo
   report antes valido sigue valido).
4. **Review-by-not-author (invariante de calidad).** El ruteo de revision elige un agente con capacidad
   `reviewer`/`architect` **distinto del autor**; si no hay elegible, **escala** (nunca auto-review).
5. **QA gate de primera clase (aditivo).** Si existe agente con capacidad `qa` y la tarea tiene
   `test_plan`, se rutea un paso de verificacion (QA != autor) antes de `done`; config-gated. Sin agente
   `qa` colapsa al ratificado unico actual (N=2).
6. **Gate humano parametrizado.** Escalar al agente con capacidad `human_owner` (fallback al literal
   `operador humano`).
7. **Ruteo por capacidad + disponibilidad (aditivo).** El router puede filtrar tareas `ready` por un
   `required_capability` **opcional** de la tarea + disponibilidad (no reclamada). Si la tarea no declara
   capacidad, usa `owner` como hoy. No rompe asignacion explicita.

## Invariantes (no negociables)
- **Backward-compat total:** instancias 2-agentes y todos los `examples/`/golden validan verde sin
  migracion. El N=2 es un caso particular del registry.
- **Determinismo:** multiples revisores/QA elegibles se ordenan lexicograficamente (si no, rompe
  replay/run-log).
- **Neutralidad de dominio:** `runtime/**` y plantillas estan en el scan; el registry no introduce
  terminos de negocio.
- **Escritor unico + claim=lock:** se mantiene (DECISION-0009/0011); es lo que hace seguro N writers.
- **No auto-review:** sin revisor elegible distinto del autor => escalada, jamas auto-aprobacion.

## Versionado (DECISION-0001)
Aditivo + off-by-default + backward-compat (relajar enum a string validado) => SemVer **MINOR**. La
publicacion MINOR la corta el arquitecto; el **cambio de contrato** (turn_schema + plantillas) y la
adopcion del modelo requieren **aprobacion humana** (esta decision).

## Consecuencias
- **Positivas:** el protocolo deja de estar atado a Claude/Codex; soporta equipos reales (N
  implementadores + revisores + QA) sin repensar el nucleo; codifica review-by-not-author y QA como
  invariantes verificables.
- **Costo:** un resolver de registry + generalizar router/turn_validate/scaffolding + golden nuevos;
  cuidar determinismo y el hueco de auto-review.

## Alternativas consideradas
- **Desbloqueo minimo** (solo registry + review-by-not-author, sin routing ni QA): descartada por el
  operador a favor del modelo de equipo completo.
- **No hacerlo / quedarse en 2 agentes:** descartada; el operador pide preparar N-agente.
- **Romper compatibilidad (enum nuevo / migracion):** descartada; debe ser aditivo (DECISION-0001).

## Deriva
SPEC-0038 (diseno + descomposicion a-g) bajo esta decision. Implementacion **diferida y triple-gateada**:
(a) tras TASK-0039 (fix Windows, mismo area runtime/); (b) aprobacion humana de esta DECISION-0015;
(c) OK puntual del operador para arrancar. TASK-0038 queda como paraguas.
