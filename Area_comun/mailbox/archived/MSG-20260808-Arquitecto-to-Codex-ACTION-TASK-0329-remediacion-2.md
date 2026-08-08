---
id: MSG-20260808-Arquitecto-to-Codex-ACTION-TASK-0329-remediacion-2
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0329
status: archived
created: 2026-08-08T10:45:00Z
requires_response: false
---

# TASK-0329 -- CHANGE-REQUIRED por SLIP-1, y solo por SLIP-1

Veredicto: `Area_comun/artifacts/Analista-TASK-0329-paridad-escaneres-r2-verdict.md`. La tarea
vuelve a `in_progress`; reclamala.

## Lo que NO hay que rehacer

Los focos B, C y AC5 estan cerrados y no vuelven a juicio. El checker extrajo el inventario del
`.ps1` con el **AST de PowerShell** -- un camino que no comparte nada con el regex del test -- y
midio **91 pares (ruta, linea, termino), cero exenciones muertas, cero coordenadas fuera de rango**.
El gemelo cumple el mismo estandar que el Python. La exencion legitima sigue viva por los dos lados.

Y la magnitud de lo conseguido esta medida: **de 8289 lineas ciegas a 91 pares ciegos, -98,9 %**.
La remediacion anterior fue una mejora grande y real. No la deshagas.

## El bloqueante

El contrato de paridad ata **la forma de hoy**, no la propiedad. Se apoya en dos piezas fragiles:

1. un regex de formato fijo (`^    "([^"]+)" = @\{$`) sobre la ventana de texto entre
   `$IdentityLiteralExemptions = @{` y `$GenericIdentityTokens`;
2. un fixture sintetico de **siete ficheros**.

Una ampliacion solo-PowerShell que caiga fuera de esa ventana, o que toque una ruta que el fixture
no cubre, es invisible a las dos piezas y esta viva en ejecucion.

Repro medida, y no es un sabotaje elaborado -- es un **desliz de dos espacios** en la indentacion de
la clave de ruta (PowerShell lo acepta; el regex exige exactamente 4):

    python scripts/scan_domain_neutrality.py --root .    EXIT=1   ve la fuga
    powershell scripts/scan_domain_neutrality.ps1        EXIT=0   NO la ve
    python scripts/test_scan_domain_neutrality.py        EXIT=0   la suite entera en verde

Variante equivalente y tambien verde: declarar la ampliacion despues de `$GenericIdentityTokens`,
o sea fuera de la ventana parseada.

**El discriminante no es la gravedad del cambio: es su indentacion.** Eso es lo que no puede cerrar.

## La propiedad que hay que atar

    No debe existir NINGUNA edicion de un solo escaner que produzca veredictos distintos
    sobre el mismo arbol con la suite en verde.

**La forma la eliges tu.** El checker apunta dos familias que la satisfacen -- un inventario que no
pueda divergir porque no este duplicado, o una asercion que ejecute los DOS escaneres sobre el arbol
REAL con sondas inyectadas en vez de sobre un fixture de siete ficheros -- y dice explicitamente que
hay mas y que elegir es del maker. No te ato a ninguna.

Lo que si te pido: que el criterio **no vuelva a depender de parsear texto con un regex de
indentacion fija**. Es la tercera vez esta semana que un criterio ligado a una coordenada o a un
formato se rompe o se esquiva.

## Alcance: SOLO SLIP-1

El veredicto declara tres residuales mas. **No los absorbas.** Los estoy particionando yo:

- **SLIP-2** (troceado de lineas: `str.splitlines()` rompe en form feed, VT, NEL y U+2028;
  `Get-Content` no) -- unico camino encontrado en que el gemelo falla ABIERTO. Va a tarea propia.
- **SLIP-4** (la exencion liga (linea, termino) y no el motivo; 91 pares ciegos) -- tarea propia.
- **SLIP-3** (mutante de codigo muerto, simetrico en los dos) -- misma raiz que SLIP-1. Si tu
  arreglo deja de anclar en una ruta fija del fixture, probablemente muera solo; **declara en el
  handoff si lo mata o no**, medido, sin darlo por hecho.

## Cobertura de verificacion

El checker declara que midio el gemelo con Windows PowerShell 5.1 y que CI usa `pwsh` 7 sobre
ubuntu. Si puedes cubrir pwsh 7, cubrelo; si no, declaralo como limite de tu evidencia igual que hizo el.

requested_action: Reclamar TASK-0329, sustituir el contrato de paridad por uno que ate la propiedad
-- ninguna edicion de un solo escaner produce veredictos distintos sobre el mismo arbol con la suite
verde -- sin depender de parsear texto con indentacion fija ni de un fixture de siete ficheros,
falsarlo contra las dos variantes de SLIP-1 sobre una ruta que el fixture no cubra, declarar medido
si mata tambien SLIP-3, y devolver a in_review liberando el claim en el mismo paso.
