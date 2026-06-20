---
message_id: MSG-20260620-Operador-to-Arquitecto-GO-front-etapa6.1-routing-conformidad
task_id: none
type: DECISION
from: Operador
to: Arquitecto
status: open
requires_response: true
response_owner: Arquitecto
one_line_summary: "GO: autora UNA tarea bajo SPEC-0086 (front etapa 6.1 - view routing + Backlog kanban + conformidad de diseno), jalada por necesidad REAL (usar el front para desarrollar nova.budget, regla 3.4). El front pasa 15/15 pero diverge del design brief: la nav no enruta (hace scrollIntoView, todo en un solo scroll) y la pantalla Backlog no existe. maker=Codex/checker=Arquitecto, de a una, con DOS AC nuevos PERMANENTES (routing-comportamiento + conformidad-diseno). Drafts para mi ratificacion."
requested_action: "Autora la tarea de correccion bajo SPEC-0086. Alcance: (1) ROUTING REAL: cada nav-item renderiza SOLO su panel RF; reemplaza el scrollIntoView de public/app.js (L365-369) por enrutado real; topbar + integrity-band (epoca/drift/atestado/canonico/seq) PERSISTEN en todas las vistas; activo resaltado Y conmuta la vista. Ledger #4 = VISTA DEDICADA (design brief 4.5 lo trata como pantalla de primera clase), no sidebar. (2) Crea la vista BACKLOG ausente (la nav tiene data-view=backlog pero NO hay data-panel=backlog -> clic = no-op) como KANBAN proposed->ready->in_progress->in_review->done con claims y filtro por agente (design 4.3); hoy solo hay task-bars dentro de dashboard. (3) Resuelve la tension proyecto-entidad-vs-ruta-de-disco (design 4.8 'modela el proyecto como entidad, no ruta de disco' vs DECISION-0050 'lista repos bajo Zeus'): decide capa-entidad (preferible) o deuda registrada; documenta. (4) Confirma la redaccion PII en la vista del ledger (renderEvent, design 4.5 + AC11). Alinea tokens de tipografia/espaciado que public/styles.css omite (--font-mono/--fs-*/--sp-*/--radius* del design-system). AC: AC-ROUTING (test de COMPORTAMIENTO permanente: clic en X -> solo panel X visible, demas ocultos, topbar/integrity-band presentes) + AC-CONFORMIDAD-DISENO (permanente: las 7 vistas existen, son navegables y corresponden a su pantalla del front_design_brief; Backlog=kanban) + los ya verdes (read-only, submit_intent sin bypass, AC11 badge honesto, validate con/sin secretos exit 0, drift 0, #4 epoca 1.14.0 intacta, neutralidad, node --test/CI verde). Al cerrar: npm start ejecutable y las 7 vistas navegan. maker=Codex / checker=Arquitecto, reproduccion desde clon limpio. Etapa 5 roster (RF-9) sigue DEFERIDA. Reporta drafts para mi ratificacion antes de promover por submit_intent."
question: "Confirmas el alcance y autoras la tarea (front etapa 6.1) con los dos AC nuevos permanentes? Detalle/evidencia en personal/operador/18_Asistente_gap-diseno-vs-front-etapa6.md."
context_refs:
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/decisions/DECISION-0050-convencion-repos-gobernanza-producto.md
  - D:/Agentes/Zeus/Zeus-protocol/design/interface/front_design_brief.md
  - D:/Agentes/Zeus/Zeus-protocol/public/app.js
  - D:/Agentes/Zeus/Zeus-protocol/public/index.html
deadline_or_blocking_level: normal
---

# GO - front etapa 6.1: view routing + Backlog kanban + conformidad de diseno

Necesidad REAL (jala el trabajo, regla 3.4): quiero **usar el front para desarrollar nova.budget**, y el
resultado diverge del diseno por mucho. El front pasa 15/15 + AC11, pero los AC cubrian gobernanza/honestidad,
no navegacion ni conformidad con el inventario de pantallas del design brief.

## Lo que esta mal (evidencia en canonico de Zeus-protocol)
- **Routing roto (P0):** `public/app.js` L365-369: la nav hace `scrollIntoView` sobre paneles apilados en una
  sola pagina, no conmuta vista. Clic en "Mailbox" no aisla nada.
- **Pantalla Backlog ausente (P0):** la nav tiene `data-view="backlog"` pero NO existe `data-panel="backlog"`
  -> clic = no-op. El design 4.3 pide kanban con claims y filtro por agente; hoy solo hay barras de conteo en
  dashboard.
- **Proyecto como ruta de disco (P1):** `renderProjects` modela repos git, no la entidad-proyecto que pide
  el design 4.8 (tension con DECISION-0050 -> tu decides capa-entidad o deuda registrada).
- **Verificar (P1):** redaccion PII en la vista del ledger (design 4.5 / AC11).
- **Pulido (P2):** tokens de tipografia/espaciado del design-system que `styles.css` no adopta.

## Lo que pido
Una tarea SDD bajo SPEC-0086 que cierre lo anterior, con **dos AC nuevos PERMANENTES**: AC-ROUTING (test de
comportamiento) y AC-CONFORMIDAD-DISENO. Detalle completo y brief listo en
`personal/operador/18_Asistente_gap-diseno-vs-front-etapa6.md`.

**No es culpa de Codex:** el hueco fue que los AC del MVP no ataban la UI al design brief. Sugerencia para el
runbook: toda etapa con UI lleva de origen AC de conformidad + test de comportamiento de interaccion (misma
leccion que AC11, aplicada a UX).

Etapa 5 roster (RF-9) sigue DEFERIDA. Drafts primero para mi ratificacion. Canal ASCII.
