---
message_id: MSG-20260620-Operador-to-Arquitecto-addendum-TASK-0132-selector
task_id: TASK-0132
type: DECISION
from: Operador
to: Arquitecto
status: open
requires_response: false
response_owner: Arquitecto
one_line_summary: "Addendum a TASK-0132 (antes de promover): la vista Projects debe ser el SELECTOR/launcher del design component, no la lista read-only de hoy. Explicito: (1) tarjetas-ENTIDAD que abren mission-control; (2) tarjeta '+ add project' CABLEADA al kickoff RF-10 que YA existe en src/server.js (GOVERNED_ACTIONS 'Project kickoff T0', task_upsert via submit_intent), surfaceado EN EL SELECTOR, no solo en Operate. El git-init del repo sigue siendo paso manual del operador (sin bypass). Cae dentro de la conformidad 4.8 + fidelidad por pantalla, pero lo fijo explicito para que no se cuele."
requested_action: "Antes de promover TASK-0132, incorpora explicito al alcance: la vista Projects (RF-12) se rehace como el SELECTOR del componente de diseno (design/interface/components/selector/index.html), no la lista read-only actual ('hub-centric read-only selector' en index.html solo pinta tarjetas estaticas name/branch/head/commit/state). Debe traer: (a) tarjetas-ENTIDAD del proyecto (modelo G4 capa-entidad ya aprobado: {id,name,kind,source,state}) con badges por-proyecto, que al abrir entran a la mission-control de ESE proyecto; (b) una tarjeta '+ add project' (la addcard del diseno) para LANZAR un proyecto nuevo desde el selector, CABLEADA a la accion gobernada RF-10 'Project kickoff T0' que YA existe en src/server.js (intentKinds task_upsert, idempotency_key front:project-kickoff-t0, via runtime/submit_intent.py) -- hoy esa accion solo aparece en la vista Operate, desconectada del selector. El front NO hace mkdir/writeFile/git-init: el git-init del repo nuevo es paso manual del operador; el selector solo registra el T0 gobernado por submit_intent (prueba negativa intacta). AC13 (conformidad-diseno) cubre que la vista Projects = el selector del design brief 4.8. Resto de TASK-0132 sin cambios (Backlog kanban, PII-confirm, tokens, fidelidad). maker=Codex/checker=Arquitecto."
question: none
context_refs:
  - Area_comun/mailbox/open/MSG-20260620-Operador-to-Arquitecto-GO-ratifica-TASK-0132.md
  - personal/Arquitecto/carril_A/DRAFT-TASK-0132-front-etapa6.1.md
  - D:/Agentes/Zeus/Zeus-protocol/design/interface/components/selector/index.html
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
  - D:/Agentes/Zeus/Zeus-protocol/public/app.js
deadline_or_blocking_level: normal
---

# Addendum a TASK-0132: la vista Projects debe ser el SELECTOR, no una lista read-only

Verifique el front (Zeus 2ca79cc) contra el componente de diseno del selector. La vista Projects de hoy es
una **lista read-only** (panel "hub-centric read-only selector": tarjetas estaticas name/branch/head/commit/
state). **Le faltan las afordancias del selector del diseno** y por eso no puedo cargar/lanzar proyectos
nuevos desde ahi.

Lo concreto a fijar en TASK-0132 (cae en conformidad 4.8 + fidelidad, pero lo hago explicito):

1. **Tarjetas-ENTIDAD que abren mission-control** (modelo G4 capa-entidad ya aprobado), con badges por-proyecto.
2. **Tarjeta "+ add project" para lanzar un proyecto nuevo DESDE el selector**, cableada al kickoff **RF-10 que
   YA existe** en `src/server.js` (accion gobernada "Project kickoff T0", `task_upsert` via submit_intent).
   Hoy ese kickoff solo vive en la vista **Operate**, desconectado del selector. El `git init` del repo sigue
   siendo mi paso manual; el front solo emite el T0 gobernado por submit_intent (sin bypass, prueba negativa
   intacta).

No reabras lo verde (routing TASK-0131). Resto de TASK-0132 igual. Verifico tu cierre en canonico. Canal ASCII.
