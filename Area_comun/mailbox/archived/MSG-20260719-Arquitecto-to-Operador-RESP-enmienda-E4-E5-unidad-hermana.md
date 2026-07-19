---
message_id: MSG-20260719-Arquitecto-to-Operador-RESP-enmienda-E4-E5-unidad-hermana
from: Arquitecto
to: Operador
type: RESP
status: archived
requires_response: false
created_at: 2026-07-19
context_refs:
  - Area_comun/mailbox/open/MSG-20260719-Operador-to-Arquitecto-ENMIENDA-E4-E5-adoptable-githooks.md
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
  - Area_comun/tasks/TASK-0266-d0103-e4e5-propagacion-harness-adoptable.md
one_line_summary: "RESP E4/E5 (21:09 local): ruteo resuelto como UNIDAD HERMANA TASK-0266 (tu preferencia + razon de proceso E1), registrada en ready con DoR completo, secuenciada tras el cierre de 0257. Enmiendas E4/E5 selladas en la 0103 (commit 7fbb88a). Fila de tabla incluida (C1)."
---

# RESP - Enmiendas E4/E5: unidad hermana TASK-0266

Hora local: 2026-07-19 21:09. Decision del ruteo delegado: **unidad hermana**, como
preferias. Razon adicional de proceso: plegar E4/E5 en TASK-0257 cambiaria su
acceptance a mitad de fix-loop, rompiendo la cobertura del carve-out E1 (exige MISMO
acceptance) y forzando re-aprobacion -- la unidad hermana evita justo eso.

Sellado (commit 7fbb88a, pusheado):
- E4 y E5 registradas como enmiendas en DECISION-0103 citando tu MSG como firma.
- TASK-0266 registrada con intake DoR completo y promovida a ready.

Fila de tabla (C1, mismo formato del plan aprobado):

| id | goal (compacto) | acceptance (compacto) | verification_cmd (nucleo) | required_capability | risk | estimate |
|---|---|---|---|---|---|---|
| TASK-0266 | E4/E5: .githooks/** adoptable en upgrade_instance + new_instance cablea core.hooksPath | delta adoptable visible en sandbox; instancia nueva nace armada sin paso manual y prueba negativa aborta; instancia existente upgradeada recibe el hook y valida verde; cero cambios al hook en si | dry-run upgrade + new_instance a temporal + prueba negativa + validate/scans | implementer | low | S |

Secuencia: arranca tras el CIERRE de TASK-0257 (comparte scripts/new_instance.py con su
scope); puede correr en paralelo con TASK-0258 (rutas disjuntas), GO de a una. Aplicar
el upgrade a NOVA real queda FUERA (operacion aparte que gateas tu).

Estado del fix-loop al momento de esta RESP: re-entrega de 0257 cerrada (F01/F02
remediados segun el maker) y re-juicio ruteado al Analista; TASK-0258 sigue cerrada
hasta el GO del gate.
