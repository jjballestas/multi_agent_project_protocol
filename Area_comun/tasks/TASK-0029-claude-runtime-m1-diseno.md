---
id: TASK-0029
owner: Claude
status: done
type: analysis
priority: normal
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0027]
relates_to: [TASK-0028, TASK-0030, TASK-0031]
phase: P2
objective: Disenar runtime M1 (aplicacion de turno + gate/commit/revert + interfaz adapter + replay loop) bajo DECISION-0009, sin nueva decision.
expected_output: DISENO-runtime-m1.md + SPEC-0029 (apply+gate+vcs) + SPEC-0030 (adapter+replay+--run) + backlog TASK-0030/0031.
question_to_resolve: Como dar el primer escritor seguro del runtime manteniendolo determinista y testeable (sin invocar LLMs todavia).
closure_criterion: Diseno + 2 specs emitidos (spec_id resoluble, status ready) + TASK-0030/0031 promovidas a ready; validador verde.
---

# TASK-0029 — Runtime M1 (diseño): apply + gate/rollback + adapter replay

> `analysis` bajo [DECISION-0009](../decisions/DECISION-0009-runtime-orquestacion.md). Continua M0
> (TASK-0026/0027). Refina el limite del DISENO base §7: **invocacion de agente real = M2**; M1 usa un
> **replay adapter** para cerrar el loop de forma determinista. Neutral (tooling).

## Entregado por Claude
- `Area_comun/artifacts/DISENO-runtime-m1.md` — alcance, tick, seguridad, troceo, golden, riesgos.
- `Area_comun/specs/SPEC-0029-turn-apply-gate.md` — `vcs.py` + `apply.py` + `gate.py` (1 turno = 1
  commit / revert; write-allowlist dura).
- `Area_comun/specs/SPEC-0030-adapter-replay-loop.md` — `AgentAdapter` + `replay` + `--run`/`--max-iter`
  + run-log.
- Promueve **TASK-0030** (apply+gate+vcs, SPEC-0029) y **TASK-0031** (adapter+replay+loop, SPEC-0030).

## Decisiones de diseño
- **Escritor unico** (orquestador) ⇒ atomicidad; alинеado con DECISION-0011 (claims por fila) para el
  estado. Replay adapter = sin red, golden deterministas. Real `claude_adapter`/`codex_adapter` = M2.
- Orden de cola recomendado: TASK-0028 → TASK-0025 → TASK-0030 → TASK-0031.
