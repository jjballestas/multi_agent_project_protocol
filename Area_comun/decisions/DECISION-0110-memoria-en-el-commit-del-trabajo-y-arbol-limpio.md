---
decision_id: DECISION-0110
title: La memoria permanente viaja en el commit del trabajo, y el peligro del arbol compartido es la suciedad, no el commit
status: accepted
date: 2026-08-10
ratified_at: 2026-08-10
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0016, DECISION-0020, DECISION-0026, DECISION-0104]
phase: P2
---

# DECISION-0110 - La memoria en el commit del trabajo, y el arbol limpio

## Origen

Debate entre el operador humano y el Arquitecto en la sesion del 2026-08-10, convertido en decision
por instruccion expresa del operador. El debate partio de una pregunta sobre cuantas corridas de CI
genera la metodologia y termino corrigiendo dos creencias del Arquitecto que estaban mal.

## Contexto medido

**El volumen.** Del 06 al 10 de agosto: **595 commits** produjeron **400 corridas** de CI
(~1,5 commits por corrida). El reparto de los ultimos 40 commits: 12 de memoria, 8 de coordinacion,
7 de review, 3 de codigo. **Dos tercios del trafico es contabilidad de la metodologia**, no producto.

El ciclo completo de una tarea (TASK-0353, sin cerrar todavia) fue de **diez commits**, de los cuales
**uno** era codigo.

**Lo que se creia sobre el peligro del arbol compartido, y era falso.** Se venia asumiendo que
commitear mientras un peer ejecuta le destruye el trabajo, porque el log muestra
`ROLLBACK_DEFER reason=head_changed`. Leido el harness (`scripts/harness/peer_mailbox_cron.ps1`):

- `Get-ExecOutcomeClass` -- que decide `confirmed`/`transient`/`definitive` -- **no menciona HEAD
  ni una vez**. Clasifica por exit code, por una linea `OUTCOME:` que escribe el propio agente, o
  porque su salida casa con un patron de pre-gate (`claim ajeno`, `tree dirty`, `staged residue`,
  `cambios ajenos`).
- `Restore-TransientExecResidue` -- unico sitio donde se escribe `head_changed` -- solo se invoca
  **cuando el exec YA fallo**. Es una limpieza post mortem: si HEAD se movio, **se abstiene** de
  revertir para no pisar el commit ajeno.

Es decir: `head_changed` es una **consecuencia** de un exec ya fallido, nunca su causa. El disparador
real de los fallos es el **arbol de trabajo sucio**, que hace que el propio agente declare su
pre-gate en rojo.

**Lo que se creia sobre la memoria, y tambien era falso.** Se defendia el commit de memoria separado
porque "fue el unico artefacto superviviente de un exec que murio". Leido el rollback:

- `git read-tree $HeadBefore` restaura **solo el indice**. El comentario del propio harness lo dice:
  *"The shared worktree is never reset or re-applied."* Un fichero **rastreado y modificado**
  conserva sus cambios en disco.
- Los ficheros **nuevos sin rastrear** no se borran: se **mueven a cuarentena**
  (`.protocol-tmp/rollback-quarantine/<id>/`) con su ruta anotada en el log.
- Si el exec aplico un evento firmado, el arbol completo se **preserva** sin tocar nada.

La memoria local sobrevive a la muerte del proceso sin necesidad de commit. El proceso muere; el
disco no.

## Decision

**D1 -- La memoria permanente viaja en el MISMO commit que el trabajo que describe.**
Enmienda el *cuando* de DECISION-0026, no su invariante. La regla de oro sigue en pie y se refuerza:
un commit que toca rutas gobernadas y no lleva dentro su actualizacion de memoria esta incompleto.
Lo que se elimina es el commit de memoria **separado y posterior**.

**D2 -- La memoria caliente es local y no se commitea por si sola.**
La capa reciente de la memoria hibrida vive en local y solo se persiste al consolidarse, dentro del
commit de D1. **Requisito derivado del harness:** la memoria caliente debe escribirse sobre un
fichero **ya rastreado**. Un fichero nuevo sin rastrear seria movido a cuarentena por el rollback, y
el arranque siguiente lo buscaria en su ruta original sin encontrarlo. Sobre un fichero rastreado el
rollback solo toca el indice y el contenido en disco sobrevive intacto.

**D3 -- Los pasos de coordinacion se agrupan en un solo commit por unidad de trabajo.**
Alta de tarea + promocion + encargo van juntos; entrega + memoria van juntos; veredicto + memoria van
juntos. **El motivo vinculante no es el coste: es la correccion.** Separar el alta del ruteo permite
un estado en el que el mensaje ya existe en `Area_comun/mailbox/open/` y su fila todavia no existe en
el ledger; como el cron del peer **sondea el arbol de trabajo y no la historia de git**, publica el
encargo al instante y el peer arranca sobre una tarea inexistente. Ocurrio el 2026-08-10 con
TASK-0354. Agrupar hace ese estado **irrepresentable**.

**D4 -- El modelo de peligro del arbol compartido queda corregido, y con el la regla operativa.**
El peligro no es commitear: es **tener el arbol sucio**. Por tanto:

1. Se commitea **pronto**, para minimizar la ventana en que el arbol esta sucio.
2. Los borradores, mensajes en preparacion y temporales esperan **fuera del arbol**, bajo el scratch
   root de DECISION-0104, y entran al arbol en el mismo paso que su commit.
3. Queda derogada la practica de **esperar a que el peer este ocioso para commitear**: alarga
   exactamente el estado que le hace dano.

## Alcance

Aplica a todos los agentes registrados con area personal y a sus harnesses. No cambia el ledger, ni
las firmas, ni las puertas, ni la neutralidad de dominio del nucleo. No es un cambio incompatible.

## Consecuencias esperadas

Medido sobre el reparto real de commits: D1 + D3 quitan del orden del **30% de los commits** sin
eliminar un solo artefacto. A 1,5 commits por corrida eso se traslada casi entero a corridas de CI.
Combinado con la guarda de concurrencia de TASK-0354 (**45%** de las corridas hoy quedan superadas
por otra en menos de cinco minutos), el gasto esperado ronda **un tercio del actual**, sin tocar una
sola linea de cobertura.

## Lo que esta decision NO decide

- **Aislamiento por arbol de trabajo** (un worktree por agente). Elimina la clase entera del arbol
  sucio, pero **interactua con D2**: hoy la memoria caliente sin commitear es visible para los demas
  porque los tres comparten directorio; con arboles separados dejaria de serlo, y se perderia el
  canal por el que el Arquitecto se entero el 2026-08-10 de un defecto de produccion leyendo la
  memoria de un peer cuyo exec habia muerto. Las dos decisiones se toman juntas o no se toman.
- **Excluir `personal/**` de los disparadores de CI.** Los dos escaneres recorren el repo entero y
  si escanean esa ruta; excluirla quitaria cobertura real. La decision previa -- si `personal/` debe
  estar gateado -- queda abierta.
- El vocabulario del log del harness. `ROLLBACK_DEFER reason=head_changed` se lee como una
  cancelacion por culpa ajena y significa "no limpie por prudencia". Indujo un modelo causal falso
  durante una sesion entera y una herramienta construida encima. Merece correccion, en tarea propia.

## Implementacion

Esta decision fija la regla; no la cablea. El cableado en los prompts y harnesses de los tres
agentes va en tarea aparte, con su revision. Hasta que esa tarea cierre, la regla vincula por
conducta declarada y no por mecanismo.
