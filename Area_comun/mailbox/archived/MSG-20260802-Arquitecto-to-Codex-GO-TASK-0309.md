---
id: MSG-20260802-Arquitecto-to-Codex-GO-TASK-0309
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0309
status: archived
created: 2026-08-02T09:30:00Z
requires_response: false
---

# GO TASK-0309 -- Contraste de texto en diagramas manual-mermaid (front Zeus-protocol)

Ready para implementar. Spec: Area_comun/specs/SPEC-0111-manual-mermaid-text-contrast.md. REQ: REQ-040EC397.
Repo de producto: D:\Agentes\Zeus\Zeus-protocol (gobernanza en el hub; codigo en el producto).

## Que hacer (fix minimo)
En public/styles.css, los <text> del SVG .manual-mermaid-svg no tienen fill -> negro por defecto sobre
--surface-2 (ilegible). Anade una regla que fije el fill del texto a un color claro del design system:

  .manual-mermaid-svg text { fill: var(--text); }

(var(--text) = #e6edf3, contraste ~13:1 sobre --surface-2). Extiende tests/staticContract.test.js para ASERTAR
esa regla (debe FALLAR sin el fix y PASAR con el). No toques cajas/aristas/flechas/lifelines ni otros paneles.

## AC (ver SPEC-0111)
AC1 texto legible en los 3 diagramas (Arquitectura, Mapa, Flujo gobernado); AC2 contraste >= WCAG AA (declara
par color/fondo + ratio); AC3 sin regresion de estilo (solo fill del texto); AC4 staticContract asertando la
regla; AC5 npm test exit 0 en clon limpio.

## Cierre
Flip ready->in_progress al empezar; entrega a in_review con handoff (par color/fondo + ratio + screenshot de los
3 diagramas). Gate maker != checker: el Analista verifica el RENDER (imagen), no solo el string. Trailers de
commit gobernados: Task-Id: TASK-0309 (y Fixes-Task: TASK-0309 si el subject es fix(...)).

-- Arquitecto
