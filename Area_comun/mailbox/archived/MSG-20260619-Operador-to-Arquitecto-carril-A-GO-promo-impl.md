---
message_id: MSG-20260619-Operador-to-Arquitecto-carril-A-GO-promo-impl
type: DECISION
task_id: TASK-0120
from: Operador
to: Arquitecto
requires_response: false
status: archived
one_line_summary: GO a la promocion 0043/0082/0120 (verificada: tx atomica 5 ops, NO toca event_state, #4 OFF, MINOR 1.12.0, TASK-0120 ready/Codex). NO gateo la implementacion: lanza el GO a Codex EN CUANTO el mirror confirme commit + drift 0 + read-back en disco, con 4 condiciones. Reservo el gate del operador para provisioning REAL + re-genesis + flip.
requested_action: "Aplicar PROMOTE-0043 por el mirror sobre copia limpia==HEAD; tras commit + drift 0 + read-back, lanzar GO de implementacion de TASK-0120 a Codex con las 4 condiciones. NO encender #4."
context_refs:
  - personal/Arquitecto/carril_A/PROMOTE-0043-intents.json
  - personal/Arquitecto/carril_A/PROMOTE-0043-APPLY.md
  - Area_comun/mailbox/open/MSG-20260619-Operador-to-Arquitecto-carril-A-integridad-recurrente.md
validation_refs:
  - "intents.json verificado en disco: 5 ops (claim/decision DECISION-0043/task_upsert TASK-0120 ready owner Codex/project_narrative 1.12.0/claim); 0 menciones chain_enabled|agent_signatures_enabled|anchor_enabled|event_state; flags en disco siguen false; protocol_version 1.11.0 (->1.12.0 al aplicar)"
deadline_or_blocking_level: normal
---

# GO promocion del cargador + GO de implementacion (no gateado) - #4 OFF

Verifique la tx en disco: 5 ops atomicas, **no toca `event_state` ni los flags** (#4 sigue OFF), MINOR
1.11.0->1.12.0 correcto, TASK-0120 ready/Codex (maker!=checker). Bien construida. **GO a aplicarla** por
el mirror sobre copia limpia == HEAD (sin re-genesis: esta promocion no escribe el event log).

## Tu pregunta: NO gateo la implementacion
Dejala fluir. Ya aprobamos la ruta del cargador; implementar TASK-0120 es el paso natural y de bajo
riesgo (codigo + goldens aditivos, off-by-default, no enciende #4, no provisiona, no re-genesis). Lanza el
GO de implementacion a Codex **en cuanto el mirror confirme commit + drift 0 + read-back en disco**, con:

1. Codex corre el nuevo golden `event_auth_secret_resolution_cases` (AC1-AC8) verde, en copia verificada
   limpia que persiste.
2. #4 OFF; sin provisioning real; secretos solo fixtures bajo `examples/`; sin tocar flags.
3. maker!=checker: Codex implementa -> tu reproduces/revisas.
4. Misma disciplina de persistencia/corrupcion del FS (verificar limpio==HEAD al escribir).

## Donde SI gateo (operador)
El GO del operador queda reservado para: **provisioning con secretos REALES + anchor remoto + re-genesis +
el flip de #4**. Eso no se mueve sin mi GO explicito y arbol verificado limpio en el instante.

## Coordinacion de higiene
Ya higienice `open/` antes de esto: 4 -> archived (feasibility-0043, 2x acks Arquitecto, ack Codex) y
`integridad-y-secuencia` -> answered. Tu manifiesto re-hace esa higiene y cierra `integridad-recurrente`
con la promocion; que el apply sea **idempotente** sobre lo ya movido (no fallar si no estan en `open/`).

Codex y crons activos. Canal ASCII.
