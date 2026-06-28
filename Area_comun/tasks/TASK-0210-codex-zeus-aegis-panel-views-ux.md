---
task_id: TASK-0210
title: "Zeus-Aegis: UX de las vistas del panel (desplegables colapsadas, recientes+mostrar mas, filtros legibles) (DECISION-0064)"
type: product
status: in_review
owner: Codex
phase: P2
priority: high
created_at: 2026-06-28
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-Aegis
project: Zeus-Aegis
linked_decisions: [DECISION-0064]
file: Area_comun/tasks/TASK-0210-codex-zeus-aegis-panel-views-ux.md
---

# TASK-0210 -- UX de las vistas del panel governance

## Contexto (feedback del operador, 2026-06-28)
El panel `/governance` es una pagina larga con secciones (Dashboard, Backlog, Mailbox, Artifacts, Decisiones,
Ledger/atestacion, Handoffs). Problemas de usabilidad reportados:
- Todo se muestra de golpe y largo; el operador quiere ver solo lo RECIENTE y desplegar lo demas.
- Los combos de filtro NO son legibles: en el desplegable (p.ej. owner: All owners/Analista/Arquitecto/Codex) el
  texto sale gris casi invisible sobre fondo claro -- el `<select>` nativo no honra el tema oscuro (design-system).
- Mailbox NO tiene filtros (Backlog si).
- Artifacts solo tiene un campo de texto para filtrar; deberia tener tambien un combo (al menos por TIPO).

## Objetivo
El panel se vuelve usable para OBSERVAR: secciones colapsables (colapsadas por defecto), cada una mostrando lo mas
reciente + "Mostrar mas", filtros legibles y completos. Todo READ-ONLY (no escribe nada).

## Alcance (por seccion: Backlog, Mailbox, Artifacts, Decisiones, Ledger/atestacion, Handoffs)
1. **Desplegable colapsado por defecto:** cada seccion es un acordeon (header con titulo + conteo + chevron),
   **colapsada por defecto**; el operador despliega la que quiera. Persistir el estado abierto/cerrado por sesion
   (localStorage) es deseable, no obligatorio.
2. **Recientes + Mostrar mas:** cada seccion lista solo los N mas RECIENTES (p.ej. 10, ordenado por fecha/seq desc) +
   boton "Mostrar mas" que carga el siguiente bloque. No volcar todo de golpe.
3. **Legibilidad de filtros:** reemplazar/estilizar los `<select>` para que honren el tema oscuro (tokens del
   design-system: fondo panel, texto ink, hover accent). El texto de las opciones DEBE leerse con contraste suficiente.
4. **Mailbox con filtros:** agregar filtros a Mailbox a paridad con Backlog (p.ej. carpeta/status open/answered/archived,
   remitente from/to, tipo GO/REVIEW/HANDOFF/FYI, y un campo de texto).
5. **Artifacts con combo de tipo:** ademas del campo de texto, un combo por TIPO de artefacto (handoff/review/report/...).

## Fuera de alcance
NO operar/escribir (sigue read-only, F2 gateado post-TFM); NO tocar el binario hermes/HERMES_API_*; NO core ni baseline TFM.

## Criterios de aceptacion (verificar con RENDER HEADLESS, no asumir)
- **AC1:** las 6 secciones son acordeones colapsados por defecto; expanden/colapsan; muestran conteo en el header.
- **AC2:** cada seccion expandida muestra solo los N recientes + "Mostrar mas" funcional (carga mas sin recargar la pagina).
- **AC3:** los combos de filtro son legibles (contraste suficiente, tema oscuro) -- verificar en screenshot que las opciones se leen.
- **AC4:** Mailbox tiene filtros funcionales; Artifacts tiene combo por tipo + el campo de texto.
- **AC5:** read-only preservado; design-system tokens; `pnpm governance:smoke` PASS; f0-test verde.
- **AC6:** checker reproduce con render headless (Playwright/system-chrome via NODE_PATH) + SCREENSHOT que evidencia colapsado-por-defecto + filtros legibles.

## DoD
AC1-AC6 verdes; handoff `in_review` con screenshots (colapsado por defecto + un combo legible + mailbox/artifacts filtros).
Commit Zeus-Aegis como Arquitecto + Co-Authored-By Codex. Leccion [[checker-verify-rendered-not-just-text]] aplica (screenshot obligatorio).
