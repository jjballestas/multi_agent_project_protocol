---
id: TASK-0345
title: Los gemelos PowerShell asumen el host Windows y nadie los ejecuta en Linux hasta que CI falla
status: in_progress
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0345-los-gemelos-powershell-asumen-el-host-windows.md
created: 2026-08-08
intake:
  type: fix
  goal: >
    En una sola jornada han aparecido CUATRO defectos de la misma clase: un gemelo PowerShell liga
    una suposicion del host Windows y falla en Linux, que es donde CI lo ejecuta. Se arreglaron uno
    a uno porque cada fallo enmascaraba al siguiente. Esta tarea ataca la CLASE: inventariar todas
    las suposiciones dependientes de host en los scripts PowerShell que CI ejecuta, ligarlas a
    formas neutrales, y anadir un contrato que los ejercite en Linux para que la quinta no se
    descubra por un fallo de CI.
  acceptance:
    - "AC1 (falsacion previa e inventario): se reproduce el fallo abierto conocido -- `Get-RelativePath` usa `MakeRelativeUri` y lanza 'This operation is not supported for a relative URI' en Linux (scan_domain_neutrality.ps1:305) -- y se INVENTARIAN todas las suposiciones dependientes de host de los .ps1 que CI ejecuta: separadores, rutas absolutas frente a relativas, troceado de lineas, mayusculas y minusculas del sistema de ficheros, y finales de linea. El inventario se entrega aunque solo una este rota."
    - "AC2 (formas neutrales): cada suposicion inventariada pasa a una forma independiente del host, o se declara por que debe seguir siendo especifica y que la protege."
    - "AC3 (los gemelos se EJERCITAN en Linux): existe al menos un job de CI que ejecuta los .ps1 afectados sobre Linux y cuyo fallo tumba el job. Hoy la unica forma de descubrir estos defectos es que otro paso deje de fallar antes."
    - "AC4 (contrato): negativo permanente que muera si un .ps1 ejecutado por CI vuelve a depender de una forma especifica del host, verificado por MUTACION. Debe caer con el mutante que reintroduzca cualquiera de las cuatro formas ya conocidas."
    - "AC5 (paridad de veredicto, no solo de ejecucion): donde exista gemelo Python, los dos deben emitir el MISMO veredicto sobre el mismo arbol en las dos plataformas, o declararse la que no se pudo medir."
    - "AC6 (cerrado en CI REAL): los pasos afectados salen success en un run real de GitHub Actions, citando su id. Ninguno de los cuatro defectos de esta clase es visible desde Windows, que es donde trabajamos."
  verification_cmd:
    - "python scripts/scan_domain_neutrality.py --root ."
    - "python scripts/scan_encoding.py --root ."
    - "python scripts/check_falsification_contracts.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - scripts/scan_domain_neutrality.ps1
    - scripts/scan_encoding.ps1
    - examples/neutrality_scan_cases/
    - .github/workflows/validate.yml
    - Area_comun/protocol/FALSIFICATION_CONTRACTS.json
  out_of_scope:
    - "El troceado de lineas de los escaneres de neutralidad (TASK-0338): coordinar, no absorber."
    - "La nocion de comando del gate de cableado (TASK-0336 B1)."
    - "La asercion de rollback del runner de retry (TASK-0343)."
    - "Codigo de producto."
  risk: high
  estimate: L
---

# TASK-0345 -- la clase, no la quinta instancia

## Las cuatro de hoy

| # | Donde | La suposicion del host |
|---|-------|------------------------|
| 1 | `scan_domain_neutrality.ps1` / `.py` (TASK-0338) | `str.splitlines()` rompe en siete separadores y `Get-Content` en uno |
| 2 | `check_falsification_contracts.py` (TASK-0336 B1) | la frontera de comando se calculaba con la nocion de linea de Python cuando quien ejecuta es bash |
| 3 | `scan_encoding.ps1` (TASK-0342, **arreglado**) | `StartsWith("$directory\")` con la barra invertida LITERAL: en Linux no casa nunca y la exclusion falla en silencio |
| 4 | `scan_domain_neutrality.ps1:305` (**este**) | `Get-RelativePath` usa `MakeRelativeUri`, que lanza en Linux cuando el URI es relativo |

**Las cuatro fallan solo fuera de Windows. Ninguna es visible desde donde trabajamos.**

## El fallo abierto conocido

CI run 31267480822, paso `Run neutrality scan validation cases`, ubuntu-latest:

    ForEach-Object: .../scripts/scan_domain_neutrality.ps1
    Line | 305 | Get-ChildItem -Path $resolvedRoot -Recurse -File -Force | ForEach-Object {
         | Exception calling "MakeRelativeUri" with "1" argument(s):
         | "This operation is not supported for a relative URI."

En local sale **exit 0**. `MakeRelativeUri` entro en `a9afe227`, hace tiempo: es **preexistente y
enmascarado**, no regresion de hoy.

## Por que la clase y no la instancia

Arreglar la cuarta por separado dejaria la quinta esperando a que otro paso deje de fallar antes. En
esta jornada, **cada arreglo de CI destapo el siguiente defecto de la misma familia**, y los cinco
llevaban meses ahi. El AC3 es el que rompe ese ciclo: si los gemelos se ejercitan en Linux, la
proxima suposicion de host se descubre al introducirla, no seis dias despues.

## Nota de encuadre

Si al inventariar resulta que la forma correcta es un helper compartido -- resolucion de rutas,
troceado de lineas -- **dilo y lo particiono**. No absorbas 0338 ni 0336: estan contratadas y en
curso.

## Inventario de suposiciones de host

| Ruta ejecutada por CI | Separadores y rutas | Troceado y finales de linea | Mayusculas/minusculas | Forma y proteccion |
|---|---|---|---|---|
| `scripts/validate_collaboration_state.ps1` | `Join-Path`, `Resolve-Path`, separadores normalizados y comparacion dependiente del host | `Get-Content` interpreta lineas PowerShell; sus casos SDD y compactos comparan contra Python | rutas `OrdinalIgnoreCase` solo en Windows, `Ordinal` fuera | especifica por semantica del validador; casos gemelos SDD/compactos |
| `scripts/scan_encoding.ps1` | `Path.GetRelativePath`, separador nativo y frontera nativa | bytes para offsets LF; `ReadAllLines` para mojibake | frontera de ruta insensible solo en Windows | neutral; `NEG-ENCODING-SKIP-PATH-SEPARATOR` y contrato TASK-0345 |
| `scripts/scan_domain_neutrality.ps1` | raiz absoluta, frontera con separador nativo y salida POSIX | el `Get-Content` conocido queda acotado a una ocurrencia bajo TASK-0338 | frontera de ruta segun host; regex y terminos deliberadamente insensibles, igual que Python | ruta neutral; troceado no absorbido, protegido contra expansion y referido a TASK-0338 |
| `examples/sdd_validation_cases/run_sdd_cases.ps1` | `Join-Path` | normaliza CRLF a LF al comparar procesos del mismo host | nombres de caso exactos | neutral; paridad Python/PowerShell en CI Linux |
| `examples/compact_comms_validation_cases/run_compact_comms_cases.ps1` | `Join-Path` | normaliza CRLF a LF al comparar procesos del mismo host | nombres de caso exactos | neutral; paridad Python/PowerShell en CI Linux |
| `examples/neutrality_scan_cases/run_neutrality_scan_cases.ps1` | `Join-Path` | normaliza CRLF a LF al comparar procesos del mismo host | nombres de caso exactos | neutral; paridad de veredicto y salida en CI Linux, con `exit 0` explicito para no filtrar el ultimo negativo esperado |
| `examples/llm_turn_wrapper_cases/run_llm_turn_wrapper_cases.ps1` | `Join-Path` | delega el contrato al runner Python | no compara rutas | neutral; smoke wrapper en CI Linux |

La cuarta averia no necesita helper compartido: una raiz resuelta y una frontera con el separador
nativo resuelven la ruta tambien en Windows PowerShell 5.1. La segunda forma conocida pertenece al lector de workflow Python,
no a un `.ps1`; sigue protegida por `NEG-FALSIFICATION-RUNNER-WIRING` de TASK-0336. El contrato
TASK-0345 comprueba que no reaparezca `splitlines()` en esa frontera.
