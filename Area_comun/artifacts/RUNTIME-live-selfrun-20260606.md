# Evidencia: primera corrida real del runtime sobre el repo vivo

Este archivo fue escrito por un **subproceso externo** invocado por el orquestador
(`runtime/orchestrator.py --run --adapter llm --llm-invoker subprocess --allow-real-invoker --once`) y **commiteado por el motor M1** sobre la rama `main`
de la instancia viva, cerrando TASK-0040 (ready -> done) en un solo turno gateado.

- Aprobado por el operador (2026-06-06, DECISION-0009 decision #2).
- El agente detras del subproceso es vendor-neutral (fuera de alcance, DECISION-0009 #1).
- Rieles probados sobre el repo VIVO: gate_pre -> route -> claim -> adapter -> validate ->
  human_gate -> apply -> gate_post -> commit (1 turno = 1 commit, revert en rojo).
