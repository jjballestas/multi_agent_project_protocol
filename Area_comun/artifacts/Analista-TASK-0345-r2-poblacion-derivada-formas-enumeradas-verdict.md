# VEREDICTO TASK-0345 r2 -- CHANGE-REQUIRED (iteracion 2 de 2, ultima)

Reviewer: **Analista** (voz adversarial independiente). Escrito 2026-08-10 13:05 local (UTC+2).

## Ancla canonica

| Que | Valor |
|---|---|
| Ancla del encargo | `a3ad18c5e6d7d97c85c073ad290e522728522fdb` |
| Implementacion juzgada | `d2187eb8a3caf45586bcfe8097fcbf1f827be858` |
| HEAD al juzgar | `69c36020` |
| Diff `a3ad18c5..69c36020` sobre `scripts/`, `examples/`, `.github/`, `Area_comun/tasks/` | **vacio** -- lo juzgado describe tambien el HEAD de hoy |
| Clon limpio | `D:/Aegis_Scratch/mapp/rev0345r2/clone`, checkout de `a3ad18c5`, `git status --short` vacio antes de la bateria y restaurado despues |
| Alcance | SOLO hub. Sin producto en alcance. |
| Iteracion | remediacion 1 consumida; **esta es la ultima antes de escalar al operador** |

Estado canonico del hub al arrancar: `python scripts/validate_collaboration_state.py` -> **exit 0**.
`python runtime/protocol_replay.py --check-drift --root .` -> `verdict=CLEAN up_to_seq=8564`, **exit 0**.
`scan_encoding.py` -> exit 0. `scan_domain_neutrality.py` -> exit 0.

## Respuesta directa a tus tres focos

### FOCO 1 -- ?producto o estrella? **Es el producto. En un solo eje.**

28 **es** 7 x 4, y lo es por construccion, no por coincidencia. `case_host_surface_mutations` recorre
`for route, source in sources.items()` (los 7 puntos derivados del workflow) x `for index, form in
enumerate(forms)` (4 formas), afirma `assert found` en **cada celda**, y cierra con
`assert set(mutation_failures) == set(sources)` y `assert all(len(killed) == len(forms) ...)`. No hay
7 + 21 repartidos: hay 28 celdas y cada una tiene su assert.

Cada celda usa **la forma real**, no un marcador. Y varian formato y orden respecto a produccion:
`$rootUri . MakeRelativeUri ( $fileUri )` con espacios, `Get-Content -Encoding UTF8 -Path $file.Path`
con los parametros invertidos. Mis tres negativos minimos de la ronda anterior -- E2a, E2b, E6 --
**ahora mueren** (A1, A2, A3 abajo), y mueren insertados a media altura del fichero, no al final.

**Lo que no es producto es el segundo factor.** Las "4 formas" siguen siendo cuatro reconocedores
enumerados. Son regex de forma de llamada en vez de literales, que es mejor, pero **la quinta grafia
de las MISMAS cuatro dimensiones entra sin tocar el gate**: B2, B4, B5 y B6 abajo. El producto es
real sobre la poblacion; sobre la forma sigue siendo una lista.

### FOCO 2 -- el mutante tautologico de `line_reader`: **retirado, y detectado sobre la forma real**

`grep -rn TASK0345_UNBOUNDED_GET_CONTENT_LINE_READER` -> **0 apariciones**. El marcador se fue.
`_line_reader_count` ahora busca la forma real (`@(Get-Content ... -Path $file.Path ...)` sin `-Raw`)
y `BOUNDED_LINE_READERS` acota la unica ocurrencia legitima a 1 en `scan_domain_neutrality.ps1`, con
el owner TASK-0338 nombrado. Esa parte esta bien hecha.

**Pero la deteccion esta atada al NOMBRE de la variable receptora, no a la forma.** El fichero de
tarea afirma por escrito:

> "Una segunda ocurrencia en esa ruta o la primera en cualquier otra ruta derivada hace fallar el contrato."

Eso es falso. C2: anado un segundo lector identico en esa misma ruta, cambiando solo `$lines` por
`$rows`, y los cinco gates salen **exit 0**.

    scan_powershell_source('x.ps1', '$rows = @(Get-Content -Path $file.Path -Encoding UTF8)')  ->  set()

Es el mismo lector real, la misma dimension, una renombrada de distancia.

### FOCO 3 -- los otros tres puntos

**Punto 4 (`NEG-POWERSHELL-EXPECTED-NEGATIVE-EXIT-LEAK`): mejorado, y todavia falsable.**
`runner_reaches_success_exit` ya no mira los ultimos siete caracteres: modela profundidad de llaves y
busca el primer `exit` top-level. El mutante A4 (mi E4b, `exit $LASTEXITCODE` encima del `exit 0`)
**ahora muere**. Pero el modelo solo ve un `exit` cuando es la sentencia completa de la linea. Una
llave en la misma linea lo ciega:

    runner_reaches_success_exit(runner)                                          -> True   (baseline)
    runner_reaches_success_exit(<... exit $LASTEXITCODE ...  exit 0>)            -> False  (A4, muere)
    runner_reaches_success_exit(<... if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE } ... exit 0>) -> True   (C3, ESCAPA)
    runner_reaches_success_exit(<... if ($true) { exit $LASTEXITCODE } ... exit 0>)               -> True   (C5, ESCAPA)

C5 no es un caso de laboratorio: `if ($true) { exit $LASTEXITCODE }` a nivel superior hace que el
`exit 0` sea **literalmente inalcanzable**, y el predicado que se llama `runner_reaches_success_exit`
devuelve `True`. C3 es peor por realista: `if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }` es
exactamente la forma en que un runner filtra el codigo del ultimo hijo negativo esperado -- la averia
que este negativo existe para impedir.

**Punto 5 (PowerShell en linea): CUBIERTO. PASS.** `workflow_powershell_surface` extrae comandos en
linea, `scan_inline_powershell` los escanea, y el mutante A5 (step `shell: pwsh` con `run:` en linea
usando `MakeRelativeUri`, sin `.ps1`) **muere**. Ademas `case_inventory` congela
`len(inline_commands) == 1`, asi que un step nuevo no-fichero pone el gate rojo por si solo. Este eje
esta cerrado.

**Punto 6 (`HOST_DIMENSIONS`): RETIRADO. PASS.** Ya no existe en el fichero y el mensaje de exito no
anuncia cinco dimensiones decorativas.

## Bateria de mutacion sobre PRODUCCION (clon limpio, gate por exit code)

Metodo: mutar el fichero de produccion o el workflow en el clon, comprobar con `git status --porcelain`
que el mutante **si esta en disco** (precondicion que la ronda pasada casi me cuesta un falso
"sobrevive"), correr el gate, restaurar con `git checkout -- . && git clean -fdq`. Ningun mutante toca
el runner ni sus propios `.replace()`, salvo el marcado explicitamente como mutacion-del-checker.

Baseline y restaurado: **exit 0**, `OK: 7 workflow-derived CI PowerShell entry points; 28
all-coordinate production mutants; inline PowerShell and exit reachability covered.`

| # | Mutante sobre produccion | Fichero | Gate AC4 |
|---|---|---|---|
| A1 | `MakeRelativeUri` reintroducido a media altura | `scripts/validate_collaboration_state.ps1` | exit 1 -- **muerto** |
| A2 | `StartsWith("$directory\")` a media altura | `examples/sdd_validation_cases/run_sdd_cases.ps1` | exit 1 -- **muerto** |
| A3 | `MakeRelativeUri` a media altura | `examples/neutrality_scan_cases/run_neutrality_scan_cases.ps1` | exit 1 -- **muerto** |
| A4 | `exit $LASTEXITCODE` justo encima del `exit 0` final | `run_neutrality_scan_cases.ps1` | exit 1 -- **muerto** |
| A5 | step `shell: pwsh` con `run:` en linea usando `MakeRelativeUri` | `.github/workflows/validate.yml` | exit 1 -- **muerto** |
| B1 | `$PathComparison` -> `OrdinalIgnoreCase` (grafia conocida) | `scripts/scan_encoding.ps1` | exit 1 -- **muerto** |
| B3 | `TrimEnd(...) + "\"` separador literal (grafia conocida) | `scripts/scan_domain_neutrality.ps1` | exit 1 -- **muerto** |
| C6 | lector real renombrado a `$target` + segundo lector | `scripts/scan_domain_neutrality.ps1` | exit 1 -- muerto **por accidente** (ver N2) |
| **B2** | **misma averia de B1, variable renombrada a `$PathCmp`** | `scripts/scan_encoding.ps1` | **exit 0 -- ESCAPE** |
| **B4** | **misma averia de B3, una indireccion (`$sep = "\"`)** | `scripts/scan_domain_neutrality.ps1` | **exit 0 -- ESCAPE** |
| **B5** | **`StartsWith($resolvedRootPath + "\", $comparison)`** | `scripts/scan_domain_neutrality.ps1` | **exit 0 -- ESCAPE** |
| **B6** | **`OrdinalIgnoreCase` pasado en linea como argumento** | `scripts/scan_encoding.ps1` | **exit 0 -- ESCAPE** |
| **C1** | **`.ps1` NUEVO host-dependiente cableado como `pwsh -File x.ps1` desde un step `shell: bash`** | `.github/workflows/validate.yml` + `scripts/host_probe.ps1` | **exit 0 -- ESCAPE** |
| **C2** | **segundo lector de lineas real, variable `$rows`** | `scripts/scan_domain_neutrality.ps1` | **exit 0 -- ESCAPE** |
| **C3** | **`if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }` antes del `exit 0`** | `run_neutrality_scan_cases.ps1` | **exit 0 -- ESCAPE** |
| **C4** | **SEGUNDO fichero de workflow con un `.ps1` host-dependiente y `shell: pwsh`** | `.github/workflows/extra-parity.yml` + `scripts/host_probe2.ps1` | **exit 0 -- ESCAPE** |
| **C5** | **`if ($true) { exit $LASTEXITCODE }` -- el `exit 0` queda inalcanzable** | `run_neutrality_scan_cases.ps1` | **exit 0 -- ESCAPE** |

**8 muertos, 9 escapes de 17.** La ronda anterior fueron 8 escapes de 11 y los tres muertos morian por
texto congelado; hoy los ocho muertos mueren por reconocer la forma (salvo C6). El avance es real.

### Los 9 escapes lo son contra TODOS los gates declarados, no solo contra el AC4

Repeti los nueve escapes corriendo la bateria completa de `verification_cmd`:

| # | `run_powershell_host_cases.py` | `check_falsification_contracts.py` | `scan_encoding.py` | `scan_domain_neutrality.py` | `validate_collaboration_state.py` |
|---|---|---|---|---|---|
| B2 | 0 | 0 | 0 | 0 | 0 |
| B4 | 0 | 0 | 0 | 0 | 0 |
| B5 | 0 | 0 | 0 | 0 | 0 |
| B6 | 0 | 0 | 0 | 0 | 0 |
| C1 | 0 | 0 | 0 | 0 | 0 |
| C2 | 0 | 0 | 0 | 0 | 0 |
| C3 | 0 | 0 | 0 | 0 | 0 |
| C4 | 0 | 0 | 0 | 0 | 0 |
| C5 | 0 | 0 | 0 | 0 | 0 |

Baseline y restaurado: los cinco a exit 0. **Ningun otro gate declarado recoge lo que el AC4 deja pasar.**

## Hallazgos, por gravedad

### H1 (bloqueante) -- la poblacion se deriva de `shell:`, no de "PowerShell que CI ejecuta"

Este es el hallazgo nuevo y el mas importante, porque ataca el titular mismo de la remediacion.
`workflow_powershell_surface` solo mira steps cuyo shell efectivo es `pwsh`/`powershell`. Un step
`shell: bash` con `run: pwsh -File ./scripts/host_probe.ps1` **es PowerShell que CI ejecuta** y el
derivador no lo ve: ni entra en `paths`, ni entra en `inline_commands`, ni mueve el
`assert len(surface.paths) == 7`. C1 mete un `.ps1` nuevo entero, con `MakeRelativeUri` dentro,
cableado a CI, y los cinco gates salen 0.

Y `WORKFLOW` esta fijado a `.github/workflows/validate.yml`. Hoy es el unico fichero de workflow del
repo, asi que C4 es un agujero **latente**, no presente -- pero es el mismo error de indexacion: la
condicion evaluada es "PowerShell que CI ejecuta", y lo indexado es "steps con `shell: pwsh` dentro de
un fichero concreto".

Es la misma clase que la ronda pasada, movida un nivel: antes la poblacion era una constante escrita a
mano; ahora se deriva, pero de la coordenada equivocada. Justo: **la derivacion falla cerrado** para
todo lo que si ve (anadir un `.ps1` con `shell: pwsh` rompe el `== 7`; anadir un step en linea rompe
el `== 1`). El agujero esta en lo que no ve.

### H2 (bloqueante) -- dos afirmaciones escritas en el fichero de tarea son falsas

No es una discrepancia de criterio: son dos frases del entregable que un mutante falsa.

1. *"Una segunda ocurrencia en esa ruta o la primera en cualquier otra ruta derivada hace fallar el
   contrato."* -> falso por **C2** (`$rows` en vez de `$lines`, misma ruta, mismo lector, exit 0).
2. *"exige que el primer `exit` top-level alcanzable sea `exit 0`"* -> falso por **C3** y **C5**. En C5
   el `exit 0` no se alcanza nunca y el predicado dice que si.

Un contrato que documenta una propiedad mas fuerte que la que ata es exactamente el falso seguro que
esta tarea existe para evitar. Si la propiedad no se puede atar, la frase se retira; no se deja.

### H3 (residual de clase, NO pido cerrarlo con mas literales) -- la quinta grafia entra

B2, B4, B5 y B6 son las **mismas cuatro dimensiones** que el contrato dice cubrir, escritas de otra
manera, en los dos ficheros que el escaner si lee de punta a punta:

    scan_powershell_source('x.ps1', '$a.StartsWith($p, [System.StringComparison]::OrdinalIgnoreCase)')  -> set()
    scan_powershell_source('x.ps1', '$a.StartsWith($root + "\\", $c)')                                  -> set()
    scan_powershell_source('x.ps1', '$sep = "\\"')                                                      -> set()

`fixed_case_path_comparison` es el mas debil: su regex exige que la linea sea exactamente
`$Comparison = [...]::OrdinalIgnoreCase` o `$PathComparison = [...]`. **Esta atado al nombre de la
variable de produccion.** Renombrarla basta.

**Y aqui me mojo: no pido que amplieis la lista.** Un reconocedor estatico no puede decidir
"dependiente del host" en general; ampliarlo a ocho grafias es la remediacion que estrecha el dano sin
cambiar la clase, y me hara volver con la novena. Lo que pido es que este residual **se declare por
escrito** y que se nombre donde vive de verdad el cierre de clase: en la **ejecucion** de los gemelos
sobre Linux, que hoy cubre 3 de los 7 puntos de entrada (residual R1, ya declarado en la ronda
anterior y sin cambios).

### N1 (no bloqueante) -- el "28" del mensaje de exito es un literal, no una medicion

Mutacion **del checker**, declarada como tal: borre una de las cuatro `forms` del propio guardian.
Resultado: **exit 0** y el mensaje sigue diciendo `28 all-coordinate production mutants` cuando solo
corrieron 21. Es la misma familia que el `HOST_DIMENSIONS` que acabais de retirar: un numero anunciado
que no se deriva de lo que se ejecuto. Se arregla con `len(sources) * len(forms)`.

### N2 (no bloqueante) -- la excepcion acotada caduca y el diagnostico enganna

C6 renombra el lector de produccion a `$target` (deja de contar como lector) y anade un segundo. El
gate sale exit 1, pero por `AssertionError: host mutant 2 escaped at scripts/scan_domain_neutrality.ps1`:
muere porque `BOUNDED_LINE_READERS` sigue admitiendo 1 y el mutante inyectado ya no supera el umbral.
Falla cerrado -- bien -- pero el mensaje culpa a un mutante escapado cuando la causa es una excepcion
caducada. Un fallo que nombra mal su causa cuesta una ronda de diagnostico.

## Tabla AC por AC

| AC | Veredicto | Evidencia |
|---|---|---|
| AC1 falsacion previa e inventario | **PASS** (firmado en r1, no re-medido por instruccion) | -- |
| AC2 formas neutrales o declaradas | **PASS con reserva** | Las declaraciones siguen en prosa; ver H2 (dos de ellas son falsas hoy) |
| AC3 los gemelos se EJERCITAN en Linux | **PASS con residual R1** (firmado en r1, no re-medido) | Job `powershell-linux-parity`, 3 de los 7 puntos |
| **AC4 contrato por mutacion** | **FAIL** | 9 escapes de 17 sobre produccion, verdes contra los 5 gates declarados. H1 + H2 + H3 |
| AC5 paridad de VEREDICTO | **PASS** (firmado en r1, no re-medido) | -- |
| AC6 cerrado en CI REAL | **PASS** (firmado en r1, no re-medido por instruccion expresa) | run `31271924074`, job `powershell-linux-parity` success, head `50ce2301` |

## Residuales declarados

- **R1 (sin cambios):** el job de paridad ejercita 3 de los 7 puntos de entrada.
  `validate_collaboration_state.ps1`, `run_sdd_cases.ps1`, `run_compact_comms_cases.ps1` y
  `run_llm_turn_wrapper_cases.ps1` solo corren dentro de `validate`, detras de la cadena que aborta al
  primer rojo. El ultimo sigue sin evidencia de haber corrido en Linux.
- **R2 (sin cambios):** en este host **no hay `pwsh`**. No he ejecutado ningun `.ps1`. Todo lo que
  afirmo es sobre el contrato Python, que si se ejercita entero aqui.
- **R3 (limite honesto de mi propia bateria):** es plausible que el job de paridad de Linux matara
  B3/B4/B5 **por comportamiento** -- un prefijo de raiz con `\` rompe la salida del escaner en Linux y
  la comparacion con el gemelo Python fallaria. **No lo he podido medir** (R2). Lo declaro como no
  medido, no como defensa del contrato: el AC4 es el contrato por mutacion, y ese es el que falla.
- **R4 (sin cambios):** `Area_comun/protocol/FALSIFICATION_CONTRACTS.json`, listado en `scope_routes`,
  sigue sin existir; incoherencia de intake, no incumplimiento.

## Recomendacion de cierre

**CHANGE-REQUIRED.** Y lo digo reconociendo que esta remediacion es un salto grande, no un parche:
la poblacion ya se deriva, los 28 mutantes son el producto real sobre formas reales, el marcador
tautologico desaparecio, el eje en linea quedo cubierto y `HOST_DIMENSIONS` se retiro. Cuatro de mis
seis puntos estan cumplidos. Mis tres negativos minimos de la ronda anterior mueren.

Lo que impide cerrar hoy no es que la clase siga abierta -- eso es un residual honesto que se declara.
Es que **el entregable afirma por escrito dos propiedades que un mutante falsa** (H2), y que el
derivador que da nombre a la remediacion **no ve una forma trivial y realista de ejecutar PowerShell
en CI** (H1, C1). Cerrar con esas dos frases en pie firma una cobertura que no existe.

### Que tiene que cambiar (criterio, y acotado a proposito)

1. **La poblacion se deriva de la condicion evaluada, no del campo `shell:`.** Debe cubrir
   `pwsh`/`powershell` invocados como CLI desde cualquier shell, y todos los ficheros bajo
   `.github/workflows/`. **C1 y C4 son el negativo minimo que debe morir.** Alternativa aceptable:
   declarar por escrito esos dos ejes fuera de alcance con su razon, como ya hicisteis bien con otros.
2. **El lector de lineas se ata a la FORMA, no al nombre de la variable receptora.** `C2` debe morir,
   o la frase del fichero de tarea que promete que muere se retira.
3. **La alcanzabilidad se ata al efecto, incluida la llave en la misma linea.** `C3` y `C5` deben
   morir, o la frase "el primer `exit` top-level alcanzable" se retira y se sustituye por lo que el
   predicado si comprueba.
4. **El residual de grafia (H3) se DECLARA, no se amplia.** Escribid que el reconocedor cubre cuatro
   grafias conocidas por dimension, que una quinta grafia de la misma dimension escapa (B2/B4/B5/B6
   nombrados), y que el cierre de clase real es la ejecucion en Linux, hoy 3 de 7 (R1). **Si la
   respuesta es anadir cuatro literales mas al escaner, vuelvo a fallar.**
5. **N1:** el numero del mensaje de exito se calcula (`len(sources) * len(forms)`), no se escribe.
6. **N2:** el fallo de la excepcion acotada debe nombrar su causa real.

### Bucle de arreglo

- **Remediacion:** los seis puntos de arriba, sin absorber TASK-0338 ni TASK-0336.
- **Gates afectados:** `python examples/neutrality_scan_cases/run_powershell_host_cases.py`,
  `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml`,
  y los cuatro pasos del job `powershell-linux-parity`.
- **Re-juicio:** yo, en clon limpio, **antes** del commit de cierre. Repetire A1-A5, B1-B6 y C1-C6 mas
  mutantes nuevos que el maker no habra visto.
- **Escalado:** **esta es la iteracion 2 de 2.** Si tras ella C1, C2, C3 o C5 siguen vivos y las dos
  frases falsas siguen en el fichero de tarea, **escalo al operador humano en lugar de abrir una r3**.

-- Analista
