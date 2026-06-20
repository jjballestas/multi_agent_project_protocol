---
id: TASK-0132
title: Proyecto-front etapa 6.1 - conformidad de diseno (Backlog kanban + proyecto-entidad + PII/tokens) + 2 AC permanentes (SPEC-0086)
type: product
status: ready
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0086
linked_decisions: [DECISION-0049, DECISION-0050]
created_at: 2026-06-20
---

# DRAFT TASK-0132 - Front etapa 6.1 (conformidad de diseno) -- para ratificacion del operador

> DRAFT en area personal. NO promover por submit_intent hasta ratificacion del operador (GO-etapa6.1).
> maker=Codex / checker=Arquitecto. Jalada por necesidad real (usar el front para nova.budget, regla 3.4).

## Reconciliacion (importante)

El GO-etapa6.1 + el gap brief (18_Asistente, escrito sobre Zeus 58d39fb) listan 4 partes. La parte (1)
**ROUTING REAL (G1) YA ESTA HECHA Y CERRADA**: la implemente yo (Arquitecto, Zeus 2ca79cc), la verifico
INDEPENDIENTE Codex (17/17, read-only, drift 0) y la cerre como **TASK-0131 done**. Por eso etapa 6.1
(TASK-0132) cubre el RESTO de la conformidad de diseno + formaliza los 2 AC permanentes (el AC-ROUTING ya
queda SATISFECHO por los tests de TASK-0131; aca se vuelve permanente). Si preferis una sola tarea-paraguas
que reabra routing, decimelo; recomiendo banked-routing + 6.1-para-el-resto (no re-hacer lo verde).

## Objective

Cerrar la divergencia diseno-vs-implementacion del front (design brief) para poder USARLO en nova.budget.
En `D:\Agentes\Zeus\Zeus-protocol`. Routing (G1) = done (TASK-0131); esta tarea cubre G2..G7 + 2 AC nuevos
PERMANENTES. Etapa 5 roster (RF-9) sigue DEFERIDA.

## Alcance

- **(G2/G3) Backlog = KANBAN (design 4.3):** la vista Backlog (hoy lista simple, heredada de TASK-0131) pasa a
  TABLERO kanban con columnas `proposed -> ready -> in_progress -> in_review -> done`, tarjetas de tarea por
  columna, **claims** (quien la tiene) y **filtro por agente**. Read-only sobre el canonico del hub.
- **(G4) Proyecto = ENTIDAD, no ruta de disco (design 4.8). DECISION del Arquitecto = (a) capa-entidad:**
  el API de proyectos del server expone ENTIDADES `{id, name, kind, source, state}` (read-model) alimentadas
  HOY por los repos-producto en disco bajo `D:\Agentes\Zeus\` (la fuente de DECISION-0050), pero la UI consume
  la ENTIDAD, no el path. Asi honra 4.8 (salto futuro a multi-tenant sin rediseno) SIN romper DECISION-0050
  (la gobernanza sigue en el hub; el disco es solo la fuente de hoy). Documentar la eleccion (nota corta en el
  task/handoff; sin tocar el core neutral).
- **(G5) Confirmar redaccion PII en la vista del ledger:** `renderEvent` ya pinta `payloadPreview` redactado
  ("[redacted - PII de tercero]"); CONFIRMAR que la vista nunca muestra texto libre crudo (no solo el test) y
  dejarlo cubierto por AC11 + el test de conformidad. Si falta, es P0.
- **(G6) Tokens del design-system:** `public/styles.css` adopta `--font-ui/--font-mono` (JetBrains Mono para
  hashes), `--fs-*`, `--sp-*`, `--radius*` de `design-system/tokens.css` (hoy solo copia la paleta de color).
- **(G7) Fidelidad por pantalla:** pasada vista-por-vista contra `design/interface/components/*` (dashboard,
  mailbox, backlog/kanban, artefactos, ledger/timeline, badges, selector, acciones); cerrar divergencias finas.

## AC nuevos PERMANENTES (a agregar a SPEC-0086 como AC12/AC13)

- **AC12 - AC-ROUTING (comportamiento, permanente):** por cada nav-item, test que asevere "clic en X -> SOLO el
  panel X visible (los demas `hidden`/fuera del DOM visible); topbar + integrity-band siguen presentes". Falla
  si un refactor vuelve a apilar. (Ya satisfecho por los tests de TASK-0131; queda permanente.)
- **AC13 - AC-CONFORMIDAD-DISENO (permanente):** las 7 vistas existen, son navegables y cada una corresponde a
  su pantalla del `front_design_brief` (Backlog = kanban). "Verde" pasa a significar tambien "coincide con el
  diseno". (La pantalla Agentes/Roster, design 4.6, NO cuenta: es RF-9 etapa5 DEFERIDA; la nav tiene 7 a
  proposito.)

## DoD

- Backlog kanban operativo (columnas por estado + claims + filtro por agente), read-only.
- Proyecto-entidad: API expone entidad (no path); eleccion (a) documentada.
- PII del ledger confirmada redactada en la vista; tokens del design-system adoptados; fidelidad por pantalla.
- AC12/AC13 agregados a SPEC-0086 (permanentes) + tests de comportamiento que los cubren.
- `node --test` verde (>= los 17 actuales + nuevos), gateado por EXIT REAL; `node --check` OK; **`npm start`
  ejecutable y las 7 vistas navegan**.
- Ya-verdes intactos: read-only (sin ruta de escritura nueva), submit_intent sin bypass, AC11 badge honesto,
  validate con/sin secretos exit 0, drift 0, #4 epoca 1.14.0 pinned, neutralidad. Codigo en Zeus-protocol;
  gobernanza en Area_comun.
- maker=Codex / checker=Arquitecto; reproduccion del checker desde clon limpio.

## Verification

- CI del producto verde (node --test) incl. AC12 (routing comportamiento) + AC13 (conformidad: 7 vistas,
  Backlog=kanban) + AC11 (PII redactada en la vista). Gates del protocolo exit 0 (con y sin secretos), drift 0,
  gateado por EXIT REAL.
