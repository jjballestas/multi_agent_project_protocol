---
id: TASK-0342
title: La exclusion de directorios del gemelo de encoding liga la barra invertida de Windows
status: in_progress
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0342-la-exclusion-del-gemelo-de-encoding-liga-la-barra-de-windows.md
created: 2026-08-08
intake:
  type: fix
  goal: >
    `scripts/scan_encoding.ps1:36` decide si una ruta esta excluida con
    `$File.FullName.StartsWith("$directory\", ...)`, con la barra invertida LITERAL. En Linux --que
    es donde CI ejecuta ese paso, sobre ubuntu-latest con pwsh-- las rutas usan barra normal, el
    prefijo nunca casa, y la exclusion de `runtime/memory` falla en SILENCIO: el escaner lee el
    SQLite `runtime/memory/index.db` y lo reporta como mojibake. El gemelo Python no tiene el
    defecto porque compara rutas RELATIVAS con barra normal. Llevaba enmascarado desde el 2026-08-02
    porque un paso anterior del mismo job caia antes.
  acceptance:
    - "AC1 (falsacion previa): se reproduce que el paso falla en un entorno POSIX y pasa en Windows con el MISMO arbol, y se demuestra que la causa es el separador y no el contenido del fichero."
    - "AC2 (la exclusion deja de ligar un separador): la decision de si una ruta esta excluida se toma sobre una forma independiente de la plataforma. Se declara la forma elegida."
    - "AC3 (paridad con el gemelo Python): los dos escaneres excluyen EXACTAMENTE el mismo conjunto de rutas sobre el mismo arbol, verificado por comportamiento en las dos plataformas o declarando la que no se pudo medir."
    - "AC4 (contrato): negativo permanente que muera si los dos escaneres dejan de coincidir en el conjunto excluido, o si la exclusion vuelve a depender de un separador concreto, verificado por MUTACION."
    - "AC5 (cerrado en CI REAL): el paso `Scan encoding with PowerShell` sale success en un run real de GitHub Actions, citando su id. Evidencia local no cierra esta tarea: el defecto NO se manifiesta en Windows."
    - "AC6 (sin regresion): los gates del repo exit 0 en clon limpio y ninguna ruta legitima pasa a excluirse."
  verification_cmd:
    - "python scripts/scan_encoding.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/check_falsification_contracts.py --root ."
  scope_routes:
    - scripts/scan_encoding.ps1
    - scripts/scan_encoding.py
    - Area_comun/protocol/FALSIFICATION_CONTRACTS.json
    - examples/
  out_of_scope:
    - "El troceado de lineas divergente entre los escaneres de neutralidad (TASK-0338)."
    - "La nocion de comando del gate de cableado (TASK-0336)."
    - "El fallo del runner de retry en CI, que es otra causa."
    - "Codigo de producto."
  risk: medium
  estimate: S
---

# TASK-0342 -- la exclusion falla en silencio fuera de Windows

## Lo medido

CI, run 31266113929, job `validate`, paso `Scan encoding with PowerShell` sobre **ubuntu-latest**:

    ENCODING ERRORS:
    - mojibake: runtime/memory/index.db:1

El fichero es una base de datos SQLite y **los dos escaneres declaran excluir `runtime/memory`**:

    python:      SKIP_RELATIVE_DIRS = {"runtime/memory"}
                 relative == item or relative.startswith(f"{item}/")     <- barra normal, relativa
    powershell:  $SkipAbsoluteDirs = @((Join-Path $ResolvedRoot "runtime/memory"))
                 $File.FullName.StartsWith("$directory\", ...)           <- barra INVERTIDA literal

En Linux `$File.FullName` es `/home/.../runtime/memory/index.db` y la comparacion busca un prefijo
terminado en `\`. No casa nunca. La exclusion no se aplica, el escaner lee el binario y grita.

## Por que es la tercera del dia

Es la tercera divergencia entre gemelos encontrada el 2026-08-08, y las tres por la misma causa de
fondo: **atar una forma concreta de plataforma o de lenguaje en vez de la propiedad**.

- **TASK-0338**: `str.splitlines()` rompe en siete separadores y `Get-Content` en uno.
- **TASK-0336 B1**: el gate calculaba la frontera de comando con la nocion de linea de Python
  cuando quien ejecuta es bash.
- **Esta**: la exclusion de rutas liga el separador de Windows cuando el gate corre en Linux.

Declararlo importa: si al arreglar esta se ve que las tres piden un criterio compartido, **dilo y lo
particiono**; no lo absorbas aqui.

## Nota sobre el AC5

Esta tarea **no se puede cerrar con evidencia local**, y no es una formalidad: el defecto es
invisible en Windows, que es donde trabajamos. Cerrarla desde aqui seria certificar verde
exactamente en el unico entorno donde el fallo no ocurre.

## Remediation 1 - declared scanned and excluded sets

The shared contract is exact-case path semantics. Both scanners scan hidden files and hidden
directories. Both exclude only files under an exact-case `runtime/memory` boundary, files with a
lowercased suffix in the shared suffix list, or files whose path has an exact-case segment in the
shared skip-directory list.

Before remediation, PowerShell effectively excluded these ten real-tree sentinels that Python
scanned because recursive enumeration omitted hidden entries:

- `Area_comun/artifacts/.gitkeep`
- `Area_comun/contracts/.gitkeep`
- `Area_comun/decisions/.gitkeep`
- `Area_comun/handoffs/.gitkeep`
- `Area_comun/mailbox/answered/.gitkeep`
- `Area_comun/mailbox/archived/.gitkeep`
- `Area_comun/mailbox/open/.gitkeep`
- `Area_comun/reports/.gitkeep`
- `Area_comun/tasks/.gitkeep`
- `runtime/.cache/note.txt`

After remediation, both scanners scan all ten. On a case-sensitive tree, both also scan
`runtime/Memory/case.txt`; only exact-case `runtime/memory/**` is excluded. The permanent property
plants a detectable sentinel in 21 paths, derives each scanner's scanned and excluded complements,
and requires the same declared 16 scanned paths and five excluded paths. Mutants independently
remove hidden enumeration, restore case-insensitive matching, restore the literal Windows
separator, and add a PowerShell-only `Area_comun/tasks` exclusion; every mutation changes the
measured set even when both scanner exit codes remain 1.

## Remediation 2 - construction-derived parity

Both scanners now define the same suffix rule: the final dot starts a suffix only when at least one
basename character precedes it, and matching normalizes that suffix to lowercase. Therefore a name
whose complete basename is `.png`, `.zip`, or `.pyc` has no suffix and is scanned by both twins;
`real.PNG` has suffix `.png` and is excluded by both.

The permanent negative derives its directory and suffix coordinates from the production
declarations of both twins. For every declared skip directory it creates an exact spelling and a
case-changed spelling; for every suffix it creates lowercase, uppercase, and dot-only basenames.
Adding another declared directory or suffix expands the property without editing its fixture. A
production mutation from `$SkipDirs -ccontains $part` to `$SkipDirs -contains $part` therefore
changes the measured set and kills the contract.

R5 is resolved as a measurement precondition. The cross-platform parity property probes the
fixture filesystem before creating case-distinct coordinates. On a case-insensitive filesystem it
reports `UNMEASURED` and exits without a false failure; the case-sensitive POSIX boundary remains a
required real Actions measurement.
