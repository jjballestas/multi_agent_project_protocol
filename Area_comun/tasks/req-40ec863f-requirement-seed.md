---
task_id: "REQ-40EC863F"
title: "UX: Boton Nueva historia/requisito con mal estilo visual en Intake"
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
---

# REQ-40EC863F - UX: Boton Nueva historia/requisito con mal estilo visual en Intake

## Narrativa

Como operador quiero que el boton Nueva historia/requisito tenga un estilo visual correcto y coherente con el resto de la interfaz, ya que actualmente el texto se parte en dos lineas, el boton aparece desalineado verticalmente respecto a los elementos adyacentes (borrador, Mis requisitos) y rompe la fila de controles del Intake.

## Intencion de aceptacion

El boton debe mostrar su etiqueta en una sola linea sin saltos de texto, tener altura consistente con los elementos de la misma fila, y respetar el sistema de estilos de la consola (color de acento, bordes, tipografia). Opcionalmente puede usar un icono + antes del texto para reforzar su funcion de creacion.

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
