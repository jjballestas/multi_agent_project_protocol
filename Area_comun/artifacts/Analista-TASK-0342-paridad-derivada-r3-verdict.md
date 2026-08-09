# Veredicto Analista -- TASK-0342 (r3): la derivacion es real, pero deriva de una VENTANA DE TEXTO

Autor: Analista (voz adversarial independiente)
Fecha: 2026-08-09 08:53 hora local (UTC+2)
Veredicto: **CHANGE-REQUIRED + ESCALADO AL OPERADOR** (iteracion 2 de 2 consumida)

## Ancla canonica

- Commit bajo revision: `3e6012a6742584921660e74064534f02b394c617` ("fix(TASK-0342): derive scanner
  parity from policy"), ancestro de `origin/main` (`397d3be3`).
- Alcance declarado por la instruccion: **solo el hub, sin producto en alcance**. Respetado.
- Estado canonico al arrancar: `python scripts/validate_collaboration_state.py` exit **0**.
- Clon limpio POSIX: `~/Aegis_Scratch/multi_agent_project_protocol/an0342r3/cc` (WSL2 Ubuntu, ext4,
  **sensible a mayusculas**), checkout de `3e6012a6`, working tree limpio. Todo medido ahi, nunca en
  el arbol caliente.
- PowerShell de medicion: **7.4.6** sobre `Linux 6.6.87.2-microsoft-standard-WSL2 x86_64`. Es la
  plataforma donde vive el defecto y donde CI ejecuta el paso.
- Codigo revisado == codigo de HEAD: `git diff 3e6012a6 397d3be3 -- scripts/ examples/
  Area_comun/protocol/FALSIFICATION_CONTRACTS.json .github/` es **vacio**.

## Metodo

El mismo de r2 y por la misma razon: se planta un centinela detectable y **el conjunto de rutas
reportadas ES el conjunto escaneado**; el complemento es el excluido. Las mutaciones se aplican a
**PRODUCCION** (`scripts/scan_encoding.ps1`, `scripts/scan_encoding.py`), no a los mutantes que el
propio runner se fabrica, cada una en un arbol nuevo, gateada por **exit code** de
`examples/encoding_gate_cases/run_encoding_gate_cases.py`.

Dos centinelas distintos, y la distincion decide un hallazgo:

- `# Espa` + U+00C3 + U+00B1 + `a` -- dispara **los dos** canales (ASCII y firma de mojibake).
- `# se` + U+00F1 + `al` (UTF-8 legitimo, bytes 0xC3 0xB1) -- dispara **solo** el canal ASCII.

## Tabla vector por vector

| # | Vector pedido | Resultado | Evidencia |
|---|---------------|-----------|-----------|
| A | Sexto directorio en `$SkipDirs`, atado **sin editar el fixture** | **PASS** en la forma declarada | A1 exit 0 sin tocar el fixture; A3 (declarado en los dos, PS no lo aplica) exit **1** en `python_scanned == powershell_scanned == expected_scanned` |
| A' | Sexto directorio escrito de **otra forma** | **SLIP** | A4 y A7: divergencia VIVA, negativo exit **0**. A5 y A8: sin divergencia, negativo exit **1** (rojo falso) |
| B | `-ccontains` revertido mata el negativo | **PASS** | B1 exit **1**, y por la asercion correcta (conjuntos medidos, no anclas de texto) |
| C | Nombre que es entero un sufijo + regla del punto inicial | **PASS** | `.png`/`.zip`/`.pyc` escaneados por los DOS; `..png` y `real.PNG` excluidos por los dos; C1/C3/C4 mueren |
| D | Sin excluir de mas (las dos direcciones) | **PASS** | Arbol real 5.404 ficheros: `GAINED=0` y `LOST=0` en los dos motores; excluidos identicos |
| E | R5 declarado o resuelto + AC5 con run REAL | **PASS** | Sonda de FS verificada por comportamiento; run `31296929292`, pasos 14/15/16 `success` |
| AC4 | Negativo que muere si dejan de coincidir en el conjunto excluido | **SLIP** | G3 (tres formas) y G4 (enumeracion oculta): divergencia real, negativo verde |

## Lo que r2 bloqueo y ahora CIERRA

### Foco B -- CERRADO. El caracter que faltaba

`$SkipDirs -ccontains $part` -> `-contains $part`, aplicado a produccion:

    B1_ccontains_reverted    exit=1  DIES
      run_encoding_gate_cases.py:207 assert python_scanned == powershell_scanned == expected_scanned

Muere, y muere **midiendo conjuntos**, no reventando un ancla de texto. En r2 esta mutacion
sobrevivia (G2). Es la linea que la propia remediacion habia escrito y ahora esta atada.

### Foco A -- CERRADO en la forma declarada, y de verdad derivado

Anado `dist` como sexto directorio, **sin tocar el fixture**:

    A1_sixth_dir_both        exit=0  (declarado en los DOS gemelos: el contrato sigue verde)
    A2_sixth_dir_ps_only     exit=1  (declarado solo en PS: muere)
    A3_sixth_dir_both_ps_behavior_ignores_it  exit=1  DIES
      run_encoding_gate_cases.py:207 assert python_scanned == powershell_scanned == expected_scanned

A3 es la prueba que pediste y es la que cuenta: los dos gemelos **declaran** `dist`, pero PowerShell
solo aplica los cinco primeros. La divergencia esta unicamente en la coordenada NUEVA, que nadie
escribio en el fixture -- y el negativo la mata por conjunto medido. **El universo se deriva, no se
enumera.** Eso es un avance real sobre r2 y hay que decirlo con esa proporcion.

### Foco C -- CERRADO. El nombre que es entero un sufijo

Produccion sin mutar, los dos gemelos sobre el mismo arbol:

    Area_comun/tasks/.png          py_reported=True   ps_reported=True
    Area_comun/tasks/.zip          py_reported=True   ps_reported=True
    Area_comun/tasks/.pyc          py_reported=True   ps_reported=True
    Area_comun/tasks/.md           py_reported=True   ps_reported=True
    Area_comun/tasks/.gitignore    py_reported=True   ps_reported=True
    Area_comun/tasks/..png         py_reported=False  ps_reported=False
    Area_comun/tasks/real.PNG      py_reported=False  ps_reported=False
    Area_comun/tasks/a.tar.zip     py_reported=False  ps_reported=False
    Area_comun/tasks/x.            py_reported=True   ps_reported=True
    DIVERGENTES: ninguna

La regla queda **declarada** en el handoff y en el codigo de los dos gemelos: el punto final abre
sufijo solo si le precede al menos un caracter del nombre, y el sufijo se normaliza a minusculas.
Consecuencia explicita, que es lo que preguntabas: **un nombre que empieza por punto y cuyo nombre
entero es un sufijo NO tiene sufijo y lo escanean los dos.** `..png` si tiene sufijo `.png` (hay un
caracter antes del punto final) y lo excluyen los dos. Coherente en las dos direcciones.

Y esta atado: `C1_ps_reverts_to_Extension` exit 1, `C3_ps_dot_boundary_off_by_one` (`-le 0` ->
`-lt 0`) exit 1, `C4_py_dot_boundary_off_by_one` (`dot > 0` -> `dot >= 0`) exit 1.

### Foco D -- CERRADO, las dos direcciones, sobre el arbol real

Arbol `3e6012a6` completo, centinela en los 5.404 ficheros, mismos datos para los cuatro escaneres:

    UNIVERSE=5404
    [before eb47942a] ONLY_PY=0  ONLY_PS=0
    [after  3e6012a6] ONLY_PY=0  ONLY_PS=0
    py: before=3885 after=3885  GAINED=0  LOST=0
    ps: before=3885 after=3885  GAINED=0  LOST=0
    EXCLUIDO despues: py == ps  (1519 rutas, identicas)

`LOST=0` es la mitad que importaba: el arreglo no dejo de mirar nada que ya miraba.

### Foco E -- R5 RESUELTO, verificado por comportamiento

La sonda `has_case_sensitive_filesystem` no la creo: la ejecuto en los tres sistemas de ficheros.

    NTFS  D:/Aegis_Scratch/...        case_sensitive=False   -> UNMEASURED, sin rojo falso
    DrvFs /mnt/d/... (WSL sobre NTFS) case_sensitive=False   -> UNMEASURED, sin rojo falso
    ext4  /home/johnb                 case_sensitive=True    -> mide

El rojo falso que r2 dejo latente esta resuelto. Y en CI **si midio**: el log del paso 16 del run
`31296929292` imprime `OK: encoding gate cases passed ...` y **no** contiene `UNMEASURED`.

### AC5 -- CI real

Run **31296929292**, `head_sha 030dd6ee`, con `git diff 3e6012a6 030dd6ee -- scripts/ examples/
Area_comun/protocol/FALSIFICATION_CONTRACTS.json .github/` **vacio** (codigo revisado identico):

    JOB powershell-linux-parity  [success]   <- entero verde
      [5] success Scan encoding with PowerShell on Linux
      [8] success Run PowerShell host-assumption contracts
    JOB validate [failure]
      [14] success Scan encoding
      [15] success Scan encoding with PowerShell     <- la evidencia del AC5
      [16] success Run encoding gate cases
      [32] failure Run runtime concurrency simulation cases   <- familia ajena, 16 pasos DESPUES

AC5 pide el PASO, no el job. Los tres salieron `success`.

## G3 -- SLIP (AC4): la derivacion deriva de una VENTANA DE TEXTO, no de la politica

No es un mutante rebuscado. Es como se escribe PowerShell.

El contrato lee la politica de los dos gemelos con **dos primitivas de rango distinto**:

    Python      import scan_encoding; set(python_scan.SKIP_DIRS)   <- el VALOR EFECTIVO
    PowerShell  re.search(rf"^\${var}\s*=\s*@\(([^\r\n]*)\)$", ...)  <- UNA LINEA, formato fijo

Todo lo que el lado PowerShell derive vale exactamente lo que valga esa expresion regular. Tres
formas la rompen, y rompen en las dos direcciones:

**G3.a -- `+=` en su propia linea: PASA EN VERDE con divergencia viva.**

    produccion mutada:  $SkipDirs += "dist"        (Python no lo declara)
    comportamiento:     runtime/dist/a.txt   py_reported=True   ps_reported=False   <-- DIVERGENTE
                        runtime/keep.txt     py_reported=True   ps_reported=True
    negativo permanente: exit=0  SOBREVIVE

**G3.b -- segunda asignacion mas abajo: PASA EN VERDE con divergencia viva.**

    produccion mutada:  un segundo $SkipDirs = @(..., "dist") mas adelante en el fichero
                        (PowerShell honra la ULTIMA; re.search lee la PRIMERA)
    comportamiento:     runtime/dist/a.txt   py_reported=True   ps_reported=False   <-- DIVERGENTE
    negativo permanente: exit=0  SOBREVIVE

**G3.c -- el espejo: cambios SIN efecto que ponen el gate ROJO.**

    A5  array multilinea (los dos gemelos de acuerdo)
        -> exit=1  AssertionError: PowerShell declaration not found: $SkipDirs
    A8  un comentario al final de la linea de declaracion, cero cambio de comportamiento
        -> exit=1  AssertionError: PowerShell declaration not found: $SkipDirs
        comprobado: runtime/dist/a.txt py=True ps=True ; runtime/node_modules/n.txt py=False ps=False
    A6  coordenada legitima sin caracter con caja ('.123'), declarada en los DOS
        -> exit=1  AssertionError: coordinate has no case-bearing character: .123

Un comentario al final de una linea tumba el gate; un `+=` en la linea siguiente lo ciega. **La
propiedad no sobrevive a cambio de formato**, y esa era la mitad del criterio que anuncie en r2:
coordenada, orden **y formato**.

Respuesta literal a tu pregunta: **el contrato ata un directorio nuevo si y solo si alguien lo
escribe en la unica forma que la regex reconoce.** No es la foto del arbol de hoy -- eso si mejoro --
pero sigue siendo la foto de **la forma de escribir de hoy**. La politica no es el texto de una
linea; es el valor que el escaner usa.

Falsable en dos comandos: anadir `$SkipDirs += "dist"` a `scripts/scan_encoding.ps1`, crear
`runtime/dist/a.txt` con un byte >127, correr los dos escaneres (Python lo reporta, PowerShell no) y
correr el negativo (exit 0).

## G4 -- SLIP (AC4): una de las tres enumeraciones ocultas no esta atada

El negativo declara cubrir "hidden entries". Su propio mutante hace
`ps_text.replace(" -File -Force", " -File")` **sin `count`**: quita las TRES a la vez. Produccion
tiene tres sitios de enumeracion y **quitar uno solo sobrevive**:

    X2_ps_hidden_force_removed   (solo Scan-AsciiPath, linea 69)   exit=0  SOBREVIVE
    X2b_force_mojibake_only      (solo Scan-MojibakeRoot, linea 103) exit=1  DIES

La divergencia de X2 es real, y solo se ve con el centinela correcto:

    centinela UTF-8 legitimo (0xC3 0xB1), canal ASCII unicamente:
      Area_comun/mailbox/open/.hidden.md   py_reported=True   ps_reported=False   <-- DIVERGENTE
      Area_comun/mailbox/open/visible.md   py_reported=True   ps_reported=True

    control, centinela de mojibake (el que usa el fixture del contrato):
      Area_comun/mailbox/open/.hidden.md   py_reported=True   ps_reported=True
      DIVERGENTES: ninguna

Ahi esta la causa, y es la misma clase de la tarea con otro disfraz: el fixture del contrato usa un
centinela que dispara **los dos canales**, y `Area_comun` esta tambien bajo la raiz de mojibake,
cuya enumeracion conserva `-Force`. El canal que si perdio los ocultos queda **enmascarado por el
otro**. Un fichero oculto del buzon con una enye legitima deja de verlo PowerShell y el contrato no
se entera.

## Mutantes de PRODUCCION -- resumen (18 vectores)

    A1  sexto directorio en los DOS gemelos                    exit=0  correcto (sin editar fixture)
    A2  sexto directorio solo en PS                            exit=1  MUERE
    A3  declarado en los dos, PS aplica solo cinco             exit=1  MUERE  <- derivacion real
    A4  $SkipDirs += "dist" en su propia linea                 exit=0  SOBREVIVE  <- G3.a
    A5  array multilinea, los dos de acuerdo                   exit=1  ROJO FALSO <- G3.c
    A6  coordenada sin caracter con caja ('.123'), los dos     exit=1  ROJO FALSO <- G3.c
    A7  segunda asignacion de $SkipDirs mas abajo              exit=0  SOBREVIVE  <- G3.b
    A8  comentario al final de la linea, cero efecto           exit=1  ROJO FALSO <- G3.c
    B1  $SkipDirs -ccontains -> -contains                      exit=1  MUERE  <- cierra G2 de r2
    B2  $SkipSuffixes -ccontains -> -contains                  exit=0  EQUIVALENTE (ver residuales)
    C1  PS vuelve a $File.Extension                            exit=1  MUERE
    C2  Python vuelve a path.suffix.lower()                    exit=0  EQUIVALENTE (ver residuales)
    C3  PS: $dot -le 0 -> -lt 0                                exit=1  MUERE
    C4  Python: dot > 0 -> dot >= 0                            exit=1  MUERE
    X1  vuelta a la barra invertida literal                    exit=1  MUERE
    X2  -Force fuera SOLO de Scan-AsciiPath                    exit=0  SOBREVIVE  <- G4
    X2b -Force fuera SOLO de Scan-MojibakeRoot                 exit=1  MUERE
    X3  Ordinal -> OrdinalIgnoreCase                           exit=1  MUERE
    X4  segundo $SkipAbsoluteDirs solo en PS                   exit=1  muere, pero por ANCLA de texto
    X5  segundo SKIP_RELATIVE_DIRS solo en Python              exit=1  MUERE (conjunto medido)
    X6  sufijo extra '.md' solo en PS                          exit=1  MUERE
    X7  $SkipSuffixes += ".md" en su propia linea              exit=1  muere, por casualidad del fixture
    X7b $SkipSuffixes += ".txt" en su propia linea             exit=1  MUERE

Dos matices que declaro para que nadie los lea de mas:

- **X4 muere por el motivo equivocado**: `assert mutant_text != ps_text` (linea 231) -- se rompe el
  ancla de texto del mutante que el propio runner se fabrica, no se mide divergencia. Falla en
  seguro, pero no es deteccion.
- **X7 muere por casualidad** (el fixture del caso `ps1 non_ascii_mailbox` usa `MSG-clean.md`), no
  por la propiedad de paridad. X7b, con `.txt`, si muere por conjunto medido porque
  `runtime/.cache/note.txt` esta en el universo. Es el mismo patron que G3: cuando la coordenada
  cae fuera del universo derivado, el escape es silencioso.

## Residuales declarados

- **R5b (nuevo):** el negativo puede **auto-desactivarse en verde**. En un sistema de ficheros
  insensible imprime `UNMEASURED` y sale **0**, y no hay ninguna asercion, en ningun sitio, de que
  la paridad se midiera al menos una vez. Hoy CI si mide (verificado en el log del run
  `31296929292`: no aparece `UNMEASURED`), pero eso no esta gateado: si manana el runner de CI
  monta un FS insensible, el gate sigue verde sin medir nada.
- **R7 (nuevo):** `case_variant` lanza `AssertionError` ante una coordenada declarada sin caracter
  con caja (medido con `.123`). Anadir a la politica un directorio o sufijo puramente numerico pone
  el gate rojo aunque los dos gemelos esten de acuerdo. Falla en seguro; conviene que quede escrito.
- **B2 y C2 son mutantes EQUIVALENTES, verificados por comportamiento, no supuestos.**
  B2: `Get-SharedSuffix` ya normaliza a minusculas y todos los sufijos declarados son minusculas
  (`a.PNG`, `b.png`, `c.PnG` excluidos por los dos, divergentes: ninguna). C2: `path.suffix.lower()`
  y `shared_suffix` solo difieren en un nombre terminado en punto, y ningun valor cae en
  `SKIP_SUFFIXES` (`x.` escaneado por los dos). Nota derivada: el helper `shared_suffix` de Python es
  un refactor sin efecto; el cambio semantico real fue el del lado PowerShell.
- **R6 (de r2, sin tocar):** dos aserciones de mutante siguen guardadas por `if os.name != "nt"`.
- **R1 (de r1, sin tocar):** `powershell.exe` 5.1 no tiene `GetRelativePath`; lanza `MethodNotFound`
  y AUN ASI imprime "OK: encoding scan is clean." y sale 0. Verde falso en Windows sin pwsh 7.
- **R3 (de r1, sin tocar):** paridad con pwsh 7 SOBRE Windows sigue sin medir en este host
  (`shutil.which("pwsh")` da `None`).

## Reproduccion con exit codes -- clon limpio POSIX sobre `3e6012a6`

    python3 scripts/scan_encoding.py --root .                       -> 0   OK: encoding scan is clean.
    python3 scripts/validate_collaboration_state.py --root .        -> 0   OK: collaboration state is valid.
    python3 scripts/check_falsification_contracts.py --root .       -> 0
    python3 scripts/check_falsification_contracts.py --inventory    -> 0
    python3 scripts/scan_domain_neutrality.py --root .              -> 0
    python3 runtime/protocol_replay.py --check-drift --root .       -> 0   verdict=CLEAN up_to_seq=8302
    python3 examples/encoding_gate_cases/run_encoding_gate_cases.py -> 0   (POSIX, pwsh 7.4.6, 7,9 s)

Los gates del repo estan verdes. El AC6 se cumple. Lo que no se cumple es el AC4.

## Recomendacion de cierre

**CHANGE-REQUIRED, y con la iteracion 2 de 2 consumida: ESCALO AL OPERADOR HUMANO**, tal como
autorizaste en la instruccion.

Quiero que se lea con la proporcion correcta. **Los dos SLIPS de r2 estan cerrados**: `-ccontains`
mata el negativo, el nombre que es entero un sufijo ya no divide a los gemelos, y --lo que mas
pesa-- **el universo se deriva de verdad**: A3 demuestra que una coordenada que nadie escribio en el
fixture queda atada por construccion. r2 medi que coincidian; r3 construye. Eso es el avance que
pedias y esta.

Lo que queda es exactamente un peldano mas arriba de donde estabamos, y es el que impide firmar:
**la construccion deriva de una linea de texto con un formato que nada obliga a mantener.** Dos
formas normales de escribir la misma politica en PowerShell (`+=`, segunda asignacion) producen
divergencia VIVA con el negativo en verde, y tres formas inocuas (multilinea, comentario al final,
coordenada sin caja) lo ponen rojo sin que nada haya cambiado. Un contrato que se rompe con un
comentario no esta atando la politica: esta atando un renglon.

Y G4 es la misma enfermedad en el otro eje: el fixture usa un centinela que dispara los dos canales,
asi que la perdida de enumeracion oculta en uno queda tapada por el otro.

### Direccion del arreglo (no la forma; la forma la elige quien implemente)

El contrato debe leer el **valor efectivo** de la politica de PowerShell, igual que ya lee el de
Python por `import`. Dos caminos que sobreviven a formato:

1. Que `scan_encoding.ps1` exponga su politica en tiempo de ejecucion (p. ej. un `-DumpPolicy` que
   imprima `$SkipDirs`, `$SkipSuffixes` y `$SkipAbsoluteDirs` ya resueltos) y que el contrato lea
   **esa salida**. Lo que se compara pasa a ser lo que el escaner usa de verdad.
2. O parsear con el **AST de PowerShell**
   (`[System.Management.Automation.Language.Parser]::ParseFile`), no con una expresion regular de
   linea.

El criterio con el que lo juzgare, y lo digo por adelantado para que no haya sorpresa: que la
propiedad sobreviva a **cambio de coordenada, de orden y de FORMATO** -- que A4, A7, A5, A8 y A6
salgan todos por el lado correcto sin editar el fixture. Y para G4, que el fixture separe los canales
(un centinela que dispare **solo** el canal ASCII) para que cada sitio de enumeracion quede atado por
si mismo, no por la suma.

### Bucle de arreglo

- **Remediacion 3 -> re-juicio del Analista antes del commit de cierre.**
- **Iteraciones agotadas (2 de 2).** No propongo otra vuelta ciega: **decision del operador humano**
  sobre si se abre una tarea nueva para G3/G4 y se cierra 0342 con los residuales declarados, o si
  se sigue en 0342 con una tercera vuelta autorizada por el.
- **Gates afectados si se sigue:** `Scan encoding`, `Scan encoding with PowerShell`,
  `Run encoding gate cases`, `powershell-linux-parity`, `check_falsification_contracts --inventory`,
  y un **run REAL de Actions** -- el AC5 aplica igual a la remediacion.

-- Analista
