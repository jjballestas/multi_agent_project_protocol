---
id: TASK-0049
owner: Codex
status: ready
type: implementation
priority: high
created_at: 2026-06-06
updated_at: 2026-06-06
depends_on: [TASK-0046]
relates_to: [TASK-0048]
phase: P2
spec_id: Area_comun/specs/SPEC-0038-n-agent-registry.md
linked_decisions: [DECISION-0015]
execution_pipeline: [apply.py persiste original_author en el estado de la tarea en la 1ra asignacion/claim (si aun no existe), inmutable despues; la guarda de exclusion reviewer/QA != autor en turn_validate/review_qa lee el autor DE RECORD solo del estado (task.original_author, fallback task.owner del estado), ignorando payload.author/original_author para ese chequeo de seguridad; payload.author queda como informacion no autoritativa; ampliar examples/runtime_review_qa_cases con casos de payload.author falsificado]
acceptance_criteria: [un turno reviewer (reject_review/approve_review) o QA (pass_qa/fail_qa) cuyo agente ES el autor de record sigue siendo RECHAZADO aunque el payload declare un author distinto/falso; la guarda NO usa payload.author/original_author para decidir exclusion (solo el estado); apply persiste original_author en la 1ra asignacion y NO lo sobreescribe en transiciones posteriores (inmutable); reasignacion de fix (assign_fix) que cambia owner NO altera original_author; los casos existentes de runtime_review_qa siguen verdes; aditivo; fallback N=2 byte-equivalente; sin red; neutralidad limpia]
test_plan: [examples/runtime_review_qa_cases ampliado: (1) actor==autor-de-record con payload.author="Otro" => reject_review/pass_qa RECHAZADO (no se puede evadir mintiendo en el payload); (2) actor!=autor-de-record con payload.author=actor (intento de hacerse pasar por no-autor) => sigue evaluandose por el estado, no por el payload; (3) original_author se fija en la 1ra asignacion y persiste tras assign_fix/owner change; (4) reviewer/qa legitimo (distinto del autor de record) => aceptado; toda la suite runtime verde + validador/encoding/neutralidad py]
closure_criteria: [original_author de record persistido por apply en la 1ra asignacion (inmutable); guarda de exclusion reviewer/QA lee solo del estado; payload.author ignorado para el chequeo de seguridad; golden ampliado verde (incl. payload falsificado rechazado) + suite completa + gates py; fallback N=2 sin regresion; neutralidad limpia; handoff autocontenido; claim liberado al pasar a in_review]
---

# TASK-0049 - Capa A.6: autor-de-record desde el estado (hardening I1/I2)

> `implementation` -> SDD. Cierra el HALLAZGO de seguridad de la review de Fase 4 (TASK-0046). Aditivo,
> fallback intacto. Endurece los invariantes I1/I2 (review/QA != autor) frente a un actor adversarial.

## Contexto (el hallazgo)

En la ratificacion de la Fase 4 (TASK-0046) se detecto que la guarda de exclusion de autor usa
`task_author(task, payload)`, que **prioriza `payload.author`/`payload.original_author` sobre el estado**
(runtime/review_qa.py). Para una guarda de SEGURIDAD (I1/I2: "ningun reviewer/QA es el autor"), confiar en
un dato controlado por el propio actor es debil: el autor real podria declarar un `payload.author` falso y
**evadir** el rechazo de self-review/self-QA. Riesgo nulo hoy (actores de buena fe, replay/recorded), pero
debe cerrarse antes de operar agentes no confiables (es el dominio de seguridad de la Fase 5, adelantado
aqui como hardening de bajo riesgo).

## Alcance

1. **Autor de record en el estado:** `apply.py` persiste `original_author` en el estado de la tarea en la
   **primera asignacion/claim** (si aun no existe). Es **inmutable** despues: las transiciones posteriores
   (incluido `assign_fix` que cambia `owner`) NO lo sobreescriben.
2. **Guarda desde el estado:** la exclusion reviewer/QA != autor (en `turn_validate`/`review_qa`) determina
   el autor leyendo SOLO del estado: `task.original_author` (fallback `task.owner` del estado). **Ignora
   `payload.author`/`payload.original_author`** para ese chequeo de seguridad. El payload puede conservar
   `author` como informacion no autoritativa (no usada por la guarda).

## Restricciones

- **Aditivo**: los casos existentes de `runtime_review_qa` siguen verdes; fallback N=2 byte-equivalente.
- **Sin red**; sin secretos; **neutralidad de dominio** intacta.
- No tocar el alcance de otras fases; si algo obliga a salir de este alcance => `blocked` + pregunta concreta.
- Handoff autocontenido; claim liberado al pasar a `in_review`.

## Nota

Este hardening complementa el nucleo (Fases 1-4) y es parte de la consolidacion de Capa A elegida por el
operador. Tras A.6 quedan en Capa A: A.2 (golden N=3/N=5), A.3 (property-based I1-I8), A.4 (concurrency
simulation), A.7 (SemVer del schema).
