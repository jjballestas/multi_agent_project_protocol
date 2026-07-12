---
message_id: MSG-20260713-Operador-to-Arquitecto-GO-build-proyector-notion
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-13
context_refs:
  - Area_comun/specs/SPEC-NOTION-PROJECTOR.md
one_line_summary: "GO para registrar + construir el PROYECTOR Notion como tarea gobernada contra SPEC-NOTION-PROJECTOR (Codex maker / Analista checker FORMAL, integridad ALTA). El workspace ya esta PROJECTOR-READY (esqueleto relacional F-NOVA-01 bidireccional + IDs canonicos + campos is_governed/synced_seq + Menus). AGENDAR con el build-open (post-30-jul): su contenido son las 6 unidades medidas, no debe competir con el SLA de Sprint 1."
requested_action: "Registra la tarea de superficie del proyector en el ledger de Aegis (task_upsert, owner Codex, contra SPEC-NOTION-PROJECTOR) y agendala para el build-open (post-30-jul). El proyector: job UNA-VIA que lee el ledger (#4 hub + Aegis) + el pre-registro y hace UPSERT idempotente de las paginas Notion, sellando la metadata de gobernanza (source_event_seq/hash/commit/actor/projector_version/synced_seq/staleness) que el Asesor NO puede llenar a mano. Checker = Analista FORMAL (contexto limpio, acceso RO al ledger + workspace de prueba). Gate = los 12 criterios de la SPEC + guard de procedencia (ledger real, no mocks) + atestacion sha256. NO urgente (metodologia tooling); su contenido real llega con las unidades medidas."
question: "Registras la tarea del proyector contra la SPEC y la agendas al build-open? El workspace ya esta projector-ready (IDs de bases abajo). Avisame el task_id para trazarlo en Notion."
---

# ACTION - GO: build del proyector Notion (tarea gobernada, agendada al build-open)

El workspace Notion esta **projector-ready**. Cierra el ciclo que acordaron los 3: construir el workspace con los
rieles -> abrir la SPEC del proyector -> cablear el proyector contra ella.

## Readiness ya HECHA por el Asesor (los rieles de s.5 + tu feedback Notion)
- **Cadena F-NOVA-01 RELACIONAL bidireccional**: Tareas <-> Specs-SDD <-> Objetos-BD <-> Casos-de-Prueba <->
  Artefactos <-> Modulos. Modulos es el hub (rollups por modulo listos). Menus (Modulo->Menu->Opcion) creada.
- **IDs canonicos**: module_code / option_id / spec_code(=Codigo) / object_id / test_id / evidence_id /
  legacy_object_id / task_id. Los titulos ya pueden cambiar sin romper trazabilidad.
- **Objetos-BD** enriquecido: schema, object_name, database_scope (DbsFinanciero/SANDBOX/SNJDC), definition_hash,
  sealed_by. **Legacy -> Reemplazo (Objeto NOVA)** relacion.
- **is_governed + synced_seq** en las bases gobernadas; **notion_native** en Menus. Separacion governed vs native lista.

## Lo que el PROYECTOR construye (no el Asesor)
El bloque completo de metadata de gobernanza por pagina (source_event_seq, source_event_hash, source_commit,
actor_id, projector_version, projected_at, synced_seq, staleness) + el UPSERT idempotente + el detector de drift
(3 familias) + los flags de estudio proyectados del pre-registro (Reservada-para-medicion + Ejecutor) + las
Unidades-Medidas del workspace Metodologia. Todo per SPEC-NOTION-PROJECTOR (integridad ALTA).

## IDs de las bases (data_source) para el proyector
- NOVA: Modulos 0bde3f40-9d21-43b0-85d6-beed1b9b0639 | Opciones 726af307-268a-418a-b64e-bd7cedfbf7bf |
  Tareas 1136f0e9-c602-4b7e-a567-3ae68a5478cd | Specs-SDD 5da4b995-bd1b-4f15-95e6-410ac66ec66b |
  Objetos-BD d47a6d59-aa34-4975-8ff6-51217ae41f15 | Objetos-Legacy ce62302d-16c4-4995-b496-c61458866c1b |
  Casos-de-Prueba c98895f0-79fa-45f2-970e-97b6265573e0 | Artefactos f04efbd7-bfcb-480a-a821-32ea82024c77 |
  Menus 7066a581-c23f-4a08-8b76-e4b84c954ed2 | Decisiones-dominio 7cc07873-bccc-4e71-8130-c94a414e3264
- METODOLOGIA: Agentes ebf10ec9-66fa-486d-b142-a81e8576de63 | Unidades-Medidas 8c90a1cb-0edf-4a75-8edc-6a3c97903bf9 |
  Decisiones-metodologia 95591ba1-4657-40af-a84b-f09ef3ded623 | TFM b4d55896-9bdd-41b9-b8b9-02294e7f459d |
  Norma d8f270ec-1451-4ec6-afbe-90b21e7e64be
- Token de API de Notion: en store seguro (no commiteado), lo provee el operador al job (SPEC 6j).

## Timing (importante)
Es tooling de metodologia; su CONTENIDO real son las 6 unidades medidas (que aun no existen). **Agendalo con el
build-open post-30-jul**; NO debe competir con el SLA duro de Sprint 1. Puede registrarse ya como tarea (ready/
backlog) y construirse cuando abra la ventana. El Asesor mantiene el workspace projector-ready mientras tanto.

-- Operador
