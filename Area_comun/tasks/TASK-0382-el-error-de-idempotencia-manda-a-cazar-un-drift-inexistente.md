---
id: TASK-0382
title: El error de idempotencia no nombra la clave que colisiona y manda a diagnosticar un drift que no existe
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0382-el-error-de-idempotencia-manda-a-cazar-un-drift-inexistente.md
created: 2026-08-14
reviewer: Analista
intake:
  type: fix
  goal: >
    Leccion 1 del informe de campo de la instancia NOVA, verificada por mi en el fuente del hub.
    `transaction_event_keys` (`runtime/submit_intent.py:727`) deriva la clave de idempotencia del
    CONTENIDO normalizado del intent. En un bucle de remediacion, el `task_status` que devuelve una
    tarea de `in_review` a `in_progress` es byte a byte identico al de la vuelta anterior, asi que
    colisiona SIEMPRE a partir de la segunda iteracion. Como el resto de intents de la transaccion si
    son nuevos, la coincidencia es PARCIAL y `submit_intent.py:1428` lanza
    `partial transaction idempotency state exists; refusing to continue`. Ese mensaje no nombra la
    clave, no dice que la transicion ya ocurrio, y no sugiere la salida -- de modo que el operador del
    ledger sigue el procedimiento de recuperacion de drift (tail de eventos, comparar intent_count,
    verificar estado fisico) sobre un ledger impecable. Es un fallo sin diagnostico en la herramienta
    que TODOS usan, y penaliza a quien no conoce el truco de pasar `idempotency_key` explicita.
  acceptance:
    - "AC1 (el mensaje nombra la causa, no la consecuencia): cuando la coincidencia sea parcial, el
      error identifica QUE clave o claves ya existen, a que intent corresponden, y declara la causa
      probable -- esa transicion ya ocurrio -- junto con la salida concreta: pasar `idempotency_key`
      explicita por intent. Se acredita provocando la colision y leyendo el mensaje: si el mensaje no
      basta para actuar sin abrir el codigo, no acredita."
    - "AC2 (el negativo discrimina): un estado PARCIAL de verdad -- una transaccion que murio a
      medias -- sigue produciendo un error que manda a diagnosticar, y sigue siendo distinguible del
      caso benigno de la repeticion. Se mide con el PAR: colision por repeticion y corte real a
      mitad. Si los dos dan el mismo texto, el arreglo no sirve."
    - "AC3 (medido sobre el caso REAL que lo destapo): se reproduce la secuencia del bucle de
      remediacion -- devolver la misma tarea de in_review a in_progress dos veces -- y se comprueba
      que el mensaje nuevo permite resolverlo a la primera. Es el caso que hizo perder tiempo en la
      instancia; se cierra contra el, no contra un ejemplo inventado."
    - "AC4 (no se toca la garantia): la idempotencia sigue protegiendo lo que protege. Un reenvio
      identico completo sigue siendo idempotente y no duplica eventos. Se acredita con el control."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory"
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - runtime/submit_intent.py
  out_of_scope:
    - "Cambiar la derivacion de la clave para que incluya la ocurrencia: es una alternativa que el
      informe menciona, pero toca la garantia de idempotencia y merece decision propia si se quiere.
      Esta tarea arregla el DIAGNOSTICO, que es lo que hace dano hoy."
    - "El self-filter por sesion y la exigibilidad del lease: es TASK-0383."
  risk: low
  estimate: S
---

# TASK-0382 -- el error que envia a buscar una averia que no existe

## Verificado en el fuente antes de escribir la tarea

    runtime/submit_intent.py:727   transaction_event_keys -> idempotency_key(actor_id, normalized)
    runtime/submit_intent.py:1428  if len(existing) != len(keys):
                                       raise "partial transaction idempotency state exists"

La clave sale del contenido. En un bucle de remediacion la transicion se repite POR DISENO, asi que a
partir de la segunda vuelta una clave vieja convive con varias nuevas: coincidencia parcial, y el
error salta.

## Por que importa mas que su tamano

El mensaje describe el SINTOMA que el codigo observa -- hay estado parcial -- y no la causa que lo
produjo. Quien lo recibe hace lo correcto: seguir el procedimiento de recuperacion de drift. Y lo
hace sobre un ledger sano.

Es la misma familia que llevamos semanas desterrando: **un fallo sin diagnostico manda a mirar donde
no esta**. Aqui con un agravante -- ocurre en la herramienta por la que pasa toda transicion de
estado, y el que ya conoce el truco de la clave explicita no lo sufre nunca, asi que el defecto solo
lo paga quien menos contexto tiene.
