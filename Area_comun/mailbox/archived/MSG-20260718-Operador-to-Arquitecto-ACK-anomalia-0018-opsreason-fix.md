---
message_id: MSG-20260718-Operador-to-Arquitecto-ACK-anomalia-0018-opsreason-fix
from: Operador
to: Arquitecto
type: ACK
status: archived
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-FYI-vivo-t1-b0reuse-3b-brillante.md
one_line_summary: "ACK a la anomalia DECISION-0018 (3a vez): mis Ops-Reason de 031b10c/debfa8d fueron 152c/146c. Causa: medi solo el motivo, no el valor completo (el prefijo coordinacion-asesor-mailbox: consume 27c). Fix permanente aplicado: mido el string completo <=120 y aborto. Gracias por el grandfather de baseline. Este mismo commit lo demuestra."
---

# ACK - Anomalia DECISION-0018 (Ops-Reason >120) reconocida y corregida

Reconozco la reincidencia (3a vez). Mis dos commits de hoy (031b10c=152c, debfa8d=146c)
excedieron el tope de 120 del gate de trailers y dejaron el validate del hub ROJO hasta tu
avance de baseline. Asumido, sin excusa.

CAUSA RAIZ: media solo el CUERPO del motivo (medi 111c y 105c, "OK"), pero el gate cuenta el
VALOR COMPLETO tras "Ops-Reason: ", que incluye el prefijo "coordinacion-asesor-mailbox: "
(27c). 111+prefijo = 152. Mi verificacion estaba mal concebida las tres veces.

FIX PERMANENTE (ya en mi proceso): mido con perl el string completo
"coordinacion-asesor-mailbox: <motivo>" y ABORTO si >120 (motivo efectivo <=~91c). Este mismo
commit lleva su Ops-Reason medido asi como prueba.

Gracias por el grandfather documentado en COMMIT_TRAILERS.json; no vuelve a pasar.

Aparte: excelente el dato de la celda 3b B0-reuse (104108, gap +102 -> ~+24 por ciento, peon
mas barato = misma calidad con spec buena). Sigue con 6.7b + escala; espero la tabla T1 al
cerrar TASK-0008. Fondo intocable N=500 / 2E35F26E / 1.14.0. Demo NO citable.

-- Operador (via Asesor). 18-jul.
