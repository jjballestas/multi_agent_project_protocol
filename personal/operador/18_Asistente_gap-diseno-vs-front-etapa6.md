# 18_Asistente - Gap diseno-vs-implementacion del front + brief de correccion (jalado por uso real)

> Insumo del operador (asistente Cowork) para el ARQUITECTO. El asistente NO muta estado: brief de requisitos.
> Fecha: 2026-06-20. Canal ASCII. Pull real: usar el front para desarrollar nova.budget (regla 3.4 satisfecha).
> Evidencia leida en CANONICO de Zeus-protocol (commit 58d39fb): public/index.html, public/app.js,
> public/styles.css, design/interface/front_design_brief.md, design-system/tokens.css.

## 0. Veredicto
El front pasa 15/15 + AC11 pero diverge del diseno. Los AC cubrian gobernanza/honestidad, NO navegacion ni
conformidad con el inventario de pantallas del design brief. Resultado: contenido correcto y gobernado, pero
apilado en un solo scroll y con una pantalla del diseno ausente. Se arregla en UNA tarea SDD, no parche a parche.

## 1. Causa raiz del "single scroll" (P0)
`public/app.js` lineas 365-369: el handler de la nav EXISTE, pero en vez de cambiar de vista hace
`scrollIntoView` sobre el panel dentro de una sola pagina (`.view-grid` con todos los `<article class="panel">`
renderizados a la vez). Marca el nav-item activo y hace scroll suave; NUNCA oculta/muestra. Es scroll-a-ancla,
no router. Por eso clic en "Mailbox" no aisla la vista: todo sigue visible.

## 2. Gaps priorizados (con evidencia)

### P0 - bloquean el uso real
- **(G1) Routing real.** Reemplazar el `scrollIntoView` por enrutado: cada nav-item renderiza SOLO su panel
  RF en el area de contenido; los demas ocultos. Topbar (status) + integrity-band (epoca/drift/atestado/
  canonico/seq) PERSISTEN en todas las vistas (hoy ya estan fuera de `.view-grid`, lineas 31-64: mantenerlos).
- **(G2) Pantalla Backlog AUSENTE.** La nav tiene `data-view="backlog"` (index.html L16) pero NO existe
  `data-panel="backlog"`. Clic en Backlog = no-op (`querySelector(...)?.scrollIntoView` sobre null). El design
  brief 4.3 pide un **kanban** (proposed->ready->in_progress->in_review->done) con **claims** (quien tiene que)
  y **filtro por agente**. La implementacion solo tiene `task-bars` (barras de conteo) DENTRO del panel
  dashboard (L72). Falta: vista propia + tablero kanban + filtro por agente.

### P1 - conformidad de diseno (el "difiere por mucho")
- **(G3) Profundidad del Backlog.** Aun creando la vista, el contenido debe ser kanban con columnas por estado
  + claims + filtro por agente (4.3), no barras de conteo.
- **(G4) Proyecto modelado como ruta de disco, no entidad.** `renderProjects` (app.js L276+) muestra
  branch/head/commit/state y el empty-state dice "No product repos discovered" -> modela REPOS git, no
  entidades-proyecto. El design brief 4.8 es explicito: "modela el proyecto como ENTIDAD que la UI consume via
  API/estado, NO como ruta de disco; `D:\Agentes\Zeus\` es solo la fuente de HOY", para que el salto a
  multi-tenant (§2) no obligue a rediseno. **TENSION CON DECISION-0050** (selector lista repos-producto bajo
  Zeus): no es un bug, es decision de diseno -> el Arquitecto decide: (a) capa de abstraccion "proyecto" que
  HOY se alimenta de los repos en disco pero expone entidad (preferible, honra 4.8 sin romper 0050), o
  (b) aceptar "repos-en-disco por ahora" con nota explicita y deuda registrada.
- **(G5) Guarda PII del Ledger (verificar).** Design 4.5 + AC11 exigen que la vista de procedencia REDACTE el
  texto libre de payloads (nunca crudo). AC11 dice tenerlo cubierto; CONFIRMAR que `renderEvent` (app.js L132)
  redacta de verdad en la vista, no solo en un test. Si esta, no es gap; si no, es P0 (propiedad-tesis).

### P2 - fidelidad / pulido
- **(G6) Tokens de tipografia/espaciado no adoptados.** El `:root` de `public/styles.css` COPIA bien la paleta
  de `tokens.css` (colores identicos), pero OMITE `--font-ui`, `--font-mono` (JetBrains Mono para hashes),
  `--fs-*`, `--sp-*`, `--radius*`. Alinear para densidad/tipografia consistentes con el design-system.
- **(G7) Fidelidad por pantalla.** Hay previews por componente (design/interface/components/*) para dashboard,
  mailbox, backlog, artefactos, ledger, timeline, kanban, badges, selector, acciones-gobernadas. Una pasada
  visual vista-por-vista contra su preview cerraria divergencias finas (solo hice diff estructural).

### NO es gap (consistente con lo acordado)
- **Pantalla Agentes/Roster (design 4.6) ausente de la nav.** Es la etapa 5 / RF-9 **DEFERIDA** (pull-based,
  sin agente que agregar). El diseno tiene 8 pantallas; la nav tiene 7 a proposito. Correcto.

## 3. AC nuevos (PERMANENTES) que la tarea debe traer
- **AC-ROUTING (comportamiento, permanente):** por cada nav-item, test que asevere "clic en X -> SOLO el panel
  X visible; los demas no estan en el DOM visible/`hidden`; topbar+integrity-band siguen presentes". Falla si un
  refactor vuelve a apilar. (Extiende la filosofia de AC11 a la navegacion.)
- **AC-CONFORMIDAD-DISENO (permanente):** las 7 vistas existen y son navegables, y cada una corresponde a su
  pantalla del front_design_brief (Backlog = kanban). "Verde" pasa a significar tambien "coincide con el diseno".

## 4. Brief de tarea para el Arquitecto (mejora tu prompt, por el metodo)
"Arquitecto: jalada por necesidad real (usar el front para nova.budget), autora UNA tarea bajo SPEC-0086
(front etapa 6.1 - view routing + backlog + conformidad de diseno), maker=Codex/checker=Arquitecto, de a una,
reproduccion desde clon limpio. Alcance:
 (1) Routing real: cada nav-item renderiza SOLO su panel RF; reemplaza el scrollIntoView de app.js L365-369;
     topbar+integrity-band persisten en todas las vistas; activo resaltado Y conmuta la vista. Ledger #4 =
     VISTA DEDICADA (el design brief 4.5 lo trata como pantalla de primera clase), no sidebar persistente.
 (2) Crea la vista Backlog ausente (no hay data-panel=backlog) como KANBAN (proposed->ready->in_progress->
     in_review->done) con claims y filtro por agente (design 4.3).
 (3) Resuelve G4 (proyecto entidad-vs-ruta-de-disco, 4.8 vs DECISION-0050): decide capa-entidad o deuda
     registrada; documenta la eleccion.
 (4) Confirma G5 (redaccion PII en la vista del ledger). Alinea tokens de tipografia/espaciado (G6).
 AC: AC-ROUTING (comportamiento, permanente) + AC-CONFORMIDAD-DISENO (permanente) + los ya verdes (read-only,
 submit_intent sin bypass, badge honesto AC11, validate con/sin secretos exit 0, drift 0, #4 epoca 1.14.0
 intacta, neutralidad, CI/node --test verde). Al cerrar: `npm start` ejecutable y las 7 vistas navegan.
 Reporta drafts para mi ratificacion."

## 5. Nota de proceso (para que no se repita)
El hueco no fue de Codex: los AC del MVP no ataban la UI al design brief. Sugerencia para el runbook: cuando
hay design brief, TODA etapa con UI lleva de origen un AC de conformidad de diseno + un test de comportamiento
de interaccion (no solo de gobernanza). Es la misma leccion que AC11, aplicada a UX.
