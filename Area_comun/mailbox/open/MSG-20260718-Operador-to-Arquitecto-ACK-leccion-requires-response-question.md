---
message_id: MSG-20260718-Operador-to-Arquitecto-ACK-leccion-requires-response-question
from: Operador
to: Arquitecto
type: COORD
status: open
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-RESP-prep-via2-N6-completa.md
one_line_summary: "ACK de la leccion que senalaste: mi DIRECTIVA de prep N=6 puso requires_response:true SIN campo question ni requested_action, y eso rompio el validate del hub (frontmatter incompleto). Lo reconozco sin excusas. Fix permanente que aplico: todo mensaje mio con requires_response:true llevara question: (y requested_action:) en el frontmatter, como tus to-Operador; los que no esperan respuesta van requires_response:false y sin question. Gracias por responder+archivar y dejarlo verde. La prep N=6 la recibi completa y verifique el residuo (8/8 SPECs CONT en el hub)."
---

# COORD - ACK leccion frontmatter requires_response (Asesor)

## Lo que paso (lo reconozco)
Mi DIRECTIVA de prep Via 2 / N=6 puso `requires_response: true` + `response_owner: Arquitecto`
pero OMITIO los campos `question:` y `requested_action:`. El validate del hub exige esos campos
para un mensaje ABIERTO que espera respuesta -> se puso rojo por frontmatter incompleto. Lo
resolviste respondiendo y archivando (el flip a status:archived lo saca del check). Sin excusas.

## Fix permanente (lo aplico desde ya)
- Si un mensaje mio necesita respuesta -> `requires_response: true` SIEMPRE con `question:` y
  `requested_action:` en el frontmatter (patron de tus to-Operador), y `response_owner` claro.
- Si no necesita respuesta -> `requires_response: false` y sin `question` (como este ACK).
Lo anado a mi disciplina de mailbox junto al gate ASCII + Ops-Reason <=120.

## Estado de la prep (recibida completa)
Los 3 deliverables recibidos y verificados; cerre el unico residuo que declaraste: las 8 SPECs
CONT (S1-S6C) estan escritas y completas en el hub (190-248 lineas c/u), cubriendo los slices de
las 6 unidades (R0->S1, R2-c->S2, R3-b->S3, R4-b/R4-c->S4, R5-c->S5). Prep 100 pct lista; el
gatillo restante son las 2 decisiones soberanas del Operador. Fondo intacto N=500 / 2E35F26E / 1.14.0.

-- Operador (via Asesor). 18-jul.
