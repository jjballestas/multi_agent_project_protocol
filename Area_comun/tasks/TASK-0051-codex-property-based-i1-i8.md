---
id: TASK-0051
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-06
updated_at: 2026-06-06
depends_on: [TASK-0049, TASK-0050]
relates_to: [TASK-0044]
phase: P2
spec_id: Area_comun/specs/SPEC-0038-n-agent-registry.md
linked_decisions: [DECISION-0015]
execution_pipeline: [nuevo harness examples/runtime_property_cases/run_runtime_property_cases.py que GENERA DETERMINISTICAMENTE muchos estados variados (enumeracion por construccion o seed FIJO derivado del indice; sin Math.random ni reloj) y comprueba para cada uno los invariantes I1-I8 reutilizando runtime.router/turn_validate/eventlog reales; agregar el runner al workflow .github/workflows/validate.yml; sin tocar runtime/]
acceptance_criteria: [para todo estado generado se cumplen: I1 ningun reviewer es autor; I2 ningun QA es autor; I3 done tiene evidencia; I4 no hay dos claims activos por tarea; I5 todo evento aplicado incrementa seq y aggregate_version; I6 replay reconstruye el mismo snapshot (hash canonico); I7 todo evento aplicado esta atribuido/autenticado (actor presente); I8 ningun intent se aplica dos veces (idempotencia); el harness es DETERMINISTA y reproducible (mismo conjunto de muestras en cada corrida); declara cuantas muestras genera y como (sin truncamiento silencioso); reutiliza el runtime real (no reimplementa invariantes); aditivo (no modifica runtime/ ni contrato ni golden existentes); sin red]
test_plan: [run_runtime_property_cases nuevo que itere sobre N muestras deterministas (documentar N) cubriendo: rosters N=2/3/5, transiciones review/qa/execute, claims (incluido intento de doble claim activo), secuencias de eventos en el event log (incluido intent duplicado por reintento). Cada invariante I1-I8 con su asercion. Reportar PASS con conteo de muestras y, si alguna falla, el estado/seed que la rompe (contraejemplo reproducible). Correr ademas TODA la suite runtime (no-regresion) + validador/encoding/neutralidad py + YAML del workflow]
closure_criteria: [harness runtime_property_cases verde sobre las muestras deterministas declaradas (I1-I8) + agregado al CI; contraejemplos reproducibles si algo falla; fallback N=2 sin regresion (suite runtime completa verde); aditivo (solo examples/ + .github/workflows); determinista/reproducible; neutralidad limpia; handoff autocontenido; claim liberado al pasar a in_review]
---

# TASK-0051 - Capa A.3: property-based de invariantes I1-I8

> `implementation` -> SDD. Cubre el **test plan global 15.4** de SPEC-0038 (property-based de los
> invariantes I1-I8). Aditivo (solo tests + CI), determinista/reproducible, fallback N=2 intacto.

## Contexto

Hoy los invariantes I1-I8 se prueban con golden puntuales (router, review_qa, eventlog, N=3/N=5). Falta el
nivel **property-based**: generar muchos estados variados y comprobar que los invariantes se mantienen en
TODOS. Como el resto del runtime es determinista (sin reloj/red/random), el property testing aqui se hace
con GENERACION DETERMINISTA (enumeracion por construccion o seed fijo derivado del indice), no con azar, de
modo que cada corrida produce exactamente el mismo conjunto de muestras (reproducible y apto para CI).

## Invariantes a comprobar (SPEC-0038 sec.15.4)

- I1: ningun reviewer es autor. I2: ningun QA es autor.
- I3: `done` tiene evidencia. I4: no hay dos claims activos por la misma tarea.
- I5: todo evento aplicado incrementa `seq` y `aggregate_version`.
- I6: replay reconstruye el mismo snapshot (hash canonico).
- I7: todo evento aplicado esta atribuido/autenticado (actor presente).
- I8: ningun intent se aplica dos veces (idempotencia).

## Alcance

- Nuevo harness `examples/runtime_property_cases/run_runtime_property_cases.py` que:
  - genera deterministicamente un conjunto declarado de estados (rosters N=2/3/5; transiciones
    review/qa/execute; claims incl. intento de doble-claim; secuencias de eventos incl. intent duplicado);
  - para cada muestra, comprueba I1-I8 reutilizando `runtime.router`, `runtime.turn_validate` y
    `runtime.eventlog` REALES (no reimplementar la logica de invariantes);
  - reporta PASS con el numero de muestras; si alguna falla, imprime el estado/seed (contraejemplo
    reproducible).
- Agregar el runner al workflow `.github/workflows/validate.yml`.

## Restricciones

- **Aditivo**: NO modificar `runtime/` ni el contrato ni los golden existentes; solo el nuevo harness + CI.
- **Determinista/reproducible**: sin `Math.random`/azar/reloj; mismas muestras en cada corrida.
- **Sin red**; sin secretos; **neutralidad de dominio** intacta.
- **Sin truncamiento silencioso**: declarar cuantas muestras se generan y la cobertura; si se acota, decirlo.
- Handoff autocontenido; claim liberado al pasar a `in_review`.

## Nota de secuencia (Capa A)

Tras A.3 quedan en Capa A: A.4 (concurrency simulation: 10 impl/100 tareas/colisiones de claim/vencimiento
de leases/agentes disabled mid-exec/intents duplicados) y A.7 (SemVer del schema). Fase B (writer-vivo del
estado de protocolo) y Fase 5 siguen GATEADAS: NO arrancar.
