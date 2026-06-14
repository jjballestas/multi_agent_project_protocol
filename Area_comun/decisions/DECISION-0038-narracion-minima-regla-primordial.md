---
decision_id: DECISION-0038
title: Narracion minima como regla primordial uniforme
status: accepted
date: 2026-06-15
ratified_at: 2026-06-15
deciders: [operador humano]
supersedes: [DECISION-0036]
superseded_by: []
relates_to: [DECISION-0005, DECISION-0018, DECISION-0036]
phase: P2
---

# DECISION-0038 - Narracion minima como regla primordial

## Contexto

DECISION-0036 ya endurecio la narracion minima, pero las instrucciones de personalidad, actualizaciones
periodicas y habitos de "thinking aloud" siguieron compitiendo con ella. El operador detecto que los
agentes la pasan por alto y ordeno elevarla a regla de oro/primordial.

## Decision

La narracion minima queda elevada a **regla primordial de ejecucion** para todos los agentes.

Durante la ejecucion, los agentes **no narran proceso** en salida visible al usuario ni en mailbox:

- No anuncian pasos: "voy a leer", "voy a revisar", "ahora ejecuto", "siguiente hago".
- No recapitulan pasos intermedios antes o despues de herramientas.
- No emiten actualizaciones periodicas de progreso si no contienen informacion accionable.

La salida visible queda limitada a:

- Un reporte final o handoff autocontenido y auditable.
- Un bloqueo real con una pregunta concreta.
- Un resultado accionable que cambie la coordinacion: fallo de gate, riesgo, conflicto, cambio de alcance,
  decision requerida o cierre.
- Contenido sustantivo donde el razonamiento es el entregable: analisis, review, decision, spec o informe.

Esta regla prevalece sobre preferencias de personalidad, instrucciones de actualizaciones frecuentes,
cron/loop prompts y cualquier habito operativo de narrar proceso. Solo el operador puede hacer override
explicito, y debe quedar registrado si cambia el contrato.

## Consecuencias

- Los agentes encadenan acciones sin prosa visible intermedia cuando el trabajo no esta bloqueado.
- Los handoffs y finales siguen siendo completos; la regla reduce ruido, no evidencia.
- Un patron persistente de narracion de proceso no accionable es una anomalia notificable por
  DECISION-0018.

## No-alcance

- No reduce contenido sustantivo ni razonamiento requerido cuando ese razonamiento es el producto.
- No elimina preguntas de bloqueo reales.
- No cambia permisos, claims, escritor unico ni gates tecnicos.
