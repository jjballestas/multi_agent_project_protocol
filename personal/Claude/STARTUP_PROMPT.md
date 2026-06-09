# STARTUP PROMPT - Claude (arquitecto) - multi_agent_project_protocol

Pega esto como primer mensaje al iniciar otra sesion de Claude en este repo.

---

Retoma como arquitecto (Claude) de multi_agent_project_protocol.

COLD-START: lee AGENTS.md seccion 0 + Area_comun/state/*.json (con utf-8-sig: Codex escribe BOM/CRLF; al
escribir usar utf-8 + ensure_ascii=False, ASCII-only) + Area_comun/mailbox/open/ + mi memoria (MEMORY.md,
linea project-state-snapshot = estado vigente; la ENTRADA 2026-06-09 al final del snapshot es lo vigente).
CHEQUEA CLAIMS.json antes de escribir cualquier ruta compartida. ASCII-only en mailbox/state (DECISION-0012).
Mi area personal = personal/Claude/ (DECISION-0016). NUNCA commitear areas personales de OTROS
(personal/operador/, personal/Codex/) -> staging de rutas EXPLICITAS, nunca `git add -A`/dir amplio.

ESTADO VIGENTE (2026-06-09, HEAD 89d140b en main; v1.1.0; protocol_version 1.1.0, runtime_version 0.11.0):

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

>>> ASUNTO ABIERTO PRINCIPAL: PILOTO SA.4 (autonomia con invoker REAL) BLOQUEADO por gap del orquestador <<<
- La cadena de invoker real esta CONSTRUIDA y FUNCIONAL: orchestrator -> preset -> runtime/llm_turn_wrapper.py
  (vendor-neutral; shutil.which; timeout<120s; extraccion JSON tolerante a fences/prosa + validacion turn_schema)
  -> backend CLI. Preset codex = `codex exec -s workspace-write -c approval_policy=never -c
  model_reasoning_effort=low --skip-git-repo-check` (low evita timeout del reasoning xhigh; ~44s). Solo Codex
  (implementer) puede hacer turnos de file-edit. codex CLI presente+autenticado (OAuth).
- AL DISPARAR EL PILOTO (invoker codex): el orquestador ruteo `execute` TASK-0091 y **codex EDITO el README
  real** (=> el invoker codex SI funciona para trabajo real), PERO el gate RECHAZO con "no active claim for
  report task_id and agent". RAIZ (8vo gap 'assumed-ready'): `orchestrator.py:482` el paso "claim" es un NO-OP
  (solo trace.append, NO crea claim); un turno `execute` asume la tarea YA reclamada (el golden
  llm_adapter_cases PRE-CREA un claim activo de Codex antes de correr; el report lo release-a). `select_ready_task`
  (router.py:176-196) rutea execute directo sobre ready SIN claim. Y Claude NO puede pre-crear un claim de Codex
  (claim acquire owner debe == actor_id). => el turno execute no tiene claim activo -> rechazo. El turno
  rechazado NO revierte el edit del agente (worktree quedo dirty; revertido con git checkout; drift 0, sin
  footprint de ledger).
- FIX PENDIENTE (decision del operador/proxima sesion), una de: (1) que el paso claim del orquestador realmente
  adquiera un claim para el owner ruteado ANTES del adapter; (2) rutear accion `claim` primero para ready sin
  claim (flujo 2-turnos claim->checkpoint->execute, encaja con el checkpoint_every_k=1 del piloto); (3) que el
  report del agente incluya claim-acquire y el orquestador lo aplique antes del gate. Es BLOQUEANTE del piloto
  SA.4 real-execute, NO del escritor-unico (ya vivo).
- ESTADO SEGURO AL CIERRE: SA.4 DE-ARMADO (runtime.real_invoker.enabled=false + runtime.supervised_autonomy.
  enabled=false; commit 89d140b). DECISION-0027 vigente; caps del sobre {max_turns:2, human_checkpoint_every_k:1,
  wall_clock_ms:180000}, kill-switch PAUSE, budget+deadline. enforce+authoritative INTACTOS ON. Capa C OFF.
  PILOTO-1 (invoker claude) ya habia validado el SOBRE (rechazo limpio, cero footprint) = safety de SA.4 OK.

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

QUE HACER AL ENTRAR:
1. Cold-start + RE-LEER state files en disco (Codex muta entre lecturas; la memoria puede quedar stale en una
   sola sesion). Revisa mailbox/open/ (hay 2 FYIs informativos abiertos: sandbox-spawn-flakiness de Codex y
   anomalia-task0092-resuelta mio a Codex; req_resp=false ambos).
2. Si el operador retoma el PILOTO SA.4: el fix del gap del orquestador (claim no-op) es PRE-REQUISITO. Discutir
   con el operador cual de las 3 opciones de fix; probablemente un TASK chico (Codex es implementer) + golden,
   luego re-armar + re-disparar el piloto con --llm-preset codex. NO re-armar SA.4 ni disparar sin GO + fix.
3. NADA gateado/supervisado (SA.4 re-fire, Capa C) sin operador PRESENTE + rollback armado + un solo
   multiplicador. Cambios de protocolo/boundary -> DECISION + aprobacion humana.
4. Verifica antes de cualquier disparo: drift 0, activation_errors None, replay==hot, PAUSE ausente.

Detalle/cronologia: MEMORY.md (linea project-state-snapshot + ENTRADA 2026-06-09 al final del snapshot) +
semi-auto-collaboration-pattern.md + permission-auto-exec.md + operator-working-style.md + cutover-risk-staging.md
+ submit-intent-live-bug.md + commit-then-memory.md.
