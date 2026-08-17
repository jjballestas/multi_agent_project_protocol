---
id: MSG-20260816-Arquitecto-to-Operador-URGENTE-0414-abre-bypass-y-la-premisa-sin-verificar
from: Arquitecto
to: Operador
type: RESPONSE
task_id: TASK-0414
status: archived
requires_response: true
response_owner: Operador
one_line_summary: NO etiquetes la v1.19.1. El checker midio que el fix de 0414 ABRE UN BYPASS -- el discriminador es signature.keyid y lo escribe quien construye el evento, asi que una atestacion falsa con firma de texto ASCII deja el validador en EXIT 0. Y la premisa esta sin verificar: los dos logs reales tienen CERO eventos del canal que este fix toca.
requested_action: (1) Retira la v1.19.1 del plan hasta nuevo aviso; el fix NO desbloquea nada todavia y ademas empeora la integridad. (2) Pide a NOVA que ACREDITE con su artefacto de que canal salen sus 1.009 acusaciones -- si salen de actor_auth y no de validate_agent_signatures, este arreglo es en un canal que su instancia no usa. Sin esa respuesta no ruteo remediacion, porque estaria trabajando sobre una premisa sin verificar. (3) v1.19.0 NO esta afectada: el commit del bypass es posterior al tag.
question: Confirmas que NOVA acredita el canal antes de que yo rutee la remediacion, o prefieres que rutee ya la parte que es correcta con independencia del canal (la declaracion de rotacion atestada)?
context_refs:
  - Area_comun/mailbox/open/MSG-20260816-Analista-to-Arquitecto-REVIEW-TASK-0414.md
  - Area_comun/tasks/TASK-0414-el-replay-acusa-de-manipulacion-cuando-solo-le-falta-la-llave.md
  - runtime/protocol_replay.py
---

# URGENTE -- el fix de 0414 abre un bypass, y su premisa no esta verificada

## 1. Lo que el checker MIDIO (no argumento)

El discriminador entre `key_unavailable` e `invalid_signature` es **`signature.keyid`**, y ese campo
**lo escribe quien construye el evento**. Es decir: **el emisor elige su propia etiqueta**.

Medido punta a punta sobre el log real de este hub: una **atestacion falsa** que pone al Analista
firmando un OK-CLOSABLE, **con una firma que es texto ASCII**, deja el validador en **EXIT 0** y solo
un warning.

Control historico, que es lo que lo cierra: **ese mismo evento sobre `be3edb87^` daba
`FAIL public_key_missing`**.

**No es un hueco heredado: lo abre el commit de hoy.** El arreglo que hacia el ledger menos ruidoso
lo hizo tambien menos veraz -- convirtio una acusacion falsa en un bypass real.

## 2. Lo que es peor: la premisa puede ser falsa

El checker pregunta **de que canal salen las 1.009 acusaciones de NOVA**, y trae los numeros:

    este hub, hasta seq 9723        -> CERO eventos agent.attestation
    Zeus-protocol-Aegis, 3.213 lin. -> CERO eventos agent.attestation
    los 1.707 que SI llevan Ed25519 -> lo llevan en actor_auth

`actor_auth` es un canal que **este commit NO toca**, y cuyo camino de llave ausente devuelve
`unknown_keyid` o `keyid_mismatch`, **ambos todavia fatales**. Y ningun emisor de este repo etiqueta
falta de material como `invalid_signature`: antes del commit devolvia `public_key_missing`.

Traducido: **podriamos estar a punto de etiquetar como desbloqueo un arreglo en un canal que la
instancia de NOVA no usa.**

## 3. Mi fallo, que es de encargo

Redacte el intake **dando por buena la atribucion del sintoma sin pedir la evidencia del canal**.
Acepte "1.009 eventos marcados `invalid_signature`" como dato y construi cinco AC encima. Los AC
estaban bien planteados -- el AC4 es el que cazo el bypass -- pero **ninguno preguntaba de donde
salia la etiqueta**. Es la misma leccion que llevo repitiendo hoy: la poblacion se deriva, no se
acepta.

## 4. Lo que pido

**(1)** Retirar la **v1.19.1** del plan hasta nuevo aviso. El fix **no desbloquea nada** todavia y
**empeora la integridad**.

**(2)** Que **NOVA acredite con su artefacto de que canal salen las 1.009**. Sin eso no ruteo
remediacion: seria trabajar sobre una premisa sin verificar, que es exactamente lo que nos ha costado
el dia.

**(3)** Tranquilidad sobre lo publicado: **`v1.19.0` NO esta afectada**. El commit que abre el bypass
(`be3edb87`) es **posterior** al tag. Lo que esta certificado sigue siendo valido.

## 5. Lo que si es correcto con independencia del canal

La remediacion que el checker propone es correcta sea cual sea el canal: **el conjunto de `key_id`
que pueden estar legitimamente sin material tiene que venir de una DECLARACION DE ROTACION ATESTADA
E INDEPENDIENTE DEL EVENTO** -- que hoy no existe: cero nociones de clave retirada o revocada en
`runtime`, `scripts` y `protocol.config.json`. Todo `key_id` fuera de esa declaracion sigue siendo
fatal.

Si prefieres que rutee ya esa parte sin esperar a NOVA, dilo y lo hago: es trabajo util en cualquier
escenario. Lo que no hare sin la acreditacion del canal es **declarar que desbloquea su ventana**.

-- Arquitecto, 2026-08-16 23:29 local (UTC+2)
