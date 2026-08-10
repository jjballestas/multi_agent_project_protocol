---
id: TASK-0345
title: Los gemelos PowerShell asumen el host Windows y nadie los ejecuta en Linux hasta que CI falla
status: done
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

## Remediacion AC4 -- iteracion 2

El inventario ejecutable ya no es una constante paralela. `workflow_powershell_surface()` parsea
el workflow, resuelve el shell efectivo de cada step y deriva los siete `.ps1` que CI evalua como
PowerShell. Tambien deriva los comandos PowerShell en linea: hoy existe uno que solo invoca Python,
pero un step nuevo con codigo en linea entra en el mismo escaneo. El mutante en linea que introduce
`MakeRelativeUri` muere, por lo que ese eje queda cubierto y no declarado fuera de alcance.

`HOST_DIMENSIONS` se retiro. El mensaje de exito ya no anuncia cinco dimensiones decorativas: informa
la poblacion derivada, 28 mutantes de produccion y las dos propiedades adicionales que realmente
mide. Los 28 mutantes son las cuatro formas PowerShell host-dependientes aplicadas a cada uno de los
siete puntos derivados, con variacion de espaciado y orden. Incluyen `MakeRelativeUri`, un separador
literal usado como frontera, una comparacion de path fijada a `OrdinalIgnoreCase` y el lector real
`Get-Content` sin `-Raw`; no usan marcadores sinteticos. La unica ocurrencia admitida del lector real
queda limitada estructuralmente a una en `scan_domain_neutrality.ps1`, bajo el owner TASK-0338.

**CORREGIDO 2026-08-10 tras el re-juicio r2.** La frase que ocupaba este lugar -- *"una segunda
ocurrencia en esa ruta o la primera en cualquier otra ruta derivada hace fallar el contrato"* -- era
**FALSA**, y el checker la falso ejecutando: la deteccion esta atada al NOMBRE de la variable
receptora, no a la forma. Medido:

    $lines = @(Get-Content -Path $file.Path -Encoding UTF8)   ->  {'unbounded_line_reader'}
    $rows  = @(Get-Content -Path $file.Path -Encoding UTF8)   ->  set()

Mismo lector real, misma dimension, una renombrada de distancia. La afirmacion se retira en vez de
matizarse: una tarea cerrada no puede conservar una promesa que su propio gate no cumple.

La forma Bash sigue fuera del alcance de implementacion de TASK-0345 y bajo TASK-0336, pero su
mutante se construye sobre el lector real de produccion y se acredita sin marcador tautologico. No
se modifica ni se redefine el contrato de TASK-0336.

`NEG-POWERSHELL-EXPECTED-NEGATIVE-EXIT-LEAK` ahora inspecciona control de flujo superior: exige que
el primer `exit` top-level alcanzable sea `exit 0`. Su mutante inserta `exit $LASTEXITCODE` justo
antes del success final, deja ese `exit 0` inalcanzable y muere. Ya no se acredita por los ultimos
siete caracteres del fichero.

AC6 permanece acreditado por el run historico `31271924074`, job `powershell-linux-parity` success,
head `50ce23010d83af5ca3c8c5f0433b2f18288eb0a8`. La facturacion impide lanzar runs nuevos, no leer
esa evidencia ya existente; no se declara AC6 pendiente.

## Residual declarado al cerrar (2026-08-10, decision del operador)

TASK-0345 se cierra **con residual declarado**, no como clase cerrada. Lo que SI logro, medido y
firmado por el checker:

- **Poblacion derivada**: 7 puntos de entrada PowerShell obtenidos del workflow, no de una lista.
- **Producto real sobre ese eje**: 28 celdas = 7 puntos x 4 formas, cada una con su assert, con la
  forma real y variando formato y orden. Los tres negativos minimos del checker mueren.
- **Mutante tautologico retirado**: `line_reader` se detecta sobre la forma real, no sobre un
  marcador plantado por el test.
- **`exit 0` inalcanzable** ya se caza; PowerShell en linea cubierto.
- **AC1, AC3, AC5 y AC6 acreditados**, el AC6 con el run real `31271924074`
  (`powershell-linux-parity` success), confirmado por el Arquitecto por separado.

**Lo que queda ABIERTO y por que no se persigue aqui:**

1. **El eje de la FORMA sigue siendo una enumeracion.** Las cuatro formas son reconocedores
   enumerados -- regex de forma de llamada, mejor que literales, pero lista al fin --. **La quinta
   grafia de esas mismas cuatro dimensiones entra sin tocar el gate.**
2. **Los detectores se atan a coordenadas incidentales**: el nombre de la variable receptora y la
   disposicion de la sentencia (`if (...) { exit $LASTEXITCODE }` en una sola linea escapa al modelo
   de profundidad de llaves).

**Razon del cierre:** este eje **no se cierra enumerando**. Cada vuelta produce la grafia siguiente
-- van dos y el checker predijo la tercera --. Cerrarlo de verdad exige reconocer PowerShell por
**estructura** y no por texto, que es un mecanismo distinto y una tarea propia: **TASK-0355**.
Seguir aqui seria exactamente el patron que esta instancia lleva ocho cadenas documentando.
