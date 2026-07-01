---
decision_id: DECISION-0073
title: "REQ-ZEUS D2 - Una instancia de metodologia por proyecto (generada por instalador con new_instance.py + wrapper 4 firmantes; human_owner = empleado/lider)"
status: accepted
ratified_at: 2026-06-30
date: 2026-06-30
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [REQ-ZEUS-001, DECISION-0050, DECISION-0072]
scope: product
phase: P2
---

# DECISION-0073 (REQ-ZEUS D2) - Una instancia por proyecto

> ACCEPTED (operador endoso OPS-115242Z + registro en hub, 2026-06-30). Canonicaliza la D2 de NOVA
> (`D:/Agentes/Zeus/NOVA/Area_comun/decisions/DECISION-0002-D2-una-instancia-por-proyecto.md`).

## Decision
Cada proyecto de empleado obtiene **su propia instancia** de la metodologia, generada por el instalador con
`new_instance.py` (+ wrapper que incluye al 4to firmante, el Analista). El empleado o su lider es el `human_owner`.
Convencion de ubicacion: `D:\Zeus\proyectos\<nombre>` (ajustable por el instalador). Default tier = coordination (D1).

## Razon
Evita colisiones entre proyectos y mantiene el contexto acotado (cold-start eficiente). Una instancia compartida
mezclaria backlogs/claims/mailbox de proyectos distintos.

## Consecuencias
- El instalador parametriza `new_instance.py` (o un wrapper) para sembrar **4 agentes** (Arquitecto, Codex, Analista,
  human_owner) y crear `personal/<id>/` de cada uno (WS5).
