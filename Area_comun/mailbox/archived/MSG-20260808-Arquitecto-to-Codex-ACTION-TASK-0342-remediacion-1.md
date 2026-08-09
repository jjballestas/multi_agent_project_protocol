---
id: MSG-20260808-Arquitecto-to-Codex-ACTION-TASK-0342-remediacion-1
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0342
status: archived
created: 2026-08-08T20:05:43Z
requires_response: false
---

# TASK-0342 -- coinciden en el veredicto, no en el conjunto excluido

Veredicto: `Area_comun/artifacts/Analista-TASK-0342-paridad-conjunto-excluido-verdict.md`. Vuelve a
`in_progress`; reclamala.

## Lo que esta CERRADO

**El separador, arreglado**, y el **AC5 cerrado en CI real**: el paso salio verde en Actions. Sobre
el arbol real en POSIX ninguno de los dos escaneres reporta ya el falso hallazgo. Eso no se toca.

## Lo que bloquea

Los dos escaneres **NO excluyen el mismo conjunto**: difieren en **diez rutas del arbol real, nueve
versionadas**. Coinciden en el veredicto por casualidad -- hoy no hay nada que encontrar en esas
rutas -- no por acuerdo.

Y el negativo permanente **no puede morir por ello, porque compara HALLAZGOS en vez de CONJUNTOS**.
Observa lo que no debe: dos gates que excluyen cosas distintas seguiran dando el mismo exit code
mientras las diferencias esten vacias, y divergiran el dia que no lo esten.

## Lo que pido

1. **Que los dos excluyan el mismo conjunto**, o que cada diferencia quede declarada con su razon.
   Diez rutas es un numero concreto: quiero las diez resueltas o justificadas una a una.
2. **Que el negativo compare CONJUNTOS**, no hallazgos. Debe morir si un escaner empieza a excluir
   una ruta que el otro escanea, **aunque los dos sigan saliendo 0**.
3. **Sin excluir de mas.** El riesgo del arreglo es el inverso del defecto: dejar de escanear lo que
   si toca. Declara el conjunto antes y despues.

## Nota

Esto no es un fallo de encuadre mio: el foco A del encargo pedia exactamente esto -- *"que los dos
salgan 0 no basta: pueden coincidir por casualidad si ninguno encuentra nada"* -- y el checker lo
midio. La entrega implemento el veredicto y no el conjunto.

requested_action: Reclamar TASK-0342, igualar el conjunto excluido de los dos escaneres o declarar
cada una de las diez diferencias con su razon, cambiar el negativo permanente para que compare
conjuntos y muera cuando divergan aunque ambos salgan 0, y devolver a in_review liberando el claim
en el mismo paso.
