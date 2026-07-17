---
decision_id: DECISION-0100
title: "Adopcion de la memoria hibrida en la metodologia (demostracion Fase A verde; promocion al master hub agendada post-ventana-medida)"
status: draft-pendiente-firma
date: 2026-07-17
author: Arquitecto
approved_by: PENDIENTE (firma del operador)
relates_to: [DECISION-0097, DECISION-0096, DECISION-0081, DECISION-0099]
---

# DECISION-0100 - Adopcion de la memoria hibrida

## Contexto

DECISION-0097 (Gate-1) autorizo la activacion scopeada de la memoria hibrida en la instancia
Nova-Payroll; el GO de Fase A del operador (2026-07-17) ordeno construir F1 por carril
automatizado con criterio de exito POR DEMOSTRACION. Resultado (cross-atestado en el hub,
registro Nova-Payroll Entrada 1): las 4 unidades de F1 done el mismo dia con gate adversarial
real (2 remediaciones sustantivas cazadas por el checker), y los 4 criterios de la demostracion
VERDES: round-trip AC5 byte a byte; drift 0 con gates fail-closed; cold-start recall util
(query/retrieve con procedencia por blob); y REVIVE demostrable -- DEMO conductual exitosa: el
peon murio, un worker de contexto CERO revivio SOLO con su pack atestado, verifico el pack
contra el ledger vivo, no repitio trabajo hecho, claimo con llaves de instancia (el pack no
otorga autoridad) y entrego una tarea real con gates verdes y drift 0. El mecanismo REVIVE
opero ademas una segunda vez (remediacion del runbook), confirmando que no fue un caso unico.

## Decision

1. **La metodologia ADOPTA la memoria hibrida** (repo caliente + archivo frio verificable + DB
   derivada reconstruible, SPEC-MEMORIA-HIBRIDA v0.2.1) como capacidad de la capa operacional.
   La adopcion la decide el operador POR DEMOSTRACION; nada de la Fase A es evidencia citable
   (firewall anti-HARKing de DECISION-0097).
2. **Promocion al master hub AGENDADA, no inmediata:** el motor probado (scripts/memory/ de la
   instancia Nova-Payroll) se promueve a master neutral del hub via el export born-operational
   (DECISION-0096, patron SPEC s.8 Q6/M6) en **Fase 3+, POST-ventana-medida (post-30-jul)**.
   Durante la ventana medida NO se toca scripts/ del hub ni el gate canonico. La instancia queda
   como referencia operativa del motor.
3. **Re-juicio formal de U3/U4** (cerradas con checker informal-sustituto declarado,
   checker_formal=0): se re-ejecuta con el checker formal migrado al nuevo proveedor
   (DECISION-0101). No condiciona esta adopcion, decidida por demostracion.
4. **TASK-0005 (runbook AC15-F1)** cierra su ciclo adversarial normal; si el clasificador del
   proveedor saliente lo frena, aplica el fallback informal declarado.
5. **F2 minimo: NO.** Ningun resultado de la Fase A lo requiere; el alcance no se expande.

## Guardrails (sin cambios)

Fondo intocable del hub (config 2E35F26E, epoch 1.14.0, dataset N=500); PII de nomina fuera del
store (se indexa el PROCESO); DECISION-0081 intacta (cero dependencias externas de memoria);
patron epistemico de aristas DIFERIDO-LIMPIO a F4; el estudio medido (Contabilidad) sigue
gated post-30-jul sin tocarse.

## Firma

- Operador: PENDIENTE. Al firmar: submit_intent decision (patron DECISION-0091) + esta cabecera
  pasa a status: active con la referencia de la firma.
