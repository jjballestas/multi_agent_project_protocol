# SUGERENCIAS - Hacia una autonomia supervisada del lazo N-agente

- Fecha: 2026-06-06
- Autor: Claude (arquitecto)
- Origen: analisis del comportamiento semi-automatico (ver
  Area_comun/reports/REPORT-20260606-comportamiento-semi-automatico.md).
- Estado: propuestas; cada una requiere decision/priorizacion del operador. NO arrancar las gateadas sin OK.
- Objetivo propuesto: "autonomia supervisada" = cerrar el lazo de EJECUCION conservando revision
  adversarial independiente + gates humanos en decisiones + paradas duras.

## Principio rector

Automatizar la EJECUCION (lo mecanico y repetitivo) y conservar al humano en las DECISIONES (contrato,
fase, release, limites) y la revision independiente como gate duro. No es "mas agentes" sino un lazo
auditable que no pierde control.

## Sugerencias accionables (priorizadas)

### S1 - Atomicidad del handoff-release (BAJO riesgo, ALTO valor) [PARCIAL: ya regulado]
- Que: garantizar que la entrega (handoff + mensaje in-review) y la transicion de estado (liberar claim +
  flip status) ocurran juntas; un turno cortado entre ambas deja estado inconsistente.
- Por que: fue la anomalia real de A.3 (TASK-0051). Ya se regulo via DECISION-0018 (regla + nota de
  atomicidad) y Codex la internalizo (A.4 y A.7 con release atomico correcto).
- Siguiente paso: cuando el runtime ejecute turnos, heredar la atomicidad de apply (backup+restore+block,
  ya ratificada en A.1) para que la garantia sea mecanica y no dependa de disciplina del agente.
- Dependencia: ninguna para la regla (hecha); para la version mecanica, el runtime como ejecutor (S3).

### S2 - Notificacion de anomalias agente-a-agente (BAJO riesgo) [HECHO]
- Que: el agente que detecta una anomalia de otro la notifica por mailbox al responsable, no solo al humano.
- Estado: establecido como DECISION-0018 en AGENTS.md/.template sec.7 + TASK_PROTOCOL. Conservar y aplicar
  en ambos sentidos.

### S3 - Reloj/disparador propio para Codex (MEDIO riesgo) [GATEADO - decision operador]
- Que: dar a Codex un mecanismo de auto-arranque (cron/disparador equivalente al ScheduleWakeup de Claude)
  para que tome su cola sin empuje humano por turno.
- Por que: hoy el operador es el reloj de Codex (evidencia: TASK-0049 espero ~2 ciclos hasta el empuje).
  Es el principal bloqueo del lazo cerrado de extremo a extremo.
- Riesgo/mitigacion: runaway y costo -> limitar con presupuesto/deadline por turno (criterio 13 de
  SPEC-0038) y un tope de iteraciones; mantener 1 commit/turno y paradas duras.
- Dependencia: idealmente despues de S5 (guardrails) si Codex va a ejecutar acciones con efecto.

### S4 - Runtime como ejecutor real de turnos + wrapper LLM real (MEDIO/ALTO riesgo) [GATEADO]
- Que: que `orquestador --run` ejecute los turnos con un adapter LLM real (hoy es replay/recorded), de modo
  que el runtime -y no la operacion manual- aplique transiciones con su atomicidad y gates.
- Por que: cierra la ironia (se construye el motor pero se opera a mano) y hereda atomicidad/gates mecanicos.
- Riesgo/mitigacion: empezar con un solo turno gateado, sin automation que lo dispare, reversible; el
  template permanece OFF.
- Dependencia: wrapper LLM real (pendiente); conviene tras S5.

### S5 - Guardrails y permisos antes de autonomia con efectos (Fase 5) [GATEADO]
- Que: tool-policy con allowlist por herramienta, side-effect gates, diff obligatorio, bloqueo de acciones
  sensibles, defensa anti-inyeccion en handoffs; y completar I1/I2 contra actores no confiables (el
  hardening autor-de-record A.6 ya cerro la via del payload).
- Por que: es el prerequisito de seguridad para cerrar el lazo con efectos externos.
- Prioridad: antes de S3/S4 si el lazo va a actuar fuera del repo.

### S6 - Event log como writer-vivo del estado de protocolo (Fase B) [GATEADO]
- Que: que el estado (tareas/claims/proyecto) se derive del event log (replay + materializacion +
  genesis-snapshot + ventana de transicion warning->hard-fail). Hoy solo el control-plane esta cableado
  (A.1 Fase A).
- Por que: habilita auditoria/replay reales y hace que la atomicidad del turno sea estructural.
- Riesgo/mitigacion: cambia el modo de edicion del estado; va con ventana de transicion y decision del
  operador (DECISION-0017 fijo el alcance A->B incremental).

### S7 - Observabilidad y presupuesto por turno (Fase 6) [GATEADO]
- Que: trace_id por evento, metricas de routing/QA/conflictos/coste, deadline y presupuesto por tarea/run
  con escalado al agotarse.
- Por que: sin esto, un lazo cerrado no es supervisable ni acotado en costo. Es la red de seguridad de S3/S4.

## Recomendacion de secuencia

S5 (guardrails) -> S6 (writer-vivo) -> S4 (runtime ejecutor + LLM real) -> S3 (disparador de Codex), con S7
(observabilidad/presupuesto) habilitado antes de S3/S4. S1 y S2 ya estan hechos/regulados. En cada paso el
riesgo queda contenido y el humano conserva las decisiones gateadas y la revision adversarial independiente.

## Que NO automatizar (conservar humano/independiente)

- Decisiones de contrato/limite/fase/release (siguen requiriendo DECISION + aprobacion humana).
- Revision adversarial por un agente distinto del autor (I1/I2): es el gate de calidad que aporto valor real.
- Paradas duras y 1 commit/turno.
