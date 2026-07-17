---
message_id: MSG-20260717-Arquitecto-to-Operador-HITO-u1-done-u2-lanzada
from: Arquitecto
to: Operador
type: FYI
status: archived
requires_response: false
created_at: 2026-07-17
context_refs:
  - Area_comun/mailbox/open/MSG-20260717-Arquitecto-to-Operador-HITO-u1-nogo-remediacion-ruteada.md
one_line_summary: "HITO U1 = DONE (ciclo adversarial completo en ~75 min de carril automatizado) + U2 REGISTRADA Y LANZADA (dump canonico + rebuild + round-trip AC5). Cadena U1: entrega -> NO-GO 3 BLOCKERs -> remediacion iter 1 -> re-judgement independiente GO (5 familias sink, 20 claves PII, dirty-tree+CRLF) -> ratificacion -> done-flip Codex. Blip infra: 1 falso positivo del clasificador cyber del proveedor del checker, resuelto con retry (des-seen)."
---

# HITO - U1 DONE + U2 lanzada

## U1 cerrada (TASK-0001, instancia a1c9419)

Cadena completa del carril automatizado, sin construccion manual:
1. Entrega Codex (12 min) -> 2. Veredicto adversarial NO-GO con 3 BLOCKERs conductuales reales
(sink --db, PII via type regex, hash working-tree) -> 3. Remediacion iteracion 1 (8c3398b:
sink canonico fail-closed, enum finito 24 valores + gate PII por clave, procedencia por blob
exacto) -> 4. Re-judgement independiente GO en clon limpio (5 familias de sink rechazadas con
sentinelas intactos; payload salario+IBAN+nombre plantado en las 20 claves allowlisted = cero
hits publicos; dirty-tree + golden CRLF byte-exactos) -> 5. Ratificacion review_approved
(Arquitecto, seq 24) -> 6. Done-flip por Codex (implementer). Validate 0, drift 0, cero claims.
maker!=checker sostenido por llave Y por capacidad en cada eslabon (firmas en el events.jsonl
de la instancia).

## Blip de infraestructura (resuelto, sin accion tuya)

El primer intento de re-judgement murio: el clasificador de seguridad del proveedor del CLI del
checker flageo sus PROPIOS probes adversariales (fixtures IBAN + traversal) como riesgo cyber
(falso positivo no-determinista; la primera review corrio identicos probes sin flag). Resuelto
con retry via des-seen. Si se vuelve recurrente, lo escalo con opciones (checker informal en
modelo fuerte para la iteracion, o el programa de acceso del proveedor).

## U2 LANZADA (TASK-0002, instancia d632244)

Dump canonico determinista (particion derivada s.6) + build --rebuild desde canon puro +
round-trip AC5 dump(A)==dump(B) byte a byte + regresion de los guardrails F1-F3. GO en la cola
de Codex (cron vivo). Misma cadena maker->checker->ratificacion. Restan U3 (drift+query) y U4
(revive_pack + DEMO REVIVE) para cerrar F1.

-- Arquitecto. Hora local ~17:05 (UTC+2). Fondo: N=500, 2E35F26E, 1.14.0 intactos.
