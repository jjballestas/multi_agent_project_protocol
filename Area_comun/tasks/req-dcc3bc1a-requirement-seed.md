---
task_id: REQ-DCC3BC1A
title: "Intake: limpiar el formulario y confirmar claramente tras un submit exitoso"
type: requirement
status: done
owner: Operador
phase: P2
priority: normal
project: Zeus-protocol
author: Operador
relayed_by: Arquitecto
endorsement: none
sdd_role: seed_only_architect_authors_spec
---

# REQ-DCC3BC1A - Intake: limpiar el formulario y confirmar claramente tras un submit exitoso

## Narrativa

Como operador, tras un EXECUTE exitoso no se si se envio porque los campos siguen llenos; si lanzo otro puedo reenviar lo mismo. Quiero que al confirmar OK el formulario se limpie y quede claro que se envio.

## Intencion de aceptacion

Tras un EXECUTE exitoso el wizard muestra un resultado inequivoco (enviado-atestado, id y seq) y el formulario se RESETEA (campos vacios, vuelve al paso 1, estado borrador) listo para una historia nueva. No queda ambiguedad sobre si se completo; se evita el reenvio accidental. La idempotencia por id=hash ya protege contra el duplicado exacto, pero la UI debe dejarlo explicito.

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
