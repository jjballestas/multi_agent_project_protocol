# Veredicto Analista -- TASK-0342 (r2): los tres SLIPS de r1 cierran; la clase deja dos socavones

Autor: Analista (voz adversarial independiente)
Fecha: 2026-08-09 03:45 hora local (UTC+2)
Veredicto: **CHANGE-REQUIRED**

## Ancla canonica

- Commit bajo revision: `eb47942a54cffff1b02838305d782bd9b991828a`, ancestro de `origin/main`
  (`a36de9f4`). La remediacion de codigo vive en `dc0bdf56` + `7691a87e`; `eb47942a` solo mueve
  ledger/handoff/mailbox.
- Estado canonico al arrancar: `python scripts/validate_collaboration_state.py` exit **0**.
- Clon limpio POSIX: `~/Aegis_Scratch/multi_agent_project_protocol/an0342r2` (WSL2 Ubuntu, ext4,
  **sensible a mayusculas**), checkout de `eb47942a`. Segundo clon `an0342r1` en `7bbc0253` para el
  antes/despues. Todo medido ahi, nunca en el arbol caliente.
- PowerShell de medicion: **7.4.6** sobre `Linux 6.6.87.2-microsoft-standard-WSL2 x86_64`, la
  plataforma donde vive el defecto y donde CI corre el paso.
- Codigo atestado por CI == codigo revisado: `git diff 677246a9 eb47942a -- scripts/
  examples/encoding_gate_cases/ Area_comun/protocol/FALSIFICATION_CONTRACTS.json .github/` es vacio.

## Metodo

Igual que en r1 y por la misma razon: para medir el conjunto EXCLUIDO sin creer ninguna declaracion
se planta un centinela detectable (`# Espa` + U+00C3 + U+00B1 + `a`, que dispara a la vez el canal
ASCII y la firma de mojibake) y el conjunto de rutas reportadas ES el conjunto escaneado.

Lo que anado en r2, y es lo que decide el veredicto: **las mutaciones se aplican a PRODUCCION**, no
a los mutantes que el propio runner se fabrica. Un contrato que mata a sus propios mutantes prueba
que sabe hacer `.replace()`; lo que hay que probar es que muere cuando el codigo que se despliega
cambia. Once mutaciones independientes sobre `scripts/scan_encoding.ps1` y `scripts/scan_encoding.py`,
cada una en un arbol nuevo, gateadas por exit code de
`examples/encoding_gate_cases/run_encoding_gate_cases.py`.

## Tabla vector por vector

| # | Vector | Resultado | Evidencia |
|---|--------|-----------|-----------|
| Foco A | Las diez rutas de r1, una a una | **PASS** | Sobre el arbol real, `ONLY_PY=0` y `ONLY_PS=0`. Las 9 versionadas las escanean ya los dos; la decima (`runtime/.cache/note.txt`) no existe en clon limpio (no versionada) y queda atada por el universo del negativo |
| Foco B | El negativo cae con los dos escaneres en 0 | **PASS** | Experimento dedicado abajo: verdictos identicos y verdes, conjuntos divergentes, contrato MUERTO |
| Foco C | Sin excluir de mas | **PASS** | `LOST=0` en las dos direcciones y en los dos escaneres; PS gana 9 rutas, no pierde ninguna |
| Foco D | Mayusculas cubiertas como propiedad, no como enumeracion | **PASS** | `Memory`, `MEMORY`, `MeMoRy` escaneadas por los dos; solo `memory` exacto excluido. La tercera variante ya esta cubierta porque se DERIVA de `Ordinal`, no se enumera |
| AC1 | Falsacion previa: la causa es el separador | **PASS (r1)** | Sin cambios |
| AC2 | La exclusion no liga un separador | **PASS** | Mutante de produccion P3 (vuelta a `\` literal) MUERE por comportamiento en POSIX |
| AC3 | Los dos escaneres excluyen EXACTAMENTE el mismo conjunto | **SLIP** | Ver G1: divergencia VIVA en produccion, no mutante |
| AC4 | Negativo que muere si dejan de coincidir en el conjunto excluido | **SLIP** | Ver G2: mutacion de un caracter en la linea que esta misma remediacion escribio, y el negativo sigue verde |
| AC5 | Paso en verde en un run REAL de Actions | **PASS** | Run `31286367935`, pasos 14/15/16 `success` + job nuevo `powershell-linux-parity` entero `success` |
| AC6 | Sin regresion, gates exit 0 en clon limpio | **PASS** | Seis gates exit 0 |

## Lo que r1 bloqueo y ahora CIERRA

### F1 (enumeracion oculta) -- CERRADO, medido sobre el arbol real

Mismo arbol para los dos juegos de escaneres, centinela en los 3.865 ficheros bajo las dos raices:

    scanners @ eb47942a : UNIVERSE=3865  PY_SCANNED=3862  PS_SCANNED=3862  ONLY_PY=0  ONLY_PS=0
    scanners @ 7bbc0253 : UNIVERSE=3865  PY_SCANNED=3862  PS_SCANNED=3853  ONLY_PY=9  ONLY_PS=0

Las nueve rutas versionadas que r1 listo -- las `.gitkeep` de `artifacts`, `contracts`, `decisions`,
`handoffs`, `mailbox/{answered,archived,open}`, `reports` y `tasks` -- las escanean hoy los dos.

### Foco C -- CERRADO: no se excluyo de mas, en las DOS direcciones

    py: before=3862 after=3862   GAINED=0   LOST=0
    ps: before=3853 after=3862   GAINED=9   LOST=0
    EXCLUIDO despues, py == ps == 3 ficheros .pyc bajo runtime/__pycache__

Medir solo `GAINED` habria dejado la mitad del riesgo sin mirar. `LOST=0` es la mitad que importaba.

### F2 (mayusculas) -- CERRADO, y por derivacion

    runtime/memory/a.txt   py_scanned=False  ps_scanned=False
    runtime/Memory/b.txt   py_scanned=True   ps_scanned=True
    runtime/MEMORY/c.txt   py_scanned=True   ps_scanned=True
    runtime/MeMoRy/d.txt   py_scanned=True   ps_scanned=True
    DIVERGENTES: ninguna

La pregunta del foco D era si `Memory` estaba tapada como caso o como clase. Es clase: `Ordinal`
decide sobre cualquier grafia, y la cuarta variante que no esta en el fixture sale bien igual. Aqui
el arreglo NO enumero.

### F3 (el negativo comparaba hallazgos) -- CERRADO. Respuesta directa al foco B

El caso exacto que en r1 pasaba desapercibido, reproducido con la mutacion aplicada a PRODUCCION
(exclusion solo-PowerShell de `Area_comun/tasks`) sobre un arbol ASCII limpio:

    python exit=0      stdout: OK: encoding scan is clean.
    powershell exit=0  stdout: OK: encoding scan is clean.        <- verdictos IDENTICOS y VERDES
    (con un centinela en Area_comun/tasks: python exit=1, powershell exit=0 -> la divergencia es real)

    PERMANENT NEGATIVE sobre esa misma produccion mutada: exit=1 -> MUERE
        run_encoding_gate_cases.py:152 assert python_scanned == powershell_scanned == expected_scanned

**Si: cae aunque los dos escaneres esten en 0 y digan lo mismo.** El centinela plantado rompe la
dependencia del contrato respecto a que el arbol tenga suciedad; ya no hereda la limpieza del arbol.
Ese era el punto y esta resuelto.

### Mutantes de PRODUCCION -- 10 de 11 mueren

    P1  revert -Force (omision de ocultos)                     exit=1 MUERE
    P2  revert Ordinal -> OrdinalIgnoreCase                    exit=1 MUERE
    P3  revert a la barra invertida literal                    exit=1 MUERE
    P4  exclusion extra solo-PS de Area_comun/tasks            exit=1 MUERE   <- el M3 que en r1 SOBREVIVIA
    P5  exclusion extra solo-PS de Area_comun/state            exit=1 MUERE
    P6  eliminar el paso de canal ASCII del mailbox            exit=1 MUERE
    P7  SkipDirs -ccontains -> -contains                       exit=0 SOBREVIVE  <- G2
    P8  skip-dir extra solo-PS 'reports'                       exit=1 MUERE
    P9  Python pierde la exclusion de runtime/memory           exit=1 MUERE
    P10 Python deja de ver entradas ocultas (espejo de P1)     exit=1 MUERE
    P11 skip-suffix extra solo-PS '.md'                        exit=1 MUERE

Esto es sustancialmente mejor que r1 y hay que decirlo: el negativo ya no mide hallazgos, mide
conjuntos, y aguanta mutacion en los dos gemelos y en las dos direcciones (excluir de mas y de menos).

## G1 -- SLIP (AC3): los gemelos NO excluyen el mismo conjunto; se rompe en el punto de fila (dotfiles)

No es un mutante. Es el codigo de `eb47942a`, medido:

    Area_comun/mailbox/open/.png       py_scanned=True   ps_scanned=False
    Area_comun/mailbox/open/.zip       py_scanned=True   ps_scanned=False
    Area_comun/mailbox/open/.pyc       py_scanned=True   ps_scanned=False
    Area_comun/mailbox/open/real.png   py_scanned=False  ps_scanned=False
    Area_comun/mailbox/open/keep.md    py_scanned=True   ps_scanned=True
    DIVERGENTES: ['.png', '.pyc', '.zip']

Causa, aislada: los dos gemelos siguen usando **dos primitivas de lenguaje distintas para "sufijo"**,
y discrepan justo en los ficheros que empiezan por punto.

    Python  Path(".png").suffix              -> ""        (rfind('.')==0 -> sin sufijo)
    .NET    FileInfo(".png").Extension       -> ".png"

Python lo escanea, PowerShell lo excluye por sufijo. Es la MISMA direccion de divergencia que r1
nombro en F1 (PS excluye lo que Python escanea), sobre el MISMO canal (`Area_comun/mailbox/**`, el
canal ASCII), sobrevivida por otro mecanismo. La remediacion cerro la instancia -- la enumeracion --
y no la clase.

Y no es una coincidencia desafortunada: `-Force` se anadio precisamente para que PowerShell VEA los
ficheros que empiezan por punto. Lo primero que PowerShell hace con un fichero que empieza por punto
cuyo nombre entero es un sufijo de la lista compartida es discrepar de Python. Se abrio la puerta y
el desacuerdo estaba justo detras.

El universo de 21 rutas del negativo contiene `runtime/skip.png` (sufijo normal) y ningun dotfile
con forma de sufijo, asi que el contrato no puede verlo. Falsable en un comando: crear
`Area_comun/mailbox/open/.png` con un byte >127 y correr los dos gates -- Python sale 1, PowerShell
sale 0.

## G2 -- SLIP (AC4): el negativo no ata `-ccontains`, que es una de las dos lineas que ESTA remediacion escribio

`dc0bdf56` cambio `-contains` por `-ccontains` en la comparacion de `$SkipDirs` para igualar la
semantica exacta de mayusculas de Python. Deshacer ese cambio -- **un caracter** -- produce
divergencia real del conjunto excluido:

    mutante P7 (-ccontains -> -contains):
        runtime/node_modules/a.txt   py_scanned=False  ps_scanned=False
        runtime/Node_Modules/b.txt   py_scanned=True   ps_scanned=False   <- divergente
        runtime/NODE_MODULES/c.txt   py_scanned=True   ps_scanned=False   <- divergente
        runtime/keep.txt             py_scanned=True   ps_scanned=True
        DIVERGENTES: ['runtime/NODE_MODULES/c.txt', 'runtime/Node_Modules/b.txt']

    permanent negative sobre ese mutante: exit=0 -> SOBREVIVE

El mutante NO es equivalente: cambia el conjunto excluido en dos rutas y el contrato lo deja pasar.
AC4 pide exactamente "que muera si los dos escaneres dejan de coincidir en el conjunto excluido", y
aqui dejan de coincidir sin que muera.

La razon es la misma que G1 y la misma que el arbol de 21 rutas: la sensibilidad a mayusculas esta
atada **solo en la frontera `runtime/memory`** (via `runtime/Memory/case.txt`), no en la lista de
directorios saltados ni en la de sufijos. La propiedad declarada en el handoff es "exact-case path
semantics" para las tres listas; el contrato solo ata una de las tres.

## Residuales declarados

- **R5 (nuevo, y el mas incomodo):** el fixture del negativo **no es satisfacible en un sistema de
  ficheros insensible a mayusculas**. Con `runtime/Memory/case.txt` y `runtime/memory/index.db` en
  NTFS colapsan al mismo directorio; medido en `D:/Aegis_Scratch/.../an0342win`, el listado real deja
  `Memory` y `memory` desaparece, e `index.db` cae dentro de `Memory/`. Encima, el hallazgo de ese
  SQLite tiene detalle U+FFFD y `scan_encoding.py` **revienta con `UnicodeEncodeError` en consola
  cp1252** (residual R2 de r1), truncando su propia salida a 12 rutas. Consecuencia: el dia que
  alguien instale pwsh 7 en un host Windows, `assert_cross_platform_skip_parity` no imprimira
  `UNMEASURED` -- se pondra ROJO en falso. Hoy esta latente porque `shutil.which("pwsh")` da `None`
  en el host Windows del equipo (solo PS 5.1). Es la misma clase de la tarea, con el signo cambiado:
  el contrato liga ahora una forma de plataforma (FS sensible a mayusculas) sin declararlo.
- **R6:** dos aserciones de mutante siguen guardadas por `if os.name != "nt"` (separador y ocultos),
  asi que en Windows esos dos mutantes solo estan atados por texto. Declarado y coherente con que la
  plataforma de medicion sea ubuntu, pero conviene que quede escrito.
- **R1 (de r1, sin tocar):** `powershell.exe` 5.1 no tiene `[System.IO.Path]::GetRelativePath`; el
  pipeline lanza `MethodNotFound` y AUN ASI imprime "OK: encoding scan is clean." y sale 0. Verde
  falso para cualquiera en Windows sin pwsh 7.
- **R3 (de r1, sin tocar):** paridad con pwsh 7 SOBRE Windows sigue sin medir en este host.

## Reproduccion con exit codes -- clon limpio POSIX sobre `eb47942a`

    python3 scripts/scan_encoding.py --root .                       -> 0   OK: encoding scan is clean.
    python3 scripts/validate_collaboration_state.py --root .        -> 0   OK: collaboration state is valid.
    python3 scripts/check_falsification_contracts.py --root .       -> 0
    python3 scripts/check_falsification_contracts.py --inventory    -> 0
    python3 scripts/scan_domain_neutrality.py --root .              -> 0
    python3 runtime/protocol_replay.py --check-drift --root .       -> 0   verdict=CLEAN up_to_seq=8222
    python3 examples/encoding_gate_cases/run_encoding_gate_cases.py -> 0   (POSIX, pwsh 7.4.6, 5,7 s)

## AC5 -- CI real

Run **31286367935** (`head_sha 677246a9`, ancestro de `eb47942a`, con codigo identico en las rutas
bajo revision):

    JOB powershell-linux-parity  [success]  <- job nuevo, entero verde
      [5] success Scan encoding with PowerShell on Linux
      [8] success Run PowerShell host-assumption contracts
    JOB validate [failure]
      [14] success Scan encoding
      [15] success Scan encoding with PowerShell      <- la evidencia del AC5
      [16] success Run encoding gate cases            <- el negativo, verde en ubuntu con pwsh 7
      [31] failure Run runtime property invariant cases   <- familia ajena, 15 pasos DESPUES

El run global es `failure` por dos familias ajenas (`mailbox retry` y `runtime property invariant`).
AC5 pide el PASO, no el job, y los tres pasos salieron `success`.

## Recomendacion de cierre

**CHANGE-REQUIRED.** Y quiero que se lea con la proporcion correcta: **los tres SLIPS de r1 estan
cerrados y bien cerrados**, los cuatro focos de la instruccion salen PASS, y el negativo paso de
mirar hallazgos a mirar conjuntos con 10 de 11 mutaciones de produccion muertas. Lo que no cierra es
estrecho y concreto: sobre el arbol real coinciden, pero **no coinciden por construccion**, y quedan
dos socavones falsables.

Respuesta directa a tu pregunta: **si, el negativo cae cuando los conjuntos divergen sin que haya
ningun hallazgo.** Medido con los dos escaneres en exit 0 diciendo lo mismo. Ese caso ya no se
escapa. El que se escapa ahora es otro: la divergencia que no pasa por ninguna de las 21 rutas del
universo.

### Bucle de arreglo esperado

1. **Remediacion 2 -- una sola nocion de sufijo (G1).** Que los dos gemelos deriven el sufijo de la
   MISMA regla, no de `Path.suffix` por un lado y `FileInfo.Extension` por el otro. Declarar cual es
   la regla para un nombre que empieza por punto: o `.png` tiene sufijo `.png` en los dos, o no lo
   tiene en ninguno. La eleccion es libre; la divergencia no.
2. **Remediacion 2 -- atar la case-sensitivity de las TRES listas (G2).** El contrato debe morir al
   revertir `-ccontains` en `$SkipDirs`, no solo al revertir `Ordinal` en la frontera
   `runtime/memory`. Sirve anadir al universo una variante de grafia por lista (p. ej.
   `runtime/Node_Modules/x.txt` y un `.PNG`), pero el criterio que juzgare es el de siempre: que la
   propiedad sobreviva a **cambio de coordenada** -- si manana se anade un sexto directorio a
   `$SkipDirs`, el contrato tiene que seguir atandolo sin que nadie edite el fixture.
3. **Declarar R5** en el handoff o resolverlo: hoy el negativo se pondra rojo en falso en Windows con
   pwsh 7, en vez de decir `UNMEASURED`. Si se declara, basta con que quede escrito y con que
   `assert_cross_platform_skip_parity` detecte el FS insensible y salga `UNMEASURED` en vez de
   fallar.
4. **Gates afectados:** `Scan encoding`, `Scan encoding with PowerShell`, `Run encoding gate cases`,
   `powershell-linux-parity`, `check_falsification_contracts --inventory`, y un run REAL de Actions
   -- el AC5 aplica igual a la remediacion, porque el cambio vuelve a ser de forma POSIX.
5. **Re-juicio del Analista antes del commit de cierre. Iteracion 1 de 2 consumida**; si a la
   siguiente sigue sin cerrar, escala al operador humano.

-- Analista
