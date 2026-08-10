---
id: TASK-0355
title: El eje de la forma no se cierra enumerando -- reconocer PowerShell por estructura y no por texto
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0355-reconocer-powershell-por-estructura-no-por-texto.md
created: 2026-08-10
---

# TASK-0355 -- la quinta grafia siempre entra

Residual declarado al cerrar TASK-0345 por decision del operador el 2026-08-10.

## Lo que quedo abierto, medido

TASK-0345 cerro el eje de la **poblacion**: 7 puntos de entrada derivados del workflow y un producto
real de 28 celdas. **No cerro el eje de la FORMA.** Las cuatro dimensiones se reconocen con cuatro
regex de forma de llamada, y la quinta grafia de esas mismas dimensiones entra sin tocar el gate.

Peor: los detectores quedaron atados a **coordenadas incidentales**. Dos escapes medidos:

    $lines = @(Get-Content -Path $file.Path -Encoding UTF8)   ->  {'unbounded_line_reader'}
    $rows  = @(Get-Content -Path $file.Path -Encoding UTF8)   ->  set()

    runner_reaches_success_exit(<... exit $LASTEXITCODE ... exit 0>)                 -> False  (muere)
    runner_reaches_success_exit(<... if ($x -ne 0) { exit $LASTEXITCODE } ... exit 0>) -> True   (ESCAPA)

El primero es una renombrada de variable. El segundo, una llave en la misma linea.

## Por que es tarea aparte y no una vuelta mas de 0345

Porque **el mecanismo es distinto**. Reconocer por texto -- por muy buena que sea la regex -- ata la
grafia, no la construccion. Van dos vueltas y el checker predijo la tercera: *"si la respuesta es
anadir dos formas mas, vuelvo a fallar"*. Cerrar la clase exige reconocer PowerShell por
**estructura**: un parser, un AST, o el propio motor de PowerShell como oraculo.

## Lo que tendria que sostener

1. El reconocimiento no depende del **nombre** de ninguna variable, del **espaciado**, del **orden**
   de parametros ni de la **disposicion** de la sentencia en lineas.
2. Se falsa con los dos escapes de arriba y con un tercero que el maker construya y declare.
3. Si la ruta elegida es usar PowerShell como oraculo, se declara la dependencia de host y que pasa
   donde no hay `pwsh` -- hoy este host no lo tiene.
4. Si se concluye que el coste no lo justifica, **la conclusion se escribe**: el eje de la forma
   queda cubierto por enumeracion, con su lista visible y su fecha, y nadie vuelve a afirmar que el
   contrato cierra la clase.

Fuera de alcance: la poblacion de puntos de entrada, ya derivada y cerrada en TASK-0345.
