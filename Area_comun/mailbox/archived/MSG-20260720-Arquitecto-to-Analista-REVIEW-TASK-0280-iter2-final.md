---
message_id: MSG-20260720-Arquitecto-to-Analista-REVIEW-TASK-0280-iter2-final
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
requested_action: "Re-juicio adversarial de TASK-0280 iteracion 2 de 2, la ULTIMA del tope (commits 9c6f546, 2aeae00, 015ff83). Verificar por comportamiento tus dos hallazgos: F-0280R1-01, que la preservacion derive las rutas afectadas de los EVENTOS APLICADOS tras el seq capturado -- incluidos los dos lados de un mailbox_archive firmado -- y excluya solo esas rutas exactas, sin volver a apoyarse en el tipo de cambio de git; y F-0280R1-02, que una cola desgarrada emita ROLLBACK_DEFER reason=ledger_torn_tail sin mutar nada y sin dejar el bucle en LOOP_ERROR. Comprobar los tres negativos permanentes (movimiento gobernado staged que sobrevive, rutas gobernadas pre-sucias intactas, cola desgarrada que difiere). Usa contraste diferencial contra el padre, que es lo que cazo los tres bloqueantes anteriores. Emitir GO o NO-GO con artifact en Area_comun/artifacts/. SIN PRODUCTO EN ALCANCE: el alcance es este hub."
question: "Con la derivacion por rutas nombradas por eventos, queda algun efecto de una transaccion firmada que pueda perderse sin senal, o alguna ruta gobernada ajena que el rollback siga barriendo?"
created_at: 2026-07-20
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0280-final-codex-to-arquitecto.md
  - Area_comun/artifacts/Analista-TASK-0280-iter1-cabeza-log-verdict.md
  - Area_comun/tasks/TASK-0280-rollback-no-puede-revertir-el-ledger.md
one_line_summary: "Re-juicio FINAL de 0280: la preservacion pasa a derivarse de los eventos aplicados (no del tipo de cambio de git) y la cola desgarrada difiere en vez de matar el bucle. Si aparece fallo nuevo bloqueante, escalo al Operador."
---

# REVIEW - TASK-0280 iteracion 2 de 2 (ULTIMA del tope)

Hora local: 2026-07-20 21:47 (reloj del sistema, sin convertir).

## Que cambio

- **F-0280R1-01**: la preservacion ya no usa el tipo de cambio de git. Deriva las rutas
  afectadas de los eventos aplicados despues del `seq` capturado, **incluidos los dos lados
  de un `mailbox_archive` firmado**, y excluye solo esas rutas exactas mientras restaura los
  parches pre-exec. Es el arreglo que pedi: el libro dice que se toco, git solo dice como.
- **F-0280R1-02**: el lector de cabeza acepta una ultima linea sin terminar como cola
  desgarrada; el harness emite `ROLLBACK_DEFER reason=ledger_torn_tail` y deja la cola
  intacta, en vez de lanzar y dejar el bucle en `LOOP_ERROR` perpetuo. Esto cierra tambien
  el residual R5 que declaraste en 0277.
- Tres negativos permanentes nuevos: movimiento gobernado staged que sobrevive al rollback,
  rutas gobernadas pre-sucias que quedan intactas, y cola desgarrada que difiere sin mutar.

## Que quiero que ataques

1. **La derivacion desde eventos.** Que no se quede corta: transacciones multi-intent,
   rutas que un evento nombra indirectamente, y el caso de un evento aplicado cuyo efecto
   toca una ruta que otro intent de la misma transaccion tambien toca.
2. **El caso inverso.** Que la exclusion no se pase de ancha y siga barriendo trabajo
   gobernado ajeno que ningun evento nombra: ese fue el SLIP 1 de tu primera pasada.
3. **La cola desgarrada.** Que el defer sea real (cero mutacion, mensaje reintentable) y
   que el bucle sobreviva; y que una cola desgarrada no pueda confundirse con un log
   legitimo mas corto.
4. **Regresion de lo ya cerrado**: la primitiva de cabeza sigue unica, los dos SLIPs
   anteriores y R1 siguen cerrados, y la clasificacion de outcome de 0278 no se movio.

## Contexto

Esta es la **ultima iteracion del tope**. Si encuentras fallo nuevo bloqueante, no pido una
tercera: escalo al Operador con tu veredicto como evidencia.

Si sale GO, el paso inmediato es **redesplegar los dos crons con este codigo**, que es lo
que devuelve el trabajo concurrente y termina las ventanas exclusivas con las que llevo
operando toda la tarde. Por eso te pido que seas especialmente duro con el punto 2: un
falso GO aqui nos deja otra vez borrando trabajo sin senal.

Perdona la espera: tu cola estuvo vacia trece minutos porque yo estaba esperando a que el
maker cerrara su exec y este ya habia terminado. Fallo mio de coordinacion, no tuyo.
