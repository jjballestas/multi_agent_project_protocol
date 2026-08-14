---
id: TASK-0386
title: El gate se fia de dos fuentes que el propio actor escribe -- una cadena de git config y una fila JSON sin commitear
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0386-el-gate-se-fia-de-fuentes-que-el-actor-escribe.md
created: 2026-08-14
reviewer: Analista
intake:
  type: fix
  goal: >
    Sale de la review de TASK-0378 (propiedades P-IDENT y P-LEDGER-CLAIM del veredicto). El gate de
    claim de producto responde a la pregunta "el claim es del actor que commitea?" leyendo DOS
    fuentes que el propio actor puede escribir sin dejar rastro atestado: (1) el actor sale de
    `git config user.name` (`check_commit_trailers.py:79-80`), que en un arbol de trabajo COMPARTIDO
    vale lo mismo para los tres agentes -- el Arquitecto midio un falso negativo (su claim activo
    rechazado) y el checker midio el falso positivo decisivo: commit de producto bajo el claim de
    OTRO, con `-c user.name=Codex`, exit 0 y HEAD movido, sin auto-clamarse; (2) el claim se lee de
    `Area_comun/state/CLAIMS.json` **del arbol de trabajo**, no del indice ni del estado commiteado
    -- el checker anadio una fila SIN stagearla, commiteo producto, exit 0, y
    `git show HEAD:Area_comun/state/CLAIMS.json | grep -c CLAIM-FABRICATED` da **0**: el commit
    entro bajo un claim que aparece cero veces en el ledger, sin evento, sin `submit_intent`, e
    indistinguible de uno legitimo para un auditor posterior. Ni siquiera hace falta un flag: basta
    un editor. Clase: **el control se fia de la etiqueta que el vigilado se escribe**, que es la
    misma enfermedad que TASK-0378 vino a cerrar, un piso mas abajo. NO cabe en el residual declarado
    de 0378 (que deja medio abierta la familia maker==checker porque un actor puede AUTO-clamarse):
    aqui el actor usa el claim AJENO, y el Punto 2 -- comprobar que el checker esta vivo -- no cierra
    eso, porque de nada sirve si el maker puede presentarse como el checker.
  acceptance:
    - "AC1 (P-IDENT): la identidad con la que el gate compara el `owner` del claim NO puede ser un
      valor que el actor escriba sin rastro atestado. Se acredita mostrando que muere el vector I1
      del veredicto: commit de producto bajo el claim de otro actor declarando su nombre. Por exit
      code y por movimiento de HEAD, no por nombre de test."
    - "AC2 (P-LEDGER-CLAIM): el claim que autoriza el commit debe existir en el estado GOBERNADO, no
      en el arbol de trabajo. Se acredita mostrando que muere el vector I2: fila de claim anadida al
      fichero sin stagear ni commitear. Comprobar ADEMAS que el claim legitimo -- creado por
      `submit_intent` y aun sin commitear, que es el estado normal en el instante del commit -- SIGUE
      pasando: si el arreglo exige que el claim este ya commiteado, rompe el flujo real de todos."
    - "AC3 (prueba de que RECHAZA, misma exigencia que 0378): los dos vectores entregan su rechazo
      EJECUTADO con salida y exit code, mas su control historico en verde. Un control que nunca ha
      dicho que no no esta demostrado."
    - "AC4 (no se cambia de sitio el agujero): la fuente nueva no puede quedar tambien bajo el
      control del actor. Se acredita nombrando la fuente y mostrando por que el actor no puede
      escribirla -- si la respuesta es 'no la escribe porque no deberia', no acredita."
    - "AC5 (el camino feliz sigue vivo): los tres agentes pueden commitear su trabajo legitimo en el
      arbol compartido sin pasos manuales nuevos por commit. Medido con un commit real de cada rol,
      no afirmado."
  verification_cmd:
    - "python scripts/test_commit_msg_hook.py"
    - "python scripts/test_precommit_hook.py"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory"
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/check_commit_trailers.py
    - .githooks/pre-commit
    - scripts/test_commit_msg_hook.py
    - scripts/test_precommit_hook.py
  out_of_scope:
    - "El perimetro de rutas de producto y la exencion de coordinacion: son TASK-0378, que sigue
      abierta con su remediacion propia. Esta tarea no toca DONDE aplica el gate, solo DE QUE se fia
      para responder quien."
    - "Rediseñar la identidad de los agentes en el arbol compartido (un arbol por agente, credenciales
      por proceso, etc.). Si el arreglo lo necesitara, se para y se pregunta: es cambio de topologia
      operativa y lo aprueba el operador."
    - "El Punto 2 de la DECISION del Operador (liveness de checker). Es la otra mitad de la familia
      maker==checker y va por su carril."
  risk: high
  estimate: M
---

# TASK-0386 -- el gate se fia de lo que el vigilado escribe

## Los dos vectores, medidos

**I1 -- identidad (Arquitecto y checker, por separado).**

    check_commit_trailers.py:79   def commit_actor(root): return git config user.name
    check_commit_trailers.py:89   if row.get("owner") != actor: continue

    arbol vivo:  user.name = Codex   (para los TRES agentes)

    falso negativo  claim propio activo, scope correcto  -> RECHAZADO
    falso positivo  `-c user.name=Codex`, claim de Codex -> exit 0, HEAD MOVED

**I2 -- el claim no necesita existir en el ledger (checker).**

    fila CLAIM-FABRICATED anadida a Area_comun/state/CLAIMS.json, SIN stagear
    commit de producto                                   -> exit 0, HEAD b454ce80 -> 652c7f1a
    git show HEAD:Area_comun/state/CLAIMS.json | grep -c CLAIM-FABRICATED  ->  0

## Por que se registra ANTES de cerrar 0378

Condicion explicita del checker, y la comparto: publicar el gate como "el claim es del actor que
commitea" cuando la identidad es un flag y el claim es una linea sin commitear seria publicar
exactamente lo que el hallazgo denuncia -- **un control que parece completo sin serlo**. Que salga a
tarea propia es aceptable; que salga sin registrar, no.

## Nota de registro

El propio veredicto que reporta I1 esta autorado por git como `Codex` estando firmado por el
Analista. Su commit es una instancia del defecto que reporta, y queda con su hash como la evidencia
mas directa de que esa fuente no distingue a nadie.
