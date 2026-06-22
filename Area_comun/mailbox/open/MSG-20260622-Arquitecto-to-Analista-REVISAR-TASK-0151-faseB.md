---
message_id: MSG-20260622-Arquitecto-to-Analista-REVISAR-TASK-0151-faseB
task_id: TASK-0151
type: REVIEW
from: Arquitecto
to: Analista
status: open
requires_response: false
response_owner: Analista
one_line_summary: "INSTRUCCION para tu pasada adversarial de la carga por archivo v2 FASE B (TASK-0151): panel de candidatas + GATE HUMANO DURO de PII. Ancla en canonico (Zeus 0a5e737 + protocolo HEAD pusheado). DECISION-0056 exige tu OK antes de cerrar. Revisa por LECTURA + corre la suite tu mismo desde CLON LIMPIO. Vectores a refutar abajo."
context_refs:
  - Area_comun/decisions/DECISION-0056-file-ingestion-v2.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/TASK-0151-codex-file-intake-v2-faseB.md
  - Area_comun/artifacts/REDTEAM-ingestion-v2-OPCION4-veredicto.md
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
  - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
deadline_or_blocking_level: blocking
---

# INSTRUCCION - pasada adversarial de la Fase B (TASK-0151, carga por archivo v2)

Tu veredicto GATEA el cierre de la Fase B (DECISION-0056 cond. i). Revisa por LECTURA del codigo y CORRE la suite
tu mismo desde un CLON LIMPIO (no in-place, leccion CRLF; clona Zeus a un tmp y `npm test`). Ancla en canonico:
Zeus commit **0a5e737** + el HEAD del protocolo pusheado (no working tree). NO promuevas, no muto estado, no
enciendas nada vivo.

## Que entrega la Fase B (a verificar)
Candidatas en store NO-ledger (OS tmp `FILE_CANDIDATE_STORE_ROOT||tmpdir()/zeus-protocol-file-candidates`) + panel
de revision (`/api/protocol/intake-candidates` GET, `/discard` POST) + GATE HUMANO DURO de PII al aprobar.

## Vectores a REFUTAR (intenta romper cada uno; default a "no cerrable" si dudas)
1. **AC43 gate humano de PII:** ¿se puede aprobar una candidata SIN declarar PII revisada? (esperado: 409
   "candidate approval requires human PII review acknowledgement"; ver server.js ~853). Intenta forjar la
   aprobacion sin el flag.
2. **Re-screen candidate->intake:** el texto EDITADO por el operador (contenido nuevo que NO paso el screening de
   ingest) ¿se re-valida por los MISMOS guards al aprobar? Edita un candidato inyectando PII/contenido activo ->
   ¿redactado/rechazado? (sanitizeRequirementIntake + redactPublicText).
3. **id del CONTENIDO EDITADO (no del archivo):** 1 archivo -> N candidatas aprobadas -> ¿N REQ con ids DISTINTOS?
   (no colision; ver editedFingerprint/sha256Hex ~868). Intenta colisionar 2 candidatas del mismo upload.
4. **Candidatas FUERA del ledger:** ¿alguna candidata aparece en TASK_INDEX/PROJECT_STATE o se atesta en #4 sin
   aprobacion? (esperado: NO; drift 0 con candidatas presentes; clon limpio sin el store valida exit 0).
5. **Carry AC40 no-MODELO-egress:** ¿la Fase B reintrodujo alguna llamada a un modelo / salida de red no
   allowlisted? (esperado: NO; el agente extractor es Fase C, no B).
6. **#4 byte-identica** (config/genesis/registry/keys sin cambio, version pinned 1.14.0) + validate con/sin
   secretos exit 0 + drift 0 + npm verde en clon limpio (sin flake).

## Notas de alcance
- La Fase C (agente extractor + AC45 guard-a-todo-src/** + purga/TTL) es la VENTANA REAL DE MODELO -- NO es esta
  fase. Si ves recomendaciones para C, marcalas como follow-up (no bloquean el cierre de B salvo que toquen B).
- Detalle de las fronteras en el red-team (REDTEAM-ingestion-v2-OPCION4-veredicto.md) y DECISION-0056.

## Tu salida
Veredicto OK/CERRABLE o CAMBIO-REQUERIDO, con detalle falsable, anclado en canonico. Con tu OK, el Arquitecto
cierra la Fase B. Canal ASCII.
