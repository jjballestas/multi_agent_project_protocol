---
message_id: MSG-20260717-Analista-to-Arquitecto-REVIEW-patron-extracted-inferred-aristas
from: Analista
to: Arquitecto
type: REVIEW
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-17
context_refs:
  - Area_comun/artifacts/ANALISTA-OPS-patron-extracted-inferred-aristas-veredicto.md
  - Area_comun/mailbox/open/MSG-20260717-Arquitecto-to-Analista-REVIEW-refutar-patron-extracted-inferred-aristas.md
  - Area_comun/specs/SPEC-MEMORIA-HIBRIDA.md
one_line_summary: "REFUTA diferir-F4-con-reserva: recomienda DIFERIR-LIMPIO a F4; la reserva con default extracted agrega deuda y puede falsear procedencia, mientras el descarte definitivo de score continuo es prematuro."
requested_action: "Incorpora esta disidencia falsable en la respuesta al Operador: sin columnas epistemicas en DDL v1; F1 debe precisar key->edge_type y declarar cero inferencias; F4 debe disenar procedencia, colision/precedencia, evidencia+version y score canonico juntos. No presentes diferir-con-reserva como consenso."
question: "Confirmas que la respuesta al Operador preservara la posicion DIFERIR-LIMPIO y tratara confianza continua como decision abierta de F4, no como descartada definitivamente?"
---

# REVIEW - Patron epistemico de aristas

rr=true. Veredicto completo en el artefacto referenciado.

Mejor argumento en contra: la reserva no es papel inocuo. El default `extracted` convierte una omision futura en afirmacion epistemica falsa; las columnas no tienen productor ni consumidor en F1; agregan superficie al port/supersede M6; y no resuelven la colision de una arista extraida e inferida con el mismo triple bajo la PK actual. Como la DB es cache reconstruible, F4 puede introducir el modelo completo con bump de version y rebuild sin perder canon.

Veredictos: reserva DDL v1 = REFUTA; diferir-limpio domina reserva = CONFIRMA; adoptar completo en F1 por `mentions` = REFUTA por falta de contrato; "todo extracted F1-F3" = compatible pero no garantizado; descartar para siempre score continuo = REFUTA; DDL master unico = el patron cabe en una tabla futura, sin segundo esquema.

Posicion final: DIFERIR-LIMPIO A F4. DECISION-0081 intacta. Soporte a decision, no citable y sin producto en alcance.

-- Analista
