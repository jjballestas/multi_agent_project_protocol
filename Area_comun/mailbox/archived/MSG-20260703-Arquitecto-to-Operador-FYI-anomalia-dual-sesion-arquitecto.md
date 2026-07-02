---
message_id: MSG-20260703-Arquitecto-to-Operador-FYI-anomalia-dual-sesion-arquitecto
from: Arquitecto
to: Operador
type: FYI
status: archived
requires_response: true
response_owner: Operador
created_at: 2026-07-03
context_refs:
  - Area_comun/state/CLAIMS.json
  - Area_comun/tasks/TASK-0241-visionnova-f1d-taxonomia-defectos.md
one_line_summary: "Anomalia DECISION-0018: DOS sesiones Arquitecto activas coordinando F1 en paralelo; pido cerrar una (recomiendo la anterior)."
requested_action: "Cerrar una de las dos sesiones Arquitecto (recomiendo la ANTERIOR; esta sesion arranco 2026-07-03 ~00:42 con el prompt de sesion 20260703). Mientras convivan, el claim de ledger es el unico mutex entre ellas."
question: "Cual de las dos sesiones Arquitecto cierro/queda? (recomendacion: queda la nueva, cerrar la anterior)"
---

# FYI - Anomalia: DOS sesiones Arquitecto coordinando en paralelo

Hora: 2026-07-03 01:20 (local).

## Hecho observado
La sesion Arquitecto NUEVA (arrancada ~00:42 con "Retoma como Arquitecto") detecto que la
sesion Arquitecto ANTERIOR sigue VIVA y coordinando: 00:49-01:00 ejecuto la higiene del ciclo
0240 (TX-hyg0240-b1/b2, commit 571709e) y promovio TASK-0242 ready + GO a Codex (commit
89bce74). Ambas firman actor_id "Arquitecto" y reaccionan a los mismos eventos del arbol.

## Riesgo
- Promociones/GOs duplicados y ediciones divergentes sobre las mismas rutas compartidas.
- Los self-filter de ambos monitores ignoran los commits de la otra (misma firma
  Co-Authored-By), asi que ninguna ve a la otra como peer activity: la colision seria
  silenciosa.
- El ledger (submit_intent atomico + claims) contiene el dano; el mailbox y los archivos
  compartidos no tienen ese mutex.

## Mitigacion ya aplicada por esta sesion
- Particion de carriles via CLAIM: esta sesion tomo TASK-0241 (F1-D taxonomia, owner
  Arquitecto) con CLAIM-20260703-arquitecto-0241-taxonomia y la trabaja; el carril 0242 queda
  con el GO ya emitido por la sesion anterior (valido, no se duplica).
- Esta sesion NO repite higiene ni GOs ya emitidos; verifica CLAIMS.json antes de cada
  escritura compartida.
