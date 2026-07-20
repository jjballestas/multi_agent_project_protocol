---
message_id: MSG-20260720-Arquitecto-to-Operador-ESCALADA-TASK-0280-tope-agotado
from: Arquitecto
to: Operador
type: DECISION
status: archived
requires_response: true
response_owner: Operador
requested_action: "ESCALADA formal de TASK-0280 con el tope de dos iteraciones agotado. Se pide decision entre: (A) iteracion 3 con acceptance CAMBIADO a rollback conservador por defecto -- ante cualquier ambiguedad no revierte, deja residuo y senala -- mas la regla dura de que el log no puede emitir PRESERVED sin verificar contra disco; (B) iteracion 3 acotada solo a las dos regresiones enumeradas (dos rutas de archivo y la rama de poda, mas tolerancia a linea ilegible en cualquier posicion); (C) redesplegar el codigo actual asumiendo el riesgo documentado; (D) congelar 0280 y seguir con ventanas exclusivas hasta manana. El Arquitecto recomienda A. Cambiar el acceptance de una unidad ya aprobada requiere tu re-aprobacion por el candado E1, y por eso esto no se rutea solo."
question: "Autorizas A (rollback conservador por defecto, acceptance cambiado), o prefieres B, C o D?"
created_at: 2026-07-20
context_refs:
  - Area_comun/artifacts/Analista-TASK-0280-iter2-preservacion-eventos-verdict.md
  - Area_comun/mailbox/open/MSG-20260720-Operador-to-Arquitecto-COORD-0280-tope-agotado-sin-escalar.md
  - Area_comun/tasks/TASK-0280-rollback-no-puede-revertir-el-ledger.md
one_line_summary: "TASK-0280 agoto su tope: tres iteraciones cerrando los casos enumerados y abriendo los adyacentes. Se escala con recomendacion de cambiar el enfoque a rollback conservador por defecto, no de comprar otra ronda del mismo patron."
---

# ESCALADA - TASK-0280, tope agotado

Hora local: 2026-07-20 23:05 (reloj del sistema).

## Primero, mi fallo

El NO-GO se emitio a las 22:06 y la escalada sale ahora. Treinta y cinco minutos sin
recoger, con el arbol limpio y sin nadie bloqueado, pero fuera de la regla que yo mismo
declare: un tope agotado escala, y escala cuando ocurre. Estaba vigilando el exec del
checker y no volvi a mirar la bandeja cuando entrego. La cadena no se destrabo sola porque
tu la levantaste, que es justo lo que la guarda deberia hacer innecesario.

## Lo que se cerro y lo que no

**Cerrado y verificado por comportamiento:** el `mailbox_archive` firmado ya no pierde su
destino; la cola desgarrada difiere sin matar el bucle; los pre-sucios ajenos quedan
intactos. En dos vectores el codigo nuevo es **estrictamente mejor** que el que corre hoy.

**Bloquea:**

- **F-0280R2-01, regresion.** El conjunto de rutas derivadas de eventos no nombra los dos
  espejos de archivo ni tiene rama para `protocol_prune`. Una poda firmada seguida de un
  aborto deja la fila **fuera del estado caliente y fuera del espejo**: no existe en ningun
  sitio. El padre si la conservaba. Y el log dice `PRESERVED`.
- **F-0280R2-02, regresion.** La tolerancia se hizo solo para la cola: una linea ilegible a
  media cola vuelve a matar el bucle. El ladrillo no se cerro, se mudo.
- **F-0280R2-03, preexistente.** Un `decision` firmado crea un documento, el rollback lo
  destruye, y el log dice `PRESERVED`.

## El patron, que es lo que de verdad hay que decidir

Tres iteraciones con la misma forma: cada version cierra los casos que el veredicto
anterior **enumero** y abre los adyacentes que nadie enumero. Rutas, luego tipo de cambio,
luego nombre de evento. Siempre un discriminador nuevo, siempre un caso complementario
fuera. Una cuarta ronda del mismo enfoque compra el siguiente caso adyacente, no la
garantia.

Y el sintoma que mas me preocupa se repite en las tres: **el log afirma `PRESERVED`
mientras destruye**. Un exito falso es peor que un fallo, porque apaga la vigilancia. Es
exactamente lo que produjo la atestacion sin respaldo de las 18:33.

## Opciones

- **(A) Rollback conservador por defecto -- RECOMENDADA.** Ante cualquier ambiguedad (un
  evento que nombra ficheros, una linea ilegible en cualquier posicion, una transaccion que
  crea o borra) **no revierte: deja el residuo y senala**. Convierte tres bloqueantes en un
  residuo declarado y visible. El principio detras: perder trabajo es peor que dejar basura,
  y hoy tenemos evidencia de los dos danos, con la basura siendo siempre reparable y la
  perdida no. Incluye la regla dura de que el log **no puede emitir `PRESERVED` sin
  verificarlo contra disco**.
- **(B) Iteracion 3 acotada** a las dos regresiones enumeradas. Barata, y probablemente
  verde en el siguiente juicio, pero es la cuarta ronda del patron que acaba de fallar tres
  veces.
- **(C) Redesplegar el codigo actual** asumiendo el riesgo documentado. No la recomiendo: la
  poda es justamente lo que corro en cada checkpoint, y ese es el vector roto.
- **(D) Congelar 0280** y seguir con ventanas exclusivas hasta manana.

## Por que no lo decido yo

La opcion A **cambia el acceptance** de una unidad ya aprobada: pasa de "el rollback
preserva el ledger" a "el rollback no revierte ante ambiguedad y senala". Tu candado E1 dice
que una remediacion solo esta cubierta por la aprobacion original si conserva el mismo
acceptance, el mismo scope y el mismo risk. Este cambia acceptance y sube el residuo
aceptado, asi que necesita tu firma.

Hay ademas una opcion **B de medio plazo** que anoto sin pedirtela hoy: que el exec
**declare que va a escribir antes de escribirlo**, para que el rollback no deduzca sino que
consulte. Es unidad de diseno propia, no iteracion de esta.

## Situacion mientras decides

Nada en riesgo. El harness vivo sigue con el codigo anterior, mis escrituras de ledger van
en ventanas exclusivas con los crons parados, el arbol esta limpio, el validador verde y el
fondo intocable intacto. El coste es que el trabajo esta serializado.
