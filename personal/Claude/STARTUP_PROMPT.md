# STARTUP PROMPT - Claude (arquitecto) - multi_agent_project_protocol

Pega esto como primer mensaje al iniciar otra sesion de Claude en este repo.

---

> UPDATE 2026-06-09 (HEAD 0d9bb07, drift 0 seq 181) — LO MAS VIGENTE, manda sobre lo de abajo:
> SANDBOX_OK paso esta sesion (PowerShell limpio post-restart). RATIFICACION TASK-0093 CERRADA =
> **changes_requested** (RECHAZADA, NO done). El mecanismo gap-8 (acquire_routed_claim) esta bien y
> aceptado, pero FALLA el DoD explicito de SPEC-0070 §2.4+§4.1+Q2 = **release-on-rejection**: el claim
> que el orquestador adquiere queda HUERFANO (active) en todo path de rechazo (unreported/validate/
> budget/human_gate) que hace break ANTES de apply; with_terminal_claim_release solo cubre el GREEN
> terminal. CONFIRMADO con probe committed: personal/Claude/probe_task0093_release_on_rejection.py.
> El operador eligio REJECT sobre accept+followup. Ejecutado por submit_intent (reject_review
> in_review->changes_requested = capability reviewer) + finding accionable a Codex en
> mailbox/open/MSG-20260609-Claude-to-Codex-task0093-changes-requested.md (requires_response). Commit
> 0d9bb07 pusheado. SECUENCIA: el operador empuja a Codex (PUSH-DRIVEN) -> Codex reclama TASK-0093
> (changes_requested->claimed) e implementa release-on-rejection + goldens -> entrega in_review ->
> RE-RATIFICO (su golden + mi probe como regresion + 51 regresiones + validador/drift) -> si verde
> CIERRO -> SMOKE REAL end-to-end -> GO operador al re-fire SA.4. SA.4 sigue DE-ARMADO; enforce/
> authoritative ON; Capa C OFF. (El resto del documento describe el camino previo al rechazo.)

Retoma como arquitecto (Claude) de multi_agent_project_protocol.

COLD-START: lee AGENTS.md seccion 0 + Area_comun/state/*.json (con utf-8-sig: Codex escribe BOM/CRLF; al
escribir usar utf-8 + ensure_ascii=False, ASCII-only) + Area_comun/mailbox/open/ + mi memoria (MEMORY.md,
linea project-state-snapshot = estado vigente; la ENTRADA 2026-06-09 al final del snapshot es lo vigente).
CHEQUEA CLAIMS.json antes de escribir cualquier ruta compartida. ASCII-only en mailbox/state (DECISION-0012).
Mi area personal = personal/Claude/ (DECISION-0016). NUNCA commitear areas personales de OTROS
(personal/operador/, personal/Codex/) -> staging de rutas EXPLICITAS, nunca `git add -A`/dir amplio.

ESTADO VIGENTE (2026-06-09, HEAD 720b417 en main; v1.1.0; protocol_version 1.1.0, runtime_version 0.11.0;
drift 0 seq 174). NOTA: esta sesion se REINICIO para que Codex/extension tomen el fix de sandbox (ver abajo).
AL VOLVER: 1ro `Write-Output SANDBOX_OK` debe pasar (si no, el fix no quedo / falta restart).

>>> ESCRITOR-UNICO VIVO Y CONSOLIDADO <<<
- event_state = {enabled, materialize, enforce, authoritative} TODOS true. enforce TIENE DIENTES: editar
  Area_comun/state/*.json A MANO = drift HARD-FAIL (gate B.3). TODA transicion de estado va por
  `runtime/submit_intent.py` (intents: task_status, task_upsert, claim, decision, project_narrative,
  protocol_prune); cierres multi-paso = UNA transaccion atomica `submit_intent --intents`. drift 0 sostenido.
  authoritative=true es MARCADOR DECLARATIVO (sin callers de comportamiento distintos; la garantia escritor-unico
  la da ENFORCE). ROLLBACK del escritor-unico = poner los 4 flags a false (lossless, ensayado).
- maintenance.enabled=true (prune reencauzado por submit_intent en instancia viva; template intacto).
- CAPABILITIES (clave operativa): la capability requerida sale del CONTENIDO del turno/intent, NO del owner.
  Claude = [architect, orchestrator, qa, reviewer]; Codex = [implementer, test_engineer]. Claude PUEDE:
  task_upsert, task_status in_review->done (reviewer), claims propias, project_narrative, protocol_prune,
  decision. Claude NO PUEDE: editar archivos / task_status ->in_review/->done/->blocked / ready->in_progress
  (todo eso exige IMPLEMENTER). Para holds/cierres de tareas implementer, usa task_upsert.

ESTADO DONE (historico consolidado):
- v1.0.0: nucleo Fases 1-4 + Capa A + Fase 5 + D0 motor + D2 (tiers) + wrapper LLM + anti-colision. Paraguas
  TASK-0038 (N-agente) cerrado. Fase B (writer-vivo) completa.
- FASE 7 COMPLETA (release eng): SBOM/manifiesto+verify/provenance/firma/docs (RELEASE_ENGINEERING.md).
- AUTONOMIA SUPERVISADA documental SA.1-SA.5 COMPLETA (sobre+max_turns+runreport, kill-switch PAUSE+wall_clock,
  checkpoint humano por K turnos, docs SUPERVISED_AUTONOMY.md). Todo OFF-BY-DEFAULT.
- DECISION-0025 (Agent Teams bridge) promovida SOLO Capas A+B (sombra/aditivo/drift benigno); Capa C diferida.
  TASK-0083 (bridge A+B, runtime/team_bridge.py) DONE; team_bridge.enabled=false (OFF).
- DECISIONES: 27 en ledger. DECISION-0026 = regla de oro: ACTUALIZAR MEMORIA TRAS CADA COMMIT (todos los
  agentes). DECISION-0027 = activacion piloto SA.4.
- Proximos IDs: TASK-0093 / SPEC-0070 (verificar en TASK_INDEX al entrar).

>>> ASUNTO ABIERTO PRINCIPAL: gap-8 YA ARREGLADO (TASK-0093) - estoy MID-RATIFICACION + smoke pendiente <<<
- gap-8 (paso claim NO-OP del orquestador) FIX IMPLEMENTADO por Codex: TASK-0093 (SPEC-0070, opcion 1),
  commit d6569f4 "fix(runtime): acquire routed claims before turns", status in_review, claim liberado.
  Cambios: orchestrator.py `acquire_routed_claim` en el paso claim (antes del adapter): reusa claim activo
  owner+task si existe (idempotente -> byte-equiv goldens con pre-claim), si falta lo adquiere por
  submit_intent con actor_id=owner (owner==actor pasa validate_scope_authority), si submit_intent falla por
  conflicto -> rechaza el turno ANTES del adapter (cero commit). apply.py `with_terminal_claim_release`
  inyecta release del claim cuando el outcome/transition es terminal (in_review/done/blocked) y el report no
  lo trae (handoff-release, section 7). llm_adapter build_prompt: "do not include transitions.claims" (sin
  doble-acquire). 3 goldens nuevos en runtime_loop_cases (sin-pre-claim aceptado / pre-claim sin acquire extra
  / claim ajeno rechazado). Handoff: Area_comun/handoffs/HANDOFF-TASK-0093-codex-to-claude-1.md.
- MI RATIFICACION (en curso, reproducida): 51 goldens verdes (runtime_loop 11, SA 9, real_adapter 4,
  llm_adapter 6, intent_flow 11, wrapper 10) + validador/neutralidad/encoding verdes + drift 0. Diff revisado.
  >>> HALLAZGO ABIERTO A CONFIRMAR (release-on-rejection): el claim se adquiere ANTES del turno; en los paths
  de RECHAZO por gate/validate (unreported worktree change / validate-error / gate-not-green en apply), el
  orquestador NO libera el claim adquirido -> posible CLAIM HUERFANO + worktree dirty (rompe el cero-footprint
  que tenia el piloto). `with_terminal_claim_release` solo cubre el path GREEN terminal, no las rechazos.
  ANTES DEL VEREDICTO: confirmar con un golden adversarial (acquire-exitoso -> turno rechazado por scope) si
  el claim queda huerfano; si se confirma -> finding a Codex (blocked-with-finding) O aceptar con follow-up +
  el checkpoint humano del piloto lo caza. Los OTROS puntos (idempotencia, conflicto-rechazo, handoff-release,
  reconciliacion sin doble-acquire) los doy por buenos. La paridad .ps1 / drift-0-bajo-authoritative del
  acquire NO la cubren los goldens (event_state off) -> lo cubre el SMOKE REAL.
- SANDBOX FIX APLICADO (operador): C:\Users\johnb\.codex\config.toml `[windows] sandbox` elevated -> unelevated.
  Causa raiz: os error 740 (ERROR_ELEVATION_REQUIRED) - el setup refresh del sandbox de Windows exige elevacion
  que ni el app-server background ni codex exec no-interactivo consiguen. Correlacion con la INSTALACION DEL CLI
  confirmada (config.toml global reescrito hoy con elevated, lo leen CLI + extension). unelevated = ACL-based,
  no requiere admin. POR ESO se reinicio la sesion. AL VOLVER: `Write-Output SANDBOX_OK` debe pasar.
- CODEX ES PUSH-DRIVEN (hecho operativo, operador 2026-06-09): su lazo NO auto-ejecuta; solo corre cuando el
  operador lo empuja ("tienes mensaje"). NO asumir "ready+GO => Codex auto-reclama"; el disparador es el push.
  Follow-up: eximir mailbox/ del auto_claim de Codex (lockea el canal de coordinacion; smell DECISION-0020).
- SECUENCIA RESTANTE (mi turno, tras restart + SANDBOX_OK): (1) confirmar el hallazgo release-on-rejection
  (golden adversarial); (2) VEREDICTO de ratificacion; (3) cerrar TASK-0093 (reviewer in_review->done por
  submit_intent + handoff->archived + FYI accept) si verde, o devolver finding; (4) SMOKE REAL end-to-end
  (orquestador adquiere claim -> codex edita README -> gate ACEPTA), AHORA viable con sandbox unelevated; el
  invoker codex confirmado vivo (PONG); (5) reportar al operador para GO al re-fire SA.4.
- SA.4 SIGUE DE-ARMADO (runtime.real_invoker.enabled=false + supervised_autonomy.enabled=false). DECISION-0027
  vigente; caps {max_turns:2, human_checkpoint_every_k:1, wall_clock_ms:180000}, PAUSE, budget+deadline.
  enforce+authoritative INTACTOS ON. Capa C OFF. PILOTO-1 (invoker claude) valido el SOBRE (rechazo limpio).
  El re-fire es EL UNICO MULTIPLICADOR; solo con GO del operador + sandbox verde + ratificacion cerrada.

>>> REGLAS DE RIESGO (innegociables) <<<
- UN SOLO MULTIPLICADOR DE RIESGO POR VENTANA: NUNCA enforce + SA.4 + Capa C juntos. Cada uno testeable y
  reversible por separado.
- Activaciones gateadas (SA.4 re-fire, Capa C del bridge): SOLO con el operador PRESENTE, con rollback armado.
  No en tick desatendido.
- enforce protege el LEDGER JSON (drift=hard-fail) pero NO los archivos de PROSA-contrato (AGENTS.md/CLAUDE.md/
  decisions/specs/protocol/reportes) -> ahi la anti-colision sigue MANUAL: git diff antes, STAGING DE RUTAS
  EXPLICITAS (nunca git add -A que barra al peer/operador), revisar git diff --cached.

LAZO DE TRABAJO (semi-automatico):
- Codex AUTONOMO (~100s): auto-reclama `ready` (via submit_intent), ejecuta, poda, detecta anomalias
  (DECISION-0018). Release atomico = handoff + in-review + claim liberado + flip status. Si lo cazas mid-release:
  espera, no toques. A veces commitea su entrega en background.
- Yo (Claude) reacciono via ScheduleWakeup: al ver in_review + claim liberado, RATIFICO ADVERSARIAL (corro YO
  el golden de la tarea + regresiones + validador/encoding/neutralidad + smoke; leo el codigo nuevo), flip a
  done por submit_intent, in_review->archived + FYI accept (RE-APUNTAR el deliverable del msg in-review a
  mailbox/archived/ tras moverlo, o el validador falla 'deliverable missing'), claim efimero, promuevo la
  siguiente de a una con GO+ETA, commit (paths explicitos) + push, ACTUALIZO MEMORIA (DECISION-0026).

PERMISOS (settings.json auto-allow cd/python/git add,rm,tag,restore,commit,push/grep/etc.): el harness pide
prompt para comandos COMPUESTOS (varios `&&`, multilinea) y `-m` con SALTOS DE LINEA -> emitir UN comando por
Bash; commits con DOS flags `-m`. Heredocs/loops bash pueden auto-irse a background (output a veces no se
captura) -> preferir scripts _tmp_*.py en personal/Claude/ o driver python inline. Ver [[permission-auto-exec]].

QUE HACER AL ENTRAR (tras el restart):
1. Cold-start + RE-LEER state files en disco. PRIMERO `Write-Output SANDBOX_OK` (debe pasar; si no, el fix de
   config.toml unelevated no quedo o falta restart -> avisar al operador). Verifica drift 0 (seq ~174+),
   TASK-0093 = in_review owner Codex. Revisa mailbox/open/ (mis RESPONSE a Codex sobre sandbox/liveness +
   FYIs informativos). Codex es PUSH-DRIVEN: no esperes que arranque solo.
2. RETOMAR LA RATIFICACION de TASK-0093 (es mi turno; ver ASUNTO ABIERTO arriba): confirmar el hallazgo
   release-on-rejection con un golden adversarial (acquire-exitoso -> turno rechazado por scope). Si el claim
   queda huerfano -> devolver finding a Codex; si no, o si se acepta con follow-up -> VEREDICTO -> cerrar
   TASK-0093 (reviewer in_review->done por submit_intent) -> SMOKE REAL end-to-end (sandbox ya unelevated) ->
   reportar al operador para el GO al re-fire SA.4.
3. NADA gateado/supervisado (SA.4 re-fire, Capa C) sin operador PRESENTE + rollback armado + un solo
   multiplicador. NO re-armar SA.4 ni disparar el piloto sin GO + ratificacion cerrada + sandbox verde.
   Cambios de protocolo/boundary -> DECISION + aprobacion humana.
4. Verifica antes de cualquier disparo: drift 0, activation_errors None, replay==hot, PAUSE ausente, SANDBOX_OK.

Detalle/cronologia: MEMORY.md (linea project-state-snapshot + ENTRADA 2026-06-09 al final del snapshot) +
semi-auto-collaboration-pattern.md + permission-auto-exec.md + operator-working-style.md + cutover-risk-staging.md
+ submit-intent-live-bug.md + commit-then-memory.md.
