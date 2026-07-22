---
artifact: Analista-TASK-0283-denominador-rejuicio-verdict
task: TASK-0283
reviewer: Analista
verdict: CHANGE-REQUIRED
iteration: 2
created_at: 2026-07-22
anchors:
  product_commit: none (SIN PRODUCTO EN ALCANCE)
  reviewed_commit: 2a52e0c
  protocol_head: c1b17bc
---

# Analista - Re-juicio TASK-0283 (denominador independiente)

Hora local: 2026-07-22 15:35 (reloj del sistema, sin convertir).

## Ancla canonica

- Commit del entregable juzgado: `2a52e0c` (test: add independent negative denominator).
- HEAD del protocolo al juzgar: `c1b17bc` (== origin/main; sin drift). Los tres commits
  posteriores a `2a52e0c` (e017b57, 7eb2d41, c1b17bc) no tocan `scripts/` ni `examples/`
  bajo revision -- verificado con `git show --stat`.
- Escrutinio en CLON LIMPIO en `D:/c283`, checkout `2a52e0c`, gates por exit code. No
  juzgue sobre el arbol caliente. Cada ataque lo elegi yo (no el del maker), edite el clon,
  corri el checker, restaure con `git checkout`; arbol restaurado limpio al terminar.
- SIN PRODUCTO EN ALCANCE (respetado; el fondo pineado y el dataset N=500 no se tocaron).

## Reproduccion (exit codes en el clon limpio)

Gates base, todos verdes:

```
python scripts/check_falsification_contracts.py --root . --inventory  -> 0  (permanent_negatives=14 declared=14 missing=0)
python scripts/test_falsification_contracts.py                         -> 0
python scripts/validate_collaboration_state.py --root .                -> 0
python scripts/scan_encoding.py                                        -> 0
python scripts/scan_domain_neutrality.py                               -> 0
```

Ataques adversariales (blancos mios):

```
A) Q3-MARCADO   negativo NUEVO con marker 'my-marked-shadow' y SIN contrato, en el runner mailbox_retry
     -> exit 1  permanent_negatives=15 declared=14 missing=1
        ERROR: my-marked-shadow: permanent negative ...run_mailbox_retry_cases.py:case_marked_shadow has no declared contract

B) Q3-SIN-MARKER  negativo permanente REAL sin marker y sin contrato
     def case_untagged_shadow():
         output = "safe"
         assert "reset --hard" not in output      # negativo real: debe ponerse rojo si el guard degrada
     -> exit 0  permanent_negatives=14 declared=14 missing=0   (INVISIBLE al inventario)

C) EVASION-OFF-GLOB  negativo REAL con marker correcto pero en un fichero que el glob no recorre
     examples/shadow_cases/case_shadow.py  (marker 'offglob-shadow')  -- no matchea examples/**/run_*.py
     -> exit 0  permanent_negatives=14 declared=14 missing=0   (INVISIBLE al inventario)

D) Q1a regresion  relajo la frontera declarada 'assert mutant_output == "live"' de retry-utf8-residue-path
     -> exit 1  ERROR: retry-utf8-residue-path: assertion boundary not found beside the test: assert mutant_output == "live"

E) Q4 regresion  relajo UNA de las dos fronteras de protocol-replay-drift-exit ('assert inverted({"has_drift": True}) == 0')
     -> exit 1  ERROR: protocol-replay-drift-exit: assertion boundary not found beside the test: ...
```

## Tabla vector-a-vector

| # | Lo que pedia la instruccion | Blanco que elegi | Resultado | Dictamen |
|---|------------------------------|------------------|-----------|----------|
| A (Q3-marcado) | Un negativo marcado sin contrato -> ROJO por missing>0 | case_marked_shadow (marker, sin contrato) | exit 1, missing=1, ERROR nominal | PASS - el denominador SI tiene dientes para el conjunto MARCADO |
| B (Q3-sin-marker) | Un negativo NUEVO real sin declarar -> ROJO | case_untagged_shadow (negativo real, sin marker) | exit 0, sigue 14/14, missing=0 | **SLIP - BLOQUEANTE: el negativo real queda invisible** |
| C (evasion off-glob) | La enumeracion AST no se puede evadir | negativo marcado en fichero fuera del glob | exit 0, 14/14, missing=0 | **SLIP - BLOQUEANTE: la enumeracion se evade por nombre de fichero** |
| D (Q1a) | Degradar una frontera declarada -> ROJO | retry-utf8-residue-path (borrar frontera) | exit 1, mensaje exacto | PASS - regresion intacta |
| E (Q4) | Relajar UNA de dos fronteras -> ROJO | protocol-replay-drift-exit (2 fronteras) | exit 1, mensaje exacto | PASS - regresion intacta |

## Juicio

**Lo que el maker cerro (credito completo, verificado):** el commit `2a52e0c` anade un
denominador REAL e independiente de la lista de contratos. `missing` ya no es el literal 0
sino una resta computada `existentes - declarados`; un negativo MARCADO sin contrato pone el
inventario en rojo (vector A: missing=1). Esto cierra exactamente el bloqueante de mi
iteracion 1 tal como lo redacte ("denominador independiente; missing computado"). La
deteccion de DEGRADACION de un contrato declarado (Q1a/Q4) sigue con dientes, incluida la
frontera multiple. Nada de esto retrocedio.

**Lo que sigue abierto (el bloqueante de esta iteracion):** el universo que el descubridor
enumera es **auto-declarado dos veces**: una funcion solo entra al denominador si (1) lleva
el docstring `PERMANENT_NEGATIVE:` Y (2) vive en un fichero `examples/**/run_*.py`. Un
negativo permanente REAL que omita el marker (vector B) o que este en otro fichero (vector C)
es invisible: el inventario reporta cobertura total `14/14 missing=0` mientras existe un
negativo sin declarar. Es la MISMA enfermedad que esta unidad se cargo de curar ("que no se
pueda colar un test-sombra sin declararla"), movida una capa arriba: antes bastaba con no
poner el contrato; ahora basta con no poner el marker (que es justo lo que un autor de
sombra -- o un descuido -- hara). La pregunta literal del REVIEW ("existe alguna forma de
que un negativo real quede fuera de la enumeracion AST y por tanto invisible al inventario?")
tiene respuesta demostrada: SI, por dos vias independientes.

**Corroboracion en el arbol vivo (no es el load-bearing, pero confirma que no es hipotetico):**
`examples/attestation_negative_cases/run_attestation_negative_cases.py` es una familia real de
negativos permanentes (mutadores `mutate_payload`, `delete_event`, `insert_event`,
`reorder_events`, `unregistered_key`, `cross_attribution`; cada caso exige que una atestacion
manipulada sea RECHAZADA). Es glob-reachable (`run_*.py`) y no lleva ni un marker: no esta
entre los 14. El inventario dice `missing=0` como si la suite tuviera exactamente 14
negativos, cuando tiene mas sin contar. Eso choca de frente con el acceptance #3, clausula 2:
"...sin dejar el resto como 'pendiente' indefinido." El resto queda mudo, no pendiente-visible.

## Recomendacion de cierre

**CHANGE-REQUIRED (NO-GO). Iteracion 2 de 2 -> se alcanza el tope; escalo al operador la
DECISION DE ALCANCE.**

Motivo del escalado (no es puro codigo): cerrar del todo la evasion exige definir "que es el
universo de negativos". Un denominador 100% independiente del autor es, en el limite,
indecidible -- no se puede saber mecanicamente que un test "debe quedarse rojo" sin ALGUNA
senal del autor; el marker ES esa senal minima, y mi propia remediacion de iteracion 1
tambien era declaration-based. Por eso la parte que falta es una decision de alcance del
operador, no un tercer rebote ciego al maker.

## Bucle de correccion / escalado

Al operador, para elegir el alcance (basta UNA de las dos direcciones; el maker no necesita
ambas):

- **R1 (fail-closed, cierra la evasion dentro de scope):** en los ficheros-runner de
  negativos, toda funcion cuyo cuerpo contenga un patron de asercion-negativa debe llevar
  marker+contrato o un waiver explicito (`# NOT-A-PERMANENT-NEGATIVE`), de modo que OMITIR el
  marker falle ruidoso en vez de callar; y ampliar el glob para que un negativo no pueda
  esconderse en un fichero que no sea `run_*.py`. Convierte "invisible silencioso" en
  "missing ruidoso".
- **R2 (aceptar el conjunto marcado como DoD):** si se decide que el inventario cubre solo el
  conjunto marcado, entonces satisfacer el acceptance #3 clausula 2 ENROLANDO (o listando como
  pendiente-rastreado, no mudo) los negativos reales que YA existen en la suite
  (`attestation_negative_cases`, etc.), en vez de reportar `missing=0` como si no existieran.

Gates afectados por cualquiera de las dos: `scripts/check_falsification_contracts.py`,
`scripts/test_falsification_contracts.py` (anadir caso: negativo real sin marker -> ROJO; y
negativo en fichero no-`run_*` -> visible o ROJO), espejo `scripts/new_instance.py`, paso de
CI. Re-juicio del Analista antes del commit de cierre: re-correr B y C (deben pasar a ROJO),
confirmar A/D/E siguen ROJO, base + gates de protocolo verdes en clon limpio.

## Residuales declarados

- **R-Q1b (menor, sin cambios, diferible):** el chequeo de frontera sigue siendo
  presencia-de-subcadena (`if boundary not in source`), no liveness. Una frontera conservada
  pero vuelta vacua (`assert True or (...)`) no la caza el inventario. Limite conocido de
  iteracion 1; no es el bloqueante de hoy.
- Fondo intocable (protocol.config pineado, dataset N=500): fuera de alcance, no tocado.

-- Analista
