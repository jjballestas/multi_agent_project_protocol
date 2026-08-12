---
id: TASK-0366
title: Un mensaje sin tarea numerada no puede reservar ejecucion y muere en silencio a las dos horas
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0366-mensaje-sin-tarea-numerada-muere-en-silencio.md
created: 2026-08-12
intake:
  type: fix
  goal: >
    El arnes de los peones (`scripts/harness/peer_mailbox_cron.ps1`) deriva el alcance de trabajo de
    un mensaje a partir de su `task_id`: `Get-MessageWorkDescriptor` exige la forma `TASK-NNNN`,
    resuelve su fila en el indice y lee los `scope_routes` del fichero de la tarea. Cuando cualquiera
    de esos pasos no da resultado devuelve nulo, y `Acquire-ExecReservation` responde
    `message_scope_ambiguous`: el mensaje se DIFIERE. El diferido no es un fallo visible -- se
    reintenta cada ronda hasta agotar su ventana (7200 s) y entonces el mensaje muere sin haber sido
    leido nunca. Observado en vivo el 2026-08-12 con la review formal de SPEC-MEMORIA-HIBRIDA, que
    llevaba `task_id: none` por ser una review de SPEC y no de tarea: se encolo, se difirio en la
    primera ronda y habria muerto callada. El coordinador no tiene forma de distinguir "el peon esta
    ocupado" de "este mensaje no puede ejecutarse NUNCA", que son estados opuestos: uno se espera y
    el otro se corrige.
  acceptance:
    - "AC1 (los dos estados dejan de ser el mismo): un diferido por causa TRANSITORIA (peer ocupado,
      claim externo vivo, residuo vivo) y un diferido por causa PERMANENTE (el mensaje no puede
      producir descriptor de trabajo por su propia forma) se distinguen en la senal que el arnes
      emite, no solo en el texto de un `reason`. Se acredita con los dos casos corriendo y su salida
      lado a lado."
    - "AC2 (la causa permanente no consume la ventana): un mensaje cuya causa de diferido no puede
      cambiar por espera no se reintenta hasta agotar el reloj. Se acredita midiendo: hoy el mismo
      mensaje consume su ventana entera; despues no. La medicion es de CONDUCTA (rondas consumidas),
      no de lectura del codigo."
    - "AC3 (nadie muere callado): cuando un mensaje se descarta por causa permanente, el hecho llega
      al coordinador por un canal que este lee -- no solo al log del cron. Se acredita provocando el
      descarte y enseniando donde aparece."
    - "AC4 (el criterio, no el caso): la correccion nombra la propiedad `este mensaje no puede
      producir descriptor de trabajo por su forma`, no el caso concreto `task_id: none`. Se acredita
      con las OTRAS formas de la misma clase que hoy caen en el mismo agujero: `task_id` con forma
      valida cuya fila no existe en el indice, fila que apunta a un fichero ausente, y fichero sin
      bloque `scope_routes`. Las cuatro tienen que quedar del mismo lado del criterio."
    - "AC5 (el negativo sigue vivo): un diferido legitimo por causa transitoria sigue difiriendo y
      sigue reintentando como hoy. Un cambio que arregle el caso permanente y ademas deje de esperar
      al peer ocupado no acredita: se mide con el par."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/harness/peer_mailbox_cron.ps1
  out_of_scope:
    - "El guard de residuo que veta sin mirar scope: es TASK-0337, otra causa y otra tarea."
    - "El techo duro que corta entre la entrega y el ledger: es otro frente, no este."
    - "Cambiar la politica de que una review deba ir numerada: la convencion se mantiene; esta tarea
      trata de que su incumplimiento sea RUIDOSO, no de permitirlo."
  risk: low
  estimate: S
---

# TASK-0366 -- el diferido permanente es indistinguible del transitorio

## Como se caza

El 2026-08-12, tras relanzar el cron del checker, su log dio esto en la primera ronda:

    RETRY_DEFER defer=1 attempts=0 elapsed_seconds=0 timeout_seconds=7200
                reason=message_scope_ambiguous
                message=MSG-...-REVIEW-SPEC-MEMORIA-HIBRIDA-formal.md

El mensaje pedia una review de SPEC, no de tarea, y por eso llevaba `task_id: none`. Nada en esa
linea distingue "vuelve dentro de un rato" de "esto no va a poder ejecutarse nunca". La diferencia se
descubrio leyendo el arnes, no observandolo: `Get-MessageWorkDescriptor` devuelve nulo en cuanto el
`task_id` no casa con `^TASK-[0-9]{4}$`, y sin descriptor no hay reserva.

## Por que importa mas de lo que parece

El diferido es el mecanismo de cortesia del arnes: existe para no pisar a un peer ocupado. Al meter
en el mismo cajon una condicion que la espera JAMAS resuelve, el mecanismo se convierte en un
temporizador de olvido. El coordinador ve un peon vivo, un mensaje en `open/` y ningun error -- el
cuadro exacto de "esta trabajando" mientras no trabaja nadie.

Es la misma familia que las lecciones de esta instancia sobre afirmaciones de instrumentos: el
silencio del arnes no es evidencia de progreso.

## Nota de alcance

El caso que lo destapo se corrige por convencion (la review va numerada, TASK-0365). Esta tarea NO
es ese arreglo: es que la proxima vez que alguien encole algo inejecutable, se entere.
