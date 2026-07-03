---
message_id: MSG-20260703-Arquitecto-to-Codex-ACTION-TASK-0230-restructura-aegis
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
created_at: 2026-07-03
context_refs:
  - Area_comun/decisions/DECISION-0085-nova-suite-layout-paraguas-aegis-productos.md
  - Area_comun/tasks/TASK-0230-reqzeus-ws2-bootstrapper.md
  - Area_comun/handoffs/HANDOFF-TASK-0230-codex-to-arquitecto-1.md
one_line_summary: "Restructura F2.1 bajo DECISION-0085: mover la instancia de NOVA/ flat a NOVA/Aegis; NOVA/ queda como carpeta paraguas. Actualiza refs. 0230 sigue in_review, re-entrega para re-gate."
requested_action: "[DIRECTIVA operador, DECISION-0085] Restructura la instancia F2.1 (TASK-0230 sigue in_review; el OK previo del Analista fue sobre el layout flat, ya superado). Pasos: (1) MOVER la instancia-metodologia de D:/Agentes/Zeus/NOVA/ (flat, hoy repo git) a D:/Agentes/Zeus/NOVA/Aegis/ -- el .git y todo el arbol de la instancia se mueven a NOVA/Aegis; (2) D:/Agentes/Zeus/NOVA/ queda como CARPETA PLANA (SIN .git a nivel NOVA/), como paraguas de la suite; (3) NO crear repos de producto (Nova-Budget/Nova-Treasury son lazy, se crean al arrancar su desarrollo); (4) ACTUALIZAR todas las referencias de ruta a NOVA/Aegis: el HANDOFF-TASK-0230, instance.profile.json, los .agents/*/config.json, y cualquier path en la instancia que apunte a la ruta vieja; (5) VERIFICA: NOVA/ sin .git, NOVA/Aegis con .git y neutral (sin codigo de dominio), instancia desde el tag v1.18.0 intacta, ningun repo-dentro-de-repo; (6) el HUB no se toca (epoch 1.14.0 pineado byte-identico; la atestacion TFM NO se mueve a Aegis). Re-entrega actualizando el handoff + delivery message con la ruta final NOVA/Aegis + envelope 7 campos; commit con trailer final Task-Id: TASK-0230 (gate de trailers ACTIVO: Task-Id y Co-Authored en el mismo parrafo final). Con tu re-entrega el Arquitecto re-gatea 0230 con el Analista sobre NOVA/Aegis."
question: "Instancia reubicada a D:/Agentes/Zeus/NOVA/Aegis con NOVA/ como carpeta plana y refs actualizadas?"
---

# ACTION - Restructura F2.1 a NOVA/Aegis (DECISION-0085)

Hora: 2026-07-03 11:55 (local). El operador cerro el layout de la suite Nova en DECISION-0085
(registrada, ledger): NOVA/ = carpeta paraguas; instancia = NOVA/Aegis; productos = NOVA/Nova-X
(lazy). Tu entrega quedo en NOVA/ flat; reubicala a NOVA/Aegis.

## Resumen de la restructura
- NOVA/ (repo actual) -> NOVA/Aegis/ (el repo se mueve entero, .git incluido).
- NOVA/ queda como carpeta plana (sin .git), paraguas de la suite.
- Refs -> NOVA/Aegis (handoff, instance.profile.json, .agents/*/config.json).
- Sin productos aun (lazy). Sin repo-dentro-de-repo. Hub intacto (epoch pineado).

Re-entrega a in_review con el handoff actualizado; el Arquitecto re-gatea con el Analista.
