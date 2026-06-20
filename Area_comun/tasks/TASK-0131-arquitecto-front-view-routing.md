---
id: TASK-0131
title: Proyecto-front - routing real de vistas (cada nav item renderiza SOLO su panel; header persistente) (SPEC-0086 RF-1..RF-12)
type: product
status: done
owner: Arquitecto
phase: P2
priority: high
spec_id: SPEC-0086
linked_decisions: [DECISION-0049, DECISION-0050]
created_at: 2026-06-20
---

# TASK-0131 - Front: routing real de vistas

## Objective

Pedido directo del operador. Hoy el sidebar tiene 7 nav items (Dashboard, Mailbox, Backlog, Artifacts,
Ledger #4, Operate, Projects) pero al clickear NO cambia la vista: la app es un scroll unico con todos los
paneles apilados (el handler solo hace `scrollIntoView`). Implementar **routing real de vistas**: cada nav
item renderiza SOLO su panel en el area de contenido. En `D:\Agentes\Zeus\Zeus-protocol`. maker=Arquitecto
(operador-dirigido); aceptacion visual del operador en el browser = checker. Read-only intacto (sin nueva
ruta de escritura; #4 epoca 1.14.0 pinned).

## Alcance

- Cada nav item (`data-view`) muestra SOLO su panel (`data-panel`) y oculta los demas. Activo resaltado
  (ya existe) Y cambia la vista de verdad.
- **Header persistente** en todas las vistas: topbar (status/source) + integrity-band (epoch/drift/attested/
  canonical/validator) + metrics (seq/mailbox/claims/tasks) quedan FUERA del area ruteada.
- **Ledger #4 = su propia vista dedicada** (decision aplicada de forma consistente; sin sidebar derecho
  persistente). El `view-grid` pasa a mostrar un panel a la vez (ancho completo).
- **Backlog** (nav item hoy sin panel) recibe una vista real: lista de tareas abiertas (id/titulo/owner/
  status/priority) read-only desde el modelo observado.
- Logica de routing en funcion PURA testeable (`resolveActiveView` + `computeViewVisibility`): solo la vista
  activa visible; vista desconocida -> fallback dashboard. Se elimina el `scrollIntoView` (el bug).

## DoD

- Clickear "Mailbox" muestra SOLO mailbox; "Artifacts" SOLO artifacts; etc. (los 7 nav items rutean a un
  unico panel). Header (epoch/drift/attested/seq) visible en todas las vistas.
- `node --test` verde (>= los 15 actuales + nuevos de routing), gateado por EXIT REAL; `node --check` OK;
  app ejecutable (`npm start`) y sirve los assets actualizados (smoke server).
- Read-only intacto: ninguna ruta de escritura nueva; sin tocar #4/config (epoca 1.14.0).
- Gates del protocolo (gobernanza de esta tarea en Area_comun): `validate_collaboration_state.py --root .`
  CON y SIN secretos exit 0; drift 0.

## Verification

- Test de comportamiento del routing (funcion pura): `computeViewVisibility(v)` deja SOLO `v` visible;
  `resolveActiveView(desconocido)` -> dashboard. Contrato estatico: los 7 `data-view` tienen su `data-panel`;
  `showView` + `toggleAttribute("hidden", ...)` presentes; `scrollIntoView` AUSENTE.
- Smoke del server (`npm start`): `/healthz`, `/api/protocol/observe` OK; assets servidos.
- Gates del protocolo exit 0 (con y sin secretos), drift 0, gateado por EXIT REAL.
