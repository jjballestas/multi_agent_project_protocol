---
spec_id: SPEC-0086
task_id: TASK-0124
type: product
status: accepted
linked_decisions:
  - DECISION-0049
  - DECISION-0029
  - DECISION-0047
  - DECISION-0048
created_at: 2026-06-19
updated_at: 2026-06-19
author: Arquitecto
---

# SPEC-0086 - Proyecto-front MVP (UI single-operator) para operar/observar el protocolo

## Context

DECISION-0049: el proyecto-front (UI single-operator) es el proyecto PRIMARIO de tesis y T0. Repo producto
`D:\Agentes\Zeus\Zeus-protocol` (codigo); gobernanza (esta SPEC, tasks, handoffs) en `Area_comun` (atestada
#4 = dataset publicable). Insumos: `D:\Agentes\Zeus\Zeus-protocol\design\front_requirements.html` (RF/RNF) +
`front_pipeline.html` (etapas). El diseno UI de Claude Design (`design\interface\`) alimenta las tareas de
UI; NO bloquea el resto del SPEC. maker=Codex, checker=Arquitecto, de a una etapa.

## Principio rector (RNF-1/RNF-2)

El front **observa** el protocolo por **patron read-only sobre el CANONICO** (objetos git / origin, NO el
working tree volatil que se re-trunca) y **opera SOLO via `submit_intent`** (escritor unico). NUNCA escribe
estado/ledger directo ni bypassa gates/#4/drift. Toda escritura = transaccion atomica idempotente por
`submit_intent`. PII-free; canal ASCII para lo que escribe al protocolo.

## Scope (MVP-T0 = RF-1..RF-10)

- **Observar (read-only):** RF-1 dashboard (TASK_INDEX backlog, CLAIMS, PROJECT_STATE, version/epoca, drift
  verde/rojo), RF-2 mailbox (open/answered/archived, requires_response), RF-3 artefactos navegables
  (decisiones/specs/tasks/handoffs/reports por id + *_refs), RF-4 ledger #4 / procedencia (timeline
  atestado: seq, actor, firma verificada, prev_hash, anclaje; badge atestado).
- **Operar (gobernado via submit_intent):** RF-5 acciones SDD (crear DECISION/SPEC/task, abrir handoff,
  enviar mailbox), RF-6 GO del operador (aprobar / responder requires_response), RF-7 disparar run de agente
  (caps de autonomia supervisada), RF-8 disparar validacion (validate/gates -> drift/cadena/firmas/anclas/
  scans).
- **N-agente (RF-9, MVP-min):** ver el roster (agent_registry + tool_policy + llm_cli_presets); alta/baja/
  edicion de agente o modelo = **flujo de re-genesis-boundary gobernado** + provisioning de clave (A2), NO
  un toggle (ceremonia gobernada; el conjunto de firmantes queda pinned por el genesis). El MVP solo
  EXPONE/prepara el flujo; la ceremonia es gateada por el operador.
- **Kickoff (RF-10):** lanzar un proyecto nuevo bajo `D:\Agentes\Zeus\` (su primer handoff gobernado = su T0).
- **Intake gobernado de requisitos (RF-14; DECISION-0051):** el operador monta una historia/requisito en un
  wizard (titulo, narrativa, intencion de aceptacion en lenguaje llano, proyecto destino) y la emite como
  artefacto GOBERNADO via submit_intent EXECUTE (`task_upsert` de una tarea `type:requirement`, `actorId:
  "Operador"`, idempotente). Es la SEMILLA del pipeline SDD; el Arquitecto la consume para autorar la SPEC
  (handoff explicito). Habilita la PRIMERA superficie de escritura EXECUTE del operador desde el front,
  acotada al intake, con confirmacion visible. Cuelga del patron `governed-action` (un solo writer).

## Out Of Scope (posterior, pull-based, regla 3.4)

RF-11 export del dataset (etapa 4 posterior), RF-12 multi-proyecto rico (etapa 6 MVP-light minimo),
RF-13 coste/observabilidad; **multi-tenant** (RNF-7, su propia DECISION); Fase 4 / discovery. NO meter
producto/dominio en el core neutral.

## Diseno (etapas del pipeline; una a la vez, SDD)

- **Pre-req (floor):** connector **CI** (deny-by-default, DECISION-0048) ANTES del codigo que compila/testea;
  Git ya esta (TASK-0123). Lectura del protocolo por patron read-only (connector / objetos git).
- **Etapa 1 - Andamiaje:** stack web en `Zeus-protocol`; pipeline CI verde (via connector CI); lectura
  read-only del estado/ledger del canonico; esqueleto de navegacion + base de componentes (segun diseno UI).
- **Etapa 2 - Observar (MVP-read):** RF-1..RF-4 sobre el canonico.
- **Etapa 3 - Operar (MVP-governed):** RF-5..RF-8 via `submit_intent` (sin bypass).
- **Etapa 4 (vista) - Atestacion:** RF-4 timeline + estado boundary T0 / sello / manifest (export = posterior).
- **Etapa 5 - Roster N-agente (RF-9):** exponer/preparar el flujo re-genesis-boundary (ceremonia gateada).
- **Etapa 6 - Multi-proyecto (MVP-light):** selector de proyectos bajo Zeus.

## acceptance_criteria

- **AC1 - Read-only sobre canonico.** Las vistas (RF-1..RF-4) leen el estado/ledger del **canonico** (git
  objects/origin), no el working tree; ningun camino de la UI escribe estado/ledger directo. Verificable:
  grep/review = 0 escrituras fuera de `submit_intent`; las vistas funcionan contra un checkout limpio.
- **AC2 - Escritura SOLO via submit_intent.** Toda accion (RF-5..RF-8, RF-10) emite la transicion por
  `submit_intent` (atomica, idempotente, con actor/timestamp); 0 bypass de gates/#4/drift. Prueba negativa:
  intento de escritura directa al ledger desde el front -> rechazado/ausente por diseno.
- **AC3 - Atestacion visible y correcta.** RF-4 muestra seq/actor/firma verificada/prev_hash/anclaje del
  ledger #4; la verificacion de firma coincide con `validate_chain`/`validate_agent_signatures`/
  `verify_anchor`. Drift verde/rojo coincide con `protocol_state_drift`.
- **AC4 - Gobierno / sin bypass (RNF-1).** No existe ruta en el front que altere estado/ledger sin
  `submit_intent`; lecturas read-only; el front no muestra ni almacena secretos (RNF-4); nunca PII al event
  log (RNF-5).
- **AC5 - Integridad de fuente (RNF-2).** Operaciones que escriben corren con disciplina de canonico/clon
  limpio; el front refleja origin, no el working tree volatil.
- **AC6 - Neutralidad / acoplamiento (RNF-6).** El codigo del front vive SOLO en `Zeus-protocol`; cero
  producto en el core neutral / `*.template.*`; el front no escribe el protocolo salvo por `submit_intent`.
  scan_domain_neutrality del core sigue limpio.
- **AC7 - CI verde como gate (RNF-8).** El pipeline CI del producto (via connector CI) corre y queda verde
  como gate de release de cada etapa.
- **AC8 - Roster re-genesis-gobernado (RF-9).** El MVP NO permite alta/baja de agente como toggle; expone el
  flujo y lo encamina por re-genesis-boundary gateado por el operador (RNF-3, DECISION-0047).
- **AC9 - Determinismo / trazabilidad (RNF-9).** Cada accion del operador queda como evento gobernado en el
  ledger (atestado); vistas deterministas (epoca/version/drift).
- **AC10 - Gates del protocolo verdes.** La coordinacion (esta SPEC, tasks, handoffs) en `Area_comun` deja
  `validate_collaboration_state --root .` exit 0 (con y SIN secretos, DECISION-0046), encoding/neutralidad
  limpios, drift 0; el codigo del producto pasa su CI.
- **AC11 - Honestidad de estado regresion-proof (test de COMPORTAMIENTO) [PERMANENTE].** Para TODA pieza del
  front con badges/indicadores derivados de verificacion (chip canonico, atestacion #4, drift, source-state),
  la honestidad no descansa en string-match: existe un **test de comportamiento** que inyecta una
  verificacion-runtime controlada y asevera el render real -- verificacion que FALLA / no-canonico / no
  verificable -> badge **NO-verde** (warn/danger/indeterminate); TODO valido -> verde; payload de texto libre
  -> SIEMPRE redactado. Falla si un refactor repinta verde una verificacion fallida. AC permanente de las
  etapas con UI (4 ya cubierta retro por TASK-0129; 5/6 lo traen de origen). Es la propiedad-tesis (un badge
  que mienta sobre el estado es el pecado capital): nunca verde hardcodeado.

- **AC12 - AC-ROUTING (comportamiento) [PERMANENTE].** Para CADA nav-item del front, un test de comportamiento
  asevera "clic en X -> SOLO el panel X visible (los demas `hidden`/fuera del DOM visible); topbar +
  integrity-band (epoca/drift/atestado/canonico/seq) SIGUEN presentes". Falla si un refactor vuelve a apilar
  las vistas en un solo scroll (regresion-proof de la navegacion; extiende AC11 a la UX). Satisfecho de origen
  por TASK-0131; permanente para toda etapa con UI navegable.
- **AC13 - AC-CONFORMIDAD-DISENO [PERMANENTE].** Las vistas del front EXISTEN, son navegables y cada una
  corresponde a su pantalla del `front_design_brief` (Backlog=kanban con claims+filtro; Projects=selector con
  entity-cards + "+ add project" cableado al kickoff RF-10 gobernado; Ledger #4=vista dedicada). "Verde" pasa a
  significar tambien "coincide con el diseno". (La pantalla Agentes/Roster 4.6 NO cuenta mientras RF-9 etapa5
  este DEFERIDA; la nav lleva 7 vistas a proposito.) Toda etapa con UI sobre un design brief trae de origen un
  AC de conformidad + un test de comportamiento de interaccion (leccion de proceso, runbook).

### Intake gobernado de requisitos (RF-14; DECISION-0051) - AC14..AC17

- **AC14 - Intake -> artefacto gobernado atribuido al Operador, idempotente.** El wizard estructura la
  historia (titulo, narrativa, intencion de aceptacion en lenguaje llano, proyecto destino) y la emite SOLO
  via submit_intent (`task_upsert` de una tarea `type:requirement`, status `proposed`, `author/owner:
  Operador`). Test de comportamiento: el submit de intake produce el requirement con `author=Operador`;
  re-submit con la misma `idempotency_key` NO duplica. El intake es la SEMILLA, no una SPEC.
- **AC15 - EXECUTE: prueba negativa Y camino feliz con WRITE REAL (DECISION-0052; revisado).** (i) Negativo:
  EXECUTE solo escribe con `confirm:SUBMIT_INTENT`; sin confirm -> rechazo (409), sin escritura. (ii) CAMINO
  FELIZ (write REAL, no mock): test de comportamiento PERMANENTE en CI que demuestra `execute+confirm` ->
  escritura REAL por submit_intent: el requirement aterriza en TASK_INDEX/PROJECT_STATE (proposed,
  author=Operador, relayed_by=Arquitecto), runtime ok con seq, drift 0 despues. El front emite el intake con
  actor RELAY=Arquitecto (firmante pinned) determinado SERVER-SIDE (ver AC19); preview(dry_run) != envio. NO
  basta el dry_run ni el 409: hay que probar que el happy path ESCRIBE de verdad. (Cierra el miss de TASK-0133.)
- **AC18 - Atribucion honesta del relay (RENDER).** Test de RENDER: la UI muestra firmante=Arquitecto y
  `author:Operador`; NINGUN verde/elemento afirma que "Operador firmo". El evento lleva
  `author:Operador`+`relayed_by:Arquitecto`.
- **AC19 - ANTI-IMPERSONACION (prueba negativa PERMANENTE) [CRITICO; DECISION-0052].** El servidor NUNCA
  confia en el cliente para autoria ni forma: se elimina `payload.actorId` y los `payload.intents` crudos;
  cada accion = builder SERVER-SIDE con forma estricta. Test de comportamiento permanente en CI: un POST al
  endpoint EXECUTE que intente (a) un actor distinto, o (b) intents/forma arbitrarios (decision/claim/
  task_status/cualquier forma != requirement-intake) para firmarse como Arquitecto -> es RECHAZADO (no
  construye, no firma, no escribe). Solo la forma exacta del requirement-intake se relaya. Falla si un cliente
  local puede forjar un evento atestado firmado como Arquitecto. Remedia la anomalia DECISION-0018 mergeada en
  Zeus 42e7931.
- **AC20 - Accountability del relay [DECISION-0052].** Firma del relay = ORIGEN+TRANSPORTE, NO aval
  (`endorsement:none`); el aval es la SPEC posterior. Test: un evento relayado NO se cuenta/renderiza como
  AUTORADO ni avalado por el Arquitecto.
- **AC4-byte (refuerzo #4).** El relay/intake no toca `protocol.config.json` (signer set), genesis, keys ni
  `protocol_version`: se aserta BYTE-IDENTIDAD antes/despues (drift 0 es necesario, no suficiente).
- **AC22 - Un intake deja el canonico VERDE [PERMANENTE; DECISION-0018].** Tras un intake EXECUTE, el estado
  resultante pasa `validate_collaboration_state` exit 0: el seed file referenciado por el `task_upsert`
  requirement EXISTE (escrito por el builder) y los claim scopes del relay usan selectores VALIDOS para el
  validador (que reconoce ids de requisito `REQ-[0-9A-Fa-f]+` ademas de `TASK-\d{4}`). Test de comportamiento
  PERMANENTE: tras un intake real, validate exit 0 (regresion-proof; un intake nunca rompe el canonico).
  Remedia la anomalia DECISION-0018 (TASK-0136).
- **AC21 - Reset del formulario + confirmacion inequivoca tras EXECUTE exitoso [comportamiento PERMANENTE; REQ-DCC3BC1A].**
  Tras un EXECUTE **exitoso** del intake (respuesta real del runtime: applied true + seq), el wizard: (a) muestra
  un resultado INEQUIVOCO derivado de la respuesta REAL ("enviado - evento gobernado") con el **id del requisito
  (REQ-xxxx)** y el **seq** del evento; (b) **RESETEA el formulario**: campos vacios, vuelve al paso 1 (capturar),
  estado borrador, `piiAck=false`, listo para una historia NUEVA sin texto stale. Honestidad (hereda AC11): la
  confirmacion y el reset SOLO ocurren si el execute REALMENTE aplico (applied true + seq); si el execute **falla**
  o no se confirma -> **NO reset, NO verde, error real visible, borrador conservado** para reintentar. Elimina el
  reenvio accidental y el mangleo de la siguiente submission por campos stale. Test de COMPORTAMIENTO permanente:
  execute OK -> asertar render de id+seq y formulario reseteado (campos vacios, paso 1, borrador, piiAck=false);
  execute FALLIDO -> asertar NO reset, NO verde, error real, borrador conservado. UX read-only: NO nueva superficie
  de escritura (cuelga del submit ya gobernado). Conformidad AC13 contra `components/intake/` (wizard-4-resultado).
- **AC23 - Vista Help: guia navegable de metodologia y consola, read-only, honesta [comportamiento PERMANENTE; REQ-FB27AF72].**
  Un nav item **Help** entra en `NAV_VIEWS` (routing 1:1 con su panel, hereda AC12: al activarlo solo el panel
  Help es visible y el resto queda hidden; vista desconocida -> fallback DEFAULT_VIEW). El panel renderiza una
  guia DETALLADA y NAVEGABLE (secciones + indice/glosario) que cubre: la consola; observar vs operar;
  `submit_intent` como ESCRITOR UNICO; dry_run vs execute/confirmacion; atestacion #4; las vistas; el intake
  gobernado (RF-14); el pipeline SDD; y un glosario. **Fuente unica = `docs/MANUAL-operador.md`** (se REUSA, NO
  se duplica una copia divergente). Honestidad (hereda AC11): refleja lo que la app HACE HOY incluidas sus
  limitaciones; lo no implementado se marca pendiente/fuera-de-alcance, nunca se afirma como activo. **Read-only:**
  la vista NO escribe estado/ledger, NO expone superficie de escritura (sin botones de accion / sin llamadas a
  `/actions/submit`), extiende la prueba negativa de no-bypass (AC17). Conforme al design-system (hereda AC13:
  dark-first, tokens, la vista existe y navega). Test de COMPORTAMIENTO permanente: "help" en NAV_VIEWS ->
  routing solo-su-panel + fallback; el panel deriva su contenido del manual (no placeholder; cubre las secciones
  clave/glosario); el panel no expone superficie de escritura.
- **AC24 - Mailbox-archive gobernado de 1 click, atestado e idempotente [comportamiento PERMANENTE; DECISION-0053; REQ-B65E7802].**
  La vista **Mailbox** muestra los mensajes con su **estado** (open/answered/archived) y marca los consumidos. Un
  **boton "archivar"** por mensaje en `open/` dispara la accion de relay gobernada `mailbox-archive`: el builder
  SERVER-SIDE construye el intent core `mailbox_archive` desde un `message_id` VALIDADO -> `submit_intent` emite un
  evento ATESTADO (author=Operador, relayed_by=Arquitecto, endorsement=none) y el runtime mueve `open/<msg>.md` ->
  `archived/<msg>.md` con `status: archived` (ASCII). **NUNCA edita el mailbox directo:** no hay ruta de escritura
  del front al filesystem; todo pasa por el runtime (escritor unico; extiende la prueba negativa de no-bypass AC17).
  **Idempotente:** re-archivar (mismo idempotency_key / mensaje ya archivado) es no-op, no falla ni duplica.
  **Honestidad (hereda AC11):** el archive y el cambio de estado en la UI SOLO se reflejan si el runtime REALMENTE
  aplico (evento con seq); si falla -> error real visible, el mensaje sigue en open/, NO se pinta como archivado.
  Conforme al design-system (hereda AC13). Un archive REAL deja el canonico VERDE (validate exit 0; el mensaje
  movido casa carpeta/status; regresion-proof, espiritu AC22).
- **AC25 - ANTI-IMPERSONACION de mailbox-archive (prueba negativa PERMANENTE) [CRITICO; DECISION-0053].** El servidor
  NUNCA confia en datos crudos del cliente para esta accion. Test permanente (no reabrir el 403): forjar
  `payload.actorId`/`payload.intents`/llaves extra -> RECHAZADO (assertAllowedKeys; hereda AC19); archivar un
  `message_id` inexistente o una ruta FUERA de `Area_comun/mailbox/open/` (path-traversal) -> RECHAZADO; usar
  `mailbox-archive` para emitir CUALQUIER otro intent que no sea el `mailbox_archive` de forma exacta -> RECHAZADO.
  El hard-gate 403 admite EXACTAMENTE {`requirement-intake`, `mailbox-archive`}; toda otra forma 403. El evento
  relayado NO se cuenta/renderiza como AUTORADO ni avalado por el Arquitecto (hereda AC20). **AC4-byte:** el nuevo
  intent kind y la accion NO tocan `protocol.config.json` (signer set)/genesis/keys/`protocol_version`; se asierta
  BYTE-IDENTIDAD antes/despues (drift 0 necesario, no suficiente). Golden cases negativos PERMANENTES en el core.
- **AC26 - Neutralidad del core: atribucion CALLER-DERIVED del `mailbox_archive`, regresion-proof [comportamiento PERMANENTE; DECISION-0053; pasada del Analista].**
  El core generico (`runtime/submit_intent.py`) NO lleva literales de identidad de agente/instancia: la atribucion
  (`author`, `relayed_by`) del intent `mailbox_archive` la PROVEE EL CALLER (el front/Zeus, igual que el intake),
  no se hardcodea en el runtime. El core usa ROLES, no nombres. **Falsable (gate permanente):**
  `grep '"Operador"|"Arquitecto"' runtime/submit_intent.py` = 0 (antes del fix = 2, defecto). Esto tambien cierra
  el riesgo #5 (un archive directo no-via-front no queda mis-atribuido a una identidad fija). **Regresion-proof:**
  `scan_domain_neutrality` se EXTIENDE para atrapar literales de identidad de agente en el core (esta clase de
  regresion deja de ser silenciosa; filosofia AC11/AC22). **Bounding del `message_id`:** la regex se acota a
  `[A-Za-z0-9._-]` (sin `:` = NTFS ADS en Windows), manteniendo la guarda de path (no `/`,`\`,`..`, resolve-escape).
  Follow-up EXPLICITO (fuera de esta task): leaks analogos preexistentes (`apply.py` owner default, `context.py`
  implementer->nombre). El core permanece DOMAIN/INSTANCE-NEUTRAL (regla 1).
- **AC27 - Auto commit+push gobernado, acotado, atomico y honesto [comportamiento PERMANENTE; DECISION-0054; REQ-444E0DE5].**
  Tras un EXECUTE gobernado EXITOSO (requirement-intake / mailbox-archive), si la capacidad esta HABILITADA, el
  server hace `git add` de EXACTAMENTE las rutas reportadas por la transaccion submit_intent (task/seed file +
  `events.jsonl`/`snapshot.json`/`CLAIMS`/`PROJECT_STATE`/`TASK_INDEX`(+slim)), `git commit` con mensaje TEMPLADO
  server-side (ASCII; deriva de actionId+id+seq), y `git push` al remote/branch PRE-CONFIGURADO. **Honestidad
  (hereda AC11):** solo con push OK se reporta "enviado + aterrizado en canonico" con el **HEAD (sha)** y el
  **seq** REALES; si el push FALLA (red/auth/non-fast-forward) -> error real visible, NO verde, resultado =
  NO-aterrizado (el commit local puede existir, pero no se afirma aterrizado). **OFF BY DEFAULT:** capacidad
  deshabilitada por defecto; flag + remote/branch en registro FUERA del config pinned (#4 epoca 1.14.0); push vivo
  contra el remote real = GO posterior del operador. **Snapshot consistente:** commitea exactamente los outputs ->
  el clon limpio del HEAD pusheado valida exit 0 (regresion-proof estilo AC22).
- **AC28 - Anti-commit-arbitrario y anti-egress inseguro (prueba negativa PERMANENTE) [CRITICO; DECISION-0054].**
  Tests permanentes (no reabrir): un archivo **SUCIO AJENO** (no escrito por la transaccion) NO entra al commit
  (add explicito de rutas derivadas server-side; NUNCA `git add -A`/`.`); el cliente **NO puede inyectar** rutas ni
  el mensaje de commit (ambos server-side); **NO force-push** (`--force`/`--force-with-lease` ausentes;
  non-fast-forward -> error SEGURO "remote advanced", nunca sobrescribe el remote); el front **NUNCA** recibe/
  almacena credenciales (git las resuelve via el credential helper del entorno); el commit+push NO emite eventos
  ni muta el ledger (solo persiste en git lo que submit_intent escribio); **#4 byte-identica** (config/genesis/keys
  sin cambio; se asierta antes/despues). Carry AC17 (no es un 2o escritor del ledger).
- **AC29 - Refetch fresco al navegar [comportamiento PERMANENTE; REQ-C1976857].** Al activar un nav-item, la vista
  hace **fetch fresco** al server y actualiza su contenido sin requerir F5: Ledger seq, conteo del Backlog, Mailbox
  y la barra de integridad reflejan el canonico ACTUAL. Incluye **boton de recarga manual** por seccion y
  **refresco por intervalo** configurable (opt-in). READ-ONLY (solo GETs de observe; no toca submit_intent, carry
  AC17). Honestidad (AC11): si el fetch falla -> estado de error, no datos stale pintados como frescos. Test de
  comportamiento: navegar a una vista dispara el fetch (mock) y re-renderiza con el dato nuevo; el intervalo
  configurable se respeta; sin intervalo, no hay polling. Carry AC12 (routing) / AC13 (design). #4 byte-identica.
- **AC30 - Indicador de frescura + staleness [comportamiento PERMANENTE; REQ-547C6C54].** La barra de integridad /
  pie de seccion muestra **"actualizado hace Ns"**; durante una carga, un spinner/indicador sutil; si el dato es
  STALE (> N s sin refrescar) el indicador cambia de estado visual. Deriva del timestamp REAL del ultimo fetch
  exitoso (no estatico). READ-ONLY (carry AC17). Honestidad (AC11): el indicador refleja la antiguedad real, nunca
  pinta "fresco" un dato viejo. Test de comportamiento: tras un fetch, el indicador muestra la antiguedad; pasado
  el umbral pasa a STALE; durante carga muestra el spinner. Construye sobre AC29. Carry AC12/AC13; #4 byte-identica.
- **AC31 - Tooltips en badges de integridad [comportamiento PERMANENTE; REQ-4120B017].** Hover sobre cada badge de
  la barra de integridad (epoch/drift/attested/canonical/validator-exit) muestra un tooltip corto: valor normal,
  que significa cuando cambia, cuando preocuparse (ej. drift=0 OK, drift>0 atencion). READ-ONLY. Texto consistente
  con el glosario del Help (no contradice la doc). Accesible (title/aria). Test de comportamiento: cada badge
  expone su tooltip con el contenido esperado para los 5 badges. Carry AC11/AC12/AC13/AC17; #4 byte-identica.
- **AC32 - Tooltips en codigos RF-N y acronimos [comportamiento PERMANENTE; REQ-3E31293F].** Hover sobre un codigo
  RF-N (RF-5, RF-14...) o acronimo (SDD/T0/HMAC/PII...) en cualquier vista muestra su nombre completo; los codigos
  son interactivos (cursor pointer). El diccionario es UNA fuente unica (compartida con el glosario del Help, no
  duplicada). READ-ONLY. Test de comportamiento: hover sobre RF-5/SDD/HMAC rinde el texto esperado; el set cubre
  los codigos que el front realmente muestra. Carry AC11/AC12/AC13/AC17; #4 byte-identica.
- **AC33 - Render de diagramas Mermaid en Help [comportamiento PERMANENTE; REQ-D2C6579F].** Los bloques Mermaid de
  las secciones 4/5/6/7 del Help se renderizan como diagramas (SVG) en vez de texto crudo. **SIN agregar dependencia
  de servidor / npm install:** vendorizar la lib como asset estatico servido por el propio server, o SVG
  pre-generado; preserva la propiedad "sin dependencias" de la consola. READ-ONLY. Test de comportamiento: el panel
  Help no muestra el codigo mermaid crudo de esos bloques (render presente); el server sigue sin deps de npm.
  Carry AC11/AC12/AC13/AC17; #4 byte-identica.
- **AC34 - Jerarquia tipografica Mailbox/Backlog [conformidad-diseno PERMANENTE; REQ-28118FC3].** En tarjetas de
  Mailbox el ASUNTO es prominente y el `MSG-...` secundario (menor tamano/contraste); en Backlog el TITULO primero
  y el `REQ-/TASK-id` secundario debajo. Tokens del design-system (AC13). READ-ONLY. Test de conformidad: el id
  tecnico no tiene el mismo peso visual que el asunto/titulo (clases/tokens correctos). Carry AC11/AC12/AC13/AC17;
  #4 byte-identica.
- **AC35 - Kanban: colapsar columnas vacias + mostrar done [comportamiento PERMANENTE; REQ-B97838C6].** Las columnas
  del Backlog con count=0 se muestran compactas (solo cabecera, sin hueco); la columna **done MUESTRA su contenido**
  (lista o resumen paginado, no solo el numero). El ancho se adapta al contenido real. READ-ONLY. Test de
  comportamiento: con una columna en 0 -> modo compacto; done con N tareas -> renderiza/pagina; no queda done con
  count pero sin lista. Carry AC11/AC12/AC13/AC17; #4 byte-identica.
- **AC36 - Filtros + paginacion del Ledger #4 [comportamiento PERMANENTE; REQ-9AF54A75].** La cabecera del Ledger
  ofrece filtro por **actor** y por **tipo de evento**; al seleccionar, la lista se reduce a los que coinciden;
  **paginacion/carga progresiva** para no renderizar 900+ eventos a la vez. READ-ONLY sobre el ledger atestado; el
  texto libre sigue REDACTADO (no afloja PII). Test de comportamiento: filtrar por actor=Codex / tipo=intent.applied
  reduce la lista; la paginacion limita el render; sin filtro, pagina por defecto. Carry AC11/AC12/AC13/AC17;
  #4 byte-identica.
- **AC37 - Carga de requerimiento por archivo, gobernada y acotada [comportamiento PERMANENTE; DECISION-0055; REQ-31100EAF].**
  Desde el Intake, el operador adjunta un archivo; el server (a) valida **tipo** (allowlist .md/.txt), **tamano**
  (<= N KB) y **nombre saneado** (sin path traversal); (b) extrae el texto como contenido INERTE (nunca ejecutado/
  evaluado); (c) aplica **PII structural guard + ASCII** al texto extraido; (d) alimenta el MISMO
  `requirement-intake` (task_upsert type=requirement, author=Operador, relayed_by=Arquitecto provistos por el
  caller). Solo el EXECUTE gobernado escribe; preview(dry_run) != green. **Idempotente:** re-subir el mismo archivo
  (mismo id-hash) no duplica. **Honestidad (AC11):** exito SOLO con el requerimiento REALMENTE escrito (id+seq
  reales); ingestion/execute fallidos -> error real, no verde. **OFF BY DEFAULT** (flag fuera del config pinned;
  uso vivo = pre-auth condicionada del operador, activacion runtime). El HEAD resultante valida exit 0 (regresion-
  proof, estilo AC22).
- **AC38 - Anti-abuso de ingestion (prueba negativa PERMANENTE) [CRITICO; DECISION-0055].** Tests permanentes (no
  reabrir): tipo NO permitido (binario/ejecutable) -> RECHAZADO; archivo sobre-tamano -> RECHAZADO; nombre con
  **path traversal** (`/`,`\`,`..`,`:`, control) -> RECHAZADO/saneado; contenido "activo" (script/macro) -> tratado
  como TEXTO INERTE, nunca ejecutado/renderizado; el cliente NO inyecta actor ni rutas de escritura (server-side,
  hereda AC19); sin egress; **#4 byte-identica** (config/genesis/keys sin cambio). PII: patrones tipo NIT/razon
  social/SQL en el archivo -> el plano publicable no expone el literal. Golden/test del lado server.
- **AC39 - Intake honesto: no requerimientos fantasma desde placeholder/vacio + proyecto explicito [comportamiento PERMANENTE; REQ-643B160A].**
  El EXECUTE del intake (RF-14) NUNCA crea un requerimiento a partir de texto placeholder/ejemplo o campos vacios:
  (a) **rechaza** (sin preview-as-green) si la **narrativa** o la **intencion de aceptacion** estan VACIAS o son
  IGUALES al placeholder/ejemplo conocido (validacion server-side, no solo client-side); (b) el **proyecto destino
  debe elegirse explicitamente** -> NO defaultea a `Zeus-protocol` (ni a ningun proyecto) cuando el operador no
  eligio; un EXECUTE sin proyecto explicito se rechaza. Honestidad (hereda AC11): el rechazo es un error real, no
  un verde; solo un requerimiento con contenido REAL aterriza (id+seq). Remedia la anomalia del fantasma
  REQ-984A85C6 (ya cancelado). Test de COMPORTAMIENTO permanente: narrativa/aceptacion vacias o == placeholder ->
  RECHAZADO (no se crea REQ, no verde); proyecto no elegido -> RECHAZADO; contenido real + proyecto explicito ->
  requirement real id+seq. Carry AC11/AC14/AC22; #4 byte-identica. Read-only sobre la superficie de escritura
  (tightening de la validacion del execute ya gobernado; no abre superficie nueva).
- **AC40 - Upload gobernado server-NO-MODELO-EGRESS: screening PII real + store fuera del dataset + SHA-256 + emit extraction-task [PERMANENTE; DECISION-0056; REQ-D642E4D8].**
  El upload es accion gobernada server-side. **El server NO llama a ningun endpoint de MODELO/inferencia** (sin
  SDK de modelo, sin socket a host de LLM, sin API key de modelo) -- garantia ESTRECHA, NO "cero egress" (el
  `git push` gobernado del intake es transporte existente DECISION-0054). El upload: (a) corre **screening de PII
  REAL best-effort** (email/telefono/documento-cedula/NIT/razon-social/SQL/nombres heuristicos) + ASCII sobre el
  contenido; HONESTO: best-effort, **NO** se afirma PII-free garantizado ni "ningun LLM ve PII"; (b) guarda el
  archivo en un **STORE FUERA DEL DATASET ATESTADO** (tmp del SO o area gitignored entregada con su linea
  `.gitignore` en el MISMO commit y EXCLUIDA del git-status del indicador canonico), ruta server-derived acotada,
  nombre saneado (sin traversal), allowlist .md/.txt + limite de tamano (hereda AC37/AC38), contenido INERTE; el
  **hash atestado del archivo es SHA-256 sobre los BYTES CRUDOS** (no FNV-32 ni sobre texto saneado); (c) emite una
  **TAREA de extraccion con CONTRATO AUTOCONTENIDO** (ruta, formato de salida de candidatas, criterio de done) via
  `task_upsert` con status YA VALIDO (NO crea intent kind/status nuevo). El evento atestado solo registra "archivo
  subido (sha256) + extraccion pedida". **Idempotente** por (sha256-bytes + project). **#4 byte-identica.** Test +
  PRUEBA NEGATIVA: el handler de upload no importa SDK de modelo ni abre socket a host de LLM (estatico falsable +
  control positivo); tipo/tamano/traversal -> rechazado; `git ls-files <store>` vacio; el screening corre antes de
  persistir.
- **AC41 - Extraccion = trabajo de AGENTE (egress del agente acotado/consentido) -> candidatas en STORE NO-LEDGER fuera del backlog [PERMANENTE; DECISION-0056].**
  La extraccion (archivo -> historias candidatas) la hace un **AGENTE** que toma la tarea (no el server). RECONOCIDO:
  el agente LEE el archivo externo (post best-effort screening); el upload **etiqueta/consiente y registra** que el
  archivo sera leido por el agente extractor (ventana reconocida, no oculta). Las candidatas viven en un **STORE
  NO-LEDGER, gitignored, FUERA del dataset**, con **ciclo de vida propio que NO es `task_status`** (el estado
  `candidate` NO existe en VALID_TASK_STATUSES y NO se agrega): el ledger atestado **NUNCA** ve `candidate`, no
  tocan TASK_INDEX/PROJECT_STATE; **drift 0 con candidatas presentes**; un clon limpio sin el store sigue validando
  exit 0. El no-determinismo del LLM queda FUERA de #4. Test: candidatas producidas no aparecen en TASK_INDEX ni en
  el validate del ledger; drift 0.
- **AC42 - Selector de modo (digitado vs archivo), obligatorios en ambos, rama-archivo gateada [PERMANENTE; REQ-D642E4D8].**
  Antes de crear, el operador elige el MODO: (a) "Nueva historia digitada" -> campos actuales; (b) "Por carga de
  archivo". En AMBOS se validan los **obligatorios** antes de EXECUTE (carry AC39). La **rama "por carga de archivo"
  se GATEA detras de B+C** (feature-flag de UI: no se ofrece vacia) o lleva un consumidor minimo no-LLM (archivo
  entero = 1 candidato editable). Conforme al design-system (AC13). Test: cada modo expone su flujo; ninguno permite
  EXECUTE con obligatorios vacios/placeholder; modo-archivo no se ofrece sin B+C activos.
- **AC43 - GATE HUMANO DURO de PII + aprobacion por candidata; id del contenido editado [CRITICO PERMANENTE; DECISION-0056].**
  El operador revisa/edita CADA candidata en el panel y para **APROBARLA DECLARA explicitamente que reviso PII**
  (atestacion humana por-candidata; el front EXPONE la accion de aprobar/editar/descartar por candidata). Solo una
  candidata APROBADA pasa por el `requirement-intake` EXISTENTE (execute gobernado AC39) con **re-screening de PII**
  en la frontera candidate->intake (el texto EDITADO -- contenido nuevo que no paso el gate de ingest -- se valida
  por los MISMOS guards al aprobar). El **id/idempotency** del requirement deriva del **CONTENIDO EDITADO**
  (title+narrative+intent+project), NO del archivo (1 archivo -> N candidatas -> N requirements distintos; re-aprobar
  la misma candidata es idempotente). El `narrative` aprobado se atesta en #4 (IRREVERSIBLE) -> la declaracion
  humana es el gate duro antes del write inmutable. **Atribucion (D-ACTOR): relay honesto** author=Operador/
  relayed_by=Arquitecto (sin tocar registry, #4 byte-identica). Test: aprobar sin declarar PII -> bloqueado;
  editar un candidato para inyectar PII/contenido activo -> redactado/rechazado al aprobar; 1 archivo -> 3
  candidatas -> 3 REQ con ids distintos.
- **AC44 - Anti-abuso, estados de extraccion, purga y procedencia (prueba negativa PERMANENTE) [CRITICO; DECISION-0056].**
  Tests permanentes: server **no-MODELO-egress** (estatico falsable + control positivo); store de uploads y
  candidatas FUERA del dataset (gitignored, `git ls-files` vacio, excluido del git-status del indicador, no toca
  `Area_comun/state`/working-tree -- 2a-superficie aislada, unica mutacion de ledger = `task_upsert` via
  submit_intent); contenido INERTE; **estados de extraccion explicitos** (encolada / sin-agente-en-loop con aviso /
  corriendo / completed-empty / completed-N con cap maximo / failed con razon + timeout/liberacion del claim);
  **purga del raw** al estado terminal del candidato + TTL para huerfanos (test: el raw no sobrevive al estado
  terminal; clon limpio sin la carpeta valida exit 0); **procedencia PII-free determinista** en el requirement
  aprobado (sha256 archivo + id extraction-task + hash candidato pre-edicion); errores/logs del flujo NO ecoan
  contenido crudo; el panel (front) es read/edit local puro (sin SDK/fetch de modelo en el browser);
  **#4 byte-identica** (config/genesis/registry/keys sin cambio, version pinned 1.14.0). OFF-by-default.
  Un upload->aprobacion real deja el canonico VERDE (regresion-proof, AC22).
- **AC45 - Endurecimiento pre-Fase-C: guard de salida de red a TODO src/** + purga/TTL del raw [PERMANENTE; DECISION-0056; pasada del Analista TASK-0150].**
  PREREQUISITO antes de Fase C (cuando enciende el agente extractor = ventana real de modelo): (a) el guard de
  AC40 se AMPLIA a **TODO `src/**`** (no solo el handler de upload) y marca **CUALQUIER salida de red** (no solo
  proveedores de modelo nombrados): import/require de SDKs de modelo, `fetch`/`http(s)`/`node:net|tls|dgram`/
  `WebSocket` a hosts no-allowlisted -- el unico egress permitido es el `git push` gobernado existente y las
  lecturas read-only ya allowlisted; prueba estatica falsable + control positivo. (b) **politica de purga/TTL del
  raw** en os-tmp: el archivo se borra al estado terminal del candidato (aprobado/descartado) + barredor TTL para
  huerfanos (agente murio / sin aprobar); test: el raw no sobrevive al estado terminal; un proceso reiniciado
  purga huerfanos > TTL. (c) **estabilidad de CI:** los tests del flujo son deterministas / no sensibles a timeout
  (sin flake frio-vs-caliente). Carry AC40/AC44; #4 byte-identica. Bloquea el cierre de Fase C.
- **AC46 - Guard de egress ALLOWLIST (deny-all) + ejecucion dinamica [PERMANENTE; DECISION-0056; pasada del Analista TASK-0152; PRECONDICION del uso vivo del extractor].**
  El guard de salida de red de AC45 pasa de **denylist** (proveedores/clientes nombrados) a **ALLOWLIST deny-all**:
  el scan estatico de TODO `src/**` marca **CUALQUIER `import`/`require` cuyo modulo NO este en una lista permitida
  explicita** (p.ej. fs/path/crypto/url/os/util + el wrapper de git gobernado), no solo los proveedores conocidos.
  Esto cierra el residual reconocido por el Analista (clientes HTTP no listados: phin/needle/bent/ky/...; el denylist
  no puede enumerarlos todos). Ademas el guard marca **ejecucion dinamica**: `eval(` y `new Function(` (ofuscacion /
  egress encubierto). El unico egress permitido sigue siendo el `git push` gobernado + lecturas read-only ya
  allowlisted. Prueba estatica falsable + **control positivo POR familia**, incluyendo al menos: un cliente HTTP NO
  listado (p.ej. `import phin from "phin"`) -> FLAGGED; `eval(`/`new Function(` -> FLAGGED; un import permitido
  (fs/path/...) -> `[]`; el `git push` gobernado -> `[]`. El src real da `[]` (sin falso positivo). Carry AC45/AC41.
  #4 byte-identica. **NO enciende el uso vivo**; es PRECONDICION del GO de uso vivo del extractor (ventana de modelo).
- **AC47 - Aislamiento de la suite del entorno de runtime del operador [PERMANENTE; DECISION-0056].**
  `npm test` NO debe heredar los env de runtime del operador. Al arrancar, la suite limpia/sobrescribe con fixtures
  propias `AUTO_COMMIT_PUSH_CONFIG_PATH`, `FILE_INGESTION_CONFIG_PATH` (y cualquier env que altere el off-by-default),
  de modo que el resultado sea **determinista** independientemente del shell. Motivo: hoy, si el operador corre los
  tests con el server push-vivo/ingestion ON en el mismo shell, salen 3 rojos FALSOS (off-by-default 200!=403,
  executes 502!=200) aunque el codigo este verde en clon limpio -- es aislamiento del harness, no un defecto del
  producto. Test falsable: con esos env apuntando a configs "ON", la suite sigue verde porque los aisla; un test que
  dependa del env heredado rompe el aislamiento. #4 byte-identica.
- **AC48 - Boton 'Nueva historia/requisito' con estilo gobernado [comportamiento PERMANENTE; REQ-40EC863F].** El
  boton de la vista Intake usa la clase de boton gobernada del design-system (`governed-button`) + los design
  tokens (no estilo ad-hoc/roto). Behavior-test: el render del boton expone la clase gobernada y los tokens; un
  boton con estilo ad-hoc rompe el test.
- **AC49 - 'Nueva historia/requisito' NO resetea el formulario tipeado [comportamiento PERMANENTE; REQ-0873A67C].**
  El reset del formulario del Intake ocurre SOLO tras un EXECUTE exitoso (AC21); el boton/paso 'Nueva historia'
  (compose) NO borra el contenido que el operador ya tipeo. Behavior-test: simular texto en el form + accion
  'Nueva historia' (sin execute) -> el contenido persiste; reset solo con `status.variant === "ok"`.
- **AC50 - El sitio refleja el canonico fresco sin reiniciar el servidor [comportamiento PERMANENTE; REQ-6D80DB17].**
  El server lee el canonico FRESCO por request (via `git show`/`git diff` del HEAD, sin cache de modulo del
  snapshot) y el front refetcha al navegar (AC29), de modo que un commit nuevo del protocolo aparece sin reiniciar.
  Behavior-test: cambiar el canonico (nuevo HEAD) entre dos requests -> el segundo refleja el cambio sin reinicio;
  un cache de modulo del canonico rompe el test.
- **AC51 - Extractor TROCEADO: contexto acotado por llamada, escala a cualquier tamano [PERMANENTE; DECISION-0058].**
  El provider `local-vlm` del extractor procesa **per-pagina** (PDF -> imagen por pagina) y **per-chunk** (texto
  grande partido en pedazos acotados), **una llamada al modelo por pagina/chunk**. El `num_ctx`/payload por llamada
  es **fijo y acotado**, independiente del tamano total del documento. Las candidatas de todas las paginas/chunks
  se **acumulan y deduplican** en el store no-ledger. Behavior-test: un documento de N paginas produce N llamadas
  acotadas (no una con contexto N-dependiente); duplicados entre paginas se colapsan; cubre los 5 formatos
  (pdf/imagen via vision, md/html/txt via texto).
- **AC52 - Frontera de egress del Extractor = SOLO endpoint local allowlisted [CRITICO PERMANENTE; DECISION-0058].**
  El extractor live solo puede llamar al **endpoint del modelo local configurado** (p.ej. `127.0.0.1:11434`); el
  guard de egress (AC46 deny-all) **allowlistea unicamente ese host:puerto local** y marca CUALQUIER otra salida
  de red (incluido cualquier host no-loopback). El contenido del archivo NUNCA va a un host externo. Control
  positivo: una llamada a un host no-loopback desde el extractor -> FLAGGED; la llamada al endpoint local
  configurado -> permitida; un endpoint con host != loopback en la config -> rechazado. Off-by-default
  (`local-vlm` solo activo con flag + consentimiento explicito).
- **AC53 - Extractor: salida estructurada robusta + carry de PII/no-ledger [PERMANENTE; DECISION-0058].** El
  extractor parsea de la respuesta del modelo SOLO el JSON de candidatas (tolerante a campos de razonamiento
  separados / texto extra; descarta lo que no sea candidata valida; no crashea si el modelo divaga). Las candidatas
  van al store NO-ledger; el **GATE HUMANO DURO de PII (AC43)** + aprobacion humana antes del intake se mantienen
  sin cambio (carry). El extractor NO escribe el ledger (sin `submit_intent`), NO toca codigo/estado. #4
  byte-identica (el core no cambia). Behavior-test: respuesta con razonamiento+JSON -> extrae solo las candidatas;
  respuesta basura -> 0 candidatas sin crash; ninguna candidata entra al intake sin aprobacion humana.
- **AC54 - Extractor = worker de PRODUCTO con autoria honesta, fuera del config #4 [PERMANENTE; DECISION-0058 Opcion 2].**
  El Extractor se registra en un **registro de workers a nivel PRODUCTO** (Zeus, FUERA de protocol.config.json; sin
  re-genesis): id `Extractor`, rol/extraccion, modelo por defecto `qwen3-vl:4b-instruct`, endpoint loopback. Firma
  sus candidatas con una **clave de PRODUCTO** (Ed25519 propia, privada fuera del repo); cada candidata lleva la
  firma + el id del firmante -> autoria honesta verificable. NO esta en el `agent_registry` #4 ni en
  `signature_config` (no firma el ledger). Behavior-test: cada candidata producida lleva firma valida del Extractor;
  una firma forjada/ausente se detecta; el registro de workers NO toca el config #4 (config pinned 1.14.0,
  byte-identica); off-by-default (el provider live solo con flag+consentimiento).
- **AC55 - Intake: el modo "carga por archivo" abre una SECCION dedicada, sin scroll y sin pedir campos antes [PERMANENTE; REQ intake-ux-feedback].**
  Elegir "carga por archivo" en el Intake abre una seccion propia cuyo primer elemento visible es el selector de
  archivo + el boton "Extraer requisito" (no requiere scroll para alcanzar el cargador). Los campos Titulo /
  Narrativa / Intencion de aceptacion NO se solicitan antes de cargar el archivo (vienen del archivo o los propone
  el modelo). Behavior-test: en modo archivo el selector y el boton "Extraer requisito" estan en el render inicial
  de la seccion; los inputs Titulo/Narrativa/Intencion no se renderizan ni se exigen antes de la carga.
- **AC56 - Boton "Extraer requisito" -> Extractor -> candidatas como TARJETAS [PERMANENTE; REQ intake-ux-feedback].**
  El boton envia el archivo al agente Extractor por la ruta gobernada de extraccion (off-by-default, loopback, carry
  AC51-AC54) y al volver muestra las candidatas como tarjetas visuales (una por candidata, pendientes de aprobacion).
  Behavior-test: respuesta con N candidatas -> N tarjetas; 0 candidatas -> mensaje sin crash; respeta consent + gate
  de PII; ninguna candidata entra al ledger sin aprobacion humana + submit_intent.
- **AC57 - Click en una tarjeta candidata puebla [Titulo, Narrativa, Intencion de aceptacion] [PERMANENTE; REQ intake-ux-feedback].**
  Al hacer click en una tarjeta, las secciones Titulo / Narrativa / Intencion de aceptacion se cargan con los valores
  de esa candidata, quedando pendientes de aprobacion/envio humano (no entran al ledger hasta submit_intent +
  aprobacion). Behavior-test: click en tarjeta -> los tres campos toman los valores de la candidata; el gate humano
  de PII/aprobacion se mantiene antes del submit.
- **AC58 - Auto-commit-push ergonomico: el submit gobernado llega al canonico sin push manual [PERMANENTE; REQ intake-ux-feedback].**
  El server resuelve la config de auto-commit-push (y de file-ingestion) prefiriendo el override runtime gitignored
  (`*.runtime.json`) cuando existe, y cae al config VERSIONADO off-by-default cuando no. Con el override activo,
  presionar "Execute submit_intent" hace commit+push del output gobernado a origin -> el Arquitecto/checker lo ve sin
  push manual. El config versionado permanece `enabled:false` (invariante off-by-default intacto para clones/CI). El
  push NO es un segundo escritor: solo propaga el output ya escrito por submit_intent (carry AC17/no-bypass).
  Behavior-test: override presente+enabled -> el submit dispara commit+push (git mockeado); override ausente -> sin
  push (off); el config versionado sigue `enabled:false`.
- **AC59 - En modo carga-por-archivo el boton "Execute submit_intent" esta OCULTO [PERMANENTE; REQ intake-ux-feedback-2].**
  El boton "Execute submit_intent" (envio individual de UN requisito) NO se muestra en el modo carga-por-archivo
  mientras el flujo es extraer-tarjetas. Solo se habilita (a) al hacer click en una tarjeta candidata y APROBAR ese
  requisito (la accion de aprobar de la tarjeta es la que envia), o (b) en el modo individual/typed explicito. Asi el
  operador no presiona el boton equivocado en el flujo por archivo. Behavior-test: en modo file sin tarjeta
  seleccionada -> el boton Execute NO esta presente/visible; al aprobar una tarjeta o en modo typed -> disponible.
- **AC60 - El selector de PROYECTO DESTINO es el primer elemento de la carga por archivo [PERMANENTE; REQ intake-ux-feedback-2].**
  En la seccion de carga por archivo, el selector de "Proyecto destino" se renderiza como PRIMER div, ANTES del
  selector de archivos. Behavior-test: en el orden del DOM de la seccion file, el selector de proyecto precede al
  input de archivo.
- **AC61 - "Extraer requisito" muestra un INDICADOR DE PROCESAMIENTO [PERMANENTE; REQ intake-ux-feedback-2].**
  Al presionar "Extraer requisito", como el agente tarda, el front muestra un estado visible de "procesando" (spinner
  o texto) y deshabilita el boton hasta que la extraccion responde, para que el operador no crea que no pasa nada.
  Behavior-test: al disparar la extraccion el estado pasa a procesando + boton deshabilitado; al volver, se limpia.
- **AC62 - Errores en ROJO + aviso de ingestion fiel [PERMANENTE; REQ intake-ux-feedback-2].**
  Los mensajes de error (extraccion fallida, archivo rechazado, sin candidatas con causa) se muestran en ROJO/estado
  de error visible, no como texto neutro. El aviso de ingestion refleja las EXTENSIONES REALES y maxBytes del config
  cargado (no el literal hardcodeado ".md/.txt"). Behavior-test: una respuesta de error pinta el estado rojo; el
  aviso lista las extensiones del config vivo.
- **AC63 - "Extraer requisito" muestra las candidatas como TARJETAS end-to-end (fix 0-candidatas) [PERMANENTE; REQ intake-ux-feedback-2].**
  Tras una extraccion exitosa las candidatas aparecen como TARJETAS VISIBLES sin accion manual extra (refresh real del
  panel de candidatas). Se diagnostica y corrige el caso "Sin candidatas" sobre un .md valido multi-seccion: (a) el
  server vivo HONRA el override runtime (file-ingestion.runtime.json -> extractor enabled, provider local-vlm,
  endpoint loopback) -- si el proceso corre con el config versionado el extractor queda OFF; (b) la extraccion
  local-vlm PARSEA y ALMACENA candidatas de un documento con varias historias (carry AC53 parseo robusto + AC51
  troceado + AC52 egress loopback + AC43 gate PII + candidatas no-ledger); (c) si la extraccion produce 0 candidatas
  con causa (modelo vacio, timeout), se reporta como ERROR visible (AC62), no como panel silenciosamente vacio. Repro
  documentado: con el server vivo (runtime override + Ollama), subir un .md multi-historia (p.ej.
  `historias_panel_operar_agentes.md`) -> aparecen N tarjetas candidatas. #4 byte-identica; off-by-default intacto.
- **AC64 - La subida-para-EXTRAER NO exige acceptanceIntent (alinea AC55) [PERMANENTE; REQ intake-ux-feedback-3].**
  En el flujo de carga por archivo, la peticion de EXTRACCION (que crea la TASK-EXTRACT) NO requiere
  `acceptanceIntent` ni los demas campos de requisito: solo archivo + proyecto (+ ack de PII). El `acceptanceIntent`
  (y titulo/narrativa) se exige unicamente al APROBAR una candidata (post-extraccion), porque vienen del archivo o
  los propone el modelo (coherente con AC55: no se piden campos antes de la carga). Hoy `sanitizeFileExtractionUpload`
  llama `validateHonestRequirementField("acceptanceIntent", ...)` y bloquea la extraccion con "acceptanceIntent is
  required" -> se corrige: acceptanceIntent OPCIONAL en la subida-para-extraer; sigue REQUERIDO en
  `sanitizeCandidate` (aprobacion). Behavior-test: extraer con acceptanceIntent vacio -> OK (no 400); aprobar una
  candidata sin acceptanceIntent -> sigue rechazando. Carry AC43 gate PII + candidatas no-ledger.
- **AC65 - La confirmacion de PII se ve ALINEADA y legible [PERMANENTE; REQ intake-ux-feedback-3].**
  El control de confirmacion de PII (checkbox + etiqueta) se renderiza ALINEADO y legible: el checkbox alineado al
  inicio del texto, el texto envuelve limpio (sin desbordes ni solapes). La redaccion es clara para el operador (la
  jerga tecnica tipo "escribe via runtime/submit_intent.py como relay acotado" se simplifica a lenguaje llano, sin
  perder el sentido: confirmo que revise PII y que esta accion se ejecuta de forma gobernada). Behavior-test: el
  nodo del checkbox y su label estan asociados (htmlFor/anidado) y el contenedor aplica la alineacion esperada.
- **AC16 - Guarda PII ESTRUCTURAL + ASCII (pasada del Analista).** La guarda NO depende de un detector
  automatico (TASK-0118/DEF-PII = `proposed`, no existe aun): (a) separar la intencion-en-lenguaje-llano
  (plano publicable) del payload sensible; (b) redactar/marcar el texto libre en todo plano
  publicable/exportable; (c) canal ASCII en todo string que el front escriba al protocolo; (d) advertir al
  operador en compose y en confirm ("no incluyas PII de terceros: NIT, razon social, datos SQL"). Coherente
  con DECISION-0040. Test: payload con patrones tipo NIT/razon social/SQL -> el plano publicable no expone el
  literal; el intake NO levanta el gate TASK-0118/DEF-PII antes de captura viva real. NOTA (Analista): la
  redaccion es best-effort por PATRONES (NIT/razon social/SQL); **no se afirma "PII-free" garantizado** (un
  nombre/email/telefono podria pasar) -- DEF-PII (TASK-0118) sigue siendo el gate.
- **AC17 - No-bypass.** Se mantiene `directLedgerWrites:false`; ninguna ruta del front escribe estado/ledger
  fuera de submit_intent (extiende la prueba negativa de superficie de TASK-0127). El intake cuelga del
  patron `governed-action` (un solo writer), no crea un segundo escritor.

> RF-14 se construye CONTRA el diseno ya entregado por Claude Design en
> `Zeus-protocol/design/interface/components/intake/` (lista, wizard-1-capturar, wizard-2-preview,
> wizard-3-confirmar, wizard-4-resultado, detalle, estados, NOTES.md): **AC13 (conformidad de diseno) aplica
> a estas pantallas**.

## test_plan

- **Producto (Zeus-protocol):** suite del front (unit/integration) + CI verde; pruebas de que las vistas
  leen canonico read-only y que toda accion va por `submit_intent` (mock/dry-run del runtime); prueba
  negativa: no hay camino de escritura directa al ledger.
- **Atestacion:** dado un ledger fixture, el front muestra la verificacion de firmas/cadena/anclaje igual
  que las funciones del runtime.
- **Gobernanza (protocolo):** validate/encoding/neutralidad exit 0 en clon limpio (con y sin secretos);
  cada etapa cierra con su evidencia atestada bajo #4.

## closure_criteria

- Por ETAPA (SDD, maker=Codex/checker=Arquitecto): AC aplicables verdes; CI del producto verde; gobernanza
  en Area_comun valida (exit 0); reporte atestado. El MVP-T0 cierra cuando RF-1..RF-10 (etapas 1-3 +
  vista de atestacion + roster-min + kickoff) estan verdes. Sin tocar #4/config pinned (epoca 1.14.0);
  capacidades fuera del config (DECISION-0047). Export/multi-tenant/Fase4 = posterior.

## Risks

- **Bypass del escritor unico.** Mitigacion: AC2/AC4 (toda escritura por submit_intent; prueba negativa);
  review de que no hay ruta directa.
- **Leer working tree volatil en vez del canonico.** Mitigacion: AC1/AC5 (read-only sobre origin/objetos
  git); disciplina de clon limpio para escrituras.
- **Front infla el contexto de los agentes / coste.** Mitigacion: RNF-10 (contexto minimo; digestion de
  skills); el front no entra al hot path de los agentes.
- **Acoplar el core al producto.** Mitigacion: RNF-6 (producto en repo aparte; unidireccional).

## Traceability

| Requirement | Task | Test | Closure |
|-------------|------|------|---------|
| RF-1..RF-4 observar read-only canonico | TASK-0124 (etapas 1-2) | vistas vs canonico; atestacion vs runtime | AC1/AC3/AC5 |
| RF-5..RF-8,RF-10 operar gobernado | TASK-0124 (etapa 3) | toda accion via submit_intent; prueba negativa | AC2/AC4/AC9 |
| RF-9 roster re-genesis-gobernado | TASK-0124 (etapa 5) | flujo gateado, no toggle | AC8 |
| Honestidad de estado regresion-proof | TASK-0129 (badge behavior test) + etapa5/6 | test de comportamiento: verif. falla -> badge no-verde; valido -> verde; PII redactada | AC11 |
| CI verde / neutralidad / gates | TASK-0124 | CI producto + validate/scan protocolo | AC6/AC7/AC10 |
| RF-14 intake gobernado de requisitos | TASK-0133 (DECISION-0051) | wizard -> task_upsert requirement (Operador, idempotente); EXECUTE con confirmacion (prueba negativa); PII estructural+ASCII; no-bypass; conforme al diseno components/intake/ | AC14/AC15/AC16/AC17 + AC11/AC12/AC13 |
| RF-14 remediacion seguridad (relay acotado + anti-impersonacion) | TASK-0134 (DECISION-0052) | builders server-side (sin trust de payload.actorId/intents); relay-como-Arquitecto SOLO para requirement-intake; firma=origen+transporte no aval; write real demostrado; #4 byte-identico | AC15(write-real)/AC18/AC19/AC20/AC4-byte + carry AC11/12/13/14/16/17 |
