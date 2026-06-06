# Session report - Release v0.8.0 (runtime M1)

- Date: 2026-06-06
- Phase: P2 (Adopcion y expansion)
- Process status: closed (v0.8.0 publicada)
- Ratification: aprobada por el human owner (corte de release); TASK-0030/0031 ratificadas por Claude

## 1. In One Sentence
Se publica **v0.8.0**: cierra **runtime M1** — el primer escritor seguro (apply+gate+commit/revert) y
el loop determinista (`--run`) via replay adapter — aditivo y off-by-default (`runtime.enabled:false`).

## 2. What Was Done
- Ratificacion de **TASK-0030** (apply+gate+vcs, SPEC-0029): `runtime/apply.py` (escribe solo si
  `validate_turn` pasa), `runtime/gate.py` (validador + scan), `runtime/vcs.py` (1 commit por turno
  verde; `git restore` + `blocked` en gate rojo). Golden repo-fixture 4/4.
- Ratificacion de **TASK-0031** (adapter+replay+loop, SPEC-0030): `AgentAdapter` (Protocol
  vendor-neutral), `ReplayAdapter` determinista, `runlog.py` (`--run-id` inyectable + default
  `RUN-<sha256>`), `orchestrator --run/--once/--max-iter` reusando el motor de 0030. Golden loop 5/5.
- **Coordinacion proactiva** (indicacion del operador): mensaje previo a Codex fijo el `RUN-id`
  determinista antes de codificar el run-log ⇒ cero re-trabajo; Codex anadio `context_refs` por su cuenta.
- Corte de release: CHANGELOG `[0.8.0]`, `protocol_version` 0.7.0 → 0.8.0, AGENTS.md y PROJECT_STATE
  actualizados, tag `v0.8.0`.

## 3. SDD Summary
- Specs cubiertas (impl) en v0.8.0: SPEC-0029 (apply+gate+vcs), SPEC-0030 (adapter+replay+loop).
- Tasks done: TASK-0030, TASK-0031 (sobre el diseno TASK-0029 ya cerrado en v0.7.0).
- Acceptance: 0030 golden 4/4 (commit en verde, restore+blocked en rojo, rechazo de path de politica,
  no-write en report stale); 0031 golden 5/5 (`--once`=1 turno/1 commit + run-log exacto, secuencia
  determinista con `--max-iter`, `human_required`=parada dura, `--plan` sin regresion, `enabled:false`
  aborta `--run`).
- Test plans: golden runtime (loop/apply/router/turn) + validador + scan + regresion; todos verdes (.py;
  .ps1 atestiguado por Codex/CI — deny-rule PowerShell en sesion arquitecto; aqui sin cambios de validador).
- Desviaciones: ninguna. Limite M1/M2: agente LLM real y loop autonomo = M2.

## 4. Decisions
- DECISION-0009 (runtime de orquestacion, opt-in/off-by-default) y DECISION-0001 (versionado). Cambio
  **MINOR**: aditivo, neutral, back-compatible, off-by-default.

## 5. Current Project State
- **v0.8.0 publicada**; `protocol_version=0.8.0`; validador + scan + golden verdes.
- Done: TASK-0022..0031. Runtime M0+M1 completos (off-by-default). Sin tareas ready/in_progress.
- Sin claims activos de implementacion tras el cierre; sin bloqueos.

## 6. Next Steps
1. **Claude:** derivar specs/tasks de **runtime M2** desde `DISENO-runtime-m2.md` §5 (adapters LLM
   reales claude/codex + loop autonomo Claude↔Codex + mailbox-auto + budget/run-log/metricas).
2. **Codex:** implementar M2 segun cola, sobre la interfaz `AgentAdapter` (el loop M1 no cambia).
3. Proxima poda: archivar la ventana reciente de done (TASK-0024..0031).

## 7. What We Need From The Human Owner
- **Push** de los commits + el tag `v0.8.0` al remoto privado (pendiente de tu visto bueno).
- **APROBACION HUMANA** para activar `runtime.enabled:true` (encender el runtime es cambio de modo de
  operacion; sigue off por defecto hasta tu decision — DECISION-0009).
- Confirmar el orden de M2 (que hito atacar primero del troceo de DISENO-M2 §5).

## 8. Risks Or Ambiguities
- Paridad `.ps1` no ejecutada por Claude (deny-rule); n/a para 0030/0031 (codigo python; sin cambio del
  validador). Codex/CI la atestiguan.
- Ventana reciente de done en estado caliente; mitiga la proxima poda.
- Runtime real (M2) introducira riesgo de coste/escape: ya mitigado por diseno (gate por turno, 1
  commit/turno, budget+`--max-iter`, sandbox, gates humanos como paradas duras).

## 9. Communication Status
- Open messages (requiring response): ninguno bloqueante (OKs de cierre + housekeeping de mailbox).
- Active blocks: ninguno.
- Decisions required / human-required: push + tag; activar runtime (no bloqueante).

## 10. Details
- CHANGELOG `[0.8.0]`; DECISION-0009/0001; SPEC-0029/0030; TASK-0030/0031; HANDOFF-TASK-0030/0031.
- Commit de release v0.8.0 + tag `v0.8.0` sobre HEAD `d3fd121` (v0.7.0).
