# SPEC-0095 - Front: Intake modo "necesidad" (dictar/escribir) -> mismo pipeline de extraccion -> candidatas (REQ-7095D30A)

- **Estado:** draft. Maker: Codex. Checker: Arquitecto + PASADA DEL ANALISTA (PII del texto libre + egress de voz
  opt-in + no-egress de modelo + store fuera del dataset).
- **Fecha:** 2026-06-25. Repo producto: D:/Agentes/Zeus/Zeus-protocol.
- **Origen:** REQ-7095D30A (operador, via Intake gobernado). Reutiliza SPEC-0094/TASK-0179 (dictado por voz) +
  SPEC-0086 AC40-AC44 / TASK-0180 (pipeline Fase B: consumidor determinista no-LLM + store no-ledger + panel de
  revision + gate PII humano).

## Objetivo
Un **tercer modo de entrada** en el Intake -- "Necesidad" (dictar o escribir) -- junto a "Manual" y "Por archivo".
Abre un formulario aparte con un **textarea grande** + el **control de dictado por voz** (el mismo de la opcion
manual), y la **botonera del modo archivo** (Extraer -> candidatas como tarjetas). La necesidad escrita/dictada se
**envia al MISMO pipeline de extraccion** que la carga por archivo (consumidor **determinista no-LLM**), produce
**candidatas** que el operador revisa/edita/aprueba/rechaza, y solo las aprobadas aterrizan como requirements por
el intake gobernado existente.

## Motor de extraccion (decision del operador)
Se construye sobre el **consumidor determinista no-LLM** ya entregado (TASK-0180; provider `deterministic-local`,
`maxCandidates 1`, marcador `none_deterministic_no_llm`): la necesidad -> 1 candidata editable, **sin egress de
modelo**. Cuando se encienda el **extractor LLM (Fase C, gateado)**, este modo hereda 1..N automaticamente por usar
el mismo pipeline. **Fuera de alcance:** el extractor LLM real + su frontera de egress (AC45/AC46).

## Frontera (se MANTIENE; no se debilita)
- **Egress de voz (SPEC-0093/0094):** el dictado usa Web Speech API; off-by-default + opt-in con aviso; sin aceptar
  no captura; sin soporte degrada limpio. Reuso del control de TASK-0179 (es-CO, captura manual con Stop/timer/
  indicador).
- **No-egress de modelo:** el consumidor es determinista (sin fetch/localVlm/http.request/net.connect; el browser
  no referencia modelo).
- **PII (frontera de atestacion -- aclarado tras TASK-0181/Analista):** el texto de la necesidad se envia como
  FUENTE al MISMO flujo de extraccion que el modo archivo (`buildFileExtractionIntents`): el evento ATESTADO #4
  registra UNICAMENTE el SHA-256 de la fuente (JAMAS el texto crudo); el contenido se screenea best-effort (AC40) y
  vive en el store NO-LEDGER `.runtime`; la REDACCION + hard-gate de PII ocurre al APROBAR la candidata (AC43: gate
  humano + re-screening candidate->intake) -> el requirement final aterriza redactado. El texto crudo presente en el
  body del submit es el INSUMO al screening, NO una escritura al ledger atestado (mismo contrato que el modo archivo,
  server.js sin cambios). NO se exige "redaccion en el submit de la fuente"; se exige que el texto crudo NUNCA llegue
  a un evento #4.
- **Sin nueva ruta de escritura** mas alla del `extraction-task` + `requirement-intake` ya gobernados; store de
  candidatas NO-LEDGER (.runtime/file-candidates gitignored, fuera del dataset; drift 0 con candidatas presentes).

## acceptance_criteria
- **AC1 (modo necesidad en el selector)** El panel de Intake ofrece el modo **"Necesidad"** (dictar/escribir) junto
  a Manual y Por archivo (carry AC42; obligatorios validados antes de EXECUTE en su flujo). Conforme al
  design-system (AC13). Behavior-test: el selector expone el modo necesidad con su flujo propio.
- **AC2 (formulario textarea + mic)** El modo necesidad abre un formulario aparte con un **textarea grande** + el
  **control de dictado por voz reutilizado** (SPEC-0094: es-CO, captura manual continuous con Stop/timer/indicador,
  egress opt-in/off-by-default + aviso). Texto escrito o dictado llena el textarea. Behavior-test: el formulario
  expone textarea + control de mic; el dictado inserta el texto en el textarea (carry SPEC-0094 AC1-AC4).
- **AC3 (envio al pipeline determinista)** La botonera (estilo modo-archivo) permite **Extraer**: el contenido del
  textarea se envia como FUENTE (inerte, screened best-effort PII) al **MISMO** pipeline que el modo-archivo ->
  **consumidor determinista no-LLM** -> candidatas en el store NO-LEDGER `.runtime/file-candidates` gitignored
  fuera del dataset. NO invoca fetch/modelo. Behavior-test: el envio del modo necesidad emite la extraction-task
  determinista; sin egress de modelo; las candidatas no aparecen en TASK_INDEX (drift 0; clon limpio sin store
  valida exit 0).
- **AC3-bis (frontera de atestacion PII, PERMANENTE -- gateante TASK-0181)** Behavior-test que pruebe que una
  necesidad con literales PII (email/telefono/documento/direccion) emite intents donde el texto crudo NO aparece:
  los intents atestados (`buildFileExtractionIntents`) contienen `source_file_sha256` y NO los literales PII del
  textarea. El texto crudo NUNCA llega a un evento #4. Cierra formalmente la observacion del Analista.
- **AC4 (revision + gate PII + aprobar, reuso)** Las candidatas del modo necesidad usan el **MISMO** panel de
  revision + **gate PII humano** (AC43) + aprobar -> `requirement-intake` gobernado (AC39) que el modo-archivo:
  aprobar exige declarar PII (piiReviewed===true), el id deriva del CONTENIDO EDITADO, solo aprobadas aterrizan como
  requirements; descartar purga el raw. Behavior-test: aprobar sin declarar PII -> bloqueado; con PII declarada ->
  requirement real (id+seq).

## Carries (deben seguir verdes)
- Egress de voz off-by-default + aviso opt-in (SPEC-0093/0094); no-egress de modelo (consumidor determinista);
  store fuera del dataset + drift 0 + purga del raw (AC44); OFF-by-default; #4 byte-identica; AC11/AC12/AC13.

## DoD
- AC1-AC4 + carries verdes con behavior-tests; `node --test` clon limpio exit 0 (estable); validate con/sin
  secretos exit 0; **drift 0 con candidatas presentes**; neutralidad/encoding limpio; #4 byte-identica; sin nueva
  ruta de escritura (unica mutacion de ledger = el `requirement-intake`/`task_upsert` ya gobernado).
- Checker (Arquitecto) clon limpio; maker!=checker. **PASADA DEL ANALISTA** (PII del texto libre de la necesidad +
  egress de voz opt-in + no-egress de modelo + store fuera del dataset + gate PII humano efectivo).
- REPRO: en el Intake, elegir "Necesidad" -> formulario con textarea + mic; dictar/escribir una necesidad ->
  Extraer -> aparece 1 candidata editable; aprobar sin declarar PII = bloqueado; declarar PII + aprobar -> aterriza
  1 requirement real; descartar -> purga el raw; clon limpio sin el store valida exit 0; drift 0.

## Notas
- 1..N: hoy 1 candidata (determinista, maxCandidates 1); 1..N llega al encender Fase C (mismo pipeline), sin tocar
  este modo. El modo necesidad es, en lo esencial, una nueva SUPERFICIE DE ENTRADA (textarea/voz) al pipeline ya
  entregado de la carga por archivo.
