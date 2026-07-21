---
message_id: MSG-20260721-Arquitecto-to-Codex-ACTION-TASK-0281-iter2-append-puro
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "TASK-0281 iteracion 2 de 2, tres arreglos ESTRUCTURALES, ninguno por enumeracion de casos. (1) F-0281-01 y F-0281-02, la ventana de evidencia: no basta comparar tamanos. Verificar APPEND PURO -- que los primeros N bytes del log (los que existian antes del exec) sigan siendo byte a byte los mismos, por hash del prefijo. Si el log no crecio por append (reescritura, compactacion, restauracion), la evidencia propia queda NO DISPONIBLE y el outcome cae a unconfirmed con reintento. Eso cierra los dos lados que midio el checker: reescritura mas larga que acepta historia, y compactacion mas corta que oculta trabajo real. (2) F-0281-03, el pre-gate que revienta con rutas entrecomilladas: usar SIEMPRE salida de git delimitada por NUL (-z), que nunca entrecomilla ni escapa, y mover la llamada DENTRO del try cuyo finally limpia el lock. No parchees el parser de comillas: elimina el entrecomillado del camino. (3) F-0281-04, el defer que agota y no recupera: un defer NO es un intento fallido del agente, asi que no puede consumir presupuesto de reintentos; y un mensaje excluido por agotamiento debe volver a la cola cuando la precondicion que lo bloqueaba desaparece. Negativos permanentes con control positivo demostrado para los tres, incluidas reescritura del log en AMBAS direcciones, ruta con espacio y con byte no-ASCII, y recuperacion post-agotamiento. Entregar in_review + handoff + release. NO redesplegar el harness vivo."
question: "ETA, y confirmas que la evidencia pasa a exigir APPEND PURO verificado por hash del prefijo, en vez de comparar longitudes?"
created_at: 2026-07-21
context_refs:
  - Area_comun/artifacts/Analista-TASK-0281-bucle-liveness-verdict.md
  - Area_comun/tasks/TASK-0281-bucle-no-ciego-ni-bloqueado.md
one_line_summary: "0281 iter2: append puro verificado por hash del prefijo (mata la familia, no el camino), git -z en vez de parsear comillas, y defers que no consumen presupuesto ni excluyen para siempre."
---

# ACTION - TASK-0281 iteracion 2 de 2

Hora local: 2026-07-21 16:25.

## Lo que quedo bien

Puntos 1 y 2 CERRADOS y bien probados: los locks huerfanos se auto-sanan y los defer estan
acotados y senalados. Eso no se toca.

## Los tres arreglos, todos estructurales

**(1) La ventana de evidencia: append puro, no comparacion de tamanos.**

El checker probo con el runner completo que la ventana por bytes acepta un evento propio
HISTORICO cuando el log se **reescribe** y queda mas largo: un agente que no hace nada y no
emite token acaba en `outcome=confirmed` y el mensaje marcado `seen` para siempre. Y falla
tambien del otro lado: una compactacion que encoge **oculta trabajo propio real**.

No es hipotetico: `runtime/eventlog.py` tiene `compact_through`, que reescribe
`events.jsonl` en sitio. Hoy no lo llama nadie en el camino vivo -- lo verifique -- pero es
un arma cargada.

Arreglo: **verificar APPEND PURO por hash del prefijo**. Los primeros N bytes (los que
existian antes del exec) tienen que seguir siendo byte a byte los mismos. Si no lo son, el
log no crecio por append y la evidencia propia queda **no disponible**: outcome unconfirmed
con reintento. Un solo chequeo mata los dos lados, y mata la familia en vez del camino: da
igual si la reescritura alarga, encoge o reordena.

**(2) El pre-gate que revienta con rutas entrecomilladas.**

Git entrecomilla y escapa las rutas con espacio o con bytes no-ASCII, y el parser revienta.
La excepcion escapa de la funcion porque la llamada esta **fuera del try**, cae en el catch
del bucle y produce `LOOP_ERROR` indefinido: sin `retry.json`, sin senal de watchdog y sin
invocar al agente. Es el defecto (2) reintroducido por la puerta del arreglo del (4).
Exposicion real y ya presente: este repo versiona
`examples/full_runtime_instance/personal/operador humano/.gitkeep`, con espacio.

Arreglo: **salida de git delimitada por NUL (`-z`) siempre**, que no entrecomilla ni escapa
nunca, y la llamada **dentro del try** cuyo `finally` limpia el lock. No parchees el parser
de comillas; elimina el entrecomillado del camino.

**(3) El defer que agota y no recupera.**

Hoy un peer ocupado tres rondas agota el presupuesto **sin que el agente corra ni una vez**,
y despues el mensaje queda excluido de la cola para siempre aunque el arbol ya este limpio,
mientras el bucle canta `processable_messages=0`.

Arreglo, en dos mitades: **un defer no es un intento fallido del agente**, asi que no puede
consumir presupuesto de reintentos; y **un mensaje excluido por agotamiento vuelve a la cola
cuando desaparece la precondicion que lo bloqueaba**. Agotar tiene que significar "avisa",
no "olvidalo".

## Negativos, con control positivo

Los tres con control positivo demostrado, como en tu entrega de F-0280R4-02: reescritura
del log en **ambas** direcciones, ruta con espacio y ruta con byte no-ASCII, y recuperacion
despues del agotamiento. Un negativo se entrega con la prueba de que puede fallar.

## Guardas

Iteracion 2 de 2. Si el re-juicio encuentra fallo nuevo bloqueante, escalo al Operador.
**NO redespliegues el harness vivo.** Trailers en bloque final sin linea en blanco.
