---
message_id: MSG-20260619-Operador-to-Arquitecto-convencion-repos-front-panel
type: DECISION
task_id: none
from: Operador
to: Arquitecto
requires_response: true
response_owner: Arquitecto
status: answered
one_line_summary: Registrar en runbook + AGENTS.md la convencion de repos/operacion: gobernanza/atestacion SIEMPRE en el protocolo; codigo de producto SIEMPRE en su repo bajo D:\Agentes\Zeus; el runtime de cada agente accede a ambos POR RUTA (ya configurado); el FRONT es el panel del operador -> VS Code es OPCIONAL (no se necesita multi-root). Patron repetible para proyectos futuros.
requested_action: "Registrar la convencion (abajo) en el runbook y en AGENTS.md (seccion de arquitectura de repos / acoplamiento unidireccional), via flujo gobernado (DECISION ligera o edicion atestada por submit_intent). Es convencion de metodologia, NEUTRAL (cero dominio). NO toca el config pinned (#4 intacto; AGENTS.md no esta pinned por el genesis)."
question: "Confirmas registrar esta convencion (governance-en-protocolo / codigo-en-repo-de-producto / runtime-por-ruta / front = panel del operador, VS Code opcional) en runbook + AGENTS.md por flujo gobernado?"
context_refs:
  - AGENTS.md
  - Area_comun/decisions/DECISION-0049-proyecto-front-primario-t0-zeus.md
  - personal/operador/sintesis_hoja_de_ruta.html
deadline_or_blocking_level: normal
---

# Convencion de repos y operacion (registrar en runbook + AGENTS.md)

Para que nadie vuelva a asumir que hace falta "VS Code multi-root", fija esta convencion:

1. **Gobernanza / coordinacion / atestacion -> SIEMPRE en el protocolo** (`multi_agent_project_protocol`):
   DECISION/SPEC/tasks/handoffs/mailbox + `submit_intent` + ledger #4. **Es el dataset.** Nunca dentro de un
   repo de producto (alli no se atestaria).
2. **Codigo de producto -> SIEMPRE en su repo bajo `D:\Agentes\Zeus\`** (acoplamiento unidireccional; el
   core neutral del protocolo NO se toca). Hoy: `Zeus-protocol`.
3. **El runtime de cada agente accede a AMBOS por RUTA** (ya configurado): Codex commitea codigo en
   `Zeus-protocol` y atesta gobernanza en el protocolo, sin necesitar ningun workspace de VS Code.
4. **El FRONT (`Zeus-protocol`) es el PANEL del operador** -> reemplaza la necesidad de VS Code para
   **operar y observar** la metodologia (ver mailbox/estado/ledger/atestacion, dar GOs, lanzar agentes,
   multi-proyecto). **VS Code = OPCIONAL** (solo para mirar codigo crudo). El "multi-root" era andamio
   temporal, no requisito.
5. **Patron repetible:** cada proyecto futuro (Budget, etc.) tiene su propio repo bajo `D:\Agentes\Zeus\`;
   la gobernanza de TODOS vive en el unico protocolo (hub permanente). Los repos de producto rotan; el
   protocolo es constante.

Registrar en runbook + AGENTS.md (s. arquitectura de repos / acoplamiento). #4 intacto (epoca 1.14.0;
AGENTS.md no esta pinned). Neutral. Canal ASCII.
