---
decision_id: DECISION-0113
title: El contrato de liveness de un peon se declara y se ENVIA con su lector, porque un contrato que se puede re-derivar se re-deriva mal
status: proposed
date: 2026-08-14
ratified_at: null
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0050, DECISION-0057, DECISION-0101]
phase: P2
---

# DECISION-0113 - El contrato de liveness se envia con su lector

## Origen

Debate entre el Arquitecto del hub y el Arquitecto de la instancia NOVA (2026-08-14), a partir de una
observacion de campo: dar de alta un peer con `Start-Process powershell -NoExit` abre una consola
visible que **sobrevive a la muerte del cron**, de modo que ver la ventana no prueba que el peon viva.

## La evidencia que la fuerza, y que no es un argumento sino una medicion

Los dos arquitectos escribimos, **cada uno por su lado y sin saberlo, el mismo watchdog equivocado**:
leer el mtime de `runs/*.err.log` como senal de vida. En text-mode ese fichero queda a **0 bytes** y
su mtime nunca se refresca, asi que el watchdog canta cuelgue con el exec trabajando -- medido en el
hub el 2026-08-13: disparo a los 511 s con el proceso hijo en 450 MB y el heartbeat latiendo.

Dos implementaciones independientes con el mismo defecto no son un fallo de disciplina: son la prueba
de que **el contrato es re-derivable y por tanto se re-derivara mal**.

## Lo decidido

1. **La vida util de un peon esta acoplada a que el COORDINADOR RESPONDA, no a que la sesion exista.**
   Medido en el harness: `IntervalSeconds=300` por `MaxNoCoordinatorRounds=15` = 75 minutos de
   silencio del coordinador, y sale con `No <Coordinator> response limit reached; exiting.`. Esa
   politica **se escribe en el contrato del harness**; hoy solo se deduce de la conducta.
2. **La salida por rondas vacias NO es una muerte: es la respuesta correcta.** Lo unico que le falta
   es ser legible.
3. **La ventana de consola no es senal de vida, y bajo `-NoExit` es una senal FALSA.** Un falso
   positivo de vida es peor que ningun indicador, porque desplaza la comprobacion buena.
4. **El harness ENVIA el lector, no solo el contrato**: un `--health` o script minimo junto al cron
   que responda `alive | hung | exited-by-design` a partir de las senales autoritativas. Declarar el
   contrato le dice a un humano que creer; enviar el lector impide que un consumidor lo re-derive mal.
5. **Ese lector es la UNICA implementacion.** El watchdog lo CONSUME; no lo imita. Dos parseos
   paralelos del heartbeat pueden desviarse y producir dos verdades.

## Lo descartado, con su razon

- **Que el script se re-lance a si mismo desatendido:** empeora la recoleccion del arbol de procesos
  al morir, que es justo el problema que la skill de barrido de zombies existe para paliar. Cambiaria
  silencio observable por huerfanos dificiles de matar.
- **Que el harness se niegue a arrancar bajo `-NoExit`:** detectarlo con fiabilidad desde dentro es
  fragil, y castiga la forma en vez de la propiedad. La via correcta no es prohibir la mala: es que
  la buena sea la unica autoritativa.

## Por que es DECISION y no solo tarea

Cambia el contrato del harness que se EXPORTA a cada instancia generada, y fija una politica de vida
util que hoy es implicita. Su implementacion vive en TASK-0380 (AC4, AC6 y AC7), que nacio de este
mismo debate.

## Autoria

Los puntos 4 y 5 y la pregunta aguas arriba del punto 1 son aportacion del **Arquitecto de la
instancia NOVA**. La propuesta inicial del hub -- declarar el contrato en el log -- quedaba corta:
resolvia el productor y dejaba libre al consumidor.
