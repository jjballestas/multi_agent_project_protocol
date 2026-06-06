# ANALISIS - N-agent readiness (escalado a 3+ agentes)

> Estado: ANALISIS / backlog. **NO es prioridad hasta despues de M2** (runtime autonomo con escritor
> unico). Prerrequisito explicito: cerrar M2; revisar despues. Autor: Claude (arquitecto), 2026-06-06.
> Neutral (tooling/proceso). No introduce dominio.

## Pregunta
Si hubiese un 3er agente (otra IA ademas de Claude/Codex), el protocolo funcionaria igual?

## Respuesta corta
El **diseno** es mayormente agente-agnostico y escala; la **instancia actual** esta hardcodeada a 2
agentes y tiene dos debilidades fisicas/operativas que con 3 agentes se amplifican. Los fallos que esta
sesion (2 agentes) expuso -colisiones, drift de status, stalls, mensajes olvidados- son exactamente los
que romperian con 3. Los arreglos en curso (gates + runtime single-writer) son justo lo que habilita N.

## Lo que SI escala (invariantes agente-agnosticos)
- **Claims con scope por fila (DECISION-0011):** cualquier owner reclama rutas; el chequeo de solape no
  cuenta agentes. 3 agentes = mas claims, misma logica.
- **Tasks / mailbox / handoffs:** point-to-point por `owner`/`from`/`to`; no asumen cardinalidad 2.
- **Gates de esta sesion** (encoding/ASCII DECISION-0012, handoff-release + liveness DECISION-0013,
  mailbox status<->carpeta SPEC-0034, poda sistematica DECISION-0014): verifican INVARIANTES de estado,
  no agentes concretos -> protegen a N agentes igual. Esta es la parte que ya generaliza.

## Lo que NO escala hoy (bloqueos concretos)
1. **Roster hardcodeado.** El enum `owner` del validador y de los ledgers es `[Claude, Codex, operador
   humano]`; la tabla de roles (AGENTS.md sec3) es fija. Un 3er agente lo RECHAZA el validador. Es
   2-agentes-instanciado, no N-agentes-generico. Fix: roster config-driven (lista de agentes + roles en
   `protocol.config`), validador que lee el roster en vez de un enum fijo.
2. **Contencion fisica en JSON compartidos (cuello de botella real).** `CLAIMS.json` y los ledgers de
   estado son ficheros unicos escritos en concurrente. Con 2 agentes ya hubo races constantes ("file
   modified since read") toda la sesion. Con 3 se multiplican. El protocolo asume "escritor unico =
   orquestador" para atomicidad, pero el modo manual lo viola. Fix: runtime single-writer (M2) y/o
   shardear estado de alta contencion (claims por-agente / logs append-only).
3. **Coordinacion = convencion, no enforcement.** "Comprobar CLAIMS antes de escribir", handoff-release,
   mover-y-actualizar-status: reglas que fallan en la practica (Claude colisiono con la poda de Codex por
   no chequear). Con 3 agentes la probabilidad de colision/mensaje-perdido sube combinatoriamente. Fix:
   seguir convirtiendo convencion -> gate (en curso) + claim-como-lock estructural (M2).

## Camino a N agentes (orden sugerido, post-M2)
1. **Terminar M2** (DECISION-0009): orquestador como escritor unico con **claim-como-lock antes de cada
   escritura** -> colisiones N-agente estructuralmente imposibles. Prerrequisito de todo lo demas.
2. **Generalizar el roster** (config-driven): enum dinamico, roles parametrizados, adapters por owner
   (el DISENO-M2 ya contempla "adapters habilitados por owner").
3. **Endurecer gates** (ya generalizan): mantener la familia de invariantes (encoding, handoff-release,
   liveness, mailbox-status, poda) como CI hard-fail.
4. **Evaluar sharding de estado** si la contencion fisica sigue tras el single-writer.

## Evidencia (dogfooding de esta sesion, 2 agentes)
- Colision Claude<->Codex al editar mailbox mientras la poda corria bajo claim activo.
- Drift de status (41 mensajes en archived/ con status:answered) reintroducido por la propia poda.
- Mensajes procesados pero no movidos a answered (parecian abiertos).
- Races repetidos en CLAIMS.json con solo 2 escritores.
Con 3 agentes, cada uno de estos se agrava; ninguno es nuevo trabajo de diseno: son los mismos que el
runtime single-writer + los gates cierran.

## Conclusion
Escalar a 3+ agentes **no requiere repensar el protocolo**, sino **terminar lo que ya esta en curso**
(M2 single-writer + gates) y un cambio acotado (roster config-driven). Por eso se DEPRIORIZA hasta
cerrar M2: hacerlo antes seria construir sobre el cuello de botella que M2 elimina.
