---
id: TASK-0425
title: El arnes suelta el lease de un exec que sigue VIVO -- descarta el veredicto del kill que el mismo calcula
status: ready
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0425-el-arnes-suelta-el-lease-de-un-exec-que-sigue-vivo.md
created: 2026-08-22
reviewer: Analista
intake:
  type: fix
  goal: >
    Stop-LeaseProcessTree DEVUELVE si el arbol murio de verdad: $false en TREE_KILL_INCOMPLETE
    (scripts/harness/peer_mailbox_cron.ps1:289), $false en TREE_KILL_FAIL (:295) y, en el camino
    feliz, la comprobacion viva "return (-not (Get-Process -Id $Lease.pid))" (:292). El arnes ya
    sabe usar ese veredicto: en la rama de lease huerfano (:339) escribe
    "if (-not (Stop-LeaseProcessTree ...)) { return }" y se abstiene. Pero en las DOS ramas de
    terminacion por plazo lo tira: :1643 y :1678 envuelven la llamada en [void] y hacen break
    aunque el kill haya fallado; el WaitForExit(2000) que sigue solo ESCRIBE
    TREE_KILL_WAIT_TIMEOUT y continua igual. Tras el break, el proceso sigue vivo, la lectura del
    codigo de salida no da un numero (de ahi el "EXEC_EXIT code= outcome=unconfirmed" que reporta
    la instancia NOVA, con el campo code VACIO), y el bloque finally (:1733-1734) borra el lease
    INCONDICIONALMENTE. Resultado: un exec vivo sin lease, y el ciclo siguiente arranca un SEGUNDO
    exec del mismo peer sobre el MISMO arbol. NOVA lo midio por pid y por crecimiento del err.log.
    Que el mismo fichero honre el veredicto en un sitio y lo descarte en otros dos hace de esto una
    OMISION, no una decision de diseno.
  acceptance:
    - "AC1: con el kill FALLIDO (Stop-LeaseProcessTree devuelve false) y el proceso aun vivo, el
      arnes NO borra el lease y NO admite un exec nuevo del mismo peer. Acreditar en banco con un
      proceso que sobreviva al kill, comprobando por pid que no arrancan dos."
    - "AC2: con el kill CORRECTO, la conducta actual no cambia: lease liberado y cola avanzando.
      Acreditar el par completo, no solo la rama que falla."
    - "AC3: el veredicto se consume en las TRES llamadas. Un negativo permanente debe morir si
      alguien vuelve a envolver :1643 o :1678 en [void]: la prueba perturba la PRODUCCION, no un
      doble del runner."
    - "AC4: cuando el kill falla, el suceso queda VISIBLE con su causa en el log del cron -- hoy
      TREE_KILL_WAIT_TIMEOUT se escribe y se ignora, que es peor que no escribirlo: parece
      atendido."
    - "AC5: el estado irresoluble (proceso vivo que no muere) NO se resuelve inventando un codigo
      de salida. Se declara como tal y se preserva el lease; el harness no puede afirmar un
      outcome de una tarea cuyo exec no ha terminado."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/harness/peer_mailbox_cron.ps1
    - scripts/
  out_of_scope:
    - "NO se toca la politica de plazos ni los tiempos de EXEC_HUNG: el defecto es que el veredicto
      del kill se descarte, no cuando se decide matar."
    - "NO se toca la clasificacion de outcome por fallo de proveedor: es TASK-0424."
  risk: high
  estimate: M
---

# TASK-0425 -- el arnes suelta el lease de un exec que sigue vivo

## La prueba de que es omision y no diseno

La misma funcion, tres llamadas, dos conductas:

    :339    if (-not (Stop-LeaseProcessTree -Lease $lease -Reason "orphan_expired")) { return }
    :1643   [void](Stop-LeaseProcessTree -Lease $lease -Reason "deadline")
    :1678   [void](Stop-LeaseProcessTree -Lease $lease -Reason "post_delivery")

En `:339` el arnes se abstiene si el kill fallo. En `:1643` y `:1678` decide lo contrario sobre la
misma pregunta. Cuando un fichero ya define el predicado mas fuerte en un sitio, la version debil
de al lado no es una eleccion: es un olvido.

## La cadena hasta el dano

    kill falla -> [void] lo descarta -> WaitForExit(2000) falla -> se ESCRIBE
    TREE_KILL_WAIT_TIMEOUT -> break igual -> el codigo de salida no existe (code= vacio) ->
    finally borra el lease -> el ciclo siguiente arranca otro exec sobre el mismo arbol

Dos execs del mismo peer escribiendo el mismo arbol es la condicion que las reservas de exec
existen para impedir. El lease no fallo: se solto a proposito sobre una premisa que el propio
arnes habia calculado como falsa y habia tirado.
