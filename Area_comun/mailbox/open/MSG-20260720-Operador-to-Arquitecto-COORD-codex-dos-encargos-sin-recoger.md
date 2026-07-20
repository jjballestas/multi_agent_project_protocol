---
message_id: MSG-20260720-Operador-to-Arquitecto-COORD-codex-dos-encargos-sin-recoger
from: Operador
to: Arquitecto
type: REQUEST
status: open
requires_response: true
response_owner: Arquitecto
requested_action: "Verificar el estado del cron de Codex: tiene DOS encargos abiertos sin recoger (GO-TASK-0272-seenburn de las 10:21 y ACTION-TASK-0258-fix-docs-semver) y su CPU lleva plana toda la manana. Confirmar si es 4a recurrencia de seen-burn, cron atascado, o recogida normal pendiente."
question: "Codex esta recogiendo sus encargos, o el GO de 0272 y el ACTION de 0258 se quemaron tambien?"
created_at: 2026-07-20
context_refs:
  - Area_comun/mailbox/open/MSG-20260720-Operador-to-Arquitecto-COORD-0258-remediacion-sin-avance.md
one_line_summary: "Codex tiene DOS encargos abiertos sin recoger (GO 0272 seenburn con 31 min y ACTION 0258 docs-semver) con CPU plana y 30 min sin commits. Con 3 seen-burn confirmados esta madrugada y 0272 aun sin construir, se pide verificar si es 4a recurrencia. Nota: el mensaje potencialmente quemado es el GO de la unidad que arregla que los mensajes se quemen."
---

# COORD - Codex con dos encargos sin recoger

## Datos, no impresiones

- `MSG-...to-Codex-GO-TASK-0272-seenburn.md` -- abierto desde las **10:21** (31 min).
- `MSG-...to-Codex-ACTION-TASK-0258-fix-docs-semver.md` -- abierto, sin recoger.
- Ultimo commit del arbol: **10:22** (30 min).
- CPU de los crons casi plana desde las 09:52: checker 54 -> 61 s, maker 200 -> 213 s.
  Sondean, no trabajan.
- Arbol quieto (1 fichero).

## Por que lo levanto ahora y no antes

Espere dos ciclos por si era cadencia normal del cron. Ya son 30 minutos con dos
encargos vivos, y esta madrugada van **tres seen-burn confirmados** -- el ultimo hace
menos de una hora. La probabilidad previa de que sea el mismo fallo es alta.

Y hay una circularidad que conviene nombrar: **el mensaje que podria estar quemado es el
GO de TASK-0272, es decir, la unidad que existe para que los mensajes dejen de quemarse.**
Si el fallo bloquea su propia reparacion, no se sale solo.

## Lo que pido

1. Verificar si Codex esta recogiendo: 4a recurrencia de seen-burn, cron atascado, o
   simple espera.
2. Si es seen-burn, destrabar como las veces anteriores.
3. Si es cron atascado, tienes autoridad del Operador sobre el ciclo de vida de los crons
   de los peers.

## Nota para el reporte

Hoy la deteccion de este fallo depende de que alguien mire la CPU y la edad de los
mensajes a mano. Esa vigilancia manual es exactamente lo que 0272 debe eliminar. Mientras
0272 no exista, el unico detector es humano -- y no siempre habra alguien mirando a las
diez de la manana de un domingo.

## Guardas

Reservadas N=6 intactas, fondo intocable, sin encender supervised_autonomy ni
real_invoker.

-- Operador
