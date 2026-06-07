---
decision_id: DECISION-0022
title: Runtime como escritor autoritativo del estado de protocolo + genesis por referencia (no por volcado)
status: proposed
date: 2026-06-07
ratified_at: null
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0017, DECISION-0019, DECISION-0014, DECISION-0011, DECISION-0009]
phase: P2
---

# DECISION-0022 - Runtime como escritor autoritativo del estado + genesis por referencia

> Estado: PROPOSED (2026-06-07). El operador autorizo INICIAR la Fase B.4 y fijo la restriccion de diseno
> del genesis. Esta decision habilita el cambio de modo operativo (runtime = escritor unico, prohibir
> edicion manual) que es la rebanada B.4 de la Fase B (SPEC-0039). Es un cambio de FRONTERA del contrato
> operativo => requiere aprobacion humana antes de ratificar y de aterrizar la prohibicion. Off-by-default,
> opt-in por instancia, solo runtime-tier; coordination-tier no se ve afectado.

## Contexto

La Fase B llevo el event log de observacional (B.1) a materializador opt-in (B.2) y a hard-gate del drift
(B.3). La ultima rebanada (B.4) cierra el "writer-vivo": el runtime pasa a ser el **escritor autoritativo**
del estado de protocolo (TASK_INDEX/PROJECT_STATE/CLAIMS) y se **prohibe la edicion manual** de esos JSON en
las instancias que lo activen. Esto cambia el modo operativo actual (agentes editando el ledger a mano), por
lo que es una decision de frontera, no solo una tarea aditiva.

Ademas, convertir el estado actual en el evento `genesis` plantea un riesgo de eficiencia y de prompt: si el
genesis **incrusta** todo el estado, infla el event log, el contexto del agente y el cold-start
(DECISION-0014).

## Decision

1. **Runtime escritor autoritativo (opt-in, runtime-tier).** Una instancia `adoption_tier=runtime` puede
   activar el modo en el que el runtime es el unico escritor del estado de protocolo: las transiciones se
   emiten como intents al runtime (intent -> apply -> event log -> materializacion) y la edicion manual de
   `Area_comun/state/*.json` queda **prohibida** (el hard-gate de B.3 la rechaza como drift). Off-by-default;
   se activa con decision propia de la instancia + los flags `event_state.enabled/materialize/enforce` + un
   flag de modo autoritativo. Reversible hasta el momento de la prohibicion dura.

2. **Genesis por REFERENCIA, no por volcado (restriccion del operador).** El evento `genesis` NO incrusta el
   estado completo. Registra una **referencia verificable al snapshot de corte** con, al menos:
   `hash` (hash canonico del snapshot), `commit` (SHA de git del corte), `actor`, `timestamp` (logico,
   provisto; sin reloj del runtime para preservar determinismo del replay) y `schema_version`. El **snapshot
   completo se persiste fuera del prompt**, content-addressed por su `hash` (p.ej.
   `runtime/state/snapshots/<hash>.json`), y solo se consulta o materializa cuando el runtime lo necesita.
   El replay carga el snapshot por su `hash`, **verifica** que el hash recomputado coincide (integridad), y
   materializa desde ahi. Asi el event log y el contexto del agente permanecen livianos (una referencia, no
   un dump).

3. **coordination-tier intacto.** Las instancias `coordination-tier` (sin `runtime/`) NO adoptan este modo:
   para ellas la edicion manual del ledger sigue siendo el flujo normal. La prohibicion aplica solo donde el
   runtime es el escritor.

## Aplicacion

- Implementacion = Fase B.4 (SPEC-0055): genesis-por-referencia + carga/verificacion del snapshot
  content-addressed + flag de modo autoritativo + prohibicion (via hard-gate B.3) + docs de migracion
  (coordination/manual -> runtime-escritor) y de reversa.
- `AGENTS.md`/`AGENTS.template.md` y `TASK_PROTOCOL.md`: nota de que, en instancias con runtime-escritor
  activo, las transiciones pasan por el runtime y la edicion manual del estado esta prohibida.
- La regla anti-colision (DECISION-0020) se vuelve mayormente innecesaria en ese modo (no hay dos escritores
  manuales); se mantiene para coordination-tier y para la fase de transicion.

## Versionado y neutralidad (DECISION-0001)

- Off-by-default + opt-in + coordination-tier intacto => el cambio es **aditivo** para quien no lo activa.
  Para quien lo activa, cambia el flujo operativo (edicion manual prohibida): se evalua como
  **MINOR-con-migracion** o **MAJOR** segun rompa o no una instancia valida existente; lo fija el operador
  al ratificar/release. Neutral de dominio (coordinacion de proceso, sin terminos de negocio).
- Genesis-por-referencia: aditivo y favorable al presupuesto de cold-start (DECISION-0014); sin secretos.

## Pendiente antes de ACCEPTED

- [ ] Cerrar B.3 (TASK-0068) primero (B.4 se monta sobre el hard-gate de B.3).
- [ ] Aprobacion del operador humano (cambio de frontera del modo operativo) + SemVer fijado.
- [ ] Numero de decision confirmado (0022) y enlazado en PROJECT_STATE#decisions.
