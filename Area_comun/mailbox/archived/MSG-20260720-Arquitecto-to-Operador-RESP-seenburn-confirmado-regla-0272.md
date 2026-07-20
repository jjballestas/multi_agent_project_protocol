---
message_id: MSG-20260720-Arquitecto-to-Operador-RESP-seenburn-confirmado-regla-0272
from: Arquitecto
to: Operador
type: RESP
status: archived
requires_response: false
created_at: 2026-07-20
context_refs:
  - Area_comun/mailbox/open/MSG-20260720-Operador-to-Arquitecto-COORD-0258-remediacion-sin-avance.md
  - Area_comun/tasks/TASK-0272-harness-seenburn-retry-pregate-rojo.md
one_line_summary: "RESP (09:58 local): SEEN-BURN CONFIRMADO, tenias razon -- el exec de la remediacion 0258 aborto a las 08:47 por MI claim de higiene activo (envelope correcto: DECISION-0020) y el harness quemo el mensaje. Des-seen aplicado, reprocesa ya. Es la 3a recurrencia (no 2a): registrada como TASK-0272 con intake DoR completo, priority high, esperando tu GO. Y una leccion mia: yo cause la ventana ocupada."
---

# RESP - seen-burn confirmado; regla registrada como TASK-0272

Hora local: 2026-07-20 09:58. Confirmado punto por punto:

1. **SI era seen-burn.** El exec de Codex sobre la ACTION docs de 0258 corrio a las
   08:47, se nego CORRECTAMENTE ("Arquitecto debe completar o revertir limpiamente
   CLAIM-arq-hyg-0847...; ejecutar submit_intent ahora violaria DECISION-0020") y el
   harness marco el mensaje como visto igualmente. Quietud silenciosa desde entonces.
2. **Destrabado**: des-seen aplicado a las 09:55; mis claims estan todos liberados
   (cero activos) y el arbol quieto, asi que su proximo ciclo (~5 min) lo procesa
   limpio.
3. **Es la TERCERA, no la segunda.** El patron aparecio tambien el 19-jul con la ACTION
   de remediacion de 0257 (mismo mecanismo, misma negativa correcta del peer). Tu
   criterio de la C3-bis aplica con margen: **registrada TASK-0272** con intake DoR
   completo, priority high, y hace las DOS cosas que apuntaste -- marcado de visto solo
   tras ejecucion confirmada Y deteccion/senal cuando el reintento se agota. Con
   taxonomia transitorio-vs-definitivo para que jamas reintente una negativa
   principiada del checker. **Esperando tu GO**; no la arranco sola.

## Autocritica (parte del bucle, no adorno)

Las tres veces la ventana ocupada la cause YO: mi claim de higiene o mi ledger a medio
commitear. El harness quemo el mensaje, pero quien puso la piedra fui yo. Dos
correcciones mias ya aplicadas hoy: staging por lista explicita (nada de -A dir-level en
rutas compartidas) y ciclos de ledger por pasos separados con verificacion entre cada
uno. La tercera -- no rutear ACTIONs mientras tengo un claim de higiene en vuelo -- la
adopto desde ahora: primero libero, luego ruteo.

## Estado de la tanda al momento de esta RESP

- DONE: 0257, 0267, 0268, 0270, 0271. **E6 RESUELTA** (0269 ratificada; cifra del checker
  70.7s caliente / piso 43s = 2.9x tu umbral -> E6-A PERMANENTE sellado sin re-litigar;
  dato clave: materializar solo costaba 1.9s, el coste nunca estuvo ahi).
- EN VUELO: 0258 (fix docs SemVer, reprocesando ahora tras el des-seen).
- COLA: 0259-0264 -> gate 0265 -> cierre de tanda.
- TUYO: GO del build-open N=6 (respondido ADELANTABLE con evidencia verificada), GO de
  TASK-0272, y la oferta vieja de endurecimiento del ledger (parqueable si no la quieres).

Gracias por la vigilancia: los tres episodios los cazo un humano mirando CPU plana, no el
sistema. Eso es exactamente lo que 0272 viene a corregir.
