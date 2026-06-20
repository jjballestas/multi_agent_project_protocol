---
id: TASK-0132
title: Proyecto-front etapa 6.1 - conformidad de diseno (Backlog kanban + Projects=selector/launcher + proyecto-entidad + PII/tokens) + AC12/AC13 permanentes (SPEC-0086)
type: product
status: done
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0086
linked_decisions: [DECISION-0049, DECISION-0050]
created_at: 2026-06-20
---

# TASK-0132 - Front etapa 6.1 (conformidad de diseno)

## Objective

Cerrar la divergencia diseno-vs-implementacion del front (design brief) para poder USARLO en nova.budget
(necesidad real, regla 3.4). Ratificada por el operador (OPCION A): el routing (G1) ya esta hecho+verificado+
cerrado (TASK-0131, Zeus 2ca79cc); esta tarea cubre el RESTO de la conformidad + formaliza AC12/AC13
permanentes. En `D:\Agentes\Zeus\Zeus-protocol`. maker=Codex / checker=Arquitecto. Etapa 5 roster (RF-9)
DEFERIDA. **NO reabrir el routing verde.**

## Alcance

- **(G2/G3) Backlog = KANBAN (design 4.3):** la vista Backlog (hoy lista simple) pasa a TABLERO kanban con
  columnas `proposed -> ready -> in_progress -> in_review -> done`, tarjetas por columna, **claims** (quien la
  tiene) y **filtro por agente**. Read-only sobre el canonico del hub.

- **(G4) Proyecto = ENTIDAD, no ruta de disco (design 4.8) -- aprobado capa-entidad (a):** el API de proyectos
  del server expone ENTIDADES `{id, name, kind, source, state}` (read-model) alimentadas HOY por los
  repos-producto en disco bajo `D:\Agentes\Zeus\` (fuente de DECISION-0050), pero la UI consume la ENTIDAD, no
  el path. Honra 4.8 (futuro multi-tenant) SIN romper DECISION-0050. Documentar la eleccion.

- **(ADDENDUM operador) Vista Projects (RF-12) = SELECTOR/launcher, no lista read-only:** rehacer la vista
  Projects segun `design/interface/components/selector/index.html` (hoy es una lista estatica name/branch/head/
  commit/state). Debe traer:
  - **(a)** tarjetas-ENTIDAD del proyecto (modelo G4 `{id,name,kind,source,state}`) con badges por-proyecto,
    que al abrir entran a la mission-control de ESE proyecto.
  - **(b)** una tarjeta **"+ add project"** (addcard del diseno) para LANZAR un proyecto nuevo DESDE el selector,
    **cableada a la accion gobernada RF-10 "Project kickoff T0" que YA existe** en `src/server.js`
    (`intentKinds: ["task_upsert"]`, `idempotency_key front:project-kickoff-t0`, via `runtime/submit_intent.py`)
    -- hoy esa accion solo aparece en la vista Operate, desconectada del selector; surfaceala EN el selector.
  - El front **NO** hace `mkdir`/`writeFile`/`git-init`: el `git init` del repo nuevo es paso MANUAL del
    operador; el selector solo emite el T0 gobernado por `submit_intent` (sin bypass; **prueba negativa intacta**).

- **(G5) Confirmar redaccion PII en la vista del ledger:** `renderEvent` ya redacta `payloadPreview`
  ("[redacted - PII de tercero]"); CONFIRMAR que la vista NUNCA muestra texto libre crudo (no solo el test) y
  dejarlo cubierto por AC11 + el test de conformidad. Si falta, es P0.

- **(G6) Tokens del design-system:** `public/styles.css` adopta `--font-ui/--font-mono` (JetBrains Mono para
  hashes), `--fs-*`, `--sp-*`, `--radius*` de `design-system/tokens.css` (hoy solo copia la paleta).

- **(G7) Fidelidad por pantalla:** pasada vista-por-vista contra `design/interface/components/*`; cerrar
  divergencias finas.

## AC nuevos PERMANENTES (condicion de cierre innegociable; agregados a SPEC-0086)

- **AC12 - AC-ROUTING (comportamiento, permanente):** por cada nav-item, test que asevere "clic en X -> SOLO el
  panel X visible (los demas `hidden`); topbar + integrity-band siguen presentes". Falla si un refactor vuelve
  a apilar. (Ya satisfecho por los tests de TASK-0131; queda permanente.)
- **AC13 - AC-CONFORMIDAD-DISENO (permanente):** las 7 vistas existen, navegables y cada una corresponde a su
  pantalla del `front_design_brief` (Backlog=kanban; Projects=selector con entity-cards + add-project cableado
  al kickoff RF-10). "Verde" pasa a significar tambien "coincide con el diseno". (La pantalla Agentes/Roster
  4.6 NO cuenta: RF-9 etapa5 DEFERIDA; la nav tiene 7 a proposito.)

## DoD

- Backlog kanban (columnas + claims + filtro por agente); Projects=selector (entity-cards que abren
  mission-control + "+ add project" cableado al kickoff RF-10 gobernado, sin git-init del front, prueba
  negativa verde); proyecto-entidad documentado; PII del ledger confirmada en la vista; tokens adoptados;
  fidelidad por pantalla.
- **AC12/AC13 en SPEC-0086** (ya agregados por el Arquitecto) cubiertos por tests de comportamiento.
- `node --test` verde (>= los 17 actuales + nuevos), gateado por EXIT REAL; `node --check` OK; **`npm start`
  ejecutable y las 7 vistas navegan**.
- Ya-verdes intactos: read-only (sin ruta de escritura nueva del front; toda escritura por submit_intent),
  AC11 badge honesto, validate con/sin secretos exit 0, drift 0, #4 epoca 1.14.0 pinned, neutralidad.
  Codigo en Zeus-protocol; gobernanza en Area_comun.
- maker=Codex / checker=Arquitecto; reproduccion del checker desde clon limpio.

## Verification

- CI del producto verde (node --test) incl. AC12 (routing comportamiento) + AC13 (conformidad: 7 vistas,
  Backlog=kanban, Projects=selector con add-project gobernado) + AC11 (PII redactada en la vista) + prueba
  negativa (kickoff/selector solo via submit_intent; sin mkdir/writeFile/git-init en el front).
- Gates del protocolo exit 0 (con y sin secretos), drift 0, gateado por EXIT REAL del validador.
