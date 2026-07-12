---
message_id: MSG-20260712-Arquitecto-to-Operador-RESP-consenso-notion-3firmantes
from: Arquitecto
to: Operador
type: FYI
status: archived
requires_response: false
created_at: 2026-07-12
context_refs:
  - Area_comun/mailbox/open/MSG-20260712-Operador-to-Arquitecto-ACTION-enfoque-workspace-notion-control-proyecto.md
  - Area_comun/mailbox/open/MSG-20260712-Arquitecto-to-Operador-RESP-enfoque-workspace-notion.md
  - Area_comun/artifacts/ANALISTA-OPS-enfoque-notion-qa-checker-veredicto.md
one_line_summary: "CONSENSO DE LOS 3 (Asesor + Arquitecto + Analista): CONVERGE. Notion = read-model AUDITADO del ledger #4, nunca fuente; ningun campo gobernado sin evento fuente (seq/actor/commit/hash). Secuencia recomendada: construir el workspace con las DBs marcadas mirror-vs-nativa, y ANTES de cablear el proyector ledger->Notion abrir una SPEC del proyector con los tests minimos (drift/auditoria/F-NOVA-01). Doy el modelo consolidado."
requested_action: ""
---

# RESP - Consenso de los 3 firmantes: workspace Notion (control de proyecto)

## 1. El consenso CONVERGE (los 3 coinciden en la regla dura)
- **Asesor:** frontera de gobernanza (Notion = planeacion/visibilidad; ledger = autoridad) + dimension de estudio
  (flags reserva/employee-run como mirror) + endoso de la propuesta DBA.
- **Arquitecto (yo):** Notion = read-model del #4; frontera por capa; sync UNA VIA ledger->Notion con `synced_seq`;
  modelo de entidades alineado a hub/Aegis/Notion (DECISION-0088/0093/0050); endoso DBA con la restriccion
  "state-machine de tarea = proyeccion, no fuente".
- **Analista (checker):** OK/CERRABLE como enfoque, con trazabilidad RELACIONAL obligatoria y auditoria por campo;
  NO cerrable como implementacion hasta que exista una SPEC/prototipo del proyector con tests minimos.

**Regla dura acordada por los 3:** Notion puede ser read-model operativo, pero **ningun campo gobernado tiene
autoridad si no esta derivado de un evento del ledger y trazado a su `seq`/actor/commit/hash**. Notion NUNCA es
fuente de tarea, decision, claim, evidencia gobernada, reserva de medicion, agent_registry ni estado de objeto
validado. Si Notion se vuelve fuente -> se rompe la atestacion #4 y el estudio queda auditablemente debil.

## 2. Modelo consolidado (lo que los 3 endosamos)
### 2a. Cadena relacional OBLIGATORIA (aporte central del Analista)
No campos sueltos: `Modulo/Opcion -> Spec-SDD -> Objeto-BD-NOVA -> Caso-de-Prueba -> Evidencia -> Evento-ledger`. La
cobertura F-NOVA-01 solo cuenta si la cadena es relacional y obligatoria (enlaces libres NO bastan).

### 2b. Campos de gobernanza por pagina espejada (mejora del `synced_seq`)
Cada pagina gobernada guarda: `source_event_seq`, `source_event_hash`, `source_aggregate_id`, `source_kind`,
`source_commit`, `actor_id`, `projector_version`, `projected_at`, `synced_seq`, y un campo calculado
`staleness` (`fresh`/`stale`/`orphan`/`conflict`/`unverified`). Cada relacion critica guarda la version fuente de sus
DOS extremos. Evidencia gobernada exige `command`+`exit_code`+`commit`+`task_id`+`ledger_seq_source`; sin ellos
degrada a nota `native_planning`, no `governed`.

### 2c. Separacion mirror vs nativa
Marcar EXPLICITAMENTE cada DB/campo: `governed` (mirror read-only del ledger) vs `notion_native=true` (planeacion:
vistas, kanban de migracion, comentarios, orden visual, etiquetas no gobernadas). Objetos-BD-NOVA: la definicion
autoritativa es `OBJECT_DEFINITION`/script versionado con hash; Notion NO redefine procs/vistas/triggers. DB Agentes
= mirror del agent_registry gobernado (capabilities/keyids), no lista libre.

### 2d. Sync + drift detector
Sync UNA VIA: un proyector idempotente lee eventos del ledger y hace UPSERT de las paginas; Notion nunca llama a
`submit_intent` para escribir estado gobernado (si el operador acciona desde Notion, el boton dispara un
`submit_intent` FIRMADO -> el ledger cambia y el proyector lo espeja de vuelta). Drift detector (solo-lectura contra
Notion): reproyecta ledger->tabla temp, lee Notion por API, compara por clave estable, y FALLA en 3 familias
(faltante en Notion / extra gobernado sin evento fuente / mismatch); auto-fix SOLO re-ejecutando el proyector, jamas
aceptando el valor de Notion como canonico.

## 3. Secuencia recomendada (los 3 la endosan)
1. **Construir el workspace** con la propuesta DBA + las 2 adiciones del Asesor (frontera + estudio) + las
   marcas mirror/nativa de arriba. La state-machine de TAREA es proyeccion del `task_status` del ledger; la de
   MIGRACION (EN_ESPERA..MIGRADO) puede ser mas nativa (tracking de diseno sin dientes).
2. **ANTES de cablear el proyector ledger->Notion**, abrir una **SPEC del proyector** (p.ej. SPEC-NOTION-PROJECTOR)
   con los tests minimos que el Analista fija: (a) proyector idempotente; (b) drift Notion-vs-ledger (missing/extra/
   mismatch); (c) test que IMPIDE promover estado gobernado desde Notion sin `submit_intent`; (d) cobertura
   F-NOVA-01 que falla si falta cualquier tramo SDD->objeto->prueba->evidencia; (e) auditoria que falla si un campo
   gobernado carece de `seq`/actor/commit/hash. Si das el GO, la escribo (patron NOVA-SPEC-T-001, como el kit
   SPEC-CONT).
3. **Vista maker (Codex):** pendiente -- Codex esta construyendo B (TASK-9303) ahora. La infiero: una tarea Notion
   de build ESPEJA el `task_status` que produce el `submit_intent`/handoff de Codex; el `task_id` es la clave de
   union. Cuando Codex quede libre, le pido su vista para cerrar el 4o angulo.

## 4. Anclas verificadas
Analista reviso en HEAD `6ba22cd` (su ancla), validate vivo 0 + clon limpio sin secrets 0, scan_domain_neutrality 0,
scan_encoding 0, drift 0 `up_to_seq=4572`, `protocol.config.json` byte-identico (sha256 2E35F26E...). Riesgo residual
que declara (no atribuible a esto): `npm test` raiz de Nova-Budget sale -4058 por ausencia de package.json en la
raiz -- no sirve como gate de cierre de producto (ya conocido).

## Resumen de una linea
Los 3 convergen: Notion = read-model AUDITADO del #4 (nunca fuente); cadena relacional obligatoria + campos de
gobernanza por pagina (seq/hash/actor/commit/staleness) + separacion mirror/nativa + drift detector read-only.
Construir con esos rieles; abrir la SPEC del proyector con tests ANTES de cablearlo. Dame el GO y escribo la SPEC.

-- Arquitecto (2026-07-12 17:58 local/UTC+2)
