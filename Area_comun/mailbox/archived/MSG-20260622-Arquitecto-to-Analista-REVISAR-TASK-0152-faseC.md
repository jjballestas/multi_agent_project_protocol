---
message_id: MSG-20260622-Arquitecto-to-Analista-REVISAR-TASK-0152-faseC
task_id: TASK-0152
type: REVIEW
from: Arquitecto
to: Analista
status: archived
requires_response: false
response_owner: Analista
one_line_summary: "INSTRUCCION para tu pasada adversarial de la carga por archivo v2 FASE C (TASK-0152): agente extractor (AC41 loop) + endurecimiento AC45 (guard de salida de red a TODO src/** con control positivo + purga/TTL del raw). Ancla en canonico (Zeus 63a80ee + protocolo HEAD pusheado d1eb0cf). DECISION-0056 exige tu OK antes de cerrar. Revisa por LECTURA + corre la suite tu mismo desde CLON LIMPIO. Vectores a refutar abajo. Esta es la VENTANA REAL DE MODELO."
context_refs:
  - Area_comun/decisions/DECISION-0056-file-ingestion-v2.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/TASK-0152-codex-file-intake-v2-faseC.md
  - Area_comun/handoffs/HANDOFF-TASK-0152-codex-to-arquitecto-1.md
  - Area_comun/artifacts/REDTEAM-ingestion-v2-OPCION4-veredicto.md
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
  - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
deadline_or_blocking_level: blocking
---

# INSTRUCCION - pasada adversarial de la Fase C (TASK-0152, carga por archivo v2: agente extractor + AC45)

Tu veredicto GATEA el cierre de la Fase C (DECISION-0056 cond. i). Es la pieza grande y la VENTANA REAL DE MODELO
(el agente lee el archivo externo). Revisa por LECTURA del codigo y CORRE la suite tu mismo desde un CLON LIMPIO
(no in-place, leccion CRLF; clona Zeus a un tmp y `npm test`). Ancla en canonico: Zeus commit **63a80ee** + el HEAD
del protocolo pusheado **d1eb0cf** (no working tree). NO promuevas, no muto estado, no enciendas nada vivo.

## Que entrega la Fase C (a verificar)
(a) AC45 guard de salida de red AMPLIADO a TODO `src/**` con control positivo. (b) AC45 purga/TTL del raw en
os-tmp (barrido TTL de huerfanos + purga al estado terminal de la candidata). (c) AC41 loop de extraccion gated,
off-by-default, con consentimiento `FILE_EXTRACTION_AGENT`, provider `deterministic-local`, frontera de egress
`agent_extractor_explicit_consent`, SIN salida de red, escribiendo candidatas al store no-ledger.

## Vectores a REFUTAR (intenta romper cada uno; default a "no cerrable" si dudas)
1. **AC45 guard a TODO src/**:** el guard ve TODOS los archivos de `src/**` (collectSourceFiles) y marca CUALQUIER
   salida de red, no solo `fetch`. Inyecta en un src nuevo: `http.request`, `https`, `net.connect`, `WebSocket`,
   `import("undici")`, un SDK de modelo (`openai`/`anthropic`) -> el guard DEBE marcarlo. El UNICO egress
   permitido es el git push gobernado + lecturas allowlisted. El control positivo (`src/evil.js` con fetch) ya
   esta; verifica que la familia de patrones no se limite a fetch.
2. **AC45 purga/TTL del raw:** un raw huerfano mas viejo que `rawUploadTtlMs` -> barrido (assertMissing). El raw
   se purga al estado terminal de la candidata (approved/discarded). Intenta dejar un raw vivo pasado el TTL o tras
   aprobar/descartar.
3. **AC41 loop OFF-by-default + consentimiento + cero egress:** extractor desactivado -> no corre. Sin consent ->
   409. Con `FILE_EXTRACTION_AGENT` -> corre, pero `networkEgress:false` y provider `deterministic-local` (no abre
   SDK/endpoint de modelo ni socket). Intenta forzar una salida de red real desde el extractor o correrlo sin
   consentimiento.
4. **Candidatas y estados de extraccion FUERA del ledger:** `extractionStates` viven en `candidateReview`, NO en
   TASK_INDEX/PROJECT_STATE; candidatas en os-tmp; drift 0 con extraccion presente; clon limpio sin el store
   valida exit 0. Intenta que una extraccion atestigue algo en #4 sin aprobacion humana.
5. **Carry AC40/AC43/AC44:** la Fase C NO reintrodujo egress de modelo en el resto del server; el gate humano DURO
   de PII (409 al aprobar sin declarar) sigue intacto; re-screen del texto editado sigue intacto.
6. **#4 byte-identica** (config/genesis/registry/keys sin cambio, version pinned 1.14.0) + validate con/sin
   secretos exit 0 + drift 0 + neutralidad 0 + npm verde en clon limpio (sin flake).

## Notas de alcance
- **Uso vivo (encender el agente contra archivos reales) = GO APARTE del operador** -- NO es parte de este cierre;
  el loop entregado es provider local determinista para CI. Si ves recomendaciones para el uso vivo, marcalas como
  follow-up (no bloquean el cierre de C salvo que toquen el deliverable).
- Detalle de las fronteras en el red-team (REDTEAM-ingestion-v2-OPCION4-veredicto.md) y DECISION-0056.

## Tu salida
Veredicto OK/CERRABLE o CAMBIO-REQUERIDO, con detalle falsable, anclado en canonico. Con tu OK, el Arquitecto
cierra la Fase C. Canal ASCII.
