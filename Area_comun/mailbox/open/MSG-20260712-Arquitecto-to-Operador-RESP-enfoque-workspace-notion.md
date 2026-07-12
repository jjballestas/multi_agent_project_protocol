---
message_id: MSG-20260712-Arquitecto-to-Operador-RESP-enfoque-workspace-notion
from: Arquitecto
to: Operador
type: FYI
status: open
requires_response: false
created_at: 2026-07-12
context_refs:
  - Area_comun/mailbox/open/MSG-20260712-Operador-to-Arquitecto-ACTION-enfoque-workspace-notion-control-proyecto.md
  - Area_comun/decisions/DECISION-0088-asiento-coordinacion-build-escalonado-hub-instancia.md
  - Area_comun/decisions/DECISION-0093-corte-gobernanza-hub-aegis-inmediato.md
  - Area_comun/decisions/DECISION-0050-convencion-repos-gobernanza-producto.md
one_line_summary: "Enfoque del Arquitecto para el workspace Notion: Notion = PROYECCION (read-model) del ledger atestado, NUNCA fuente de estado gobernado. Frontera dura por capa, sync estrictamente una-via ledger->Notion con proyector idempotente + synced_seq (staleness detectable). Endoso la propuesta DBA + el enfoque del Asesor CON la restriccion de frontera. Ruteo REQUEST al Analista. AVISO: crons de Codex y Analista OFF (heartbeat 2026-07-07) -> reactivar para sus enfoques y para que B avance."
requested_action: ""
---

# RESP - Enfoque del Arquitecto: workspace Notion como PROYECCION del ledger

## 0. Principio rector (una frase)
**Notion es una PROYECCION (read-model) del ledger atestado, NUNCA una fuente.** El #4 (hub + Aegis) es el
write-model event-sourced y firmado; Notion es una vista materializada de solo-lectura para planeacion humana. Es un
CQRS: si Notion puede escribir estado gobernado, tenemos DOS fuentes de verdad -> drift + perdida de atestacion +
hueco en el estudio (la medicion lee EVENTOS del ledger, no Notion). Toda mi arquitectura sale de aqui.

## 1. Frontera de gobernanza por capa (el punto duro que pides)
| Contenido | Autoridad | Notion |
|---|---|---|
| task_status / claims / decisiones / atestacion-firma / config-epoch / eventos de medicion (F3.3, Q1-Q5) | **LEDGER (#4), con dientes (submit_intent, enforce, cadena)** | **MIRROR read-only** (nunca escribe) |
| NORMA (factory/protocol): AGENTS.md, protocol docs, templates | git/hub (versionado) | **LINK canonico** (jamas copia -- copiar = forkear la norma) |
| ADR (decision_log): DECISION-* | hub `Area_comun/decisions/` | **MIRROR read-only** (id/titulo/status/supersede + link al .md gobernado) |
| design-source (55 dicc HTML, WS1/SDD): objetos legacy + objetos BD NOVA | D:/Agentes/Ingenas + la BD desplegada (OBJECT_DEFINITION) | **INDEX/tracker** (la definicion autoritativa es el objeto desplegado, no Notion) |
| PLANEACION/VISIBILIDAD: roadmap, kanban, agrupaciones, notas, rollups | **Notion (nativo)** | libre -- MIENTRAS no reclame ser estado gobernado |

Regla operativa: cada pagina Notion que espeja algo gobernado lleva (a) un badge "GOBERNADO / read-only", (b) el
`task_id`/`decision_id` de origen, (c) el `synced_seq` del evento que la genero. Los campos de planeacion nativos
(prioridad-nota, kanban-posicion, comentarios) viven aparte y NO se confunden con los gobernados.

## 2. Sync: estrictamente UNA VIA ledger -> Notion
- **Proyector** (script) que lee los eventos del ledger (`task_upsert`, `task_status`, `claim`, `decision`) por
  `task_id`/`decision_id` y hace UPSERT idempotente de las paginas Notion. Notion NUNCA llama a `submit_intent`.
- **Staleness detectable = anti-mentira:** el proyector sella cada pagina con el `seq` del evento fuente; si el
  `synced_seq` de una pagina < head del ledger para ese id, la pagina esta STALE -> la alarma la vigila el Analista
  (integridad del modelo). Sin este sello, Notion "miente en silencio" cuando el ledger avanza.
- **Bidireccional NO.** Si el operador quiere accionar desde Notion (p.ej. "promover tarea"), el boton dispara un
  `submit_intent` firmado por el actor humano/agente correspondiente -> el estado cambia EN EL LEDGER y el proyector
  lo espeja de vuelta. Notion nunca es el que "flipea" el status; solo lanza la intent gobernada.

## 3. Modelo de entidades desde la frontera DECISION-0088/0093/0050
- **HUB (hub permanente = el dataset):** gobernanza/coordinacion/atestacion -- DECISION/SPEC/tasks/handoffs/mailbox
  + submit_intent + el #4 atestado. Notion `Decisiones-ADR`, `Specs-SDD`, `Tareas (gobernanza)`, `Agentes` ESPEJAN
  el ledger del HUB.
- **AEGIS (y futuras instancias de producto, D:/Agentes/Zeus/...):** ledger PROPIO de la instancia (tareas de build
  gobernadas, atestacion propia, cross-atestada al hub por DECISION-0088/0093). Notion `Tareas (build)` ESPEJAN el
  ledger de la INSTANCIA, con etiqueta de instancia. El config-epoch/re-genesis (jheredia/jball) es gobernado por el
  ledger de Aegis; Notion solo muestra el mirror del agent_registry.
- **NOTION:** capa de planeacion/visibilidad/decision humana UNICAMENTE -- roadmap, kanban, rollups Tareas->Modulo,
  la vista de control del operador. JAMAS autoritativa de estado gobernado.
- Asi el modelo respeta el acoplamiento unidireccional (DECISION-0050): la gobernanza vive en el hub (constante), los
  productos rotan por instancia, y Notion es una capa de lectura transversal que NO invierte el acoplamiento.

## 4. Dimension de estudio (endoso el punto 2 del Asesor, con la restriccion de frontera)
Las Opciones/Tareas deben marcar las unidades RESERVADAS para MEDICION (las 6 pre-registradas) con flag
"no-construir-hasta-sello", y el flag employee-run (jheredia) vs operador (jball) para atribucion. **PERO** ese flag
debe ser un MIRROR de un marcador GOBERNADO (la reserva vive en el ledger/pre-registro), no un campo Notion libre --
si no, el ledger y Notion divergen sobre que esta reservado y el operador podria construir una reservada por error
(se pierde la medicion, no se mide retroactivo). Es exactamente el caso donde Notion-como-fuente rompe el estudio.

## 5. Reconciliacion con la propuesta DBA + el Asesor
- **Endoso la propuesta DBA:** sus DBs mapean a la estructura real del diccionario (Objetos-Legacy = ws1/
  formularios, Objetos-BD-NOVA = procs/vistas/triggers, ADR = decision_log, Artefactos = evidencias, Agentes). Las
  dos maquinas de estado (migracion + tarea) son correctas.
- **CON una restriccion dura:** la maquina de estado de TAREA en Notion debe ser una PROYECCION del `task_status`
  del ledger, NO una maquina independiente. Si Notion corre su propio ciclo Backlog..Hecho desacoplado del ledger,
  hay dos verdades del status de tarea. La state-machine de MIGRACION (EN_ESPERA..MIGRADO) puede ser mas nativa de
  Notion PORQUE la migracion legacy->NOVA no es estado gobernado con dientes (es tracking de diseno) -- pero cuando
  una migracion se vuelve una tarea de build gobernada, su status lo manda el ledger.
- **DB Agentes = mirror del agent_registry gobernado** (Codex/Analista/Arquitecto/jheredia/jball con capabilities/
  keyids), no lista libre (endoso el punto 4 del Asesor). Asi Notion no puede contradecir quien firma que.
- Marcar EXPLICITAMENTE en el modelo cuales DBs son MIRROR (Tareas-gobernanza, Tareas-build, Decisiones-ADR, Specs,
  Agentes) vs NATIVAS-de-planeacion (roadmap, kanban de migracion, notas). Esa etiqueta es la que hace legible la
  frontera para el equipo.

## 6. Coordinacion Analista + Codex
- Ruteo REQUEST al **Analista** (`MSG-Arquitecto-to-Analista-REQUEST-enfoque-notion`) por su carril: trazabilidad
  SDD->objeto->caso de prueba->evidencia en el modelo, integridad/no-stale (el sello `synced_seq` de s.2), y el
  requisito de auditoria (todo campo gobernado en Notion traza a un evento del ledger).
- **AVISO OPERACIONAL (anomalia, DECISION-0018):** los crons de **Codex y Analista estan OFF** (ultimo heartbeat
  2026-07-07, sin pid). Consecuencias: (a) el Analista NO producira su enfoque hasta que lo reactives; (b) **Codex
  no esta construyendo B (TASK-9303)** -- sigue `ready` sin claim, y B es el guardrail antes de la 1a unidad
  gobernada de Julian. Para el consenso de los 3 y para que B avance: reactiva ambos crons. Si prefieres, dame el GO
  y coordino la reactivacion segun DECISION-0057 (runtime-only).

## Resumen de una linea
Notion = read-model del #4 (nunca fuente); frontera por capa (gobernado=mirror read-only, norma=link, ADR=mirror,
design-source=index, planeacion=nativa); sync una-via ledger->Notion con `synced_seq` para cazar staleness; modelo
de entidades alineado a hub/Aegis/Notion (DECISION-0088/0093/0050); flags de estudio como mirror gobernado. Endoso
DBA+Asesor con la restriccion "la state-machine de tarea es proyeccion, no fuente".

-- Arquitecto (2026-07-12 17:40 local/UTC+2)
