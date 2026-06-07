---
decision_id: DECISION-0022
title: Runtime como escritor autoritativo del estado de protocolo + genesis por referencia (no por volcado)
status: accepted
date: 2026-06-07
ratified_at: 2026-06-07
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0017, DECISION-0019, DECISION-0014, DECISION-0011, DECISION-0009]
phase: P2
---

# DECISION-0022 - Runtime como escritor autoritativo del estado + genesis por referencia

> Estado: ACCEPTED como DIRECCION TECNICA (2026-06-07, ratificada por el operador). SemVer:
> **MINOR-con-migracion** (off-by-default, opt-in, coordination-tier intacto). Habilita el cambio de modo
> operativo (runtime = escritor unico, prohibir edicion manual) que es la rebanada B.4 de la Fase B
> (SPEC-0039). CONDICION DEL OPERADOR: la implementacion de B.4 se construye apagada, pero **ACTIVAR enforce/
> modo autoritativo en la INSTANCIA VIVA exige una aprobacion explicita POSTERIOR**, condicionada a:
> (1) B.3 (TASK-0068) cerrada, (2) validacion de replay/materializacion, (3) plan de rollback documentado.
> Off-by-default, opt-in por instancia, solo runtime-tier; coordination-tier no se ve afectado.

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
- `AGENTS.md`/`AGENTS.template.md` y `TASK_PROTOCOL.md`: nota (entregada con B.4) de que, en instancias con
  runtime-escritor activo, las transiciones pasan por el runtime y la edicion manual del estado esta prohibida.
- La regla anti-colision (DECISION-0020) se vuelve mayormente innecesaria en ese modo (no hay dos escritores
  manuales); se mantiene para coordination-tier y para la fase de transicion.

## Versionado y neutralidad (DECISION-0001)

- **SemVer: MINOR-con-migracion** (fijado por el operador 2026-06-07). Off-by-default + opt-in +
  coordination-tier intacto => aditivo para quien no lo activa; para quien lo activa hay migracion asistida.
  Neutral de dominio (coordinacion de proceso, sin terminos de negocio).
- Genesis-por-referencia: aditivo y favorable al presupuesto de cold-start (DECISION-0014); sin secretos.

## Condiciones para ACTIVAR enforce/modo autoritativo en la instancia viva (aprobacion separada)

La direccion tecnica esta ratificada y B.4 se implementa **apagada**. Encender el modo en el repo vivo
(`event_state.enforce`/`authoritative` = true) es un paso OPERATIVO aparte que requiere **aprobacion explicita
del operador POSTERIOR al cierre de B.3**, condicionada a:

- [ ] B.3 (TASK-0068) `done` y ratificada. (CUMPLIDO 2026-06-07.)
- [ ] Validacion de replay/materializacion sobre el estado vivo (round-trip genesis-ref -> replay ->
      materialize == estado canonico; integridad por hash).
- [ ] **Plan de rollback** documentado y probado (apagar flags devuelve a edicion manual; el snapshot
      content-addressed y el commit de corte permiten reconstruir el estado previo).

Hasta esa aprobacion, B.4 queda como capacidad disponible pero **inactiva** en la instancia viva.

## Consecuencias

- Cierra el "writer-vivo" del estado de protocolo de forma reversible y verificable, sin inflar el cold-start
  (genesis por referencia).
- Mantiene dos modos: coordination-tier / manual (sin cambios) y runtime-escritor (opt-in, gateado).
- La prohibicion DURA permanente (retirar el flujo manual sin reversa) NO entra aqui; seria un paso futuro
  explicito con su propia decision.
