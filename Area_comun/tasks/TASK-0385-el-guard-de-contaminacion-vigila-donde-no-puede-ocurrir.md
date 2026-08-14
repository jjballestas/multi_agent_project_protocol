---
id: TASK-0385
title: El guard de contaminacion vigila el unico sitio donde la contaminacion es imposible -- CI clona limpio, el veneno vive en el arbol persistente
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0385-el-guard-de-contaminacion-vigila-donde-no-puede-ocurrir.md
created: 2026-08-14
reviewer: Analista
intake:
  type: fix
  goal: >
    Origen: anomalia DECISION-0018 levantada por el Analista el 2026-08-14 y confirmada por el
    Arquitecto de forma independiente. El arbol de trabajo vivo tenia
    `core.hooksPath = /tmp/task0364-poisoned-hooks`, un directorio de prueba de TASK-0364 que ni
    siquiera existe, asi que git no ejecutaba hook alguna: `.githooks/pre-commit` y
    `.githooks/commit-msg` llevaban DOS DIAS inertes para todo commit local de los tres agentes. Ya
    existe un guard contra exactamente esto en `.github/workflows/validate.yml:651-664`, que rechaza
    el run si `core.hooksPath` no es cadena vacia ni `.githooks` -- pero corre sobre el checkout de
    CI, que es un clon fresco y por tanto estructuralmente limpio. **El guard esta colocado en el
    unico sitio donde la contaminacion no puede ocurrir.** El envenenamiento solo existe en un arbol
    de trabajo PERSISTENTE, que es precisamente donde nada mira. Clase del defecto: un control
    correcto apuntando a una poblacion vacia -- pasa siempre, y su verde no significa nada.
  acceptance:
    - "AC1 (el control mira donde el fallo puede ocurrir): la comprobacion de `core.hooksPath` se
      ejecuta en el arbol de trabajo persistente, no solo en el checkout de CI. Se acredita
      envenenando `core.hooksPath` en un clon de sonda y comprobando por exit code que el control
      DICE QUE NO; y con el control historico: sin envenenar, exit 0."
    - "AC2 (prueba de que RECHAZA, con las tres formas del veneno): apuntar a un directorio
      INEXISTENTE (la forma real que ocurrio), apuntar a un directorio existente pero sin las hooks
      gobernadas, y apuntar a un directorio con hooks DISTINTAS de las gobernadas. Las tres con su
      salida y su exit code. Un control que solo caza el caso que ya conocemos no esta demostrado."
    - "AC3 (el control no depende de que alguien se acuerde de invocarlo): queda enganchado a un
      punto que se ejecuta solo en el flujo normal de trabajo -- el arranque del arnes de los peones
      es el candidato natural, porque es lo unico que corre en todo arbol persistente y en cada
      sesion. Se acredita mostrando el punto de enganche EJECUTADO, no declarado."
    - "AC4 (el diagnostico nombra el arreglo): el mensaje de rechazo imprime el valor encontrado y la
      instruccion literal de rearme (`git config core.hooksPath .githooks`). Se acredita por la
      salida del caso negativo."
    - "AC5 (no rompe los entornos legitimos): un checkout de CI limpio (hooksPath vacio) y un arbol
      correctamente armado (`.githooks`) siguen pasando sin pasos nuevos. Medido, no afirmado."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory"
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - .github/workflows/validate.yml
    - scripts/harness/peer_mailbox_cron.ps1
  out_of_scope:
    - "El contenido del gate de claim de producto (TASK-0378). Esta tarea NO juzga si el gate exige
      lo correcto: se ocupa de que el gate se EJECUTE. Son dos propiedades distintas y 0378 esta en
      review; ensancharla ahora repetiria el patron que esta cadena ya ha pagado tres veces."
    - "Limpiar el residuo concreto de TASK-0364 en el arbol del Arquitecto: ya rearmado a mano el
      2026-08-14 15:27 local. Lo que esta tarea entrega es que NO VUELVA a pasar inadvertido."
    - "Auditar que otras pruebas dejan estado global sin restaurar. Es la clase hermana y merece su
      propia tarea; aqui solo se cierra el vector de `core.hooksPath`."
  risk: medium
  estimate: M
---

# TASK-0385 -- el guard vigila donde no puede pasar

## Lo medido, por el Analista

Par que discrimina, sobre un clon de sonda con el MISMO commit y el MISMO mensaje invalido:

    ARM A  core.hooksPath = /tmp/task0364-poisoned-hooks   (el valor real del arbol vivo)
           -> el commit ENTRA. HEAD avanza.

    ARM B  core.hooksPath = .githooks
           -> RECHAZADO. HEAD no se mueve.
              "commit trailer gate: missing exact final trailer; write `Task-Id: TASK-XXXX` ..."

El brazo A era el estado del arbol de los tres agentes durante dos dias.

## Lo confirmado por el Arquitecto

El commit de cierre de TASK-0368 (`2d2eeb4d`) toco `runtime/state/` con su `Task-Id` y **paso porque
no corrio hook alguna**, no porque ningun gate lo aprobara. Es la forma pura de "mergeado no es
desplegado": el refuerzo de TASK-0378 se estaba entregando encima de un mecanismo apagado.

## Por que es tarea propia y no un parche

Porque el defecto no es el valor envenenado -- eso se rearma en un segundo. El defecto es que
**existia un control para esto y su verde no significaba nada**, por estar mirando una poblacion
estructuralmente vacia. Rearmar sin mover el control deja el mismo agujero esperando al siguiente
test que no restaure lo que toca.
