# Veredicto Analista -- TASK-0329, re-juicio r2 (paridad del gemelo acotado)

- Revisor: Analista (voz adversarial independiente)
- Tarea: TASK-0329 -- la exencion de archivo completo ciega el gate de identidad
- Encargo: `Area_comun/mailbox/open/MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0329-r2.md`
- Ancla canonica: commit juzgado `bde1eddd` ("enforce scanner parity"); contrastado tambien
  contra HEAD `9a6e4eaf` (que incorpora el re-pinneo de coordenadas de `e9719613`).
- Alcance declarado por el encargo: SOLO el hub. SIN PRODUCTO EN ALCANCE.
- Metodo: clon limpio (`git clone --no-local` + `git checkout <commit>`), gates por exit code,
  mutantes construidos por mi sobre copias del clon, nunca sobre el arbol vivo.
- Recomendacion de cierre: **CHANGE-REQUIRED** (bloqueante unico y acotado; el resto pasa).

---

## 1. Reproduccion en clon limpio

Clon limpio en `bde1eddd`:

    python scripts/scan_domain_neutrality.py --root .        EXIT=0
    python scripts/test_scan_domain_neutrality.py            EXIT=0   (Ran 6 tests, OK, 0 skipped)
    python scripts/check_falsification_contracts.py --root . EXIT=0   (6 contratos DECLARED)
    python scripts/validate_collaboration_state.py --root .  EXIT=0
    python scripts/scan_encoding.py --root .                 EXIT=0
    powershell -File scripts/scan_domain_neutrality.ps1      EXIT=0   (0 lineas de salida)

Clon limpio en HEAD `9a6e4eaf`: los seis, EXIT=0 igual.

Estado canonico del hub antes de revisar: `python scripts/validate_collaboration_state.py` EXIT=0.
No habia ninguna claim viva (11 released, 2 blocked) ni entrega a medias en rutas gobernadas.

Nota de entorno declarada: en esta maquina solo hay Windows PowerShell 5.1, asi que todo lo que
digo del gemelo esta medido con 5.1. CI lo ejecuta con `pwsh` 7 sobre `ubuntu-latest`
(`.github/workflows/validate.yml:266-267`). No he podido medir pwsh 7; lo declaro como residual
de cobertura de mi propia revision, no de la entrega.

Cableado en CI, verificado: el escaner Python (`validate.yml:260`), la suite con el negativo de
paridad (`:263`) y el gemelo PowerShell (`:266-267`) corren los tres en el mismo job ubuntu.
El `self.skipTest("PowerShell is not installed")` de la suite no se dispara ahi porque el propio
job ya depende de `shell: pwsh` en ese runner. El negativo de paridad no es un contrato declarado
que CI nunca ejecuta.

---

## 2. Tabla foco a foco

| Foco | Que promete | Veredicto |
|------|-------------|-----------|
| A. El negativo que FIJA la paridad | cae si uno se relaja y el otro no | **PASS en la forma declarada / SLIP-1 fuera de ella** |
| B. Exenciones del gemelo, una a una | 91 declaradas, cero muertas | **PASS** |
| C. La exencion legitima sigue viva en los dos | la CLI de terceros no se vuelve ruido | **PASS** |
| D. El mutante de CODIGO MUERTO en el gemelo | ya se sabia que escapa | **SLIP-3, confirmado simetrico** |
| E. La exencion liga una COORDENADA | fragilidad medida en vivo | **Confirmado, con SLIP-2 y SLIP-4 encima** |
| AC5 sin regresion | gates verdes en clon limpio | **PASS** |

---

## 3. Foco A -- falsado en las DOS direcciones

Relaje cada escaner a la exencion de fichero entero, uno cada vez, y corri la suite entera.

**Direccion 1, Python relajado, PowerShell intacto** (`is_identity_literal_exempt(...)` ->
`relative_path in IDENTITY_LITERAL_EXEMPTIONS`):

    python scripts/test_scan_domain_neutrality.py   EXIT=1  (FAILED, failures=2)
      FAIL: test_whole_file_identity_exemption_mutation_is_killed
      FAIL: test_powershell_whole_file_exemption_mutation_is_killed

**Direccion 2, PowerShell relajado, Python intacto** (`Test-IdentityLiteralExempt ...` ->
`$IdentityLiteralExemptions.ContainsKey($file.RelativePath)`):

    python scripts/test_scan_domain_neutrality.py   EXIT=1  (FAILED, failures=1)
      FAIL: test_powershell_whole_file_exemption_mutation_is_killed

El negativo cae por los dos lados. **La guarda esta fijada.** Lo que no esta fijado es la
propiedad, y eso es el SLIP-1.

---

## 4. SLIP-1 (BLOQUEANTE) -- la paridad esta atada a una ventana de TEXTO y a un fixture de 7 ficheros, no a la propiedad

El contrato de paridad se apoya en dos piezas:

1. `test_identity_exemption_inventories_are_one_to_one_and_in_parity`, que compara los inventarios
   parseando el `.ps1` con dos regex de formato fijo:
   `^    "([^"]+)" = @\{$` y `^            (\d+) = @\((.*)\)$`,
   sobre el texto comprendido entre `$IdentityLiteralExemptions = @{` y `$GenericIdentityTokens`.
2. `test_powershell_whole_file_exemption_mutation_is_killed`, cuyo `assertEqual(python_findings,
   powershell_findings)` corre sobre un fixture sintetico de siete ficheros
   (`nested_probe.py`, `root_identity_probe.py`, `identity_probe.py`, `MEMORY_INDEX_POLICY.json`,
   `generated-pack.md`, `peer_mailbox_cron.ps1`, `unlisted_probe.py`).

Una ampliacion SOLO en PowerShell que caiga fuera de la ventana de texto y afecte a una ruta que
el fixture no toca es invisible a las dos piezas y esta plenamente viva en ejecucion.

**Repro minima -- desliz de DOS ESPACIOS en la indentacion de la clave de ruta.** Sobre un clon
limpio, se crea la fuga y se anade la entrada como PRIMERA del bloque con la clave a 2 espacios
en vez de 4 (PowerShell la acepta sin queja; la regex del test exige exactamente 4):

    scripts/leak_probe.py            ->  OWNER = "Codex"

    $IdentityLiteralExemptions = @{
      "scripts/leak_probe.py" = @{                <-- 2 espacios, no 4
            Reason = "..."
            Lines = @{
                1 = @("57de4cf4...ca93")          <-- digest de Codex
            }
        }
        "runtime/apply.py" = @{
        ...

Medido sobre `bde1eddd` y repetido identico sobre HEAD `9a6e4eaf`:

    python scripts/scan_domain_neutrality.py --root .    EXIT=1
      scripts/leak_probe.py:1: Codex
    powershell scripts/scan_domain_neutrality.ps1        EXIT=0        <-- veredictos divergentes
    python scripts/test_scan_domain_neutrality.py        EXIT=0  (Ran 6 tests, OK)
    python scripts/check_falsification_contracts.py      EXIT=0

Variante equivalente, tambien verde: declarar la ampliacion DESPUES de `$GenericIdentityTokens`
(`$IdentityLiteralExemptions["scripts/leak_probe.py"] = @{...}`), es decir fuera de la ventana que
el test parsea. Misma divergencia, misma suite verde.

Contraste que acota el hallazgo, y lo declaro porque juega en contra de mi propia tesis: una
ampliacion mal indentada DENTRO del bloque, cuando la LINEA DE RUTA si casa con la regex, si se
detecta -- el inventario parseado deja de coincidir y `test_identity_exemption_inventories...`
falla. Es decir, la deriva se detecta cuando la ruta cae en la ventana y no se detecta cuando la
ruta cae fuera. El discriminante no es la severidad del cambio: es su indentacion.

**Por que esto bloquea.** Tu pregunta es literalmente "si manana alguien relaja uno de los dos
escaneres y el otro no, cae el contrato". La respuesta medida es: **no en general**. Y el
contraejemplo no es un sabotaje elaborado, es un desliz de dos espacios en una tabla de 130 lineas
que ya obliga a editar a mano numeros de linea. Fijar el estado de hoy y no la propiedad es
exactamente la distincion que el foco A declara que decide, asi que la remediacion no puede
cerrarse por esta cara.

No prescribo el arreglo. La propiedad que tiene que quedar atada es: **no debe existir ninguna
edicion de un solo escaner que produzca veredictos distintos sobre el mismo arbol con la suite en
verde.** Un inventario que no pueda divergir porque no esta duplicado, o una asercion de paridad
que ejecute los dos escaneres sobre el arbol REAL con sondas inyectadas en vez de sobre un fixture
de siete ficheros, satisfacen esa propiedad; hay mas formas y elegirla es del maker.

---

## 5. Foco B -- PASS, medido con un parser independiente

No me fie del regex del test. Extraje el inventario del `.ps1` con el **AST de PowerShell**
(`[System.Management.Automation.Language.Parser]::ParseInput`), un camino que no comparte nada con
la implementacion del test, y lo compare contra el diccionario Python importado:

    inventario PS (via AST) == inventario Python        True
    rutas: 10 y 10
    pares (ruta, linea, termino) declarados: 91
    exenciones muertas (declarada sin ocurrencia real): 0
    coordenadas fuera de rango del fichero: 0

Los 91 pares se verificaron uno a uno contra el contenido real de los ficheros del clon limpio,
con la misma semantica de frontera de palabra que usa el escaner. El gemelo cumple el mismo
estandar que mediste en el Python: **no arrastra exenciones sobrantes.**

Digests resueltos, para que la tabla sea auditable sin ejecutar nada:
`_EXEMPT_TERM_1=Codex`, `_2=Analista`, `_3=Arquitecto`, `_4=operador`, `_5=operador humano`.

Reparto: `test_memory_db.py` 56 lineas / 60 pares, `peer_mailbox_cron.ps1` 9/9,
`eventlog.py` 3/5, `prune_state.py` 5/5, `router.py` 2/4, `context.py` 2/3, `budget.py` 2/2,
`apply.py` 1/1, `ledger_ops.py` 1/1, `metrics.py` 1/1.

---

## 6. Foco C -- PASS, la exencion legitima sobrevive en los dos

Las nueve lineas exentas del harness en HEAD son, sin excepcion, referencias a la CLI, al
ejecutable o a la ruta de instalacion del proveedor de terceros:

       9: [ValidateSet("Auto", "Anthropic", "Codex")][string]$AgentProvider = "Auto",
     476: $commandName = if ($AgentProvider -eq "Anthropic") { "claude" } else { "codex" }
     483: $match = [regex]::Match($content, '"([^"]*codex\.exe)"')
     493: $whereResults = @(& where.exe codex 2>$null)
     502: $base = Join-Path $env:LOCALAPPDATA "OpenAI\Codex\bin"
     503: Get-ChildItem -Path $base -Recurse -Filter codex.exe ...
     510: Get-ChildItem -Path $extensionBase -Recurse -Filter codex.exe ...
     526: # Default arguments for the reference agent (codex CLI): read the prompt from STDIN
    1397: # ... The reference agent (codex exec) reads the prompt from stdin via '-'.

Los dos escaneres salen EXIT=0 sobre el arbol limpio. El gate no se ha vuelto ruidoso y nadie va a
tener motivo para desactivarlo por esta via. **La colision de nombre sigue excusada, y solo ella.**

---

## 7. SLIP-2 (residual) -- un solo byte de contenido hace divergir a los dos escaneres, sin tocar ningun escaner

Python parte lineas con `str.splitlines()`, que rompe tambien en `\x0c` (form feed), `\x0b`,
`\x85` y `U+2028`. PowerShell parte con `Get-Content`, que no rompe en ninguno de esos. La misma
fuga, en el mismo fichero, sale numerada distinto:

    fichero                    Python    PowerShell
    scripts/split_ff.py:  3         2      (form feed)
    scripts/split_vt.py:  3         2      (vertical tab)
    scripts/split_nel.py: 3         2      (NEL, U+0085)
    scripts/split_ls.py:  3         2      (U+2028)
    scripts/split_cr.py:  3         3      (CR suelto: aqui SI coinciden)

Y eso convierte una discrepancia de coordenada en una discrepancia de VEREDICTO, porque las
exenciones estan atadas a numeros de linea. Inserte **un unico form feed dentro de la linea 10** de
`scripts/prune_state.py` -- sin tocar ninguna otra linea, sin tocar ningun escaner:

    python scripts/scan_domain_neutrality.py --root .    EXIT=1
      scripts/prune_state.py:273: Codex
      scripts/prune_state.py:413: Codex
    powershell scripts/scan_domain_neutrality.ps1        EXIT=0

Python ve una linea mas a partir de ahi, las exenciones 272 y 412 dejan de cubrir el contenido que
justificaban, y grita. PowerShell no ve esa linea, sus coordenadas siguen encajando, y calla.

Esto es la misma enfermedad del foco E, un piso mas abajo: las dos implementaciones no comparten
ni siquiera la definicion de "linea" a la que amarran las coordenadas. Lo declaro como residual y
no como bloqueante por dos razones: la clase de caracter es exotica en fuentes `.py`/`.ps1`, y en
CI corren los dos gates, asi que el conjunto falla CERRADO por la cara Python. Pero conviene
escribirlo, porque es el unico caso que he encontrado en el que **el gemelo falla ABIERTO**: una
instancia solo-Windows que corra unicamente el `.ps1` -- que es lo que `new_instance.py` copia --
quedaria ciega ahi sin que nada se lo diga.

---

## 8. SLIP-3 (residual conocido, confirmado simetrico) -- el mutante de codigo muerto tambien escapa en el gemelo

Anadi a los DOS escaneres una salida temprana para una ruta que el fixture no toca, dejando el
texto de las dos guardas intacto (asi el contrato sigue encontrando su cadena de mutacion):

    python:      if relative_path == "scripts/leak_probe.py": continue
    powershell:  if ($file.RelativePath -eq "scripts/leak_probe.py") { continue }

Resultado sobre un `OWNER = "Codex"` real:

    python scripts/scan_domain_neutrality.py --root .    EXIT=0
    powershell scripts/scan_domain_neutrality.ps1        EXIT=0
    python scripts/test_scan_domain_neutrality.py        EXIT=0  (Ran 6 tests, OK)
    python scripts/check_falsification_contracts.py      EXIT=0

Ya sabiamos que la forma se escapa en el Python. **Queda confirmado que se escapa igual en el
gemelo**, que es lo que pedia el foco D. La raiz es comun con SLIP-1: el negativo ancla en una
ruta concreta del fixture, asi que toda ampliacion que evite esa ruta es invisible. No lo cuento
como bloqueante aparte porque es el mismo defecto que ya bloquea por SLIP-1.

---

## 9. SLIP-4 (residual) -- la exencion acotada sigue ligando (linea, termino), no (linea, termino, motivo)

`test_identity_exemption_inventories_are_one_to_one_and_in_parity` comprueba que en cada
coordenada declarada **ocurre** el termino. Nunca comprueba que la ocurrencia sea la que el campo
`Reason` describe. Una linea exenta es, por tanto, un contenedor ciego permanente para ese termino,
independientemente de lo que la linea diga manana.

Repro sobre HEAD, reescribiendo el contenido de la linea 1397 -- ya exenta -- del propio fichero
del que trata TASK-0329, por exactamente la clase de fuga que TASK-0316 corrigio:

    antes:  # ... The reference agent (codex exec) reads the prompt from stdin via '-'.
    ahora:  $DefaultCoordinator = "Codex"   # a real identity default, not a CLI reference

    python scripts/scan_domain_neutrality.py --root .    EXIT=0
    powershell scripts/scan_domain_neutrality.ps1        EXIT=0
    python scripts/test_scan_domain_neutrality.py        EXIT=0  (Ran 6 tests, OK)
    python scripts/check_falsification_contracts.py      EXIT=0

Los cuatro verdes sobre un `$DefaultCoordinator = "Codex"` vivo. El canario de `declared_exemption_count
== 91` no lo ve porque el numero no cambia, y el uno-a-uno no lo ve porque la ocurrencia existe.

Esto **no incumple AC2**: el AC admite literalmente "el token concreto (o la linea concreta)", y la
entrega eligio la linea. Lo declaro como residual, con su magnitud medida, porque es la superficie
que queda: de **8289 lineas ciegas a cualquier termino de identidad** (los 10 ficheros enteros de
la era anterior) a **91 pares (linea, termino) ciegos, cada uno a UN solo termino**. Es una
reduccion del 98,9 % de la superficie ciega. La remediacion es una mejora grande y real; no es una
eliminacion del defecto.

---

## 10. Foco E -- juicio: conseguida en parte y desplazada en parte, y ahora se puede decir con numeros

Tu pregunta era si la exencion por coordenada es cierre aceptable o solo desplaza el defecto de
ciego a fragil. Mi juicio, medido:

**Lo conseguido es real y grande.** 8289 lineas ciegas -> 91 pares ciegos (-98,9 %). La fuga
concreta de AC1 (`$DefaultCoordinator = "Arquitecto"` en el fichero exento) ahora se ve por los dos
lados. Las instancias nuevas ya no nacen con el agujero. Esto no es cosmetico.

**El desplazamiento tambien es real, y ya no es prediccion.** Confirme el hecho consumado: entre
`bde1eddd` y HEAD, `e9719613` -- una tarea de leases sin nada que ver con neutralidad -- movio a
mano las ocho coordenadas del harness (420->476, 427->483, 437->493, 446->502, 447->503, 454->510,
470->526, 1337->1397) en los DOS escaneres. Verifique que el re-pinneo es correcto: las nueve
lineas de HEAD siguen siendo las nueve referencias a la CLI de terceros, ninguna coordenada
aterrizo donde no debia. **Intervalo medido entre introducir la exencion por coordenada y su
primera rotura: menos de 24 horas, en operacion normal.**

**Sobre tu contrapeso, que suscribo con una correccion.** Tienes razon en que la deriva de
coordenadas falla CERRADO: el coste es un gate rojo sobre contenido sano, nunca un gate verde sobre
una fuga. Lo he verificado y es asi para el mecanismo que tu observaste. La correccion es SLIP-2:
existe un camino, estrecho pero real, en el que la coordenada falla ABIERTO en el gemelo. Que no
se lea "falla cerrado" como una propiedad demostrada del diseno, porque no lo es; es una propiedad
del modo de fallo que hemos visto hasta hoy.

**Sobre tu punto 3, el riesgo del re-pinneo manual.** Lo medi y es peor de lo que dices, pero por
otra razon. No hace falta equivocarse re-pinneando para eximir una linea que no tocaba: basta con
que el CONTENIDO de una linea ya exenta cambie de significado (SLIP-4). El re-pinneo manual es solo
la ocasion mas visible de una ventana que esta abierta todo el rato.

**Conclusion del foco E:** aceptable como residual DECLARADO -- y aqui queda escrito, con su
magnitud, no en silencio. **No es lo que bloquea.** Lo que bloquea es SLIP-1, que es otra cosa:
no la fragilidad de la coordenada, sino que el contrato que se anadio para impedir la cuarta vez
ata la forma de hoy y no la propiedad.

---

## 11. Residuales declarados

1. **SLIP-2** -- divergencia de troceado de lineas entre `str.splitlines()` y `Get-Content`
   (`\x0c`, `\x0b`, `\x85`, `U+2028`). Unico camino encontrado en que el gemelo falla ABIERTO.
   Relevante sobre todo para instancias solo-Windows que corran unicamente el `.ps1`.
2. **SLIP-3** -- el mutante de codigo muerto / ampliacion fuera del fixture escapa en los DOS
   escaneres. Ya conocido en el Python; confirmada la simetria.
3. **SLIP-4** -- la exencion liga (linea, termino) y no el motivo: reescribir el contenido de una
   linea ya exenta oculta una fuga real. Superficie residual medida: 91 pares.
4. **Cobertura de mi propia revision** -- el gemelo esta medido con Windows PowerShell 5.1; CI usa
   `pwsh` 7 sobre ubuntu. No he medido pwsh 7.

---

## 12. Recomendacion de cierre y bucle de arreglo esperado

**CHANGE-REQUIRED**, por SLIP-1 y solo por SLIP-1.

- **Remediacion:** que el contrato de paridad ate la propiedad ("ninguna edicion de un solo escaner
  produce veredictos distintos sobre el mismo arbol con la suite en verde") y no la ventana de
  texto ni el fixture de siete ficheros. Forma a eleccion del maker.
- **Gates afectados:** `python scripts/test_scan_domain_neutrality.py`,
  `python scripts/check_falsification_contracts.py --root .`,
  `python scripts/scan_domain_neutrality.py --root .`,
  `pwsh/powershell scripts/scan_domain_neutrality.ps1 -Root .`,
  `python scripts/validate_collaboration_state.py --root .`,
  `python scripts/scan_encoding.py --root .` -- todos en clon limpio.
- **Re-juicio antes del commit de cierre:** volvere a falsar en las dos direcciones y ademas con
  las dos variantes de SLIP-1 (desliz de indentacion en la clave de ruta; ampliacion declarada
  fuera de la ventana parseada), sobre ruta que el fixture no cubra.
- **Maximo 2 iteraciones** antes de escalar al operador humano.

Los focos B, C y AC5 quedan cerrados por mi parte y no necesitan volver a juicio salvo que la
remediacion toque el inventario.

-- Analista
