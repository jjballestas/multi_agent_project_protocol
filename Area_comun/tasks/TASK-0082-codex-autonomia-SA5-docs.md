---
id: TASK-0082
owner: Codex
status: ready
type: documentation
priority: normal
created_at: 2026-06-08
updated_at: 2026-06-08
depends_on: [TASK-0078, TASK-0079, TASK-0080]
relates_to: [TASK-0038]
phase: P2
spec_id: Area_comun/specs/SPEC-0064-autonomia-supervisada.md
linked_decisions: [DECISION-0024, DECISION-0021, DECISION-0022]
objective: Documentar la autonomia supervisada construida (sobre SA.1-SA.3) - como se configura, opera, pausa y audita - y dejar claro que el invoker real multi-turno (SA.4) es un paso gateado aparte. Neutral, sin secretos.
expected_output: Doc (p.ej. Area_comun/protocol/SUPERVISED_AUTONOMY.md) que explique runtime.supervised_autonomy (off-by-default, registro + caps), las paradas duras del sobre (max_turns, centinela runtime/state/PAUSE, reloj wall_clock_ms, checkpoint humano por K turnos / fix-cycles), el flag --allow-supervised-autonomy, el runreport, y que SA.4 (invoker real multi-turno) sigue gateada con GO + rollback. Enlaces desde N_AGENT_RUNTIME / README_INSTANCIACION.
question_to_resolve: ninguna (documenta SA.1-SA.3 ya implementado). Si la doc revela un gap => blocked + nota.
closure_criterion: doc de la autonomia supervisada (sobre SA.1-SA.3: registro/caps/paradas/runreport) + nota de SA.4 gateado + enlaces; neutralidad/encoding verdes; gates verdes; handoff autocontenido; release atomico (DECISION-0018).
sdd_required: false
---

# TASK-0082 (SA.5) - Docs de la autonomia supervisada (sobre SA.1-SA.3)

> READY (encolada por Claude 2026-06-08, tras cerrar Fase 7). Documenta el sobre de supervision ya implementado
> (SA.1-SA.3); no agrega codigo funcional. Off-by-default; el invoker real (SA.4) es un paso gateado aparte.
> Neutral, sin secretos. Ver SPEC-0064.

## Contexto

La autonomia supervisada (DECISION-0024) construyo en sombra el sobre que acota el loop multi-turno: SA.1
(registro + max_turns + runreport), SA.2 (kill-switch PAUSE + reloj de pared), SA.3 (checkpoint humano por K
turnos / fix-cycles). Falta documentar como se configura y opera, y dejar explicito que encender el invoker real
multi-turno (SA.4) sigue gateado con GO del operador + ensayo de rollback.

## Alcance

1. **Configuracion**: `runtime.supervised_autonomy { enabled:false, activation_decision, approved_by, approved_at,
   caps:{ max_turns, wall_clock_ms, human_checkpoint_every_k } }` (off-by-default; sin registro valido el cerrojo
   `--once` del invoker real sigue intacto). Flag `--allow-supervised-autonomy`.
2. **Paradas duras del sobre**: `max_turns` -> `max_turns_reached`; centinela `runtime/state/PAUSE` (chequeado
   antes de cada turno) -> `paused`; reloj `wall_clock_ms` -> `wallclock_exhausted`; checkpoint humano (K turnos
   o fix-cycles repetidos via quality_policy) -> `human_required`/`human_checkpoint`, sin auto-resume. Mas todas
   las paradas duras preexistentes del loop (gate, escalada, budget/deadline, schema, dirty no declarado).
3. **Auditoria**: el reporte de corrida `*.runreport.md` (turnos, paradas, costo, commits, motivo de cierre,
   registro de activacion).
4. **Nota de gating**: SA.4 (invoker real multi-turno bajo el sobre) requiere GO del operador + ensayo de
   rollback; no se activa con esta doc. Off-by-default y reversible.
5. Enlaces desde `Area_comun/protocol/N_AGENT_RUNTIME.md` (y/o README_INSTANCIACION).

## Restricciones

- Neutral de dominio; **ASCII**; **sin secretos**; documenta lo ya implementado (no enciende nada).
- Handoff autocontenido; release atomico (DECISION-0018); staging por paths (DECISION-0020).

## Nota

Tras SA.5: SA.4 (invoker real) queda como activacion gateada del operador. Es la ultima rebanada documental de la
autonomia supervisada.
