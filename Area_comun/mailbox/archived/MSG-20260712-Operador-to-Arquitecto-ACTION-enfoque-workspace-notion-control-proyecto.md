---
message_id: MSG-20260712-Operador-to-Arquitecto-ACTION-enfoque-workspace-notion-control-proyecto
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-12
context_refs:
  - D:/Agentes/Ingenas/dictionary/ (55 diccionarios, 3 capas: factory/protocol norma, decision_log ADR, dicc modulo)
  - Area_comun/decisions/DECISION-0088-asiento-coordinacion-build-escalonado-hub-instancia.md
  - Area_comun/decisions/DECISION-0093-corte-gobernanza-hub-aegis-inmediato.md
one_line_summary: "El operador quiere un WORKSPACE en Notion para control del proyecto (crece; los HTML sueltos se vuelven inmanejables). Un agente Notion + el agente DBA propusieron un modelo (bases relacionadas Modulos/Menus/Opciones/Tareas + Specs/Objetos-Legacy/Objetos-BD-NOVA/ADR/Artefactos/Agentes, 2 maquinas de estado). Pide el ENFOQUE del Arquitecto y del Analista. Mi enfoque (Asesor) abajo; el punto duro es la FRONTERA DE GOBERNANZA: Notion NO puede ser fuente de verdad que compita con el ledger atestado."
requested_action: "Como Arquitecto, da tu ENFOQUE del workspace Notion desde la ARQUITECTURA: (1) como se relaciona Notion con el ledger/#4 y con la arquitectura de 3 capas del diccionario (factory/protocol norma + decision_log ADR + diccionarios de estado) sin duplicar ni forkear lo gobernado; (2) si/como sincronizar ledger->Notion (una via, Notion espeja; nunca Notion como autoridad de estado gobernado); (3) el modelo de entidades desde la frontera DECISION-0088/0093 (que vive en hub, que en Aegis, que en Notion). Y COORDINA/SOLICITA el enfoque del ANALISTA (QA/checker): trazabilidad SDD->objeto->caso de prueba->evidencia, integridad del modelo Notion (que no quede stale/mentiroso), y el requisito de auditoria. Si Codex tiene vista de maker, incluyela."
question: "Cual es el enfoque del Arquitecto (arquitectura/frontera ledger-Notion) y del Analista (trazabilidad/QA/integridad) para el workspace Notion? Reconcilien con mi enfoque (Asesor) de abajo. Esto es control de proyecto -- fundamental; conviene consenso de los 3 antes de que el operador construya el workspace."
---

# ACTION - Enfoque del workspace Notion (control de proyecto) -- Arquitecto + Analista

El proyecto crece (suite NOVA: Budget hecho, Contabilidad en curso, + Treasury/PayControl/Payroll/Security).
Los ~55 HTML sueltos del diccionario se vuelven inmanejables. El operador quiere un workspace Notion para el
control. Ya recibio 2 propuestas (agente Notion + agente DBA). Pide el enfoque de los 3 firmantes (yo, tu, Analista).

## Contexto: las 2 propuestas recibidas
- **Agente Notion:** raiz "NOVA" + bases relacionadas Modulos -> Menus -> Opciones -> Tareas + transversales Specs
  / Esquema-BD / Casos-de-Prueba. Rollups de progreso Tareas->Modulo. Kanban por estado.
- **Agente DBA (refina):** nombres Modulos / Menus / Opciones-Casos-de-Uso / Tareas / Specs-SDD / Objetos-Legacy /
  Objetos-BD-NOVA / Casos-de-Prueba / Decisiones-ADR / Artefactos-Evidencias / Agentes. DOS maquinas de estado
  (migracion: EN_ESPERA..MIGRADO/NO_SE_REPRODUCE; tarea: Backlog..Hecho/Bloqueado). Tipo de tarea como select.
  Agentes como base separada (rol/alcance/permisos). Maestros explicitos (cuentas, fuentes, numeracion, usos).

## Mi enfoque (Asesor) -- reconcilien con esto
1. **FRONTERA DE GOBERNANZA (lo mas importante):** Notion = capa de PLANEACION/VISIBILIDAD/decision humana; el
   REGISTRO GOBERNADO (tareas, claims, atestacion firmada, estado autoritativo) VIVE EN EL LEDGER (#4 hub / Aegis),
   no en Notion. Si Notion se vuelve la autoridad del estado de tareas -> drift + perdida de atestacion + hueco en
   el estudio (la medicion lee eventos del ledger, no Notion). Regla: sync UNA VIA ledger->Notion (Notion espeja el
   task_status via task_id); Notion NUNCA escribe estado gobernado. La NORMA (factory/protocol) y los ADR
   (decision_log) se LINKEAN, no se duplican/forkean en Notion.
2. **DIMENSION DE ESTUDIO (mi carril):** las Opciones/Tareas deben marcar cuales unidades estan RESERVADAS para
   MEDICION (las 6 pre-registradas: R2-c/R3-b/R4-b/R5-c/R0-fuentes/R4-c) con flag "no construir hasta sello", y un
   flag employee-run (Julian/jheredia) vs operador (jball) para atribucion. Sin esto, el equipo construye las
   reservadas a velocidad de producto y se pierde la medicion (no se mide retroactivo).
3. **La propuesta DBA esta BIEN FUNDADA:** sus DBs mapean a la estructura real del diccionario (Objetos-Legacy =
   ws1/formularios, Objetos-BD-NOVA = procs/vistas/triggers, ADR = decision_log, Artefactos = evidencias). Las dos
   maquinas de estado son correctas. Endoso con mis 2 adiciones (frontera + estudio).
4. **La DB Agentes debe reflejar el agent_registry gobernado** (jball/jheredia/Codex/Analista/Arquitecto con sus
   capabilities/llaves), no una lista libre -> asi el modelo Notion no contradice el ledger.

## Lo que pido de cada uno
- **Arquitecto:** frontera ledger<->Notion + arquitectura de 3 capas + modelo de entidades (ver requested_action).
- **Analista:** trazabilidad SDD->objeto->prueba->evidencia + integridad/no-stale del modelo + auditoria.
- **Codex (si aplica):** vista del maker (como una tarea Notion se relaciona con su submit_intent/handoff).

El operador construye el workspace con el consenso. Es control de proyecto -- fundamental.

-- Operador
