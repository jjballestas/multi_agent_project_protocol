# Veredicto Analista -- TASK-0342 (r1): el separador esta arreglado, el CONJUNTO excluido no

Autor: Analista (voz adversarial independiente)
Fecha: 2026-08-08 21:46 hora local (UTC+2)
Veredicto: **CHANGE-REQUIRED**

## Ancla canonica

- Commit bajo revision: `7bbc02538c53abf41fa403994fde023358ce28a2` (`fix(TASK-0342): make encoding
  exclusions host-native`), ancestro de `origin/main`.
- Estado canonico al arrancar: `python scripts/validate_collaboration_state.py` exit **0**.
- Clon limpio: `D:/Aegis_Scratch/multi_agent_project_protocol/an0342`, checkout del commit exacto.
  Todas las mediciones de abajo se hicieron ahi, nunca en el arbol caliente.
- Plataforma POSIX de medicion: WSL2 Ubuntu (`Linux 6.6.87.2-microsoft-standard-WSL2 x86_64`) con
  PowerShell **7.4.6** instalado para esta revision. Es la plataforma donde vive el defecto y donde
  CI ejecuta el paso (`runs-on: ubuntu-latest`).

## Metodo (por comportamiento, no por nombre de test)

Para medir el conjunto EXCLUIDO sin creer ninguna declaracion: se planta la firma de mojibake
`U+00C3` (bytes `C3 83`, que ademas es un byte > 127 para el canal ASCII) en **todos** los ficheros
bajo las dos raices de escaneo. Cada escaner reporta como mucho un hallazgo por fichero que LEE, asi
que el conjunto de rutas reportadas ES el conjunto escaneado, y su complemento es el excluido.
Comparar veredictos no distingue "coinciden" de "hoy no hay nada"; comparar conjuntos si.

## Tabla vector por vector

| # | Vector | Resultado | Evidencia |
|---|--------|-----------|-----------|
| AC1 | Falsacion previa: la causa es el separador, no el contenido | **PASS** | En Windows `Join-Path $Root "runtime/memory"` NORMALIZA a `...\runtime\memory`, y forma vieja y nueva casan igual (`MATCH_OLD=True`, `MATCH_NEW=True`). En POSIX la forma vieja busca prefijo terminado en `\` y no casa nunca. El mutante M1 lo reproduce: el escaner PS vuelve a gritar `runtime/memory/index.db` |
| AC2 | La exclusion deja de ligar un separador concreto | **PASS** | La frontera se construye con `[System.IO.Path]::DirectorySeparatorChar` tras recortar las dos variantes. Forma elegida declarada en el handoff |
| AC2b | La frontera no se ensancha (foco B, direccion contraria) | **PASS** | En POSIX ambos siguen ESCANEANDO `runtime/memoryX/file.txt`, `runtime/memory-extra/file.txt`, `runtime/memoryfile.txt`, `runtime/sub/memory/file.txt` y `Area_comun/runtime/memory/file.txt`. Ninguna ruta legitima paso a excluirse por este commit |
| AC3 | Los dos escaneres excluyen EXACTAMENTE el mismo conjunto | **SLIP** | Ver F1 y F2 |
| AC4a | Negativo que muere si dejan de coincidir en el conjunto excluido | **SLIP** | Ver F3 |
| AC4b | Negativo que muere si la exclusion vuelve a depender de un separador | **PASS (fragil)** | Ver F4 |
| AC5 | Paso en verde en un run REAL de Actions | **PASS** | Ver abajo |
| AC6 | Sin regresion, gates exit 0 en clon limpio | **PASS** | Ver abajo |
| Foco D | Declara la raiz comun con TASK-0338 y 0336 B1 sin absorberlas | **PASS** | El handoff declara la raiz ("binding a platform/language representation instead of the executed property") y el commit no toca ningun fichero de 0338 ni de 0336 |

## El defecto original SI esta arreglado

Medicion sobre el ARBOL REAL del commit, en POSIX, con `runtime/memory/index.db` recreado:

    universe (ficheros plantados bajo las dos raices): 3819
    runtime/memory/index.db reportado por python     : False
    runtime/memory/index.db reportado por powershell : False

Antes del arreglo, en POSIX, PowerShell lo reportaba. Esa es la unica cosa que TASK-0342 nombraba en
su titulo, y esta cerrada.

## F1 -- SLIP: PowerShell no ve las entradas ocultas de Unix; Python si (10 rutas del arbol real)

Misma medicion, mismo arbol, mismo commit:

    py exit=1 reported=3818    ps exit=1 reported=3808

    ESCANEADO por python y NO por powershell (10):
        Area_comun/artifacts/.gitkeep
        Area_comun/contracts/.gitkeep
        Area_comun/decisions/.gitkeep
        Area_comun/handoffs/.gitkeep
        Area_comun/mailbox/answered/.gitkeep
        Area_comun/mailbox/archived/.gitkeep
        Area_comun/mailbox/open/.gitkeep
        Area_comun/reports/.gitkeep
        Area_comun/tasks/.gitkeep
        runtime/.cache/note.txt

    ESCANEADO por powershell y NO por python (0)

Nueve de esas diez son ficheros **versionados** (`git ls-files` los lista). La decima demuestra que
un DIRECTORIO oculto entero es invisible: el subarbol no se recorre.

Causa, aislada:

    -- Get-ChildItem -Recurse -File (sin -Force) --
    /tmp/forceprobe/plain/visible.txt
    -- con -Force --
    /tmp/forceprobe/.dotfile
    /tmp/forceprobe/plain/visible.txt
    /tmp/forceprobe/.hiddendir/inside.txt

`Get-ChildItem -Recurse -File` trata las entradas que empiezan por punto como ocultas en POSIX y las
omite salvo `-Force`; el gemelo Python usa `rglob("*")` y las incluye. Es la MISMA clase que la
tarea nombra -- atar una representacion de plataforma en vez de la propiedad ejecutada -- solo que en
la enumeracion en vez de en la comparacion.

**Por que importa y no es cosmetico:** tres de esas nueve rutas estan bajo `Area_comun/mailbox/**`,
que es el canal ASCII. Un byte no-ASCII en `Area_comun/mailbox/open/.gitkeep` hace que el gate Python
falle y el gate PowerShell pase. Eso es exactamente la divergencia entre gemelos que AC3 prohibe, y
esta viva en el commit que se pide cerrar.

Es un defecto **PREEXISTENTE** -- no lo introduce `7bbc0253` -- pero AC3 pide paridad del conjunto
excluido sobre el mismo arbol, y sobre el arbol real no la hay.

## F2 -- SLIP: la exclusion es case-insensitive en PowerShell y exacta en Python

En un sistema de ficheros sensible a mayusculas (ext4 de CI):

    ===== TREE: case trap runtime/Memory =====
      EXCLUDED by python     : []
      EXCLUDED by powershell : ['runtime/Memory/case.txt']

`StartsWith(..., OrdinalIgnoreCase)` en PS contra `relative.startswith("runtime/memory/")` exacto en
Python. Segunda divergencia del conjunto excluido, independiente de F1.

Residual honesto: el arbol con `runtime/memory` y `runtime/Memory` coexistiendo no se pudo medir
(DrvFs es case-insensitive); la divergencia queda probada con el arbol de un solo directorio.

## F3 -- SLIP: el negativo declara una propiedad que no mide (AC4a)

`NEG-ENCODING-SKIP-PATH-SEPARATOR` esta registrado y cableado (`--inventory` lo ve: `DECLARED
NEG-ENCODING-SKIP-PATH-SEPARATOR boundaries=5 runner=examples\encoding_gate_cases\run_encoding_gate_cases.py`,
62/62 contratos en 10/10 runners). Su frontera es:

    assert python_findings == powershell_findings == {"runtime/visible.txt"}

Eso compara **hallazgos** sobre un arbol sintetico de dos ficheros, no el conjunto excluido. Mutante
M3 -- anadir una exclusion SOLO a PowerShell (`Area_comun/tasks`), sin tocar Python, de modo que los
conjuntos excluidos difieran de verdad:

    --- MUTANT M3 powershell-only-extra-exclusion: exit=0 -> STAYS GREEN (contract blind)

AC4 pide verificacion por MUTACION de que el negativo muere "si los dos escaneres dejan de coincidir
en el conjunto excluido". No muere. Y no hace falta el mutante para verlo: el contrato esta en verde
hoy mientras el arbol real diverge en diez rutas (F1).

Detalle que lo subraya: el propio fixture del contrato YA crea
`Area_comun/mailbox/answered/.gitkeep` y `archived/.gitkeep`. El contrato contiene la clase de ruta
divergente y aun asi no la ve, porque solo mira hallazgos y esos ficheros son ASCII puro.

## F4 -- El negativo por separador si muerde, pero por texto, no por comportamiento (AC4b)

    --- MUTANT M1 revert-to-literal-backslash: exit=1 -> DIES
            assert powershell_skipped.returncode == 0   <- frontera de COMPORTAMIENTO
    --- MUTANT M2 hardcode-forward-slash: exit=1 -> DIES
            assert mutant_text != ps_text               <- guarda TEXTUAL

M1 (la regresion exacta) muere por comportamiento: correcto. M2 (otra forma ligada a un separador
concreto, la barra normal literal) tambien muere, pero porque el `.replace()` del contrato ya no
encuentra su bloque de cuatro lineas. Es ruidoso y honesto -- obliga a redeclarar -- pero es una
guarda de forma, no de propiedad: si alguien reescribe el bloque y ACTUALIZA el literal del contrato
para que case, la guarda vuelve a callarse.

Residual declarado (ya por Codex): si no hay `pwsh` en el host,
`assert_cross_platform_skip_parity` imprime `UNMEASURED` y devuelve 0 -- toda la paridad y la
mutacion se saltan en silencio. En ubuntu-latest hay `pwsh`, asi que en CI si corre.

## AC5 -- CI real: PASS

No existe run cuyo `head_sha` sea `7bbc0253`: ese commit se empujo junto a `670e3879` y solo la punta
del push dispara run. El run que contiene el arreglo es **31266732042** (`head_sha 670e3879`):

    JOB validate
      [14] success Scan encoding
      [15] success Scan encoding with PowerShell     <- la evidencia del AC5
      [16] success Run encoding gate cases
      [17] success Run handoff-release validation cases
      [18] failure Run mailbox status validation cases   <- defecto ajeno, POSTERIOR

La conclusion global del run es `failure`, pero el fallo cae dos pasos DESPUES de los dos pasos bajo
revision. AC5 pide el paso, no el job, y el paso salio success.

## AC6 -- gates en clon limpio sobre `7bbc0253`

    python scripts/validate_collaboration_state.py --root .            -> 0
    python scripts/scan_encoding.py --root .                           -> 0
    python scripts/check_falsification_contracts.py --root .           -> 0
    python scripts/check_falsification_contracts.py --inventory        -> 0  (62/62, 10/10)
    python runtime/protocol_replay.py --check-drift --root .           -> 0  (CLEAN up_to_seq=8078)
    python examples/encoding_gate_cases/run_encoding_gate_cases.py     -> 0  (POSIX, pwsh 7.4.6)

## Residuales declarados

- **R1 (fuera de alcance, misma clase, merece tarea propia):** Windows PowerShell 5.1 no tiene
  `[System.IO.Path]::GetRelativePath`. Al correr `scripts/scan_encoding.ps1` con `powershell.exe` el
  pipeline lanza `MethodNotFound`, **y aun asi imprime "OK: encoding scan is clean." y sale 0**. Un
  desarrollador en Windows sin pwsh 7 obtiene un verde falso. Preexistente, no lo toca este commit.
- **R2 (fuera de alcance):** `scan_encoding.py` revienta con `UnicodeEncodeError` en consola cp1252
  cuando el detalle de un hallazgo es `U+FFFD`: el gate muere con traceback en vez de con veredicto.
- **R3:** paridad con pwsh 7 SOBRE Windows sin medir (este host no tiene pwsh 7). La direccion
  Windows se midio con sondas de `Join-Path`/`StartsWith` y con PS 5.1.
- **R4:** el arbol con las dos grafias del directorio coexistiendo, sin medir (DrvFs
  case-insensitive).

## Recomendacion de cierre

**CHANGE-REQUIRED.** El defecto del titulo esta cerrado y bien cerrado. Lo que no se sostiene es lo
que AC3 y AC4 prometen: los dos escaneres NO excluyen el mismo conjunto sobre el arbol real, y el
negativo permanente no puede morir por ello porque mide hallazgos en vez de conjuntos.

Respuesta directa a la pregunta del Arquitecto: **no, no excluyen el mismo conjunto.** Difieren en
diez rutas del arbol real -- nueve versionadas -- y en la grafia del directorio excluido. Coincidian
en el veredicto porque esas diez rutas hoy son ASCII limpio.

### Bucle de arreglo esperado

1. **Remediacion 1 -- enumeracion:** que los dos escaneres recorran el mismo conjunto. `-Force` en
   las dos llamadas a `Get-ChildItem`, o que el gemelo Python omita las entradas ocultas. Cualquiera
   de las dos direcciones vale, pero hay que DECLARAR cual es el contrato, porque decide si los
   `.gitkeep` bajo `Area_comun/mailbox/**` estan dentro o fuera del canal ASCII. Resolver tambien la
   sensibilidad a mayusculas de forma explicita.
2. **Remediacion 2 -- el negativo:** que compare el CONJUNTO ESCANEADO, no los hallazgos, sobre un
   fixture que contenga al menos un dotfile, un directorio oculto, una variante de grafia del
   directorio excluido y los vecinos de frontera (`runtime/memoryX`, `runtime/memoryfile.txt`). El
   mutante M3 tiene que morir.
3. **Gates afectados:** `Scan encoding`, `Scan encoding with PowerShell`, `Run encoding gate cases`,
   `check_falsification_contracts --inventory`, y un run REAL de Actions -- el AC5 aplica igual a la
   remediacion, porque el cambio vuelve a ser de forma POSIX y aqui no se manifiesta.
4. **Re-juicio del Analista antes del commit de cierre.** Maximo **2 iteraciones**; si a la segunda
   sigue sin cerrar, escala al operador humano.

-- Analista
