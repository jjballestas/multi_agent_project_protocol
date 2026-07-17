---
message_id: MSG-20260717-Arquitecto-to-Operador-RESP-0099-sellada-version-corregida
from: Arquitecto
to: Operador
type: RESP
status: archived
requires_response: false
created_at: 2026-07-17
context_refs:
  - Area_comun/decisions/DECISION-0099-politica-roster-peones-maker-only-checker-fuerte.md
  - Area_comun/mailbox/open/MSG-20260717-Operador-to-Arquitecto-DIRECTIVA-correccion-pre-sello-0099-peon-subordinado-al-maker.md
one_line_summary: "DECISION-0099 SELLADA en su version CORREGIDA (tx seq 4713-4715, status active): regla 1 = peon ejecutor de codigo SUBORDINADO al maker; regla 2 = el MAKER (modelo fuerte) gobierna a los peones con especificacion detallada y responde ante el checker; regla 3 checker fuerte sin cambios. Tu firma (585b7ab) aplicada a esta version por tu DIRECTIVA (dca50ec). Espejo al export 0096 = tarea de mantenimiento pendiente. FYI anomalia menor: el MSG de FIRMA venia con requires_response sin question -> validate rojo; reparado con question minima."
---

# RESP - DECISION-0099 sellada (version corregida)

## Confirmacion (responde tus dos rr: FIRMA + CORRECCION)

SI: NO selle el draft original. Aplique tu correccion pre-sello VERBATIM y selle esa version:
- **Regla 1:** peon = ejecutor de codigo SUBORDINADO al maker (modelo debil, p.ej. local 3B-8B);
  jamas maker autonomo, checker, orquestador ni firmante.
- **Regla 2:** el MAKER (modelo fuerte) gobierna a los peones: asigna sub-tareas con
  especificacion DETALLADA sin ambiguedad (DoR completo) y RESPONDE por el resultado ante el
  checker; tarea subespecificada no se rutea a peon.
- **Regla 3:** checker en modelo fuerte, sin cambios (maker!=checker por capacidad y por llave).

Sello: submit_intent decision patron 0091, tx seq 4713-4715, status active, approved_by con la
referencia de tu FIRMA (585b7ab) + la correccion (dca50ec). Espejo al export born-operational
(0096): tarea de mantenimiento del template, la registro en la cola no-bloqueante.

## FYI anomalia menor (para el gate del asesor)

El MSG de FIRMA llego marcado como respuesta-requerida pero sin campo question -> el validador
canonico del mailbox fallo (validate=1) en todo el arbol hasta la reparacion. Lo repare anadiendo la question
minima (mismo patron que el fix open->answered del 13-jul). Sugerencia: el gate pre-commit del
asesor deberia chequear el par requires_response/question ademas de ASCII y Ops-Reason<=120.
Nota mia: mi propio gate tambien fallo aqui -- commitee un HITO con validate=1 sin frenar (el
exit-code quedo enmascarado); ya corregido el habito: gate DURO por exit-code pre-commit.

## Carril U1/U2 (contexto)

U1 = DONE (ciclo adversarial completo). U2 (round-trip AC5) en construccion por Codex.

-- Arquitecto. Hora local ~17:20 (UTC+2). Fondo: N=500, 2E35F26E, 1.14.0 intactos.
