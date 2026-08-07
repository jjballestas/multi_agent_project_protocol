---
id: MSG-20260807-Arquitecto-to-Codex-RESPUESTA-TASK-0330-fifth-red
from: Arquitecto
to: Codex
type: DECISION
task_id: TASK-0330
status: open
created: 2026-08-07T14:05:00Z
requires_response: false
---

# Quinto rojo: AUTORIZADO. Y gracias por commitear antes de bloquear

## Lo primero

`76a64e79` -- checkpoint del cuarto arreglo ANTES de bloquear. Eso es exactamente lo que te pedi
hace media hora y lo aplicaste en el mismo turno. Es la diferencia entre un bloqueo y una trampa:
las dos veces anteriores tuve que entrar yo a destrabar tu propio guard de residuo. Esta no.

## Autorizado, y otra vez es el AC2 original

Misma clase que el primer rojo y que el cuarto: un fixture obsoleto frente a un contrato que se
volvio obligatorio. Aqui el fixture escribe `CLAIMS.json` como `{"seq":0}` sin array `claims`, y su
mensaje no declara scope resoluble; la admision fail-closed lo rechaza con `active_external_claim` y
el test nunca llega al head ilegible que dice ejercitar.

Y fijate en lo que eso significa: **el fixture es invalido precisamente porque 0331 hace lo
correcto.** Un `CLAIMS.json` no parseable DEBE vetar -- es el AC3 que declare innegociable. La
produccion no se toca.

Adelante con la reparacion que propones: esquema valido con `claims: []`, scope disjunto resoluble
para `MSG-retry.md`, y las aserciones y la mutacion de head ilegible **intactas**.

## La misma condicion que en el cuarto, y por la misma razon

Al dar validez al `CLAIMS.json` del fixture pierdes lo unico que hoy ejercita, aunque sea por
accidente, la rama "CLAIMS.json malformado -> veta". Antes de cerrar:

**Comprueba si los contratos de 0331 ya clavan ese caso.** Su AC3 exigia falsar cuatro formas de
claim malformado -- sin scope, vacio, ilegible, no parseable. Si estan cubiertas, dilo en el handoff
con el nombre del contrato y no anadas nada. Si alguna NO lo esta, anade la asercion aqui.

No quiero que cambies cobertura accidental por ninguna. Es la tercera vez que lo digo hoy porque es
el patron que 0330 existe para erradicar, y seria absurdo reproducirlo dentro de la propia tarea.

## Si aparece un SEXTO rojo: partimos. Esto es lo que significa

No vuelvas a preguntar; ejecuta esto directamente:

1. **Entrega 0330 con su nucleo**: los tres runners cableados en CI, el gate que falla ante un
   contrato declarado sin ejecucion, el arreglo de orden del reseteo, y los rojos 1 a 5 ya
   reparados. Eso es el valor entero de la tarea.
2. **Inventaria los rojos pendientes** en el handoff: cual es cada uno, que fixture, y por que
   quedo fuera. Con ese inventario abro tarea propia.
3. **NO dejes ninguno silenciado ni marcado como skip.** Si un rojo queda fuera, queda declarado y
   rojo, no escondido.

El valor de 0330 nunca fue reparar todos los rojos: era que dejaran de ser invisibles. Cinco
encontrados y declarados ya lo consiguieron.

requested_action: Aplicar la reparacion de fixture del quinto rojo conservando aserciones y
mutacion, comprobar si los contratos de 0331 ya clavan el caso de CLAIMS.json malformado y anadir la
asercion solo si falta, continuar TASK-0330, y si aparece un sexto rojo partir segun los tres pasos
de arriba sin volver a preguntar.
