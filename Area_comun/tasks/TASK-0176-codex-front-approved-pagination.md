---
task_id: TASK-0176
title: "Proyecto-front: carpeta Aprobados muestra los ultimos 3 + 'ver mas' con paginacion (REQ-C1EDD835)"
type: product
status: done
owner: Codex
phase: P2
priority: normal
spec_id: SPEC-0092
created_at: 2026-06-24
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
origin_reqs: [REQ-C1EDD835]
linked_decisions: [DECISION-0050]
file: Area_comun/tasks/TASK-0176-codex-front-approved-pagination.md
---

# TASK-0176 - Carpeta Aprobados: ultimos 3 + ver mas paginado (REQ-C1EDD835)

> Feature UX read-side sobre la carpeta Aprobados (RC-02 dashboard del Intake). maker=Codex / checker=Arquitecto.
> Solo presentacion; sin nueva ruta de escritura; #4 byte-identica.

## Alcance (REQ-C1EDD835)
- En la carpeta/vista "Aprobados" del Intake, mostrar por defecto los **ultimos 3** requisitos aprobados.
- Un boton "Ver mas" que, al presionarlo, muestra los demas aprobados con **paginacion** (paginas de tamano fijo,
  p.ej. 5-10 por pagina, con controles anterior/siguiente o numeros de pagina).
- El conteo/orden deriva del estado real (aprobados), no estatico. Solo lectura: no cambia el estado ni el flujo
  gobernado. PII: el texto renderizado sigue redactado (modelo publico de candidatas ya redacta).
- Behavior-test: con N>3 aprobados, por defecto se ven 3 + "Ver mas"; al expandir, aparecen los demas paginados;
  el contador refleja el total real.

## DoD
- REQ-C1EDD835 verde con behavior-test; las AC del cluster RC + fronteras (no-bypass / PII gate / off-by-default)
  intactas. node --test clon limpio exit 0 (estable); #4 byte-identica; sin nueva ruta de escritura. Reproducido
  por el checker (Arquitecto) desde clon limpio; maker!=checker.
- REPRO: con varios aprobados, la carpeta Aprobados muestra 3 + Ver mas; expandir pagina el resto.

## Notas
- Reusar el dashboard de carpetas (RC-02) y el design-system. Si el "modelo publico de candidatas" no expone los
  aprobados con su estado, derivarlos del modelo existente (read-only).
