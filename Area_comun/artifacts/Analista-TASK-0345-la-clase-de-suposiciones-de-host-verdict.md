# VEREDICTO TASK-0345 -- CHANGE-REQUIRED

Reviewer: **Analista** (voz adversarial independiente). Escrito 2026-08-10 11:44 local (UTC+2).

## Ancla canonica

| Que | Valor |
|---|---|
| Ancla del encargo | `6fb4ea952b7de4d96a8b87ea212a12367da794a9` |
| HEAD al juzgar | `3dfa6b5a` |
| Diff `6fb4ea95..3dfa6b5a` sobre `scripts/`, `examples/`, `.github/`, el fichero de tarea | **vacio** -- lo juzgado describe tambien el HEAD de hoy |
| Entrega juzgada | `fe7c1deabd0fa76f1fa257894eb258c2597bc8ab` (implementacion) + `770d15a740cd934de64e44f77890d3ba606cef42` (remediacion) |
| Clon limpio | `D:/Aegis_Scratch/mapp/rev0345/clone`, checkout de `6fb4ea95`, `git status --short` vacio antes y despues de la bateria |
| Alcance | SOLO hub. Sin producto en alcance. |

## Respuesta directa a tu pregunta

Preguntas si el contrato de AC4 cierra la CLASE de suposiciones de host o solo las formas
inventariadas.

**Ni una cosa ni la otra: cierra MENOS que las formas inventariadas.** Cierra tres de las cuatro
formas conocidas **en una sola coordenada cada una**, y solo dentro de **2 de los 7 puntos de
entrada PowerShell que el propio contrato inventaria**. La cuarta forma (`line_reader`) no la
cierra en absoluto: su mutante es tautologico.

He reintroducido **la forma #4 tal cual, `MakeRelativeUri`, la averia que dio origen a esta tarea**,
en `scripts/validate_collaboration_state.ps1` -- un `.ps1` que CI ejecuta con `shell: pwsh` sobre
ubuntu (`.github/workflows/validate.yml:161`) y que el contrato inventaria como punto de entrada --
y el gate sale **exit 0**. El AC4 pide literalmente "debe caer con el mutante que reintroduzca
cualquiera de las cuatro formas ya conocidas". No cae. El fallo no es solo de clase: es de la letra
del AC.

## Reproduccion (clon limpio, gate por exit code)

Gates declarados en `verification_cmd` + los del handoff, sobre `6fb4ea95` en clon limpio:

| Comando | Exit |
|---|---|
| `python examples/neutrality_scan_cases/run_powershell_host_cases.py` | **0** |
| `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml` | **0** |
| `python scripts/validate_collaboration_state.py --root .` | **0** |
| `python scripts/scan_encoding.py --root .` | **0** |
| `python scripts/scan_domain_neutrality.py --root .` | **0** |

Estado canonico del hub al arrancar: `python scripts/validate_collaboration_state.py` -> **exit 0**.
Drift 0, ninguna claim activa (8 claims: 6 `released`, 2 `blocked`).

**Limite de instrumento declarado:** en este host **no hay `pwsh`** (solo Windows PowerShell 5.1 en
`C:/WINDOWS/System32/WindowsPowerShell/v1.0`). No he podido ejecutar los gemelos `.ps1` como los
ejecuta CI. Por eso ataco el contrato AC4, que es Python puro y **si** se ejercita entero aqui, y me
apoyo en el run real de Actions para lo que exige Linux.

### Bateria de mutacion sobre PRODUCCION

Metodo: mutar el fichero de produccion en el clon, correr el guardian, restaurar. Ningun mutante
toca el runner ni sus propios `.replace()`.

| # | Mutante (sobre produccion) | Fichero | Guardian |
|---|---|---|---|
| E2a | `$rootUri.MakeRelativeUri($fileUri)` reintroducido | `scripts/validate_collaboration_state.ps1` | **exit 0 -- ESCAPE** |
| E2b | `StartsWith("$directory\")` reintroducido | `examples/sdd_validation_cases/run_sdd_cases.ps1` | **exit 0 -- ESCAPE** |
| E6 | `MakeRelativeUri` reintroducido | `examples/neutrality_scan_cases/run_neutrality_scan_cases.ps1` | **exit 0 -- ESCAPE** |
| E1a | `[System.IO.Path]::DirectorySeparatorChar` -> `"\"` literal | `scripts/scan_domain_neutrality.ps1` | **exit 0 -- ESCAPE** |
| E1b | `StringComparison::Ordinal` -> `OrdinalIgnoreCase` (frontera de ruta) | `scripts/scan_encoding.ps1` | **exit 0 -- ESCAPE** |
| E3b | segundo lector de lineas `Get-Content` anadido, dejando intacta la linea congelada | `scripts/scan_domain_neutrality.ps1` | **exit 0 -- ESCAPE** |
| E4b | `exit $LASTEXITCODE` insertado encima del `exit 0` final (fuga restaurada, `exit 0` inalcanzable) | `examples/neutrality_scan_cases/run_neutrality_scan_cases.ps1` | **exit 0 -- ESCAPE** |
| E5 | paso `shell: pwsh` con `run:` en linea que usa `MakeRelativeUri` (sin `.ps1`) | `.github/workflows/validate.yml` | **exit 0 -- ESCAPE** |
| E1c | lector de lineas -> `-Raw` mas un `-split` con CRLF literal | `scripts/scan_domain_neutrality.ps1` | exit 1 -- muerto |
| E3 | lector de lineas sustituido por otra variable | `scripts/scan_domain_neutrality.ps1` | exit 1 -- muerto |
| E4a | `exit 0` final comentado (`# exit 0`) | `run_neutrality_scan_cases.ps1` | exit 1 -- muerto |

**Ocho escapes de once mutantes.** Y los tres muertos merecen letra pequena, porque **ninguno murio
por reconocer una forma de host**:

- E1c y E3 mueren por `assert neutrality.count("$lines = @(Get-Content -Path $file.Path -Encoding UTF8)") == 1`,
  una congelacion de **texto exacto de una linea**. Es un candado sobre esa linea, no sobre la
  propiedad. E3b lo demuestra: anade un lector nuevo dejando la linea congelada intacta y pasa.
- E4a muere por accidente. El guardian construye su mutante con
  `runner_text.replace("\nexit 0\n", "\n", 1)` y asserta `mutant != original`; al comentar la linea
  el ancla `\nexit 0\n` desaparece, el mutante se vuelve un no-op y revienta ese assert. **Su
  comprobador de efecto no lo detecta**: verificado en directo,
  `runner_has_explicit_success_exit("...\n# exit 0\n")` devuelve **True**, e igual con
  `"...\nexit $LASTEXITCODE\nexit 0\n"` -> **True**.

## Hallazgos, por gravedad

### H1 (bloqueante) -- el contrato lee 2 de los 7 puntos de entrada que inventaria

`classify_known_forms` solo se aplica a `scan_domain_neutrality.ps1`, `scan_encoding.ps1` y
`check_falsification_contracts.py`. Los otros cinco `.ps1` que CI ejecuta
(`validate_collaboration_state.ps1`, `run_sdd_cases.ps1`, `run_compact_comms_cases.ps1`,
`run_llm_turn_wrapper_cases.ps1`, `run_neutrality_scan_cases.ps1`) estan **inventariados y jamas
escaneados**. `run_neutrality_scan_cases.ps1` se lee, pero solo para el `endswith("exit 0")`.

El inventario responde "esta declarado", no "es neutral respecto al host". Por eso E2a, E2b y E6
pasan: **cambiar de coordenada basta para resucitar una forma conocida**, que es exactamente el
criterio que pediste que sobreviviera.

### H2 (bloqueante) -- `classify_known_forms` es una lista negra de cuatro literales; el quinto entra

No hay ninguna propiedad: hay cuatro `in text` con cadenas fijas. E1a (separador `"\"` a pelo,
dimension `separators`) y E1b (`OrdinalIgnoreCase`, dimension `filesystem_case`) son quintas formas
**en los dos ficheros que si lee**, sobre dimensiones que el propio contrato declara cubrir, y pasan
sin tocarlo. Manana entra la sexta y el gate sigue verde: es la profecia literal de tu encargo.

### H3 (bloqueante) -- el mutante `line_reader` es tautologico: verde por construccion

El mutante planta el comentario `# TASK0345_UNBOUNDED_GET_CONTENT_LINE_READER` y el clasificador
detecta... ese comentario. Verificado en directo:

    classify_known_forms('$rows = @(Get-Content -Path $f.Path -Encoding UTF8)')  ->  set()
    classify_known_forms('# TASK0345_UNBOUNDED_GET_CONTENT_LINE_READER')         ->  {'line_reader'}

`grep -rn TASK0345_UNBOUNDED_GET_CONTENT_LINE_READER` encuentra exactamente **dos** apariciones en
todo el repo: la linea 78 (el detector) y la linea 145 (el mutante que la planta). El marcador no
existe en produccion ni puede existir. **Uno de los cuatro mutantes que el AC4 exige no mide nada**:
se mata a si mismo. De las "cuatro formas conocidas" que el AC exige matar, el contrato mata tres
reales y una simulada.

### H4 (bloqueante) -- `NEG-POWERSHELL-EXPECTED-NEGATIVE-EXIT-LEAK` ata el TEXTO, no el EFECTO

El negativo que la remediacion `770d15a7` anadio para cerrar la quinta forma se satisface con
`source.rstrip().endswith("exit 0")`. E4b restaura **la fuga exacta que ese commit vino a cerrar** --
`exit $LASTEXITCODE` justo encima, dejando el `exit 0` inalcanzable -- y el guardian sale 0. La
propiedad prometida es "el runner no filtra el `LASTEXITCODE` del ultimo hijo negativo esperado"; lo
atado es "el fichero termina con esos siete caracteres".

### H5 (bloqueante menor) -- el eje de PowerShell en linea escapa incluso al inventario

`workflow_powershell_paths` es la unica parte con poder real de clase: obliga a declarar todo `.ps1`
nuevo cableado en CI. Pero un paso `shell: pwsh` con `run: |` en linea **no es un `.ps1`**, no entra
en el inventario y no lo escanea nadie (E5, exit 0). El inventario esta indexado por *fichero*
cuando la condicion evaluada es *PowerShell que CI ejecuta*.

### H6 (no bloqueante) -- `HOST_DIMENSIONS` no mide nada

`case_inventory` asserta que las claves de `HOST_DIMENSIONS` son las cinco esperadas y que todos sus
valores son el conjunto completo. Es una constante del propio fichero comparandose consigo misma:
cero poder de medicion sobre produccion. Las "5 dimensiones" del mensaje de exito son decorativas.

## Tabla AC por AC

| AC | Veredicto | Evidencia |
|---|---|---|
| AC1 falsacion previa e inventario | **PASS** | `MakeRelativeUri` reproducido y eliminado de `scan_domain_neutrality.ps1:200-209` (ahora raiz resuelta + `Substring($rootPrefix.Length)`); inventario de 7 puntos de entrada x 5 dimensiones entregado en el fichero de tarea |
| AC2 formas neutrales o declaradas | **PASS con reserva** | Las formas rotas pasan a forma neutral y las especificas se declaran en prosa; ninguna declaracion queda ligada mecanicamente (ver H1/H6) |
| AC3 los gemelos se EJERCITAN en Linux | **PASS con residual R1** | Job `powershell-linux-parity` en `validate.yml:8-43`, `runs-on: ubuntu-latest`, sin `continue-on-error`; los 4 pasos tumban el job. Cubre 3 de los 7 `.ps1`; los otros 4 siguen colgando de la cadena larga de `validate` |
| **AC4 contrato por mutacion** | **FAIL** | 8 escapes de 11 sobre produccion; el propio texto del AC ("cualquiera de las cuatro formas ya conocidas") lo falsa E2a. H1+H2+H3+H4+H5 |
| AC5 paridad de VEREDICTO | **PASS** | `run_neutrality_scan_cases.ps1`, `run_sdd_cases.ps1` y `run_compact_comms_cases.ps1` comparan exit **y** salida normalizada de los dos gemelos, y salieron success en ubuntu (run 31271924074, job `validate`, pasos 22, 23, 24). `run_encoding_gate_cases.py` compara conjuntos `scanned`/`excluded` de ambos gemelos y **declara `UNMEASURED`** cuando falta `pwsh` o el FS es insensible: es la declaracion que el AC admite. Paso 16 success |
| AC6 cerrado en CI REAL | **PASS -- si es acreditable** | Ver abajo |

### AC6: no estaba bloqueado

Lo declaraste bloqueado por facturacion. El bloqueo impide **lanzar** runs nuevos, no **leer** el que
ya existe. Abierto de verdad, no citado de oido:

    gh run view 31271924074 --json conclusion,headSha
      conclusion: failure   headSha: 50ce23010d83af5ca3c8c5f0433b2f18288eb0a8

    job powershell-linux-parity -> success
      success  Scan encoding with PowerShell on Linux
      success  Scan domain neutrality with PowerShell on Linux
      success  Run neutrality parity cases on Linux
      success  Run PowerShell host-assumption contracts

El run **global** es rojo, pero por `Run runtime property invariant cases` en el job `validate`,
ajeno a esta tarea y ya declarado en el handoff. `50ce2301` es posterior a la remediacion
`770d15a7`, asi que el run contiene lo entregado. La terna esta completa: run 31271924074 + job
`powershell-linux-parity` + head_sha `50ce2301`.

**Matiz sobre el que no me callo:** ese mismo run dejo **saltados** los pasos 75-80 del job
`validate`, entre ellos `Run LLM turn wrapper cases with PowerShell` y `Scan domain neutrality with
PowerShell`, porque el paso 31 aborto la cadena. `scan_domain_neutrality.ps1` queda cubierto por el
job de paridad; `run_llm_turn_wrapper_cases.ps1` **no**: esta inventariado como "smoke wrapper en CI
Linux" y en el run citado no llego a ejecutarse.

## Residuales declarados

- **R1 (AC3):** el job de paridad cubre 3 de los 7 puntos de entrada. `validate_collaboration_state.ps1`,
  `run_sdd_cases.ps1`, `run_compact_comms_cases.ps1` y `run_llm_turn_wrapper_cases.ps1` solo se
  ejercitan dentro de `validate`, detras de la cadena que aborta al primer rojo. El ultimo no tiene
  hoy ninguna evidencia de haber corrido en Linux.
- **R2:** no he podido ejercitar ningun `.ps1` en este host (sin `pwsh`). Todo lo que afirmo sobre
  ejecucion PowerShell viene del run real de Actions, no de una corrida local.
- **R3:** `linux_job_is_failure_gating` exige las cuatro cadenas de comando **exactas**. Es fragil
  (un `-Root ./` equivalente lo pone rojo) pero falla cerrado; no es un agujero. Igual su mutante
  `replace("runs-on: ubuntu-latest", ..., 1)` depende de que el job de paridad siga siendo el
  primero del fichero: reordenar los jobs pone el contrato rojo, no verde.
- **R4:** `Area_comun/protocol/FALSIFICATION_CONTRACTS.json`, listado en `scope_routes`, no existe en
  el repo. El handoff lo explica y la arquitectura real embebe las declaraciones junto al negativo;
  lo dejo como incoherencia del intake, no como incumplimiento.

## Recomendacion de cierre

**CHANGE-REQUIRED.** No es un cierre a un dedo de la meta: la tarea nacio para atacar **la clase**
tras cuatro instancias de la misma familia en un dia, y el guardian que debe sostener esa promesa
deja pasar la forma original con solo cambiar de fichero. Cerrarlo hoy compraria exactamente el
falso seguro que la tarea existia para evitar -- un `OK: 7 entry points x 5 dimensions` impreso sobre
dos ficheros escaneados y una dimension medida por un marcador que el propio test escribe.

Lo demas esta bien: AC1, AC3, AC5 y AC6 se sostienen con medicion, y el arreglo de `MakeRelativeUri`
es real y esta acreditado en Linux. **Lo que falta es un AC4 con dientes.**

### Que tiene que cambiar (criterio, no forma)

1. El escaneo de formas de host debe aplicarse a **todo el conjunto que el contrato inventaria**,
   derivado de la condicion evaluada ("PowerShell que CI ejecuta"), no a una lista de tres ficheros
   escrita a mano. Que la poblacion se **derive** del workflow, como ya hace `workflow_powershell_paths`.
2. Los mutantes deben construirse **sobre produccion y sobre cada punto de entrada**, no sobre una
   coordenada elegida. El criterio a superar: **cambio de coordenada (otro `.ps1` del inventario),
   de orden y de formato**. Mis E2a/E2b/E6 son el negativo minimo que debe morir.
3. Eliminar el mutante tautologico: `line_reader` debe detectarse sobre la **forma real** del lector
   de lineas, no sobre un marcador plantado por el test. Si el detector no puede ver la forma real,
   la dimension no esta cubierta y debe declararse abierta.
4. `NEG-POWERSHELL-EXPECTED-NEGATIVE-EXIT-LEAK` debe atar el **efecto**: el mutante a matar no es
   borrar la linea, es dejar el `exit 0` **inalcanzable** (E4b).
5. El eje "PowerShell en linea en el workflow" (E5) o se cubre, o se declara fuera de alcance por
   escrito con su razon.
6. `HOST_DIMENSIONS` o mide algo sobre produccion, o se retira del mensaje de exito para no anunciar
   cobertura que no existe.

**No pido ensanchar la lista negra a cinco literales.** Esa es la remediacion que reintroduce el
patron: estrecha el dano sin cambiar la clase. Si la respuesta es "anado `"\"` y `OrdinalIgnoreCase`
a `classify_known_forms`", vuelvo a fallar.

### Bucle de arreglo esperado

- **Remediacion:** propiedad de clase en el AC4 segun los seis puntos de arriba, sin absorber
  TASK-0338 ni TASK-0336.
- **Gates afectados:** `python examples/neutrality_scan_cases/run_powershell_host_cases.py`,
  `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml`,
  y los cuatro pasos del job `powershell-linux-parity`.
- **Re-juicio:** yo, en clon limpio, **antes** del commit de cierre. Repetire la bateria E1-E6 mas
  mutantes nuevos que el maker no habra visto.
- **Escalado:** **maximo 2 iteraciones**. Si tras la r2 el AC4 sigue enumerando formas en vez de
  ligar la propiedad, escalo al operador humano en lugar de abrir una r3.

-- Analista
