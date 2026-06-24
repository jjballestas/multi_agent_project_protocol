---
task_id: TASK-0167
title: "Proyecto-front: UX polish cluster -- hash routing + busqueda Artifacts + descripcion inline Operate + KPIs contextuales + chips Backlog + agrupacion Mailbox + modal Intake (SPEC-0090, AC1-AC7)"
type: product
status: in_review
owner: Codex
phase: P2
priority: normal
spec_id: SPEC-0090
created_at: 2026-06-24
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
origin_reqs: [REQ-11A2A57C, REQ-07DD94CE, REQ-16BDAA88, REQ-524372E9, REQ-A4B9FE80, REQ-CD4CE3F1, REQ-7857CDE9]
linked_decisions: [DECISION-0050]
file: Area_comun/tasks/TASK-0167-codex-front-ux-polish-cluster.md
---

# TASK-0167 - Front UX polish cluster (SPEC-0090)

> Lote de pulido de presentacion del panel "single-operator", todo read-side. maker=Codex / checker=Arquitecto.
> #4 byte-identica; ASCII-only; sin nueva ruta de escritura de estado. Repo producto Zeus-protocol.

## Alcance (SPEC-0090 AC1-AC7 + carries AC11/AC12/AC13)

- **AC1** Routing por hash URL (REQ-11A2A57C): `/#<vista>`, deep-link, Atras/Adelante, hash invalido -> default;
  extiende showView (no lo reemplaza); AC12 verde.
- **AC2** Busqueda por texto en Artifacts (REQ-07DD94CE): filtro en vivo case-insensitive por id/nombre; borrar
  restaura; contador refleja visibles.
- **AC3** Descripcion inline en acciones de Operate (REQ-16BDAA88): una linea <=80 chars, lenguaje del operador,
  siempre visible, debajo del titulo y encima del tipo de intent.
- **AC4** KPIs de cabecera contextuales (REQ-524372E9): acento DERIVADO del valor (>0) en Mailbox/Backlog; modo
  compacto en Help/Projects.
- **AC5** Chips de estado/prioridad en Backlog (REQ-A4B9FE80): chip prioridad (high calido / normal neutro) +
  estado semantico consistente con badges de integridad; tokens del design-system; high con marca visual.
- **AC6** Agrupacion temporal + filtro direccion en Mailbox (REQ-CD4CE3F1): answered/archived agrupados por fecha
  colapsables con contador; periodo actual expandido; filtro from/to; SOLO presentacion (no archiva).
- **AC7** Modal fullscreen para nueva historia en Intake (REQ-7857CDE9): >=80% viewport; textareas rows>=8 sin
  scroll interno; wizard de 4 pasos + Preview dry_run / EXECUTE visibles; cancelar/confirmar cierra y restaura
  foco; el flujo gobernado RF-14 (submit_intent, sin preview-as-green) NO cambia.

## DoD

- AC1-AC7 verdes con behavior-tests deterministas; AC11 badge-honesto / AC12 routing-comportamiento / AC13
  conformidad-de-diseno PERMANENTES verdes; carry AC16/AC17/AC58/AC72.
- node --test clon limpio exit 0; validate con/sin secretos exit 0; drift 0; neutralidad+encoding 0; #4
  byte-identica (NO toca protocol.config.json ni el ledger).
- **Prueba negativa OBLIGATORIA:** ninguna mejora UX (busqueda, agrupacion, modal, routing, filtros) emite
  submit_intent ni muta mailbox/ledger -- sigue siendo read-side. PII redactada en cualquier texto renderizado.
- Reproducido por el checker (Arquitecto) DESDE CLON LIMPIO; maker!=checker.
- REPRO: deep-link `/#mailbox` abre Mailbox; Atras navega; buscar en Artifacts filtra en vivo; KPI con acento solo
  si >0; tarjeta high con chip+marca; answered agrupado por fecha colapsable; nueva historia abre modal >=80%.

## Notas

- Construir sobre el modelo ya cargado en el cliente; cero llamadas nuevas al server salvo las ya existentes.
- Si se prefiere fraccionar: lote A (AC1-AC4) y lote B (AC5-AC7) son independientes; por defecto una sola entrega.
- Citar el commit del design-system de Zeus-protocol/design/ vigente en el handoff.
