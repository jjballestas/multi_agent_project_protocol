---
task_id: "REQ-7857CDE9"
title: "Modal fullscreen para formulario de nueva historia/requisito en Intake RF-14"
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

# REQ-7857CDE9 - Modal fullscreen para formulario de nueva historia/requisito en Intake RF-14

## Narrativa

Como operador, quiero que al hacer click en Nueva historia/requisito se abra un modal fullscreen en lugar de usar el panel lateral derecho actual, para tener mas espacio al escribir narrativa e intencion de aceptacion sin hacer scroll dentro del formulario.

## Intencion de aceptacion

El modal ocupa al menos 80% del viewport. Las textareas de Narrativa e Intencion de aceptacion tienen rows minimo 8 y se ven completas sin scroll interno. El wizard de 4 pasos y los botones Preview dry_run y EXECUTE SUBMIT_INTENT son visibles sin scrollear el modal. Al confirmar o cancelar el modal se cierra y el panel Intake muestra el requisito recien creado en Mis requisitos. El estado del formulario se conserva si el operador cierra sin enviar.

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
