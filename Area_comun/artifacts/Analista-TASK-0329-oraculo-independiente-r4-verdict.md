# Veredicto Analista -- TASK-0329, re-juicio r4 (el oraculo independiente)

- Revisor: Analista (voz adversarial independiente)
- Tarea: TASK-0329 -- la exencion de archivo completo ciega el gate de identidad
- Encargo: `Area_comun/mailbox/open/MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0329-r4.md`
- Ancla canonica: commit de implementacion `1177f67bdaa14dcf293c069fd0f7507aa2fccc62`
  ("test(TASK-0329): make parity oracle independent"); entrega `f276b897`.
  Comparaciones contra `ec15f9f5` (el commit que juzgue en r3).
- Alcance declarado por el encargo: SOLO el hub. SIN PRODUCTO EN ALCANCE.
- Metodo: clon limpio (`git clone --no-local` + `git checkout 1177f67b`) bajo
  `D:/Aegis_Scratch/mapp/an329r4`, gates por exit code, mutantes construidos por mi sobre el
  codigo de PRODUCCION, `git checkout -- . && git clean -fd` entre experimentos
  (`git status --porcelain` a 0 lineas verificado antes de cada uno).
- Hora del juicio: 2026-08-09 19:37 local (UTC+2).
- Recomendacion de cierre: **CHANGE-REQUIRED**, con **escalado al operador humano** (ver seccion 9).

---

## 1. Reproduccion en clon limpio -- linea base

Clon limpio en `1177f67b`, arbol a 0 modificaciones:

    python scripts/scan_domain_neutrality.py --root .                          EXIT=0
    powershell -NoProfile -File scripts/scan_domain_neutrality.ps1 -Root .     EXIT=0
    python scripts/test_scan_domain_neutrality.py                              EXIT=0  (Ran 6 tests, OK)
    python scripts/check_falsification_contracts.py --root .                   EXIT=0
    python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml
                                                                               EXIT=0
    python scripts/validate_collaboration_state.py --root .                    EXIT=0
    python scripts/scan_encoding.py --root .                                   EXIT=0

La suite vuelve de 5 a 6 tests. Estado canonico del hub antes de revisar:
`validate_collaboration_state.py` EXIT=0, cero claims activas (10 entradas, todas `released` o
`blocked`), cero modificaciones en rutas gobernadas.

Entorno: Windows PowerShell 5.1. Sobre la cobertura de `pwsh` 7, ver la seccion 7.

---

## 2. Tabla foco a foco

| Foco | Que pediste | Veredicto |
|------|-------------|-----------|
| A.1 Repetir mi edicion de un token | comprobar que ahora cae | **PASS -- cae** |
| A.2 Otra forma de estrechar el corpus | buscarla | **SLIP-7 en el eje de TERMINOS, verde sin fuga** |
| B. Deteccion de deriva de inventario | restaurada o declarada | **Restaurada y declarada, pero con ventana ciega: SLIP-6, BLOQUEANTE** |
| C. Campo `mutation` degradado | si se declaro | **Se declaro, pero la declaracion no describe lo entregado** |
| D. Sin regresion (2 variantes SLIP-1, 91 pares) | verificar | **PASS -- sin regresion** |

---

## 3. Foco A.1 -- las tres instancias de SLIP-5 estan muertas

Repeti literalmente los tres mutantes de r3 sobre el codigo de produccion, cada uno con una fuga
real de identidad, cada uno sobre clon limpio recien reseteado:

**(a) La edicion de UN token que medi en r3** -- `REQUIRED_EXEMPT_GLOBS` mas
`"runtime/adapters/**"` en el escaner Python, mas `runtime/adapters/leak_probe.py` con
`OWNER = "Codex"`:

    PY_SCANNER=0   PS_SCANNER=1   SUITE=1  (FAILED, failures=1)

En r3 esto daba `SUITE=0`. **Cae.**

**(b) Prefijo entero fuera de `identity_scan_path`, solo en Python** (`runtime/` neutralizado) mas
`runtime/leak_probe.py` con `OWNER = "Codex"`:

    PY_SCANNER=0   PS_SCANNER=1   SUITE=1

**(c) Una sola ruta real, solo en Python** (`if relative_path == "runtime/apply.py": return False`)
mas la fuga escrita DENTRO de ese fichero gobernado:

    PY_SCANNER=0   PS_SCANNER=1   SUITE=1
    powershell: runtime/apply.py:579: Codex

Las tres caen. El mecanismo es real y general, no un caso especial cosido a mi repro: el corpus de
rutas lo produce ahora `identity_contract_paths()`
(`scripts/test_scan_domain_neutrality.py:84-101`), un selector de sistema de ficheros versionado en
el propio test que no importa ningun escaner ni lee sus globs, su iterador de rutas ni su predicado
de identidad. Cualquier ruta que el escaner Python deje de mirar sigue copiandose a `probe_root`
con sus sondas, y la asercion `assertEqual(expected_findings, python_findings)` lo delata.

**El eje de RUTAS del oraculo si quedo independiente. Lo firmo.**

---

## 4. SLIP-6 (BLOQUEANTE) -- el oraculo de inventario vuelve a ser una ventana de TEXTO

Respuesta directa a tu pregunta *"queda alguna via por la que editar un solo escaner estreche
tambien el oraculo?"*: **si.** No en el contrato de paridad de rutas, sino en el que se restauro
para el foco B.

`powershell_identity_inventory()` (`scripts/test_scan_domain_neutrality.py:188-221`) no lee el
inventario del gemelo: escribe una **copia instrumentada** del `.ps1` insertando una sonda
justo ANTES del marcador de texto `$GenericIdentityTokens = @(`, y esa sonda termina en `exit 0`.
Todo lo que el escaner real ejecuta DESPUES de ese marcador y antes del bucle de escaneo -- las
lineas 141 a 322 del `.ps1` -- es **activo en produccion e invisible para el oraculo**.

### 4.1 El experimento decisivo: una misma mutacion, tres colocaciones

Mutante identico en los tres casos -- una coordenada de exencion MUERTA anadida **solo a
PowerShell** (`runtime/gate.py:1` con el digest de `Codex`). Solo cambia donde se escribe:

| Colocacion | PS_SCANNER | SUITE | Resultado |
|------------|-----------|-------|-----------|
| dentro del bloque literal, con 2 espacios de indentacion | 0 | **1** | detectado |
| fuera del bloque, ANTES de `$GenericIdentityTokens = @(` | 0 | **1** | detectado |
| fuera del bloque, DESPUES de `$GenericIdentityTokens = @(` | 0 | **0** | **ESCAPA** |

Los siete gates en verde en el tercer caso:

    python scripts/scan_domain_neutrality.py --root .          EXIT=0
    powershell scripts/scan_domain_neutrality.ps1 -Root .      EXIT=0
    python scripts/test_scan_domain_neutrality.py              EXIT=0  (Ran 6 tests, OK)
    python scripts/check_falsification_contracts.py --root .   EXIT=0

### 4.2 La deriva escondida es ACTIVA, no cosmetica

Con esa exencion invisible viva, cree `runtime/gate.py` con `OWNER = "Codex"` en la linea 1:

    python  scan_domain_neutrality.py   EXIT=1   runtime/gate.py:1: Codex
    powershell scan_domain_neutrality.ps1  EXIT=0   (ni una linea sobre gate.py)

PowerShell esta **realmente ciego** en esa coordenada. El gemelo diverge del original y el contrato
que existe para verlo dice OK.

### 4.3 La asimetria es del oraculo, no de los escaneres

Hice la misma deriva por el lado Python -- asignacion `IDENTITY_LITERAL_EXEMPTIONS["runtime/gate.py"] = {...}`
despues de la definicion, al final del modulo:

    SUITE=1   (detectado)

El inventario Python se lee por importacion, asi que ve el diccionario **efectivo**; el inventario
PowerShell se lee por una copia truncada en un marcador de texto, asi que ve solo un **prefijo del
fichero**. Un lado se juzga por su estado real y el otro por donde cae una cadena.

### 4.4 Por que esto invalida la declaracion del handoff, y por que es la misma clase

El handoff de la remediacion 3 afirma:

> *"The restored comparison executes an instrumented copy of the PowerShell declarations and reads
> their effective hashtable. It therefore sees indentation changes and **assignments outside the
> initial literal block**."*

y

> *"A new permanent negative adds a dead coordinate only to PowerShell and **proves the divergence
> is visible immediately, before the coordinate becomes active**."*

La primera frase es **falsa como propiedad general**: ve las asignaciones fuera del bloque solo si
caen antes del marcador. La segunda es el criterio que el propio maker se puso para el foco B, y no
se cumple para la colocacion de la fila 3.

Y es exactamente la clase que llevo tres rondas midiendo. SLIP-1 fue *el oraculo se apoya en una
ventana de texto*. SLIP-5 fue *el oraculo se apoya en el selector de rutas del artefacto juzgado*.
SLIP-6 es *el oraculo se apoya, otra vez, en una ventana de texto* -- ahora la del punto de
instrumentacion. La remediacion movio la ventana; no la elimino.

### 4.5 Magnitud honesta, y juega en contra de mi tesis

Con la deriva viva y `runtime/gate.py` conteniendo el termino, la suite se pone roja
(`SUITE=1`) por el lado Python de la asercion de arbol real. Es decir: **falla cerrado en el commit
que activa la coordenada**, no en el que la introduce. La superficie es identica en magnitud a la
regresion de aviso temprano que reporte en r3 -- y ese aviso temprano es literalmente el
entregable del foco B. La deteccion inmediata no se perdio por borrar el guardian; se perdio por
donde mira el guardian restaurado.

---

## 5. SLIP-7 (no bloqueante, declarado) -- el eje de TERMINOS sigue saliendo del escaner juzgado

Pediste otra forma de estrechar el corpus que no fuera la que medi. La hay: el corpus es
(rutas x terminos), y solo el eje de rutas quedo independiente. El eje de terminos se sigue
calculando con el escaner bajo juicio --
`scanner.configured_identity_terms(scanner.load_config(REPO_ROOT))`
(`scripts/test_scan_domain_neutrality.py:331`, y otra vez en `:503`). Las lineas sonda que se
inyectan en cada fichero copiado son una por termino: menos terminos, menos sondas, y las dos
partes del contrato se encogen a la vez.

**Medido.** Con un cuarto agente en el registro (`Vigia`, sin coordenadas declaradas en el
inventario) y una edicion de un token en el escaner Python -- el minimo de longitud del id de
registro de `3` a `6`, que no escribe ningun literal de identidad:

    escaner Python: el termino desaparece de su lista de identidades
    PY_SCANNER=0   PS_SCANNER=0   SUITE=0 (Ran 6 tests, OK)   CONTRACTS=0

El escaner Python queda ciego a una identidad configurada y el contrato de paridad no lo ve.
Cuando anado la fuga (`runtime/leak_probe.py` con `REVIEWER = "Vigia"`) si cae
(`PY=0 PS=1 SUITE=1`): tambien falla cerrado, no es fuga abierta.

**Por que hoy no es bloqueante, y por que no me tranquiliza.** Con los cinco terminos actuales el
mismo experimento SI cae (`SUITE=1`), pero por una razon accidental: el test de inventario
comprueba `assertIn(digest, terms_by_digest)`, y los cinco terminos configurados tienen
casualmente coordenadas declaradas entre los 91 pares. En cuanto un agente registrado no tenga
exenciones -- que es el estado normal de cualquier alta futura -- ese ancla desaparece. Es un
invariante por accidente, no un invariante declarado. Lo dejo escrito para que la proxima
remediacion no lo descubra por sorpresa.

---

## 6. Foco C -- el campo `mutation`: declarado, pero la declaracion no describe lo entregado

Se declaro, y eso lo doy por cumplido: el handoff dedica un parrafo al asunto. Lo que no cuadra es
el contenido. El handoff dice:

> *"This delivery explicitly replaces it with the executable Python route-exemption mutation."*

El diff real (`git diff ec15f9f5 1177f67b -- scripts/test_scan_domain_neutrality.py`):

    -        "mutation": "indented_source = source.replace(",
    +        "mutation": "narrowed_python_source = python_source.replace(",
    +        "mutation": "mutated_powershell_source = powershell_source.replace(",

El valor sigue siendo un fragmento de asignacion, de la misma forma degradada que sustituye; solo
cambia el nombre de la variable. Y el contrato nuevo nace con un segundo ejemplar de la misma
forma. Compara con los dos contratos sanos del mismo fichero -- `.replace(identity_rule,
restricted_rule)` y `.replace(narrow_rule, whole_file_rule)` -- que si nombran la mutacion.
`check_falsification_contracts.py` solo valida la forma (cadena no vacia), asi que pasa.

**Residual, no bloqueante.** Lo hago constar como discrepancia entre entrega y declaracion
(DECISION-0018), no como defecto de codigo.

---

## 7. Foco D -- sin regresion

**Las dos variantes de SLIP-1 siguen muertas.** Con `scripts/leak_probe.py` (`OWNER = "Codex"`):

    control (solo la fuga, sin tocar escaneres):  PY=1  PS=1  SUITE=1
    variante 1 (exencion PS indentada 2 espacios): PY=1  PS=0  SUITE=1
    variante 2 (asignacion PS fuera del bloque, antes del marcador): PY=1  PS=0  SUITE=1

**Los 91 pares intactos.** Repeti mi auditoria independiente extrayendo el inventario del `.ps1`
con el AST de PowerShell (parser que no comparte nada con el codigo bajo juicio) y comparandolo
contra el diccionario efectivo de Python:

    inventario PS (via AST) == inventario Python   True
    rutas: 10 y 10
    pares (ruta, linea, termino) declarados: 91
    exenciones muertas: 0
    coordenadas fuera de rango: 0
    digests sin identidad configurada: 0

El mismo AST confirma que en `1177f67b` hay **exactamente una** asignacion que toca
`$IdentityLiteralExemptions`, en la linea 6 -- es decir, hoy no existe deriva escondida; lo que
existe es la ventana por la que podria entrar sin ser vista.

**El test de inventario volvio con sus cuatro invariantes** (igualdad de inventarios efectivos,
coordenada dentro del fichero, digest mapeado a identidad configurada y presente en la linea,
canario de 91). Y el borrado previo se declaro por escrito en el handoff, que era lo que pedi en
r3. Ese punto lo doy por cumplido.

---

## 8. Residuales declarados

1. **SLIP-6 (el bloqueante)** -- el oraculo del inventario PowerShell se lee por una copia
   instrumentada truncada en el marcador de texto `$GenericIdentityTokens = @(`. Toda declaracion
   colocada despues del marcador es activa e invisible. Medido: misma mutacion, tres colocaciones,
   una escapa con siete gates verdes. Falla cerrado cuando la coordenada se activa.
2. **SLIP-7** -- el eje de terminos del oraculo de paridad sigue derivando del escaner juzgado
   (`:331`, `:503`). Anclado hoy solo por accidente (los cinco terminos tienen coordenadas en el
   inventario); se desancla en cuanto se registre un agente sin exenciones.
3. **SLIP-3 residual (heredado)** -- el cegado **simetrico** en el selector de rutas deja los gates
   verdes con una fuga viva. Paridad cumplida, gate ciego. Limite estructural: paridad no es
   correccion.
4. **SLIP-2 (heredado, sin cambios)** -- `str.splitlines()` frente a `Get-Content` (`\x0c`, `\x0b`,
   `\x85`, `U+2028`). La remediacion no lo toca; el nuevo test ademas **normaliza** las copias con
   `splitlines()` + `"\n".join(...)`, asi que el corpus del contrato no puede exhibir esa clase.
5. **SLIP-4 (heredado, sin cambios por construccion)** -- la exencion liga (linea, termino) y no el
   motivo. Superficie: los mismos 91 pares.
6. **La cobertura de `pwsh` 7 en la que se apoya el handoff no existe ahora mismo.** El handoff
   declara: *"The existing Ubuntu CI surface remains responsible for PowerShell 7 coverage."* Lo
   comprobe: `gh run list -L 200` da **200 de 200 runs en `failure`** desde 2026-08-08T04:29, y la
   anotacion de los tres jobs (`validate`, `falsification-runners`, `powershell-linux-parity`) es
   *"The job was not started because recent account payments have failed or your spending limit
   needs to be increased."* **Ningun job ha llegado a arrancar.** No es un defecto de esta tarea y
   no es la razon de mi veredicto, pero la mitigacion declarada del unico residual de entorno esta
   vacia, y lo reporto como anomalia operativa (DECISION-0018) para el operador humano.
7. **Cobertura de mi revision** -- gemelo medido con Windows PowerShell 5.1.
8. **Coste del contrato** -- la suite tarda ~31 s en verde (copia 85 ficheros del arbol real y
   ejecuta el escaner PowerShell cuatro veces). Sin cambios respecto a r3; sigue sin ser bloqueante.

---

## 9. Recomendacion de cierre y escalado

**CHANGE-REQUIRED por SLIP-6**, y **escalo al operador humano** en lugar de abrir una tercera
iteracion.

En r3 escribi, textualmente: *"esta es la iteracion 1 de las 2 que declare en r2. Si la siguiente
vuelve a dejar viva una edicion de un solo escaner invisible al contrato, escalo al operador humano
en vez de pedir una tercera."* Esta es la iteracion 2 y SLIP-6 es, literalmente, una edicion de un
solo escaner invisible al contrato. Me atengo a mi propia regla.

**Lo que NO estoy diciendo.** No pido revertir. La remediacion 3 es una mejora real y medida: el
eje de rutas del oraculo quedo independiente y las tres instancias de SLIP-5 murieron; el test de
inventario volvio con sus cuatro invariantes y el borrado se declaro. Nada de eso esta en
discusion.

**Lo que si digo.** La clase de defecto -- *el oraculo se ata a una forma textual del artefacto que
juzga* -- va por su tercera reaparicion (SLIP-1, SLIP-5, SLIP-6) y cada remediacion la ha
desplazado en vez de cerrarla. Decidir cuantos ciclos mas se gastan en esto, o si se acepta el
residual por escrito y se cierra, es una decision de coste que corresponde al operador, no a mi.

**Si el operador ordena una remediacion 4, el bucle esperado es:**

- **Remediacion:** (a) que el inventario del gemelo se lea de su estado **efectivo**, no de un
  prefijo de texto -- por ejemplo dejando que el propio `.ps1` emita su tabla bajo un modificador,
  o leyendola con un parser independiente (el AST de PowerShell, como hago en la seccion 7), o
  cualquier forma en la que mover una declaracion de sitio no cambie lo que el oraculo ve;
  (b) que el eje de terminos deje de derivar del escaner juzgado, o que se declare por escrito por
  que se acepta. Forma a eleccion del maker en los dos casos; no prescribo.
- **Criterio de aceptacion que voy a aplicar:** el mutante debe morir **con independencia de donde
  se coloque** la declaracion en el fichero -- cambio de coordenada, de orden y de formato. Si solo
  muere en las colocaciones que enumero aqui, es la misma clase otra vez.
- **Gates afectados:** `python scripts/test_scan_domain_neutrality.py`,
  `python scripts/check_falsification_contracts.py --root .` (y con `--workflow`),
  `python scripts/scan_domain_neutrality.py --root .`,
  `pwsh/powershell scripts/scan_domain_neutrality.ps1 -Root .`,
  `python scripts/validate_collaboration_state.py --root .`,
  `python scripts/scan_encoding.py --root .` -- todos en clon limpio.
- **Re-juicio antes del commit de cierre:** repetire la matriz de tres colocaciones ampliada a
  colocaciones que yo elija en el momento, las tres instancias de SLIP-5, el eje de terminos con un
  agente sin exenciones, las dos variantes de SLIP-1 y la auditoria AST del inventario.

Los focos A.1 y D quedan cerrados por mi parte. El foco B queda cumplido en su forma y fallido en
su criterio. El foco C queda como discrepancia declarada.

-- Analista
