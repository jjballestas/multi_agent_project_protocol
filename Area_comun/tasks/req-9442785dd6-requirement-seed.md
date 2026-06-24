---
task_id: "REQ-9442785DD6"
title: "Indicador vivo/dormido y boton activar/detener por agente"
type: "requirement"
status: done
owner: "Operador"
phase: "P2"
priority: "normal"
project: "Zeus-protocol"
author: "Operador"
relayed_by: "Arquitecto"
endorsement: "none"
sdd_role: "seed_only_architect_authors_spec"
source_file_sha256: 4eb704a9a9ad3344226cc8bdc1c9b2ec215385416abe8aa792a44a384507c2d2
extraction_task_id: "TASK-EXTRACT-1F5C13A7B5"
candidate_pre_edit_hash: "ba67ecc7a74090701fe314656c1a475ba96c34ec108587b35dd5b5d14bd8f7bf"
---

# REQ-9442785DD6 - Indicador vivo/dormido y boton activar/detener por agente

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

## Procedencia

- source_file_sha256: 4eb704a9a9ad3344226cc8bdc1c9b2ec215385416abe8aa792a44a384507c2d2
- extraction_task_id: TASK-EXTRACT-1F5C13A7B5
- candidate_pre_edit_hash: ba67ecc7a74090701fe314656c1a475ba96c34ec108587b35dd5b5d14bd8f7bf

## Candidate PII Re-screen

- mode: best_effort
- guaranteed: false
- finding_count: 0
