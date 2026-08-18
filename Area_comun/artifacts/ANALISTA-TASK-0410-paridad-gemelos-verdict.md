# ANALISTA -- veredicto TASK-0410 (paridad de gemelos, 4 AC + 2 ampliaciones)

- Reviewer: Analista (checker independiente; no implemento, no cierro, no ratifico)
- Fecha: 2026-08-18 18:14 local (UTC+2) / 2026-08-18T16:14:54Z
- Encargo: `Area_comun/mailbox/open/MSG-20260818-Arquitecto-to-Analista-REVIEW-TASK-0410.md`
- Recomendacion de cierre: **CHANGE-REQUIRED** (una ampliacion IN-SCOPE queda a medias, con escape
  reproducible en la plataforma que gatea)

## 1. Ancla canonica

| Cosa | Valor |
|---|---|
| Commit bajo review | `96af63c655922eaa3a12cffb44fe48ad21351ebe` (Codex, 2026-08-18 16:29 +0200) |
| Control historico | `96af63c6^` |
| Clon limpio | `D:/Aegis_Scratch/protocol/r0410/cc` (`git clone -s -n` + `git checkout 96af63c6`) |
| Clon limpio (viejo) | `D:/Aegis_Scratch/protocol/r0410/old` (`git checkout 96af63c6^`) |
| Ficheros tocados | 3 (`scan_domain_neutrality.py`, `.ps1`, `test_scan_domain_neutrality.py`) |

**Fondo intocable -- verificado, NO se toco:**

    sha256(protocol.config.json)[:8] = 2E35F26E    (esperado 2E35F26E)   OK
    protocol_version                 = 1.14.0                           OK
    git diff --stat 96af63c6^ 96af63c6 -- protocol.config.json  ->  0 lineas   OK

## 2. Reproduccion -- puertas por EXIT CODE, en el clon limpio

| Gate | Corridas | Exit | Nota |
|---|---|---|---|
| `python -m unittest scripts.test_scan_domain_neutrality` | 2 | 0 / 0 | 9 tests, 156s la primera |
| `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory` | 1 | 0 | 77/77 declarados |
| `python scripts/scan_encoding.py --root .` | 1 | 0 | |
| `python scripts/scan_domain_neutrality.py --root .` | 1 | 0 | 0 hallazgos |
| `python scripts/validate_collaboration_state.py` | 1 (clon) + 1 (arbol) | 0 / 0 | `OK: collaboration state is valid.` |

**Control historico (el verde NO lo produce el codigo viejo):**

    (en /old, commit 96af63c6^)  python -m unittest scripts.test_scan_domain_neutrality
    -> EXIT 1 ; Ran 6 tests ; FAILED (failures=1)
       File ".../test_scan_domain_neutrality.py", line 536,
         self.assertEqual(python_inventory, powershell_inventory)
       AssertionError: ... c857d09db23e6822e3600bc06ad8d58f92ed62b... ...

El viejo es ROJO por la divergencia exacta que la tarea nombra. El verde es discriminante.

## 3. Cardinal publicado, RE-DERIVADO desde la corrida que gatea

**Unidad: ternas (ruta, linea, digest) del inventario de exenciones de identidad literal.**

    files = 9 | pares (ruta,linea) = 80 | ternas = 88

Antes: Python 92 ternas, PowerShell 91. Se retiran 4 ternas del gemelo Python (3 de
`runtime/context.py` + 1 divergente) y 3 del PowerShell -> **88 == 88**. El 88 sale de la corrida
del test (perturbacion P2: `AssertionError: 88 != 89`), no del arbol caliente.

## 4. Tabla vector por vector

| # | Corte del encargo | Veredicto |
|---|---|---|
| 1 | AC1 -- divergencia por CAUSA, no por conteo | **PASS** |
| 2 | AC2 -- borrado acreditado con el 2x2 de la posicion | **PASS** |
| 3 | AC3 -- negativo por mutacion sobre PRODUCCION, mismo mensaje | **PASS** |
| 4 | AC4 -- detector de coordenadas muertas COMO CLASE | **PASS** (residual declarado) |
| 5 | Cardinal derivado: sospecha de vacuidad | **PASS** (no vacuo; subsumido) |
| 6 | E6 -- masters Markdown escaneados | **PASS** (cardinal 198 NO re-derivable) |
| 7 | RES-3 -- paridad de comportamiento por caja | **SLIPS -- BLOQUEANTE** |

---

### (1) AC1 -- PASS. Premisa del maker verificada, y la respuesta es "las dos cosas"

Identidades REALMENTE escaneadas en `96af63c6`:

    configured_identity_terms(load_config('.'))
    N_TERMS = 5
    ['Analista', 'Arquitecto', 'Codex', 'operador', 'operador humano']

    sha256('claude'.casefold()) = c857d09db23e6822e3600bc06ad8d58f92ed62bc8efd81c753f77048662cb97d
                                  ==  _EXEMPT_TERM_6 borrado

La premisa del maker es CIERTA: el termino de la exencion 92 no esta entre las 5 identidades
configuradas. La divergencia es esa terna, en `scripts/harness/peer_mailbox_cron.ps1:555`, presente
solo en el gemelo Python -> **el gemelo Python era el MAS PERMISIVO**, luego la reparacion correcta
es QUITAR, no copiar al PowerShell. Direccion acreditada.

**Sobre "es no-op o no": es no-op para el ESCANER, y NO es no-op para el TEST.** Medido:

    (escaner) restaurando _EXEMPT_TERM_6 en el .py y comparando hallazgos contra el shipped:
      BASE_EXIT=0 lines=0 | RESTORED_EXIT=0 lines=0 | FINDINGS_IDENTICAL=True
      -> exencion MUERTA: el termino no se busca, la exencion no puede disparar jamas.

    (test)    el control historico de arriba: con la terna presente, EXIT 1 en la asercion de paridad.

Es decir: la exencion no tapaba nada, pero si rompia el gate. AC1 acreditado por causa.

### (2) AC2 -- PASS. 2x2 de la posicion, con la direccion medida

Sonda: `probe_ac2/runtime/context.py` con violaciones ALCANZABLES inyectadas en el hueco exacto que
dejo el borrado (linea 16 = `Codex`, linea 17 = `operador humano`). `runtime/**` esta en
`scan_globs` del config, luego el hueco es alcanzable de verdad.

**Celda A -- escaner SHIPPED (96af63c6), sin la exencion: la violacion debe MORIR.**

    python cc/scripts/scan_domain_neutrality.py --root probe_ac2
      runtime/context.py:16: Codex
      runtime/context.py:17: operador
      runtime/context.py:17: operador humano
      PY_EXIT=1
    powershell -File cc/scripts/scan_domain_neutrality.ps1 -Root probe_ac2
      runtime/context.py:16: Codex
      runtime/context.py:17: operador
      runtime/context.py:17: operador humano
      PS_EXIT=1

**Celda B -- codigo borrado RE-INYECTADO VERBATIM en LOS DOS gemelos: debe SOBREVIVIR.**

    python ac2b/scan_domain_neutrality.py --root probe_ac2          -> PY_EXIT=0  (silencio)
    powershell -File ac2b/scan_domain_neutrality.ps1 -Root probe_ac2 -> PS_EXIT=0  (silencio)

La direccion queda medida: quitando el guardia en AMBAS versiones, la version vieja SUPRIME y la
nueva REPORTA, sobre la misma entrada y en las mismas coordenadas. El borrado era load-bearing y
apuntaba a lineas donde hoy ya no vive su objeto (`runtime/context.py:16-17` = "implementer" /
"human_owner"). AC2 acreditado.

### (3) AC3 -- PASS. La mutacion se ejerce sobre produccion, y los mensajes coinciden

`powershell_source = POWERSHELL_SCANNER_PATH.read_text(...)` -> el `.ps1` SHIPPED. Los 5 mutantes se
derivan de ese texto (cada uno con `assertNotEqual(powershell_source, mutant_source)`), y el
inventario del mutante se obtiene **EJECUTANDO** el `.ps1` mutado con `-DumpIdentityInventory`
(estado efectivo en runtime), no parseandolo con regex. No se mide contra el runner ni contra
mutantes fabricados por el runner.

    INVENTORY_MUTATION_BALANCE total=5 caught=5 escaped=0 axes=coordinate,order,format

Mismo mensaje en los dos gemelos: acreditado por comportamiento en la Celda A de arriba -- las tres
lineas de hallazgo son identicas entre `.py` y `.ps1`.

*Observacion de baja severidad (no bloquea):* con inventario por volcado en runtime, los 5 mutantes
de forma/orden/coordenada estan cazados **por construccion** (PowerShell ejecuta cualquier forma
declarativa antes del volcado). El negativo por tanto no discrimina formas: discrimina una
REGRESION a parseo por texto. Es correcto como guardia de diseno; no lo es como medida de
sensibilidad del inventario.

### (4) AC4 -- PASS por comportamiento, con un residual que hay que nombrar

El control de CLASE existe y dispara. Inyecte una CUARTA coordenada muerta -- declarada en LOS DOS
gemelos, apuntando a una linea que no contiene su objeto:

    python -m unittest ...test_identity_exemption_inventories_are_one_to_one_and_in_parity
    P3_AC4_dead_coordinate_both_twins EXIT=1
      File ".../test_scan_domain_neutrality.py", line 611, in ...
        self.assertGreaterEqual(
      AssertionError: 0 not greater than or equal to 1 : runtime/context.py:2:Codex

Marca la exencion por ruta:linea:termino. Es un control de clase, no una reparacion de tres casos.
Respondo la pregunta del encargo: **no es "solo se repararon estas tres"**.

**Residual declarado (RES-A):** ese control es PRE-EXISTENTE (el diff de `96af63c6` no toca las
lineas 605-613) y esta **rio abajo** de `assertEqual(python_inventory, powershell_inventory)`
(linea 536) dentro del MISMO metodo. Por fail-fast, **cualquier divergencia de paridad enmascara
TODAS las coordenadas muertas**: es exactamente por eso que las tres de `runtime/context.py`
sobrevivieron mientras "el control seguia declarandose sano" -- en la corrida vieja el detector
NUNCA se alcanzo (la traza cae en la linea 536, no en la 611). El maker no entrego control nuevo
para AC4 y no declaro esta dependencia de orden en su memoria. Cumple la letra del AC; deja viva la
condicion que la tarea describe.

### (5) El corte que mas preocupaba -- el cardinal derivado NO es vacuo

La sospecha era "dos fuentes que degradan al MISMO default". **No ocurre.** Medido con perturbacion
de UNA sola fuente (una entrada extra en el `.ps1` y solo en el `.ps1`):

    P1  perturbar SOLO el .ps1                          -> EXIT 1
        traza: line 536  self.assertEqual(python_inventory, powershell_inventory)
    P2  igual, con la asercion de paridad NEUTRALIZADA  -> EXIT 1
        traza: line 618  self.assertEqual(declared_exemption_count, expected_exemption_count)
        AssertionError: 88 != 89
    P2b asercion de paridad neutralizada, SIN perturbar -> EXIT 0     (control NULO)

P2b descarta que el rojo de P2 venga de neutralizar la paridad. Las dos fuentes son independientes
de verdad: `python_inventory` sale del dict del modulo `.py`; `powershell_inventory` sale de
EJECUTAR el `.ps1`. El cardinal derivado discrimina.

**Residual declarado (RES-B), honesto:** el cardinal esta **SUBSUMIDO**, no vacuo. Con la paridad
viva 82 lineas antes en el mismo metodo, ambas sumas se calculan sobre diccionarios ya afirmados
IGUALES: la linea 618 no puede ser jamas la asercion que falla. Es una frontera declarada en
`FALSIFICATION_CONTRACTS` que es infalsificable *in situ*. No es el defecto que se temia y no
bloquea; es deuda de contrato, y `--inventory` no la ve porque verifica DECLARACION.

### (6) E6 -- PASS en mecanismo; el cardinal 198 NO se re-deriva

Mecanismo correcto: una linea en CADA gemelo (`REQUIRED_SCAN_GLOBS` y `$RequiredScanGlobs`),
`protocol.config.json` intacto (verificado arriba). No quedo a medias en un solo gemelo.

**Censo re-derivado. Unidad: ficheros admitidos por la etapa de seleccion del escaner, clon limpio
en 96af63c6.**

    total admitidos            144  ->  152     (+8, -0)
    .md bajo scripts/          0/8  ->  8/8
    poblacion "bajo claude-skills":
      scripts/instance_assets/claude-skills/**   N=5   antes 0/5   ahora 5/5     CERRADO
      .claude/skills/**                          N=10  antes 0/10  ahora 0/10    sigue en 0

**El cardinal "0 de 198" del GO no re-deriva.** En el arbol de entrega la poblacion de ficheros bajo
cualquier directorio `claude-skills` es **5**, y bajo `.claude/skills/` es **10** (15 en total).
Ninguna unidad que pueda nombrar da 198. Poblaciones vecinas medidas, por si el 198 venia de otra:
`.md` totales 4984; `.md` no exentos 203 (de los cuales admitidos 31 -> 39, hueco 164, incluidos
`AGENTS.md`, `Area_comun/README.md`, `Area_comun/specs/*.md`). Si "los masters" eran
`scripts/instance_assets/claude-skills/`, E6 esta CERRADO 5/5 y el 198 es un cardinal publicado sin
re-derivacion. Si eran otra poblacion, E6 no esta cerrado -- y eso lo decide quien publico el 198,
no yo.

**Residual declarado (RES-C):** `.claude/skills/**` (10 ficheros, las skills VIVAS) sigue sin
escanearse: `.claude/` no casa con ningun glob de scan. No lo llamo incumplimiento porque el GO
apunta a los masters, pero es la mitad del mismo riesgo.

### (7) RES-3 -- SLIPS. BLOQUEANTE. La clase sigue viva y los gemelos siguen dando veredictos OPUESTOS

El GO nombra la clase por su OPERADOR: *"`ContainsKey` de una hashtable de PowerShell es insensible
a mayusculas; la pertenencia a un `set` de Python no lo es"*. El maker reparo **el ejemplo dado**
(`Test-AnyGlob`: `-match` -> `-cmatch`, que resuelve `scripts/Secrets/leak.py`) y dejo **la clase**.

**Censo completo de operadores insensibles a caja que quedan en el gemelo PowerShell:**

| linea | operador | objeto | gemelo Python | veredictos opuestos? |
|---|---|---|---|---|
| 254 | `$IdentityLiteralExemptions.ContainsKey($RelativePath)` | clave de RUTA | `.get(relative_path)` sensible | **SI -- SIN GUARDIA** |
| 258 | `$declaration.Lines.ContainsKey($LineNumber)` | clave int | `.get(line_number)` | no (enteros) |
| 269 | `$declaration.Lines[$LineNumber] -contains $digest` | digest hex | `digest in allowed_terms` sensible | si, pero GUARDADO |
| 217/225/230 | `$GenericIdentityTokens -contains $x.ToLowerInvariant()` | token generico | `casefold() in {...}` | ambos lados normalizados; residual `ToLowerInvariant` vs `casefold` |
| 280/306/322 | `-eq` sobre literales de control | flags/kind | n/a | no |
| 179/199/335 | `-match` / `-replace` | patron con `(?i)` explicito o separador | idem en Python | no |

**Escape 1 -- linea 254, REPRODUCIDO, sin guardia.** Sonda: fichero real cuya ruta relativa difiere
en caja de la clave declarada. Los dos gemelos lo ESCANEAN (el glob `scripts/**/*.ps1` casa en los
dos, ya sensible a caja tras el fix); divergen en la BUSQUEDA de la exencion.

    probe_res3/scripts/Harness/peer_mailbox_cron.ps1   (linea 555: $owner = "Codex")

    python cc/scripts/scan_domain_neutrality.py --root probe_res3
      scripts/Harness/peer_mailbox_cron.ps1:555: Codex
      PY_EXIT=1
    powershell -NoProfile -File cc/scripts/scan_domain_neutrality.ps1 -Root probe_res3
      PS_EXIT=0        <-- silencio

**Mismo fichero, misma linea, misma identidad configurada: Python 1, PowerShell 0.** Es literalmente
la frase del GO -- "los dos gemelos dan veredictos OPUESTOS sobre la misma entrada" -- todavia viva
en `scan_domain_neutrality.ps1` despues del fix, y ademas en la direccion PELIGROSA: **PowerShell es
el permisivo**, exime en silencio una fuga de identidad real.

**Es alcanzable en la plataforma que gatea, y precisamente en el job que existe para esto.** El paso
que ejecuta `./scripts/scan_domain_neutrality.ps1` es `.github/workflows/validate.yml:61`, dentro
del job **`powershell-linux-parity`** (`.yml:12`), `runs-on: [self-hosted, protocol-linux]`: sistema
de ficheros SENSIBLE a mayusculas, donde `scripts/harness/` y `scripts/Harness/` coexisten sin
conflicto. El job cuyo nombre es "paridad" es justo donde la paridad se rompe. No es una
construccion de laboratorio de Windows.

**Ningun test lo cubre.** La asercion de paridad compara DECLARACIONES (los dos inventarios), nunca
el COMPORTAMIENTO de la busqueda con una ruta de caja distinta;
`test_exempt_glob_matching_is_case_sensitive_in_both_gates` cubre exactamente el ejemplo del GO y
nada mas; `test_moved_exempt_identity_fails_both_gates_with_same_finding` mueve la LINEA, no la caja
de la RUTA. Verificado: la suite entera da EXIT 0 en el commit con este escape vivo.

**Escape 2 -- linea 269, divergencia real pero YA GUARDADA (residual, no bloqueante).** Con el mismo
digest declarado en hex MAYUSCULA en LOS DOS gemelos (inventarios identicos -> paridad verde):

    python res3b/scan_domain_neutrality.py --root probe_case
      scripts/harness/peer_mailbox_cron.ps1:555: Codex     PY_EXIT=1
    powershell -File res3b/scan_domain_neutrality.ps1 -Root probe_case
      PS_EXIT=0

Divergencia confirmada, pero la suite la caza rio abajo:

    P4_UPPERCASE_EXIT=1
      line 608  self.assertIn(digest, terms_by_digest, digest)
      AssertionError: '57DE4CF4...' not found in {...'57de4cf4...': 'Codex'...}

Lo declaro como residual del mismo patron: el guardia es incidental (nace de comparar contra
`hexdigest()` en minusculas), no un control de caja deliberado.

## 5. Residuales declarados

- **RES-A** -- el detector de coordenadas muertas (AC4) esta rio abajo de la asercion de paridad en
  el mismo metodo: cualquier divergencia de inventario lo enmascara por completo.
- **RES-B** -- `assertEqual(declared_exemption_count, expected_exemption_count)` es infalsificable
  *in situ* (subsumida por la paridad afirmada 82 lineas antes); frontera declarada en
  `FALSIFICATION_CONTRACTS` que no puede fallar.
- **RES-C** -- `.claude/skills/**` (10 ficheros vivos) sigue con 0 cobertura de escaneo.
- **RES-D** -- el cardinal "0 de 198" del GO no re-deriva contra el arbol de entrega (poblacion real
  medida: 5 bajo `claude-skills`, 15 contando `.claude/skills/`).
- **RES-E** -- `ToLowerInvariant()` (PowerShell) vs `casefold()` (Python) sobre tokens genericos: no
  son la misma normalizacion; sin explotacion medida hoy.
- **RES-F** -- el negativo por mutacion de inventario (5/5) esta cazado por construccion bajo volcado
  en runtime; guarda una regresion de diseno, no mide sensibilidad.
- **CI** -- no lo uso como evidencia, y coincido con el maker: el paso que ejecuta este gate esta
  SKIPPED detras de un job rojo previo. Todas mis puertas son ejecucion directa en clon limpio.

## 6. Recomendacion

**CHANGE-REQUIRED.** Cuatro AC acreditados por comportamiento (AC1, AC2, AC3, AC4) y E6 entregado en
mecanismo; **la ampliacion RES-3 esta a medias**: se reparo el ejemplo (`-cmatch` en los globs) y no
la clase (`ContainsKey` en la busqueda de exenciones), y el escape resultante esta REPRODUCIDO,
sin guardia, y es alcanzable en el runner Linux que ejecuta el gate. El propio encargo fija el
criterio: *"Si cualquiera de las dos queda a medias, no hay cierre."*

**Lazo de arreglo esperado (r1), maximo 2 iteraciones antes de escalar al operador humano:**

1. Remediacion en `scripts/scan_domain_neutrality.ps1`: sustituir la pertenencia insensible a caja
   de `Test-IdentityLiteralExempt` por comparacion ORDINAL sensible a mayusculas para la clave de
   RUTA (linea 254) y para el digest (linea 269) -- p.ej. diccionario ordinal
   (`[System.Collections.Generic.Dictionary[string,object]]::new([StringComparer]::Ordinal)`) o
   comparacion explicita `-ceq`. La forma la elige el maker, no yo.
2. Negativo NUEVO que ate la clase por COMPORTAMIENTO, no por ejemplo: una ruta cuya caja difiere de
   la clave de exencion debe producir el **mismo** veredicto en los dos gemelos. Debe MORIR contra
   el codigo de `96af63c6` (control historico) y sobrevivir contra el remediado.
3. Gates afectados a re-correr: `test_scan_domain_neutrality` (2 corridas),
   `check_falsification_contracts --inventory`, `scan_domain_neutrality` (los DOS gemelos),
   `scan_encoding`, `validate_collaboration_state`. `protocol.config.json` sigue prohibido.
4. Re-juicio del checker ANTES del commit de cierre.

Sugerido, no bloqueante: cerrar RES-A moviendo el detector de coordenadas muertas fuera de la
sombra de la asercion de paridad (metodo propio, o `subTest`), para que una divergencia de
inventario deje de enmascarar la clase entera.

-- Analista, 2026-08-18 18:14 local (UTC+2)
