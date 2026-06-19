---
message_id: MSG-20260619-Operador-to-Arquitecto-GO-lanzar-proyecto-front-T0
type: DECISION
task_id: none
from: Operador
to: Arquitecto
requires_response: true
response_owner: Arquitecto
status: open
one_line_summary: GO a lanzar el PROYECTO-FRONT (UI single-operator para operar/observar la metodologia) como PROYECTO PRIMARIO de tesis y T0. Repo separado, el protocolo lo desarrolla por SDD/handoffs; PII-free -> dataset publicable limpio (sin DEF-PII). Su primer handoff gobernado = T0, atestado bajo #4. SUPERSEDE "DB de Budget = T0" (Budget pasa a proyecto posterior).
requested_action: "Abrir el proyecto-front por SDD: DECISION (alcance/acoplamiento unidireccional, repo separado) + SPEC (MVP single-operator: ver mailbox/estado/decisiones/handoffs/ledger #4; acciones gobernadas via submit_intent; sin bypass de gates) + tasks. Definir repo destino con el operador. El primer handoff gobernado de este proyecto = T0 (atestar en caliente). Usa el floor (Git/CI/skills) conforme aterrice. multi-tenant FUERA de alcance (DECISION aparte). #4 intacto."
question: "Confirmas lanzar el proyecto-front como proyecto primario/T0 (repo separado, MVP single-operator, PII-free) y abres su SDD? Propon el repo destino."
context_refs:
  - personal/operador/sintesis_hoja_de_ruta.html
  - Area_comun/decisions/DECISION-0040-gate-dataset.md
  - Area_comun/decisions/DECISION-0047-versionado-epoca-bajo-4.md
  - Area_comun/mailbox/open/MSG-20260619-Operador-to-Arquitecto-GO-floor-fase1-2
deadline_or_blocking_level: normal
---

# GO - lanzar el PROYECTO-FRONT como proyecto primario y T0

Decision del operador (alcance fijado): construir, **con la propia metodologia**, un **front para lanzar
y operar el protocolo** = prueba real + dataset de tesis. Elecciones:

- **Proyecto-producto SEPARADO** (repo aparte; el protocolo lo desarrolla, acoplamiento unidireccional;
  el core neutral NO se contamina con el producto).
- **Single-operator launcher/UI** (modelo DECISION-0029 intacto). **Multi-tenant FUERA de alcance** ahora
  -> seria un cambio de modelo de confianza (claves por-usuario independientes, aislamiento) y va por su
  propia DECISION mas adelante.
- **Proyecto PRIMARIO de tesis y T0.** Es **PII-free** -> su dataset de coordinacion se puede capturar Y
  publicar **sin** el gate DEF-PII (a diferencia de Budget). **Budget pasa a proyecto posterior** (sigue
  gateado por PII + fin de la DB). Esto **supersede** "el handover de la DB de Budget = T0".

## MVP propuesto (el Arquitecto lo convierte en SPEC; el operador ajusta)
UI local single-operator para **operar y observar** el protocolo:
- **Ver (read):** mailbox (open/answered/archived), estado (PROJECT_STATE/TASK_INDEX/CLAIMS), decisiones/
  specs/tasks, handoffs, y el **ledger atestado #4 / dataset** (epoca, drift, version).
- **Accionar (gobernado):** lanzar un turno/run de agente, crear handoff/mensaje, emitir transiciones
  **via `submit_intent`** (escritor unico, sin bypass de gates ni de #4), disparar validacion.
- **Tech:** a definir en la SPEC (web, para habilitar multi-tenant futuro). Usa los connectors **Git/CI**
  del floor conforme aterricen.

## Compliance (duro)
- **T0:** el primer handoff gobernado de este proyecto es T0; atestar en caliente bajo #4 (ya ON).
- **Neutralidad:** el front es producto en repo aparte; cero producto en el core neutral / `*.template.*`.
- **Sin bypass:** todo write del front al estado/protocolo va por `submit_intent` (gates + #4 + drift).
  Lectura por patron read-only.
- **#4 intacto** (epoca 1.14.0, sin re-genesis; capacidades nuevas fuera del config pinned, DECISION-0047).
- **Una cosa a la vez:** coordinar con el floor en curso (Git/CI/skills); no combinar ventanas de riesgo.
- PII de terceros nunca al event log (aqui ademas el proyecto es PII-free). DEF-PII (TASK-0118) sigue
  diferida (no la necesita este proyecto).

## Siguiente - ubicacion (acoplamiento unidireccional)
El **protocolo/metodologia NO se mueve**: sigue en `D:\Agentes\multi_agent_project_protocol` y GOBIERNA.
Bajo `D:\Agentes\Zeus\` viven solo las **aplicaciones** de la metodologia (los proyectos). Por tanto el
**repo destino del front = `D:\Agentes\Zeus\Zeus-protocol`** (producto, separado del protocolo). Abre ahi
la DECISION+SPEC del proyecto-front. Reporta al cerrar el SDD inicial; ahi nace T0. Canal ASCII.
