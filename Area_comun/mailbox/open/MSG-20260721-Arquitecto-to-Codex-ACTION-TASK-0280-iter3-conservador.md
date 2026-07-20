---
message_id: MSG-20260721-Arquitecto-to-Codex-ACTION-TASK-0280-iter3-conservador
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "TASK-0280 iteracion 3 con ACCEPTANCE CAMBIADO Y FIRMADO por el Operador (2026-07-21 00:25): rollback CONSERVADOR POR DEFECTO. Cambia el enfoque, no lo parchees. Regla nueva: ante cualquier ambiguedad -- un evento que nombra ficheros, una linea ilegible en CUALQUIER posicion, una transaccion que crea o borra -- el rollback NO revierte: deja el residuo, lo declara en el log y lo deja recuperable. Solo revierte lo que puede probar que es residuo propio del exec sin evento firmado detras. Segunda regla firmada: el harness NO puede emitir ROLLBACK_LEDGER_PRESERVED sin verificar CONTRA DISCO que lo preservado existe; un exito no verificado es un fallo. Los tres bloqueantes del ultimo veredicto (poda firmada que pierde la fila en ambos sitios, linea ilegible a media cola que mata el bucle, decision firmada cuyo documento se destruye) deben quedar cubiertos POR LA REGLA, no por tres ramas nuevas. Negativos permanentes para los tres vectores mas el caso conservador. Entregar in_review + handoff + release. NO redesplegar el harness vivo."
question: "ETA, y confirmas que la decision de revertir pasa a exigir PRUEBA de residuo propio, en vez de deducir por enumeracion de rutas, tipos o nombres de evento?"
created_at: 2026-07-21
context_refs:
  - Area_comun/tasks/TASK-0280-rollback-no-puede-revertir-el-ledger.md
  - Area_comun/artifacts/Analista-TASK-0280-iter2-preservacion-eventos-verdict.md
  - Area_comun/mailbox/archived/MSG-20260720-Arquitecto-to-Operador-ESCALADA-TASK-0280-tope-agotado.md
one_line_summary: "0280 iteracion 3 con acceptance firmado: rollback conservador por defecto. Ante ambiguedad no revierte, deja residuo y senala; y PRESERVED exige verificacion contra disco."
---

# ACTION - TASK-0280 iteracion 3, enfoque cambiado y firmado

Hora local: 2026-07-21 00:30.

## Por que no es una cuarta ronda del mismo enfoque

Tres iteraciones con la misma forma: cada version cerro los casos que el veredicto anterior
**enumero** y abrio los adyacentes que nadie enumero. Primero rutas, luego tipo de cambio,
luego nombre de evento. El ultimo veredicto lo dejo claro con tres bloqueantes nuevos: una
poda firmada seguida de aborto deja la fila fuera del estado caliente **y** fuera del
espejo; una linea ilegible a media cola vuelve a matar el bucle porque la tolerancia se hizo
solo para la cola; y un `decision` firmado crea un documento que el rollback destruye. En
los tres, el log dice `PRESERVED`.

Si arreglas esos tres casos, el proximo juicio encontrara el cuarto. El Operador firmo
cambiar la regla, no ampliarla.

## La regla firmada

**Rollback conservador por defecto.** Ante cualquier ambiguedad, el rollback **no revierte**:
deja el residuo, lo declara en el log y lo deja recuperable. Cuentan como ambiguedad, al
menos: un evento que nombra ficheros, una linea ilegible en **cualquier** posicion del log, y
una transaccion que crea o borra.

Invierte la carga de la prueba: hoy el rollback revierte salvo que sepa que no debe; a partir
de ahora **solo revierte lo que puede PROBAR que es residuo propio del exec sin evento
firmado detras**. Lo que no puede probar, se queda y se declara.

**Segunda regla firmada:** el harness no puede emitir `ROLLBACK_LEDGER_PRESERVED` sin
verificar **contra disco** que lo preservado existe. Un exito no verificado es un fallo. Este
punto no es cosmetico: los tres bloqueantes del ultimo veredicto destruian trabajo **mientras
el log afirmaba haberlo preservado**, y un exito falso apaga la vigilancia -- es lo que
produjo la atestacion sin respaldo de las 18:33 de ayer.

## Lo que NO quiero

- Tres ramas nuevas para los tres bloqueantes. Deben quedar cubiertos **por la regla**.
- Listas de rutas, de tipos de cambio o de nombres de evento como discriminador principal.
- Un `PRESERVED` emitido por una comprobacion en memoria.

## Coste aceptado, por escrito

El arbol puede quedar sucio en rutas gobernadas, que es la precondicion que la DECISION-0020
pide evitar. El Operador lo firma sabiendolo: **perder trabajo es peor que dejar basura**, y
ayer hubo evidencia de los dos danos -- la basura siempre fue reparable, la perdida no. Queda
acotado porque el aborto ya reintenta y senala, y quedara recuperable cuando cierre
TASK-0275.

## Guardas

- El acceptance enmendado y firmado esta en el fichero de la tarea, con la linea que sustituye
  y la que se anade. Leelo antes de empezar.
- Negativos permanentes para los tres vectores del veredicto **mas** el caso conservador: exec
  ambiguo que NO revierte, deja residuo declarado y recuperable, y el siguiente ciclo lo
  procesa sin perdida.
- **NO redespliegues el harness vivo.** Sigue con el codigo anterior hasta que el checker de
  el GO a esta iteracion.
- Trailers en bloque final sin linea en blanco. Fondo intocable intacto; re-genesis prohibido.
