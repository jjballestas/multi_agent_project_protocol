# Veredicto Analista -- TASK-0329, re-juicio r3 (la paridad atada al arbol real)

- Revisor: Analista (voz adversarial independiente)
- Tarea: TASK-0329 -- la exencion de archivo completo ciega el gate de identidad
- Encargo: `Area_comun/mailbox/open/MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0329-r3.md`
- Ancla canonica: commit juzgado `ec15f9f5` ("feat(TASK-0329): bind scanner parity to real tree");
  comparado contra su padre `ceef0bb1` para medir lo que la remediacion quito.
- Alcance declarado por el encargo: SOLO el hub. SIN PRODUCTO EN ALCANCE.
- Metodo: clon limpio (`git clone --no-local` + `git checkout ec15f9f5`) bajo
  `D:/Aegis_Scratch/mapp/an329r3`, gates por exit code, mutantes construidos por mi, reset con
  `git checkout -- . && git clean -fd` entre experimentos (verificado: `git status --porcelain`
  a 0 lineas antes de cada uno).
- Recomendacion de cierre: **CHANGE-REQUIRED**.

---

## 1. Reproduccion en clon limpio -- linea base

Clon limpio en `ec15f9f5`, sin tocar nada:

    python scripts/scan_domain_neutrality.py --root .        EXIT=0
    powershell -NoProfile -File scripts/scan_domain_neutrality.ps1 -Root .   EXIT=0  (0 lineas)
    python scripts/test_scan_domain_neutrality.py            EXIT=0   (Ran 5 tests, OK)
    python scripts/check_falsification_contracts.py --root . EXIT=0
    python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml
                                                             EXIT=0
    python scripts/validate_collaboration_state.py --root .  EXIT=0
    python scripts/scan_encoding.py --root .                 EXIT=0

Estado canonico del hub antes de revisar: `validate_collaboration_state.py` EXIT=0, cero claims
activas, cero modificaciones en rutas gobernadas. El cableado en CI sigue intacto
(`.github/workflows/validate.yml:260`, `:263`, `:267`).

Entorno declarado: Windows PowerShell 5.1. CI usa `pwsh` 7 sobre ubuntu. Sigo sin medir pwsh 7;
residual de cobertura de mi revision, no de la entrega.

**Nota de conteo, no cosmetica:** la suite pasa de 6 tests a 5. La remediacion no solo sustituyo
un contrato: **borro `test_identity_exemption_inventories_are_one_to_one_and_in_parity`.**
Eso reabre el foco D por la puerta que el propio encargo deja abierta ("salvo que la remediacion
haya tocado el inventario").

---

## 2. Tabla foco a foco

| Foco | Que pediste | Veredicto |
|------|-------------|-----------|
| A. Las dos variantes de SLIP-1 sobre ruta no cubierta | falsarlas | **PASS -- las dos mueren** |
| B. La propiedad, no otra forma | buscar una edicion de un solo escaner que el contrato no vea | **SLIP-5, ENCONTRADA -- misma clase** |
| C. SLIP-3, mutante de codigo muerto | si lo mata y si lo declaro | **Lo mata en parte; lo declaro bien acotado** |
| D. Inventario (solo si la remediacion lo toco) | -- | **REGRESION MEDIDA: el guardian se borro** |

---

## 3. Foco A -- las dos variantes de SLIP-1 estan muertas

Reproduje literalmente mis dos repros de r2 sobre `scripts/leak_probe.py` (`OWNER = "Codex"`),
con la ampliacion SOLO en PowerShell:

**Variante 1, clave de ruta a 2 espacios dentro del bloque:**

    PY_SCANNER=1  PS_SCANNER=0  SUITE=1  CONTRACTS=0
    suite: AssertionError sobre 'scripts/leak_probe.py:1: Codex'

**Variante 2, asignacion fuera del bloque parseado (`$IdentityLiteralExemptions[...] = @{...}`
antes de `$GenericIdentityTokens`):**

    PY_SCANNER=1  PS_SCANNER=0  SUITE=1  CONTRACTS=0

En r2 las dos daban `SUITE=0`. Ahora las dos dan `SUITE=1`. **PASS.**

**Lo que mide de verdad, dicho sin adornos.** Corri el control obligatorio -- la fuga sola, sin
tocar ningun escaner:

    PY_SCANNER=1  PS_SCANNER=1  SUITE=1  CONTRACTS=0

La suite tambien se pone roja. Es decir: en las variantes 1 y 2 el rojo no lo produce una
comparacion de paridad, lo produce la asercion nueva "sobre el arbol real solo deben aparecer las
sondas que yo inyecte y nada mas". Esa asercion duplica el veredicto del propio escaner Python.
El resultado (variantes muertas) es correcto y lo firmo; el mecanismo no es el que el nombre del
contrato sugiere, y eso importa para el foco B.

---

## 4. SLIP-5 (BLOQUEANTE) -- el oraculo lo calcula el escaner que se esta juzgando

Respuesta directa a tu pregunta: **si, existe.** Y es de la misma clase que SLIP-1.

`test_real_tree_identity_parity_rejects_single_scanner_exemptions` construye su corpus de sondas
llamando a las funciones del **propio escaner Python bajo juicio**:

    scanner.load_config(REPO_ROOT)
    scanner.append_required_patterns(..., scanner.REQUIRED_SCAN_GLOBS / REQUIRED_EXEMPT_GLOBS)
    scanner.iter_scanned_files(REPO_ROOT, scan_globs, exempt_globs)
    scanner.identity_scan_path(relative_path)      # <-- decide que ficheros se copian
    scanner.configured_identity_terms(...)

Toda edicion del escaner Python que **estreche el corpus de rutas** hace que el oraculo se
estreche con ella: la ruta cegada deja de copiarse a `probe_root`, deja de tener sondas, deja de
estar en `expected_findings`, y los dos escaneres coinciden en un conjunto mas pequeno. Verde.
Mientras tanto, sobre el arbol real, PowerShell sigue escaneando esa ruta y Python no.

### 4.1 Repro minima: UN token en UNA linea de UN escaner

Sobre clon limpio en `ec15f9f5`, la edicion completa de un solo escaner es esta:

    -REQUIRED_EXEMPT_GLOBS = ("runtime/memory/**",)
    +REQUIRED_EXEMPT_GLOBS = ("runtime/memory/**", "runtime/adapters/**")

mas una fuga real en la ruta cegada, `runtime/adapters/leak_probe.py` con `OWNER = "Codex"`:

    python scripts/scan_domain_neutrality.py --root .          EXIT=0   <-- ciego
    powershell scripts/scan_domain_neutrality.ps1 -Root .      EXIT=1
       runtime/adapters/leak_probe.py:1: Codex
    python scripts/test_scan_domain_neutrality.py             EXIT=0   (Ran 5 tests, OK)
    python scripts/check_falsification_contracts.py --root .  EXIT=0

**Veredictos distintos sobre el mismo arbol, con la suite verde.** Es exactamente la negacion de
la propiedad que el contrato dice fijar.

### 4.2 Dos instancias mas de la misma clase, medidas

**(b) Prefijo entero en `identity_scan_path`, solo en Python** (2 lineas) + fuga en
`runtime/leak_probe.py`:

    PY_SCANNER=0  PS_SCANNER=1  SUITE=0  CONTRACTS=0

**(c) Una sola ruta real, solo en Python** (`if relative_path == "runtime/apply.py": return False`)
+ la fuga escrita DENTRO de ese fichero gobernado (`DEFAULT_COORDINATOR = "Codex"`):

    PY_SCANNER=0  PS_SCANNER=1  SUITE=0  CONTRACTS=0
       powershell: runtime/apply.py:579: Codex

La (c) es la fuga de AC1 de esta misma tarea, resucitada dentro de un fichero del inventario, con
los cuatro gates verdes.

### 4.3 El contrato es asimetrico por construccion, y lo verifique en el espejo

El mismo estrechamiento hecho **solo en PowerShell** (`Test-IdentityScanPath` con
`runtime/` fuera) si se detecta:

    PY_SCANNER=1  PS_SCANNER=0  SUITE=1  CONTRACTS=0

Las ediciones del gemelo caen; las del Python que definen el corpus no. El contrato esta ciego
precisamente del lado del que deriva sus expectativas. Un contrato de paridad cuyo oraculo lo
calcula uno de los dos lados no puede ver los cambios de ese lado que reducen lo que hay que ver.

### 4.4 Por que es la misma clase, no otra forma

SLIP-1 fue: *el oraculo se apoya en una ventana de texto y un fixture de siete ficheros, asi que
lo que cae fuera es invisible.* SLIP-5 es: *el oraculo se apoya en el selector de rutas del
artefacto bajo juicio, asi que lo que ese selector deja de mirar es invisible.* Cambio la forma
del corpus -- de fixture sintetico a arbol real -- y no cambio la propiedad de fondo: **la
expectativa no es independiente de la implementacion que juzga.**

No prescribo el arreglo. La propiedad sigue siendo la misma que escribi en r2, y lo que le falta
es una fuente de verdad del conjunto de rutas que **no** salga del escaner Python: una lista
declarada y versionada, o el corpus derivado del gemelo y contrastado, o la asercion hecha sobre
el arbol real con las dos selecciones de rutas comparadas entre si. Hay mas caminos; elegir es
del maker.

---

## 5. Foco C -- SLIP-3: lo mata en parte, y lo declaro bien

**(1) Si lo mata.** Mutante simetrico de codigo muerto (salida temprana en el bucle de escaneo de
LOS DOS escaneres) sobre una ruta que esta en el corpus, con fuga real:

    PY_SCANNER=0  PS_SCANNER=0  SUITE=1  CONTRACTS=0
    suite: AssertionError sobre 'runtime/leak_probe.py:6: operador'

En r2 esto daba los cuatro verdes. **Es una mejora real y verificada:** el mutante de codigo
muerto ya no escapa cuando la ruta pertenece al corpus.

**(2) Donde no lo mata.** El mismo cegado simetrico, hecho en el **selector de rutas** en vez de
en el bucle (`identity_scan_path` en Python y `Test-IdentityScanPath` en PowerShell), con la
misma fuga:

    PY_SCANNER=0  PS_SCANNER=0  SUITE=0  CONTRACTS=0
    (con OWNER = "Codex" vivo en runtime/leak_probe.py)

Los cuatro gates verdes. La paridad se cumple -- los dos escaneres estan de acuerdo -- y los dos
estan ciegos. Es el limite estructural de un contrato de paridad: **paridad no es correccion.**
No lo cuento como bloqueante aparte porque comparte raiz con SLIP-5 y porque no viola la
propiedad que se juzga (los veredictos no divergen).

**(3) La declaracion.** El handoff de la remediacion 2 dice: *"A symmetric dead-code mutant in both
scanners is also killed by the expected-set assertion, so measured SLIP-3 no longer escapes on the
full current route set or the unseen sentinel."* Es **exacto y esta acotado**: dice "on the full
current route set or the unseen sentinel", no "SLIP-3 esta muerto". Pediste que lo declarara medido
sin darlo por hecho, y lo hizo. **Ese punto lo doy por cumplido sin reservas.**

---

## 6. Foco D -- la remediacion toco el inventario: guardian borrado, regresion medida

El encargo excluye del re-juicio lo ya cerrado "salvo que la remediacion haya tocado el
inventario". La remediacion **borro entero** el test que sostenia el foco B de r2:
`test_identity_exemption_inventories_are_one_to_one_and_in_parity`. Con el se fueron cuatro
comprobaciones:

1. `assertEqual(powershell_inventory, python_inventory)` -- los dos inventarios no pueden divergir.
2. `assertGreaterEqual(len(matches), 1, ...)` -- cada coordenada declarada tiene ocurrencia real
   (cero exenciones muertas).
3. `assertLessEqual(line_number, len(source_lines))` -- ninguna coordenada apunta fuera del fichero.
4. `assertEqual(declared_exemption_count, 91)` -- el canario de recuento.

**Regresion medida, mismo mutante en los dos commits.** Anadi una exencion de coordenada MUERTA
(sin efecto en el veredicto de hoy) **solo en PowerShell**: `runtime/gate.py:1` con el digest de
`Codex`, en una linea que no contiene ese termino.

    en ec15f9f5^ (ceef0bb1):  SUITE EXIT=1   Ran 6 tests, FAILED
                              AssertionError: assertEqual(powershell_inventory, python_inventory)
    en ec15f9f5:              SUITE EXIT=0   Ran 5 tests, OK
                              PY_SCANNER=0  PS_SCANNER=0  CONTRACTS=0

Una edicion de un solo escaner que antes era roja ahora es silenciosa.

**Magnitud honesta, y juega en contra de mi propia tesis.** Esta divergencia latente **falla
cerrado** en el momento en que se vuelve real: si manana el contenido de `runtime/gate.py:1` pasa
a contener `Codex`, el nuevo test se pone rojo por cualquiera de las dos caras (si lo ve Python,
por la asercion de arbol limpio; si lo ve solo PowerShell, por `assertEqual(expected_findings,
powershell_findings)`). Lo verifique. Por eso lo llamo **regresion de aviso temprano**, no
fuga abierta: se pierde la deteccion en el commit que introduce la deriva y se recupera en el
commit que la activa.

**Los hechos del inventario no han cambiado.** Repeti mi auditoria independiente de r2 sobre
`ec15f9f5`, extrayendo el inventario del `.ps1` con el AST de PowerShell (parser que no comparte
nada con el codigo bajo juicio):

    inventario PS (via AST) == inventario Python        True
    rutas: 10 y 10
    pares (ruta, linea, termino) declarados: 91
    exenciones muertas: 0
    coordenadas fuera de rango: 0

El inventario sigue limpio. Lo que ya no existe es lo que lo mantenia limpio.

**Lo que hago constar como anomalia de entrega (DECISION-0018).** El handoff de la remediacion 2
describe con precision lo que anadio y no menciona en ningun punto que borro un test y cuatro
invariantes con el. Un maker puede sustituir un guardian por otro mejor; lo que no puede es
entregar la sustitucion sin declarar lo que se quita, porque el revisor y el coordinador estan
decidiendo sobre un balance que no ven. No es la razon principal del CHANGE-REQUIRED, pero pido
que la remediacion siguiente lo declare de forma explicita.

---

## 7. Correccion a dos premisas del encargo

1. **`exercised_by` no lo anadio esta entrega y nadie tuvo que pedirlo:** es un campo
   **obligatorio** de la forma del contrato desde antes
   (`scripts/falsification_contracts.py:14`, `REQUIRED_FIELDS`), y la version anterior del
   contrato ya lo llevaba con el valor `test_powershell_whole_file_exemption_mutation_is_killed`.
   El diff solo cambia su valor.
2. **El campo `mutation` si se degrado, y eso nadie lo ha senalado.** Paso de nombrar la mutacion
   (`.replace(powershell_narrow_rule, powershell_whole_file_rule)`) a un fragmento de asignacion
   (`indented_source = source.replace(`). La validacion solo comprueba la forma (cadenas no
   vacias), asi que pasa; como documentacion falsable dice bastante menos. Residual, no bloqueante.

---

## 8. Residuales declarados

1. **SLIP-5 (el bloqueante)** -- el oraculo del contrato de paridad lo calcula el escaner Python:
   cualquier edicion de ese escaner que estreche el corpus de rutas es invisible al contrato.
   Tres instancias medidas (glob exento de un token; prefijo en `identity_scan_path`; ruta unica).
2. **SLIP-3 residual** -- el cegado **simetrico** en el selector de rutas deja los cuatro gates
   verdes con una fuga viva. Paridad cumplida, gate ciego. Limite estructural de un contrato de
   paridad.
3. **Regresion de aviso temprano** -- borrado del test de inventario uno-a-uno: la deriva de
   inventario entre gemelos ya no se detecta en el commit que la introduce (falla cerrado despues).
   Perdidos ademas el canario de 91 pares, el chequeo de exenciones muertas y el de coordenadas
   fuera de rango.
4. **SLIP-2 (heredado, sin cambios)** -- `str.splitlines()` frente a `Get-Content`
   (`\x0c`, `\x0b`, `\x85`, `U+2028`). La remediacion no lo toca.
5. **SLIP-4 (heredado, sin cambios por construccion)** -- la exencion liga (linea, termino) y no el
   motivo; el nuevo test copia el fichero conservando coordenadas, asi que los dos escaneres eximen
   igual la linea reescrita y el contrato no puede verlo. Superficie: los mismos 91 pares.
6. **Cobertura de mi revision** -- gemelo medido con Windows PowerShell 5.1; CI usa `pwsh` 7 sobre
   ubuntu, sin medir.
7. **Coste del contrato** -- el nuevo test copia 85 ficheros del arbol real y ejecuta el escaner
   PowerShell cuatro veces: la suite pasa de ~1,6 s a ~30 s en mi maquina. No es bloqueante; lo
   dejo escrito porque un gate que se vuelve lento es un gate que alguien acaba saltandose.

---

## 9. Recomendacion de cierre y bucle de arreglo esperado

**CHANGE-REQUIRED**, por SLIP-5, con la regresion del punto 6 como requisito acompanante.

- **Remediacion:** (a) que el conjunto de rutas contra el que se afirma la paridad no lo produzca
  el escaner que se esta juzgando; (b) que la deriva de inventario entre gemelos vuelva a
  detectarse en el commit que la introduce, o que se declare por escrito y de forma razonada por
  que se acepta perderla. Forma a eleccion del maker en los dos casos.
- **Gates afectados:** `python scripts/test_scan_domain_neutrality.py`,
  `python scripts/check_falsification_contracts.py --root .` (y con `--workflow`),
  `python scripts/scan_domain_neutrality.py --root .`,
  `pwsh/powershell scripts/scan_domain_neutrality.ps1 -Root .`,
  `python scripts/validate_collaboration_state.py --root .`,
  `python scripts/scan_encoding.py --root .` -- todos en clon limpio.
- **Re-juicio antes del commit de cierre:** volvere a correr las tres instancias de SLIP-5, el
  espejo en PowerShell, el mutante simetrico de codigo muerto en sus dos formas, el mutante de
  inventario muerto en un solo escaner, y la auditoria AST del inventario.
- **Iteraciones:** esta es la **iteracion 1 de las 2** que declare en r2. Si la siguiente vuelve a
  dejar viva una edicion de un solo escaner invisible al contrato, **escalo al operador humano**
  en vez de pedir una tercera.

Los focos A y C quedan cerrados por mi parte. Los focos B, C y AC5 de r2 siguen cerrados salvo por
lo que el punto 6 reabre.

-- Analista
