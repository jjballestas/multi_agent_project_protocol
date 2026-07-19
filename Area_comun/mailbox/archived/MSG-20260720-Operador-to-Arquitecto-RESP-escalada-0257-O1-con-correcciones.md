---
message_id: MSG-20260720-Operador-to-Arquitecto-RESP-escalada-0257-O1-con-correcciones
from: Operador
to: Arquitecto
type: RESP
status: archived
requires_response: false
created_at: 2026-07-20
context_refs:
  - Area_comun/mailbox/open/MSG-20260719-Arquitecto-to-Operador-ESCALADA-0257-tope-agotado-decision.md
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
one_line_summary: "DECISION del Operador sobre la escalada de TASK-0257: O1 (0257 blocked, residuo a TASK-0267, GO de 0267 YA) con DOS correcciones al texto del cierre -- C1: F-0257-03 se cierra como RESIDUAL ESTRUCTURAL declarado, NO como arreglado por 0267 (un hook borrado no se ejecuta, la materializacion no lo alcanza); C2: unidad nueva que anada al CI la verificacion de existencia y SHA-256 de .githooks/pre-commit, unica capa donde F-0257-03 es cerrable. Ademas un punto a EVALUAR (no decidido): el coste de 42.9 s en ruta gobernada."
---

# RESP - escalada TASK-0257: O1 con dos correcciones

Buen trabajo de los tres en esta tanda. El gate temprano (E2) se pago solo: cazo cinco
defectos reales antes de que se construyera nada encima. Y el STOP al agotarse el tope
salio sin que nadie tuviera que recordarlo. Eso es exactamente lo que la 0103 buscaba.

## Decision: O1

TASK-0257 queda `blocked`. El residuo F-0257-04 se transfiere al acceptance de
TASK-0267 (hook v2 por materializacion del indice) y autorizo su **GO ya**.

Descarto O2. Otra iteracion del mismo enfoque compra el siguiente caso de git, no la
garantia; y el coste ya va por 42.9 s.

## Correccion 1 - F-0257-03 NO lo arregla 0267

El texto de la escalada dice que la materializacion "mata TODOS de raiz", incluido el
hook borrado. Eso no puede ser cierto, y la evidencia es del propio veredicto del
Analista (`D - propio hook | SLIPS`):

`git rm .githooks/pre-commit` **elimina el fichero del arbol de trabajo**. En el commit
siguiente git busca el hook, no lo encuentra y **no ejecuta nada**. Ninguna logica
interna puede intervenir -- ni la materializacion ni ninguna otra -- porque el hook no
llega a correr. No es un caso mas del enumerado de git: es que el juez no existe.

La materializacion SI mata F-0257-01 y F-0257-04 (casos donde el hook si se ejecuta) y
ademas elimina el mutex de H2. Por eso 0267 sigue valiendo la pena y por eso le doy GO.

Pero **F-0257-03 se cierra como RESIDUAL ESTRUCTURAL DECLARADO**, no como defecto que
0267 remedia. Que quede por escrito en el cierre de 0257 y en el acceptance de 0267:
un hook no puede defenderse de su propio borrado. Decirlo vale mas que tres iteraciones
mas intentando lo imposible.

## Correccion 2 - cerrar F-0257-03 donde SI es cerrable

Hallazgo del Asesor, verificado: `.github/workflows/validate.yml` **no menciona
`.githooks` en absoluto**. Sus pasos son validate (Python y PowerShell, hub e instancia)
y el drift de la guia HTML. Es decir: **si alguien borra el hook, hoy no lo detecta nadie
en ninguna capa** -- ni el hook (no corre), ni el CI (no mira).

Unidad nueva (o plegada a 0267 si a tu juicio encaja mejor): **paso de CI que verifique
que `.githooks/pre-commit` existe y que su SHA-256 coincide con el esperado**. El hash ya
esta calculado por el Analista en la prueba de export de los tres tiers:
`3C52D876F4EF6662F5E2C5F1937DF9F6609C05AF5216B1D119081A328C559225`.

Esa es la unica capa donde F-0257-03 es cerrable: en el CI el borrado aparece como diff,
desde clon limpio, y el committer no lo alcanza. Barato y necesario.

Nota de coherencia con la C5: esto refuerza el reparto correcto -- el **hook es la primera
linea** (feedback local rapido) y el **CI es el enforcement duro**. La C5 no muere; se
coloca en su sitio.

## Punto a EVALUAR (no decidido) - el coste

La serie del modo completo fue 11.5-12.9 s -> 29.5 s -> **42.9 s**, y el fix de H2 anadira
coste encima. El modo acotado (0.383 s) funciona y el Analista marco PASA correctamente:
el acceptance pedia modo acotado y existe.

Pero la ruta gobernada es donde este equipo REALMENTE trabaja -- cada mensaje de mailbox,
cada operacion de ledger. Cumple la letra; quiero que evalues si cumple el espiritu.

Concretamente, evalua y reporta (no decidas): si se adopta la lectura de que el hook es
la primera linea y el CI el enforcement, **?sigue justificandose el modo completo de 43 s
en local, o basta el acotado?** Quiero el numero y tu criterio antes de decidirlo yo.

## Ejecucion

- 0257 -> `blocked` con los dos residuales declarados (F-0257-03 estructural, F-0257-04
  transferido).
- 0267 -> **GO**, con F-0257-04 en su acceptance y la nota de que NO cubre F-0257-03.
- Unidad de CI (nueva o plegada a 0267) -> registrala con intake DoR completo.
- 0258 sigue retenida por E1 hasta que el conjunto del harness tenga cierre.
- Guardas de siempre: reservadas N=6 intactas, fondo intocable, sin encender
  supervised_autonomy ni real_invoker.

-- Operador
