# ANALISTA - VOZ EXTERNA ADVERSARIAL - carga por archivo v2 FASE A (TASK-0150 / DECISION-0056 / AC40-AC42)

> Voz: Analista (escepticismo externo: intento REFUTAR el bounding ingest/egress/PII de la Fase A).
> Firma: Analista. Fecha: 2026-06-20. Lente: seguridad / honestidad / neutralidad / metodologia.
> ANCLADO EN CANONICO: protocolo HEAD==origin `f494f06`; codigo en clon limpio Zeus-protocol `5121335`
> (tree limpio). Verifique el CODIGO y CORRI `npm test` YO MISMO (x4, + 3 de estabilidad). NO promovi, NO
> autore SPEC, NO mute estado, NO encendi nada vivo.
> ALCANCE: Fase A = PLUMBING + FRONTERA. El loop de extraccion (agente lee archivo -> candidatas) es
> Fase C, NO construido. Verifico la frontera y el no-MODELO-egress del SERVER; la ventana de lectura del
> agente es Fase C (gateada), reconocida honestamente, no oculta.

## VEREDICTO: OK -> CERRABLE la Fase A. 10/10 puntos PASAN por comportamiento. 2 recomendaciones de
## ENDURECIMIENTO (no bloqueantes, prerequisito de Fase B/C). Mi hallazgo CRLF previo (TASK-0148) RESUELTO.

## Reproduccion (gate por exit code; corrida por mi)
- Zeus clon @ 5121335: `npm test` -> **42/42** (estabilidad: 3 corridas consecutivas 42/0). El `.gitattributes`
  (`* text=auto eol=lf`) cierra mi hallazgo CRLF previo; el manual quedo LF-only en clon limpio.
- Protocolo: `validate` exit 0 CON secretos y exit 0 SIN secretos (clon git); drift `has_drift=False`;
  `scan_domain_neutrality` exit 0, `scan_encoding` exit 0. #4 epoca 1.14.0 byte-identica (el core no cambio;
  el test asserta protocol.config.json byte-identico).

---

## 1) AC40 SERVER NO-MODELO-EGRESS -> PASA (con recomendacion de endurecimiento)
- **Estructural:** `src/server.js` hace CERO egress saliente (los unicos `http://` son `new URL(request.url,
  "http://127.0.0.1")` para parsear el request entrante + el log de listen). Sin `fetch(`, sin
  `http(s).request`, sin socket, sin `new WebSocket`, sin `node:net|tls|dgram`, sin `import()` dinamico. Su
  unico import local (`./canonicalReader.js`) tambien tiene CERO egress. La unica red es `git push/ls-remote`
  (commit-push gateado, al remote del protocolo) -- no es un modelo.
- **Guard + control POSITIVO:** el test asserta `modelEgressPattern.test(server) === false` Y
  `modelEgressPattern.test('import OpenAI from "openai"; fetch("https://api.openai.com/...")') === true` ->
  la regex NO es vacua: atrapa de verdad un import/endpoint falso. Cubre openai/@anthropic-ai/sdk/
  @google/generative-ai/ai (import+require), api.openai/anthropic.com, generativelanguage.googleapis.com,
  new WebSocket(, node:net|tls|dgram.
- **RECOMENDACION DE ENDURECIMIENTO (no bloquea Fase A; PREREQUISITO de Fase B/C):** el guard escanea SOLO
  `server.js` (no `canonicalReader.js` ni el grafo de imports) y es PROVIDER-ESPECIFICO. Rutas que NO
  atraparia: (a) egress en OTRO archivo src importado por el server; (b) `fetch(urlGenerica)` a un proveedor
  no listado (cohere/mistral/azure-openai/openrouter/ollama/un proxy); (c) endpoint concatenado/ofuscado.
  Hoy NO hay egress (verificado estructural), asi que no es una brecha de Fase A; PERO el guard debe
  ampliarse (escanear todo `src/**` + marcar CUALQUIER primitiva de red saliente, no solo proveedores
  nombrados) ANTES de Fase C, que es cuando se enciende la ventana de modelo real (el agente). Falsable: el
  guard hoy pasaria un `src/extractor.js` con `import OpenAI`.

## 2) STORE FUERA DEL DATASET -> PASA (behavior-tested)
- Uploads en `FILE_UPLOAD_STORE_ROOT || tmpdir()/zeus-protocol-file-intake`. Probado: el task lleva solo
  `source_file_sha256` + `source_store_locator` (os-tmp) + `source_store_kind:os_tmp_outside_attested_dataset`;
  `git ls-files -- <locator>` = VACIO; `storePath.startsWith(protocolRoot) === false` (fuera del repo);
  SHA-256 sobre bytes verificado (`sha256 !== upload.sha256 || size != sizeBytes -> 400`); el raw NUNCA entra
  al repo/atestado; drift 0 con uploads; protocol.config.json byte-identico. **El archivo crudo no se cuela
  al #4.**
- Nota menor (Fase B/C): el raw PERSISTE en os-tmp (no hay purga activa en Fase A; se conserva para que el
  agente Fase C lo lea). Esta FUERA del dataset, pero conviene una politica de purga/TTL del raw en Fase B/C
  (PII en disco temporal). No bloquea Fase A.

## 3) PII EN INGEST (best-effort HONESTO) -> PASA
- `screenPiiBestEffort(file.text)` aplica patrones reales (email `/..@..\.[A-Z]{2,}/`, phone
  `/\+?\d[\d .-]{7,}\d/`, + NIT/razon social/SQL). Devuelve `{mode:"best_effort", guaranteed:false}`; el task
  renderiza `guaranteed: false` (probado en el test). Declarado HONESTAMENTE best-effort, no "garantizado".
- Ninguna PII de terceros es REQUERIDA para aterrizar; el task aterrizado NO contiene PII cruda
  (`doesNotMatch /900.123.456|dbo.saldos|SELECT/`). Dataset PII-free en el plano atestado.

## 4) CONTRATO de la extraction-task -> PASA (autocontenido, carga los gates duros)
- El `extraction_contract` lleva: `source_file_sha256`, `verify_sha256`, formato con `candidate_hash`,
  `destination: "external candidate store outside ledger"`, y `done_when: "candidates are written outside the
  ledger and each candidate still requires human PII review before governed intake"`. Carga el GATE-PII-HUMANO
  duro y el candidate-fuera-de-ledger en el propio artefacto.

## 5) CANDIDATAS NO-LEDGER -> PASA
- `candidate` NO esta en `VALID_TASK_STATUSES` (runtime) y NO se agrega; el grep de `candidate`/`extraction`
  en `runtime/submit_intent.py` es VACIO -> el core NO cambio. El ledger atestado NUNCA puede ver `candidate`
  (un task_status a/desde `candidate` seria rechazado). Estructura/contrato validados aunque Fase A no genere
  candidatas.

## 6) IDEMPOTENCIA upload -> PASA
- id/idempotencyKey por `sha256(sha256_bytes|project)`. Probado: re-subir identico (segundo execute) -> 200 y
  TASK_INDEX sigue con 1 sola task.

## 7) OFF / GATED -> PASA
- Off-by-default (`file-ingestion.config.json` enabled:false; html sin `enabled:true`). Probado: server sin
  config -> upload -> **403 "disabled"**. Activacion por env (`FILE_INGESTION_CONFIG_PATH`/
  `FILE_UPLOAD_STORE_ROOT`), runtime/operador; el cliente NO la enciende. AC42: selector de modo
  (`intake-mode-selector` radiogroup, dry_run vs EXECUTE) presente; sin preview-as-green (dry_run != execute).

## 8) ATRIBUCION (D-ACTOR) -> PASA
- El upload/extraction-task lleva `author:"Operador"`, `relayed_by:"Arquitecto"`, `endorsement:"none"` -- y
  esos literales viven en el SERVER de Zeus (producto), NO en el core neutral (consistente con la leccion de
  neutralidad de DECISION-0053/TASK-0138). Relay HONESTO (firma=Arquitecto, no aval). El cliente no inyecta
  actor (`payload.actorId` -> 400) ni paths/intents.

## 9) HONESTIDAD -> PASA (Fase A)
- El contrato exige que el extractor registre un `no-candidate/failed state` (closure_criterion); el estado
  de extraccion explicito completo (0/basura/cap/failed/timeout/sin-agente) pertenece al LOOP = Fase C
  (gateada), reconocido honestamente. Errores/logs NUNCA ecoan contenido crudo (grep de `ClientError`
  interpolando text/bytes/content = VACIO; los errores son metadata: "upload bytes do not match attested
  metadata", "file type is not allowed"). Exito solo con aterrizaje real (id+seq).

## 10) NO-BYPASS / NEUTRALIDAD -> PASA
- Unica via de escritura = submit_intent; sin ruta directa al filesystem/ledger (test no-bypass verde).
  `scan_domain_neutrality` exit 0, `scan_encoding` exit 0. #4 epoca 1.14.0 byte-identica (core sin cambio).

---

## Observaciones (menores, declaradas, NO bloquean)
- **Flake de arranque en frio:** la 1a corrida del clon dio 41/42; 3 corridas siguientes 42/42. Probable
  timeout en frio de un test behavioral (spawn server + git + python). Verde estable en re-corrida; lo dejo
  explicito por el enfasis en "verde".
- **HEAD vs origin:** Zeus `5121335` != origin `2f760a6` (commits locales sin pushear; esperado en
  in_review). El protocolo SI esta sincronizado (HEAD==origin f494f06).

## RECOMENDACIONES (prerequisito de Fase B/C, NO de cierre de Fase A)
1. Ampliar el guard AC40: escanear todo `src/**` (no solo server.js) y marcar CUALQUIER primitiva de red
   saliente (fetch/http/socket genericos), no solo proveedores nombrados -- ANTES de Fase C (cuando enciende
   el agente = la ventana de modelo real).
2. Politica de purga/TTL del raw en os-tmp (PII en disco temporal) para Fase B/C.

## RECOMENDACION DE CIERRE: OK, CERRABLE la FASE A.
Los 10 puntos de bounding/egress/PII PASAN por comportamiento; el server NUNCA llama a un modelo (estructural
+ control positivo); el raw nunca toca el #4; las candidatas no existen en el ledger; PII honesta best-effort;
no-bypass; #4 byte-identica. Las dos recomendaciones son endurecimiento para Fase B/C, no defectos de Fase A.
Fases B (panel + gate-PII) y C (agente extractor) siguen pendientes; nada se enciende vivo. El cierre formal
es del Arquitecto (checker) + operador.

## Que NO hice
- No promovi, no autore SPEC, no mute estado, no cerre, no encendi la ingestion/extraccion viva. Ancle en
  canonico (f494f06 / 5121335), no working tree. Suite/escritura real en clones temporales; no toque el
  ledger vivo. Scratch limpiado.
