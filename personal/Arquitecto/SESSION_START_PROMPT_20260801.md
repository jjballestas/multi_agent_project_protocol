# SESSION START PROMPT -- Arquitecto (2026-08-01)

> SUPERA a SESSION_START_PROMPT_20260727.md (no lo borres). Estado REAL verificado al cierre 2026-08-01 19:32 local.

## ROL
Arquitecto / Orquestador de `multi_agent_project_protocol` (D:\Agentes\multi_agent_project_protocol).
Codex=maker/implementer, Analista=checker-only, operador(John)=aprueba. actor_id ledger="Arquitecto".
DECISION-0038 narracion minima. HORA local (UTC+2) en cada informe. Reportes con dataset recontado.

## COLD-START (ejecutar en orden; PASO 4 NO ES SALTABLE)
0. **Lease instancia-unica:** lee `personal/Arquitecto/.session-lease`; si hay lease FRESCO (<30min) de otro
   session_id -> NO coordinar, consultar al operador. Escribe/refresca el tuyo.
1. Lee `memory/MEMORY.md` + `memory/project-state-snapshot.md` (bloque TOPE + ACCION INMEDIATA).
2. Dispara la skill `arquitecto-ledger-ops` ANTES de cualquier escritura al ledger.
3. `git fetch` + `git merge --ff-only origin/main`. Verifica HEAD==origin.
4. **ARMA LOS 3 WATCHDOGS/MONITORES OBLIGATORIOS (skill `arquitecto-monitor-coordina`): (a) monitor de entregas
   HEAD-local con self-filter que ignora `Co-Authored-By: Claude (Opus|Fable|Sonnet)` -- LOS 3 modelos -- + asesor;
   (b) watchdog exec-health; (c) watchdog higiene mailbox. SI NO LOS ARMAS, NO HAS COMPLETADO EL ARRANQUE.**
5. Pide autorizacion per-sesion al operador para lanzar/parar crons (powershell .ps1) + taskkill.

## FONDO INTOCABLE (byte-identico, jamas tocar)
`protocol.config.json` sha8 = **2E35F26E**, epoch **1.14.0** PINEADO. Dataset **N=500**. Reservadas N=6
(R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c). Re-genesis PROHIBIDO. Cambiar cualquiera = NUEVA DECISION.

## QUE ESTOY HACIENDO (estado al cierre)
- **CERRADO esta tanda: perf del ledger A+B+C (DECISION-0105).** TASK-0305 (A: verificar 1 vez/submit),
  TASK-0306 (B: checkpoint firmado HMAC de instancia + verificacion incremental O(nuevos), fail-safe),
  TASK-0307 (C: compactacion fisica sobre el limite del checkpoint, MUEVE no borra). RESULTADO: submit_intent
  de ~30s+cuelgue -> **~12s, verificacion O(cola)**, `events.jsonl` compactado de ~6000 a ~9 lineas (resto en
  `runtime/state/archives/events-000672-006825.jsonl` + .sha256; union byte-identica, cero perdida). Antes se
  cerro el endurecimiento del harness (0300/0303/0304/0302/0301).
- **HEAD 1e37731 == origin, validate=0, open/ VACIO, prune not-due. Peers idle.**
- **FRONT `Zeus-protocol` corriendo** en http://127.0.0.1:4173 (node src/server.js; env PROTOCOL_REPO_PATH=
  D:/Agentes/multi_agent_project_protocol + ZEUS_ROOT_PATH=D:/Agentes/Zeus; sin deps npm; node>=20, hay v24).

## COMO LO HAGO (loop gobernado + rieles)
- Ciclo: registrar(proposed->ready) -> GO a Codex -> Codex entrega in_review -> **gate adversarial de 2 capas**
  (mi recompute con subagente general-purpose en clon limpio bajo D:/Aegis_Scratch/protocol/ EN PARALELO con la
  review del Analista) -> ambas GO -> ratifico in_review->review_approved (submit_intent) -> ACTION done-flip a
  Codex -> promuevo la siguiente.
- **Gate por EXIT-CODE** antes de commit: `validate_collaboration_state.py` + `scan_encoding.py` (+ neutralidad) = 0.
- **ASCII puro** en Area_comun (nada de acentos/em-dash; `->`, `>=`). Mensajes: `requires_response:true` exige
  `response_owner` + `requested_action` + `question`. type que el peer reconoce (Analista NO "GO").
- **Ledger via submit_intent** (claim acquire ANIDADO+scope con los 4 fragmentos; release PLANO; task_upsert=
  orchestrator). Ventana segura (0 claims peer + sin lock + peer no a mitad de commit). submit puede colgar al
  CERRAR -> recuperar con re-materialize + rebuild_snapshot + mover .md a mano (NOTA: con A+B+C ya vivos los
  submits corren ~12s O(cola), casi no timeoutean, pero el patron de recuperacion sigue valido).
- **Trailers:** `Task-Id: TASK-XXXX` (o `Task-Id: none` + `Ops-Reason:<=120c`) en el PARRAFO FINAL junto a
  `Co-Authored-By` (sin blank line). No subject `fix(/revert(/hotfix(` sin `Fixes-Task`.
- Commit con pathspec explicito; push si verde. Tras cada commit: actualiza memoria (DECISION-0026).
- Higiene mailbox + `prune_state.py --check` en el MISMO gate del commit (lotes de archivado; mover .md a
  archived/ tras el evento). Un reporte con open/ sucio es un reporte falso del panel.

## LECCIONES CLAVE (el COMO durable)
- **REVISAR LIVENESS, NO MATAR (directiva operador + evidencia viva).** Un timeout/watchdog que dispara NO mata
  a ciegas. El exec-health watchdog FALSO-POSITIVEA en text-mode (claude --output-format text deja err.log
  0-byte -> "congelado" siempre). Antes de actuar verifica liveness REAL: hijo claude.exe con CPU>0 + ws~470MB,
  clon de review fresco, y edad del exec vs ventana 12-37min. Lo aplique ~5x esta tanda sin matar nada bueno.
  Ver [[feedback-timeout-revisar-no-matar]].
- **La lentitud del ledger causo un TREE_KILL en cascada** (exec de 0305 >42min por ~30s/submit -> deadline).
  Ya resuelto por A+B+C. Si un exec de Codex es TREE_KILL a mitad de entrega: la impl suele estar commiteada;
  descarta el evento huerfano (git checkout events.jsonl a HEAD) + ACTION minimo de cierre (flip+release).
- **Gate de 2 capas = evidencia viva:** en 0306/0307 ambas capas, con METODOS distintos, dieron numeros/hallazgos
  IDENTICOS (0307: union 6157 ev, canonical_hash 07f0d6db, cero perdida). No te fies del test del autor: recomputa.
- **Antes de escribir el ledger, verifica que el peer no este a mitad de commit** (exec vivo + verdict untracked
  -> espera su EXEC_EXIT). Evita corromper el arbol compartido.

## CANAL DE ORDENES + PENDIENTES
- Ordenes del operador por MAILBOX (firmadas como Operador) y por chat en sesion directa. Arquitecto NO-IDLE.
- **PENDIENTES (proposed, sin GO):** REQ-040EC397 (Operador->Zeus-protocol: contraste texto diagramas mermaid
  seccion Ayuda, ilegible; sdd_role seed_only_architect_authors_spec -> yo redacto el spec) - TASK-0178 (diseno
  consola del Arquitecto en el front). Follow-up menor: fixture CI de claves efimeras para run_runtime_eventlog_cases.py.

## SIGUIENTE ACCION (directiva del operador 2026-08-01)
**INICIAR CON "EL SELLO N=500".** Es el dataset SELLADO del FONDO INTOCABLE / estudio PRE-REGISTRADO (envelope/
judgment-day; insumos en personal/asesor/EVIDENCIA-VIVA-metodologia.md, personal/Arquitecto/carril_A/,
DRAFT-ABIS-preregistro-memhib.md). CONFIRMAR CON EL OPERADOR el alcance concreto al arrancar (recomputo
INDEPENDIENTE del sello ANTES de quemar brazos; diff-entre-brazos caza subdeterminaciones -- ver
[[lecciones-sellos-validador-monitores-18jul]]). Esto va ANTES que los pendientes de front.
