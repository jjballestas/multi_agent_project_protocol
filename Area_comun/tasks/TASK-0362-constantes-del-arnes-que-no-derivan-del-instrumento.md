---
id: TASK-0362
title: Quedan dos constantes en la sonda que no derivan del instrumento, y una de ellas deja un caso pasando sin medir lo que dice
status: proposed
owner: Codex
file: Area_comun/tasks/TASK-0362-constantes-del-arnes-que-no-derivan-del-instrumento.md
type: fix
intake:
  type: fix
  goal: "Cerrar los dos residuales que TASK-0361 dejo declarados en `scripts/test_exec_lease_harness.py`. R2: la vida del worker de `retiring_child` sigue siendo un 3500 fijo y nadie acredita que el nieto se retirara ANTES de la segunda muestra, asi que en una maquina distinta el caso pasaria sin estar midiendo un hijo retirado -- verde que no discrimina, la misma clase que 0361 acaba de cerrar. R1: el 4500 de la formula es un duplicado a mano de los dos `Start-Sleep` de la sonda; desincronizarlos (segundo sleep 3000 -> 9000) deja la vida derivada quieta en 11844 ms y devuelve el delta cero."
  acceptance:
    - "AC1 (falsacion previa de R2): se acredita que hoy el caso `retiring_child` puede pasar SIN que el nieto se haya retirado antes de la segunda muestra, fabricando la condicion (encarecer el instrumento o alargar la vida del nieto) y mostrando que el caso sigue en verde. Medido, no argumentado."
    - "AC2 (R2, la vida del worker se DERIVA): la vida del worker de `retiring_child` se calcula del coste observado del instrumento, igual que ya hace el resto de la sonda tras 0361. Ninguna cifra fija elegida para que cuadre."
    - "AC3 (R2, se acredita el hecho que el caso presume): el caso afirma explicitamente que el nieto SE RETIRO antes de la segunda muestra, y si no fue asi falla con un diagnostico que lo diga -- no pasa en silencio ni devuelve un resultado indistinguible del caso sano."
    - "AC4 (R1, la geometria deja de estar duplicada a mano): el 4500 se deriva de los `Start-Sleep` reales de la sonda en vez de repetirlos. Se falsa cambiando SOLO uno de los sleeps y comprobando que la vida derivada se mueve con el; hoy no se mueve."
    - "AC5 (el verde DISCRIMINA): la bateria de 0361 se repite sobre este cambio -- codigo previo y codigo nuevo bajo el MISMO instrumento encarecido -- y el previo falla mientras el nuevo pasa. Un verde que ambas versiones comparten no acredita nada; asi lo demostro el checker en 0361."
    - "AC6 (sin regresion): `python scripts/test_exec_lease_harness.py` sale EXIT=0 en clon limpio CON HISTORIA COMPLETA en tres corridas consecutivas, reportando los casos de cada una, y ningun caso queda desactivado ni relajado."
  verification_cmd:
    - "python scripts/test_exec_lease_harness.py"
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - scripts/test_exec_lease_harness.py
  out_of_scope:
    - "R3 de TASK-0361 (el AC4 de aquella tarea quedo a nivel de test y no de asercion individual): declarado sin tarea, no se aborda aqui."
    - "AC5, la asercion sobre el desenlace y el residual R6 de TASK-0359: son propiedades del contrato de liveness y van en su vuelta 2."
    - "Acreditar nada en un run REAL de Actions: la facturacion sigue bloqueada."
  risk: low
  estimate: S
---

# TASK-0362 -- dos constantes que no derivan

Residuales declarados por el checker al ratificar TASK-0361
(`Analista-TASK-0361-vida-derivada-del-instrumento-verdict.md`). Ninguno bloqueaba el cierre de
aquella: R1 ya falla ruidosamente por su AC3, y R2 no rompe nada hoy.

## R2 -- el caso puede pasar sin medir lo que dice medir

La vida del worker de `retiring_child` sigue siendo **3500 fijo**, y nada acredita que el nieto se
retirara antes de la segunda muestra. En una maquina donde el instrumento cueste mas, el caso
**pasaria igual sin haber medido nunca un hijo retirado**.

Es exactamente la clase que 0361 acaba de cerrar, y sobrevive en el mismo fichero: un verde que no
discrimina. El checker lo recomendo como unidad propia y por eso esta aqui, en vez de enterrado como
cuarto punto de una remediacion de contrato.

## R1 -- la geometria esta duplicada a mano

El `4500` de la formula repite a mano los dos `Start-Sleep` de la sonda en vez de derivarse de ellos.
Desincronizados -- cambiando **solo** el segundo sleep de 3000 a 9000 -- la vida derivada no se mueve
(11844 ms) y vuelve el delta cero.

## Por que va DESPUES de la vuelta 2 de 0359

Comparten fichero. Dos unidades vivas sobre `test_exec_lease_harness.py` se serializarian de todos
modos por la admision scope-aware, asi que se hacen en orden: primero el contrato de liveness, luego
el arnes.
