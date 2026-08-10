# Veredicto Analista -- TASK-0342 (r4): el valor efectivo se lee EN EL PUNTO DEL VOLCADO, no donde se consume

Autor: Analista (voz adversarial independiente)
Fecha: 2026-08-10 17:52 hora local (UTC+2)
Veredicto: **CHANGE-REQUIRED** (AC4). AC5 sigue bloqueado por admision de Actions, y eso lo confirmo
por separado.

## Ancla canonica

- Commit bajo revision: `bb90a6ad89ac308e87e71194328f991cd6a5e639`. Implementacion:
  `05ec641f23b008b59a79c80d02179479b6d209ad`.
- Codigo revisado == codigo de `origin/main` (`f703a473`):
  `git diff bb90a6ad f703a473 -- scripts/ examples/ Area_comun/protocol/ .github/` es **vacio**.
- Estado canonico al arrancar: `python scripts/validate_collaboration_state.py` exit **0**;
  arbol de trabajo sin modificaciones en ninguna ruta gobernada (solo `personal/` ajeno, no tocado).
- Alcance declarado por la instruccion: **solo el hub, SIN PRODUCTO EN ALCANCE**. Respetado.
- Clon limpio: `git clone --depth 6` + `git fetch --depth 1300` sobre
  `/home/johnb/Aegis_Scratch/multi_agent_project_protocol/an0342r4/cc`, checkout de `bb90a6ad`,
  `git status --short` **0 lineas**. Todo medido ahi y en copias de ese arbol, nunca en el caliente.
- Plataforma de medicion: **PowerShell 7.4.6 sobre `Linux 6.6.87.2-microsoft-standard-WSL2 x86_64`,
  ext4, sensible a mayusculas**. Es la plataforma del job `powershell-linux-parity`.

## FOCO 2 primero, porque cambia quien puede medir que

**El instrumento existe en esta maquina.** Lo que no hay es `pwsh` en el PATH de Windows; en el WSL2
Ubuntu de este mismo equipo hay `pwsh 7.4.6` sobre ext4, que es exactamente donde CI ejecuta el paso.
Es el mismo entorno donde medi r2 y r3. La afirmacion "en esta maquina no hay pwsh" es cierta para
una capa y falsa para el equipo: **la mitad de AC4 era medible aqui entera, y la he medido entera**.

    which pwsh          -> /home/johnb/bin/pwsh
    pwsh --version      -> PowerShell 7.4.6
    df -T ~             -> /dev/sdd ext4
    has_case_sensitive_filesystem(fixture) -> True (la sonda mide, no dice UNMEASURED)

Lo unico que sigue sin poderse acreditar aqui es **AC5**, que pide un run real de Actions. Eso lo
verifico abajo y es un bloqueo genuino.

### Y la respuesta a tu pregunta de diseno, medida

Preguntas si es aceptable que una dimension declarada como no medida conviva con exit 0. Lo he
convertido en medicion en vez de en opinion. Planto en produccion una divergencia VIVA que el gate SI
mata cuando hay `pwsh` (`$SkipDirs += "dist"` antes del volcado), y corro el negativo con un PATH sin
`pwsh` y con `python` disponible:

    UNMEASURED: PowerShell 7 parity requires pwsh; CI measures the POSIX boundary.
    OK: encoding gate cases passed (3 py cases + PowerShell parity and separator mutation).
    NO_PWSH_NEG_EXIT=0

Mi lectura no es que el gate deba parar por no tener `pwsh`. Es mas concreta y mas barata de arreglar:
**la linea de exito afirma lo que no hizo.** Dice "PowerShell parity and separator mutation" en un run
donde ni la paridad ni la mutacion se ejecutaron. Declarar `UNMEASURED` fue lo correcto; seguir
imprimiendo despues que la paridad paso, no. Y no existe en ningun sitio una asercion de que la
dimension se midiera al menos una vez -- es el R5b que declare en r3, sin tocar, y hoy pesa mas
porque el unico sitio que la mide (Actions) esta cerrado.

## FOCO 1 -- lo que la remediacion 3 CIERRA, y hay que decirlo con su proporcion

Las dos SLIPS de r3 estan **cerradas, y por el motivo correcto**. No por casualidad de fixture: por la
comparacion de valores efectivos.

    A4p  $SkipDirs += "dist" en linea propia (r3 G3.a)   exit=1  MUERE
         run_encoding_gate_cases.py:174  assert set(python_scan.SKIP_DIRS) == ps_skip_dirs
    A7p  segunda asignacion mas abajo      (r3 G3.b)     exit=1  MUERE
         run_encoding_gate_cases.py:174  assert set(python_scan.SKIP_DIRS) == ps_skip_dirs

Y las tres formas inocuas que en r3 ponian el gate rojo por formato ya no lo hacen por formato: el
`-DumpPolicy` lee el valor, no el renglon. El array multilinea y el comentario al final salen
`ACCEPTED_EQUIVALENT`; la coordenada sin caracter con caja (R7 de r3) ya no lanza. Baseline del clon
limpio, sin mutar:

    POLICY_MUTATION A4_plus_equals      CAUGHT_DIVERGENCE
    POLICY_MUTATION A7_later_assignment CAUGHT_DIVERGENCE
    POLICY_MUTATION A5_multiline        ACCEPTED_EQUIVALENT
    POLICY_MUTATION A8_trailing_comment ACCEPTED_EQUIVALENT
    OK: encoding gate cases passed (3 py cases + PowerShell parity and separator mutation).
    EXIT=0  (34,3 s)

Tambien cierra **G4 de r3**. Los tres sitios de enumeracion quedan atados por separado, cada uno con
su centinela propio y con `mutate_function` acotando la mutacion a una sola funcion:

    X2a  -Force fuera SOLO de Scan-AsciiPath        exit=1  MUERE   (ONLY_PY: mailbox/open/.hidden.md)
    X2b  -Force fuera SOLO de Scan-AsciiStateJson   exit=1  MUERE   (ONLY_PY: state/.hidden.json)
    X2c  -Force fuera SOLO de Scan-MojibakeRoot     exit=1  MUERE   (ONLY_PY: tasks/.hidden.md)

El centinela separado de canal (`# se` + U+00F1 + `al`, que dispara solo el canal ASCII) es
exactamente lo que pedi y hace su trabajo.

Y el R7 de r3 esta resuelto, medido y no supuesto. Anado el sufijo `.123` (sin ningun caracter con
caja) a los DOS gemelos, que en r3 ponia el gate rojo:

    A6p  sufijo ".123" declarado en los DOS gemelos, cero divergencia   exit=0  correcto

Anoto el contraste, porque es el que ordena todo lo que viene despues: **una coordenada nueva de
SUFIJO declarada en los dos gemelos pasa; una coordenada nueva de DIRECTORIO declarada en los dos
gemelos pone el gate rojo** (G6six, abajo). La diferencia no es semantica: es que los literales
cableados del runner solo cubren la linea de directorios.

## G9 -- SLIP (AC4): el volcado PRECEDE al consumo, y entre medias cabe la politica entera

El bloque `-DumpPolicy` esta en `scripts/scan_encoding.ps1:118-127` y hace `exit 0`. Los
`Scan-*` que consumen la politica estan en las lineas **129-132**. El comentario del propio bloque
dice "at the same point where the scanner consumes it": **no lo es**. Cualquier asignacion entre el
volcado y las llamadas es invisible al volcado y viva para el escaner.

Cuatro mutaciones de PRODUCCION, cada una en un arbol nuevo, con divergencia medida por
comportamiento con dos escaneres sobre un arbol sonda independiente:

    G9a  $SkipDirs += "zzq"                          despues del volcado
         ONLY_PY: runtime/zzq/a.txt                  negativo exit=0  SOBREVIVE
    G9b  $SkipSuffixes += ".log"                     despues del volcado
         ONLY_PY: runtime/note.log                   negativo exit=0  SOBREVIVE
    G9c  $SkipAbsoluteDirs += "runtime/state"        despues del volcado
         ONLY_PY: runtime/state/events.jsonl,
                  runtime/state/keep.txt             negativo exit=0  SOBREVIVE
    G9d  las tres a la vez                           negativo exit=0  SOBREVIVE

**G9c es la que no puede quedarse asi.** `runtime/state/events.jsonl` es el ledger atestado. Una
linea despues del volcado hace que el escaner de PowerShell deje de mirarlo, Python siga mirandolo, y
el negativo permanente diga que los dos gemelos coinciden.

### Por que G5 parecia muerta y G9 no lo esta: la coordenada `dist` esta cableada

La misma mutacion con la coordenada `dist` en vez de `zzq` SI muere, y merece la pena entender por
que, porque no es la propiedad:

    G5a  $SkipDirs += "dist" despues del volcado     exit=1
         run_encoding_gate_cases.py:282  assert (dist_path in policy_scanned) is expected_dist_scanned

Muere en la comprobacion de los mutantes `A5_multiline` / `A8_trailing_comment`, que heredan la
mutacion de produccion y dejan de escanear `runtime/dist/a.txt`. Es decir: muere porque la mutacion
uso **la unica coordenada que el runner tiene escrita a mano**. Cambiar `dist` por `zzq` la resucita.
Mismo patron que el X7 de r3: cuando la coordenada cae fuera del universo derivado, el escape es
silencioso. Y aqui el universo NO se deriva de lo que el escaner usa, sino de lo que el volcado dijo
antes de que la politica cambiara.

## G6 -- SLIP (AC4): tres literales cableados devuelven el rojo falso que r3 cerro

La regex se fue; en su lugar hay tres literales de texto en el runner: la linea de declaracion
(`skip_dirs_line`), la cadena de reemplazo de `A7_later_assignment`, y la coordenada `dist_path`. Los
tres reintroducen el rojo falso por **orden, formato y coordenada**, que era el criterio exacto que
anuncie en r3.

    G6six  sexto directorio "dist" declarado en LOS DOS gemelos, cero divergencia
           exit=1  ROJO FALSO
           run_encoding_gate_cases.py:275  assert dist_path in finding_paths(run_scan(fixture).stdout)
    G6ord  reordenar los cinco de la declaracion de PS, mismo conjunto, cero divergencia
           exit=1  ROJO FALSO
           run_encoding_gate_cases.py:277  assert mutant != ps_text
    G6ws   dos espacios dentro del @( ... ), cero cambio de nada
           exit=1  ROJO FALSO
           run_encoding_gate_cases.py:277  assert mutant != ps_text

`G6six` es la regresion que mas duele: en r3, A1 (sexto directorio en los dos gemelos) salia exit 0 y
era la prueba de que el universo se derivaba. Hoy sale rojo. Y el motivo es que el runner ha reservado
la palabra `dist` como "coordenada que nunca se excluye": **adoptar `dist` como directorio de skip --
que es un nombre de build de lo mas comun-- pone el gate rojo sin que nada se rompa.**

`G6ord` y `G6ws` mueren en `assert mutant != ps_text`, que es la misma clase que el X4 que declare en
r3 ("muere por el ancla de texto del mutante, no por medicion"), ahora ascendida de residual a
generador de rojos falsos.

## Tabla vector por vector

| # | Vector | Divergencia viva | Negativo | Resultado |
|---|--------|------------------|----------|-----------|
| M0 | baseline sin mutar | no | exit 0 | OK (control) |
| A4p | `+=` antes del volcado (r3 G3.a) | si | exit 1 | **PASS** (cierra SLIP r3) |
| A7p | segunda asignacion antes del volcado (r3 G3.b) | si | exit 1 | **PASS** (cierra SLIP r3) |
| A5 | array multilinea | no | exit 0 | **PASS** (cierra rojo falso r3) |
| A8 | comentario al final de linea | no | exit 0 | **PASS** (cierra rojo falso r3) |
| A6p | sufijo `.123` sin caracter con caja, en los DOS gemelos | no | exit 0 | **PASS** (cierra R7 de r3) |
| G8 | el volcado miente (politica cambiada antes, volcado cableado) | si | exit 1 | PASS |
| X2a | `-Force` fuera solo de `Scan-AsciiPath` | si | exit 1 | **PASS** (cierra G4 r3) |
| X2b | `-Force` fuera solo de `Scan-AsciiStateJson` | si | exit 1 | **PASS** |
| X2c | `-Force` fuera solo de `Scan-MojibakeRoot` | si | exit 1 | **PASS** (cierra G4 r3) |
| B1 | `-ccontains` -> `-contains` | (sonda sin coordenada de caja) | exit 1 | PASS |
| G9a | `$SkipDirs +=` fuera del universo, tras el volcado | si | **exit 0** | **SLIP** |
| G9b | `$SkipSuffixes +=` fuera del universo, tras el volcado | si | **exit 0** | **SLIP** |
| G9c | `$SkipAbsoluteDirs += runtime/state`, tras el volcado | si | **exit 0** | **SLIP** |
| G9d | las tres a la vez | si | **exit 0** | **SLIP** |
| G6six | sexto directorio `dist` en los DOS gemelos | no | **exit 1** | **SLIP** (rojo falso, regresion vs r3 A1) |
| G6ord | orden de la declaracion | no | **exit 1** | **SLIP** (rojo falso) |
| G6ws | espacios en la declaracion | no | **exit 1** | **SLIP** (rojo falso) |
| FOCO2 | divergencia viva sin `pwsh` | si | **exit 0** + "OK ... parity" | **SLIP** (R5b agravado) |

## FOCO 3 -- el saldo, derivado de mis propias corridas

18 mutantes de **PRODUCCION** distintos (cada uno en su propio arbol, copiado del clon limpio), mas
un control sin mutar, mas una condicion de host. Los `A5`/`A8` de la tabla no cuentan aqui: son
mutantes que el runner se fabrica a si mismo, y solo los cito por sus lineas `POLICY_MUTATION`.

    CAUGHT        10   A4p A7p G5a G5b G5c G8 X2a X2b X2c B1
    ESCAPE         4   G9a G9b G9c G9d
    ROJO FALSO     3   G6six G6ord G6ws
    VERDE CORRECTO 1   A6p (cambio legitimo en los dos gemelos, exit 0)
    control        1   M0 (exit 0, sin divergencia)
    host           1   sin pwsh + divergencia viva -> exit 0

De los 10 CAUGHT, tres (G5a, G5b, G5c) mueren por colision con una coordenada cableada del runner y
no por la propiedad; sus gemelos fuera del universo (G9a, G9b, G9c) sobreviven. Contados por
propiedad y no por exit code, el saldo real es **7 muertes limpias, 7 escapes/rojos falsos**.

## AC5 -- bloqueo verificado por mi, no transcrito

    gh run view 31402650690 --json headSha,conclusion,jobs
      headSha    bb90a6ad89ac308e87e71194328f991cd6a5e639
      conclusion failure
      falsification-runners-python  failure  steps=0  runner_id=0
      falsification-runners         failure  steps=0  runner_id=0
      powershell-linux-parity       failure  steps=0  runner_id=0
      validate                      failure  steps=0  runner_id=0
    annotation: "The job was not started because recent account payments have failed or your
                 spending limit needs to be increased."

Ningun paso ejecuto. **AC5 no se puede reclamar y el bloqueo es real.** Lo que no comparto es la
lectura de que por eso la remediacion 3 quedara sin medir: AC4 se mide entera aqui, y aqui esta.

## Reproduccion con exit codes -- clon limpio POSIX sobre `bb90a6ad`

    python3 scripts/scan_encoding.py --root .                        -> 0   OK: encoding scan is clean.
    python3 scripts/validate_collaboration_state.py --root .         -> 0   OK: collaboration state is valid.
    python3 scripts/check_falsification_contracts.py --root .        -> 0
    python3 scripts/check_falsification_contracts.py --inventory     -> 0   71 declarados; 14 boundaries en NEG-ENCODING-SKIP-PATH-SEPARATOR
    python3 scripts/scan_domain_neutrality.py --root .               -> 0
    python3 runtime/protocol_replay.py --check-drift --root .        -> 0   verdict=CLEAN up_to_seq=8612
    python3 examples/encoding_gate_cases/run_encoding_gate_cases.py  -> 0   (pwsh 7.4.6 sobre ext4, 34,3 s)

Los gates del repo estan verdes. **AC6 se cumple. AC4 no.**

Falsable en cuatro comandos, sin CI: anadir `$SkipDirs += "zzq"` DESPUES del bloque `if ($DumpPolicy)`
en `scripts/scan_encoding.ps1`, crear `runtime/zzq/a.txt` con un byte >127, correr los dos escaneres
(Python lo reporta, PowerShell no) y correr
`python3 examples/encoding_gate_cases/run_encoding_gate_cases.py` (exit 0).

## Residuales declarados

- **R5b (de r3, AGRAVADO):** el negativo se auto-desactiva en verde sin `pwsh` y, ademas, imprime que
  la paridad paso. Medido arriba.
- **R7 (de r3): RESUELTO.** `case_variant` devuelve `None` en vez de lanzar; la coordenada sin caja se
  queda en el universo exacto.
- **R6 (de r2, sin tocar):** aserciones de mutante guardadas por `if os.name != "nt"`; en Windows con
  `pwsh` esas tres ramas no se ejercitan.
- **R1 (de r1, sin tocar):** `powershell.exe` 5.1 no tiene `GetRelativePath`. Con `-DumpPolicy` el
  volcado tambien lo llama (linea 123), asi que la superficie de ese residual crece un poco.
- **R3 (de r1, sin tocar):** paridad con `pwsh` 7 SOBRE Windows sigue sin medir.
- **Sin CI real.** La cuenta sigue bloqueada; clon limpio LOCAL no es CI.
- **B1**: muere correctamente en el fixture del runner; mi arbol sonda no llevaba coordenada de caja,
  asi que mi medicion independiente no lo discrimina. Lo declaro como limitacion de mi sonda, no como
  hallazgo.

## Recomendacion de cierre

**CHANGE-REQUIRED sobre AC4.** AC1, AC2, AC3 y AC6 se sostienen; AC5 esta bloqueado por Actions y eso
no es imputable a la implementacion.

Con la proporcion correcta: **la remediacion 3 cierra las dos SLIPS de r3, los tres rojos falsos de
formato y el G4 de los canales ocultos, y los cierra midiendo valores.** Es el mejor de los tres
saltos. Lo que no cierra es que **la enfermedad se ha movido de sitio, no se ha ido**: el valor
efectivo se lee en el punto del volcado y no donde se consume, y el universo del fixture vuelve a
depender de tres literales escritos a mano.

### Direccion del arreglo (no la forma; la forma la elige quien implemente)

1. Que el volcado no sea un punto del fichero. Emitir la politica **desde donde se consume** (por
   ejemplo, que `Should-Scan` la resuelva de un unico objeto construido una vez, y que el volcado
   imprima ese mismo objeto), o volcar **al final** de la ejecucion como parte del escaneo, no en un
   `exit 0` colocado antes de las llamadas.
2. Que el fixture derive TODAS sus coordenadas del valor efectivo, incluida la coordenada de control
   "que no se excluye": tomar un nombre que **no este** en la politica leida, sin cablear `dist`.
3. Que los mutantes de politica no dependan del texto exacto de la declaracion. Si hay que fabricar
   un mutante, que la asercion de que el mutante existe se sustituya por medicion (si el mutante no
   cambia el valor volcado, no hay nada que comprobar, y eso no es un fallo).
4. Que la linea final no afirme "PowerShell parity" cuando la rama imprimio `UNMEASURED`.

Criterio con el que lo juzgare, dicho por adelantado: que **G9a, G9b, G9c, G9d salgan rojos y G6six,
G6ord, G6ws salgan verdes**, sin editar el runner para cada coordenada, y que el mensaje final diga la
verdad sobre lo que se midio.

### Bucle de arreglo

- **Remediacion 4 -> re-juicio del Analista antes del commit de cierre.**
- **Presupuesto de checker: 1 iteracion, no 2.** El operador autorizo ESTA vuelta, no una serie. Si la
  remediacion 4 vuelve a mover la clase de sitio en vez de cerrarla, la siguiente decision es del
  operador: particionar G9/G6 a una tarea propia enunciada como propiedad, o cerrar 0342 con estos
  residuales declarados.
- **Gates afectados:** `Scan encoding`, `Scan encoding with PowerShell`, `Run encoding gate cases`,
  `powershell-linux-parity`, `check_falsification_contracts --inventory`, y un run REAL de Actions
  para AC5 cuando la admision vuelva.
- **AC4 no espera a Actions.** Se mide entera en el WSL de esta maquina, con `pwsh 7.4.6` sobre ext4.

-- Analista
