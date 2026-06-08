---
id: TASK-0091
owner: Codex
status: ready
type: documentation
priority: normal
created_at: 2026-06-09
updated_at: 2026-06-09
depends_on: []
relates_to: [TASK-0088, DECISION-0027]
phase: P2
spec_id: none
linked_decisions: [DECISION-0027, DECISION-0024]
objective: (TAREA-OBJETIVO DEL PILOTO SA.4) Anadir una nota aclaratoria corta (1-2 frases) al FINAL de examples/neutrality_scan_cases/README.md que explique que cubre el escaneo de neutralidad de dominio y como interpretar un caso que falla. SOLO PROSA en ese README; NO tocar fixtures, configs, codigo, goldens ni otros archivos.
expected_output: examples/neutrality_scan_cases/README.md con 1-2 frases nuevas al final aclarando el alcance del escaneo de neutralidad (denylist de terminos de dominio en rutas generic/core) y que un caso que "falla" significa que el escaneo DETECTO un termino prohibido (es el comportamiento esperado del caso negativo). Neutral, ASCII, sin secretos. Un solo archivo cambiado.
question_to_resolve: ninguna. Si el README no existe o el cambio requiere tocar otra cosa, parar con outcome blocked/human_required y reportar (falla cerrada).
closure_criterion: examples/neutrality_scan_cases/README.md con la nota (solo prosa, 1 archivo) + neutralidad/encoding verdes + el caso/golden de neutralidad sigue verde; sin tocar fixtures/configs/codigo/goldens; cambio reversible.
sdd_required: false
---

# TASK-0091 (PILOTO SA.4) - Nota aclaratoria en el README del escaneo de neutralidad

> READY (encolada por Claude 2026-06-09 VIA submit_intent). **TAREA-OBJETIVO DEL PRIMER PILOTO SA.4** (invoker
> real multi-turno bajo el sobre, DECISION-0027): bajo riesgo, acotada, solo prosa, fuera de nucleo y
> `*.template.*`, completable en 1 turno, reversible. El sobre acota: caps max_turns=2 / human_checkpoint_every_k=1
> (checkpoint humano OBLIGATORIO tras el turno 1, sin auto-resume) / wall_clock_ms=180000 / PAUSE.

## Alcance

Anadir al FINAL de `examples/neutrality_scan_cases/README.md` una nota corta (1-2 frases) que aclare:
- que cubre el escaneo de neutralidad de dominio (deteccion de terminos del denylist en rutas generic/core via
  `scan_globs`), y
- como leer un caso que "falla": el escaneo DETECTO un termino prohibido -> es el resultado esperado del caso
  negativo (no un bug).

## Restricciones (duras)

- **SOLO PROSA** en ese unico README. NO tocar fixtures, configs, codigo, goldens, ni otros archivos.
- Neutral de dominio, ASCII, sin secretos. Cambio reversible.
- Si algo exige salirse de este alcance -> parar (blocked/human_required) y reportar (falla cerrada).

## Nota

Es el piloto de activacion de SA.4. El loop hace 1 turno y PARA en el checkpoint humano tras el turno 1; el
arquitecto revisa (turnos, paradas, costo, commit, diff) y ratifica ANTES de cualquier turno 2.
