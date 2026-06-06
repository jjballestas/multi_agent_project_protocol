---
id: TASK-0052
owner: Codex
status: ready
type: implementation
priority: high
created_at: 2026-06-06
updated_at: 2026-06-06
depends_on: [TASK-0050, TASK-0051]
relates_to: [TASK-0044]
phase: P2
spec_id: Area_comun/specs/SPEC-0038-n-agent-registry.md
linked_decisions: [DECISION-0015]
execution_pipeline: [nuevo harness examples/runtime_concurrency_cases/run_runtime_concurrency_cases.py que simula DETERMINISTICAMENTE (sin random/reloj/red; por construccion/seed fijo) 10 implementadores y 100 tareas reutilizando el runtime real (router/eventlog/turn_validate), inyectando colisiones de claim, vencimiento de leases + re-claim con fencing, agentes disabled a mitad de ejecucion e intents duplicados por reintento; agregar el runner al workflow .github/workflows/validate.yml; sin tocar runtime/]
acceptance_criteria: [la simulacion (10 implementadores, 100 tareas) corre determinista y reproducible (mismas semillas => mismo resultado; sin random/reloj/red); (1) los conflictos quedan REGISTRADOS y NO son silenciosos: doble-claim sobre una tarea => uno gana y el otro queda rechazado/visible; fencing obsoleto tras re-claim => rechazo registrado; (2) el snapshot del event log NO se corrompe: replay reconstruye el mismo hash canonico / assert_snapshot_matches pasa al final; (3) la distribucion de carga entre los 10 implementadores queda dentro del fairness_ratio configurado; (4) CERO doble-aplicaciones (idempotencia: ningun intent se aplica dos veces, ni siquiera con reintentos); agentes disabled a mitad NO reciben nuevas asignaciones; aditivo (no modifica runtime/ ni contrato ni golden existentes); declara tamano de simulacion y semillas]
test_plan: [run_runtime_concurrency_cases nuevo: escenario 10x100 determinista que ejercita colisiones de claim, expiracion de lease + re-claim con fencing creciente, disable de un agente a mitad, y reenvio de intents duplicados. Aserciones: conflictos contados y visibles (no silenciosos); assert_snapshot_matches / replay hash al final; ratio de carga max/min dentro de fairness_ratio; conteo de aplicaciones == intents unicos (cero doble-aplicacion). Reportar metricas (asignaciones por agente, conflictos, rechazos por fencing, dedups) y contraejemplo/semilla si falla. Correr ademas TODA la suite runtime (no-regresion) + validador/encoding/neutralidad py + YAML]
closure_criteria: [harness runtime_concurrency_cases verde (conflictos registrados, snapshot sin corrupcion, fairness dentro de umbral, cero doble-aplicaciones) + agregado al CI; metricas y semillas declaradas; fallback N=2 sin regresion (suite runtime completa verde); aditivo (solo examples/ + .github/workflows); determinista/reproducible; neutralidad limpia; handoff autocontenido; release ATOMICO al pasar a in_review (mensaje + flip claim/status juntos, DECISION-0018)]
---

# TASK-0052 - Capa A.4: concurrency simulation

> `implementation` -> SDD. Cubre el **test plan global 15.5** de SPEC-0038 (concurrency simulation).
> Aditivo (solo tests + CI), determinista/reproducible, fallback N=2 intacto.

## Contexto

Cerradas A.5/A.1/A.6/A.2/A.3, el ultimo gran golden del test plan global es la **simulacion de
concurrencia**: estresar el control-plane (claims/leases/fencing/idempotencia) y el router (fairness) bajo
muchos agentes y tareas, demostrando que los conflictos se registran sin corromper el estado ni
doble-aplicar. Como el runtime es determinista, la simulacion se hace por construccion/seed fijo (sin
azar), reproducible en CI.

## Escenario (SPEC-0038 sec.15.5)

10 implementadores, 100 tareas, con inyeccion determinista de:
- colisiones de claim (dos agentes intentan la misma tarea);
- vencimiento de leases + re-claim con `fencing_token` creciente;
- agentes `disabled` a mitad de ejecucion;
- intents duplicados por reintento.

## Resultado esperado (aserciones)

1. **Conflictos registrados, no silenciosos:** doble-claim => uno gana, el otro rechazo visible; fencing
   obsoleto => rechazo registrado (state.stale_fencing_rejected o equivalente).
2. **Sin corrupcion del snapshot:** replay reconstruye el mismo hash canonico / `assert_snapshot_matches`
   pasa al final.
3. **Distribucion dentro de `fairness_ratio`:** carga max/min entre implementadores dentro del umbral.
4. **Cero doble-aplicaciones:** aplicaciones == intents unicos; idempotencia se mantiene con reintentos.
   Agentes disabled a mitad no reciben nuevas asignaciones.

## Restricciones

- **Aditivo**: NO modificar `runtime/` ni el contrato ni los golden existentes; solo el nuevo harness + CI.
- **Determinista/reproducible**: sin `Math.random`/azar/reloj; declarar tamano y semillas; contraejemplo
  reproducible si falla.
- **Sin red**; sin secretos; **neutralidad de dominio** intacta.
- Handoff autocontenido; **release ATOMICO** al pasar a `in_review` (mensaje in-review + liberar claim +
  flip status, juntos en el mismo turno; DECISION-0018).

## Nota de secuencia (Capa A)

Tras A.4 queda en Capa A: A.7 (SemVer del schema de turno). Con A.4 cerrada, el test plan global 15.3-15.5
queda cubierto. Fase B (writer-vivo del estado de protocolo) y Fase 5 siguen GATEADAS: NO arrancar.
