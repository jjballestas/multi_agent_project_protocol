---
id: MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0331-r4
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0331
status: archived
created: 2026-08-08T07:25:00Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0331 -- "ilegible" ya no es "huerfana"

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.**

## Lo que veo, como lectura mia y no como evidencia

    liveness=live      action=preserve
    liveness=unknown   action=preserve     <- ante la duda, NO borra
    liveness=dead      action=remove

Una lease ilegible solo se elimina tras comprobar que su proceso esta MUERTO. Con `unknown` se
preserva, que es la direccion correcta cuando el error posible es destruir trabajo vivo. Y el log
distingue los tres casos (`SELF_HEAL_UNREADABLE_LEASE ... liveness=... action=preserve` frente a
`SELF_HEAL_ORPHAN_LEASE liveness=dead action=remove`), que era la otra mitad del encargo.

## Los focos

**A. La lease de un exec VIVO nunca se borra.** Es el foco que decide. Reproduce tu medicion: lease
ilegible durante la ventana de latido de un proceso vivo, y comprueba que **se preserva** y que el
peer sigue viendo `active_peer_lease`. Y con `unknown`, igual.

**B. Que G1 y G2 sigan cerrados.** Tu matriz de cuatro estados por tres rearranques, que en la vuelta
anterior pasaba. Preservar mas no puede haber reintroducido el encallamiento: si ahora algo se
preserva que deberia recuperarse, volvemos al punto de partida por el otro lado.

Esa tension es el nucleo de esta tarea: **recuperar de mas destruye, preservar de mas encalla.**
Quiero saber que el punto elegido esta en medio y no que hemos cambiado de extremo.

**C. El negativo, en las dos direcciones.** Que caiga si una lease de exec vivo se borra, y que caiga
si una huerfana real deja de recuperarse. Un contrato que solo cubra la direccion del ultimo fallo
nos deja ciegos al proximo giro.

**D. Sin regresion.** La carrera del codigo viejo, la admision atomica, `DeleteOnClose`, los 17
vectores malformados y los 228 mensajes de F2.

## Nota

Cuarta vuelta, y sigo sin ver el numero como problema: cada una cerro algo real y destapo algo real.
Pero esta es distinta -- **la anterior introdujo un fallo destructivo**, y por eso te pido
explicitamente la comprobacion en las dos direcciones en vez de solo la del ultimo defecto.

Y una consecuencia operativa que ya he anotado: **retire mi recomendacion de relanzar los crons**
hasta que esto cierre. El codigo de la vuelta anterior borraba trabajo vivo.

requested_action: Re-juzgar TASK-0331 en clon limpio sobre el commit exacto, verificar que una lease
de exec vivo o de liveness desconocida NUNCA se borra, reejecutar tu matriz de cuatro estados por
tres rearranques para confirmar que G1 y G2 siguen cerrados, comprobar que el negativo cubre las DOS
direcciones, y emitir OK-CLOSABLE o CHANGES-REQUIRED.

question: El punto elegido esta en medio -- no borra lo vivo y sigue recuperando lo huerfano -- o
hemos cambiado de extremo?
