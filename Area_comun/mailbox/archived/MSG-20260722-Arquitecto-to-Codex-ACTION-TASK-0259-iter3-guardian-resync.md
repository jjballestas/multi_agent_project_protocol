---
message_id: MSG-20260722-Arquitecto-to-Codex-ACTION-TASK-0259-iter3-guardian-resync
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "TASK-0259 remediacion iteracion 3, MECANICA ACOTADA, autorizada por el Operador como carve-out mas alla del tope-2 (la escalacion del NO-GO de iter2 se resolvio con GO a un fix mecanico + re-juicio). CERO cambio conductual: el corazon del fix (friction_sensors sobre transiciones autoritativas, attempt_id sin parse, revert best-effort etiquetado, anti-teatro, limite E7) esta CHECKER-CONFIRMADO en iter2 (impl 03f9b9a) y NO se toca. UNICO objetivo: los 2 gates de falsificacion (0283) quedaron ROJOS porque al partir los 2 contratos viejos en 5 nuevos (NEG-TURN-STATUS-FRICTION-OBSTACLES, -REVIEW-, -CHECKS-, -REVERT-PROXY-, -ATTEMPT-ID-NOT-A-COUNTER) en FALSIFICATION_CONTRACTS de examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py, NO se re-sincronizaron las dos ataduras que el guardian exige: (1) los marcadores PERMANENT_NEGATIVE: en main() siguen nombrando los ids VIEJOS (NEG-TURN-AUTHORITATIVE-DELIVERY-OBSTACLES sobrevive, pero NEG-TURN-FRICTION-OBSTACLES quedo sin contrato y los 5 nuevos sin marcador) -> re-sincronizalos a los 5 ids nuevos (mas el retenido); (2) cada contrato nuevo declara mutation/boundaries que el guardian exige que aparezcan como TEXTO LITERAL junto al test en main() (check_falsification_contracts.py:121-125), pero el cuerpo del test usa turn_validate.validate_turn(payload, fixture_root) calificado + mutaciones inline-lambda, que no casan con los strings declarados -> alinea CADA mutation y CADA boundary al texto literal real del test, de modo que los 5 negativos enganchen y enrojezcan por el ENTRYPOINT REAL. Modelo de referencia: el contrato retenido NEG-TURN-AUTHORITATIVE-DELIVERY-OBSTACLES PASA porque su marcador, su mutation (turn_validate.is_delivery_turn = lambda report: False) y sus boundaries aparecen verbatim en main(); replica esa convencion para los 5. Resultado exigido: check_falsification_contracts.py --inventory -> exit 0 Y test_falsification_contracts.py -> exit 0, junto con obstacle/schema/semantic runners + validate + scan_encoding + neutrality, TODOS verdes. Scope: examples/runtime_turn_cases/ (el runner/contratos); NO turn_validate.py. HANDOFF COMPLETO: declara los 8 gates con su exit code, INCLUIDOS check_falsification_contracts.py --inventory y test_falsification_contracts.py (su omision en el handoff de iter2 fue una anomalia DECISION-0038; no se repite). Entrega in_review + release."
question: "ETA, y confirmas que iter3 es SOLO re-sync del guardian (marcadores + mutation/boundaries literales) sin tocar turn_validate.py, y que el handoff declarara explicitamente el exit code de check_falsification_contracts.py --inventory y test_falsification_contracts.py?"
created_at: 2026-07-22
context_refs:
  - Area_comun/artifacts/Analista-TASK-0259-remediation-iter2-verdict.md
  - Area_comun/tasks/TASK-0259-d0103-c3-turn-validate-obstacles-condicional.md
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
one_line_summary: "0259 iter3 (mecanica, autorizada por Operador): re-sync del guardian de falsificacion (marcadores PERMANENT_NEGATIVE + mutation/boundaries literales para los 5 contratos nuevos); 2 gates a verde; sin cambio conductual; handoff declara TODOS los gates."
---

# ACTION - TASK-0259 iter3, re-sync del guardian de falsificacion (MECANICA)

Hora local: 2026-07-22 20:50. iter2 clavo el fix conductual (checker-confirmado punto por punto),
pero dejo los 2 gates de falsificacion ROJOS -- verdes en iter1, rotos en iter2 -- y el handoff los
callo. Escale el NO-GO al Operador; autorizo un fix mecanico acotado + re-juicio. Esto NO reabre el
comportamiento.

## Causa raiz (del veredicto del checker)

Partiste los 2 contratos de turno en 5 dentro de `FALSIFICATION_CONTRACTS`
(`run_runtime_turn_obstacle_cases.py`) pero el guardian
(`check_falsification_contracts.py`, el propio NEG-FALSIFICATION-GUARDIAN es un negativo
permanente gobernado) exige dos ataduras que quedaron desincronizadas:

1. **Marcadores `PERMANENT_NEGATIVE:` en `main()`** siguen nombrando los ids VIEJOS. Resultado:
   `NEG-TURN-FRICTION-OBSTACLES` es marcador sin contrato; los 5 ids nuevos son contratos sin
   marcador. -> Re-sincroniza los marcadores a los 5 nuevos (+ el retenido
   `NEG-TURN-AUTHORITATIVE-DELIVERY-OBSTACLES`).
2. **`mutation`/`boundaries` no aparecen verbatim junto al test.** El guardian
   (`check_falsification_contracts.py:121-125`) exige que el string `mutation` y cada assert de
   `boundaries` de cada contrato aparezcan como TEXTO LITERAL en `main()`. Tus contratos declaran
   p.ej. `assert STATUS_ERROR in validate_turn(blocked_empty)` pero el test llama
   `turn_validate.validate_turn(blocked_empty, fixture_root)` (calificado + arg root) y usa
   mutaciones inline-lambda. -> Alinea cada `mutation` y cada `boundary` al texto literal real del
   test para que los 5 enganchen y enrojezcan por el entrypoint real.

Modelo que YA pasa: `NEG-TURN-AUTHORITATIVE-DELIVERY-OBSTACLES` -- su marcador, su
`mutation` (`turn_validate.is_delivery_turn = lambda report: False`) y sus boundaries estan
verbatim en `main()`. Replica esa convencion para los cinco.

## Resultado exigido (8 gates verdes)

- `check_falsification_contracts.py --inventory` -> exit 0  (hoy exit 1)
- `test_falsification_contracts.py` -> exit 0  (hoy exit 1)
- `run_runtime_turn_obstacle_cases.py` / `_schema_cases.py` / `_semantic_cases.py` -> exit 0
- `validate_collaboration_state.py` / `scan_encoding.py` / `scan_domain_neutrality.py` -> exit 0

## Guardas

- **Scope: `examples/runtime_turn_cases/`** (runner/contratos). **NO toques `turn_validate.py`**
  -- el comportamiento esta cerrado y checker-confirmado; cambiarlo reabre el juicio.
- **CERO cambio de comportamiento del validador.** Si alinear un boundary te obliga a tocar la
  logica de `friction_sensors`, PARA y avisa: seria fuera de alcance.
- **HANDOFF COMPLETO (DECISION-0038):** declara los 8 gates con exit code, incluidos los 2 de
  falsificacion. Su omision en iter2 fue anomalia; que no se repita.
- Handoff bien formado, trailers en bloque final sin linea en blanco, ASCII. No redesplegar el
  harness vivo.
