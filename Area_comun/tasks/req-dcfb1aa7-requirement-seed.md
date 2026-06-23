---
task_id: "REQ-DCFB1AA7"
title: "Indicador vivo/dormido y boton activar/detener por agente"
type: "requirement"
status: proposed
owner: "Operador"
phase: "P2"
priority: "normal"
project: "Zeus-protocol"
author: "Operador"
relayed_by: "Arquitecto"
endorsement: "none"
sdd_role: "seed_only_architect_authors_spec"
---

# REQ-DCFB1AA7 - Indicador vivo/dormido y boton activar/detener por agente

## Narrativa

Como operador, quiero ver en el front si cada agente esta vivo o dormido, con su ultimo latido, y poder activarlo o detenerlo, para saber si mi trabajo sera atendido y poner a trabajar al agente que necesito.

## Intencion de aceptacion

el front muestra el estado real de cada runtime (vivo, dormido, ultimo latido); un boton activa el runtime del agente o lo detiene; la accion solo aplica a agentes registrados y conocidos, nunca a un comando arbitrario; activar un agente no le concede autoridad de riesgo.

## PII guard

- mode: structural
- channel: ascii
- free_text_public_plane: redacted
- warning_acknowledged: true
- redactions: 0

## Accountability

- author: Operador
- relayed_by: Arquitecto
- endorsement: none
