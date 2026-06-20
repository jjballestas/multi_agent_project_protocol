---
message_id: MSG-20260620-Arquitecto-to-Operador-etapa6.1-draft
type: FYI
task_id: none
from: Arquitecto
to: Operador
status: archived
requires_response: false
one_line_summary: Respuesta a GO-etapa6.1 - alcance confirmado + draft TASK-0132 listo para tu ratificacion. RECONCILIACION: el routing (G1) ya estaba HECHO+VERIFICADO+CERRADO como TASK-0131 (Zeus 2ca79cc, Codex verifico, yo cerre); etapa 6.1 cubre el RESTO (Backlog kanban, proyecto-entidad, PII-confirm, tokens, fidelidad) + 2 AC permanentes. G4 decidido = capa-entidad (a). No promovi: espero tu GO de ratificacion. maker=Codex.
context_refs:
  - personal/Arquitecto/carril_A/DRAFT-TASK-0132-front-etapa6.1.md
  - Area_comun/tasks/TASK-0131-arquitecto-front-view-routing.md
  - personal/operador/18_Asistente_gap-diseno-vs-front-etapa6.md
deadline_or_blocking_level: normal
---

# Respuesta a GO-etapa6.1: draft listo para ratificacion

**Alcance confirmado.** Una aclaracion importante (colision temporal): tu gap brief se escribio sobre Zeus
58d39fb, ANTES de que arreglara el routing. Estado real:

- **G1 ROUTING REAL: HECHO, VERIFICADO Y CERRADO.** Lo implemente yo (Zeus **2ca79cc**: scrollIntoView
  reemplazado por routing real, header persistente, Ledger #4 vista propia, Backlog con vista). Codex lo
  verifico INDEPENDIENTE (17/17, read-only, drift 0, smoke) y movio a in_review; yo (reviewer) cerre
  **TASK-0131 done**. maker!=checker preservado (autor=Arquitecto, verificador=Codex, cierre=reviewer) --
  asi resolvimos el capability-gate que mencione.

- **Etapa 6.1 (DRAFT TASK-0132) = el RESTO de la conformidad de diseno** (no re-hace lo verde): Backlog
  **kanban** (4.3, claims + filtro por agente), proyecto-**entidad** (4.8), confirmar PII en la vista (4.5),
  tokens del design-system, fidelidad por pantalla. maker=Codex/checker=Arquitecto.

- **Los 2 AC nuevos PERMANENTES** quedan en la tarea, a agregar a SPEC-0086 como **AC12 (AC-ROUTING,
  comportamiento)** -- ya satisfecho por los tests de TASK-0131, se vuelve permanente -- y **AC13
  (AC-CONFORMIDAD-DISENO)**: las 7 vistas existen, navegables, cada una = su pantalla del design brief
  (Backlog=kanban). Tu leccion de proceso (UI -> AC de conformidad + test de comportamiento de interaccion)
  la anoto para el runbook.

- **G4 (proyecto entidad-vs-ruta-de-disco) DECIDIDO por mi = (a) capa-entidad:** el API expone entidades
  `{id,name,kind,source,state}` alimentadas HOY por los repos bajo Zeus (fuente de DECISION-0050), pero la UI
  consume la ENTIDAD, no el path -> honra design 4.8 (futuro multi-tenant sin rediseno) SIN romper 0050.

**No promovi nada por submit_intent** (espero tu ratificacion). Draft completo en
`personal/Arquitecto/carril_A/DRAFT-TASK-0132-front-etapa6.1.md`. UNA decision para vos: banked-routing
(TASK-0131 cerrado) + 6.1-para-el-resto = RECOMENDADO (no re-hace lo verde); o preferis UNA tarea-paraguas
que reabra routing. Con tu GO de ratificacion lo promuevo y Codex implementa. Canal ASCII.
