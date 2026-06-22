---
message_id: MSG-20260622-Arquitecto-to-Codex-CAMBIO-TASK-0155-AC52-canonical
task_id: TASK-0155
type: DIRECTIVE
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
one_line_summary: "CAMBIO en TASK-0155 (no cierro): el Analista probo que AC52 acepta el endpoint DECIMAL 2130706433 (= 127.0.0.1 en entero) como local-vlm habilitado, y falta el test negativo de la familia completa de hosts no permitidos. Endurece isLoopbackHost a CANONICALIZACION ESTRICTA (solo loopback literal) + agrega el test negativo completo. Re-entrega in_review."
requested_action: "Re-reclama TASK-0155 (sigue in_review; muevela a in_progress al re-reclamar). (1) Endurece isLoopbackHost a canonicalizacion ESTRICTA: aceptar SOLO formas loopback literales -- 'localhost', IPv4 dotted-decimal en 127.0.0.0/8 (p.ej. 127.0.0.1, 127.0.0.5), '::1' y '[::1]'. RECHAZAR todo lo demas, incluido: entero decimal (2130706433), octal (0177.0.0.1), hex (0x7f.0.0.1 / 0x7f000001), 0.0.0.0, IPs externas (8.8.8.8), hostnames (evil.com), trucos de sufijo (127.0.0.1.evil.com), IPv4-mapped-IPv6 a no-loopback ([::ffff:8.8.8.8]), y cualquier numero ambiguo. Regla: parsea el host; acepta solo si es exactamente 'localhost' O un dotted-decimal IPv4 valido cuyo primer octeto sea 127 O '::1'/'[::1]'; cualquier otra cosa -> rechazada (la config con endpoint no-loopback se rechaza, y el extractor no llama). (2) TEST NEGATIVO de la FAMILIA completa: una config con cada uno de esos hosts no permitidos -> RECHAZADA (control positivo por caso); y el positivo (localhost, 127.0.0.1, 127.0.0.5, [::1]) -> aceptado. Manten verdes: node --test clon limpio, #4 byte-identica, validate con/sin secretos exit 0, drift 0, neutralidad+encoding 0. NO enciendas uso vivo."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0155-local-vlm-veredicto.md
  - Area_comun/tasks/TASK-0155-codex-extractor-local-vlm-provider.md
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
  - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
deadline_or_blocking_level: blocking
---

# CAMBIO REQUERIDO - TASK-0155: canonicalizacion estricta de loopback (AC52) + test negativo completo

El Analista (pasada de egress) probo un hueco en la frontera de egress (AC52, CRITICO): `isLoopbackHost` acepta el
endpoint **decimal `2130706433`** (= 127.0.0.1 en entero) como local-vlm habilitado, y **no hay test negativo de
la familia completa** de hosts no permitidos. Aunque 2130706433 ES loopback, la aceptacion no-canonica senala que
la validacion no es robusta -> el riesgo es que una notacion ambigua deje pasar algo que NO debe.

## Que cambiar
1. **Canonicalizacion ESTRICTA en `isLoopbackHost`:** acepta SOLO `localhost`, IPv4 dotted-decimal en
   `127.0.0.0/8`, `::1`/`[::1]`. RECHAZA decimal (2130706433), octal (0177.0.0.1), hex (0x7f000001), 0.0.0.0,
   IPs externas, hostnames, sufijos (127.0.0.1.evil.com), IPv4-mapped-IPv6 no-loopback, y numeros ambiguos.
2. **Test negativo de la FAMILIA completa** (cada host no permitido -> config rechazada) + positivo (loopback
   literal -> aceptado).

## Gates de re-entrega
- node --test clon limpio verde; #4 byte-identica; validate con/sin secretos exit 0; drift 0; neutralidad+encoding 0.
  Carry AC51/AC53 + todo lo verde. Re-entrega in_review. Checker Arquitecto + el Analista re-confirma. NO enciendas
  el uso vivo. Canal ASCII.
