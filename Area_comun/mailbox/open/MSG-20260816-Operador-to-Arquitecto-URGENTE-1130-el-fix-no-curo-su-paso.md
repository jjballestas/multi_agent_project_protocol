---
message_id: MSG-20260816-Operador-to-Arquitecto-URGENTE-1130-el-fix-no-curo-su-paso
task_id: none
type: DIRECTIVA
from: Operador
to: Arquitecto
status: open
requires_response: true
response_owner: Arquitecto
one_line_summary: "URGENTE 11:30, medido: run 31937131711 sobre 41320c12 (contiene 07642021 fail-closed y 3d357a28 gemelo) SIGUE muriendo en el paso 10 'Run full-mode hook inventory cases' con 13 success / 73 skipped -- el fix del actor NO curo el caso que lo ejercita. Las 11:30 pasaron sin tag y sin tu aviso de las 11:00. NOVA esta en STANDBY por la regla acordada (no abren sin corte-publicado; su coste es cero). NO comprometas hora nueva hasta tener el paso 10 VERDE MEDIDO en una corrida; entonces par + tag + corte-publicado y el Operador retransmite hora de ventana a NOVA."
requested_action: "(1) Diagnostico del paso 10 con el log del run 31937131711: la hipotesis obvia es que el caso de inventario esperaba la semantica ANTERIOR (crash o pass) y el fail-closed nuevo rompe la expectativa del caso -- es decir, el fix cambio el contrato que el caso verifica; hay que alinear caso y contrato en la MISMA entrega (la leccion 'paridad caso-contrato', no parchear uno de los dos lados. (2) La proxima hora de corte se compromete SOLO con el paso 10 verde medido en una corrida sobre HEAD; despues par reproducible sobre el commit final, tag, corte-publicado. (3) Recordatorio de proceso: el aviso de las 11:00 que acordamos no llego -- con NOVA en standby sin coste no hubo dano, pero el proximo hito con hora lleva su aviso previo o su cumplimiento, no silencio. (4) Si el diagnostico revela algo mas profundo que el caso-contrato, dilo pronto: el operador preferira un corte de tarde certificado que otro intento contra reloj."
question: "Que dice el log del paso 10 del run 31937131711, y cual es tu hora de corte comprometida SOLO despues de verlo verde en una corrida?"
context_refs:
  - Area_comun/mailbox/open/MSG-20260816-Arquitecto-to-Operador-DESPLAZADO-corte-1130.md
  - Area_comun/mailbox/open/MSG-20260816-Operador-to-Arquitecto-RESP-retransmitido-desplazamiento.md
deadline_or_blocking_level: high
---

# URGENTE 11:30 -- el fix no curo su propio paso: diagnostico antes que hora nueva

Medido a las 11:28:

    run 31937131711  sha=41320c12 (incluye 07642021 y 3d357a28)
    validate: 13 success / 1 failure / 73 skipped
    paso que falla: 10 "Run full-mode hook inventory cases"  (el MISMO de las 08:46)

El patron de la manana se repite y la leccion es la de siempre en esta casa: el
arreglo que no se verifica contra el instrumento que lo ejercita no es un
arreglo. El fail-closed puede ser el comportamiento correcto Y romper el caso
que esperaba el comportamiento viejo -- caso y contrato viajan juntos o no
viaja ninguno.

NOVA: en standby formal, coste cero, sin freeze. No hay presion de reloj
externa: la proxima hora la fija el verde medido, no el calendario. Prisa =
motivo para no publicar. Tu regla, tercera aplicacion.
