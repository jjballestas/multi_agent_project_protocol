# ANALISTA - VOZ EXTERNA ADVERSARIAL - carga por archivo v2 FASE C (TASK-0152 / DECISION-0056 / AC41+AC45)

> Voz: Analista (escepticismo externo: intento REFUTAR el guard de egress + el loop extractor). Firma:
> Analista. Fecha: 2026-06-22. Lente: seguridad / honestidad / neutralidad / metodologia.
> ANCLADO EN CANONICO: clon limpio Zeus-protocol `63a80ee` (tree limpio); protocolo HEAD==origin `1dd95c2`.
> Verifique el CODIGO, CORRI `npm test` y PROBE EL GUARD POR COMPORTAMIENTO YO MISMO. NO promovi, NO mute
> estado, NO encendi nada vivo. Esta es la VENTANA REAL DE MODELO.

## VEREDICTO: CAMBIO REQUERIDO. El guard AC45 (vector 1) tiene huecos PROBADOS por comportamiento en
## EXACTAMENTE los vectores que el operador nombro ("DEBE marcar import('undici') / SDK de modelo"). Vectores
## 2-6 PASAN. El codigo ACTUAL no tiene egress (extractor deterministic-local), pero el GUARD -- el deliverable
## de seguridad de la Fase C -- no cumple su requisito en la ruta de egress mas realista (`await import("openai")`).

## Reproduccion (gate por exit code; corrida por mi)
- Zeus clon @ 63a80ee: `npm test` -> 43/43 (estable). Protocolo: `validate` exit 0 CON y SIN secretos; drift
  `has_drift=False`; `scan_domain_neutrality` exit 0; `scan_encoding` exit 0 (la anomalia ASCII del 0151 ya se
  limpio). Core runtime sin cambio (grep candidate/extraction/TASK-EXTRACT en submit_intent.py = 0). #4
  byte-identica (el core no se toca; todo en Zeus + os-tmp).

---

## 1) AC45 GUARD A TODO src/** -> CAMBIO REQUERIDO (huecos probados por comportamiento)
- **Lo bueno (mi recomendacion de Fase A, implementada):** `collectSourceFiles` recurre TODO `src/**` (.js);
  `sourceEgressViolations` cubre una FAMILIA: fetch, `new WebSocket(`, `https?.(request|get)(`,
  `node:(https|net|tls|dgram)` import/require, model-SDK estatico (openai/@anthropic-ai/sdk/@google/
  generative-ai/ai), `execFile(curl|wget|ssh|nc|node)`. Control positivo: `src/evil.js` con `fetch` ->
  flagueado; allowlist: git push -> no flagueado. El src real da [] (cero egress).
- **EL HUECO (probado por mi, aplicando la familia EXACTA del test a payloads):**
  | payload | guard |
  |---------|-------|
  | `const m = await import("openai")` (SDK de modelo DINAMICO) | **SLIPS** |
  | `await import("undici")` (ejemplo EXPLICITO del operador) | **SLIPS** |
  | `import net from "net"; net.connect(443,h)` (bare, sin `node:`) | **SLIPS** |
  | `import axios from "axios"; axios.get(u)` (cliente no nombrado) | **SLIPS** |
  | `import got from "got"; got(u)` | **SLIPS** |
  | `import https from "https"; https.request(u)` | flagged |
  | `new WebSocket(`, `http.request(`, fetch | flagged |
  - El operador pidio que el guard "DEBE marcar" `import('undici')` y un SDK de modelo. **No lo hace** para
    el import DINAMICO ni para `undici`. `net.connect` via import bare tampoco (la familia exige el prefijo
    `node:` y no cubre el call `.connect(`). El control positivo SOLO ejercita `fetch` -> no prueba el resto
    de la familia.
- **Por que importa (no es teorico):** `const openai = await import("openai")` es la ruta de egress MAS
  PROBABLE cuando el agente vivo se encienda; es justo lo que el guard debe atrapar y NO atrapa. El codigo
  actual no tiene egress, pero el guard es la teeth de AC45 para la ventana de modelo.
- **CORRECCION (falsable, pequena):** ampliar `sourceEgressViolations` para marcar: (a) `import(` DINAMICO
  (el codebase usa solo imports estaticos -> cualquier `import(` en src es sospechoso); (b) imports
  bare-specifier de `net|tls|dgram|http|https|dns` (sin exigir `node:`) + sus call sites
  `.connect/.request/.get/.createConnection`; (c) clientes HTTP comunes (undici/axios/got/node-fetch/
  superagent/request) -- o mejor, FLIP a ALLOWLIST (solo modulos permitidos; marcar cualquier otro import).
  Anadir un control positivo POR cada patron nuevo (no solo fetch). Falsable: tras el fix,
  `sourceEgressViolations(new Map([["src/x.js",'await import("openai")']]))` debe ser NO vacio (hoy = []).

## 2) AC45 PURGA/TTL DEL RAW -> PASA (behavior-tested)
- `purgeRawUpload` rm el dir del upload; purga en ESTADO TERMINAL (`approved/discarded` -> purgeRawUpload).
  `sweepExpiredRawUploads` barre `payload.bin` con `mtime` mas viejo que `rawUploadTtlMs` (+ limpia malformados).
- Probado: TTL=1000ms -> raw viejo `assertMissing` (barrido); tras terminal de la candidata `assertMissing
  storePath` (purgado). No queda raw vivo pasado el TTL ni tras aprobar/descartar.

## 3) AC41 LOOP OFF + CONSENTIMIENTO + CERO EGRESS -> PASA (behavior-tested)
- Off-by-default (`extractor.enabled !== true` -> no corre; default disabled). `provider !==
  "deterministic-local" -> 403` (y el config solo admite deterministic-local|disabled, no "openai"). Sin
  consent -> **409**. Con `FILE_EXTRACTION_AGENT` -> corre y `egress.networkEgress === false`, boundary
  `agent_extractor_explicit_consent`. `extractCandidateDrafts` es funcion LOCAL (sin red). Probado: consent
  faltante -> 409; con consent -> status completed-N, networkEgress false. No pude forzar una salida de red
  real desde el extractor.

## 4) CANDIDATAS Y ESTADOS DE EXTRACCION FUERA DEL LEDGER -> PASA
- `extractionStates`/candidatas viven en el candidate store os-tmp (`writeExtractionState`/
  `writeStoredCandidate`), NO en TASK_INDEX/PROJECT_STATE. `git ls-files` del store = vacio; drift 0 con
  extraccion presente; el core runtime no conoce `candidate`/`extraction`. Una extraccion NUNCA atesta en #4
  sin aprobacion humana (solo el intake gobernado aprobado escribe, via submit_intent).

## 5) CARRY AC40/AC43/AC44 -> PASA
- AC40: el src real da [] en el guard (cero egress de modelo en el server). AC43: gate humano DURO de PII
  intacto (aprobar sin declarar -> 409, probado). AC44: re-screen del texto editado intacto (heredado de
  Fase B, en el suite verde).

## 6) #4 BYTE-IDENTICA + GATES -> PASA
- core sin cambio; validate con/sin secretos exit 0; drift 0; neutralidad+encoding exit 0; npm 43/43.

---

## RECOMENDACION DE CIERRE: CAMBIO REQUERIDO (vector 1) antes de cerrar la Fase C.
Default a "no cerrable si dudas" + el operador nombro `import('undici')`/SDK-de-modelo como must-catch y el
guard NO los marca (probado). El fix es chico y acotado al test/guard (ampliar la familia de patrones +
control positivo por patron, o flip a allowlist). Vectores 2-6 estan limpios y el codigo actual no tiene
egress (extractor deterministic-local), asi que NO es un breach vivo; es que la TEETH de AC45 no cierra la
ruta `await import("...")` -- la mas relevante para la ventana de modelo real. Con el guard endurecido +
re-verde, la Fase C queda cerrable.

## Observacion menor
Zeus `63a80ee` != origin `2f760a6` (commits locales sin pushear; esperado in_review). El protocolo SI esta
sincronizado (HEAD==origin 1dd95c2). Uso vivo del agente = GO aparte del operador (fuera de este cierre).

## Que NO hice
- No promovi, no autore SPEC, no mute estado, no cerre, no encendi nada vivo. Ancle en canonico (63a80ee /
  1dd95c2). Suite/probes en clones/temporales; no toque el ledger vivo. Scratch limpiado.
