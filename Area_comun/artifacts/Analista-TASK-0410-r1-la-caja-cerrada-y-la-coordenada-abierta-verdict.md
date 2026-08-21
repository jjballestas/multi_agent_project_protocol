# ANALISTA -- veredicto TASK-0410 r1 (vehiculo TASK-0422)

- Reviewer: Analista (checker independiente; no implemento, no cierro, no ratifico)
- Fecha: 2026-08-22 01:40 local (UTC+2) / 2026-08-21T23:40Z
- Encargo: `Area_comun/mailbox/open/MSG-20260821-Arquitecto-to-Analista-REVIEW-TASK-0410-r1-reemision.md`
- Vehiculo: TASK-0422 (`scope_routes: Area_comun/artifacts/`)
- Recomendacion de cierre: **CHANGE-REQUIRED**

## 0. Respuesta directa a la pregunta del encargo

**Si** a la mitad que se pregunta explicitamente y **no** al conjunto:

1. La pertenencia ORDINAL **cierra los DOS escapes de CAJA que motivaron el CHANGE-REQUIRED**
   (clave de RUTA, linea 254; digest, linea 269). Reproducido con control historico: donde el
   codigo de control da veredictos OPUESTOS, el remediado da el MISMO veredicto y el MISMO mensaje.
2. **El censo CUADRA: 88 == 88**, re-derivado por mi, de forma independiente, de LOS DOS gemelos
   (9 ficheros, 80 pares ruta:linea, 88 ternas ruta:linea:digest).
3. **La divergencia de paridad del inventario de identidad NO queda cerrada.** El inventario esta
   declarado por la terna (ruta, LINEA, digest) y los dos gemelos **siguen sin coincidir en que es
   "la linea N"**: un solo caracter invisible en un fichero exento produce veredictos OPUESTOS
   (Python exit 1, PowerShell exit 0). Cinco separadores reproducen el escape. Ningun test lo cubre.
   La suite entera sale verde con el escape VIVO.

Corridas por puerta: declaradas una por una en la seccion 2. Ninguna puerta cuyo resultado gatea el
juicio se apoya en una sola corrida.

## 1. Ancla canonica

| Cosa | Valor |
|---|---|
| Commit bajo review | `b7bb0be117889c1721d6c4fd72f76b429ca27fd0` (Codex, 2026-08-18 21:15 +0200) |
| Control historico | `b7bb0be1^` = `e94b312f` |
| HEAD del protocolo al emitir | `ecc9ab13` (== `origin/main`; no toca los escaneres) |
| Clon limpio (ancla) | `D:/Aegis_Scratch/protocol/r0410r1/cc` (`git clone -s -n` + `checkout b7bb0be1`) |
| Clon limpio (control) | `D:/Aegis_Scratch/protocol/r0410r1/old` (`checkout b7bb0be1^`) |
| Ficheros tocados por r1 | 2 (`scan_domain_neutrality.ps1` +19/-5, `test_scan_domain_neutrality.py` +14) |

**El control historico es legitimo:** entre `96af63c6` (el commit del CHANGE-REQUIRED) y `b7bb0be1^`
el unico cambio bajo `scripts/`, `.github/` y `protocol.config.json` es
`check_falsification_contracts.py` (+6 lineas). Los DOS escaneres son identicos entre ambos, luego
`b7bb0be1^` mide exactamente el comportamiento que el CHANGE-REQUIRED rechazo.

**Fondo intocable -- verificado, NO se toco:**

    sha256(protocol.config.json)[:8] en b7bb0be1 = 2E35F26E    (esperado 2E35F26E)   OK
    git diff --stat b7bb0be1^ b7bb0be1 -- protocol.config.json  ->  0 lineas          OK

## 2. Reproduccion -- puertas por EXIT CODE, en clon limpio

| Puerta | Corridas | Exit | Nota |
|---|---|---|---|
| `python -m unittest scripts.test_scan_domain_neutrality` (ancla) | 2 | 0 / 0 | 10 tests; 537.5 s y 423.6 s |
| `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory` | 1 | 0 | los 4 contratos NEG-NEUTRALITY-* DECLARED |
| `python scripts/scan_encoding.py --root .` | 1 | 0 | |
| `python scripts/scan_domain_neutrality.py --root .` | 1 | 0 | 0 hallazgos |
| `pwsh -File scripts/scan_domain_neutrality.ps1 -Root .` | 1 | 0 | 0 hallazgos |
| `python scripts/validate_collaboration_state.py --root .` | 1 (clon) + 1 (arbol) | 0 / 0 | `OK: collaboration state is valid.` |

Balances que imprime la suite en las dos corridas, identicos:

    INVENTORY_MUTATION_BALANCE total=5 caught=5 escaped=0 axes=coordinate,order,format
    TERM_MUTATION_BALANCE expected=623 current=623 mutant=534 losses=89

**Puerta EXCLUIDA por no reproducible: ninguna.** Las dos corridas de la suite coinciden en exit
code, en numero de tests y en los dos balances. El CI no lo uso como evidencia y no afirmo nada
sobre su estado de hoy: no abri ninguna corrida. Todo lo que cito es ejecucion directa en clon
limpio.

## 3. El censo, re-derivado por mi -- no lo tomo del test

**Unidad: ternas (ruta, linea, digest) del inventario de exenciones de identidad literal.**
Las dos fuentes se obtienen por caminos distintos: el gemelo Python por importacion del modulo, el
gemelo PowerShell por EJECUCION con `-DumpIdentityInventory` (estado efectivo en runtime).

    gemelo Python       9 ficheros | 80 pares (ruta,linea) | 88 ternas
    gemelo PowerShell   9 ficheros | 80 pares (ruta,linea) | 88 ternas      -> 88 == 88

Pares por fichero, identicos en los dos: `runtime/apply.py` 1, `runtime/budget.py` 2,
`runtime/eventlog.py` 3, `runtime/ledger_ops.py` 1, `runtime/metrics.py` 1, `runtime/router.py` 2,
`scripts/harness/peer_mailbox_cron.ps1` 9, `scripts/memory/test_memory_db.py` 56,
`scripts/prune_state.py` 5. **El censo cuadra.**

## 4. Tabla vector por vector

| # | Vector | Veredicto |
|---|---|---|
| V1 | Escape 1 -- caja de la clave de RUTA (linea 254) | **PASS -- cerrado, discriminante** |
| V2 | Escape 2 -- caja del DIGEST (linea 269) | **PASS en efecto / SLIP en guardia** |
| V3 | El negativo nuevo muere contra el control historico | **PASS (con reserva)** |
| V4 | La CLASE de pertenencia insensible a caja, no el ejemplo | **SLIPS (linea 211, no bloqueante)** |
| V5 | Censo 88 == 88 re-derivado de los dos gemelos | **PASS** |
| V6 | Paridad del inventario por su COORDENADA (la linea) | **SLIPS -- BLOQUEANTE** |
| V7 | `StartsWith`/`EndsWith` sensibles a cultura (.NET) vs ordinal (Python) | **PASS -- divergente pero INALCANZABLE** |
| V8 | `ToLowerInvariant()` vs `casefold()` sobre tokens genericos | **PASS -- sin explotacion (RES-E)** |

---

### V1 -- PASS. El escape que motivo el rechazo esta cerrado, y el control lo discrimina

Sonda `probe/`: el MISMO fichero declarado en dos cajas, `scripts/Harness/peer_mailbox_cron.ps1`
(no exento) y `scripts/harness/peer_mailbox_cron.ps1` (exento en la linea 555), con
`$owner = "Codex"` en la linea 555 de ambos.

    (ancla b7bb0be1)
    python  cc/scripts/scan_domain_neutrality.py  --root probe
      scripts/Harness/peer_mailbox_cron.ps1:555: Codex        PY_EXIT=1
    pwsh -File cc/scripts/scan_domain_neutrality.ps1 -Root probe
      scripts/Harness/peer_mailbox_cron.ps1:555: Codex        PS_EXIT=1

    (control b7bb0be1^)
    python  old/scripts/scan_domain_neutrality.py  --root probe
      scripts/Harness/peer_mailbox_cron.ps1:555: Codex        PY_EXIT=1
    pwsh -File old/scripts/scan_domain_neutrality.ps1 -Root probe
                                                              PS_EXIT=0   <-- silencio

Mismo mensaje, mismo exit, y el ruido correcto: los dos gemelos EXIMEN la variante en minusculas.
El verde no lo produce el codigo viejo.

### V2 -- PASS en efecto, SLIP en guardia. El arreglo funciona y NINGUN test lo ata

Aislado en `probe2/` (solo la ruta en minusculas, para que el unico eje sea el digest). Linea base:
los dos gemelos exentos, exit 0 / exit 0. Con el digest declarado en hex MAYUSCULA **en los DOS
gemelos** (inventarios identicos, luego la asercion de paridad sigue verde):

    (ancla)    python  res3b_cc/scan_domain_neutrality.py  --root probe2
                 scripts/harness/peer_mailbox_cron.ps1:555: Codex      PY_EXIT=1
               pwsh -File res3b_cc/scan_domain_neutrality.ps1 -Root probe2
                 scripts/harness/peer_mailbox_cron.ps1:555: Codex      PS_EXIT=1
    (control)  python  res3b_old/scan_domain_neutrality.py --root probe2    PY_EXIT=1
               pwsh -File res3b_old/scan_domain_neutrality.ps1 -Root probe2 PS_EXIT=0

El efecto esta acreditado. **Pero el arreglo no tiene guardia.** Mutante `mut269`: el clon del ancla
con **una sola** edicion -- revertir la comparacion ordinal del digest a `-contains`, dejando el
arreglo de la ruta (254) intacto:

    python -m unittest scripts.test_scan_domain_neutrality   ->  Ran 10 tests ... OK
                                                                 SUITE_MUT269_EXIT=0

La suite entera sobrevive al borrado del arreglo. Es deuda de negativo, no defecto de hoy: cualquier
refactor puede reintroducir la insensibilidad del digest sin que nada enrojezca.

### V3 -- PASS con reserva. El negativo nuevo SI muere contra el control

2x2 de la posicion. Mutante `mut/`: el fichero de test del ancla **verbatim** + el
`scan_domain_neutrality.ps1` del control (verificado por md5: `mut` test == `cc` test, `mut` ps1 ==
`old` ps1).

    python -m unittest ...test_identity_exemption_path_matching_is_case_sensitive_in_both_gates
      FAILED (failures=1)     NEWTEST_ON_OLDPS1_EXIT=1
      test_scan_domain_neutrality.py:662  self.assertIn(expected, powershell_result.stdout)
      AssertionError: 'scripts/Harness/peer_mailbox_cron.ps1:555: Codex' not found in '...'

Muere por la razon correcta. **Reserva, de baja severidad:** la mitad
`assertEqual(powershell_result.returncode, 1)` **no discrimina** -- el gemelo viejo tambien sale 1,
por hallazgos ajenos a la sonda. Toda la potencia del vector la lleva el `assertIn`.

### V4 -- SLIPS. Se arreglaron las lineas enumeradas; la clase sigue viva una funcion mas arriba

El maker fue mas alla de las dos lineas que yo nombre: tambien paso a `Ordinal` la pertenencia de
`$RequiredScanGlobs`/`$RequiredExemptGlobs` (lineas 292 y 299). Se le reconoce. Pero el censo
completo de pertenencias del gemelo PowerShell deja **una** sin tocar, y es la que construye el
universo de terminos:

    scripts/scan_domain_neutrality.ps1:211
      $terms = New-Object System.Collections.Generic.HashSet[string] ([System.StringComparer]::OrdinalIgnoreCase)
    scripts/scan_domain_neutrality.py:230
      terms: set[str] = set()                      # sensible a caja

Sonda `probeC1/`: config con `agent_registry.agents = [Codex]` y `agent_roles = {implementer: codex}`.

    python  cc/scripts/scan_domain_neutrality.py  --root probeC1
      scripts/probe.py:1: Codex
      scripts/probe.py:1: codex                    PY_EXIT=1   (2 hallazgos)
    pwsh -File cc/scripts/scan_domain_neutrality.ps1 -Root probeC1
      scripts/probe.py:1: Codex                    PS_EXIT=1   (1 hallazgo)

**Causa medida, no inferida.** Copia del `.ps1` del ancla con **una sola** edicion -- el comparador
de la linea 211 a `Ordinal`:

    pwsh -File slip2/scan_domain_neutrality.ps1 -Root probeC1
      scripts/probe.py:1: Codex
      scripts/probe.py:1: codex                    PS_EXIT=1   (2 hallazgos, == Python)

Es exactamente la clase del CHANGE-REQUIRED ("pertenencia insensible a caja en PowerShell frente a
pertenencia sensible en Python"), en el mismo fichero, 45 lineas por encima de la funcion reparada.
**No la declaro bloqueante** porque no invierte el veredicto: los exit codes coinciden (los dos 1) y
la exencion no se ve afectada -- el digest se calcula sobre el termino ya normalizado, luego las
variantes de caja comparten digest. Lo que rompe es la **paridad del MENSAJE**, que es lo que exige
el AC3 y lo que compara el contrato `NEG-NEUTRALITY-IDENTITY-EXEMPTION-PARITY`. Hoy no es
explotable en ESTA instancia (su config no tiene identidades que difieran solo en caja); si lo es en
cualquier instancia adoptante, que es a quien se le envia el escaner.

### V6 -- SLIPS. BLOQUEANTE. Los dos gemelos no coinciden en QUE es la linea N

El inventario se declara por la terna (ruta, LINEA, digest). V1 y V2 arreglaron la ruta y el digest.
La **coordenada** sigue divergiendo, y esta vez si invierte el veredicto.

    scan_domain_neutrality.py:267    for line_number, line in enumerate(text.splitlines(), start=1)
    scan_domain_neutrality.ps1:329   $lines = @(Get-Content -Path $file.Path -Encoding UTF8)

`str.splitlines()` de Python parte tambien en U+000B, U+000C, U+001C..U+001E, U+0085, U+2028 y
U+2029. `Get-Content` no. Un solo caracter de esos, insertado antes de una linea exenta, desplaza la
numeracion de un gemelo y no la del otro. El mecanismo no depende de la plataforma; lo medi en
Windows.

Sonda `probeLF/`: `scripts/harness/peer_mailbox_cron.ps1` (fichero REAL del inventario, exento en la
linea 555) con **un** U+000C insertado antes de `$owner = "Codex"`.

    numeracion medida:   PY splitlines -> 556        PS Get-Content -> 555

    (ancla b7bb0be1)
    python  cc/scripts/scan_domain_neutrality.py  --root probeLF
      scripts/harness/peer_mailbox_cron.ps1:556: Codex        PY_EXIT=1
    pwsh -File cc/scripts/scan_domain_neutrality.ps1 -Root probeLF
                                                              PS_EXIT=0   <-- silencio

**Misma entrada, veredictos OPUESTOS, y PowerShell es el PERMISIVO** -- exime en silencio una fuga
de identidad real, que es la direccion peligrosa y la frase literal del GO que abrio la ampliacion.

Familia acotada por medicion (todas contra el ancla, misma sonda, un separador cada vez):

| separador | Python | PowerShell | diverge |
|---|---|---|---|
| U+000B VT | exit 1 | exit 0 | SI |
| U+000C FF | exit 1 | exit 0 | SI |
| U+001C FS | exit 1 | exit 0 | SI |
| U+0085 NEL | exit 1 | exit 0 | SI |
| U+2028 LS | exit 1 | exit 0 | SI |

**Ningun test lo cubre**: en `test_scan_domain_neutrality.py` no hay una sola sonda con esos
caracteres (las 11 apariciones de `splitlines` son troceo de STDOUT o del fuente, no sondas de
entrada). Y la suite completa sale **exit 0** en el ancla con el escape VIVO -- verde no
discriminante para este eje.

**Atribucion honesta: es HEREDADO, no lo introdujo la r1.** El mismo control historico lo reproduce
igual (`old`: PY exit 1 / PS exit 0). Lo declaro bloqueante no por atribucion sino por el criterio
que la propia tarea fija en su AC3: *"mover el objeto vigilado debe hacer FALLAR a los DOS gemelos
con el mismo mensaje. Si solo falla uno, la paridad no esta acreditada."* Aqui el objeto vigilado se
mueve -- una linea, con un byte invisible -- y **solo falla uno**. Cerrar TASK-0410 hoy inscribiria
en el ledger que la paridad del inventario de identidad esta acreditada cuando un caracter la
derriba, con el gemelo que gatea quedandose callado.

### V7 -- PASS. Divergencia real, pero INALCANZABLE: la mido y la declaro

`Test-IdentityScanPath` usa `.StartsWith("runtime/")` / `.EndsWith(".py")`, que en .NET son
**sensibles a cultura** por defecto; el gemelo Python usa `startswith`/`endswith`, ordinales.
Medido:

    pwsh : ("run" + [char]0x00AD + "time/x.py").StartsWith("runtime/")            -> True
           ("run" + [char]0x00AD + "time/x.py").StartsWith("runtime/", Ordinal)   -> False
    py   : "run\u00ADtime/x.py".startswith("runtime/")                            -> False

La divergencia existe, pero **no es alcanzable**: la seleccion de ficheros corre ANTES y usa globs
ordinales en los dos gemelos (`-cmatch` en PowerShell, `re.compile` sin `IGNORECASE` en Python).
Para llegar a `Test-IdentityScanPath` la ruta ya tiene que casar `^scripts/...\.py$` o
`^runtime/...` literalmente, y entonces los dos `startswith` coinciden. Lo dejo declarado como
residual latente: si alguien relaja los globs, se vuelve explotable sin tocar esta funcion.

### V8 -- PASS. `ToLowerInvariant()` vs `casefold()`: sin explotacion sobre la lista real

Los cuatro tokens genericos son `agent`, `human`, `humano`, `owner`: ASCII puros, sin ninguna
diferencia entre las dos normalizaciones. Ademas el `-contains` de esa comparacion recibe el valor
ya normalizado, luego su insensibilidad no anade nada. Se mantiene como residual (RES-E), sin
explotacion medida, igual que en el veredicto anterior.

## 5. Residuales declarados

- **RES-1 (nuevo, BLOQUEANTE)** -- V6: la coordenada del inventario diverge entre gemelos por el
  troceo de lineas; cinco separadores producen veredictos opuestos con PowerShell permisivo;
  heredado, sin cobertura de test.
- **RES-2 (nuevo)** -- V4: `HashSet[string]` con `StringComparer::OrdinalIgnoreCase` en
  `scan_domain_neutrality.ps1:211` frente a `set()` en el gemelo Python; rompe paridad de MENSAJE,
  no de exit code; causa probada por edicion unica.
- **RES-3 (nuevo)** -- V2: el arreglo ordinal del digest (linea 269) no tiene negativo; `mut269`
  demuestra que la suite completa sale verde sin el.
- **RES-4 (nuevo)** -- V7: `StartsWith`/`EndsWith` sensibles a cultura, divergentes pero
  inalcanzables tras la seleccion por globs ordinales.
- **RES-A (vigente)** -- el detector de coordenadas muertas (AC4) sigue rio abajo de
  `assertEqual(python_inventory, powershell_inventory)` en el mismo metodo: cualquier divergencia de
  paridad lo enmascara entero. La r1 no lo toco.
- **RES-B (vigente)** -- `assertEqual(declared_exemption_count, expected_exemption_count)` sigue
  subsumida por la paridad afirmada 82 lineas antes: frontera declarada que no puede fallar in situ.
- **RES-C (vigente)** -- `.claude/skills/**` sigue con 0 cobertura de escaneo.
- **RES-E (vigente)** -- `ToLowerInvariant()` vs `casefold()`, sin explotacion medida.
- **CI** -- no lo uso como evidencia. Todas mis puertas son ejecucion directa en clon limpio.

## 6. Recomendacion

**CHANGE-REQUIRED.** La r1 **cumplio su mandato**: los dos escapes de caja que motivaron el rechazo
estan cerrados y acreditados con control historico, el negativo pedido existe y muere contra el
codigo viejo, el censo cuadra 88 == 88 y las seis puertas salen verdes -- la suite en dos corridas
coincidentes. No bloqueo por nada de eso.

Bloqueo por **RES-1**: al ejercer la familia entera en vez del ejemplo, la garantia que la tarea
gobierna sigue rota por otro eje de la MISMA terna, con veredictos opuestos reproducidos sobre el
fichero real del inventario y el gemelo que gatea quedandose callado.

**Lazo de arreglo esperado (r2). Es la SEGUNDA de las dos iteraciones que declare: si la r2 no lo
cierra, escala al operador humano.**

1. Igualar el troceo de lineas entre gemelos. La forma la elige el maker; la mas barata es que el
   gemelo Python deje de usar `str.splitlines()` y parta solo por `\r\n|\n`, que es lo que hace
   `Get-Content`. `protocol.config.json` sigue prohibido.
2. Negativo NUEVO por COMPORTAMIENTO que ate el eje, no un separador: para **cada** separador de la
   tabla de V6, un fichero exento con ese caracter insertado antes de la linea exenta debe producir
   el **mismo** veredicto y el **mismo** mensaje en los dos gemelos. Debe MORIR contra `b7bb0be1`
   (control historico) y sobrevivir contra el remediado. Un test que solo pruebe U+000C repite el
   patron que trajo esta r1.
3. Cerrar RES-2 en el mismo paso -- es una linea (`StringComparer::Ordinal` en la 211) y su
   negativo: una config con identidades que difieren solo en caja debe dar el MISMO conjunto de
   hallazgos en los dos gemelos.
4. Cerrar RES-3 -- negativo para el digest ordinal; hoy `mut269` sale verde sin el arreglo.
5. Puertas a re-correr: `test_scan_domain_neutrality` (2 corridas),
   `check_falsification_contracts --inventory`, `scan_domain_neutrality` (los DOS gemelos),
   `scan_encoding`, `validate_collaboration_state`.
6. Re-juicio del checker ANTES del commit de cierre.

**Alternativa de gobierno, si el Arquitecto prefiere no ampliar mas TASK-0410:** RES-1 es HEREDADO y
no atribuible a la r1 -- exactamente el caso por el que TASK-0410 salio de TASK-0337. Es legitimo
enrutarlo como tarea propia y cerrar TASK-0410 con RES-1 **nombrado en el cierre**. Lo que no es
legitimo es cerrarla en silencio: el titulo de la tarea afirma que la paridad del inventario
diverge, y con RES-1 vivo sigue divergiendo. Esa decision es del Arquitecto o del operador, no mia;
mi veredicto tecnico es el de arriba.

Sugerido, no bloqueante: RES-A sigue en pie y sigue siendo barato (sacar el detector de coordenadas
muertas de la sombra de la asercion de paridad, con `subTest` o metodo propio).

-- Analista, 2026-08-22 01:40 local (UTC+2)
