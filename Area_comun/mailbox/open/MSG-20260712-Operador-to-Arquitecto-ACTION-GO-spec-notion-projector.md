---
message_id: MSG-20260712-Operador-to-Arquitecto-ACTION-GO-spec-notion-projector
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-12
context_refs:
  - Area_comun/mailbox/open/MSG-20260712-Arquitecto-to-Operador-RESP-consenso-notion-3firmantes.md
one_line_summary: "GO a escribir SPEC-NOTION-PROJECTOR (patron NOVA-SPEC-T-001) con los tests minimos del consenso de los 3, ANTES de cablear el proyector ledger->Notion. Refinamiento del operador: DOS workspaces (NOVA producto + Metodologia), unidos NO por relacion cross-workspace sino por el ledger + task_id; y la dimension de estudio (flags reserva/employee-run) la setea el proyector desde el pre-registro."
requested_action: "Escribe la SPEC-NOTION-PROJECTOR (patron NOVA-SPEC-T-001, como el kit SPEC-CONT) con los tests minimos que fijo el consenso: (a) proyector idempotente; (b) drift Notion-vs-ledger (missing/extra/mismatch, solo-lectura, auto-fix solo re-proyectando); (c) test que IMPIDE promover estado gobernado desde Notion sin submit_intent firmado; (d) cobertura F-NOVA-01 que falla si falta cualquier tramo de la cadena relacional Modulo/Opcion->Spec-SDD->Objeto-BD-NOVA->Caso-de-Prueba->Evidencia->Evento-ledger; (e) auditoria que falla si un campo gobernado carece de seq/actor/commit/hash. AGREGA del refinamiento del operador: (f) DOS workspaces (NOVA + Metodologia) proyectados AMBOS desde el ledger, unidos por task_id (no por relacion cross-workspace de Notion); (g) el proyector setea el flag Reservada-para-medicion + Ejecutor(empleado/operador/agente) leyendo el pre-registro (DRAFT-PREREGISTRO s.3) -> materializa el registro 'Unidades Medidas' en el workspace Metodologia. Optimiza las vistas HUMANAS (kanban 'mis tareas' + progreso) sobre el backbone de gobernanza."
question: "Confirmas GO a la SPEC-NOTION-PROJECTOR con los tests (a-e del consenso) + las adiciones (f) dos-workspaces-via-ledger y (g) proyeccion de la reserva de medicion? Cuando este, el operador (con su agente Notion) construye el workspace y luego se cablea el proyector."
---

# ACTION - GO: SPEC-NOTION-PROJECTOR (tests antes de cablear) + 2 workspaces + dimension estudio

Consenso de los 3 recibido y endosado. GO a escribir la SPEC del proyector ANTES de cablearlo, como fijaste.

## Tests minimos (del consenso -- incluir tal cual)
(a) proyector idempotente; (b) drift Notion-vs-ledger read-only (missing / extra-sin-evento / mismatch), auto-fix
SOLO re-proyectando, jamas aceptando Notion como canonico; (c) test que impide promover estado gobernado desde
Notion sin `submit_intent` firmado (boton Notion -> submit_intent firmado -> ledger -> proyector espeja de vuelta);
(d) cobertura F-NOVA-01 que falla si falta un tramo de la cadena relacional obligatoria
`Modulo/Opcion -> Spec-SDD -> Objeto-BD-NOVA -> Caso-de-Prueba -> Evidencia -> Evento-ledger`; (e) auditoria por
campo gobernado (falla si falta seq/actor/commit/hash/staleness).

## Adiciones del refinamiento del operador
- **(f) DOS workspaces:** NOVA (producto) + Metodologia (estudio/norma/gobernanza). Se proyectan AMBOS desde el
  MISMO ledger; el puente NO es una relacion cross-workspace de Notion (fragil) sino el **task_id** como clave
  universal. Cada workspace espeja su parte; ninguno es autoridad.
- **(g) Dimension de estudio (carril Asesor):** el proyector lee el pre-registro (`personal/asesor/
  DRAFT-PREREGISTRO-contabilidad-employee-run.md` s.3, muestra N=6) y setea en la tarea NOVA el flag
  `Reservada-para-medicion` + `Ejecutor` (empleado jheredia / operador jball / agente), y materializa el registro
  `Unidades Medidas` en el workspace Metodologia (mismo task_id). Sin esto, el equipo construye las 6 reservadas a
  velocidad de producto y se pierde la medicion (no se mide retroactivo).
- **Prioriza las vistas HUMANAS** (kanban "mis tareas" por persona/estado + dashboards de progreso por modulo)
  sobre el backbone de gobernanza -- ese backbone va debajo, callado; la capa visible es el proposito (el operador:
  "necesitamos ver que nos toca y como avanza").

## Decisiones en Notion (aclaracion del operador, para la SPEC)
Las decisiones-como-registro (ADR / DECISION-00xx) NO van a Notion (link a decision_log). Notion trackea
trabajo: tareas/actividades/requerimientos + seguimiento. Solo dos cosas decision-relacionadas entran: decisiones
PENDIENTES (como tareas tipo "Decision") + link al ADR que gobierna una tarea.

-- Operador
