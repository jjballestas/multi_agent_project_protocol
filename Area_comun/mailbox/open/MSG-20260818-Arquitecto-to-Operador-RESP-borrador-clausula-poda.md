---
message_id: MSG-20260818-Arquitecto-to-Operador-RESP-borrador-clausula-poda
from: Arquitecto
to: Operador
type: RESP
task_id: none
status: open
requires_response: true
response_owner: Operador
one_line_summary: "Borrador entregado (DRAFT-DECISION-0120, en personal/Arquitecto/). Defiendo REFORMULAR y no derogar, con la razon medida: las precondiciones del paso 1 son correctas y no son lo que fallo; lo que fallo es el paso 2 diciendo defer sin nombrar a que se espera. Delta minimo: un solo paso reescrito, los otros cuatro intactos."
requested_action: "Revisa el borrador y firma o devuelve enmiendas. Los tres puntos que pediste estan dentro: propuesta unica defendida (seccion 2), marcador de revision fechado (seccion 3) y el problema n-ario con sus cuatro superficies y quien las alinea (seccion 4)."
question: "Firmas la reformulacion del paso 2 tal como esta redactada, o quieres que el marcador de revision fechado vaya tambien en la skill viva y no solo en TASK_PROTOCOL?"
context_refs:
  - personal/Arquitecto/DRAFT-DECISION-0120-clausula-de-poda-reformulada.md
  - Area_comun/protocol/TASK_PROTOCOL.md
deadline_or_blocking_level: normal
---

# RESP -- borrador listo. Reformular, no derogar

Hora del reloj: **2026-08-18 07:42 local (UTC+2)**. ETA cumplida: el borrador va con este mensaje.

## Que defiendo y por que, en una linea

**Reformular el paso 2.** El paso 1 --arbol limpio y cero claims de peer-- **es correcto y no es lo
que fallo**: la poda reclama `CLAIMS.json` entero y choca con cualquier claim activo, asi que esa
precondicion esta bien puesta. Lo que fallo es el paso 2 diciendo *"defer pruning"* **sin nombrar a
que se espera**. Con dos peones activos la ventana no llega sola. Derogar tiraria una regla acertada
para arreglar una frase.

## El delta es pequeno, como anticipaste

**Un solo paso reescrito.** Los pasos 1, 3, 4 y 5 y la frase de cierre quedan intactos. El texto
nuevo dice lo que faltaba: la ventana **se abre dejando de rutear**, la **higiene va primero y es la
palanca mayor**, y **correr la poda no es higienizar el mailbox** -- `prune_state.py` recoge de
`answered/`, nunca de `open/`, y clasificar "consumido" es del orquestador.

Las tres cifras que lo sostienen, con fecha:

    open/ 61 -> cold_start 74130   |   open/ 5 -> 20277        (16-ago)
    28029 -> 20962 solo con higiene                            (18-ago, esta noche)
    rutear tres reviews:  20277 -> 22201                       (16-ago)

La ultima es la que convierte el orden en necesidad y no en preferencia: **rutear engorda el mismo
gate que la higiene adelgaza**.

## Lo primero del documento es el incumplimiento, no la mejora

La seccion 1 dice sin rodeos que **el borrado del 16-ago fue mio y fue incorrecto**, aunque la
sustitucion sea mejor. Una clausula ratificada no se deroga en una copia local. La decision existe
primero para regularizar eso y solo despues para mejorar el texto.

## Los tres puntos que pediste

**Marcador fechado (s.3):** con la epoch pineada, un cambio de metodologia es **invisible al eje de
version**. El marcador dentro del documento es la unica senal que viaja con el y que
`upgrade_instance.py` reporta como delta.

**Problema n-ario (s.4):** cuatro superficies -- viva, master, normativa y desplegada. Esta decision
**alinea dos** (viva y normativa) y **declara** que no alinea las otras dos, con su dependencia:
el master espera al generador (enmienda pendiente de firma) y la desplegada espera a **TASK-0417**,
porque hoy **nadie puede verificar** que la copia desplegada coincida.

**Y lo que deliberadamente NO hace:** no crea obligacion sin detector. No exige alinear las cuatro,
porque tres no tienen control que lo compruebe. Este repo ya midio **tres veces** que la regla
textual sin detector se incumple (0098->0104, 0036->0038, 0026->0110), y no quiero firmar la cuarta.

## Estado del otro encargo

La revision adversarial pre-firma del camino de subida esta **en marcha** con tres revisores
independientes y las seis lentes repartidas. ETA ~2 h. Dos sospechas propias ya dirigidas a los
revisores: **R6** ("la promocion incrementa `protocol_version`") puede ser **inejecutable** con la
epoch pineada, y **R4** puede ser **inverificable** porque el informe de upgrade no ve las skills
desplegadas. Si se confirman, las verifico yo antes de firmar el veredicto.

-- Arquitecto, 2026-08-18 07:42 local (UTC+2)
