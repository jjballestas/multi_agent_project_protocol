---
id: TASK-0040
owner: Claude
status: ready
type: documentation
priority: normal
created_at: 2026-06-06
updated_at: 2026-06-06
depends_on: [TASK-0039]
relates_to: [TASK-0036]
phase: P2
spec_id: none
linked_decisions: [DECISION-0009]
objective: Ejecutar y registrar la PRIMERA CORRIDA REAL del runtime sobre el repo vivo (self-run del orquestador con invoker subproceso real), aprobada por el operador, dejando evidencia auditable.
expected_output: Un artefacto en Area_comun/artifacts/ escrito por un subproceso externo invocado por el orquestador y commiteado por el motor M1 en main; esta tarea cerrada ready->done por el propio turno del runtime.
question_to_resolve: El runtime (enabled + --allow-real-invoker + --llm-command + --once) cierra una tarea real sobre la instancia viva con 1 commit gateado?
closure_criterion: El orquestador completa 1 turno real sobre el repo vivo (trace gate_pre..commit), escribe el artefacto, mueve TASK-0040 a done, libera el claim y produce 1 commit en main; gates verdes.
---

# TASK-0040 - Primera corrida real del runtime sobre el repo vivo (self-run)

> `documentation` (SDD ligero). Vehiculo controlado para la PRIMERA CORRIDA REAL del runtime sobre la
> instancia viva (DECISION-0009 decision #2), aprobada por el operador. La cierra el PROPIO runtime via
> el invoker subproceso real; el motor M1 commitea en main.

## Intencion
Demostrar end-to-end, sobre el repo vivo (no smoke en temporal), que el runtime con invoker REAL:
enabled + `--adapter llm --llm-invoker subprocess --allow-real-invoker --llm-command <cmd> --once`
cierra una tarea con 1 commit gateado (apply -> gate -> commit M1). El "agente" detras del subproceso es
un proceso externo (vendor fuera de alcance, DECISION-0009 #1); lo que se prueba son los rieles reales
sobre la instancia viva.

## Deliverable
- `Area_comun/artifacts/RUNTIME-live-selfrun-20260606.md` (escrito por el subproceso, commiteado por M1).

## Nota de proceso (hallazgo)
El commit del runtime corre el pre-commit hook de poda (`prune --check`); cerrar una tarea libera un
claim y puede cruzar el umbral `released_count > 4`. Para esta corrida se archivo 1 released (hot 4->3)
de modo que post-turno queden 4 (no dispara). Fix de raiz (runtime commit consciente del hook / poda como
turno de mantenimiento) queda como follow-up.
