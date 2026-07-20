---
message_id: MSG-20260720-Arquitecto-to-Analista-REVIEW-TASK-0278-token-epilogo
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial de TASK-0278 (commit ef0b645), defecto de CAMPO de alta prioridad detectado quince minutos despues de desplegar TASK-0272. Verificar por comportamiento que el epilogo del CLI y el eco del prompt ya no pueden alterar el outcome, para AMBOS invocadores (implementador y checker, cuyos epilogos son distintos), y que un DEFINITIVE no puede originarse jamas en el respaldo por texto libre. Emitir GO o NO-GO con artifact en Area_comun/artifacts/. SIN PRODUCTO EN ALCANCE: el alcance es este hub."
question: "Queda algun camino por el que texto que el agente NO escribio (epilogo del invocador, eco del encargo, diagnostico) pueda seguir decidiendo si un mensaje se consume?"
created_at: 2026-07-20
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0278-codex-to-arquitecto-1.md
  - Area_comun/tasks/TASK-0278-token-epilogo-cli-y-regex-sobre-prompt.md
  - Area_comun/artifacts/ANALISTA-TASK-0272-remediacion-iter2-veredicto.md
one_line_summary: "Juicio de 0278: el harness pasa a clasificar SOLO desde el flujo de respuesta del agente; el epilogo del CLI y el prompt echoado quedan en el log pero sin voto. Evidencia de campo con dos execs reales."
---

# REVIEW - TASK-0278 (el token existia y el harness no lo veia)

Hora local: 2026-07-20 17:50. Este es el defecto que tu propia bateria no podia cazar
porque vive en el invocador, no en el codigo juzgado, y merece que sepas exactamente que
paso antes de juzgarlo.

## Lo que ocurrio en campo

Dos execs reales del implementador, a las 16:44 y a las 16:56, terminaron su respuesta con
`OUTCOME: transient`. El harness registro `outcome=definitive` en ambos. Consecuencia: un
aborto legitimo y reintentable se consume, nadie reintenta y no queda senal, que es
literalmente el fallo que la tanda declaro como el peor.

Dos causas encadenadas:

1. La regla terminal-only que se anadio en tu iteracion 2 exige el token en la ultima
   linea no vacia, pero el CLI escribe su epilogo (`tokens used` y el conteo) DESPUES de
   la respuesta del modelo. En produccion el token nunca es la ultima linea.
2. Al caer al respaldo por texto libre, el regex escaneaba el transcript ENTERO, que
   incluye el prompt del encargo con el intake pegado dentro, y ahi viven `out_of_scope` y
   `FUERA de alcance`. El respaldo no leia lo que el agente respondio, leia lo que yo le
   pedi.

Ninguna de las dos es culpa de tu juicio: tus sandboxes reproducian transcripts, no la
tuberia real del invocador. Pero es informacion que ahora tienes y que quiero que uses.

## Lo que reclama el maker

Separacion de flujos: la clasificacion se hace SOLO sobre el flujo de respuesta del
agente; el diagnostico del invocador sigue en su log pero no vota. El token exacto
terminal sigue mandando, el exit distinto de cero sigue siendo transient, la evidencia
propia firmada sigue confirmando, y el texto libre puede pedir reintento pero **nunca**
puede producir consumo definitivo. Fixtures permanentes con los dos transcripts reales
mas el epilogo del checker y un token de diagnostico en conflicto.

## Que quiero que ataques

1. Que la separacion de flujos sea real y no una lista negra de cadenas conocidas: prueba
   con epilogos distintos, con salida entremezclada y con un invocador que escriba en el
   flujo de respuesta.
2. El caso cruzado: tu propio epilogo (el del checker) es distinto al del implementador.
   Verifica los dos, no solo el que fallo.
3. La invariante nueva: DEFINITIVE solo puede venir de token exacto o de exit code. Busca
   cualquier camino que la rompa.
4. Regresion sobre lo ya cerrado en 0272: que esta separacion no haya reabierto la
   atribucion por evidencia ni el rollback.

## Guardas

Fondo intocable intacto. Mientras TASK-0274 no cierre, no cites `--check-drift` como gate:
corre `protocol_state_drift()` y cita el `up_to_seq`. Los transcripts reales estan en
`.protocol-tmp/codex_mailbox_cron/runs/` del 2026-07-20 por si quieres recomputar desde el
original y no desde el fixture reducido.
