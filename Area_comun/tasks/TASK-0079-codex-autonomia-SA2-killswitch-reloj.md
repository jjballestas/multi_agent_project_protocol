---
id: TASK-0079
owner: Codex
status: done
type: implementation
priority: normal
created_at: 2026-06-08
updated_at: 2026-06-08
depends_on: [TASK-0078]
relates_to: [TASK-0038]
phase: P2
spec_id: Area_comun/specs/SPEC-0064-autonomia-supervisada.md
linked_decisions: [DECISION-0024, DECISION-0021, DECISION-0022]
execution_pipeline: [C3 kill-switch/pausa - el loop comprueba un centinela (runtime/state/PAUSE) ANTES de cada turno; si existe para con outcome=paused sin mutar estado (no auto-resume); C4 reloj de pared - caps.wall_clock_ms (determinista via clock-fixed en tests) acumula duraciones y al exceder para con outcome=wallclock_exhausted; golden examples/supervised_autonomy_cases (o nuevo) que prueban para-por-pausa y para-por-reloj con RecordedInvoker; off/sin registro byte-equivalente; paridad .ps1 + CI]
acceptance_criteria: [el loop con supervised_autonomy activo y registro valido para con outcome=paused cuando existe el centinela runtime/state/PAUSE (chequeo ANTES de cada turno, sin mutar estado); para con outcome=wallclock_exhausted al exceder caps.wall_clock_ms (determinista, clock-fixed); sin flag/registro el comportamiento es byte-equivalente; NO toca el invoker real (cerrojo --once intacto); determinista sin reloj/red; sin secretos; neutral; paridad .ps1; golden + gates verdes]
expected_output: runtime/orchestrator.py + runtime/supervised_autonomy.py (kill-switch + reloj) + golden + CI; autonomia sigue off-by-default; invoker real intacto.
test_plan: [golden: para por centinela PAUSE (antes de turno, sin mutar); para por wall_clock_ms (clock-fixed); off byte-equivalente; cerrojo real --once intacto; determinismo + paridad py/ps]
question_to_resolve: ninguna (alcance SA.2 en SPEC-0064). Forma del centinela = archivo runtime/state/PAUSE (confirmado en SPEC-0064 C3). Si se requiriera tocar el invoker real => blocked + pregunta.
closure_criterion: kill-switch (centinela PAUSE antes de cada turno -> outcome=paused, no auto-resume) + reloj de pared (caps.wall_clock_ms -> outcome=wallclock_exhausted) ejercitados con RecordedInvoker + golden + paridad .ps1; off byte-equivalente; invoker real intacto; gates verdes; handoff autocontenido; release atomico (DECISION-0018).
closure_criteria: [C3 centinela runtime/state/PAUSE chequeado antes de cada turno -> outcome=paused sin mutar estado, sin auto-resume; C4 caps.wall_clock_ms -> outcome=wallclock_exhausted determinista (clock-fixed); golden para-por-pausa y para-por-reloj con RecordedInvoker; off/sin registro byte-equivalente; invoker real --once intacto; determinista sin reloj/red; sin secretos; neutral; paridad/delegacion .ps1 + CI; gates verdes; handoff autocontenido; release atomico DECISION-0018; staging por paths DECISION-0020]
---

# TASK-0079 (SA.2) - Kill-switch (pausa) + reloj de pared

> IN_REVIEW (entregada por Codex 2026-06-08). Segunda rebanada de autonomia supervisada
> (DECISION-0024 aprobada). SHADOW: sin agentes reales, invoker real intacto, autonomia off-by-default. Ver
> SPEC-0064 (componentes C3 + C4).

## Contexto

SA.1 (TASK-0078) entrego el sobre base (registro + max_turns + runreport) ejercitado con RecordedInvoker. SA.2
agrega dos paradas duras mas del sobre: la **pausa/kill-switch** entre turnos y el **reloj de pared** por corrida.

## Alcance (SPEC-0064 C3 + C4)

1. **C3 kill-switch / pausa**: el loop comprueba un centinela `runtime/state/PAUSE` **antes de cada turno**; si
   existe, para con `outcome=paused` sin mutar estado. Reanudar exige quitar el centinela + re-invocar (no
   auto-resume).
2. **C4 reloj de pared**: `caps.wall_clock_ms` (determinista via `--clock-fixed` en tests); el loop acumula
   duraciones y al exceder para con `outcome=wallclock_exhausted`.
3. **Golden** (sin red): para por pausa; para por reloj; off/sin registro byte-equivalente; cerrojo real intacto.
   Paridad `.ps1` + CI.

## Restricciones

- Off-by-default; **NO toques el invoker real** (DECISION-0021 intacto); **NO enciendas autonomia**.
- Determinista (sin reloj/red salvo lo provisto); sin secretos; neutral. Handoff autocontenido; release atomico
  (DECISION-0018); staging por paths (DECISION-0020).

## Nota

Tras SA.2: SA.3 (checkpoint humano forzado + escalacion). SA.4 (invoker real multi-turno bajo el sobre) sigue
gateada con GO del operador + ensayo de rollback.
