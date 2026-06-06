# Session report - Comportamiento semi-automatico del lazo Claude <-> Codex <-> operador

- Date: 2026-06-06
- Phase: P2
- Process status: closed (analisis entregado)
- Ratification: draft (pendiente de ratificacion del operador)
- Autor: Claude (arquitecto). Pedido por el operador.

## 1. In One Sentence

El sistema multi-agente opera hoy de forma "semi-automatica": la coordinacion y la revision estan
automatizadas (Claude se auto-despierta y reacciona), pero la ejecucion de implementacion (Codex) depende
de un empuje humano por turno; el motor que cerraria ese lazo es justo lo que se esta construyendo.

## 2. What Was Done

Durante esta sesion el lazo cerro en cadena ~9 tareas (N-agente Fases 2-4 + toda la Capa A: A.1-A.7),
cada una bajo el mismo ciclo: Claude encola -> el operador empuja a Codex -> Codex implementa y entrega
(handoff + in-review + release) -> Claude ratifica adversarialmente, cierra, encola la siguiente, commitea
y se re-agenda. Se observo el comportamiento en vivo y se registro evidencia directa.

## 3. Mapa de autonomia (quien es el "reloj" de cada actor)

- **Claude (arquitecto):** se auto-dispara. Usa un temporizador propio (ScheduleWakeup ~270s) como reloj;
  cada despertar sondea mailbox/handoffs/estado y, al detectar una entrega, ratifica corriendo el mismo la
  suite, cierra, encola la siguiente tarea, commitea/pushea y se re-agenda. Sin intervencion humana por
  iteracion.
- **Codex (implementador):** NO se auto-dispara. Requiere que el operador le indique "monitorea y reacciona"
  en cada turno. Su reloj es el operador.
- **Operador (humano):** es el reloj de Codex y el que autoriza lo gateado (fases condicionadas, releases,
  cambios de contrato/limite).

La asimetria es el hallazgo central: una mitad del lazo corre sola; la otra depende de empuje humano.

## 4. Evidencia empirica de la sesion

- **Asimetria confirmada:** TASK-0049 quedo `ready` ~2 ciclos sin que Codex la reclamara, hasta el empuje
  del operador. Los ~9 cierres de Claude ocurrieron sin intervencion humana por iteracion.
- **Concurrencia real:** en TASK-0045 Codex arranco su turno entre dos lecturas de Claude; son procesos
  genuinamente concurrentes, por eso la disciplina de claims importa.
- **No-atomicidad del turno (anomalia en A.3 / TASK-0051):** Codex dejo un handoff-release incompleto: el
  mensaje declaraba "claim liberado" pero el estado quedaba inconsistente (claim active + in_progress). El
  turno se corto entre escribir la entrega y persistir la transicion de estado.
- **Auto-correccion del sistema:** esa anomalia origino DECISION-0018 (notificar anomalias por mailbox +
  atomicidad del handoff-release); en las dos tareas siguientes (A.4 y A.7) Codex aplico el release atomico
  correctamente. El protocolo se ajusto y el comportamiento mejoro en el ciclo siguiente.
- **La revision independiente aporto valor real (no fue sello de goma):** detecto un hallazgo de seguridad
  (exclusion de autor evadible via payload -> origino A.6), una observacion de portabilidad (import del
  validador) y la anomalia de proceso. Las entregas de Codex fueron de buena calidad (ratificacion verde),
  pero la revision adversarial encontro cosas que el autor no.

## 5. Analisis: por que es "semi-automatico" y donde esta el humano en el lazo

La capa de coordinacion/ratificacion/cierre (Claude) es autonoma intra-ciclo. La capa de ejecucion (Codex)
es dependiente de empuje humano. El operador permanece en el lazo en dos puntos: (1) como reloj de Codex
(operativo, por turno) y (2) como autoridad de decisiones gateadas (estrategico: fases, releases, limites).
El primero es el que impide el lazo cerrado de extremo a extremo; el segundo es deseable y debe conservarse.

**Ironia central:** se esta construyendo el runtime N-agente (orquestador --run, event log, router, maquina
Review/QA, writer-vivo) que automatizaria este lazo y daria atomicidad de turno, pero se construye
operandolo a mano. Hoy los turnos los ejecutan los agentes + el empuje del operador, no el runtime; el
event log aun no es el writer-vivo del estado (Fase B gateada) y el adapter LLM real no esta cableado. La
no-atomicidad observada en A.3 es exactamente lo que el `apply` atomico del runtime (ratificado en A.1)
evitaria si el runtime ejecutara los turnos.

## 6. Lo que funciona (conservar) vs. lo que falta (para cerrar el lazo)

Conservar (hace seguro el semi-automatismo): revision adversarial independiente (revisor != autor, ahora
garantizado por I1/I2 endurecidos en A.6); 1 commit por turno; claims efimeros; no tocar rutas bajo claim
ajeno; prune; gates verdes antes de cada push; decisiones gateadas al humano.

Falta para automatizar la ejecucion de Codex: un reloj/disparador propio para Codex; el runtime como
ejecutor real de turnos (adapter LLM real, no replay); el writer-vivo del estado (Fase B); y los guardrails
(Fase 5) antes de dar autonomia con efectos externos.

## 7. Riesgos

Cerrar el lazo del todo sin guardrails implica: perdida de los puntos de control humano, runaway de
iteraciones, costo de tokens sin supervision y acciones externas sin contencion. Por eso no se recomienda
full-auto todavia.

## 8. Recomendacion (resumen; detalle accionable en el artefacto de sugerencias)

Nivel objetivo: "autonomia supervisada". Cerrar el lazo de EJECUCION (Codex con reloj propio + runtime
ejecutor) manteniendo la revision adversarial independiente como gate duro, los gates humanos en
decisiones de contrato/fase/release, y las paradas duras. Las sugerencias accionables, priorizadas, estan
en el artefacto formal: `Area_comun/artifacts/SUGERENCIAS-autonomia-semi-automatica-20260606.md`.

## 9. What We Need From The Human Owner

- Decidir si se adopta el objetivo de "autonomia supervisada" y en que orden (ver artefacto de sugerencias).
- Decision aparte ya solicitada: siguiente paso tras la Capa A completa (release v0.10.0 / Fase 5 / Fase B /
  detener), en MSG-20260606-Claude-to-operador-capaA-completa.

## 10. Details

- Observaciones en memoria del arquitecto: semi-auto-collaboration-pattern.
- Sugerencias accionables: Area_comun/artifacts/SUGERENCIAS-autonomia-semi-automatica-20260606.md.
- Decisiones relacionadas: DECISION-0018 (notificacion de anomalias), DECISION-0009 (runtime),
  DECISION-0013 (liveness/visibilidad), DECISION-0015 (N-agente).
- Evidencia: TASK-0044..0053 (N-agente Fases 2-4 + Capa A), HANDOFF-TASK-0045..0053, SPEC-0038/SPEC-0039.
