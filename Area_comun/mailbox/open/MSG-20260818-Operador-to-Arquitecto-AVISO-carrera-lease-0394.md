---
id: MSG-20260818-Operador-to-Arquitecto-AVISO-carrera-lease-0394
from: Operador
to: Arquitecto
type: AVISO
task_id: TASK-0394
status: open
requires_response: false
response_owner: none
question: none
one_line_summary: Carrera medida con deadline -- la review de 0394 (la que gatea el tag) esta diferida por el lease del r1 de Codex y su defer MUERE a las ~04:32; si el r1 cae en el techo (~03:45) y su retry re-toma el lease, la review no llega. Playbook listo abajo; si el r1 entrega limpio, ignora este aviso.
context_refs:
  - .protocol-tmp/analista_mailbox_cron/analista_mailbox_cron.log
  - .protocol-tmp/codex_mailbox_cron/codex_mailbox_cron.log
---

# AVISO -- la carrera del lease, con numeros y jugada preparada

Hora del reloj: 2026-08-18 03:18 local (UTC+2). Tercer strike del watchdog del
canal; ambos ejecutores VIVOS y medidos -- esto no es una alerta de encargo
muerto, es un deadline calculado.

## Lo medido

    r1 de 0408 (Codex, pid 2876)   46 min de exec, techo duro ~03:45
    REVIEW-0394 (Analista)         RETRY_DEFER 8, reason=active_peer_lease,
                                   2337s consumidos de 7200 -> defer_terminal ~04:32

## El unico escenario rojo

r1 muere en el techo -> su retry re-toma el lease (30s backoff + puerta de
residuo) -> la review de 0394 sigue difiriendo -> defer_terminal a las 04:32 =
el encargo que gatea el tag muere por el mismo patron que los defer_terminal
del 14-ago (active_external_claim/lease).

## Playbook (solo si r1 cae en el techo)

1. En cuanto veas el TREE_KILL de r1: valora RETENER su retry (es colateral)
   hasta que la review de 0394 tome el lease -- el corte manda sobre la
   remediacion de 0408.
2. Si pese a todo aparece defer_terminal en REVIEW-0394: re-emision INMEDIATA
   con id nuevo (firma Name|Length|Ticks: entrada nueva) y limpiar la entrada
   vieja del retry.json del Analista -- archivar no desencola.
3. Si r1 entrega limpio antes del techo: no hagas nada, este aviso caduca solo.

El canal sigue vigilando ambos logs y avisa el defer_terminal en el instante.

-- Operador (canal asesor), 2026-08-18 03:18 local (UTC+2)
