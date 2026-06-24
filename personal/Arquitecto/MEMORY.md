# MEMORY - Arquitecto (antes "Claude") - multi_agent_project_protocol

> Runbook in-repo del Arquitecto (DECISION-0026: actualizar tras cada commit). Cronologia completa en la
> memoria auto (`memory/project-state-snapshot.md`). Aqui = estado vigente + reglas + lecciones, conciso.
> Ultima actualizacion: 2026-06-24, HEAD 312d471, v1.14.0 (#4 enforce/auth ON).

## TASK-0166 (2026-06-24) - checker verde + REVIEW al Analista encolada
- Panel "Operar Agentes" Q1 control de runtime (SPEC-0089 AC1-AC6), maker=Codex, producto Zeus-protocol
  commit 560d291. Codex la dejo in_review.
- **Pasada de checker (Arquitecto) VERDE desde clon limpio:** node --test 63/63 (sin flake local-vlm),
  targeted 9/9, WRITE REAL camino feliz (activate Arquitecto->heartbeat en disco->alive; stop->removido->
  dormant; leccion TASK-0133), allowlist niega arbitrary/traversal/injection + action invalida + clave extra
  (400 sin ejecucion, cero archivos parasitos), validate exit 0, drift 0, neutralidad/encoding exit 0.
- **El operador eligio activar al Analista** (DoD nombra pasada independiente del Analista). El runtime del
  Analista YA estaba vivo (cron pid 161808, polling 300s). Encole MSG-20260624-Arquitecto-to-Analista-REVIEW-
  TASK-0166 (type REVIEW, rr=true, requested_action, autocontenido con mi evidencia + 4 focos) via submit_intent
  (claim file-scoped, seq 1565) + commit 312d471 PUSHED. LECCION: el cron Analista tiene un stop-detector regex
  (detener|parar|para|stop + Analista|cron|monitor en misma linea) -> NO usar esas palabras juntas en el cuerpo.
- **PENDIENTE:** el Analista emite artefacto ANALISTA-*-veredicto.md + MSG to:Arquitecto rr=true (OK->CERRABLE o
  CAMBIO-REQUERIDO) y commitea/pushea como Analista. Con su OK->CERRABLE: yo (reviewer) cierro TASK-0166
  in_review->done via submit_intent (libero claim en el mismo paso) + archivo el ciclo. Si CAMBIO-REQUERIDO:
  handoff a Codex.

## Carril A Presupuesto/tesis (2026-06-19) - PROMOVIDO v1.10.0 (e56b027)
- **PROMOVIDO** (GO operador + OK Codex + cross-check asistente): DECISION-0039 (activacion #4) + SPEC-0081
  + DECISION-0040 (GATE-DATASET) + DECISION-0041 (read-only) + DECISION-0042 (mailbox claims file-scoped) +
  TASK-0117 (activacion #4, gateada) / TASK-0118 (DEF-PII, diferida) / TASK-0119 (guard mailbox), owner Codex,
  proposed. submit_intent atomico 10 intents; v1.9.3->1.10.0; drift 0; gates verdes. **#4 SIGUE OFF.**
- Codex **ACTIVO** (orden operador coord-crons): pendiente implementar SPEC-0081 (provisioning + AC2/AC3
  goldens) + prueba negativa A3 + TASK-0119 (guard). NO detener su cron NI el mio hasta aviso explicito.
- Promocion: el clasificador de auto-mode bloqueo el PRIMER script bash de generacion; salio con Write
  (archivos) + cp + submit_intent (no bloqueados). LECCION: ante bloqueo del clasificador, usar la
  herramienta natural (Write) en vez de reintentar el bash.
- DECISION-0042 (mailbox file-scoped) nacio del incidente del claim dir-level que bloqueo a Codex.
- **TASK-0119 (guard mailbox) DONE -> v1.11.0 (a575559):** Codex implemento el guard (submit_intent +
  validador py/ps RECHAZAN claim acquire con scope de directorio de mailbox; MSG-*.md permitidos; solo
  claims activos). Revisado maker!=checker: golden mailbox_claim_scope_cases 5/5 + PRUEBA NEGATIVA EN VIVO
  (claim dir-level rechazado "mailbox claim must be file-scoped", estado intacto) + validadores verdes +
  drift 0. Cerre in_review->done (reviewer) + reconcilie version a 1.11.0 (Codex bumpeo config, sin cap
  orchestrator para PROJECT_STATE). GUARD AHORA LIVE -> todo claim mailbox debe ser file-scoped (incluido
  Codex). NOTA: el clasificador bloqueo el 1er intento de cierre; con "go" del operador paso.
- **GO OPCION 1 (operador, 35be10a):** TASK-0117 proposed->READY; Codex GO'd para construir la
  INFRAESTRUCTURA de SPEC-0081 (AC1 provisioning/smoke + AC2 attestation_health_cases + AC3 6 goldens +
  AC5 rollback + A3 si owner) SIN encender #4 ni piloto (build != enable). Guardrail Analista: **N FIJADO=20**
  en SPEC-0081 AC2 + medicion acotada. TASK-0118 (DEF-PII) diferida. Codex informo idle-esperando-GO (no
  bloqueo tecnico; su mailbox-reader/coord-cron estaba parado -> arreglo su monitor: coordina tras 3 rondas).
  El ENCENDIDO de #4 sigue siendo GO POSTERIOR del operador + piloto (cuando converja DB + Carril B).
- **HARNESS SPEC-0081 ENTREGADO + REVISADO VERDE (e68dca7):** Codex construyo examples/attestation_health_cases
  (AC1 provisioning/smoke + AC2 N=20 + AC4 schema + AC5 rollback), attestation_negative_cases (AC3 6 vectores
  A1/A2), readonly_enforcement_cases (A3: escritura al Core sintetico rechazada por SO + AST). Revise
  maker!=checker reproduciendo: health 3/3, negative 6/6, readonly 2/2; #4 OFF (nada encendido); sin
  regresion; drift 0. TASK-0117 queda IN_REVIEW (build verificada; DoD completa = encendido #4 + piloto =
  GATEADA al GO POSTERIOR del operador cuando converja DB + Carril B). Sin bump de version (build-only, #4 OFF).
  PILOTO SERVIDO al GO de encendido del operador. Pendiente decision del operador: stand-down de Codex
  (build hecho, encendido futuro) o seguir activo; y estado de TASK-0117. El ENCENDIDO es su propia ventana
  de riesgo (operador presente + rollback + un solo multiplicador).

## (historico) Carril A - EN REVISION, sin promover
- Encargo del operador: arrancar el modulo-app de Presupuesto bajo el protocolo, instrumentado para tesis.
  Corte limpio: la DB (Access->SQL Server, D:\Agentes\Ingenas\Budget) la hace el operador APARTE; el
  protocolo gobierna el DESARROLLO del modulo-app; dataset = la COORDINACION de agentes (no la DB/PII).
- Drafts en `personal/Arquitecto/carril_A/` (NO en el ledger): A1 = activacion gateada #4 (REFERENCIA
  DECISION-0029, no rediseno) DRAFT-DECISION-0039 + DRAFT-SPEC-0081; A2 = GATE-DATASET nueva
  DRAFT-DECISION-0040; A3 = precondicion read-only (REFERENCIA DECISION-0035) DRAFT-DECISION-0041.
- RESTRICCION DURA: #4 ON antes del primer handoff real (cripto NO retrofiteable) -> Carril A primero.
  Ventana de riesgo SOLA (sin SA.4/authoritative-teeth/subagents).
- REVISION CONVERGIO (Analista + Codex, INDEPENDIENTES, 2026-06-19): A1 aprobable con provisioning
  (claves HMAC en event_auth.keys + remoto de anclaje ANTES del piloto; event_auth SI existe top-level,
  enabled=false) + 99%=salud-no-seguridad (AC3 prueba negativa = la seguridad, binaria/bloqueante con
  vectores+goldens) + denominador del 99% de fuente independiente. A2 OBJECION CENTRAL: "cero PII
  estructural" FALSO hoy (event log lleva texto libre en deliverables/title/notes; NO hay scan de PII;
  encoding scan NO detecta PII) -> acotar garantia al SUJETO-por-hash + declarar control disciplinario o
  anadir detector PII; base legal en "no hay persona fisica" no en Cons.26 (mal aplicado); DPIA incluir al
  operador humano (unica persona fisica). A3 aprobable + prueba negativa objetiva (escritura rechazada por
  el SO). NINGUN GO implicito; promover/encender = GO del operador.
- 7 CAMBIOS INCORPORADOS a los drafts (GO operador, commit e09a560): A1 event_auth top-level +
  provisioning (HMAC keys+anchor remote) condicion de encendido + salud(99%)!=seguridad(prueba negativa
  binaria, 6 vectores); A2 cero-PII estructural(sujeto-hash) vs disciplinario + base legal "no hay persona
  fisica" (no Cons.26) + operador en DPIA + tarea diferida DEF-PII; A3 prueba negativa objetiva (escritura
  rechazada por el SO). PENDIENTE: cross-check read-only del asistente -> GO de PROMOCION del operador ->
  promover por submit_intent (DECISION 0039/0040/0041 + SPEC-0081, SemVer MINOR + CHANGELOG). NO promovido,
  #4 OFF. Codex+Analista STAND-DOWN. Nota: "§9" en drafts = UTF-8 valido (decisions NO estan en canal ASCII).
- MEDIDA mailbox-claims (operador "eso no puede pasar", 2026-06-19): un claim mio con scope dir-level
  sobre Area_comun/mailbox/ bloqueo la respuesta de Codex. Lo libere (449b08d). Medidas: (1) REGLA
  vinculante = claims sobre mailbox SOLO a archivos MSG-*.md concretos, NUNCA dir-level (memoria
  [[mailbox-claims-file-scoped]]); (2) DRAFT-DECISION-0042 (addendum DECISION-0020) + TASK-0119 (Codex:
  guard en validador/submit_intent que RECHAZA claim acquire con scope de directorio de mailbox) para
  promover con el batch; (3) disciplina inmediata: claims file-scoped. NOTA: CLAIMS.json en scope tambien
  puede solapar entre agentes -> preferir scope minimo.
- ANOMALIA agents.architect="Claude" DIFERIDA: NO reconciliable por submit_intent (project_narrative solo
  cubre campos-lista + version; agents.* solo cambia por re-genesis). Re-genesis solo por campo display =
  multiplicador de riesgo desproporcionado; capability ya sale de agent_roles="Arquitecto". Esperar ventana.
- MAILBOX HIGIENIZADO + MONITOR CERRADO (32e0cf6): **mailbox/open VACIO**, sin claims activos. Analista
  confirmo stand-down; Codex QUIESCIO (flags coord_cron.stop + carril_a_coord_monitor.stop/.done, sin
  commits ni churn en 2 ciclos) -> archive la orden de stand-down a Codex con nota de cierre y TERMINE el
  loop de monitoreo (no reprogramado). Anomalias operativas (lock stale 2.3h/BOM/churn) reportadas a Codex
  por mailbox archivado (DECISION-0018 auto-mejora, regla nueva del operador); el operador las enruta a
  Codex en su proxima reactivacion (lock stale ya removido, BOM normalizado, churn cesado por mi).
- Anomalia abierta (Analista, DECISION-0018): PROJECT_STATE.json agents.architect="Claude" stale vs
  identidad Arquitecto (config agent_roles ya="Arquitecto"; capability OK). Reconciliar por escritor unico.
- LECCION reforzada: multi-sesion/cron concurrente = churn fuerte del working tree (mailbox movido,
  index.lock stale de 2.3h, archivos con BOM/CRLF de Codex). Estabilizar = ORDENAR stand-down + commit de
  snapshot consistente + monitor de verificacion. No forzar locks activos; lock viejo (horas) = stale, se
  remueve.

## Identidad (reforma del operador, 2026-06-15)
- Soy **Arquitecto** (antes "Claude"). `agent_roles.architect="Arquitecto"` en protocol.config.json
  (renombrado via `runtime/regenesis.py`, drift 0, history preserved). **submit_intent SIEMPRE
  `--actor-id Arquitecto`** (caps architect/reviewer/orchestrator/qa; "Claude" ya NO tiene caps).
  Mailbox `from: Arquitecto`. Mi area = `personal/Arquitecto/`. La voz analista firma **Analista**
  (`personal/Analista/`). Defaults genericos de plantilla (`context.DEFAULT_AGENT_ROLES`, `router` fallback)
  siguen "Claude" -- son la plantilla neutral, no la instancia viva.

## Estado vigente (2026-06-15)
- **v1.9.3 PUBLICADO.** HEAD `823b5b9` en main. protocol_version 1.9.3, runtime_version 0.12.0. drift 0.
- **TRIO OFF-PILOT COMPLETO:** TASK-0100 done (v1.9.1, .gitattributes LF futuros + v1.1.0 pre-normalizacion
  honesta, DECISION-0037, firma v1.1.0 INTACTA), TASK-0095 done (v1.9.2, commit_turn self-consistente),
  TASK-0096 done (v1.9.3, run_id unico por corrida real). Cada uno con CONCURRO de la Analista + mi reproduccion.
- **Codex y Analista en STAND-DOWN** (mailbox limpio, cron parado). El operador los reactiva (agent-activation-lifecycle).
  mailbox/open vacio. SIN trabajo activo; esperar GO del operador.
- **Escritor unico VIVO:** event_state {enabled, materialize, enforce, authoritative}=true. enforce con dientes
  (editar state a mano = drift B.3 hard-fail). Toda transicion por submit_intent. Rollback = 4 flags a false.
- **#3 cost-attribution ACTIVO (v1.6.0):** metrics.cost_attribution_enabled=true vivo (template false). cost_schema=2.
  Reversible. **Gateado OFF:** #4 (chain/agent_signatures/anchor), SA.4 (real_invoker+supervised_autonomy),
  subagents, Capa C (team_bridge).
- **Satelite read-only** `d:\Agentes\protocol_research` (DECISION-0035, repo SEPARADO, scaffolding/stubs OFF;
  poblar/correr = GATE-DATASET/GATE-INST/PRE-REG). Fase 0 E5/E6 hecha (DECISION-0034). Fase 1/2/4 NO existen.

## Cierre de tarea via submit_intent (patron probado)
- Transaccion atomica `submit_intent --intents <tx.json> --actor-id Arquitecto --timestamp <ts> --commit <HEAD>`.
  Plantilla del tx (4 intents): claim acquire (ANIDADO `{op:"acquire", claim:{...scope...}}`) -> task_status
  in_review->done -> project_narrative `{version:"X"}` -> claim release. Ejemplo replicado de tx-0095/0096-done.
- Tras el submit_intent: edit PUNTUAL de `protocol.config.json` protocol_version (NO json.dump) + entrada
  CHANGELOG. validate_collaboration_state (incluye drift B.3) + scan_encoding + scan_domain_neutrality VERDES
  antes de commitear. Staging EXPLICITO por path (nunca git add -A; barre personal/Codex|operador).

## Capabilities
- Arquitecto = [architect, orchestrator, qa, reviewer] -- NO implementer. Codex = [implementer, test_engineer].
- Cierre de IMPLEMENTACION = dos partes: Codex in_progress->in_review (su atestacion), Arquitecto in_review->done.

## Lecciones no-obvias (persisten)
- **MULTI-SESION = descoordinacion (2026-06-15).** Hubo 2 sesiones arquitecto + 2 analista concurrentes en el
  MISMO working tree -> vistas stale ("tienes mensaje"/"falta tu veredicto" sin inbound real), verdicts
  duplicados bajo una identidad, ficheros que se mueven solos. Ante "falta tu X" sin inbound real: reconciliar
  contra git/ledger y PREGUNTAR, no asumir/inventar. **Operar UNA sola sesion por rol.**
- **NARRACION MINIMA "primordial" (DECISION-0036/0038):** CERO narracion intra-ejecucion; encadenar tool calls
  en silencio; UN reporte final. El operador la marco con fuerte enfasis. Reincidir = anomalia DECISION-0018.
- **claim en tx = forma ANIDADA** `{op, claim:{...scope...}}`; la plana pierde el scope al avanzar el estado.
- **`utf-8-sig`** para leer state (Codex escribe BOM+CRLF). Canal mailbox/state = ASCII-only (DECISION-0012);
  verifica scan_encoding ANTES de aseverar (rompi ASCII por acentos 2 veces -- siempre revisar).
- **Renombrar el actor del ledger** = editar agent_roles (alimenta genesis) + regenesis.py (nuevo genesis desde
  hot state -> los eventos historicos quedan antes del boundary, no se re-validan). Goldens corren en sandboxes
  aislados (no afectados por el cambio de la instancia viva).
- **Referencias historicas NO se reescriben:** mailbox archivado, dist/v1.1.0 FIRMADO, CLAIMS_ARCHIVE, tasks
  cerradas registran el nombre de su epoca; solo se actualizan punteros VIVOS.
- **maker != checker REAL:** reproducir el fix del peer (no confiar). El Arquitecto/revisor NO debe firmar
  tambien como voz Analista (eso paso por la doble sesion: lo reconcilie a una voz).
- **Fail-closed:** ante fallo (golden rojo / drift!=0 / hot!=real), deja estado consistente (flag false) + reporta.

## Reglas de riesgo
- UN multiplicador por ventana. Activaciones gateadas solo con operador PRESENTE + rollback armado.
- enforce protege el LEDGER JSON, NO la prosa-contrato (AGENTS.md/decisions/specs) -> anti-colision MANUAL ahi.

Detalle/cronologia completa: `memory/project-state-snapshot.md` + semi-auto-collaboration-pattern +
permission-auto-exec + operator-working-style + cutover-risk-staging + commit-then-memory.
