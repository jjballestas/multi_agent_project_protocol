---
msg_id: MSG-20260703-Arquitecto-to-Operador-FYI-anomalia-dual-sesion-arquitecto
from: Arquitecto
to: Operador
type: FYI
task_id: null
requires_response: true
response_owner: Operador
created_at: 2026-07-03T01:05:00+02:00
one_line_summary: Dos sesiones Arquitecto activas en paralelo coordinando el mismo loop F1 (anomalia DECISION-0018); pido cierre de una
---

# FYI - Anomalia: DOS sesiones Arquitecto coordinando en paralelo

Hora: 2026-07-03 01:05 (local).

## Hecho observado
La sesion Arquitecto NUEVA (esta, arrancada ~00:42 con el prompt "Retoma como Arquitecto")
detecto que la sesion Arquitecto ANTERIOR sigue VIVA y coordinando: a las 00:49-01:00 la
sesion anterior ejecuto la higiene del ciclo 0240 (TX-hyg0240-b1/b2, commit 571709e),
promovio TASK-0242 ready + GO a Codex (commit 89bce74) y mantiene transacciones submit_intent
en vuelo. Ambas sesiones firman actor_id "Arquitecto" y reaccionan a los mismos eventos.

## Riesgo
- Promociones/GOs duplicados y ediciones divergentes sobre las mismas rutas.
- Los self-filter de ambos monitores ignoran los commits de la otra (misma firma Co-Authored-By),
  asi que NINGUNA ve a la otra como "peer activity": la colision seria silenciosa.
- El ledger (submit_intent atomico + claims) contiene el dano, pero el canal mailbox y los
  archivos compartidos no tienen ese mutex.

## Mitigacion aplicada por esta sesion (sin esperar)
- Particion de carriles por CLAIM en el ledger: esta sesion tomo TASK-0241 (F1-D taxonomia,
  owner Arquitecto) con claim CLAIM-20260703-arquitecto-0241-taxonomia; la sesion anterior
  quedo de facto con el carril 0242 (ya emitio su GO a Codex, valido, no lo duplico).
- Esta sesion NO repite higiene ni GOs ya emitidos.

## requested_action
Operador: cerrar/detener UNA de las dos sesiones Arquitecto (recomiendo cerrar la ANTERIOR y
dejar esta, que arranco con el prompt de sesion 20260703 actualizado). Mientras ambas vivan,
el claim del ledger es el unico mutex efectivo entre ellas.
