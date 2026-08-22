# ANALISTA -- veredicto TASK-0410 r2 (vehiculo TASK-0422)

- Reviewer: Analista (checker independiente; no implemento, no cierro, no ratifico)
- Fecha: 2026-08-22 07:39 local (UTC+2) / 2026-08-22T05:39Z
- Encargo: `Area_comun/mailbox/open/MSG-20260822-Arquitecto-to-Analista-REVIEW-TASK-0410-r2.md`
- Alcance recortado por el encargo: **solo RES-2 y RES-3**. RES-1 esta fuera y vive en TASK-0338.
- Recomendacion de cierre: **OK-CLOSABLE**, con un residual NUEVO que el cierre debe nombrar.

## 0. Respuesta directa a la pregunta del encargo

La pregunta era doble. Contesto las dos mitades por separado porque no salen igual.

1. **Si muere `mut269` al revertir el arreglo, mutando produccion y no el runner.** Muere, y por
   partida doble: muere el revert de TEXTO (`mut269`, exit 1) y muere ademas un mutante que deja la
   clausula ordinal **verbatim** en produccion y regresa el comportamiento por otra via
   (`mut269b`, exit 1, y muere en la asercion de COMPORTAMIENTO, no en la de posicion). El
   remediado restaurado sobrevive, dos corridas, exit 0. **RES-3 esta acreditado.**
2. **Si RES-2 usa `StringComparer::Ordinal`.** Lo usa, y el efecto esta acreditado: seis vectores
   de la familia dan paridad IDENTICA en el ancla, y el control historico los rompe en cuatro. Ese
   verde no lo produce el codigo viejo.

**Pero RES-2 llega sin guardia, que es exactamente el defecto que esta misma r2 fue enviada a
arreglar en RES-3.** `mut211` revierte en PRODUCCION la unica linea del arreglo de RES-2 y la suite
entera -- 11 tests, 432.9 s -- sale **exit 0**, mientras la paridad esta medida y rota. No lo
declaro bloqueante (razones en la seccion 6), pero el cierre no puede callarlo.

Corridas por puerta: declaradas una por una en la seccion 2. **Ninguna puerta excluida por no
reproducible.** CI no usado como evidencia: no abri ninguna corrida.

## 1. Ancla canonica

| Cosa | Valor |
|---|---|
| Commit bajo review | `b899167b50f0012bcdf9464723378826d5cc5b98` |
| Control historico | `b899167b^` = `371ee761` |
| HEAD del protocolo al emitir | `7a84eea9` (== `origin/main`; no toca los escaneres) |
| Clon limpio (ancla) | `D:/Aegis_Scratch/protocol/an410r2/cc` (`git clone -s -n` + `checkout b899167b`) |
| Clon limpio (control) | `D:/Aegis_Scratch/protocol/an410r2/old` (`checkout b899167b^`) |
| Ficheros de codigo tocados por la r2 | 2 (`scan_domain_neutrality.ps1` +1/-1, `test_scan_domain_neutrality.py` +39) |
| Tests nuevos en la r2 | **1** (`test_identity_exemption_digest_matching_is_ordinal_in_powershell_gate`) |

**Fondo intocable -- verificado, NO se toco:**

    sha256(protocol.config.json)[:8] en b899167b = 2E35F26E   (esperado 2E35F26E)   OK
    git diff --stat b899167b^ b899167b -- protocol.config.json  ->  0 lineas         OK

## 2. Reproduccion -- puertas por EXIT CODE, en clon limpio

| Puerta | Corridas | Exit | Nota |
|---|---|---|---|
| `python -m unittest scripts.test_scan_domain_neutrality` (ancla) | 2 | 0 / 0 | 11 tests; 452.9 s y 435.2 s |
| `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory` | 2 | 0 / 0 | salida byte-identica entre corridas |
| `python scripts/scan_encoding.py --root .` | 1 | 0 | `OK: encoding scan is clean.` |
| `python scripts/scan_domain_neutrality.py --root .` | 1 | 0 | 0 hallazgos |
| `pwsh -NoProfile -File scripts/scan_domain_neutrality.ps1 -Root .` | 1 | 0 | 0 hallazgos |
| `python scripts/validate_collaboration_state.py --root .` | 1 (clon) + 1 (arbol) | 0 / 0 | `OK: collaboration state is valid.` |

Balances impresos por la suite, **identicos en las dos corridas** y identicos a los de la r1:

    INVENTORY_MUTATION_BALANCE total=5 caught=5 escaped=0 axes=coordinate,order,format
    TERM_MUTATION_BALANCE expected=623 current=623 mutant=534 losses=89

Drift: el validador no reporta drift; su unica advertencia es la frontera conocida de verificacion
de autenticacion de eventos (`unverifiable=9442`), presente tambien en el arbol vivo y ajena a esta
entrega.

## 3. Tabla vector por vector

| # | Vector | Veredicto |
|---|---|---|
| W1 | RES-2: la linea 211 usa `StringComparer::Ordinal` en produccion | **PASS** |
| W2 | RES-2 por COMPORTAMIENTO: seis vectores de la familia, paridad en el ancla | **PASS** |
| W3 | RES-2 discriminante: el control historico rompe 4 de los 6 | **PASS** |
| W4 | RES-2 tiene GUARDIA que mate el revert | **SLIPS -- residual nuevo** |
| W5 | RES-3: `mut269` (revert de texto en produccion) muere | **PASS** |
| W6 | RES-3: `mut269b` (clausula verbatim, comportamiento regresado) muere | **PASS** |
| W7 | RES-3: produccion restaurada sobrevive | **PASS (2 corridas)** |
| W8 | RES-3 por FAMILIA: cinco variantes de caja del digest, los dos gemelos | **PASS** |
| W9 | Censo de sensibilidad a caja del gemelo PowerShell: escape NUEVO? | **PASS -- ninguno alcanzable** |
| W10 | Fondo intocable y `protocol.config.json` sin tocar | **PASS** |

---

### W1/W2/W3 -- PASS. RES-2 cierra por efecto y el control lo discrimina

Produccion en el ancla, linea 211:

    $terms = New-Object System.Collections.Generic.HashSet[string] ([System.StringComparer]::Ordinal)

y en el control (`371ee761`), la misma linea con `OrdinalIgnoreCase`. Sonda: raiz con
`protocol.config.json` propio (`scan_globs: ["scripts/*.py"]`, denylist vacia) y un
`scripts/probe.py` con las variantes de caja. Comparo **conjunto de hallazgos ordenado + exit code**
de los dos gemelos, con la salida de PowerShell capturada en BYTES y decodificada UTF-8 explicito
(mi primera pasada la decodifico con la codepage de consola y fabrico dos divergencias FALSAS en
F4/F5; corregido el instrumento, desaparecieron -- lo declaro porque casi lo reporto como hallazgo).

| vector | config | ancla `b899167b` | control `b899167b^` |
|---|---|---|---|
| F1 dos variantes `Codex`/`codex` | agent id + rol | PY 1/n=4, PS 1/n=4 -- **SAME** | PY n=4, PS n=2 -- **DIVERGE** |
| F2 tres variantes `Codex`/`codex`/`CODEX` | 2 ids + rol | PY 1/n=3, PS 1/n=3 -- **SAME** | PY n=3, PS n=1 -- **DIVERGE** |
| F3 variantes de caja en el TROCEO de rol (linea 228) | 2 roles | PY 1/n=2, PS 1/n=2 -- **SAME** | PY n=2, PS n=1 -- **DIVERGE** |
| F4 no-ASCII `Angel`/`angel` (A con tilde) | id + rol | PY 1/n=2, PS 1/n=2 -- **SAME** | PY n=2, PS n=1 -- **DIVERGE** |
| F5 eszett `Strasse`/`STRASSE` | id + rol | PY 1/n=1, PS 1/n=1 -- SAME | SAME -- **no discrimina** |
| F6 I mayuscula con punto (turco) | id + rol | PY 1/n=1, PS 1/n=1 -- SAME | SAME -- **no discrimina** |

F5 y F6 **no discriminan** y lo declaro: sondean la frontera `ToLowerInvariant()` vs `casefold()`
(RES-E) y ahi no hay explotacion, igual que en la r1. La potencia del vector la llevan F1-F4, que
cubren la clase completa que el CHANGE-REQUIRED nombro: ids de agente, valores de rol y tokens del
troceo de rol, en ASCII y fuera de ASCII. El arreglo tambien cierra la **paridad de MENSAJE**, que
era lo que RES-2 rompia: no solo coinciden los exit codes, coinciden los conjuntos de hallazgos.

### W4 -- SLIPS. El arreglo de RES-2 esta presente y NO esta acreditado

Mutante `mut211`: copia del ancla con **una sola** edicion, en PRODUCCION, revirtiendo la linea 211
a `OrdinalIgnoreCase`. El fichero de test queda **verbatim** (md5 identico al del ancla) y ningun
otro fichero difiere.

    python -m unittest scripts.test_scan_domain_neutrality
      Ran 11 tests in 432.858s ... OK              SUITE_MUT211_EXIT=0
      INVENTORY_MUTATION_BALANCE total=5 caught=5 escaped=0
      TERM_MUTATION_BALANCE expected=623 current=623 mutant=534 losses=89

y el mismo `mut211`, sobre la sonda F1, esta **medible y realmente regresado**:

      [cc]      PY exit=1 n=4 | PS exit=1 n=4   SAME
      [mut211]  PY exit=1 n=4 | PS exit=1 n=2   DIVERGE

La suite entera sobrevive al borrado del arreglo. Causa estatica, comprobada: en
`test_scan_domain_neutrality.py` **no hay una sola referencia** a `Get-ConfiguredIdentityTerms`, a
`StringComparer` ni a `OrdinalIgnoreCase`, y la r2 anadio **un** test, que es el del digest. Y no
puede haberla por accidente: la config real de esta instancia declara `Arquitecto`, `Codex`,
`Analista` y roles que no difieren solo en caja, luego sobre el arbol real los dos comparadores
producen el MISMO universo de terminos y ningun test de arbol real puede enrojecer.

Es literalmente la forma del defecto que el encargo describe para RES-3 -- *"presente pero no
acreditado; si alguien lo revertia manana nada enrojecia"* -- reaparecida en el otro residual de la
misma entrega. Lo registro como **RES-2-GUARD**.

### W5/W6/W7 -- PASS. RES-3 acreditado, y por los dos lados del 2x2 de la posicion

El test nuevo lee produccion, re-escribe el digest declarado de `runtime/apply.py:440` en HEX
MAYUSCULA, y deriva dos variantes: una con la clausula ordinal y otra con `-contains`. Exige que la
ordinal REPORTE la fuga y la insensible NO. Sus dos `assertNotEqual` son la guardia de posicion:
afirman que lo que sustituye existe en produccion.

**Hueco alcanzable -- debe MORIR.** `mut269`: una sola edicion en produccion, la clausula ordinal
del digest revertida a `-contains`, runner verbatim (md5 identico).

    python -m unittest ...test_identity_exemption_digest_matching_is_ordinal_in_powershell_gate
      FAILED (failures=1)                          MUT269_FOCUSED_EXIT=1
      test_scan_domain_neutrality.py:690  self.assertNotEqual(uppercase_inventory_source, insensitive_source)

Muere en la guardia de POSICION. Eso solo demuestra que el texto del arreglo tiene que estar. Por
eso hice el segundo, que es el que importa:

**Hueco alcanzable sin tocar el texto -- tambien debe MORIR.** `mut269b`: la clausula ordinal se
deja **byte a byte intacta** (verificado: la cadena de tres lineas sigue presente) y se inyecta
ENCIMA un retorno anticipado insensible a caja, `-contains`. La guardia de texto es ciega a esto.

    FAILED (failures=1)                            MUT269B_FOCUSED_EXIT=1
    test_scan_domain_neutrality.py:700  self.assertIn(expected, ordinal_result.stdout)
    AssertionError: 'runtime/apply.py:440: Codex' not found in '...'

Muere en la asercion de COMPORTAMIENTO. El negativo tiene, pues, las dos dentaduras: mata el borrado
del arreglo y mata la regresion que respeta su letra.

**Codigo verbatim -- debe SOBREVIVIR.** Produccion del ancla sin tocar:

    CC_FOCUSED_RUN1_EXIT=0     Ran 1 test in 1.405s ... OK
    CC_FOCUSED_RUN2_EXIT=0     Ran 1 test in 1.600s ... OK

**Declaro la direccion honestamente:** el test nuevo es una GUARDIA DE REGRESION, no la acreditacion
de un cambio de comportamiento. El arreglo ordinal del digest ya estaba en `b899167b^` (entro en la
r1), luego este test tambien pasa contra el control -- y debe pasar. Lo que la r2 aporta aqui es
exactamente lo que faltaba: que revertirlo enrojezca. Lo aporta.

### W8 -- PASS. La familia del digest, no el ejemplo

El test usa un solo ejemplo (todo MAYUSCULAS). Ejerzo la familia: recaso el digest declarado de
`runtime/apply.py:440` **en los DOS gemelos** a la vez -- inventarios identicos, luego la asercion
de paridad no enmascara nada -- y comparo veredictos.

| variante del digest declarado | ancla: PY / PS | veredicto |
|---|---|---|
| D1 minusculas (linea base) | exit 0 / exit 0, 0 hallazgos | EXENTO en los dos -- **SAME** |
| D2 MAYUSCULAS | exit 1 / exit 1, 1 hallazgo | no exento en los dos -- **SAME** |
| D3 alternado | exit 1 / exit 1 | **SAME** |
| D4 primer caracter ALFABETICO en mayuscula | exit 1 / exit 1 | **SAME** |
| D5 ultimo caracter ALFABETICO en mayuscula | exit 1 / exit 1 | **SAME** |

Los cinco coinciden tambien en el control, como debe ser. (Mi primera version de D4/D5 recasaba el
primer/ultimo caracter del digest sin comprobar que fuera una letra; `5` y `3` no tienen caja, y la
sonda era DEGENERADA -- salia "exento" por no mutar nada. Corregido a posiciones alfabeticas. Lo
declaro porque una sonda vacua que sale verde es indistinguible de una garantia.)

### W9 -- PASS. Busque un escape nuevo en la clase y no lo hay alcanzable

Censo completo de sensibilidad a caja del gemelo PowerShell en el ancla (376 lineas):

- `IgnoreCase` explicito: **una sola aparicion**, linea 197, y es la comparacion de PREFIJO DE RUTA
  bajo la rama de separador de directorio de Windows. Es deliberada y correcta: en Windows el
  sistema de ficheros es insensible; el gemelo Python hace lo propio con `os.path`.
- Lineas 254, 273, 294, 301: las cuatro pertenencias criticas ya son `[string]::Equals(...,
  StringComparison::Ordinal)`.
- Linea 261: `.ContainsKey($LineNumber)` -- claves ENTERAS, la caja no aplica.
- Lineas 217/225/230: `$GenericIdentityTokens -contains $value.ToLowerInvariant()` -- insensible,
  pero sobre valor ya normalizado y contra cuatro tokens ASCII (`agent`, `human`, `humano`,
  `owner`). Es RES-E; medido en F5/F6, sin explotacion.
- Linea 344: `$lines[$lineIndex] -match $pattern` con `$pattern` construido con el prefijo `(?i)`.
  Insensible **a proposito**, y el gemelo Python compila el mismo patron con `re.IGNORECASE`
  (linea 258). Paridad deliberada, no divergencia. Este era mi mejor candidato a escape nuevo y
  **no lo es**.
- Ordenacion: `Sort-Object { $_.ToLowerInvariant() }` frente a `sorted(terms, key=str.casefold)`.
  Con F1-F4 (dos terminos con la MISMA clave de orden) los conjuntos salieron identicos en el ancla,
  luego no hay divergencia de orden observable en la familia medida. Sin `switch`, sin `-like`, sin
  `-cmatch` relajado.

### W10 -- PASS. Fondo intocable

`2E35F26E`, cero lineas de diff en `protocol.config.json`. Verificado en el clon, no en el arbol.

## 4. Lo que este veredicto NO afirma

- **No juzgo el troceo de lineas (RES-1).** El encargo lo excluye y vive en TASK-0338. Sigue vivo:
  no lo he re-medido aqui y no lo doy por cerrado.
- **No afirmo nada sobre el CI.** No abri ninguna corrida. Todas mis puertas son ejecucion directa
  en clon limpio.
- **No afirmo que la paridad del inventario de identidad este acreditada.** Acreditada esta la CAJA
  -- ruta, digest y ahora el universo de terminos. La COORDENADA no.

## 5. Residuales declarados

- **RES-2-GUARD (NUEVO)** -- W4: el arreglo ordinal de la linea 211 no tiene negativo. `mut211`
  revierte solo esa linea en produccion y los 11 tests siguen verdes, con la paridad medida y rota.
  Ningun test referencia `Get-ConfiguredIdentityTerms`/`StringComparer`, y sobre el arbol real
  ninguno puede enrojecer porque la config no tiene identidades que difieran solo en caja.
- **RES-1 (vigente, BLOQUEANTE en su propia tarea)** -- la coordenada del inventario diverge entre
  gemelos por el troceo de lineas; cinco separadores, PowerShell el permisivo. Enrutado a TASK-0338.
- **RES-4 (vigente)** -- `StartsWith`/`EndsWith` sensibles a cultura, divergentes pero inalcanzables
  tras la seleccion por globs ordinales.
- **RES-A (vigente)** -- el detector de coordenadas muertas sigue rio abajo de
  `assertEqual(python_inventory, powershell_inventory)`: cualquier divergencia de paridad lo
  enmascara entero. La r2 no lo toco.
- **RES-B (vigente)** -- `assertEqual(declared_exemption_count, expected_exemption_count)` sigue
  subsumida por la paridad afirmada antes.
- **RES-C (vigente)** -- `.claude/skills/**` sigue con 0 cobertura de escaneo.
- **RES-E (vigente)** -- `ToLowerInvariant()` vs `casefold()`; sondeado en F5/F6, sin explotacion.

## 6. Recomendacion

**OK-CLOSABLE.** Las dos cosas que el encargo me mando refutar sobreviven a mi intento:

1. **RES-3 esta acreditado**, y con mas margen del que se pidio: el negativo mata el revert de texto
   Y mata una regresion que deja la clausula intacta, y la produccion restaurada sobrevive dos
   veces. Esa era la pieza que importaba y esta puesta.
2. **RES-2 cierra por efecto**, sobre la familia y no sobre el ejemplo, con el control historico
   rompiendo cuatro de los seis vectores. El verde no lo produce el codigo viejo.

**Por que no bloqueo con RES-2-GUARD, habiendolo medido.** Por tres razones que declaro para que
otro pueda discrepar con los mismos datos:

- **Consistencia con mi propio criterio.** En la r1 encontre esta misma forma exacta -- arreglo
  presente, sin guardia -- en el digest, y **no bloquee por ella**: la registre como RES-3 y bloquee
  por RES-1, que era un defecto de comportamiento VIVO. Aqui el comportamiento es correcto hoy y
  esta medido; lo que falta es la red que impida reintroducirlo. Cambiar de vara ahora seria
  arbitrario.
- **Presupuesto de iteraciones.** Declare dos, esta es la segunda, y el protocolo dice que a la
  tercera se escala al operador humano. Una tercera vuelta por deuda de negativo, no por defecto,
  gastaria el escalado en lo que no lo merece.
- **El cierre de 0410 ya es un cierre CON residuales nombrados**, no un cierre que afirma paridad.
  RES-2-GUARD entra ahi de forma natural.

**Lo que el cierre tiene que decir, y sin lo cual retiro el OK-CLOSABLE:** que TASK-0410 se cierra
con la CAJA acreditada -- ruta, digest y universo de terminos, con el digest ya guardado -- y con
**dos** cosas abiertas y nombradas: **RES-1**, la coordenada, en TASK-0338; y **RES-2-GUARD**, la
falta de negativo para la linea 211. No vale cerrar afirmando "paridad de inventario de identidad
acreditada".

**Sugerido, no bloqueante, y barato:** RES-2-GUARD cabe en TASK-0338, que ya va a tocar este mismo
fichero y esta misma familia de paridad; el negativo es la sonda F1 de arriba convertida en test --
una config con dos identidades que difieren solo en caja debe dar el MISMO conjunto de hallazgos en
los dos gemelos, y debe MORIR contra `b899167b^`. Lo he medido: muere. Esa decision es del
Arquitecto, no mia.

**Nota de coordinacion, con el mismo animo con el que el Arquitecto me senalo la suya:** este es el
segundo residual consecutivo de la forma "arreglo sin guardia" en la misma cadena de remediacion. No
es descuido del maker en una linea concreta; es que el lazo de arreglo pide el arreglo y trata el
negativo como opcional cuando el residual se describe en una frase. Si el patron interesa, se corta
pidiendo el negativo en el mismo renglon que el arreglo, no en el siguiente.

-- Analista, 2026-08-22 07:39 local (UTC+2)
