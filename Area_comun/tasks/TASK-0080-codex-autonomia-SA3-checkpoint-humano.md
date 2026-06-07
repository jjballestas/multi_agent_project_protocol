---
id: TASK-0080
owner: Codex
status: ready
type: implementation
priority: normal
created_at: 2026-06-08
updated_at: 2026-06-08
depends_on: [TASK-0079]
relates_to: [TASK-0038]
phase: P2
spec_id: Area_comun/specs/SPEC-0064-autonomia-supervisada.md
linked_decisions: [DECISION-0024, DECISION-0021, DECISION-0022]
execution_pipeline: [C5 checkpoint humano forzado - tras caps.human_checkpoint_every_k turnos consecutivos o ante repeticion de fix-cycles (quality_policy max_review_cycles/max_qa_cycles), el loop para con human_required=True y outcome=human_checkpoint, sin auto-resume (reanudar exige nueva invocacion humana); se apoya en la escalada existente del router y en quality_policy; runreport registra el checkpoint; golden examples/supervised_autonomy_cases ampliado (para por K turnos, para por fix-cycles repetidos) con RecordedInvoker; off/sin registro byte-equivalente; paridad .ps1 + CI]
acceptance_criteria: [el loop con supervised_autonomy activo para con human_required/outcome=human_checkpoint tras caps.human_checkpoint_every_k turnos y ante fix-cycles repetidos (quality_policy), sin auto-resume; sin flag/registro byte-equivalente; NO toca el invoker real (cerrojo --once intacto); determinista sin reloj/red; sin secretos; neutral; paridad .ps1; golden + gates verdes]
expected_output: runtime/orchestrator.py + runtime/supervised_autonomy.py (checkpoint humano + escalacion) + golden + CI; autonomia off-by-default; invoker real intacto.
test_plan: [golden: para por human_checkpoint_every_k turnos; para por fix-cycles repetidos (quality_policy); no auto-resume; off byte-equivalente; cerrojo real --once intacto; determinismo + paridad py/ps]
question_to_resolve: ninguna (alcance SA.3 en SPEC-0064 C5). Valor por defecto de human_checkpoint_every_k a confirmar (sugerencia 2). Si requiere tocar el invoker real => blocked + pregunta.
closure_criterion: checkpoint humano forzado (tras K turnos o fix-cycles repetidos -> human_required, no auto-resume) ejercitado con RecordedInvoker + golden + paridad .ps1; off byte-equivalente; invoker real intacto; gates verdes; handoff autocontenido; release atomico (DECISION-0018).
closure_criteria: [C5 checkpoint humano tras caps.human_checkpoint_every_k turnos o fix-cycles repetidos (quality_policy) -> human_required/outcome=human_checkpoint sin auto-resume; apoyo en escalada del router + quality_policy; runreport registra el checkpoint; golden (para por K turnos, para por fix-cycles); off/sin registro byte-equivalente; invoker real --once intacto; determinista sin reloj/red; sin secretos; neutral; paridad/delegacion .ps1 + CI; gates verdes; handoff autocontenido; release atomico DECISION-0018; staging por paths DECISION-0020]
---

# TASK-0080 (SA.3) - Checkpoint humano forzado + escalacion

> READY (encolada por Claude 2026-06-08 tras cerrar SA.2/TASK-0079). Tercera rebanada de autonomia supervisada
> (DECISION-0024 aprobada). SHADOW: sin agentes reales, invoker real intacto, autonomia off-by-default. Ver
> SPEC-0064 (componente C5).

## Contexto

SA.1 (sobre base) + SA.2 (kill-switch + reloj) dan paradas por max_turns, pausa y reloj. SA.3 agrega el
**checkpoint humano forzado**: el loop no debe encadenar indefinidamente sin supervision; tras K turnos o ante
repeticion de fix-cycles, para y exige re-confirmacion humana.

## Alcance (SPEC-0064 C5)

1. **Checkpoint por turnos**: `caps.human_checkpoint_every_k` -> tras K turnos consecutivos el loop para con
   `human_required=True` / `outcome=human_checkpoint`, sin auto-resume (reanudar = nueva invocacion humana).
2. **Checkpoint por fix-cycles**: ante repeticion de ciclos review/qa (quality_policy `max_review_cycles`/
   `max_qa_cycles`), el loop escala a humano. Se apoya en la escalada existente del router + quality_policy.
3. **Runreport** registra el checkpoint. **Golden** (sin red): para por K turnos; para por fix-cycles repetidos;
   off/sin registro byte-equivalente; cerrojo real intacto. Paridad `.ps1` + CI.

## Restricciones

- Off-by-default; **NO toques el invoker real** (DECISION-0021 intacto); **NO enciendas autonomia**.
- Determinista (sin reloj/red salvo lo provisto); sin secretos; neutral. Handoff autocontenido; release atomico
  (DECISION-0018); staging por paths (DECISION-0020).

## Nota

Tras SA.3: SA.4 (invoker real multi-turno bajo el sobre) -- GATEADA con GO del operador + ensayo de rollback;
no arrancar sin esa coordinacion. SA.5 = docs/promocion.
