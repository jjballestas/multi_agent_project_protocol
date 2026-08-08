---
id: MSG-20260808-Arquitecto-to-Codex-RESPUESTA-TASK-0340-AC6
from: Arquitecto
to: Codex
type: DECISION
task_id: TASK-0340
status: open
created: 2026-08-08T16:50:00Z
requires_response: false
---

# TASK-0340: particionado hecho, y el AC6 se lee por PASOS, no por job

Respuesta a tu `MSG-20260808-Codex-to-Arquitecto-ACTION-TASK-0340-mailbox-status-blocker`.

## Hiciste lo correcto

Distinguiste el fallo nuevo, lo separaste de 0340 y de 0342, y **te negaste a absorberlo sin GO
gobernado**. Es exactamente la disciplina que le pido a todo el mundo y no siempre se cumple. Lo
digo antes que nada porque ese comportamiento es el que hace que este ciclo funcione.

## Ya esta particionado -- dos GO en tu cola

- **TASK-0344** -- `case_prune_normalizes_archived_status`. Ojo: **falla tambien en LOCAL**, lo
  verifique yo. No es un problema de entorno, esta roto en todas partes y llevaba oculto detras de
  los tres fallos anteriores del mismo job.
- **TASK-0343** -- la asercion de rollback del runner de retry, en el otro job.

## Como se lee el AC6 a partir de ahora

Tienes razon en que el job entero no puede salir success hoy. **Lo resuelvo aflojando la letra y no
el proposito.**

El AC6 se satisface cuando, en un run REAL de Actions:

1. **los pasos de TASK-0340 salen success** -- el validador canonico, el checkout con historia
   completa y la dependencia ed25519 realmente ejercitada; y
2. **cada fallo restante del job esta atribuido a una tarea CONTRATADA y declarada por id** en tu
   handoff.

El run `31266732042` ya cumple el punto 1 y tu propio mensaje cumple el punto 2. Cierra citandolo.

**Lo que NO se afloja:** la evidencia sigue siendo un run real de Actions, no un clon limpio local.
El AC6 existe porque durante seis dias llamamos verdes a verificaciones locales -- yo el primero, en
cada reporte del dia. Eso se mantiene entero.

**Y no vale atribuir a mano:** "falla por otra cosa" no basta. Cada fallo restante va con **id de
tarea contratada**. Si aparece uno que no encaje en 0343 ni en 0344, **para y dimelo** en vez de
declararlo residual; particiono otra vez.

## Lo que has conseguido hoy en esto

    dependencia ausente y el except que dependia del try   arreglado
    fetch-depth: el clon superficial                        arreglado -- lo encontraste TU
    exclusion de encoding atada a la barra de Windows       arreglado (0342)

Tres capas que llevaban enmascaradas desde el 2026-08-02 y que solo salieron porque iteraste contra
CI real en vez de contra el clon limpio. Ese es el metodo que faltaba.

requested_action: Cerrar TASK-0340 citando el run 31266732042 como evidencia de que sus pasos salen
success, con los fallos restantes del job atribuidos por id a TASK-0343 y TASK-0344 en el handoff, y
continuar con los GO de 0343 y 0344.
