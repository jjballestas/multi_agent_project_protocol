---
id: TASK-0378
title: Claim obligatorio para commitear PRODUCTO -- el gate valida la etiqueta y no el proceso que la etiqueta nombra
status: in_progress
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0378-claim-obligatorio-para-commitear-producto.md
created: 2026-08-14
reviewer: Analista
intake:
  type: fix
  goal: >
    Punto 1 de la DECISION del Operador del 2026-08-14, prioridad declarada y bloqueante. Diagnostico
    en una linea: el gate valida la ETIQUETA, no el PROCESO que la etiqueta nombra. Comprobado en
    campo por la instancia NOVA: dos commits de producto (~1.200 lineas) entraron a main bajo una
    tarea con CERO claims activos, cero eventos de ledger, la tarea sin moverse de `in_progress`, sin
    review de nadie y el mismo actor de maker y checker -- y pasaron TODOS los gates en verde, con su
    `Task-Id` correcto. Medido por mi en el nucleo del hub: `scripts/check_commit_trailers.py` tiene
    96 lineas, lee `TASK_INDEX` tres veces y menciona `claim` CERO veces; `.githooks/pre-commit`
    tiene 193 lineas y menciona `claim`, `owner` o `maker` CERO veces. O sea: el claim y la
    separacion maker/checker se exigen para escribir el ESTADO gobernado y no para escribir el
    PRODUCTO -- el codigo queda fuera del perimetro de control, que es justo donde viven el valor y
    el riesgo. Es el CUARTO defecto de la misma familia; los tres previos eran gates rotos, este es
    un gate que no existe.
  acceptance:
    - "AC1 (el requisito, en el gate AUTORITATIVO): si el mensaje de commit lleva `Task-Id:
      TASK-XXXX`, `scripts/check_commit_trailers.py` exige que esa tarea tenga claim ACTIVO del actor
      que commitea, leyendo `TASK_INDEX.json` y `CLAIMS.json`. Se acredita con los CUATRO casos por
      exit code: RECHAZA con `Task-Id` sin claim; RECHAZA con claim de OTRO actor; ACEPTA con claim
      propio activo; NO exige nada con `Task-Id: none` mas `Ops-Reason`."
    - "AC2 (el mismo requisito, en el gancho LOCAL): `.githooks/pre-commit` rechaza fail-closed en el
      instante del commit, con los MISMOS cuatro casos y su propia prueba de rechazo. Reutilizar la
      logica del AC1 es correcto y preferible; lo que no acredita es declarar que el hook la hereda
      sin ejecutarla desde el hook.
      ENMIENDA 2026-08-14 (Arquitecto, tras el veredicto del checker; defecto MIO de redaccion):
      exigir al gancho local los MISMOS CUATRO casos era IMPOSIBLE de cumplir. Un `pre-commit` corre
      ANTES de que exista el mensaje del commit, asi que el caso 4 -- `Task-Id: none` mas
      `Ops-Reason` -- es irrepresentable ahi: el gancho decide con rutas staged, actor y claims, y
      ninguno de los tres es el mensaje. Codex no lo omitio por descuido; no podia. El AC queda
      REFORMULADO asi: el gancho local exige claim propio activo cuando hay rutas de PRODUCTO
      staged, y no exige nada cuando no las hay -- criterio que si puede evaluar. La exencion de
      coordinacion por `Task-Id: none` mas `Ops-Reason` se acredita SOLO en el gancho autoritativo
      (AC1), que si ve el mensaje. Los tres casos restantes del AC1 siguen exigidos en ambos."
    - "AC7 (ENMIENDA 2026-08-14, Arquitecto -- la frontera del perimetro, que el checker me pidio
      decidir): `runtime/state/` NO es perimetro de producto. Es el LEDGER, del mismo genero que
      `Area_comun/state/`, y la propia tarea excluye bloquear los commits de coordinacion. El resto
      de `runtime/` si lo es. Se acredita midiendo que un commit de transaccion gobernada que toca
      solo `runtime/state/` aterriza sin claim de producto, y que un commit que toca `runtime/` fuera
      de `state/` sigue exigiendolo."
    - "AC3 (2f por partida doble: prueba de que RECHAZA, no de que pasa): cada gancho entrega su
      propia evidencia de rechazo, ejecutada, con la salida y el exit code de los casos negativos. Un
      control que nunca ha dicho que no NO esta demostrado -- es el criterio innegociable de la
      DECISION y el motivo de que esta tarea exista."
    - "AC4 (nace con la derivacion de prefijo de instancia, o repite el defecto 1): los DOS ganchos
      derivan el prefijo de la instancia en vez de comparar rutas contra `Area_comun/` a pelo. En el
      modelo 2.A git devuelve rutas como `Aegis/...` y la comparacion cruda deja los gates CIEGOS --
      es el defecto 1 ya corregido en la instancia (`eb440d6`). Cuando la instancia ES el repo (caso
      del hub) el prefijo es cadena vacia y el comportamiento no cambia. Se acredita con los dos
      casos: prefijo vacio y prefijo no vacio."
    - "AC5 (el camino feliz no paga ceremonia): un commit legitimo con claim propio activo pasa sin
      pasos nuevos, y un commit de coordinacion con `Task-Id: none` mas `Ops-Reason` sigue pasando
      igual. Se acredita midiendo los dos, no afirmando que no se anadio friccion."
    - "AC6 (el incidente reportado habria sido frenado): se reproduce la forma del incidente -- commit
      de producto bajo una tarea sin claim activo -- y se comprueba que AHORA muere, en los dos
      ganchos, nombrando la causa."
  verification_cmd:
    - "python scripts/check_commit_trailers.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory"
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/check_commit_trailers.py
    - .githooks/pre-commit
  out_of_scope:
    - "La separacion maker/checker en la ENTREGA: el Punto 1 para el incidente reportado (tenia cero
      claims) pero por si solo deja MEDIO ABIERTA la familia maker==checker, porque un actor puede
      auto-clamarse y commitear. Eso lo cierra el Punto 2 (liveness de checker como paso 0), y va en
      tarea aparte. Esta limitacion se declara EXPLICITAMENTE en la nota de version -- orden del
      Operador -- para no publicar justo lo que el hallazgo denuncia: un control que parece completo
      sin serlo."
    - "Los Puntos 2 y 4 de la DECISION: se coordinan con el tablero F2/F3 de la memoria hibrida, no
      por riesgo de esquema (esta congelado) sino porque insertan logica en la misma secuencia de
      cold-start y semantica de estado que F2/F3 reescriben."
    - "Bloquear trabajo exploratorio o commits de coordinacion: limite explicito de la DECISION."
    - "La nota de version y su adopcion por `upgrade_instance.py`: entregable de la DECISION, pero se
      redacta cuando el gate este acreditado, no antes."
  risk: medium
  estimate: M
---

# TASK-0378 -- el gate que no existe

## Lo que paso en campo

Dos commits de producto, unas 1.200 lineas, a `main`:

    Task-Id correcto            ->  el gate lo aprueba
    claims activos              ->  0
    eventos de ledger           ->  0
    la tarea                    ->  sin moverse de in_progress
    review                      ->  ninguna
    maker y checker             ->  el mismo actor

Y **todos los gates en verde**. No fallo ningun control: es que ninguno miraba.

## Lo que medi yo en el nucleo del hub

    scripts/check_commit_trailers.py   96 lineas   menciones de "claim": 0   lee TASK_INDEX: si
    .githooks/pre-commit              193 lineas   menciones de claim/owner/maker: 0

El gate autoritativo comprueba que el `Task-Id` EXISTE. No comprueba quien puede trabajar esa tarea.
El claim se exige para escribir el ESTADO y no para escribir el CODIGO.

## Por que en los DOS ganchos

Decision de diseno del Operador, y la razon es simetrica:

    solo en el hook          ->  advertencia: --no-verify lo salta, o falta en el clon
    solo en el trailer-check ->  rechaza TARDE, cuando el commit ya existe
    en los dos               ->  inmediato E imposible de saltar

Por eso el AC3 pide **dos** pruebas de rechazo y no una: cada gancho tiene que decir que no por su
cuenta.

## La trampa al portar

El AC4 no es burocracia. En el modelo 2.A git devuelve rutas como `Aegis/...` y el nucleo las
comparaba contra `Area_comun/`: gates ciegos. Es el defecto 1 de esta misma familia, ya corregido en
la instancia. Un gate nuevo que nazca comparando a pelo repite el defecto el dia que alguien
instancie.

## El criterio que gobierna la tarea entera

**Un gate que nunca ha dicho que no, no esta demostrado.** Para cada control, la evidencia es el
RECHAZO -- no el paso.
