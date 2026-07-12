# SPEC-NOTION-PROJECTOR - Proyector una-via ledger -> Notion (control de proyecto)

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Contrato del PROYECTOR que materializa el
> workspace Notion de control de proyecto como read-model AUDITADO del ledger atestado (#4 hub + Aegis). Nace del
> consenso de los 3 firmantes (Asesor + Arquitecto + Analista) sobre la ACTION del operador (enfoque + GO
> workspace-notion). PREP/diseno: se ESCRIBE antes de cablear el proyector; el workspace lo construye el operador con
> su agente Notion, y luego se cablea el proyector contra esta SPEC. Regla rectora INNEGOCIABLE: **Notion es una
> PROYECCION; el ledger es la unica AUTORIDAD del estado gobernado.** Fuente: consenso Notion (RESP-consenso-notion-
> 3firmantes + veredicto QA del Analista) + refinamiento del operador (2 workspaces + dimension de estudio).

## Preambulo de gobierno (DoR)
- spec_id: SPEC-NOTION-PROJECTOR - task_id (instancia): asignado al registrar la tarea de superficie cuando se
  cablee el proyector (post-construccion del workspace por el operador).
- owner_maker: agente desarrollador de la instancia gobernada (repo de tooling de metodologia).
- checker: **Analista (adversarial FORMAL, contexto limpio: SPEC + diff + acceso de solo-lectura al ledger y a un
  workspace Notion de prueba, NO la conversacion del maker)** + adversarial informal en sesion separada.
- arm / q4_membership / isolation: N/A al estudio de producto; es tooling de metodologia. Criticidad de INTEGRIDAD
  **ALTA** (si el proyector deja escribir estado gobernado desde Notion o deja campos gobernados sin evento fuente,
  se rompe la atestacion #4 y el estudio queda auditablemente debil).
- **base de referencia:** el ledger atestado del hub (#4, epoch 1.14.0, config sha256 2E35F26E...) + el ledger de
  Aegis (cross-atestado, DECISION-0088/0093). El proyector LEE eventos; NO los escribe.
- **precondicion / preflight:** existe el workspace Notion (2 workspaces, construido por el operador + agente Notion)
  con las bases y campos de gobernanza de s.5; existe un token de API de Notion en un store seguro (no commiteado);
  el ledger expone sus eventos (`runtime/eventlog.all_events` / equivalente) y el pre-registro
  (`personal/asesor/DRAFT-PREREGISTRO-contabilidad-employee-run.md` s.3) es legible.
- **guard de procedencia:** los tests del proyector corren contra el LEDGER REAL (eventos + hashes) y un workspace
  Notion de prueba (o un fake tipado de la API de Notion); NINGUN mock in-memory sustituye la lectura del ledger ni
  la comparacion de drift.
- **diseno de autorizacion:** el proyector corre como job server-side con credenciales propias (token Notion +
  lectura del ledger); cualquier MUTACION de estado gobierno-relevante disparada desde Notion pasa por
  `submit_intent` FIRMADO por el actor correspondiente -> el proyector nunca escribe estado gobernado en el ledger
  ni acepta el valor de Notion como canonico.
- **measurement:** N/A directo; el proyector ES parte de la instrumentacion (materializa "Unidades Medidas").
- attestation: sha256 de esta SPEC via intent del hub en el gate correspondiente.
- stack (obligatorio): mismo stack gobernado (ASP.NET Core .NET en capas / gateways tipados / OpenTelemetry /
  ProblemDetails) o un job equivalente tipado; la API de Notion se consume por un gateway tipado (no llamadas
  crudas dispersas). Anti-patrones PROHIBIDOS: secretos en `.config`, escritura directa a Notion de campos
  gobernados sin metadata de gobernanza, aceptar Notion como fuente.

## 1. Objetivo definido
Un **proyector UNA VIA** que lee el ledger atestado (hub #4 + Aegis) y el pre-registro, y materializa DOS workspaces
Notion como read-models AUDITADOS: **NOVA** (producto) y **Metodologia** (estudio/gobernanza/norma). Cada pagina
gobernada lleva metadata de gobernanza (seq/hash/actor/commit/projector_version/staleness) que la ata a su evento
fuente; los dos workspaces se unen por `task_id` (clave universal), NO por relaciones cross-workspace de Notion. El
objetivo humano son las VISTAS (kanban "mis tareas" + dashboards de progreso), sobre un backbone de gobernanza que va
debajo, callado. Notion NUNCA es autoridad del estado gobernado.
- Fuente: consenso Notion de los 3 + refinamiento del operador (2 workspaces + dimension de estudio).
- Calidad: falsable. Bien: "cambiar `task_status` a mano en una pagina Notion NO altera el ledger, y la siguiente
  corrida del proyector RE-ESPEJA el valor canonico del ledger (Notion nunca gana); y una pagina gobernada sin
  `source_event_seq`/actor/commit/hash se degrada a `native_planning`, no cuenta como gobernada".

## 2. Usuario objetivo definido
- **Operador + equipo (humanos):** consumen las vistas de planeacion/visibilidad (kanban "mis tareas" por persona/
  estado, dashboards de progreso por modulo). No editan estado gobernado desde Notion.
- **El proyector (job server-side):** actor no-humano que corre agendado o por trigger; lee el ledger + pre-registro
  y hace UPSERT idempotente de las paginas.
- **El operador (via boton gobernado):** si acciona una promocion desde Notion, el boton dispara un `submit_intent`
  FIRMADO -> el estado cambia en el LEDGER y el proyector lo espeja de vuelta.

## 3. Alcance definido
- **Proyeccion una-via:** lee eventos del ledger (`task_upsert`, `task_status`, `claim`, `decision`) por
  `task_id`/`decision_id`/`spec_id`/`object_id`/`test_id`/`evidence_id` y hace UPSERT idempotente de las paginas
  Notion; sella cada pagina gobernada con `source_event_seq`, `source_event_hash`, `source_aggregate_id`,
  `source_kind`, `source_commit`, `actor_id`, `projector_version`, `projected_at`, `synced_seq` y un campo calculado
  `staleness` (`fresh`/`stale`/`orphan`/`conflict`/`unverified`).
- **DOS workspaces desde el MISMO ledger, unidos por `task_id`:**
  - **NOVA (producto):** Modulos / Menus / Opciones / Tareas / Specs-SDD / Objetos-Legacy / Objetos-BD-NOVA /
    Casos-de-Prueba / Evidencias.
  - **Metodologia (estudio/gobernanza):** Unidades-Medidas / Agentes / Decisiones-pendientes / links a la norma
    (factory/protocol) y a los ADR (decision_log).
  El puente entre workspaces es `task_id` (no una relacion cross-workspace de Notion, fragil); cada workspace espeja
  su parte y ninguno es autoridad.
- **Cadena relacional OBLIGATORIA (cobertura F-NOVA-01):** `Modulo/Opcion -> Spec-SDD -> Objeto-BD-NOVA ->
  Caso-de-Prueba -> Evidencia -> Evento-ledger`, con los campos minimos por entidad (s.5). Cada relacion critica
  guarda la version fuente de sus DOS extremos.
- **Dimension de estudio (carril Asesor):** el proyector LEE el pre-registro (DRAFT-PREREGISTRO s.3, muestra N=6) y
  setea en la tarea NOVA el flag `Reservada-para-medicion` + `Ejecutor` (empleado `jheredia` / operador `jball` /
  agente), y materializa el registro `Unidades-Medidas` en el workspace Metodologia (mismo `task_id`). Una unidad
  reservada queda marcada `no-construir-hasta-sello`.
- **Vistas humanas (el proposito visible):** kanban "mis tareas" por persona/estado + dashboards de progreso por
  modulo (rollups Tareas->Modulo), sobre el backbone de gobernanza.
- **Notion -> ledger (unica via de mutacion gobernada):** un boton en Notion dispara un `submit_intent` FIRMADO por
  el actor -> el ledger cambia -> el proyector espeja de vuelta. El proyector NUNCA escribe estado gobernado en el
  ledger ni acepta el valor de Notion.
- **Detector de drift (solo-lectura contra Notion):** reproyecta el ledger a una tabla temporal, lee Notion por API,
  compara por clave estable, y FALLA en 3 familias (faltante en Notion / extra gobernado sin evento fuente /
  mismatch de campo gobernado); auto-fix SOLO re-ejecutando el proyector, jamas aceptando Notion como canonico.
- **Separacion mirror vs nativa:** campos/DBs `governed` (mirror read-only) vs `notion_native=true` (planeacion:
  vistas, kanban de migracion, comentarios, orden visual, etiquetas no gobernadas).

## 4. Fuera de alcance definido
- **Notion como FUENTE de estado gobernado:** tareas/claims/decisiones/atestacion/reservas de medicion/
  agent_registry/estado de objeto validado NUNCA se originan ni tienen autoridad en Notion.
- **Decisiones-como-registro en Notion:** los ADR/DECISION-00xx NO van a Notion (link al decision_log). Solo entran
  como Notion: decisiones PENDIENTES (tareas tipo "Decision") + el link al ADR que gobierna una tarea.
- **Relacion cross-workspace de Notion como puente:** se usa `task_id`, no relaciones nativas fragiles entre
  workspaces.
- **Construir el workspace Notion (bases/campos/vistas):** lo hace el operador con su agente Notion; esta SPEC es el
  PROYECTOR que lo alimenta contra los campos de s.5.
- **Redefinir procs/vistas/triggers o la norma:** la definicion autoritativa de un Objeto-BD-NOVA es su
  `OBJECT_DEFINITION`/script versionado (Notion solo indexa con `definition_hash`); la norma factory/protocol se
  LINKEA, no se copia.
- **La capa HMAC/`event_auth`:** su verificacion es un gate separado con secretos, no parte del proyector.

## 5. Contenido / assets definidos
- **Campos de gobernanza por pagina (obligatorios en toda pagina `governed`):** `source_event_seq`,
  `source_event_hash`, `source_aggregate_id`, `source_kind`, `source_commit`, `actor_id`, `projector_version`,
  `projected_at`, `synced_seq`, `staleness`, `is_governed=true`.
- **Entidades minimas (campos clave):**
  - `Spec-SDD`: `spec_id`, `repo_path`, `commit`, `decision_id`, `ledger_seq_source`, `synced_seq`, `is_governed`.
  - `Objeto-BD-NOVA`: `object_id`, `schema`, `object_name`, `object_type`, `definition_hash`, `definition_source`
    (`OBJECT_DEFINITION`/script versionado), `spec_id`, `ledger_seq_source`, `synced_seq`.
  - `Caso-de-Prueba`: `test_id`, `scope`, `vector`, `expected_result`, `test_command`, `test_commit`,
    `covers_spec_id`, `covers_object_id`, `ledger_seq_source`, `synced_seq`.
  - `Evidencia`: `evidence_id`, `artifact_path`, `command`, `exit_code`, `run_at`, `commit`, `test_id`, `task_id`,
    `ledger_seq_source`, `synced_seq`. (Sin `exit_code`+`commit`+`task_id`+`ledger_seq_source` -> degrada a
    `native_planning`.)
  - `Tarea`: `task_id`, `status` (mirror del ledger), `owner`, `Reservada-para-medicion`, `Ejecutor`, `adr_link`.
  - `Agentes`: mirror del `agent_registry` gobernado (`id`, `capabilities`, `keyids`), NO lista libre.
  - `Unidades-Medidas` (workspace Metodologia): `task_id`, `arm`/`reserva`, `Ejecutor`, `pre_registro_ref`.
- **Proyector:** gateway tipado a la API de Notion; lector del ledger (eventos + hashes); lector del pre-registro;
  logica de UPSERT idempotente + sellado de metadata; detector de drift; job agendado/trigger.
- **Referencias:** consenso Notion (RESP-consenso-notion-3firmantes), veredicto QA del Analista
  (ANALISTA-OPS-enfoque-notion-qa-checker-veredicto), pre-registro (DRAFT-PREREGISTRO s.3), patron NOVA-SPEC-T-001.

## 6. Restricciones tecnicas definidas
- Heredadas: stack gobernado + neutralidad del nucleo (el MECANISMO del proyector es domain-neutral; NOVA/Metodologia
  son la aplicacion concreta de esta instancia).
- Propias:
  - (a) **UNA VIA:** el proyector lee el ledger y ESCRIBE Notion; NUNCA escribe estado gobernado en el ledger ni lee
    Notion como fuente de verdad de un campo gobernado.
  - (b) **METADATA DE GOBERNANZA OBLIGATORIA:** toda pagina gobernada lleva los campos de s.5 + `staleness`; sin
    ellos, degrada a `native_planning`.
  - (c) **MUTACION GOBERNADA SOLO VIA submit_intent FIRMADO:** boton Notion -> `submit_intent` firmado -> ledger ->
    espejo de vuelta. No hay ruta de escritura directa de Notion a estado gobernado.
  - (d) **CADENA RELACIONAL OBLIGATORIA:** la cobertura F-NOVA-01 solo cuenta si la cadena SDD->objeto->prueba->
    evidencia->evento es relacional y completa; enlaces libres no cuentan.
  - (e) **DRIFT DETECTOR READ-ONLY:** compara ledger-reproyectado vs Notion; auto-fix SOLO re-proyectando; jamas
    acepta el valor de Notion como reparacion canonica.
  - (f) **DOS WORKSPACES VIA task_id:** ambos se proyectan del mismo ledger; el puente es `task_id`, no una relacion
    cross-workspace de Notion.
  - (g) **FLAGS DE ESTUDIO PROYECTADOS DEL PRE-REGISTRO:** `Reservada-para-medicion` + `Ejecutor` los setea el
    proyector leyendo el pre-registro; NO son campos Notion libres (si no, el equipo construiria una reservada y se
    perderia la medicion).
  - (h) **AUDITORIA POR CAMPO GOBERNADO:** cada campo gobernado traza a `seq`/actor/commit/hash; sin ellos, degrada.
  - (i) **SEPARACION governed vs notion_native:** los campos nativos de planeacion llevan `notion_native=true` y no
    contaminan el plano gobernado.
  - (j) **SECRETOS:** el token de API de Notion vive en un store seguro (no commiteado); el proyector corre NA-limpio.
  - (k) **PAGINA BORRADA A MANO:** politica = recrear desde el ledger + reportar incidente; NUNCA aceptar el borrado
    como verdad.

## 7. Criterios de aceptacion definidos (Given/When/Then)
1. **(a) idempotencia** -- **Dado** el proyector corrido dos veces sobre el mismo estado del ledger, **entonces**
   Notion queda identico (no duplica paginas, no re-crea, no cambia campos gobernados).
2. **(c/6c) no-promocion-desde-Notion** -- **Dado** un cambio manual de `task_status` en una pagina Notion, **cuando**
   corre el proyector, **entonces** el valor canonico del ledger RE-ESPEJA (Notion no gana) y el ledger NO cambio; la
   unica via de promocion es un `submit_intent` FIRMADO disparado por el boton gobernado.
3. **(b) drift detector** -- **Dado** un workspace con (i) una pagina gobernada faltante, (ii) una pagina gobernada
   extra sin evento fuente, y (iii) un campo gobernado mutado, **entonces** el detector FALLA en las 3 familias con
   reporte falsable (`notion_page_id`, campo, valor esperado-desde-ledger, valor observado, `source_event_seq`,
   `synced_seq`); auto-fix SOLO re-proyectando.
4. **(d) cobertura F-NOVA-01** -- **Dado** una cadena `Modulo/Opcion->Spec-SDD->Objeto-BD-NOVA->Caso-de-Prueba->
   Evidencia->Evento-ledger` con un tramo faltante, **entonces** la validacion de cobertura FALLA (enlaces libres no
   cuentan).
5. **(e/h) auditoria por campo** -- **Dado** una pagina gobernada sin `source_event_seq`/`actor_id`/`source_commit`/
   `source_event_hash`, **entonces** el gate de auditoria FALLA (o la pagina degrada a `native_planning`, nunca
   `governed`).
6. **(f) dos workspaces via task_id** -- **Dado** NOVA y Metodologia proyectados del mismo ledger, **cuando** una
   tarea existe en ambos, **entonces** se unen por `task_id` (misma clave) y son consistentes; el test NO usa
   relaciones cross-workspace de Notion como puente.
7. **(g) dimension de estudio** -- **Dado** el pre-registro con 6 unidades reservadas, **cuando** corre el proyector,
   **entonces** setea `Reservada-para-medicion` + `Ejecutor` en las tareas NOVA correspondientes y materializa
   `Unidades-Medidas` en Metodologia (mismo `task_id`); una unidad reservada queda `no-construir-hasta-sello`.
8. **staleness** -- **Dado** una pagina cuyo `synced_seq` < head del ledger para su id, **entonces** su `staleness`
   se calcula `stale` (y `orphan`/`conflict`/`unverified` en sus casos).
9. **vistas humanas** -- **Dado** el backbone gobernado proyectado, **entonces** el kanban "mis tareas" (por persona/
   estado) y el dashboard de progreso por modulo renderizan desde ese backbone (rollups Tareas->Modulo).
10. **Agentes mirror** -- **Dado** el `agent_registry` gobernado, **entonces** la base Agentes lo espeja (capabilities/
    keyids); un intento de lista libre que contradiga el registry es drift detectado.
11. **secretos** -- **Dado** el proyector, **entonces** el token Notion viene de un store seguro (no commiteado) y el
    job corre NA-limpio.
12. **pagina borrada** -- **Dado** una pagina gobernada borrada a mano en Notion, **cuando** corre el proyector,
    **entonces** la RECREA desde el ledger y reporta el incidente; no acepta el borrado como verdad.

## 8. Pruebas / gates definidos
- **Unit:** UPSERT idempotente; sellado de metadata; calculo de `staleness`; degradacion governed->native por
  campos faltantes; enforcement de que ningun campo gobernado se escribe desde Notion.
- **Integracion (vs workspace Notion de prueba o fake tipado de la API):** los 5 tests minimos del consenso
  (a idempotente, b drift 3-familias, c no-promocion-sin-submit_intent, d cobertura F-NOVA-01, e auditoria por
  campo) + f (2 workspaces via task_id) + g (dimension de estudio desde el pre-registro).
- **Guard de procedencia:** los tests corren contra el LEDGER REAL (eventos + hashes) + Notion de prueba; ningun
  mock in-memory sustituye la lectura del ledger ni la comparacion de drift.
- **Gate final:** APROBADO del checker FORMAL del Analista (contexto limpio) + adversarial informal en sesion
  separada + los 12 criterios + guard de procedencia + neutralidad del mecanismo + `scan_encoding` del artefacto +
  atestacion sha256.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Notion se vuelve fuente de estado gobernado | Se rompe la atestacion #4; estudio auditablemente debil | Restricciones 6a/6c + criterios 2/6; una-via + mutacion solo via submit_intent firmado |
| Campo gobernado sin evento fuente (stale/mentiroso) | Notion "miente en silencio" cuando el ledger avanza | Restricciones 6b/6h + criterios 5/8; metadata obligatoria + staleness calculado + drift detector |
| Puente cross-workspace de Notion (fragil) en vez de task_id | Inconsistencia entre workspaces; ruptura silenciosa | Restriccion 6f + criterio 6; task_id como clave universal |
| Flags de estudio como campos Notion libres | El equipo construye una reservada -> se pierde la medicion (no retroactiva) | Restriccion 6g + criterio 7; proyectados del pre-registro |
| Drift detector que auto-acepta Notion | Reparacion canonica invertida | Restriccion 6e + criterio 3; auto-fix solo re-proyectando |
| Cobertura F-NOVA-01 con enlaces libres | Cobertura falsa (parece completa y no lo es) | Restriccion 6d + criterio 4; cadena relacional obligatoria |
| Secreto (token Notion) commiteado | Fuga de credencial | Restriccion 6j + criterio 11; store seguro, NA-limpio |
| Pagina borrada aceptada como verdad | Perdida silenciosa de estado proyectado | Restriccion 6k + criterio 12; recrear + reportar incidente |

## 10. Prioridad definida
**GOAL control de proyecto** (fundamental para el operador: "necesitamos ver que nos toca y como avanza"). Es tooling
de metodologia que hace VISIBLE el backbone de gobernanza sin volverse su autoridad. Dependencias: el ledger atestado
(#4 hub + Aegis), el pre-registro (dimension de estudio), el workspace Notion (lo construye el operador + agente
Notion), el patron congelado NOVA-SPEC-T-001. **Frontera: esta SPEC es DISENO/PREP; se cablea el proyector cuando el
workspace este construido.** Desbloquea: las vistas humanas de planeacion/visibilidad sobre un modelo que NO puede
contradecir ni forkear lo gobernado. Secuencia acordada por los 3: construir el workspace con estos rieles -> abrir
esta SPEC del proyector con los tests minimos -> cablear el proyector contra ella.
