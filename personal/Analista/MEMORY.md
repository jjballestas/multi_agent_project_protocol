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
