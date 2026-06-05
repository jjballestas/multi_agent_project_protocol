# DISEÑO — Runtime M1 (aplicación de turno + gate/rollback + adapter replay)

> **Bajo DECISION-0009** (runtime adoptado, opt-in/off-by-default). M1 es **diseño + specs + tasks**,
> NO una nueva decisión. Continúa M0 (TASK-0026/0027: `turn_schema.json`, router, `turn_validate`,
> `--plan`). Neutral (tooling). Última actualización: 2026-06-05 · Autor: Claude (arquitecto).

## 0. Resumen
M0 entregó el **plano de control read-only**: router determinista + validador de turno + `--plan`
dry-run. M1 da el **primer escritor seguro**: aplicar un *turn report* ya validado a los ficheros,
correr el **gate** (validador + scan) y hacer **1 turno = 1 commit** o, si el gate falla, **`git
revert` + `blocked` + escalar**. Y define la **interfaz `AgentAdapter`** vendor-neutral con un
**replay adapter** (lee un report pre-escrito, sin LLM) para poder correr el **loop completo de forma
determinista** y dogfoodearlo.

**Límite de M1 (refinamiento del DISENO base §7):** la invocación de un agente real
(`claude_adapter`/`codex_adapter` vía SDK/API) se mueve a **M2**. Razón: mantener M1 **determinista y
testeable con golden** (sin red, sin no-determinismo del modelo). El replay adapter cubre el loop
end-to-end; cambiar replay→real es solo otro adapter detrás de la misma interfaz.

## 1. Alcance de M1
- `runtime/vcs.py` — wrapper git: `commit_turn(message, paths)` y `revert_last()`; **write-allowlist**
  dura (nunca toca `.git/`, `Area_comun/decisions/`, `AGENTS.md`, `protocol.config*` salvo flag).
- `runtime/apply.py` — `apply_turn(report, root)`: aplica transiciones del report **ya validado**
  (`turn_validate` de M0): `task_status`, `claims` (acquire/release), `mailbox` (send/answer/archive),
  `handoff`. Determinista e idempotente-por-turno.
- `runtime/gate.py` — `run_gate(root)`: corre `validate_collaboration_state` + `scan_domain_neutrality`;
  devuelve verde/rojo + detalle. Reusa los scripts existentes (no los reescribe).
- `runtime/adapters/base.py` — `AgentAdapter` (Protocol) + tipos `ContextPack`/`TurnReport`.
- `runtime/adapters/replay.py` — adapter que devuelve un report desde un fichero (test/dogfood).
- `runtime/orchestrator.py` — extiende con `--run` (aplica de verdad) además de `--plan` (dry-run);
  `--once` (un turno) y `--max-iter N`. **`enabled:false` sigue siendo el default**.
- `runtime/runs/RUN-<id>.jsonl` — run-log por turno (unidad, agente, outcome, transición, gate, commit).

## 2. El turno (tick) en M1
```text
tick(root):
  1. gate_pre   = run_gate(root)            # si rojo de entrada -> parar + escalar (estado sucio)
  2. unit       = select_next(load_state)   # router M0 (SPEC-0027)
     if unit is None or unit.action == escalate -> stop (sin trabajo / gate humano)
  3. claim      = acquire(unit)             # lock de rutas (DECISION-0007), si aplica
  4. context    = build_context(unit)       # context pack (AGENTS.md §0) — M1 minimo
  5. report     = adapter.run_turn(context) # M1: replay adapter (report pre-escrito)
  6. errors     = validate_turn(report)     # M0 turn_validate (schema + write-allowlist + anti-carrera)
     if errors -> reject: NO se aplica nada; log; parar/seguir segun politica
  7. if report.outcome in {decision_required, human_required} or report.gate.human_required:
        write HUMAN_REPORT; stop (parada dura)        # gates humanos
  8. apply_turn(report, root)               # muta ficheros
  9. gate_post  = run_gate(root)
     if verde -> vcs.commit_turn(report.commit_message, report.changed_paths)   # 1 turno = 1 commit
     if rojo  -> vcs.revert_last(); set task blocked; write HUMAN_REPORT; stop   # rollback atomico
 10. runlog.append(...); loop (hasta none / human / max-iter / budget)
```
**Invariante:** entre el paso 8 y 9 el repo puede quedar sucio, pero **nunca se commitea** un estado
que el gate rechaza; si el gate falla se revierte al estado pre-turno. Un turno fallido **no avanza**.

## 3. `AgentAdapter` (vendor-neutral)
```python
class AgentAdapter(Protocol):
    name: str
    def run_turn(self, *, context: ContextPack, root: Path) -> dict: ...  # devuelve un turn report (turn_schema)
```
- **replay** (M1): `run_turn` lee `context.replay_report_path` y lo devuelve. Sin red, determinista.
- **manual** (M1, opcional): imprime el context pack y lee un report escrito por un humano.
- **claude/codex** (M2): invocan el SDK/CLI real; el resto del loop **no cambia** (misma interfaz).
El adapter **solo** produce el report + escribe ficheros dentro de `root`; el orquestador es el único
que aplica transiciones de estado y commitea (**escritor único** ⇒ atomicidad; ver DECISION-0011).

## 4. Seguridad
- **Write-allowlist dura** en `vcs.commit_turn`: rechaza paths bajo `.git/`, `Area_comun/decisions/`,
  `AGENTS.md`, `protocol.config*` salvo `--allow-policy` explícito (cambios de política = humano).
- **Gate por turno** antes de commitear; rojo ⇒ revert. Reusa validador + scan (AGENTS §5).
- **Gates humanos** = paradas duras (outcome/gate). El loop no se auto-continúa tras ellos.
- **Budget/`--max-iter`** como techo del loop; al alcanzarlo, para y reporta.
- **Off-by-default**: sin `runtime.enabled:true` el orquestador solo permite `--plan` (como hoy).

## 5. Entregables y troceo
| Pieza | Task (owner) | Spec |
|---|---|---|
| apply_turn + gate + vcs (commit/revert) + write-allowlist | **TASK-0030** (Codex) | SPEC-0029 |
| AgentAdapter + replay adapter + `--run` loop + run-log | **TASK-0031** (Codex) | SPEC-0030 |

**Orden recomendado (cola):** TASK-0028 (claims por fila) → TASK-0025 (frontmatter) → **TASK-0030** →
**TASK-0031**. TASK-0030/0031 son deterministas (replay), con golden, sin invocar agentes reales (M2).

## 6. Golden (deterministas, sin LLM)
- **apply/gate (SPEC-0029):** sobre repo-fixture temporal: report válido `ready→in_review` ⇒ estado
  cambia + 1 commit; report que rompe el gate (p.ej. introduce término de dominio) ⇒ `git revert` +
  tarea `blocked`, árbol restaurado; report `human_required` ⇒ no commitea, escala.
- **loop (SPEC-0030):** replay de 1..N reports ⇒ secuencia determinista de turnos; `--plan` sigue sin
  mutar; `--run --max-iter 1` aplica exactamente un turno; parada por gate humano.

## 7. Riesgos
| Riesgo | Mitigación |
|---|---|
| Apply parcial deja estado inconsistente | gate_post + revert atómico; un turno fallido no avanza |
| El adapter toca rutas de política | write-allowlist dura en vcs; flag explícito = humano |
| No-determinismo del modelo en tests | M1 usa replay adapter; agente real = M2 |
| Commits ruidosos | 1 turno = 1 commit con mensaje del report; run-log para auditoría |
| Concurrencia de escritura de estado | escritor único (orquestador) + DECISION-0011 (claims por fila) |

## 8. Qué NO incluye M1
- No invoca LLMs reales (eso es M2: `claude_adapter`/`codex_adapter`).
- No automatiza el ciclo multi-agente completo Claude↔Codex sin humano (M2).
- No cambia el modelo file-based ni añade servidor/DB. No auto-aplica cambios de política.
