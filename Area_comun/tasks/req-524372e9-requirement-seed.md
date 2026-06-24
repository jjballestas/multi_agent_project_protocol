---
task_id: "REQ-524372E9"
title: "UX: KPIs de cabecera contextuales segun la vista activa"
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

# REQ-524372E9 - UX: KPIs de cabecera contextuales segun la vista activa

## Narrativa

Como operador, quiero que los 4 KPIs de la cabecera (Ledger SEQ, Open Mailbox, Active Claims, Open Tasks) resalten o adapten su presentacion segun la vista activa, para que al estar en Mailbox el KPI de Open Mailbox sea el prominente y en Backlog destaquen Open Tasks, en lugar de tener los 4 siempre con el mismo peso visual.

## Intencion de aceptacion

En la vista Mailbox el KPI Open Mailbox tiene fondo o borde de acento cuando su valor es mayor a 0. En la vista Backlog el KPI Open Tasks tiene el mismo tratamiento. En las vistas Help y Projects los KPIs se muestran en modo compacto o reducido ya que no son accionables desde esas vistas. El KPI Ledger SEQ no tiene tratamiento especial por vista. En ninguna vista los KPIs desaparecen, solo cambia su jerarquia visual relativa.

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
