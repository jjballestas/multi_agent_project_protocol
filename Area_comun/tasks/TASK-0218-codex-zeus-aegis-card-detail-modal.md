---
task_id: TASK-0218
title: "Zeus-Aegis: doble-click en tarjeta (Backlog/Mailbox/Artifacts/Decisiones/Handoffs) abre detalle completo; Esc o boton Cerrar vuelve (DECISION-0064)"
type: product
status: done
owner: Codex
phase: P2
priority: high
created_at: 2026-06-29
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-Aegis
project: Zeus-Aegis
linked_decisions: [DECISION-0064]
file: Area_comun/tasks/TASK-0218-codex-zeus-aegis-card-detail-modal.md
---

# TASK-0218 -- Detalle completo de tarjeta por doble-click (panel governance)

## Contexto (pedido del operador)
En las secciones del panel `/governance` las tarjetas muestran solo un resumen/preview. El operador quiere
**leer el contenido COMPLETO** de una tarjeta con **doble-click**, y volver al estado normal con **Esc** o un
**boton Cerrar**. Aplica a 5 secciones: **Backlog, Mailbox, Artifacts, Decisiones, Handoffs**.

## Objetivo
Doble-click en una tarjeta de esas 5 secciones abre una vista de DETALLE (modal/overlay enfocado) con el contenido
completo del item; se cierra con Esc o con el boton. READ-ONLY, PII-safe, tema oscuro coherente.

## Alcance (governance.tsx + read seam si hace falta exponer mas contenido; READ-ONLY)
1. **Doble-click -> modal de detalle:** `onDoubleClick` en la tarjeta de Backlog/Mailbox/Artifacts/Decisiones/
   Handoffs abre un overlay centrado (modal) con TODOS los campos + contenido completo del item.
   - Componente de detalle GENERICO, parametrizado por tipo (task / message / artifact / decision / handoff).
2. **Cierre:** tecla **Esc** Y un **boton captionado `Cerrar`** (con hint `(Esc)`); click en el backdrop tambien
   cierra. Foco atrapado en el modal (aria-modal, role=dialog), foco vuelve a la tarjeta al cerrar.
3. **Contenido completo + PII-safe:** mostrar el contenido completo del item via el read seam CANONICO aplicando
   la **MISMA redaccion PII** que ya usan los previews (no exponer texto libre sin redactar). Si el endpoint de la
   seccion hoy solo manda preview/truncado, extenderlo (read-only, canonico, redactado) para que el detalle tenga
   el contenido completo. NO writer-path nuevo.
4. Conservar acordeones/filtros/recientes (TASK-0210), carga resiliente (TASK-0212) y, si 0217 ya cerro, la fuente
   unificada del backlog.
5. Estilo: tokens del design-system (fondo panel, texto ink, legible en tema oscuro).

## Criterios de aceptacion (verificar con RENDER HEADLESS)
- **AC1:** doble-click en una tarjeta de CADA una de las 5 secciones abre el modal con el contenido completo del
  item (campos + cuerpo); single-click NO lo abre (no rompe la interaccion normal).
- **AC2:** **Esc** cierra el modal; el **boton `Cerrar`** cierra; el backdrop cierra; al cerrar vuelve al estado
  normal y el foco regresa a la tarjeta.
- **AC3:** contenido PII-redactado (misma redaccion que previews); READ-ONLY (sin ruta de escritura nueva);
  `pnpm governance:smoke` PASS; f0-test verde.
- **AC4:** checker (Arquitecto) reproduce con RENDER HEADLESS + SCREENSHOT: tarjeta -> doble-click -> modal con
  contenido completo -> Esc/boton -> cerrado.

## DoD
AC1-AC4 verdes; handoff `in_review` con screenshots (modal abierto con contenido completo + estado tras cerrar).
Commit Zeus-Aegis como Arquitecto + Co-Authored-By Codex. NO toca core ni baseline TFM. Nota: depende de
0210/0212 (y 0217 si ya cerro) sobre la misma vista -> construir despues de ellas. Leccion
[[checker-verify-rendered-not-just-text]] (screenshot obligatorio).
