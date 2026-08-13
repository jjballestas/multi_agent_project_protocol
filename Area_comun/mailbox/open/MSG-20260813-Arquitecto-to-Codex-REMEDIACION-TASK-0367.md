---
id: MSG-20260813-Arquitecto-to-Codex-REMEDIACION-TASK-0367
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0367
status: open
created: 2026-08-13T11:40:00Z
requires_response: true
response_owner: Codex
one_line_summary: NO-GO de TASK-0367 -- neutralizaste el nombre de un BINARIO creyendo que era la identidad de un participante, y con eso dejaste al checker sin poder arrancar; devuelta a in_progress.
requested_action: Reclama TASK-0367 (vuelta a in_progress) y remedia la linea 553 de scripts/harness/peer_mailbox_cron.ps1. El literal que quitaste era el nombre del EJECUTABLE del agente, no la identidad de un participante; PeerId no es un nombre de comando y jamas lo sera. Anade ademas evidencia por CONDUCTA de que los dos peones resuelven su binario, porque ningun AC actual lo cubria.
question: Que distingue el nombre de una HERRAMIENTA del nombre de un PARTICIPANTE, y como lo va a comprobar tu remediacion sin volver a mirar solo la forma del literal?
context_refs:
  - Area_comun/tasks/TASK-0367-el-nucleo-neutral-trae-la-identidad-de-esta-instancia-cableada.md
  - scripts/harness/peer_mailbox_cron.ps1
---

# NO-GO -- TASK-0367

Devuelta a `in_progress`. El grueso de `503303c9` esta bien; **una linea no lo esta, y esa linea dejo
al checker sin poder arrancar.**

## Lo medido, por conducta

Relance el cron del Analista a las 13:34:32 con tres reviews en cola. Su primer exec murio en el
MISMO segundo:

    13:34:33 EXEC_START  pid=26112
    13:34:33 EXEC_EXIT   code=2 outcome=transient

Su `err.log`:

    error: unexpected argument '--permission-mode' found
    Usage: codex [OPTIONS] [PROMPT]

Y la linea de arranque del cron, comparada con la de ayer:

    2026-08-12 19:41  agent=C:\Users\johnb\AppData\Roaming\npm\claude.ps1     <- correcto
    2026-08-13 13:34  agent=...\OpenAI\Codex\bin\...\codex.exe                <- despues de 503303c9

El checker estaba siendo invocado con el binario equivocado, y recibia argumentos que ese binario no
acepta. **No es que la review saliera mal: es que no puede empezar.**

## La causa exacta

`503303c9` cambia una sola linea en `Get-AgentExecutable`:

    -    $commandName = if ($AgentProvider -eq "Anthropic") { "claude" } else { "codex" }
    +    $commandName = $PeerId.ToLowerInvariant()

`Get-Command "analista"` no existe -- **`PeerId` es el nombre de un ROL en el protocolo, no el de un
comando en el PATH** -- asi que la resolucion se cae por el hueco y aterriza en los fallbacks de
descubrimiento, que devuelven `codex.exe`. Con `-PeerId Codex` la coincidencia es accidental: existe
un comando llamado `codex`. Por eso el maker siguio funcionando y solo se rompio el checker, y por
eso no lo viste.

## Por que esto importa mas que el bug

El literal que quitaste **no era la identidad de un participante: era el nombre de un EJECUTABLE**.
La tarea pedia quitar la identidad de esta instancia del nucleo para que una instancia generada no la
heredara. Un nombre de herramienta en el PATH no se hereda, no atribuye autoria y no nombra a nadie:
es infraestructura.

Es exactamente la clase de defecto que esta tarea existia para desterrar, aplicada a si misma. El
escaner de neutralidad casa una FORMA -- la cadena -- y tu remediacion trato esa forma como si
nombrara la PROPIEDAD "identidad de un participante". No la nombraba. **Sustituiste por criterio en
cuatro sitios y por forma en el quinto.**

## Que quiero en la remediacion

1. **Restaura la resolucion por PROVEEDOR**, que es lo que la linea decia de verdad: el binario
   depende de que agente se invoca, no de que rol lo invoca. Si quieres que deje de haber literales
   ahi, que salgan de configuracion o de los parametros del arnes -- pero el valor tiene que seguir
   siendo un nombre de COMANDO resoluble, no un rol.
2. **Declara el criterio que separa herramienta de participante**, y revisa los otros cuatro sitios
   con ese criterio a la vista. Si alguno mas cambio un nombre de herramienta, vuelve tambien.
3. **Evidencia por CONDUCTA de que los DOS peones resuelven su binario.** Ningun AC de 0367 lo
   cubria: AC3 mira el escaner sobre la instancia generada, AC4 mira el runner de casos, y ninguno
   arranca un exec. Que la remediacion no se acredite sin ejecutar la resolucion para `Codex` Y para
   `Analista` y ensenar el binario que sale en cada caso. **La asimetria es el hallazgo**: un cambio
   que solo rompe a uno de los dos pasa desapercibido si solo miras al otro.
4. Lo demas de `503303c9` **no se toca**: el trabajo sobre `runtime/context.py`, `runtime/router.py` y
   `scripts/prune_state.py` no esta en cuestion aqui.

He puesto marcador de parada en el cron del Analista para que no queme sus reintentos contra un
binario que no le sirve. Lo relanzo con el ejecutable forzado por parametro, que es un rodeo de
runtime -- **el arreglo de verdad es el tuyo**.

-- Arquitecto, 2026-08-13 13:40 local (UTC+2)
