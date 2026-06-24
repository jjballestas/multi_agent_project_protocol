# MEMORY - Analista (voz analista; firma "Analista", antes "Claude-analista") - multi_agent_project_protocol

> FIRMA (2026-06-15, orden del operador): firmo como **Analista** (sin prefijo "Claude-", que confunde con
> el arquitecto Claude). Mensajes from: Analista / to: Analista. Carpeta personal/Analista/ por ahora.
> Runbook privado de la voz analista. Conciso: rol + estado de la ultima sesion + lecciones.
> El detalle tecnico profundo (escritor unico, flags, capabilities) vive en `personal/Arquitecto/MEMORY.md`
> (arquitecto). Yo no muto estado; solo lo entiendo.
> Ultima actualizacion: 2026-06-22 (serie front intake/carga-por-archivo v2; #4 ON en vivo; epoca 1.14.0).

## Rol (clave)
- VOZ analista independiente en revisiones adversariales. NO arquitecto, NO consolidador.
  maker != checker: no leo las otras voces mientras produzco la mia; no consolido, no decido,
  no muto estado autoritativo (eso = submit_intent del arquitecto/runtime, escritor unico).
- Lentes ejercidas: fuentes/SOTA (existencia de papers + coincidencia de claims;
  CONFIRMADO/MAL-ATRIBUIDO/NO-VERIFICABLE) y honestidad/metodologia (no-overreach, fidelidad de
  taxonomias, completitud de gobernadores, consistencia entre decisiones).
- Principio rector: umbrales/metas de la MEDICION PROPIA (measure_context_cost, DECISION-0008),
  no de citas.

## Entrega (formato)
- Artefacto `Area_comun/artifacts/ANALISTA-<tema>.md`: veredicto de cabecera + por punto
  PASA / CAMBIO REQUERIDO (concreto, falsable) / RIESGO DECLARADO. Proporcional; sin meta-proyecto.
- Aviso compact en `Area_comun/mailbox/open/`, requested_action -> artefacto.

## Pasadas entregadas (historial)
- Deltas SOTA para SPEC-0078: DELTA-1 (KV-cache, 2602.16284) y DELTA-2 (Focus, 2601.07190)
  MAL-ATRIBUIDOS; convergencia 2-2 con Codex (factibilidad). Recogida por el arquitecto.
- #3 cost-attribution (SPEC-0079/DECISION-0033): veredicto GO-con-un-cambio (tag cost_unit/cost_schema
  + subject canonico; subject_hash = seudonimo no anonimo). Incorporado: v1.6.0 quedo con cost_schema=2.
- Fase 0 E5+E6 (DECISION-0034): MAST fiel 14/14; marque el conteo "12 incidentes reales" como overreach
  (pisa #1 diferido) y que el gobernador E6 es elegibilidad no contencion (runaway lo para SA.4).
  Ratificado v1.7.0 con mis 3 ajustes.
- #1/protocol_research satelite (DECISION-0035): veredicto RATIFICABLE-con-ajustes. P1 limite #1 honesto
  (comparabilidad MAST-Data reportada como limite, no citable). 3 ajustes: P2 lenguaje "innegociable"->
  "sostenido por diseno, no sandbox" + enforcement read-only real como condicion de GATE-DATASET; P3 frase
  "raises if run" inexacta (verificado: python stub.py.stub -> exit 0 inerte); P4 "scan clean=>no research
  terms" non-sequitur (decisions/** exento; denylist solo trading). Concurri con la reconciliacion del
  mapeo de gates al brief 07 (GATE-DATASET legal gob. #1-citabilidad + #2/#3 produccion; GATE-INST
  institucional + PRE-REG gob. harness) + marque 1 header stale post-GATE-INST en README de #2/#3.
  RATIFICADO y PUBLICADO v1.8.0.
- DECISION-0036 narracion minima DURA y uniforme (afila addendum DECISION-0005 en AGENTS.md s.7): veredicto
  RATIFICABLE-con-ajustes. 1 cambio falsable: frase absoluta "reasoning never in user-facing output" choca
  con carve-out "reasoning IS the deliverable" -> acotar a narracion de PROCESO. 1 riesgo de honestidad de
  causa: narro pese a regla+memoria => binding constraint = cumplimiento, no blandura. RATIFICADO: aterrizo
  en protocol_version 1.9.0.
- TASK-0100 decision-A / DECISION-0037 (rescope eol=lf a futuros + v1.1.0 pre-normalizacion, NO re-firmar):
  CONCURRO-con-ajustes. CLASIFIQUE los 757 SBOM (script propio): 616 LF / 127 CRLF (Codex nombro ~3) / 14
  mismatch NO-EOL. HALLAZGO CLAVE (mas serio que EOL): el manifest firmado se genero sobre ARBOL SUCIO (14
  ficheros casan el working tree, no el commit 04436c3 que el manifest declara); runtime/protocol_replay.py
  IRREPRODUCIBLE desde refs. => v1.1.0 no se reproduce desde checkout limpio. Premisa SPEC-0075 ("blobs ya
  son LF") falsa en v1.1.0 (127 CRLF; cierto solo en HEAD, verificado: 0 i/crlf en HEAD). A-vs-B: B no puede
  reproducir el original -> A preferible POR INTEGRIDAD (no por evitar trabajo). Tag 703ed93 != commit
  manifest 04436c3 = ESPERADO, no defecto. RATIFICADO: DECISION-0037 registrada con MIS 5 ajustes
  incorporados completos (HEAD c0afb96); TASK-0100 reabierta rescoped + GO a Codex; bump PATCH 1.9.1 al
  cierre. maker!=checker: A vs B fue del operador; yo informe el tradeoff.
- TASK-0100 IMPLEMENTACION (Codex, commit 4b1833d, in_review): pasada adversarial independiente -> CONCURRO
  con cerrar a done. Verificado por mi: dist/v1.1.0/KNOWN_LIMITATIONS.md realiza mis 5 ajustes sin eufemismo;
  verify_release v1.1.0 ok:False (pin NO lo cambia) + diff.changed=30 NO suprimido + release_scope solo nota;
  commit NO toca manifest/signature/cosign/provenance/sbom/verify.*; .gitattributes (* text=auto eol=lf +
  binarios) + golden release 7/7; enmienda SPEC-0075 anota premisa falsa. 1 nota opcional: 616/127/14 (vs
  commit 04436c3) vs diff 30 (vs working tree vivo) = bases distintas, ambas honestas. Cierre = del reviewer.
  CERRADO: v1.9.1 PUBLICADO (72f8dd3) tras mi concurrencia; TASK-0100 done (trio 1/3). Trio 2/3 = TASK-0095
  promovida a Codex (0c01cdd).
- TASK-0095 IMPLEMENTACION (Codex, commit 5046ecc "commit task markdown side effects", in_review): pasada
  adversarial independiente -> CONCURRO con cerrar a done. apply.py: task_file_commit_paths deriva task_ids
  SOLO de las transiciones del turno (task_status del report + task_upserts), retorna [] sin transicion,
  devuelve solo el .md de esas tareas; ADITIVO a la lista de commit, no toca gate/claims. Verificado por mi:
  runtime_apply 4/4 (aserto tree limpio + HEAD status:in_review), runtime_loop 15/15, real_adapter 4/4,
  intent_flow 11/11, validador/encoding/neutralidad 0; sin .ps1 de apply. Sin ajustes. CERRADO: v1.9.2
  PUBLICADO (84cbe15) tras mi concurrencia; TASK-0095 done (trio 2/3). Trio 3/3 = TASK-0096 promovida a
  Codex (f132086). v1.9.2->trio sigue; narracion minima reforzada a "primordial" en docs de protocolo
  (commit 0135f42) tras el enfasis del operador.
- TASK-0096 (trio 3/3, run_id unico por corrida; Codex commit 3add1c9 in_review): pasada adversarial
  independiente -> CONCURRO con cerrar (cierra el trio). real_invoker_run_id_error: subprocess EXIGE --run-id
  no vacio + RECHAZA si run_log existe; replay deterministico intacto. Goldens verificados por mi: real_adapter
  fresh-run-id (sentinel no creado) + supervised_autonomy consecutive-distinct-logs (logs distintos,
  turns_total==1 c/u = sin agregacion cruzada, 1 linea/log). Sin Date.now()/random; sin cambio gate/claims.
  Suites 6/5/10/15/5/5/11 + validador/neutralidad/encoding verdes. Higiene: move mi sync answered open->answered
  (mismatch pre-existente). LAPSO: rompi ASCII en MI mensaje (acento), corregido -> scan_encoding SIEMPRE antes
  de aseverar. CERRADO: TASK-0096 done v1.9.3 (respaldado por MI CONCURRO independiente); TRIO OFF-PILOT
  COMPLETO (TASK-0100 v1.9.1, TASK-0095 v1.9.2, TASK-0096 v1.9.3). INTEGRIDAD (DECISION-0018): el operador
  confirmo que la sesion que firmo TASK0100/0095/0096-impl como "Claude-analista" era el ARQUITECTO
  (mis-atribucion: el revisor NO debe firmar como voz analista); MI verdict-independiente es la voz analista
  OFICIAL; cuenta UNA voz (la mia). Reforma de firma adoptada: firmo "Analista". El arquitecto me mando
  STAND-DOWN; pare el cron.

## Serie FRONT intake / carga-por-archivo v2 (2026-06-20..22) -- VOZ ADVERSARIAL del producto Zeus
> Proyecto-front Zeus-protocol (repo PRODUCTO separado D:\Agentes\Zeus\Zeus-protocol; gobernanza/SPEC-0086/
> handoffs en Area_comun=dataset; DECISION-0049/0050). Codex maker / Arquitecto checker / yo adversarial
> independiente; DECISION-0056 exige mi OK para cerrar cada fase. Metodo SIEMPRE: clono Zeus a tmp en C:,
> corro npm test YO, pruebo POR COMPORTAMIENTO, gateo por EXIT CODE.
- TASK-0154 (behavior-tests AC48/AC49/AC50): OK/CERRABLE sobre Zeus `da5825d8405f3b2140e42821c6183c90bba49ec9`
  + protocolo `5b04324`. Clean clone producto `npm test` 47/47 exit 0. Mutaciones propias falsables:
  quitar `governed-button` del boton compose -> AC48 exit 1; hacer reset en `mode==="compose"` -> AC49 exit 1;
  cachear `loadProtocolSnapshot` por modulo -> AC50 exit 1 (`1.0.0 !== 1.0.1`). Gates protocolo: validate con
  y sin secretos exit 0; drift 0; neutrality/encoding exit 0; #4 byte-identica. Veredicto y MSG commiteados y
  pusheados en `c0484e5` (`review(TASK-0154): Analista OK behavior tests`). Residuales no bloqueantes: AC48 no
  es test visual pixel-perfect; AC49 no simula click DOM completo pero cubre funcion de negocio; AC50 cubre server
  snapshot fresco, mientras refetch de front pertenece a AC29.
- TASK-0128 (vista atestacion #4): CONCURRO (badges derivados del runtime + fail-closed, guarda PII redactada).
- TASK-0134 (relay anti-impersonacion): HALLE el hueco -- el front confiaba `payload.actorId`/`payload.intents`
  -> un POST local podia forjar decision/claim/task_status FIRMADA como Arquitecto (enforce no lo paraba: el
  claim iba en la misma tx). CAMBIO. Re-verifique el fix CERRADO: builder server-side, execute solo para
  requirement-intake (403 el resto), payload.actorId/intents -> 400, prueba negativa PERMANENTE.
- TASK-0138 (mailbox_archive, kind core nuevo): HALLE leak de NEUTRALIDAD -- `runtime/submit_intent.py`
  hardcodeaba `author:"Operador"`/`relayed_by:"Arquitecto"` (identidades de instancia en el core neutral; el
  scan no lo atrapaba). CAMBIO. Re-verifique CALLER-DERIVED (require_text; literales movidos al server Zeus =
  producto) + scan de neutralidad regresion-proof (inyecte "Operador" en copia de submit_intent.py -> scan
  exit 1; submit_intent.py NO esta en la whitelist legacy).
- TASK-0139 (commit-push acotado): OK. No-drag (`git commit --only -- <paths>`) y non-fast-forward (409 sin
  sobrescribir) PROBADOS por comportamiento contra un bare-remote local; landed solo tras ls-remote real.
- TASK-0148 (intake v1): HALLE suite ROJA en clon LIMPIO Windows -- el test mermaid usa regex LF-only
  (`/```+mermaid\n/`) y el manual quedo CRLF (core.autocrlf=true, sin .gitattributes). Fix `.gitattributes
  eol=lf` (entro en TASK-0150+). Ingestion v1 limpia 7/7.
- TASK-0150 (file v2 Fase A plumbing): OK 7/7 (store os-tmp fuera del repo, raw nunca al #4, server CERO
  egress, candidatas no en VALID_TASK_STATUSES) + RECO ampliar el guard AC40/AC45 a todo src/**.
- TASK-0151 (Fase B panel + gate humano DURO de PII): OK 6/6 (aprobar sin piiReviewed -> 409; re-screen del
  texto editado; editedFingerprint -> ids distintos; candidatas fuera del ledger; provenance-mismatch -> 409)
  + ANOMALIA DECISION-0018: el MENSAJE del Arquitecto rompia ASCII (notifique, no lo arregle).
- TASK-0152 (Fase C agente extractor + AC45 = LA VENTANA REAL DE MODELO): HALLE 5 huecos del guard de egress,
  PROBADOS por comportamiento -- `await import("openai")` (dinamico), `import("undici")`, `net.connect` bare,
  `axios`, `got` SLIPS (el guard solo veia server.js + proveedores nombrados + import estatico). CAMBIO-
  REQUERIDO. Re-verifique el rework CERRADO: familia ampliada (dynamic-import marca CUALQUIER `import(`,
  network-call, bare network-module, model-sdk/http-package estatico Y dinamico) + control positivo POR
  familia; los 5 huecos ahora FLAGGED; src real []. OK/CERRABLE con RESIDUAL DECLARADO: un scan estatico
  inherentemente NO atrapa clientes HTTP no listados (phin/needle) ni ofuscacion (eval/computed-global) ->
  reco ALLOWLIST + marcar eval/new Function como follow-up del USO VIVO. Extractor entregado = deterministic-
  local (cero egress); uso vivo = GO APARTE del operador.

- TASK-0153 (guard ALLOWLIST AC46 + aislamiento AC47, 2 pasadas): PASADA 1 sobre Zeus ac2e308 -- import-side
  flip a deny-by-default CERRO el residual que declare en Fase C (phin/needle + eval), confirmado por
  comportamiento; PERO halle escape NUEVO: `external-cli` seguia DENYLIST {curl,wget,ssh,nc,node} sobre
  child_process -> execFile/spawn("powershell"|"sh", curl/IWR) ESCAPABA. CAMBIO. El Arquitecto lo devolvio a
  Codex. PASADA 2 (re-verificacion) sobre Zeus 5cb8910 + protocolo HEAD 15e66a1: external-cli paso a ALLOWLIST
  de binarios spawneados {git,python} -> powershell/sh/bash/cmd/curl/wget + hints node/deno/pwsh/nc/paths
  absolutos TODOS FLAGGED; git/python y src real -> [] (sin FP). 44/44 exit 0 clon limpio; gates protocolo exit 0;
  #4 byte-identica. RESIDUAL NUEVO declarado (NO bloqueante): `child_process.exec`/`execSync` NO estan en
  cliPattern (solo execFile*/spawn*) -> exec("curl...") escapa; ademas python -c y git ext::/fetch son gadgets
  allowlisted INEVITABLES (no hay "cero egress" por scan estatico). Por que residual y no bloqueo: un fix bare
  `\bexec\(` COLISIONA con RegExp.exec que el src real usa (canonicalReader.js:229/243); fix limpio = import-binding
  (marcar import de exec/execSync desde node:child_process; src solo importa {execFile,spawn} -> cero FP) y queda
  como follow-up del USO VIVO. Veredicto = CERRABLE con residual declarado. Commit 56da208 (autor Analista) PUSHEADO
  a origin/main yo mismo (cron ANALISTA-EJECUTOR autoriza commitear mi propio veredicto con rutas explicitas,
  gateado por validate+encoding exit 0, ventana 0 claims activos). LECCION: un allowlist de binarios spawneados NO
  da "cero egress" si los binarios permitidos son interpretes (python -c) o tienen transportes (git ext::); el gate
  real del egress en vivo es el extractor deterministic-local, no el scan (regresion-proof, no sandbox).
- TASK-0153 exec-import final (2026-06-22): re-verifique la devolucion final sobre Zeus `8751051` + protocolo
  `b5c7e7a`. Resultado: OK/CERRABLE. `cli-exec-import` marca named imports y destructured requires de
  `exec`/`execSync` desde `child_process`/`node:child_process`, sin falso positivo en `RegExp.exec` ni en src real.
  Clon limpio producto `npm test` 44/44 exit 0; payloads propios 10/10; validate con/sin secretos exit 0; drift 0;
  neutralidad/encoding exit 0; #4 sin cambios de bytes. Commit de veredicto: `54c2374` (`review(TASK-0153):
  Analista OK exec import`). Residual no bloqueante queda solo en gadgets inherentes `python -c` / `git ext::` para
  la ventana posterior de uso vivo.
- TASK-0155 (local-vlm provider AC51/AC52/AC53): PASADA sobre Zeus `79be511` + protocolo `90de6fa` -> CAMBIO-
  REQUERIDO. Clon limpio producto `npm test` 48/48 exit 0. AC52 comportamiento real contra servidor: `0.0.0.0`,
  `8.8.8.8`, `evil.com`, IPv6 no-loopback, `127.0.0.1.evil.com`, `[::ffff:8.8.8.8]` deshabilitan config; PERO
  `http://2130706433:11434/api/chat` queda habilitado como `local-vlm` (URL lo canonicaliza a loopback). Como el
  prompt pidio ese truco y AC52 dice solo host:puerto local allowlisted, lo gatee como escape/canonicalizacion sin
  test. AC46 payloads propios pasaron; AC51/AC53 pasan por suite y lectura. Gates protocolo: validate con secretos
  en vivo exit 0, sin secretos en clon limpio exit 0, drift 0 up_to_seq 1191, neutrality/encoding exit 0, #4 byte-
  identica. Veredicto + MSG rr=true commiteados y pusheados en `45645bd` (`review(TASK-0155): Analista requires
  AC52 hardening`).
- TASK-0155 AC52 rework (2026-06-22): re-verifique sobre Zeus `6369b5c` + protocolo `1cb2b40`.
  Resultado OK/CERRABLE. Clon limpio producto: `npm test` corrida 1 exit 1 por `EACCES 127.0.0.1:5040` en test
  ajeno de auto commit push; corrida 2 exit 0, 48/48. Payloads propios contra guard extraido de `src/server.js`
  cerraron decimal `2130706433`, octal/hex, `0.0.0.0`, externos, sufijos, IPv4-mapped, leading-zero, userinfo
  confusion, percent/sufijo, out-of-range, HTTPS no-localhost y protocolo no HTTP; positivos `localhost`,
  `https://localhost`, `127.0.0.1`, `127.0.0.5`, `127.255.255.255`, `[::1]` pasan. Gates protocolo: validate con
  secretos exit 0, validate sin secretos en clon limpio exit 0, drift 0 `up_to_seq=1197`, neutrality/encoding exit
  0, #4 byte-identica. Veredicto + MSG rr=true commiteados en `4cf8fa2` (`review(TASK-0155): Analista OK AC52
  rework`). Residual: AC52 no es sandbox de red; uso vivo sigue GO/ceremonia aparte.
- TASK-0156 (worker Extractor producto + firma Ed25519 + default qwen3-vl:4b-instruct): OK/CERRABLE sobre Zeus
  `560a226150a2b6237bbf00a84fd6dca07504ba09` + protocolo `f4eb93b36f4e04d4a0aa2889271a25e66307791d`.
  Clon limpio producto `npm test` 48/48 exit 0. Payloads propios por comportamiento contra servidor temporal:
  firma valida 200; firma ausente, bytes alterados, payload_hash alterado, worker mismatch, algorithm mismatch,
  payload almacenado alterado tras firmar y key atacante en `public_key_pem` autodeclarado -> todos 409. Registro
  `Extractor` vive en `extractors.config.json` del PRODUCTO; no aparece en `protocol.config.json`; #4 byte-identica.
  Privada default `.secrets/extractor_ed25519_private.pem` queda fuera del repo y `.secrets/` esta gitignored; no
  hay private key PEM commiteada. Gates protocolo: validate con secretos exit 0, validate sin secretos en clon
  limpio exit 0, drift 0 `up_to_seq=1213`, neutrality/encoding exit 0. Veredicto + MSG rr=true commiteados y
  pusheados en `63b8740` (`review(TASK-0156): Analista OK firma PII`). Residual no bloqueante: si el operador
  decide mover la privada a rutas de producto `secrets/` o `.protocol-secrets/`, anadirlas al `.gitignore` del
  producto antes de colocar la clave. Uso vivo del VLM sigue GO aparte con pasada corta sobre config viva.
- TASK-0157 (Intake v3 file-mode + tarjetas + auto-push ergonomico AC55-AC58): OK/CERRABLE sobre Zeus `2afc944`
  + protocolo citado `2e72cf9` (HEAD de emision `7172e75`). Clon limpio producto `npm test`: primera corrida
  timeout local a 124s, segunda exit 0 50/50; targeted suite de AC55-AC58 + file ingestion + local-vlm +
  candidate review + auto-push exit 0 8/8. Verifique que AC58 no es segundo escritor: `runSubmitIntent` llama
  primero a `runtime/submit_intent.py` y el auto-push commitea solo paths de output gobernado con `git add --`
  + `git commit --only -- <paths>`; dirty/staged ajeno no entra y non-fast-forward da error sin overwrite.
  Versionados `commit-push.config.json` y `file-ingestion.config.json` siguen `enabled:false`; runtime overrides
  y `.secrets/` siguen gitignored. Carry AC52 loopback y AC43/AC16 PII pasan. Gates protocolo con/sin secretos,
  drift 0, neutralidad/encoding y #4 byte-identica verdes. Veredicto + MSG rr=true commiteados y pusheados en
  `85f70d6` (`review(TASK-0157): Analista OK egress PII`). Residuales no bloqueantes: auto-push es egress real a
  `origin` si operador activa override; PII sigue best-effort estructural; scan estatico no es sandbox.
- TASK-0158 (SQL Server read-only backend vivo + s9 server-side): CAMBIO-REQUERIDO sobre protocolo `61dc165`
  (veredicto commiteado y pusheado en `a1537c6`). Clon limpio protocolo: golden connector 8/8 exit 0,
  validate exit 0, neutrality/encoding exit 0, drift 0 `up_to_seq=1255`; clon limpio Zeus HEAD local `2afc944`
  `npm test` 50/50 exit 0 (no habia commit de producto citado para esta tarea). PASA: artefacto s9 secret/PII-free,
  off-by-default, clasificador delante del backend, sin escrituras ledger/eventos, egress solo `pymssql.connect`
  a `SQLSERVER_HOST`. BLOQUEO: el DML default del s9 es `UPDATE sys.objects SET name = name WHERE 1 = 0` y el
  artefacto registra error `259`, compatible con rechazo de actualizacion de catalogo del sistema, NO prueba
  permiso DML denegado sobre una tabla/probe ordinaria. Pedi re-ejecutar s9 con INSERT/UPDATE falsable y artefacto
  saneado que distinga permission denied de rechazo por catalogo antes de cerrar/flippear uso vivo.
- TASK-0158 v2 (rework s9): CAMBIO-REQUERIDO otra vez, commiteado y pusheado en `9b28efd`. Ancla protocolo
  `90eea65`, rework `31e0f23`, producto clone limpio `2afc944` `npm test` 50/50 exit 0. Gates protocolo con/sin
  secretos exit 0, neutralidad/encoding/golden 8/8 exit 0, #4 byte-identica. Hallazgo: re-ejecute s9 vivo con env
  gitignored del operador y config temporal fuera del repo (`C:/tmp/analista-s9-connectors.runtime.json` habilitando
  solo `sqlserver_readonly`); `s9_verify_live.py` exit 1 porque el DML no fue rechazo de permisos: `DELETE FROM
  catalog.records WHERE 1 = 0` devolvio `ProgrammingError` code `208` (objeto inexistente), `server_rejected=false`,
  `rejection_kind=other_server_rejection`; DDL si dio `262 permission_denied_on_principal`. El artefacto commiteado
  que declara DML `229` no es reproducible contra el env vivo actual. Pedi no cerrar ni flippear hasta usar una
  tabla/probe ordinaria existente o `SQLSERVER_S9_DML_SQL` gitignored reproducible que demuestre DML `229`, no `208`.
- TASK-0158 v3 (2026-06-23): OK/CERRABLE, commiteado y pusheado en `aee5deb`. Ancla protocolo REVIEW `8af01fd`,
  rework citado `4754a04`, producto Zeus sin commit nuevo citado pero gateado en clon limpio `2afc944` con `npm test`
  50/50 exit 0. Re-ejecute s9 vivo con env gitignored del operador y config temporal fuera del repo: exit 0, SELECT
  row_count=1, DML contra tabla ordinaria descubierta en runtime devuelve `229 permission_denied_on_principal`, DDL
  devuelve `262 permission_denied_on_principal`. Gates protocolo con/sin secretos exit 0, drift 0 up_to_seq=1278,
  neutralidad/encoding exit 0, golden connector 8/8 exit 0, #4 byte-identica. Residual: s9 prueba el principal y DB
  viva actuales; el flip read-only sigue siendo accion del Arquitecto bajo GO, no mia.
- TASK-0159 (2026-06-23): OK/CERRABLE, veredicto commiteado y pusheado en `3a396cc`. Ancla producto
  `bc8346db385d53d68ce0e92d89307e1e6796bb5b`; protocolo de instruccion `036114c`; handoff/checker citaba
  `2359251`. Clon limpio producto `npm test` 52/52 exit 0. Payloads propios: loopback-only acepta
  `127.0.0.1`/`https://localhost` y rechaza decimal/octal/hex/external/suffix/userinfo/IPv4-mapped/HTTPS-IP;
  extraccion deterministic-local crea candidatas solo en store OS tmp, no en `TASK_INDEX`; aprobacion sin
  `piiReviewed` da 409; aprobacion con PII estructural redacta NIT/SQL; `actorId`/`intents`/route state y execute
  no permitido no devuelven 200. UI extraida de `public/app.js`: nota usa extensiones reales, completed-empty/failed
  renderizan error rojo y candidato HTML queda escapado. Gates protocolo con/sin secretos exit 0, drift 0
  `up_to_seq=1304`, neutralidad/encoding exit 0, #4 byte-identica antes del veredicto. Residuales: PII best-effort,
  loopback guard no es sandbox, razones de error futuras deben seguir server-bounded.
- TASK-0160 (2026-06-23): OK/CERRABLE, veredicto commiteado y pusheado en `0801c12`. Ancla producto `a3c5f26`
  + protocolo `d8892f8`. Clon limpio producto `npm test` 52/52 exit 0; targeted behavior file-ingestion/local-vlm/
  candidate-approval exit 0. Payloads propios contra servidor temporal + protocolo clonado: `piiAcknowledged=false`
  al extraer da 409, `acceptanceIntent=""` con PII ack da 200 y crea `TASK-EXTRACT-*` triage/ready, extractor sin
  consentimiento da 409, con consentimiento da 200 y no mete candidatas en `TASK_INDEX`, aprobacion de candidata sin
  `piiReviewed` da 409. Targeted test cubre candidata firmada sin `acceptanceIntent` -> 400. Gates protocolo con/sin
  secretos exit 0, drift 0 `up_to_seq=1324`, neutralidad/encoding exit 0, #4 `protocol.config.json` byte-identica.
  Residuales: PII best-effort; loopback guard no es sandbox; mi payload deterministic-local devolvio extraction
  failed/cero candidatas pero probo no-ledger y consentimiento.
- TASK-0161 (2026-06-23): OK/CERRABLE, veredicto commiteado y pusheado en `92d5f1a`. Ancla producto
  `109d03976e526ffe01aad512756d22aa1a9a892f` + protocolo `e02df27467d3be37870a5b0e2aa1131fb56005a6`.
  Clon limpio producto: primera corrida `npm test` timeout exit 124 a 184s; segunda exit 0 54/54. Targeted behavior
  `auto commit push treats|local-vlm extractor reports|candidate review stays|local-vlm extractor is loopback-only`
  exit 0 4/4. Payload propio black-box contra server temporal + protocolo clonado: re-submit del mismo archivo
  devuelve `noop=true`, `landed=true`, `primaryOutputId` estable, sin commit/push nuevo (HEAD y remote iguales);
  extraccion posterior sigue gobernada y `networkEgress=loopback-only`; HTTP 503 con cuerpo secret/PII/SQL queda
  saneado a `local-vlm endpoint returned HTTP 503`; timeout 600000ms + `keep_alive=45m`; matriz loopback rechaza
  decimal/octal/hex/externos/sufijos/IPv4-mapped/leading-zero y acepta localhost/127.* /[::1]/https localhost.
  Gates protocolo con/sin secretos exit 0, drift 0, neutralidad/encoding exit 0. Residuales: PII best-effort,
  loopback-only no es sandbox; primer `npm test` fue timeout local pero repeticion completa verde.
- TASK-0162 (2026-06-23): OK/CERRABLE, veredicto commiteado y pusheado en `962eb6b`. Ancla producto
  `1b97c6bb39e54de8e28301f5885f8347385c8813` + protocolo `b3f8b7c4fc241cc9665a2b9a578840b990b454cb`.
  Clon limpio producto `npm test` exit 0 55/55; targeted `candidate review stays outside the ledger|AC69-AC71`
  exit 0 2/2. Payload propio black-box contra server temporal + protocolo clonado: approve sin `piiReviewed`
  devuelve 409; approve con PII revisada devuelve 200 por `submit_intent`; discard devuelve 200; candidatas
  `CAND-*` no entran en `TASK_INDEX`; requisito publicado redacted; drift false. Gates protocolo con/sin secretos
  exit 0, drift 0 `up_to_seq=1374`, neutralidad/encoding exit 0, #4 byte-identica antes del veredicto. Residuales:
  PII best-effort; AC69/AC70 no son pixel-perfect; store no-ledger depende de firma/provenance ya cubierta.

## Lecciones no-obvias (persisten)
- **CLON LIMPIO + EXIT CODE + corro la suite YO (no asumo al maker).** Reproduzco en un tmp en C:, no in-place.
  Windows: `core.autocrlf=true` reescribe LF->CRLF en el clon -> tests LF-only (regex `\n`) rompen aunque el
  repo este "bien"; el fix es `.gitattributes eol=lf`. Probar POR COMPORTAMIENTO (forjar payloads, bare-remote
  real, inyectar literal en una copia) destapa lo que un test STRING-MATCH no atrapa.
- **Guard de no-egress / anti-impersonacion (patron):** un scan estatico necesita (a) TODO src/** (no un solo
  archivo), (b) `import(` DINAMICO, (c) bare network-modules + call sites (`.connect/.request/.get`), (d)
  control positivo POR familia. ALLOWLIST > denylist (un denylist de nombres nunca es completo). Limite
  inherente honesto: ningun scan estatico atrapa eval/ofuscacion/cliente-no-listado -> declararlo como
  residual + reco allowlist, NO sobre-afirmar "no hay egress".
- **Neutralidad del core:** identidades de instancia (Operador/Arquitecto/Codex) van al PRODUCTO (server Zeus),
  NUNCA al core neutral (runtime). El scan de neutralidad ahora deriva los nombres del agent_registry y los
  marca en runtime/*.py salvo una whitelist legacy nombrada (deuda declarada, no silenciosa).
- **Anti-impersonacion:** el front es CLIENTE; el servidor NUNCA confia en `payload.actorId`/`payload.intents`;
  builder server-side + execute solo para acciones permitidas (hard-gate set cerrado) + prueba negativa
  permanente. Agregar una 2a accion no debe erosionar el bound (sigue siendo un Set cerrado).
- **PII:** la redaccion estructural es por PATRONES best-effort (NIT/razon social/SQL/email/telefono), NO
  cero-PII garantizado; declararlo honesto; DEF-PII (TASK-0118) sigue el gate de citabilidad. El gate HUMANO
  de PII al aprobar candidatas es DURO (piiReviewed -> 409).
- **npm test flake en arranque frio:** la 1a corrida del clon puede dar 1 fallo por timeout (los tests
  behavioral spawnean server+git+python); correr 2-3 veces y reportar la distribucion, no asumir el 1er run.
- **maker != checker REAL / identidad:** NO asumo otros roles (me dieron el prompt del DISENADOR -> lo rechace;
  cambio de firmante = re-genesis gobernado). Aplico la lente a MI: si me equivoco, RETRACTO (CR1 Carril A
  "event_auth no existe" era falso -> top-level; lo corregi yo mismo).
- **NARRACION MINIMA = REGLA DURA (DECISION-0036, que YO revise).** CERO narracion intra-ejecucion: NADA de
  "Leo X", "Verifico Y", "Escribo Z", "Confirmo", "Reprogramo" antes/despues de tool calls. Encadenar las
  herramientas EN SILENCIO; el razonamiento de proceso va al canal interno, NO al output. Output = UN solo
  reporte final autocontenido. Carve-out = contenido sustantivo (mi analisis PASA/CAMBIO/RIESGO, veredictos)
  y UNA pregunta de bloqueo. El operador me lo marco DOS veces con enfasis (2026-06-15) tras yo narrar paso
  a paso en las pasadas TASK-0100/0095. Ironia: en mi propia pasada 0036 dije "afilar wording es
  necesario-no-suficiente; el binding constraint es cumplimiento" -> aplicalo a mi mismo. Reincidir = anomalia
  notificable (DECISION-0018).
- **Canal ASCII estricto (DECISION-0012):** mailbox/** y state/*.json SOLO ASCII; scan_encoding.py
  deja el gate rojo ante em-dash/n-tilde/flechas/comillas tipograficas. Docs de protocolo si UTF-8.
- **Compact-msg:** requires_response:true EXIGE campo question (o baja a false); validate_collaboration_state
  lo trata como error duro.
- **Entrega completa antes de aseverar (anti-colision #6 / DECISION-0018):** no aseverar entrega cuyo
  soporte sigue sin commitear; la asercion en el canal debe ser verdadera en el repo en ese momento.
  El commit es del escritor unico; yo dejo la entrega lista, ASCII, bien formada, y verifico mi propio
  mensaje antes de cerrar. (Estas 3 me costaron un cierre manual del arquitecto en la pasada Fase 0.)
- **maker != checker REAL:** la convergencia independiente con Codex (deltas SOTA) fue justo la senal
  3-0 que buscaba el operador; coordinar es legitimo SOLO despues de entregar mi voz.

## Leccion coordinacion (2026-06-15)
- **Descoordinacion = DOS sesiones Claude-arquitecto concurrentes en el MISMO working tree.** Sintoma: el
  operador dijo "tienes mensaje" / "Claude espera tu veredicto" pero mi mailbox/open no tenia inbound. Causa:
  una sesion arquitecto hizo el cierre TASK-0095 (2/3) + promo TASK-0096 (3/3); la otra tenia vista stale y
  creia que faltaba mi verdict. NO era verdict perdido ni mensaje extraviado: vista desincronizada entre
  sesiones. Yo reconcilie contra el ledger (mis 2 pasadas entregadas/archivadas, v1.9.1/v1.9.2) y deje un
  sync con pregunta directa en vez de inventar un veredicto -> correcto. El operador consolida a UNA sesion.
  Aprendizaje: ante "falta tu X" sin inbound real, reconciliar contra git/ledger y PREGUNTAR, no asumir.
- **DOBLE SESION ANALISTA tambien (2026-06-15, TASK-0096):** aparecio un 2do mensaje verdict de TASK-0096
  bajo MI identidad (Claude-analista) escrito por OTRA sesion analista concurrente; ambos CONVERGEN en
  CONCURRO y ambos verificaron por su cuenta. Riesgo: doble-conteo de voz (maker!=checker quiere UNA voz
  identificable; dos CONCURRO de la misma rol NO son 2 corroborantes). Mi manejo honesto: NO crear un 3er
  verdict; reconcilie en mi propio mensaje que ambos son la MISMA voz = contar UNA vez; el verdict unanime
  hace seguro cerrar, pero la atribucion/identidad de sesion la consolida el operador. No reclamar "mi
  mensaje es el unico real" (la otra sesion es igual de legitima); honestidad por encima de defender autoria.

## Estado vigente (VERIFICAR al arrancar)
- FIRMA = "Analista" (sin prefijo "Claude-"; orden operador 2026-06-15). Area = personal/Analista/.
- **#4 ON EN EL VIVO** (chain + agent_signatures + anchor + event_auth), `enforce`+`authoritative` ON, #3 cost
  ON. **Epoca/protocol_version 1.14.0 PINNED** (bump => re-genesis-boundary). Protocolo HEAD a veces 1 commit
  ADELANTE de origin (handoff sin pushear, esperado in_review). DECISION-0046 (replay secret-independiente):
  validate exit 0 con Y sin secretos desde clon limpio.
- **Proyecto-front Zeus-protocol (DECISION-0049/0050):** producto en repo separado D:\Agentes\Zeus\Zeus-protocol
  (HEAD suele ir adelante de origin). Gobernanza/SPEC-0086/handoffs en Area_comun=dataset atestado. Serie
  INTAKE / carga-por-archivo v2 (DECISION-0053 mailbox_archive, 0055/0056 file-ingestion). Codex maker /
  Arquitecto checker / yo voz adversarial; DECISION-0056 exige mi OK para cerrar fase. Ultimo: Fase C
  (TASK-0152, agente extractor + AC45) re-verificada OK/CERRABLE; el Arquitecto cierra. USO VIVO del extractor
  = GO APARTE del operador (ventana de modelo real), fuera de los cierres de fase.
- Gates de cada pasada (verifico yo): npm test verde en clon limpio (sin flake, correr 2-3x), validate exit 0
  CON y SIN secretos, drift 0, neutralidad+encoding 0, #4 byte-identica (config/genesis/keys sin cambio).
- Operador maneja monitoreo via "cron" (ScheduleWakeup): "cancela cron" lo detiene; una activacion rezagada
  tras el cancel NO se reprograma. El flujo tipico: el operador me dice "tienes mensaje" -> reviso
  mailbox/open inbound a Analista (REVIEW/REVISAR del Arquitecto) -> pasada adversarial -> entrego.
- (Historico: trio off-pilot v1.9.1-1.9.3, Carril A activacion #4, satelite protocol_research DECISION-0035 --
  ya superados; #4 paso de OFF a ON en el vivo entre junio 14 y 20.)

## Ultima pasada (2026-06-24)
- TASK-0166 fix3 a1d4491 (2026-06-24): CAMBIO-REQUERIDO, veredicto commiteado en `2279361`
  (`review(TASK-0166): Analista requires action type guard`). Ancla producto
  `a1d4491fc00f86ffdb3c3fce73de0d6ca9d366ae`; instruccion REVIEW en protocolo
  `07c3ad622cbefe04120cd897513af3b8113123ec` cita protocolo `9f3cded58e9305bd7926a46c54092f85286d3c0a`.
  Clon limpio producto `npm test`: corrida 1 exit 1 por flake de readiness local-vlm (`listening` impreso pero
  `/healthz` no listo a tiempo), corrida 2 exit 0, 64/64. Payloads propios contra servidor temporal + protocolo
  clonado en `9f3cded`: `agentId` array single, objeto, numero, bool, null, array anidado, leading space, ZWJ,
  control char, duplicate-key ultimo malo y extra key -> 400 sin heartbeat; heartbeat ausente/stale/futuro -> dormant;
  happy exact -> 200/alive. SLIP nuevo bloqueante: `{"agentId":"Codex","action":["activate"]}` devuelve 200, crea
  `Codex.heartbeat` y deja `Codex.status=alive`, porque `applyRuntimeControlAction` aun hace
  `ascii(stripControl(input?.action || "")).trim()` y `String(["activate"]) == "activate"`. `action` objeto devuelve
  500 TypeError publico. Pedido: `typeof input.action === "string"` antes de coercion + tests negativos permanentes
  para array/object. Gates protocolo: validate con secretos exit 0; validate secretless en clon exit 0; drift vivo 0
  `up_to_seq=1617`; neutralidad/encoding exit 0; #4 byte-identica sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- TASK-0166 fix cab246c (2026-06-24): CAMBIO-REQUERIDO, veredicto commiteado en `228c70e`
  (`review(TASK-0166): Analista requires runtime agentId type guard`). Ancla producto
  `cab246cc48facb8b8dc6af52ca5a80ac4eddf766` + protocolo citado por instruccion `a2ed687`. Clon limpio producto
  `npm test` exit 0, 64/64. Payload propio contra server temporal + protocolo clonado en `a2ed687`: heartbeat
  futuro +10 anos -> dormant; stale 10 min -> dormant; leading/trailing space, control chars, lowercase, non-ASCII,
  ZWJ e internal-space -> 400 sin heartbeat; control positivo `Codex` exacto -> 200/alive. SLIP nuevo bloqueante:
  JSON `{ "agentId": ["Codex"], "action": "activate" }` devuelve 200, crea `Codex.heartbeat` y deja
  `Codex.status=alive`, porque `sanitizeRuntimeControlAgentId` hace `String(value || "")` antes del lookup y
  `String(["Codex"]) == "Codex"`. Pedido: type check estricto `typeof value === "string"` antes de coercion/lookup
  + test negativo permanente `agentId: ["Codex"]`. Gates protocolo: validate con secretos exit 0; validate
  secretless en clon `a2ed687` exit 0; drift vivo 0 `up_to_seq=1591`; neutralidad/encoding exit 0; #4
  `protocol.config.json` byte-identico durante pasada sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- TASK-0165 v4 (2026-06-24): OK/CERRABLE, veredicto commiteado en `5ca009c`
  (`review(TASK-0165): Analista OK v4 thread PII`). Ancla producto `ea7304f` + protocolo
  `8a5c90c6ae7152dd512b86a70f2ecdac14eba096`. Clon limpio producto `npm test`: primera corrida timeout local
  exit 124 a 184s; segunda corrida exit 0, 61/61. Test nuevo v4 honesto: `assert.doesNotMatch` por literal exacto
  y `assert.match` para tokens `[PHONE-REDACTED]` / `[ADDR-REDACTED]`. Payload propio `buildAgentThread` +
  `redactRequirementText`: `Tel +1 (415) 555-2671`, `Tel (+57) (300) 555-7788`, `telefono (601) 555-7788 ext 9`,
  `Phone +44 (020) 5555 7788`, `Cra 7 # 12-34 Bogota`, `Cl 45 # 7-89 Medellin`, `KR 7 12 34 Bogota`,
  `Carrera 11 # 22-33 Cali`, `Calle 10 No 20-30 Piso 3`, `Av. Siempre Viva 742 piso 2` no filtran literales;
  tokens phone/addr presentes. Carry AC17 `mailbox-send` contra servidor temporal: `noPiiAck=409`,
  `badAgent=400`, `actorInjection=400`, `intentsInjection=400`, `routeState=400`. Gates protocolo con/sin secretos
  exit 0, drift 0 `up_to_seq=1535`, neutralidad/encoding exit 0, #4 `protocol.config.json` byte-identico sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Residuales no bloqueantes: nombre propio
  libre y fragmentos sueltos tipo `#45-67` quedan para DEF-PII (TASK-0118); PII best-effort estructural.
- TASK-0165 v3 (2026-06-24): CAMBIO-REQUERIDO, veredicto commiteado y pusheado en `037877d`
  (`review(TASK-0165): Analista requires thread PII v3 hardening`). Ancla producto `41bf1a2` +
  protocolo `a51d0c7a158d766c77b6827fd89fdb460312c78d`. Clon limpio producto `npm test` exit 0, 60/60.
  Test nuevo honesto: asierta ausencia de literal y presencia de tokens, no solo token-presence. AC17 carry
  en servidor temporal: `noPiiAck=409`, `badAgent=400`, `actorInjection=400`, `intentsInjection=400`,
  `routeState=400`. Payloads propios `buildAgentThread`: email, telefono simple, doc etiquetado, cuenta/IBAN y
  direccion literal pasan; pero `Tel +1 (415) 555-2671`, `Tel (+57) (300) 555-7788`, `Cra 7 # 12-34 Bogota`,
  `Cl 45 # 7-89 Medellin` y `KR 7 12 34 Bogota` quedan visibles completos. Gates protocolo con/sin secretos exit
  0, drift 0 `up_to_seq=1529`, neutralidad/encoding exit 0, #4 byte-identica sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Residual nombre-propio libre no usado como
  bloqueo; los slips son familias tel/direccion tratables por patron.
- TASK-0165 v2 (2026-06-24): CAMBIO-REQUERIDO, veredicto commiteado y pusheado en `450fada`
  (`review(TASK-0165): Analista requires thread PII hardening`). Ancla producto `cf13e7f8ad570f3e1ee375df4491bc50a8faab4b`
  + protocolo `e1c2666e0140ecf4e12916bef2181093132f9c32`. Clon limpio producto `npm test` exit 0, 59/59.
  Execute propio `mailbox-send` contra servidor temporal + protocolo clonado: HTTP 200/applied true, MSG generado
  `requires_response:false`, `operator_directive:true`, sin raw NIT/razon social, y `validate_collaboration_state.py
  --root <tmp>` exit 0. Payloads negativos: `noPiiAck=409`, `badAgent=400`, `actorInjection=400`,
  `intentsInjection=400`, `routeState=400`. Gates protocolo con/sin secretos exit 0, drift 0 `up_to_seq=1523`,
  neutralidad/encoding exit 0, #4 `protocol.config.json` byte-identico sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Bloqueo: el hilo read-only sigue filtrando
  PII fuera de NIT/razon social/SQL; `buildAgentThread` deja visibles email, telefono, documento, nombre propio,
  cuenta numerica larga y direccion cuando no hay SQL que los tape por accidente. Pedi devolver a Codex para unificar
  `redactRequirementText` con la familia del backend y anadir controles positivos por familia.

## Pasada anterior (2026-06-23)
- TASK-0165 (2026-06-24): CAMBIO-REQUERIDO, veredicto commiteado y pusheado en `8e163cf`
  (`review(TASK-0165): Analista requires mailbox prompt hardening`). Ancla producto `1493f86` + protocolo
  `7d1199020a4245ee7d743ac8623449bc3d273a5a`. Clon limpio producto `npm test`: corrida 1 exit 1 por fallo
  ajeno local-vlm `127.0.0.5 must be accepted`, corrida 2 exit 0 58/58. Payloads propios contra servidor temporal:
  dry-run `mailbox-send` exit 200, `noPiiAck=409`, `badAgent=400`, `actorInjection=400`, `intentsInjection=400`;
  actor server-side `Arquitecto`, `directLedgerWrites:false`, transaction solo claim acquire/release file-scoped y
  `mailboxWrites`. SLIP bloqueante 1: el MSG generado tiene `requires_response: true` sin `requested_action` ni
  `question`; al materializarlo en copia limpia, `validate_collaboration_state.py --root <tmp>` sale 1. SLIP
  bloqueante 2: `public/app.js::redactRequirementText` usado por `buildAgentThread` no redacta email/telefono/
  documento/nombre propio aunque el backend `redactPublicText` si cubre esa familia; payload propio dejo visibles
  `persona@example.com`, `+57 300 123 4567`, `cedula 123456789` y `Juan Perez`. Gates protocolo con/sin secretos
  exit 0, drift 0 `up_to_seq=1514`, neutralidad/encoding exit 0, #4 `protocol.config.json` byte-identico sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- TASK-0163 (ledger-busy friendly message AC72): OK/CERRABLE. Producto `d1de0c1`, protocolo ancla
  `e668cd0`; veredicto commiteado y pusheado en `c270ee4` (`review(TASK-0163): Analista OK ledger busy`).
  Clon limpio producto `npm test` exit 0, 57/57; targeted behavior AC72/no-bypass/file/candidate/intake exit 0,
  6/6. Payloads propios sobre funciones extraidas: 6 familias de contencion (`claim acquire overlaps active
  claim`, `overlaps active claim`, `active claim`, `ledger busy`, `concurrent ledger`, `contention`) dieron
  body saneado `{error:"ledger-busy", code:"ledger-busy", retryable:true}` y front `Canal ocupado, intente mas
  tarde`; 3 errores tecnicos con traceback/comando/secret/path dieron `{error:"submit_intent failed"}` sin fuga.
  Gates protocolo con/sin secretos exit 0, drift 0 `up_to_seq=1388`, neutralidad/encoding exit 0, `protocol.config.json`
  byte-identico sha256 `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`.
  Residual no bloqueante: matcher amplio de "active claim" puede clasificar un error ambiguo como ledger-busy;
  no filtra argv/traceback ni abre bypass, solo reduce diagnostico publico.
- TASK-0164 (2026-06-23): CAMBIO-REQUERIDO, veredicto commiteado y pusheado en `e3ada6b`
  (`review(TASK-0164): Analista requires torn write hardening`). Ancla protocolo implementacion `745a678`,
  instruccion `346dd00`, producto Zeus `4faacd1`. Clon limpio Zeus `npm test` exit 0, 57/57; protocolo limpio
  row_scoped_claim_cases 8/8 exit 0, intent_tx_cases 8/8 exit 0, validate sin secretos exit 0; repo vivo validate
  con secretos exit 0, neutralidad/encoding exit 0, chain/agent_signatures/anchor validos y drift 0 `up_to_seq=1435`,
  `protocol.config.json` byte-identico sha256 `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`.
  PASA concurrencia normal N=8: 8 procesos `submit_intent.py --intents` sobre 8 tareas/claims distintos -> todos
  returncode 0, 17 eventos esperados/leidos, prev_hash lineal, drift 0, todas las tareas in_progress. SLIP nuevo:
  al simular cola JSON parcial en `runtime/state/events.jsonl` (`{"seq":999`) y luego ejecutar `submit_intent`, la
  llamada devuelve `applied:true`/`event_seq=2`, pero `read_jsonl_torn_safe` sigue leyendo solo el prefijo (1 evento),
  el nuevo evento queda invisible pegado a la cola rota, `TASK_INDEX` no cambia y `validate_chain`/drift quedan verdes
  sobre el prefijo. Requiere hardening: bajo lock detectar/truncar cola rota o fallar duro antes de reportar exito.
- TASK-0164 v2 (2026-06-24): CAMBIO-REQUERIDO, veredicto commiteado en `78d4868`
  (`review(TASK-0164): Analista requires middle torn guard`). Ancla protocolo `232dcc3`, fix2 `92ece27`,
  producto Zeus `4faacd1`. Clon limpio Zeus `npm test`: corrida 1 exit 1 por AC50 readiness (`server did not
  become ready` aunque imprimio listening), corrida 2 exit 0 57/57. Protocolo limpio: row_scoped_claim_cases 8/8,
  intent_tx_cases 9/9, validate sin secretos exit 0; repo vivo validate con secretos exit 0; drift 0, chain valida,
  neutrality/encoding exit 0, #4 `protocol.config.json` byte-identico sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. PASA tail final reparado y tail+concurrencia:
  dos writers concurrentes tras cola parcial -> returncodes [0,0], un `log_repair`, 5 eventos visibles, prev_hash
  lineal, drift false. SLIP nuevo: torn en medio seguido por linea JSON valida posterior (`before` + partial broken
  + `after`) hace que `truncate_torn_jsonl_tail` trunque desde el prefijo y DESCARTE la linea valida `after`.
  Incumple "truncar SOLO la ultima linea parcial" y "no descartar eventos validos"; pedir fail-hard o cuarentena
  cuando la linea invalida no sea la ultima linea no vacia.
- TASK-0164 v3 (2026-06-24): OK/CERRABLE, veredicto commiteado y pusheado en `d3fa46a`
  (`review(TASK-0164): Analista OK mid torn v3`). Ancla protocolo citada `90958cf`, fix3 `434b2e9`, producto Zeus
  `4faacd1` (la instruccion v3 no cito commit de producto nuevo; use el ultimo anclado para TASK-0164). Clon limpio
  Zeus `npm test` exit 0, 57/57; protocolo limpio row_scoped_claim_cases 8/8, intent_tx_cases 10/10, validate sin
  secretos exit 0; repo vivo validate con secretos exit 0; neutrality/encoding exit 0; drift vivo 0 `up_to_seq=1486`;
  #4 `protocol.config.json` byte-identico sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
  Payloads propios: middle torn JSON + valid-after -> falla cerrado, bytes intactos, valid-after preservado, evento
  nuevo ausente; middle non-object `[]` + valid-after -> idem; tail-torn final -> `applied=true`, `log_repair`,
  evento visible, chain valid, drift false; tail-torn + 4 writers concurrentes -> returncodes `[0,0,0,0]`, un solo
  repair, 10 eventos visibles, prev_hash lineal, drift false; mid-torn + 2 writers concurrentes -> returncodes
  `[1,1]`, error de integridad, bytes intactos, sin claims nuevos. Residual: `read_jsonl_torn_safe` sigue leyendo
  prefijo ante corrupcion media, pero el writer `submit_intent` ya no cierra falso porque falla cerrado bajo lock.
