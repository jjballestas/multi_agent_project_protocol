---
message_id: MSG-20260707-Operador-to-Arquitecto-ACTION-correccion-rumbo-contabilidad-la-hace-operador
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-07
context_refs:
  - Area_comun/mailbox/open/MSG-20260707-Operador-to-Arquitecto-ACTION-rumbo-contabilidad-1001-1002f4.md
one_line_summary: "CORRECCION del rumbo: el Operador + el DBA estan preparando la base de datos solida de Contabilidad (como Presupuesto arranco con BD reconciliada). Eso SACA Contabilidad WS1 del carril del Arquitecto. Foco del Arquitecto/Codex = solo las dos cadenas: 1001 t3-6 PRIMERO, luego 1002 F4 (FTS-only, embeddings diferidos por PII)."
requested_action: "Ajustar el rumbo: (A) Contabilidad NO es tu prioridad ahora -- el Operador + DBA estan refinando el diseno de la BD para dejar una BASE SOLIDA (mismo patron que Presupuesto: el Arquitecto arranco con BD reconciliada, no green-field). Cuando esa base este lista (y Julian onboardeado para el build gobernado), retomas el analisis/SPECs de Contabilidad SOBRE esa base. (B) Foco AHORA = las DOS cadenas por Codex: 1001 t3-6 PRIMERO (port, Quality Panel MVP, excepciones, test plan -- cierra el producto anti-vibecoding), LUEGO 1002 F4 FTS-only (embeddings DIFERIDOS hasta politica PII del operador). Usa los huecos entre re-gates para GO TASK-1105 (infra test) y preparar los SPECs de las tareas 1001 t3-6. Sin idle."
question: "Confirmas el rumbo corregido (foco en las 2 cadenas; Contabilidad la prepara el Operador+DBA y la retomas sobre base solida)? Reporta el avance de 1001 t3-6."
---

# ACTION - Correccion de rumbo: Contabilidad la prepara el Operador+DBA

Correccion al rumbo anterior (`MSG-...-rumbo-contabilidad-1001-1002f4`): el Operador esta trabajando CON EL
DBA para refinar el diseno de la base de datos de Contabilidad -> dejar una BASE SOLIDA con que arrancar,
igual que Presupuesto (que arranco con una BD reconciliada/endurecida, no green-field). Por tanto:

## (A) Contabilidad SALE de tu carril inmediato
No arranques Contabilidad WS1 ahora -- el Operador + DBA estan haciendo la base. Cuando la base este lista
(y Julian onboardeado para el build gobernado), retomas el analisis/SPECs de Contabilidad SOBRE esa base
solida. Es el mismo patron de Presupuesto: primero base firme, luego el equipo construye encima.

## (B) Foco AHORA = las dos cadenas (Codex)
1. **1001 t3-6 PRIMERO:** crear/promover port (t3), Quality Panel MVP (t4), registro de excepciones (t5),
   test plan de ambiguedad (t6). Cierra el producto anti-vibecoding (Zeus-Aegis).
2. **1002 F4 DESPUES:** FTS + deteccion de contradicciones, **FTS-ONLY** -- embeddings DIFERIDOS hasta que
   el operador fije politica PII.
3. Huecos entre re-gates: GO TASK-1105 (infra test fixture) + preparar los SPECs de 1001 t3-6. Sin idle.

## Frontera
Todo pre-30-jul a full. Nada toca el estudio medido ni el genesis del hub. El re-genesis A2 de Julian sigue
esperando su pubkey. El Operador retoma Contabilidad contigo cuando la base este lista.

-- Operador
