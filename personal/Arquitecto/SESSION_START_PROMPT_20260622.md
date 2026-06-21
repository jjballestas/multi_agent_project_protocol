# Prompt de inicio del Arquitecto (cold-start) - 2026-06-22

> Nota: el HEAD de este encabezado es 4f81609 (cuando lo escribi). Tras commitear este propio prompt el
> canonico avanza: al arrancar usa `git fetch origin` + `git rev-parse origin/main` para el HEAD real.

Canonico GitHub HEAD 4f81609 (origin/main==HEAD). v1.14.0, enforce/auth #4 ON, drift 0, validate exit 0
(VERDE, con y SIN secretos en clon limpio). Repo protocolo (gobernanza+dataset): `D:/Agentes/multi_agent_project_protocol`.
Repo producto (front): `D:/Agentes/Zeus/Zeus-protocol` (commits LOCALES TASK-0140..0149; **push de Zeus al remote
GATEADO al operador**).

## Quien soy
Arquitecto Orquestador. maker=Codex (vivo, reactivable por el operador) / checker=Arquitecto. Reglas: CLAUDE.md +
AGENTS.md. Area personal: `personal/Arquitecto/`. Memoria viva: `~/.claude/.../memory/project-state-snapshot.md`.

## Estado
**Proyecto-front (Zeus-protocol) = T0 / proyecto primario de tesis (DECISION-0049).** El operador opera nova.budget
DESDE el front, montando requisitos por el INTAKE gobernado (RF-14, relay acotado firmado por Arquitecto en nombre
del Operador; anti-impersonacion AC19; DECISION-0051/0052). Auto commit+push (DECISION-0054) y carga por archivo
(DECISION-0055) existen OFF-by-default, activables por ENTORNO (versionado enabled:false; env
AUTO_COMMIT_PUSH_CONFIG_PATH / FILE_INGESTION_CONFIG_PATH -> *.runtime.json gitignored).

**TODO LO ENCOLADO ESTA CERRADO. Cola de trabajo VACIA.** Cerrado recientemente:
- 4 requisitos del 1er intake: TASK-0135 (reset+confirm), TASK-0137 (Help), TASK-0138 (mailbox-archive,
  DECISION-0053), TASK-0139 (auto commit+push, DECISION-0054). done.
- 9 requisitos del 2do batch (8 UX + ingestion), TASK-0140..0148 done: AC29 refetch-al-navegar, AC30
  frescura/staleness, AC31 tooltips-badges, AC32 tooltips-RF-N/acronimos, AC33 Mermaid-en-Help (sin dep npm),
  AC34 tipografia, AC35 kanban-colapsar/done, AC36 filtros-Ledger, AC37/AC38 carga-por-archivo (ingestion
  gobernada OFF-by-default, Analista OK + fix CRLF). Todos ext SPEC-0086.
- Defecto del Intake: TASK-0149 / REQ-643B160A done (AC39: el EXECUTE rechaza server-side narrativa/aceptacion
  vacias o ==placeholder, sin preview-as-green; exige proyecto explicito, no default a Zeus; los rechazos no
  crean fantasma). Remedia el fantasma REQ-984A85C6 (cancelado por prune).

## Cola / pendientes
- **Cola VACIA.** Si el operador monta nuevos requisitos por el intake (type:requirement, proposed), triagear +
  autorar SPEC (yo autoro SPEC con AC+test_plan; intake=semilla), SDD, maker=Codex/checker=Arquitecto, drafts
  para ratificacion, de a UNA.
- **PENDIENTE OPERADOR (su accion):** push de Zeus-protocol al remote (commits locales TASK-0140..0149); el
  clasificador bloquea push a remote externo, lo hace el operador.
- File ingestion / auto-push: encendido VIVO = el operador exporta el env runtime (pre-auth de ingestion ya
  registrada; auto-push se arma por env, versionado OFF).

## Reglas transversales (operador)
#4 epoca 1.14.0 BYTE-IDENTICA (no bumpear config; un bump real = re-genesis-boundary coordinado); neutralidad de
dominio en el core; carry AC11/12/13 + AC18/19/20 donde haya escritura; gates validate con/SIN secretos exit 0,
drift 0, npm test verde EN CLON LIMPIO; TODA superficie de escritura/ingreso nueva = DECISION + threat-model +
prueba negativa de impersonacion + OFF-by-default + Analista al cierre; reporta drafts de a UNO. nova.budget es
de OTRO proyecto (NOVA); fuera de Zeus-protocol.

## Lecciones operativas clave
- **CHECKER reproduce Zeus npm test DESDE CLON LIMPIO, no in-place** (el working tree puede ocultar fragilidad
  CRLF/eol; el Analista lo destapo en TASK-0148). Zeus tiene `.gitattributes eol=lf`; gate DECISION-0037.
- COMMIT gateado por EXIT del validador (no encadenar && tras un echo). Al promover/cerrar via submit_intent:
  COMMITEA EL SNAPSHOT COMPLETO junto (state + runtime/state + task/seed file + SPEC/codigo + mailbox); el clon
  limpio valida desde git HEAD.
- Cierre in_review->done = capability reviewer (la tengo); requirement proposed->done o ->cancelled = task_upsert
  capability ORCHESTRATOR (la tengo); NO editar el task file a done ANTES de aplicar el ledger.
- Anti-colision con Codex vivo: si Codex tiene CLAIM ACTIVO (in_progress) NO escribas el ledger ni commitees en
  su ventana (el task_upsert choca 'overlaps active claim'); espera a que libere. Re-leer estado tras SETTLE
  antes de declarar anomalia (un read a media escritura miente: in_progress->in_review aparece luego).
- task_status a done requiere implementer (solo Codex); por eso requirements se cierran con task_upsert(done).
- MSG rr=true SIEMPRE lleva requested_action + question; NO citar el literal requires_response:true en el CUERPO
  (usar rr=true) o el validador se dispara sobre tu propio msg. Tras git-mv de un mensaje, `git add` la ruta
  DESTINO (git mv stagea el blob del indice, no la edicion de status).
- Codex commitea bajo la identidad git del operador (autonomo); commit como Arquitecto + Co-Authored-By: Codex.
- ARMAR superficie credential-bearing/egress (push vivo, ingestion viva) = autorizacion ESPECIFICA del operador,
  no un 'go' generico; el clasificador bloquea el flip y hay que confirmar, no rodear. Activacion = RUNTIME por
  env, versionado OFF (NO commitear enabled:true en el config versionado; rompe el invariante off-by-default
  testeado y la suite).
- Autodrive: si el operador pide monitoreo, cron cada ~5min (session-only); de a UNA tarea; parar a 7 rondas
  seguidas sin actividad de Codex; al terminar la cola, stand-down a Codex + CronDelete + FYI.

## Al arrancar
`git fetch origin`; confirmar HEAD==origin, validate con/sin secretos exit 0, drift 0; revisar
`Area_comun/mailbox/open/` + claims activos. Si hay requisitos nuevos en proposed -> triagear/autorar SPEC.
Si el operador pide retomar autodrive -> re-armar cron. Canal ASCII.
