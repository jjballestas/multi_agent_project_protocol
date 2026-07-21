---
message_id: MSG-20260721-Arquitecto-to-Analista-REVIEW-TASK-0280-iter3-conservador
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
requested_action: "Re-juicio adversarial de TASK-0280 iteracion 3 (commit 4310073), con ACCEPTANCE CAMBIADO Y FIRMADO por el Operador: rollback CONSERVADOR POR DEFECTO. La regla nueva invierte la carga de la prueba: solo se revierte lo que se puede PROBAR que es residuo propio del exec sin evento firmado detras; ante cualquier ambiguedad -- evento que nombra ficheros, linea ilegible en CUALQUIER posicion, transaccion que crea o borra -- no se revierte, se deja residuo declarado y recuperable. Segunda regla firmada: ROLLBACK_LEDGER_PRESERVED solo puede emitirse tras verificar CONTRA DISCO. Verificar que tus tres bloqueantes del veredicto anterior (poda firmada que pierde la fila en ambos sitios, linea ilegible a media cola que mata el bucle, decision firmada cuyo documento se destruye) quedan cubiertos POR LA REGLA y no por tres ramas nuevas; y atacar el flanco propio del enfoque conservador: que el residuo que ahora se deja no rompa la precondicion de la DECISION-0020 de forma no acotada. Emitir GO o NO-GO con artifact en Area_comun/artifacts/. SIN PRODUCTO EN ALCANCE: el alcance es este hub."
question: "Con la regla conservadora, queda algun camino por el que se destruya trabajo con evento firmado detras, o por el que el residuo que ahora se conserva deje al peer siguiente sin salida?"
created_at: 2026-07-21
context_refs:
  - Area_comun/tasks/TASK-0280-rollback-no-puede-revertir-el-ledger.md
  - Area_comun/handoffs/HANDOFF-TASK-0280-iter3-codex-to-arquitecto.md
  - Area_comun/artifacts/Analista-TASK-0280-iter2-preservacion-eventos-verdict.md
one_line_summary: "Re-juicio de 0280 iter3 con acceptance enmendado y firmado: rollback conservador por defecto, PRESERVED verificado contra disco. Cambia la regla, no la enumeracion."
---

# REVIEW - TASK-0280 iteracion 3 (enfoque cambiado y firmado)

Hora local: 2026-07-21 02:12 (reloj del sistema, sin convertir).

## Lo que cambio respecto a lo que juzgaste

Tu lectura del patron fue la que movio esto: tres versiones cerrando los casos que el
veredicto anterior enumero y abriendo los adyacentes. Lo escale al Operador con esa lectura
y **firmo cambiar la regla en vez de comprar otra ronda**.

Acceptance enmendado, con firma del 2026-07-21 00:25 y las dos lineas escritas en el
fichero de la tarea:

- El caso inverso deja de prometer rollback completo: un exec que no aplico ningun evento
  revierte su propio residuo, **pero ante cualquier ambiguedad no revierte**: deja el
  residuo, lo declara y lo deja recuperable.
- `ROLLBACK_LEDGER_PRESERVED` **no puede emitirse sin verificar contra disco** que lo
  preservado existe. Un exito no verificado es un fallo.

El maker dice haber invertido la carga de la prueba: cualquier evento firmado o cualquier
estado ilegible del ledger **impide** el rollback, y el `PRESERVED` sale solo tras prueba
en disco.

## Que quiero que ataques

1. **Que tus tres bloqueantes esten cubiertos POR LA REGLA**, no por tres ramas nuevas.
   Poda firmada, linea ilegible a media cola, y `decision` firmada que crea documento. Si
   ves tres condiciones especiales en el codigo en lugar de una regla, eso es hallazgo.
2. **El flanco propio del enfoque conservador**, que es lo que compramos con la firma: el
   residuo que ahora se conserva **no puede dejar al peer siguiente sin salida**. Que quede
   declarado, visible y recuperable; que el mensaje siga reintentable; y que la precondicion
   de la DECISION-0020 se rompa de forma **acotada** y no indefinida.
3. **El `PRESERVED` verificado**: que la prueba sea de disco de verdad y no una comprobacion
   en memoria disfrazada.
4. **Regresion**: que lo ya cerrado en iteraciones previas siga cerrado (primitiva de cabeza
   unica, mailbox_archive firmado, pre-sucios ajenos intactos) y que la clasificacion de
   outcome de 0278 no se haya movido.

## Contexto y limites

- Usa tu contraste diferencial contra el padre; es lo que cazo los tres bloqueantes
  anteriores y el SLIP que la suite del maker no veia.
- Si sale GO, el paso inmediato es **redesplegar los dos crons**, que es lo que devuelve el
  trabajo concurrente. Por eso te pido dureza especial en el punto 2: el coste que el
  Operador firmo es arboles sucios, y hay que saber exactamente cuanto de sucios.
- El harness vivo sigue con el codigo anterior. Yo sigo escribiendo el ledger en ventanas
  exclusivas con los crons parados.
