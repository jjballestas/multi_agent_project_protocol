---
message_id: MSG-20260720-Operador-to-Arquitecto-COORD-0280-tope-agotado-sin-escalar
from: Operador
to: Arquitecto
type: REQUEST
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "Procesar el NO-GO de la iteracion 2 de TASK-0280 (tope 2/2 agotado a las 22:06) y formalizar la escalada al Operador. Han pasado 35 minutos sin actividad ni mensaje de escalada, con el arbol limpio."
question: "El veredicto de 0280 iter2 esta procesado, o la cadena se quedo sin recoger otra vez?"
created_at: 2026-07-20
context_refs:
  - Area_comun/artifacts/Analista-TASK-0280-iter2-preservacion-eventos-verdict.md
one_line_summary: "TASK-0280 agoto su tope (NO-GO iter2 a las 22:06) y 35 min despues no hay escalada ni actividad, arbol limpio. Se pide procesar y escalar. Se adjunta la lectura del Asesor: tres iteraciones cerrando casos enumerados y abriendo los adyacentes, con el agravante de que el log afirma PRESERVED mientras destruye."
---

# COORD - 0280 con tope agotado y sin escalar

## El dato

- NO-GO de la **iteracion 2 de 2** emitido a las **22:06** (`91b585c`), memoria del checker
  a las 22:07.
- **Sin actividad desde entonces.** Son las 22:41.
- Arbol de trabajo limpio, `validate` verde, sin mensajes al Operador en `open/`.

Por la regla del propio equipo, un tope agotado escala. No ha ocurrido.

## Lo que cerro y lo que no (para que no se relea entero)

**Cerrado y verificado**: W2 (`mailbox_archive` firmado ya no destruye el destino), W3 (cola
desgarrada: `ROLLBACK_DEFER`, el exec siguiente ocurre, bucle vivo), W4 (pre-sucios ajenos).

**Bloquea**:
- **F-0280R2-01 (REGRESION)**: la poda firmada mueve una fila al archivo y tras el rollback
  **no existe en ninguno de los dos sitios**; antes el espejo la conservaba.
- **F-0280R2-02 (REGRESION)**: linea ilegible **en medio** del log vuelve a matar el bucle;
  la tolerancia se hizo solo para la cola.
- **F-0280R2-03 (preexistente)**: un `decision` firmado crea un documento, el rollback lo
  destruye y el log dice `PRESERVED`.

## Lectura del Asesor

Tres iteraciones con el mismo patron: cada version cierra los casos que el veredicto
anterior **enumero** y abre los adyacentes que nadie habia enumerado. Rutas -> tipo de
cambio -> nombre de evento. Siempre un discriminador nuevo, siempre un caso complementario
fuera.

Y el sintoma grave se repite: **el log afirma `PRESERVED` mientras destruye**. Un exito
falso es peor que un fallo, porque apaga la vigilancia -- es lo que produjo la atestacion
sin respaldo de las 18:33.

## Recomendacion que ya tiene el Operador

- **NO autorizar una tercera iteracion del mismo enfoque**: compraria el siguiente caso
  adyacente, no la garantia.
- **A (recomendada)**: rollback **conservador por defecto** -- ante cualquier ambiguedad
  (evento que nombra un fichero, linea ilegible en cualquier posicion, transaccion que crea
  o borra) **no revierte: deja residuo y senala**. Convierte tres bloqueantes en un residuo
  declarado. Perder trabajo es peor que dejar basura, y hoy hay evidencia de ambos danos.
- **B (a medio plazo)**: que el exec **declare que escribe** antes de escribirlo; entonces
  el rollback no deduce, consulta. Es unidad de diseno, no iteracion.
- **En cualquier caso**: prohibir que el log emita `PRESERVED` sin verificarlo contra disco.

## Nota

Si el veredicto ya esta procesado y solo falta el mensaje, contestame en una linea. Si la
cadena se quedo sin recoger, destrabala como las veces anteriores.

-- Operador
