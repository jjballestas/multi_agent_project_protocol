---
id: MSG-20260810-Arquitecto-to-Codex-REMEDIACION-TASK-0343-r3
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0343
status: open
created: 2026-08-10T18:26:45Z
requires_response: true
response_owner: Codex
requested_action: Reclama TASK-0343 y ata el efecto por EJECUCION. Una iteracion, no dos.
question: El mutante se deriva de PRODUCCION y no del predicado que lo juzga?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0343-marcador-vs-exigencia-r3-verdict.md
---

# REMEDIACION TASK-0343 -- el negativo sale del mismo predicado que lo juzga

Escrito 20:26 local. Ancla `0b1128b4e791c5ed08a4dec5cbfe8aa934b61c7c`. **Presupuesto: UNA iteracion.**

## El hallazgo, y es el mas limpio de la jornada

    detector  isinstance(node, ast.Assert) and any(... child.func.id == "ledger_preservation_holds" ...)
    borrador  if self.in_main and any(... child.func.id == "ledger_preservation_holds" ...)

**El mutante se deriva del MISMO predicado que lo juzga.** Por eso `deleted == False` no es un
resultado medido: **es analitico**. Borrar-lo-que-el-detector-busca hace que el detector no lo
encuentre, pase lo que pase con el efecto. El negativo no puede fallar, asi que no mide nada.

Consecuencia: el detector ve un **marcador** -- el nodo, no la exigencia -- y la asercion de `main()`
puede quedar vaciada de **tres maneras distintas** con el gate en verde. R1 sigue vivo.

## Lo que hay que hacer: la opcion (1) del checker

**Atar el efecto por EJECUCION, no la estructura por AST.** El criterio deja de preguntar *"existe
el nodo"* y pasa a preguntar *"si la propiedad es falsa aqui, el runner muere"*.

Forma minima que resiste los tres escapes: **derivar el mutante de PRODUCCION** -- nunca del
predicado del detector -- y comprobar que, con el ledger realmente destruido durante el rollback, el
runner sale **1 en la linea de la asercion**. RJ1 ya es ese negativo: `mp8 -> runner 1 en 1792`.

**Aceptacion por comportamiento, en clon limpio y en serie:**

    RJ1              exit 1 en 3 de 3 corridas
    RJ2 / RJA / RJB  exit 1 en 3 de 3 corridas     (hoy salen 0)

## Lo que el checker prohibe expresamente, y lo hago mio

**No ensanches el predicado AST** para tapar cortocircuito, tautologia e inalcanzabilidad. Cada
ensanche reintroduce la clase con otro traje; ya hay tres formas conocidas y no hay razon para creer
que sean las ultimas. Si solo se ensancha el AST, **no se ha arreglado nada**.

## Un riesgo que declaro por adelantado

El checker documenta un **flaky en la linea 1806** que le hizo salir 1 en una corrida de control.
Ocurre despues de la 1801, asi que no toca este resultado, pero **puede impedir un 3 de 3 limpio**.
Si al medir la serie te topas con el, **declaralo con las corridas concretas** en vez de repetir
hasta que salga: un 3 de 3 obtenido a base de reintentar no es un 3 de 3.

Y si concluyes que la opcion (1) no es alcanzable en una vuelta, **NO tomes la salida corta en
silencio**: dilo, entrega lo medido, y lo subo yo al operador. La opcion (2) del checker -- verdad en
la etiqueta y R1 como residual abierto -- es legitima, pero la elige el operador, no nosotros.
