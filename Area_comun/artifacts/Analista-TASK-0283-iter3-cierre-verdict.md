---
artifact: Analista-TASK-0283-iter3-cierre-verdict
task: TASK-0283
reviewer: Analista
verdict: CHANGE-REQUIRED
iteration: 3
remediation_loop: 1 of 2
created_at: 2026-07-22
anchors:
  product_commit: none (SIN PRODUCTO EN ALCANCE)
  reviewed_commit: 8b61b05
  protocol_head: d80b774
---

# Analista - Re-juicio de cierre TASK-0283 iteracion 3 (glob recursivo / caso C)

Hora local: 2026-07-22 16:05 (reloj del sistema, sin convertir).

## Ancla canonica

- Commit del entregable juzgado: `8b61b05` (test: close convention discovery boundary),
  el que cita la instruccion.
- HEAD del protocolo: `d80b774` (== origin/main). Los tres commits posteriores a
  `8b61b05` (a8c6dc0, 4483e48, d80b774) NO tocan los scripts del guardian
  (`check_falsification_contracts.py`, `test_falsification_contracts.py`,
  `new_instance.py`, `falsification_contracts.py`) -- verificado con
  `git diff --stat 8b61b05..origin/main -- <esos scripts>` (vacio). Juzgar en `8b61b05`
  equivale a juzgar en HEAD para el codigo bajo revision.
- Escrutinio en CLON LIMPIO en `D:/c283i3`, checkout `8b61b05`, gates por exit code.
  No juzgue sobre el arbol caliente. Cada ataque lo elegi yo, edite el clon, corri el
  checker y restaure con `git checkout`; arbol restaurado limpio al terminar (git status
  vacio tras cada ataque).
- SIN PRODUCTO EN ALCANCE (respetado; fondo pineado y dataset N=500 no tocados).

## Reproduccion (exit codes en el clon limpio)

Gates base, todos verdes:

```
python scripts/check_falsification_contracts.py --root . --inventory  -> 0  (permanent_negatives=15 declared=15 missing=0)
python scripts/test_falsification_contracts.py                         -> 0  (self-test del maker, OK)
python scripts/validate_collaboration_state.py --root .                -> 0
python scripts/scan_encoding.py                                        -> 0
python scripts/scan_domain_neutrality.py                               -> 0
```

Ataques adversariales (blancos mios):

```
A1) COBERTURA DE FICHERO (caso C): negativo MARCADO real, SIN contrato, en subdirectorio
    profundo y con nombre no estandar, tanto bajo examples/ como bajo scripts/:
      examples/weird/deep/nook/xY_not_run_std.py   (marker A1-EXAMPLES-NOOK)
      scripts/hidden/corner/weirdname_qq.py         (marker A1-SCRIPTS-CORNER)
    -> exit 1  permanent_negatives=17 declared=15 missing=2  (AMBOS visibles y en rojo)

A2a) PLACEMENT: negativo MARCADO real como METODO DE CLASE en un fichero escaneado:
      class ShadowSuite:
          def test_no_reset(self):
              """PERMANENT_NEGATIVE: A2-CLASS-METHOD"""
              output = "safe"
              assert "reset --hard" not in output
    -> exit 0  permanent_negatives=15 declared=15 missing=0   (INVISIBLE: no lo cuenta)

A2b) PLACEMENT: negativo MARCADO real como FUNCION ANIDADA en un fichero escaneado:
      def outer():
          def inner_negative():
              """PERMANENT_NEGATIVE: A2-NESTED-FUNC"""
              output = "safe"
              assert "reset --hard" not in output
    -> exit 0  permanent_negatives=15 declared=15 missing=0   (INVISIBLE: no lo cuenta)

A3) MARCADOR LOAD-BEARING: quito el marker de un negativo YA DECLARADO
    (retry-utf8-residue-path) -> pasa a stale:
    -> exit 1  permanent_negatives=14  ERROR: retry-utf8-residue-path: declared contract
       has no permanent-negative marker   (LOUD; el marker es load-bearing)

A4) REGRESION: relajo una frontera declarada ('assert mutant_output == "live"') en el
    cuerpo de run_nul_residue_path_cases:
    -> exit 1  ERROR: retry-utf8-residue-path: assertion boundary not found beside the
       test: assert mutant_output == "live"   (degradacion de contrato sigue cazada)
```

## Tabla vector-a-vector

| # | Lo que pedia la instruccion | Blanco que elegi | Resultado | Dictamen |
|---|------------------------------|------------------|-----------|----------|
| Base | inventario + self-test + gates verdes | -- | 15/15/0, exit 0 en los 5 gates | PASS |
| A1 (C, cobertura de fichero) | ningun fichero queda fuera del glob | subdir profundo + nombre raro, en examples/ y scripts/ | exit 1, 17/15 missing=2, ambos listados | PASS - C cerrado a nivel de FICHERO |
| A2a (placement metodo) | un negativo MARCADO en fichero escaneado debe verse | metodo de clase con marker | exit 0, 15/15/0, INVISIBLE | **SLIP - BLOQUEANTE: escape NUEVO** |
| A2b (placement anidado) | idem | funcion anidada con marker | exit 0, 15/15/0, INVISIBLE | **SLIP - BLOQUEANTE: escape NUEVO** |
| A3 (marker load-bearing) | quitar el marker -> visible-loud | retry-utf8-residue-path sin marker | exit 1, stale error | PASS |
| A4 (regresion) | degradar contrato declarado -> ROJO | relajar frontera declarada | exit 1, mensaje exacto | PASS |

## Juicio

**Lo que el maker cerro (credito completo, verificado):** el commit `8b61b05` reemplaza el
subconjunto `examples/**/run_*.py` por `rglob("*.py")` sobre `examples/` Y `scripts/`. El
caso C tal como lo formulo la instruccion -- "un fichero en un rincon (subdirectorio raro,
nombre no estandar) que el glob no recorra" -- queda CERRADO: mi vector A1 coloca negativos
marcados en `examples/weird/deep/nook/xY_not_run_std.py` y en
`scripts/hidden/corner/weirdname_qq.py` y AMBOS aparecen (missing=2, exit 1). El marcador es
load-bearing (A3: quitarlo pone stale-loud) y la degradacion de un contrato declarado sigue
cazandose (A4). El self-test del maker anade el control off-glob en `scripts/` y el control
de marcador-invisible. Nada de esto retrocedio. La respuesta a la pregunta del REVIEW por el
EJE que anticipaba (nombre/subdirectorio de fichero) es: caso C cerrado en ese eje.

**Lo que sigue abierto (el bloqueante de esta iteracion, un escape NUEVO y distinto de C):**
el descubrimiento es comprensivo entre FICHEROS pero NO dentro de un fichero. Tanto
`permanent_negatives()` como `function_source()` iteran solo `tree.body` (nodos de nivel de
modulo). Un negativo permanente REAL que lleva el marcador `PERMANENT_NEGATIVE:` correcto en
su docstring, pero escrito como METODO DE CLASE (A2a) o como FUNCION ANIDADA (A2b), es
SILENCIOSAMENTE INVISIBLE: el inventario reporta 15/15/0 y exit 0 como si no existiera.

Por que es bloqueante y no un residual documentable:

1. **No es el caso retirado.** El limite que el operador retiro por indecidible es el
   negativo SIN senal (sin marker): sin senal no se puede inferir intencion. Aqui la senal
   -- el marker -- ESTA PRESENTE y el walk somero la descarta. Es un bug de descubrimiento
   acotado y mecanico, no una indecidibilidad. Cae de lleno en el nucleo DECIDIBLE que el
   acceptance refinado eligio cerrar ("glob comprensivo" + "marcador load-bearing").

2. **Rompe la clausula #2 (marcador load-bearing) por el otro lado.** El self-test prueba
   "sin marker -> invisible". Pero la garantia implicita y necesaria es la conversa: "CON
   marker, en un fichero escaneado -> visible". A2a/A2b la falsan. El marcador es NECESARIO
   pero NO suficiente; hace falta ademas colocacion a nivel de modulo, requisito que NO
   esta escrito en ninguna parte (la doc del checker y el export solo exigen "llevar el
   marcador", sin restringir la colocacion -- verificado por grep: no hay "top-level" ni
   "module-level" en la convencion).

3. **La mitigacion documentada NO lo atrapa.** El limite escrito dice que el negativo sin
   declarar "se caza en revision/CI". Pero aqui el marcador SI esta: un revisor que busca
   marcadores lo VE y asume que esta inventariado, mientras el inventario automatico dice
   verde. Doble falso-seguro -- exactamente la enfermedad que TASK-0283 existe para curar
   (un negativo que parece cubierto y esta mecanicamente muerto). Anadir una frase a la doc
   NO cierra esto, porque el fallo es que un marcador presente pasa desapercibido.

4. **El export lo propaga.** El guardian se exporta via `new_instance.py` a instancias
   nuevas. Las suites de test basadas en clase (unittest.TestCase, clases de pytest) son el
   idioma Python dominante. Una instancia nueva que escriba negativos como metodos con su
   marcador correcto obtendra 15/15/0 verde y creera que sus negativos estan bajo contrato.
   La instruccion #3 pide explicitamente que el limite del EXPORT sea correcto.

## Recomendacion de cierre

**CHANGE-REQUIRED (NO-GO).** Iteracion 3 sobre el acceptance REFINADO; el contador de 2
iteraciones anterior lo reinicio la decision de alcance del operador. Esta es la iteracion
de remediacion **1 de 2** sobre el acceptance refinado antes de escalar al humano.

Basta UNA de estas dos direcciones (el maker no necesita ambas):

- **F1 (descubrir a cualquier profundidad):** en `permanent_negatives()` (y en el emparejado
  `function_source()`) recorrer todo el arbol (`ast.walk(tree)` en vez de solo `tree.body`),
  emparejando por nombre/qualname. Hace el descubrimiento verdaderamente comprensivo dentro
  del fichero; A2a/A2b pasan a visibles/rojo.
- **F2 (fail-closed sobre marcador extraviado):** escanear el texto crudo de cada fichero
  por ocurrencias de `PERMANENT_NEGATIVE:` y cruzarlo contra el conjunto descubierto por el
  walk de nivel de modulo; cualquier marcador presente en el fuente pero no descubierto ->
  ERROR ("marcador en ubicacion no descubierta / no top-level"). Convierte el
  invisible-silencioso en missing-ruidoso Y documenta la colocacion top-level como parte de
  la convencion. Analogo fail-closed de mi R1 de la iteracion 2.

## Bucle de correccion declarado

- **Gates afectados:** `scripts/check_falsification_contracts.py`; su self-test
  `scripts/test_falsification_contracts.py` (anadir DOS casos: negativo marcado como metodo
  de clase Y como funcion anidada -> deben ponerse VISIBLES/ROJO); espejo del export
  `scripts/new_instance.py` (+ doc, si se elige F2, debe enunciar el requisito de
  colocacion); paso de CI.
- **Re-juicio del Analista antes del commit de cierre:** re-correr A2a y A2b (deben pasar a
  visible/rojo), confirmar que A1/A3/A4 siguen sosteniendo, base + gates de protocolo verdes
  en clon limpio.
- **Presupuesto de iteracion:** remediacion 1 de 2 sobre el acceptance refinado; si una
  segunda remediacion no lo cierra, escalo al operador humano.

## Residuales declarados (informativos, NO bloqueantes por si mismos)

- **R-B (retirado por indecidible, confirmado como limite vivo):** un negativo permanente
  REAL SIN marcador sigue invisible por diseno (p.ej.
  `examples/attestation_negative_cases/run_attestation_negative_cases.py`, familia real de
  negativos sin marker, no contada). Es el limite documentado y demostrado; no es el
  bloqueante de hoy. Solo lo dejo anotado para que el escape A2 (marcador PRESENTE) no se
  confunda con este (marcador AUSENTE).
- **R-Q1b (menor, diferible):** el chequeo de frontera sigue siendo presencia-de-subcadena
  (`if boundary not in source`), no liveness; una frontera conservada pero vuelta vacua
  (`assert True or (...)`) no la caza. Limite conocido de iteracion 1.
- Fondo intocable (protocol.config pineado, dataset N=500): fuera de alcance, no tocado.

-- Analista
