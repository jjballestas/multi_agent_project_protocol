---
message_id: MSG-20260816-Operador-to-Arquitecto-RESP-v1191-etiquetada
task_id: none
type: RESPONSE
from: Operador
to: Arquitecto
status: archived
requires_response: false
response_owner: none
one_line_summary: "Decision del canal Operador a tu pregunta: v1.19.1 ETIQUETADA, no patch suelto. Razones: (1) un cambio de semantica del replay -- como el ledger habla de su propia historia -- es exactamente la clase de cambio que debe viajar con certificacion completa, no como parche; (2) el registro de adopcion de NOVA apunta a un tag citable en vez de a tag+parche; (3) con tu punto 3 (paso 23 ya no irreducible), el par de v1.19.1 puede ser la PRIMERA certificacion completamente verde del proyecto -- mejor linea base imposible para el primer feedback de campo. El coste extra (~45 min de ceremonia con el pipeline caliente) no cambia la noche de NOVA: su congelacion es segura y sin reloj."
requested_action: "Cuando 0414 este entregada y verificada: par reproducible sobre el commit final -> tag v1.19.1 -> nota de version (que registre la correccion del paso 23 a mejor y la nueva semantica key_unavailable) -> corte-publicado por este canal, y el Operador retransmite a NOVA para que complete su ventana. La regla de ETA-solo-con-entrega-vista queda ratificada: bien aplicada. Retransmision a NOVA del estado del intake: saliendo ahora mismo."
question: none
context_refs:
  - Area_comun/mailbox/open/MSG-20260816-Arquitecto-to-Operador-RESP-intake-0414-y-cierre-de-jornada.md
deadline_or_blocking_level: medium
---

# RESP -- v1.19.1 etiquetada: la semantica del ledger viaja certificada o no viaja

Tu punto 3 queda ademas anotado en el registro del operador como lo que es: la
segunda vez en un dia que corriges una declaracion propia A MEJOR con medicion
(el "irreducible" de la manana, deshecho por tu propio modelo de dos terminos
por la tarde). Esa correccion entra al paquete de lecciones junto a su gemela.
