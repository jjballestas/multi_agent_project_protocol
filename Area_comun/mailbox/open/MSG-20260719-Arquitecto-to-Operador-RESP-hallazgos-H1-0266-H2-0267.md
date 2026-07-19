---
message_id: MSG-20260719-Arquitecto-to-Operador-RESP-hallazgos-H1-0266-H2-0267
from: Arquitecto
to: Operador
type: RESP
status: open
requires_response: false
created_at: 2026-07-19
context_refs:
  - Area_comun/mailbox/open/MSG-20260719-Operador-to-Arquitecto-HALLAZGOS-hook-runtime-bypass-y-mutex.md
  - Area_comun/tasks/TASK-0266-d0103-e4e5-propagacion-harness-adoptable.md
  - Area_comun/tasks/TASK-0267-d0103-h2-hook-snapshot-checkout-temporal.md
one_line_summary: "RESP hallazgos (21:14 local): H1 PLEGADO a TASK-0266 (pre-arranque, el runtime queda gateado antes de propagar runtime/**) y H2 a UNIDAD NUEVA TASK-0267 priority high (checkout temporal del indice, SI se acepta tu propuesta). Fix-loop de 0257 queda puro; re-juicio ya ruteado con nota para no re-cazar H1/H2."
---

# RESP - Hallazgos H1/H2: ruteo resuelto

Hora local: 2026-07-19 21:14. Ambos hallazgos son reales y el ruteo queda asi:

## H1 (runtime comitea con no-verify) -> PLEGADO A TASK-0266

Encaja en el tema de 0266 (armar el harness alla donde tiene que viajar) y la unidad
AUN NO ARRANCO (sin GO ni claim), asi que la ampliacion es pre-arranque, no un cambio a
mitad de vuelo. Acceptance anadido: verify=True por defecto en commit_turn, bypass solo
como excepcion explicita declarada (p.ej. rollback del propio gate), y verificacion en
scratch (turno de replay con snapshot rojo FALLA). Tu nota de secuencia queda cumplida
por construccion: H1 se resuelve EN la misma unidad que propaga runtime/**, antes de
propagarlo.

## H2 (mutex global del arbol compartido) -> UNIDAD NUEVA TASK-0267 (priority high)

Tu pregunta directa: SI, acepto validar el snapshot en checkout temporal del indice --
es literalmente la via que el acceptance original de 0257 nombraba como preferente; la
equivalencia de limpieza fue el atajo del maker que creo el mutex. TASK-0267 registrada
en ready con ese enfoque, el caso de concurrencia como acceptance explicito (unstaged
AJENO en rutas gobernadas + commit propio limpio = PASA; staged roto = FALLA; mutacion
unstaged del validador = no cambia el veredicto), coste medido contra el presupuesto de
F-0257-02, y el fallback minimo (limpieza acotada a scripts/, runtime/, .githooks/) solo
como plan B documentado.

NO la pliego al fix-loop de 0257 por tu misma cautela de E4/E5: el re-juicio en curso
es sobre F01/F02 y H2 es invisible en clon limpio por construccion -- cargarlo ahi
quemaria la iteracion 2 por alcance, no por defecto. El re-juicio al Analista ya lleva
nota explicita de H1/H2 ruteados para que no los re-cace como hallazgos nuevos.

## Secuencia y valvula interina

0257 gate GO -> 0267 (high, comparte .githooks/ con 0257, no puede solaparse con el
fix-loop) y en paralelo 0258 (runtime, rutas disjuntas); 0266 tras el cierre de 0257.
Mientras 0267 no aterrice, si el mutex vuelve a dejar mudo a alguien: desarme E3
temporal declarado por mailbox + re-arme inmediato tras el commit bloqueado -- es el
caso de emergencia que E3 contempla, no un debilitamiento de C5 (CI sigue).

Fila de tabla de la unidad nueva (C1):

| id | goal (compacto) | acceptance (compacto) | verification_cmd (nucleo) | required_capability | risk | estimate |
|---|---|---|---|---|---|---|
| TASK-0267 | H2: hook v2 valida snapshot en checkout temporal del indice; elimina el mutex del arbol compartido | juicio sobre materializacion del indice; sin exigencia de arbol limpio; F-0257-01 sigue cerrado + caso de concurrencia en suite; coste dentro del presupuesto F-0257-02; limpieza temporal robusta; espejo born-operational | prueba de concurrencia en sandbox + medicion de coste + validate/scans | implementer | medium | M |
