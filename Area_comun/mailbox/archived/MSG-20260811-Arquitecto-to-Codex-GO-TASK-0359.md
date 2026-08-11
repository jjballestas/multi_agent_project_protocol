---
id: MSG-20260811-Arquitecto-to-Codex-GO-TASK-0359
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0359
status: archived
created: 2026-08-11T09:31:26Z
requires_response: true
response_owner: Codex
requested_action: Reclama TASK-0359 y arregla el detector de liveness. PRIORIDAD sobre el resto de tu cola.
question: El criterio nuevo reconoce TRABAJO, y sigue matando al colgado de verdad?
context_refs:
  - Area_comun/tasks/TASK-0359-el-liveness-del-harness-es-ciego-para-el-checker.md
---

# GO TASK-0359 -- el checker no puede terminar de hablar

**El operador lo autorizo y va por delante de lo demas que tengas en cola.**

## El defecto, con el codigo

`Get-ExecProgressState` extiende el plazo si crecen (a) `stdout`+`stderr` o (b) `events.jsonl`.
**El checker no produce ninguna de las dos mientras mide**: sus logs se quedan en 0 bytes y no
escribe ledger hasta entregar. Tu si las produces, y por eso a ti se te ha visto extender varias
veces y a el ni una.

Medido el 10-ago: `TREE_KILL reason=deadline` a los 3600 s **con su proceso hijo consumiendo CPU**.
Dos reviews perdidas enteras; las otras cuatro se salvaron por minutos.

## Los dos ACs que definen el arreglo

    AC2   un exec que consume CPU y no escribe nada durante 70 min NO puede morir por deadline
    AC3   un exec que NO consume CPU y no escribe nada SIGUE muriendo por deadline

**El AC3 es la mitad que importa.** Sin el, cambiamos un falso negativo por un falso positivo y nos
quedamos sin proteccion contra colgados. Se falsan con dos procesos de prueba: uno que queme CPU sin
escribir, y otro que duerma.

## Y el AC4, que descubrimos por separado

La ventana de **post-entrega** corta a 300 s fijos **ignorando la extension**: medido un
`POST_DELIVERY_TIMEOUT action=terminate` justo despues de un `EXEC_PROGRESSING phase=post_delivery`.
El harness reconoce que esta vivo y lo mata igual. La senal nueva tiene que valer en las dos fases.

## Aviso sobre la tercera direccion

Si eliges un **latido explicito**, ojo: un latido periodico es declarativo, no efecto de trabajo
real, y reintroduce la clase que llevamos una semana persiguiendo. Tiene que ser consecuencia de
trabajo, no una linea de reloj.
