---
task_id: "REQ-EE0CA804"
title: "RC-01 Intake: barra de control unificada en header de seccion"
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

# REQ-EE0CA804 - RC-01 Intake: barra de control unificada en header de seccion

## Narrativa

Como operador quiero que la fila del header de la seccion Intake concentre en una sola linea: el [[DOC-REDACTED]] RF-14, el titulo, el subtitulo, los radios de modo (Manual / Por archivo) cada uno junto a su etiqueta, el boton Nueva historia/requisito y el boton Refresh; para reducir el espacio ocupado y tener el control de la seccion siempre visible sin necesidad de scroll.

## Intencion de aceptacion

1. El header de Intake muestra todo en una fila: [RF-14 badge] [Intake] [subtitulo] [espacio] [Modo: radio-Manual label-Manual | radio-Archivo label-Archivo | btn-Nueva-historia] [btn-Refresh]. 2. Cada radio esta inmediatamente antes de su label (sin separacion). 3. Los radios son solo indicadores de modo; no lanzan ningun formulario al hacer click. 4. El boton Nueva historia/requisito es el unico punto de entrada al wizard/modal. 5. El boton Refresh queda al extremo derecho fuera del bloque de modo. Referencia visual: prototipo HTML adjunto seccion header.

## PII guard

- mode: structural
- channel: ascii
- free_text_public_plane: redacted
- warning_acknowledged: true
- redactions: 1

## Accountability

- author: Operador
- relayed_by: Arquitecto
- endorsement: none
