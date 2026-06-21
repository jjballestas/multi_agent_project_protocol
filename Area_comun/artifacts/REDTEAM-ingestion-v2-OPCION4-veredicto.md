# RED-TEAM adversarial - Carga por archivo v2 (OPCION 4) - DECISION-0056 + SPEC-0086 ext10

> Revision adversarial multi-agente (5 lentes: no-egress / PII-frontera / #4-determinismo / gobernanza-ciclo /
> completitud) sobre los DRAFTS, ANTES de promover. 38/40 hallazgos confirmados contra codigo real
> (Zeus src/server.js, runtime/submit_intent.py, validate_collaboration_state.py, .gitignore).
> **VEREDICTO: FLAG-OPERADOR-ANTES** (no promover tal cual; 2 decisiones son del operador; el resto se pliega
> como edits en la misma promocion). El MECANISMO OPCION 4 es solido: #4 y escritor-unico NO se rompen.

## 2 DECISIONES DEL OPERADOR (cambian condiciones de cierre; antes de promover)

### D-PII (B2/B3/B4) - "ningun LLM ve PII de terceros" es ESTRUCTURALMENTE INALCANZABLE con screening por patrones
- El PII-gate es la allowlist de ~4 patrones (NIT/razon-social/SQL/schema) de `redactPublicText`. NO detecta
  nombres/emails/telefonos/cedulas/direcciones -- justo el PII de un archivo de historias de usuario. El AGENTE
  LLM lee el archivo (raw o saneado, sin definir) -> si el patron falla, el LLM VE PII. Y al APROBAR, el texto
  re-pasa por el MISMO redact de 4 patrones y el `narrative` se atesta en #4 (IRREVERSIBLE).
- **Decision del operador:** (a) GATE HUMANO DURO -- el operador revisa/edita el texto ANTES de que cualquier LLM
  lo lea (la extraccion deja de ser "subir->LLM"); o (b) aceptar una VENTANA DE RIESGO de PII gobernada, con
  DEF-PII/TASK-0118 como PREREQUISITO DURO (hoy diferido) antes de uso vivo; o (c) ampliar el screening a un
  detector real (email/tel/doc-id/nombres) y declarar honestamente "best-effort, no garantizado".

### D-ACTOR (M5) - el actor del evento de upload no esta fijado; el patron actual forjaria "Arquitecto"
- Fijar el actor REAL del upload del Operador exige un service-actor o `Operador` en `agent_registry`; bajo #4
  epoch-pinning eso colisiona con "registry/keys sin cambio" -> toca re-genesis-boundary.
- **Decision del operador:** (a) relay-como-Arquitecto con atribucion HONESTA (author=Operador/relayed_by=Arquitecto,
  como el intake actual; sin tocar registry); o (b) declarar service-actor/Operador en registry = ceremonia
  re-genesis-boundary gobernada.

## BLOCKERS (se resuelven con edits en la misma promocion)
- **B1 ruta de uploads:** `Area_comun/intake/uploads/` NO esta gitignored y vive DENTRO del dataset; un `git add -A`
  o el git-status del indicador canonico capturaria el raw con PII. FIX: mover uploads FUERA del repo protocolo
  (tmp del SO o repo Zeus, patron temp_paths) o entregar la linea .gitignore + AC falsable `git ls-files`=vacio +
  excluir del git-status del indicador.
- **B5 estado `candidate`:** no existe en VALID_TASK_STATUSES; `task_upsert` lo materializaria en TASK_INDEX
  (atestado) -> contradice "fuera del backlog". FIX: candidatas en STORE NO-ledger (intake/candidates/<id>/
  gitignored fuera del dataset, igual que uploads), ciclo de vida propio que NO es task_status; solo al aprobar
  nace el REQ via el intake existente; el ledger nunca ve `candidate`.
- **B6 cardinalidad:** aprobar N candidatas del MISMO archivo colisiona id/idempotency (derivado del fingerprint
  del archivo) -> la 2a sobrescribe a la 1a. FIX: el id/idempotency de la candidata aprobada deriva del CONTENIDO
  EDITADO (title+narrative+intent+project), no del archivo; fingerprint solo como metadato de procedencia.

## MAJORS (edits clave)
- M1 "no-egress" mezcla no-LLM con el git-push gobernado YA existente -> AC falso/no-falsable. Reescribir como
  "el server no llama a ningun endpoint de MODELO/inferencia" (no "cero egress"); separar del git-push gobernado.
- M2 el egress se reubica al AGENTE extractor (contenido externo crudo a un modelo posiblemente hospedado).
  Acotar la frontera del agente extractor (runtime local/on-prem declarado) o consentimiento/etiquetado por upload.
- M4 hash atestado es FNV-32 sobre texto saneado, no SHA-256 sobre bytes crudos (falsa-identidad). Usar SHA-256.
- M8 retencion/purga del raw es TODO, no AC. Ciclo de vida determinista server-side (purga al estado terminal +
  TTL para huerfanos) + test clon-limpio.
- M9/M11/M12 estados de la extraccion: 0-candidatos/basura/cap, "sin agente en el loop" (caso NORMAL single-op),
  fallas (failed + timeout del claim + validacion de forma del candidato al producirse).
- M13/M14 corte de fases: la rama "por carga de archivo" (AC42) queda VACIA hasta C -> gatearla detras de B+C, o
  consumidor minimo no-LLM; y el CONTRATO de la extraction-task debe estar en Fase A (handoff autocontenido).
- M3 prueba negativa no-egress: pinear aserciones estaticas (anti-import de SDK de modelo) + control positivo.

## MINORS (hardening)
m1 errores/logs no ecoan contenido crudo; m2 panel sin SDK/fetch de modelo en el browser; m3 nombre de archivo
atestado redactado/id opaco salado; m4 test edicion->aprobar re-screen; m6 prueba negativa 2a-superficie
(solo escribe bajo uploads/<id>, no toca state/working-tree); m7 vector LLM-parafrasea-PII en threat-model +
reservar pasada del Analista para LLM->intake; m8 gate del validador rechaza status fuera de enum (hace falsable
"candidate no entra al backlog"); m9 trazabilidad de procedencia archivo->candidato->edicion->REQ (metadato
PII-free determinista: sourceFingerprint + id extraction-task + hash candidato pre-edicion).

## Recomendacion del Arquitecto
El operador decide D-PII y D-ACTOR; con eso, pliego B1/B5/B6 + los majors/minors como edits a DECISION-0056 +
ext10 y promuevo en la misma vuelta. NO promuevo tal cual.
