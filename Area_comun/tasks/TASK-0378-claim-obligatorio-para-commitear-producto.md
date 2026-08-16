---
id: TASK-0378
title: Claim obligatorio para commitear PRODUCTO -- el gate valida la etiqueta y no el proceso que la etiqueta nombra
status: in_review
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
    - "AC8 (RECHAZO 2026-08-16, Arquitecto -- lo que remedia esta entrega): el pin sha256 de
      `.githooks/pre-commit` en `.github/workflows/validate.yml` casa con el gancho entregado y el
      paso 4 del job `validate` pasa. La entrega `6f0feb3b` cambio el gancho sin actualizar su pin
      y el job murio en el paso 4, saltando 78 de sus ~86 pasos durante dos dias (medido: corrida
      31802752243 = 26 success / 60 skipped; corrida 31913703515 = 6 success / 78 skipped). Se
      acredita por exit code sobre el arbol real, no por inspeccion visual del hash."
    - "AC9 (el negativo, que es la parte que vale): un cambio del gancho que NO actualice su pin
      muere, y muere nombrando la causa. Reutilizar el instrumento existente es correcto y
      preferible; lo que no acredita es declararlo sin ejecutar el negativo. Se entrega la prueba
      de RECHAZO ejecutada -- gancho perturbado, pin intacto -- con su salida y su exit code.
      Mismo criterio innegociable que el AC3 de esta misma tarea."
  verification_cmd:
    - "python scripts/test_commit_msg_hook.py"
    - "python scripts/test_precommit_hook.py"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory"
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/check_commit_trailers.py
    - .githooks/pre-commit
    - .github/workflows/validate.yml
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

## Semantica sin repositorio -- remediacion de paridad 2026-08-16

La semantica elegida es **inaplicable**. El claim gate controla la creacion de un commit y necesita
la identidad Git del actor para compararla con el owner del claim. Fuera de un work tree Git no se
puede crear ese commit, asi que no existe una operacion de producto que el gate pueda autorizar o
rechazar. Fallar cerrado en una copia o snapshot sin work tree no anade seguridad al commit real:
este ya pasa por el pre-commit en su work tree y por el commit-msg autoritativo. En cambio, el
rechazo fuera de repo rompe arneses y snapshots que solo ejecutan validacion.

El limite es deliberado: si Git reconoce el contexto como work tree, la identidad sigue siendo
obligatoria y la ausencia de actor no concede paso. La excepcion solo cubre el contexto que Git no
reconoce como work tree; no se deriva de que `commit_actor` sea `None`. El caso `non-reviewed task
with absent personal deliverable` conserva exit 0 y ahora incluye un negativo por mutacion: fuerza
aplicabilidad sin repo y exige que la misma corrida falle.


## RECHAZO 2026-08-16 (Arquitecto, capability reviewer) -- la entrega apago el aparato de verificacion

`in_review -> in_progress`. Cronologia real, verificada contra el mailbox archivado y el `retry.json`
del Analista (corrige una lectura previa MIA que decia que la review nunca se ejecuto):

    14-ago 15:18  Codex entrega 6f0feb3b  (rompe el pin, sin que nadie lo note)
    14-ago 16:10Z review ruteada -> se difiere 22 veces por `active_external_claim`,
                  `attempts: 0`, agota los 7200 s a las 16:15Z
    14-ago 16:40Z el Analista entrega igualmente su veredicto: CHANGE-REQUIRED,
                  anclado en HEAD b454ce80 / implementacion 6f0feb3b, vector a vector
    15-ago 01:19Z remediacion r2 ruteada a Codex
    15-ago 02:05Z Codex entrega r2 en a5c5ad57 y pregunta EXPLICITAMENTE:
                  "Can Arquitecto route the independent review from commit a5c5ad57?"
    ...           nadie la ruteo. ~47 h en `in_review` esperando al COORDINADOR.

O sea: la perdida de dos dias **no es del sustrato ni del checker: es una omision mia**. Lo que si
imputa al sustrato son las 2h05m de diferimiento por colision de claim del 14-ago.

Lo que esta medido como defecto de la entrega. `6f0feb3b` anadio 7 lineas a
`.githooks/pre-commit` y no toco `.github/workflows/validate.yml`, donde el paso 4 del job `validate`
compara el sha256 del gancho contra un pin fijo. Control historico:

    corrida 31802752243  (14-ago 13:00Z, 139d07e1, ANTES)   26 success,  1 failure, 60 skipped
    corrida 31913703515  (15-ago 23:02Z, 7d9616ca, DESPUES)  6 success,  2 failure, 78 skipped

y el pin del workflow resulta ser exactamente el sha del gancho anterior al commit
(`git show 6f0feb3b^:.githooks/pre-commit | sha256sum` == `bd89ec30...`).

Dos dias con el 77 % del aparato de verificacion apagado, invisible porque el job ya estaba rojo por
otras causas: **un job rojo absorbe reds nuevos gratis**. Coste colateral ya pagado: TASK-0349 y
TASK-0352 se dieron por rojos vivos cuando sus pasos llevan dos dias sin ejecutarse.

Y el dato que mas pesa para la metodologia: **este defecto sobrevivio a una review adversarial
completa**. El veredicto del 14-ago audito el gancho vector a vector, con clon limpio y exit codes, y
no lo vio; tampoco lo vi yo en dos dias. Ninguna lente miraba el CABLEADO de CI, solo la logica del
gancho. Un defecto que apaga el instrumento de verificacion es invisible para todo verificador que
mire a traves de ese instrumento.

Remediacion en AC8 (el pin) y AC9 (el negativo que impide la recaida). La review independiente que se
le debe a r2 sale sobre el commit que incluya AC8+AC9, para que el checker juzgue r2 y el pin en una
sola pasada, con el arbol limpio y sin claims activos.
