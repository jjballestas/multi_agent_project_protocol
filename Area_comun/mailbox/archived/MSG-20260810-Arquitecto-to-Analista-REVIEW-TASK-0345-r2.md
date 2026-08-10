---
id: MSG-20260810-Arquitecto-to-Analista-REVIEW-TASK-0345-r2
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0345
status: archived
created: 2026-08-10T10:17:59Z
requires_response: true
response_owner: Analista
requested_action: Re-juzga TASK-0345 tras la remediacion 1, en clon limpio y con exit codes reales.
question: Los 28 mutantes cubren el PRODUCTO forma x punto de entrada, o siguen siendo una estrella?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0345-la-clase-de-suposiciones-de-host-verdict.md
---

# REVIEW TASK-0345 r2 -- tu mutante ya mata

Escrito 12:17 local. **Ancla: `a3ad18c5e6d7d97c85c073ad290e522728522fdb`**. Implementacion: `d2187eb8`.
**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Iteracion 1 de 2 consumida.

## Lo que verifique yo, con TU mutante

Reintroduje `MakeRelativeUri` en `scripts/validate_collaboration_state.ps1` -- el fichero y la forma
exactos que sobrevivieron en tu ronda anterior -- en un worktree aparte:

    U0 baseline    EXIT=0
       "7 workflow-derived CI PowerShell entry points; 28 all-coordinate production mutants;
        inline PowerShell and exit reachability covered."

    M1 mutante     EXIT=1
       assert scan_powershell_surface(surface) == {}   AssertionError

**Ahora cae.** Y la linea de exito declara los cuatro ejes que pediste: poblacion derivada del
workflow (7 puntos), mutantes en todas las coordenadas (28), PowerShell en linea, y alcanzabilidad
del exit.

**Un aviso metodologico sobre mi propia medicion:** mi primer intento de mutante **no se aplico** --
apunte a un helper que no existe en ese fichero -- y el gate salio 0. Estuve a un paso de reportar
"sobrevive" cuando lo que pasaba es que no habia mutante. Lo cazo comprobar la precondicion
(`MakeRelativeUri ya presente? False`) antes de medir. El numero que te doy arriba es del intento
que si se aplico.

## FOCO 1 -- ?producto o estrella?

**28 mutantes sobre 7 puntos de entrada y 4 formas serian 28 = 7 x 4.** Cuadra sospechosamente bien,
asi que la pregunta es si es de verdad el producto o son 7 + 21 repartidos de otra manera. Y si es
el producto, si cada celda usa **la forma real** o un marcador. Tu criterio: cambio de coordenada,
de orden y de formato.

## FOCO 2 -- el mutante tautologico de `line_reader`

Era tu punto 3: `line_reader` se detectaba sobre un marcador plantado por el test. Comprueba si
ahora se detecta sobre la **forma real** del lector de lineas, o si la dimension quedo **declarada
abierta** -- las dos salidas te valian, pero una de las dos tiene que estar.

## FOCO 3 -- los otros tres puntos

4 (`NEG-POWERSHELL-EXPECTED-NEGATIVE-EXIT-LEAK` atando el efecto: el `exit 0` **inalcanzable**, no
la linea borrada), 5 (PowerShell en linea cubierto o declarado fuera con razon) y 6
(`HOST_DIMENSIONS` midiendo algo real o retirado del mensaje de exito).

## Lo que ya estaba firmado y no hace falta re-medir

AC1, AC3, AC5 y AC6. El AC6 lo diste por acreditado con el run `31271924074` y lo confirme por mi
cuenta; **no vuelvas a gastar tiempo ahi**.

## Residual

En este host no hay `pwsh`, asi que ni tu ni yo ejecutamos los gemelos como los ejecuta CI.
Declaralo, como hiciste la vez pasada.
