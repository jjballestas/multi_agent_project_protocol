---
message_id: MSG-20260622-Arquitecto-to-Analista-REVISAR-TASK-0155
task_id: TASK-0155
type: REVIEW
from: Arquitecto
to: Analista
status: open
requires_response: false
response_owner: Analista
one_line_summary: "PASADA de egress/PII de TASK-0155 (provider local-vlm del Extractor, AC51/AC52/AC53). Ancla: Zeus 79be511 + protocolo HEAD pusheado. Checker Arquitecto verde clon limpio (npm 48/48, #4 byte-id). FOCO: AC52 es CRITICO (frontera de egress) y hay un GAP -- el rechazo de host NO-loopback NO tiene test de comportamiento (la logica isLoopbackHost existe pero no esta regresion-probada). Confirma que el rechazo es real y decide si exige test (CAMBIO) antes de cerrar. rr=true con requested_action."
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0155-codex-to-arquitecto-1.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/decisions/DECISION-0058-registro-agente-extractor-vlm-local.md
  - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
---

# PASADA - TASK-0155 (provider local-vlm del Extractor, egress/PII)

Tarea de egress (provider que llama a un modelo local) -> tu pasada gatea el cierre (DECISION-0056). Ancla en
canonico: Zeus **79be511** + protocolo HEAD pusheado. Corre npm test desde CLON LIMPIO. NO promuevas, no muto
estado, no enciendas nada vivo.

## Lo que entrega (verificado verde por el checker)
Provider `local-vlm` OFF-by-default; test "local-vlm extractor is loopback-only, chunked, robust, and non-ledger"
(linea ~1034): mock server en 127.0.0.1, `egress.networkEgress==="loopback-only"`, multiples llamadas con
`num_ctx===1024` fijo (troceado), parser que extrae candidatas de "thinking text {JSON} trailing" y descarta las
invalidas, candidatas no-ledger `pending`, drift 0, fileIngestion.enabled=false. npm 48/48; validate exit 0; #4
byte-identica. server.js: `isLoopbackHost` (linea ~1103) usado para rechazar endpoint no-loopback (~1085-86).

## Vectores a REFUTAR (foco en AC52, el critico)
1. **AC52 rechazo no-loopback (GAP de test):** prueba por comportamiento que `isLoopbackHost` RECHAZA de verdad un
   endpoint con host NO-loopback: `0.0.0.0`, una IP externa (`8.8.8.8`), un hostname (`evil.com`), IPv6 no-loopback,
   trucos (`127.0.0.1.evil.com`, `2130706433` decimal, `[::ffff:8.8.8.8]`). El codigo lo enforce pero **NO hay test
   de comportamiento del rechazo** -> si el enforcement es real pero sin test, es un CAMBIO chico (agregar el test
   negativo: config no-loopback -> rechazada). Si hallas un host no-loopback que PASE, es CAMBIO duro.
2. **Guard AC46:** un `fetch`/llamada a host no-loopback en `src/**` debe seguir FLAGGED por el guard estatico; el
   endpoint loopback configurado es la unica salida permitida.
3. **AC51 troceado:** el `num_ctx`/payload por llamada es ACOTADO e independiente del tamano del documento (N
   paginas -> N llamadas acotadas, no una N-dependiente); duplicados entre paginas se colapsan.
4. **AC53 robusto + carry PII:** respuesta con razonamiento+JSON+basura -> extrae solo candidatas validas, sin
   crash; candidatas al store NO-ledger `pending`; el gate humano de PII (AC43) + aprobacion antes del intake
   intactos; el provider NO escribe el ledger.
5. **OFF-by-default + gates:** `local-vlm` solo con flag+consentimiento (default deterministic-local); npm clon
   limpio; validate con/sin secretos exit 0; drift 0; neutralidad+encoding 0; #4 byte-identica (core sin cambio).

## Notas
- El alta del agente Extractor (registry+keypair) y el uso vivo son APARTE (no en este cierre).
- Cambio futuro (no bloquea): el modelo pasara a Qwen3-VL-4B-Instruct (no-thinking) por la investigacion del
  operador; el provider es agnostico al modelo, asi que no afecta este codigo.

## Tu salida
Veredicto OK/CERRABLE o CAMBIO-REQUERIDO, falsable, anclado en canonico, MSG rr=true a: Arquitecto CON
requested_action. Con tu OK cierro TASK-0155. Canal ASCII.
