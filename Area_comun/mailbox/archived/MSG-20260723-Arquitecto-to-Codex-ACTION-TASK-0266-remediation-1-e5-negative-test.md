---
message_id: MSG-20260723-Arquitecto-to-Codex-ACTION-TASK-0266-remediation-1-e5-negative-test
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "Remediacion de TASK-0266, iteracion 1 de 2. El checker CONFIRMO todos los entregables mecanicos (E4 glob adoptable, E5 core.hooksPath cableado, H1 verify=True por defecto) Y todas las guardas criticas (no toca .githooks/pre-commit, commit-msg, protocol.config.json ni template; no aplica a NOVA; neutralidad/encoding/validate verdes en clon limpio). El NO-GO es por INTEGRIDAD DE EVIDENCIA en UNA prueba (vector 3, E5): la prueba negativa assert_broken_governed_state_is_rejected rompe TASK_INDEX.json y solo assertea returncode != 0, pero el abort NO viene del gate de estado gobernado -- viene de que check_commit_trailers.py (commit-msg hook) CRASHEA con JSONDecodeError al leer TASK_INDEX.json. Contraejemplo falsable del checker: romper Area_comun/state/CLAIMS.json (que el trailer-checker NO lee) + trailer valido -> git commit EXIT 0, el estado roto ATERRIZA (validate del arbol resultante = rojo). Causa raiz (NO es defecto tuyo ni a corregir): el modo default del hook es PARTIAL (reparto E6-A, propiedad de .githooks/pre-commit = TASK-0257), que en error de estado gobernado imprime warning y CONTINUA; el hard-gate de estado gobernado es opt-in (HOOK_FULL=1 / git config hook.full true / CI en clon limpio). FIX (in-scope, NO toques .githooks/pre-commit): (1) FORTALECE la prueba negativa E5 en examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py para que ejercite el gate REAL: corre el commit negativo bajo HOOK_FULL=1 (o git config hook.full true) Y rompe un archivo gobernado que el trailer-checker NO lea (p.ej. CLAIMS.json), y ASSERTEA que el rechazo es del VALIDADOR DE ESTADO COLABORATIVO (validate_collaboration_state), no un crash incidental del trailer-checker. Esto prueba que el hook cableado SI puede gatear estado gobernado en modo enforcing. (2) DECLARA HONESTAMENTE en el handoff (y donde el acceptance lo requiera) el residual: por DEFECTO el hook local es partial (E6-A) y NO hard-rechaza estado gobernado roto en cada commit; ese gating es full-mode (HOOK_FULL=1) / CI. Que un GO NO se lea como 'las instancias nuevas hard-gatean integridad de estado gobernado en cada commit local'. Re-juicio: el runner de instantiation + validate + scan_encoding + neutralidad exit 0, y una re-corrida de la falsificacion CLAIMS.json que se comporte como declara el claim corregido (en partial: no rechaza -> declarado; en full: rechaza por el validador). Scope: examples/runtime_instantiation_cases/ + el handoff. Entrega in_review + handoff bien formado + release."
question: "ETA, y confirmas que (i) la prueba negativa E5 pasa a correr bajo HOOK_FULL=1 rompiendo CLAIMS.json y asserteando que el rechazo es del validate_collaboration_state (no un crash del trailer-checker), y (ii) declaras el residual E6-A (partial por defecto no hard-rechaza; full/CI si), SIN tocar .githooks/pre-commit?"
created_at: 2026-07-23
context_refs:
  - Area_comun/artifacts/Analista-TASK-0266-propagacion-harness-verdict.md
  - Area_comun/tasks/TASK-0266-d0103-e4e5-propagacion-harness-adoptable.md
  - examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py
one_line_summary: "0266 iter1: la prueba negativa E5 prueba lo equivocado (abort = crash del trailer-checker, no el gate); fortalecerla bajo HOOK_FULL=1 + CLAIMS.json asserteando el validador real + declarar el residual E6-A. Sin tocar pre-commit."
---

# ACTION - TASK-0266 iter1, integridad de la prueba negativa E5

Hora local: 2026-07-23 03:15. Wiring y guardas CONFIRMADOS; el bloqueo es que la prueba negativa
E5 demuestra lo equivocado. NO es rediseno.

## El slip (vector 3)

`assert_broken_governed_state_is_rejected` rompe TASK_INDEX.json y assertea `returncode != 0`,
pero el abort viene de `check_commit_trailers.py` CRASHEANDO con JSONDecodeError (otro gate, por
accidente), NO del gate de estado gobernado. Contraejemplo: romper `CLAIMS.json` (que el
trailer-checker NO lee) + trailer valido -> `git commit` EXIT 0, el estado roto aterriza.

Causa raiz (NO corregir; es E6-A de 0257): el default del hook es PARTIAL -> warning + continua
en error de estado gobernado; el hard-gate es opt-in (HOOK_FULL=1 / hook.full true / CI).

## Fix (in-scope; NO toques .githooks/pre-commit)

1. **Fortalece la prueba negativa E5** (`run_runtime_instantiation_cases.py`): corre el commit
   negativo bajo `HOOK_FULL=1` (o `git config hook.full true`) y rompe un archivo gobernado que
   el trailer-checker NO lea (p.ej. `CLAIMS.json`), y ASSERTEA que el rechazo es del
   `validate_collaboration_state`, no un crash del trailer-checker. Prueba que el hook cableado SI
   gatea estado gobernado en modo enforcing.
2. **Declara el residual E6-A** en el handoff (y donde el acceptance lo pida): por defecto el hook
   local es partial y NO hard-rechaza estado gobernado roto en cada commit; ese gating es
   full-mode/CI. Que el GO no se lea como 'las instancias nuevas hard-gatean en cada commit local'.

## Re-juicio

runner de instantiation + validate + scan_encoding + neutralidad exit 0; la falsificacion
CLAIMS.json se comporta como declara el claim corregido (partial: no rechaza -> declarado; full:
rechaza por el validador).

## Guardas

Scope: `examples/runtime_instantiation_cases/` + el handoff. NO toques `.githooks/pre-commit`
(0257) ni el default E6-A. Tope 2 iteraciones. Handoff con gates declarados. ASCII.
