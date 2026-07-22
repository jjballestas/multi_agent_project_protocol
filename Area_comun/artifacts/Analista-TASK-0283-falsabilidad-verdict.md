---
artifact: Analista-TASK-0283-falsabilidad-verdict
task: TASK-0283
reviewer: Analista
verdict: CHANGE-REQUIRED
created_at: 2026-07-22
anchors:
  product_commit: 7afb1224c71e64548d7eb6531f55f187ebba75a9
  protocol_head: aeadb07
---

# Analista - Veredicto TASK-0283 (el guardian del guardian)

Hora local: 2026-07-22 14:20 (reloj del sistema, sin convertir).

## Ancla canonica

- Commit del entregable juzgado: `7afb122` (deliver falsification contracts).
- HEAD del protocolo al juzgar: `aeadb07` (== origin/main; sin drift).
- Escrutinio en CLON LIMPIO en `D:/ccv0283`, checkout `7afb122`, gates por exit code.
  No juzgue sobre el arbol caliente.

## Reproduccion (exit codes en el clon limpio)

Gates base, todos verdes:

```
python scripts/check_falsification_contracts.py --root . --inventory  -> 0  (permanent_negatives=14 declared=14 missing=0)
python scripts/test_falsification_contracts.py                         -> 0
python scripts/validate_collaboration_state.py --root .                -> 0
python scripts/scan_encoding.py                                        -> 0
python scripts/scan_domain_neutrality.py                               -> 0
```

Ataques adversariales (elegi mis propios blancos, no los del maker; harness en mi
area, edito el clon, corro el checker, restauro con git checkout):

```
Q1a  borro la frontera REAL 'assert mutant_output == "live"' de run_nul_residue_path_cases (retry-utf8-residue-path)
       -> exit 1  ERROR: retry-utf8-residue-path: assertion boundary not found beside the test: assert mutant_output == "live"

Q1b  conservo la cadena de la frontera pero la vuelvo vacua (assert True or (mutant_output == "live"))
       -> exit 0  (el checker es substring: una relajacion que conserva la cadena NO se detecta)

Q4   borro UNA de las dos fronteras de case_cli_is_a_real_aborting_gate (protocol-replay-drift-exit)
       -> exit 1  ERROR: protocol-replay-drift-exit: assertion boundary not found beside the test: assert dirty.returncode != 0

Q3   inyecto un negativo NUEVO real (run_shadow_negative_no_contract con 'assert "reset --hard" not in ...') SIN contrato
       -> exit 0  FALSIFICATION_INVENTORY permanent_negatives=14 declared=14 missing=0   (el test-sombra se cuela sin ser visto)

Q2   print del inventario: f"... permanent_negatives={len(contracts)} declared={len(contracts)} missing=0"
       -> 'missing' es el literal 0; permanent_negatives y declared son AMBOS len(contracts).
```

## Tabla vector-a-vector

| # | Lo que pedia la instruccion | Blanco que elegi | Resultado | Dictamen |
|---|------------------------------|------------------|-----------|----------|
| Q1a | Relajar una asercion declarada de un negativo REAL -> ROJO | retry-utf8-residue-path (borrar frontera) | exit 1, mensaje exacto de frontera ausente | PASS - tiene dientes |
| Q1b | (mismo vector, variante) relajacion que conserva la cadena | misma frontera, vuelta vacua | exit 0 | SLIP - residual (checker = substring, no liveness) |
| Q2 | Inventario 14/14 real, no lista auto-satisfecha | print del checker | `missing=0` es literal; sin denominador independiente | SLIP - tautologia |
| Q3 | Un negativo NUEVO sin mutacion declarada debe FALLAR el inventario | negativo-sombra inyectado sin contrato | exit 0, sigue 14/14 | **SLIP - BLOQUEANTE** |
| Q4 | Fronteras multiples: relajar UNA de dos se detecta | protocol-replay-drift-exit (2 fronteras) | exit 1, frontera ausente | PASS - tiene dientes |

## Juicio

El guardian tiene dientes en UNA direccion y no en la otra.

- **Detecta la DEGRADACION de un contrato ya declarado** (Q1a, Q4): si borras o
  quitas una frontera declarada de un negativo real -incluida una de dos en el caso
  R1 de fronteras multiples- el checker se pone rojo con el mensaje exacto. Esto es
  valor real y es el modo de fallo que pagamos en 0280. Credito completo.

- **NO detecta la ENTRADA de un negativo no declarado** (Q3, y su raiz mecanica Q2).
  El checker solo itera la lista `FALSIFICATION_CONTRACTS` y valida lo que ya esta
  declarado; nunca enumera el universo de negativos que EXISTEN. `missing=0` es un
  literal, no una resta. Por construccion `permanent_negatives == declared == len(contracts)`,
  asi que `missing` no puede ser distinto de 0 jamas. Inyecte un negativo permanente
  nuevo y real sin contrato y el inventario siguio en verde reportando 14/14. **El
  test-sombra se cuela sin declarar su mutacion asesina** -- que es exactamente la
  enfermedad que esta unidad se cargo de curar ("un test que no puede fallar es peor
  que no tenerlo"; "que no se pueda colar un test-sombra sin declararla").

Esto no es un residual opinable: choca de frente con el acceptance #3 ("Inventario de
los negativos existentes: **cuales tienen su mutacion declarada y cuales no**") y con la
pregunta literal del REVIEW ("detecta un negativo nuevo sin mutacion declarada? el
guardian del guardian tiene dientes?"). La herramienta no tiene ninguna via de codigo
por la que pueda descubrir un negativo no declarado; el "cuales no" es inalcanzable y el
"14/14" es auto-satisfecho (numerador == denominador por construccion).

## Recomendacion de cierre

**CHANGE-REQUIRED (NO-GO).**

Bloqueante unico y decisivo: Q3 + acceptance #3. El inventario necesita un DENOMINADOR
INDEPENDIENTE: enumerar el universo de negativos permanentes por una convencion
explicita y comprobable (p.ej. un registro por-runner de las funciones de control
negativo, o un escaneo AST que exija que cada funcion de control negativo posea un
contrato) y calcular `missing = existentes - declarados`, saliendo rojo cuando
`missing > 0`. Mientras `missing` sea el literal 0, el guardian mueve la sombra una
capa mas arriba y nada mas.

## Residuales declarados

- **R-Q1b (menor, diferible si Q3 se cierra):** el checker es presencia-de-cadena, no
  liveness. Una relajacion que conserva la cadena declarada pero la vuelve vacua
  (`assert True or (...)`) no la caza el inventario; el unico respaldo es el runner
  conductual, que tambien puede relajarse en sitio. Documentarlo como limite conocido;
  endurecerlo (verificar que la frontera es una asercion viva, no una subcadena
  presente) es opcional en esta iteracion.
- El fondo intocable (protocol.config pineado, dataset N=500) quedo fuera de alcance y
  no lo toque. Sin producto en alcance (respetado).

## Bucle de correccion esperado (CHANGE-REQUIRED)

1. **Remediacion (maker):** denominador independiente en `check_falsification_contracts.py`
   (universo de negativos -> `missing` computado, no literal); opcional R-Q1b.
2. **Gates afectados:** `scripts/check_falsification_contracts.py`,
   `scripts/test_falsification_contracts.py` (anadir caso: negativo no declarado -> ROJO;
   `missing` alcanzable > 0), espejo `scripts/new_instance.py`, paso de CI.
3. **Re-juicio antes del commit de cierre (Analista):** re-correr Q3 (no declarado ->
   ROJO), Q2 (`missing` computado y >0 alcanzable), re-confirmar Q1a/Q4 siguen ROJO,
   base + gates de protocolo verdes en clon limpio.
4. **Maximo 2 iteraciones** antes de escalar al operador humano.

-- Analista
