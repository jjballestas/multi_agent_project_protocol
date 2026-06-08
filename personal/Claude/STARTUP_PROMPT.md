# STARTUP PROMPT - Claude (arquitecto) - multi_agent_project_protocol

Pega esto como primer mensaje al iniciar otra sesion de Claude en este repo.

---

Retoma como arquitecto (Claude) de multi_agent_project_protocol.

COLD-START: lee AGENTS.md seccion 0 + Area_comun/state/*.json (con utf-8-sig: Codex escribe BOM/CRLF; al
escribir usar utf-8 + ensure_ascii=False, ASCII-only) + Area_comun/mailbox/open/ + mi memoria (MEMORY.md,
linea project-state-snapshot = estado vigente). CHEQUEA CLAIMS.json antes de escribir cualquier ruta
compartida. ASCII-only en mailbox/state (DECISION-0012). Mi area personal = personal/Claude/ (DECISION-0016).
NUNCA commitear areas personales de OTROS (personal/operador/, personal/Codex/).

>>> CODEX DESACTIVADO POR EL OPERADOR HASTA LAS 9 AM (orden del 2026-06-08 noche). NO esperes entregas de
Codex hasta entonces. TASK-0082 (SA.5 docs) quedo `ready` con GO en mailbox pero NO sera reclamada hasta que
Codex vuelva. Mientras Codex este off: NO hay lazo de ratificacion; solo trabajo de arquitecto (drafts en
personal, reportes, preparacion) o lo que pida el operador. <<<

CONTEXTO (cierre 2026-06-08, HEAD 73a8610 en main, pusheado, tag v1.0.0): producto = metodologia multiagente
distribuible. v1.0.0 PUBLICADO. Post-v1.0 el operador fue desgateando por turno.

ESTADO ACTUAL (2026-06-08):
- DONE v1.0.0: nucleo Fases 1-4 + Capa A + Fase 5 (seguridad 5.1/5.2/5.3) + D0 motor (6.1 obs + 6.2 budget
  A10) + D2 completo (tiers DECISION-0019, upgrade tier-aware, docs, PACKAGE_VERSIONING) + wrapper LLM real
  (DECISION-0021) + DECISION-0020 (anti-colision) + fix prune. Paraguas TASK-0038 (N-agente) CERRADO.
- FASE B COMPLETA, writer-vivo EN MODO SOMBRA (end-state estable): protocol.config.json event_state.enabled=
  true + materialize=true; enforce=false + authoritative=false. Edicion manual del ledger SIGUE VALIDA;
  validador emite WARNING de drift al editar a mano = ESPERADO/BENIGNO. ROLLBACK = 4 flags a false. genesis
  POR REFERENCIA (snapshot_ref content-addressed en runtime/state/snapshots/<hash>.json). runtime/state/**
  exento de neutralidad (TASK-0070).
- FASE 7 COMPLETA (release engineering, SPEC-0057): F7.1 SBOM (TASK-0071) | F7.2 manifiesto+verify (TASK-0073)
  | F7.3 provenance SLSA-lite (TASK-0074) | F7.4 firma (TASK-0075, DECISION-0023; backend fixture HMAC para
  golden, claves reales del emisor NUNCA en repo, off-by-default) | F7.5 docs (TASK-0081 =
  Area_comun/protocol/RELEASE_ENGINEERING.md). Todas ratificadas adversarialmente.
- MIGRACION ESCRITOR-UNICO: AMBOS LADOS DEL CUTOVER EN CODIGO -> CODE-READY PARA ACTIVACION.
  * submit_intent TRANSACCIONAL `--intents` (TASK-0076, SPEC-0062): un cierre/encole multi-paso (status+claim+
    task_upsert+decision) como UNA transaccion atomica con rollback. + runtime/regenesis.py (genesis fresco por
    snapshot_ref -> drift 0, no destructivo, idempotente).
  * Mandato de protocolo (lado Claude): AGENTS.md/.template + TASK_PROTOCOL documentan el flujo transaccional +
    el gate de activacion AMBOS-LAZOS.
  * Cutover lado Codex (TASK-0077, SPEC-0063): runtime/ledger_ops.py (auto-claim + handoff-release via
    submit_intent --intents; claim release AL FINAL conservando scope) + golden cutover_loop.
- AUTONOMIA SUPERVISADA (DECISION-0024 APROBADA y promovida, SPEC-0064, off-by-default): SA.1 sobre+max_turns+
  runreport (TASK-0078) | SA.2 kill-switch centinela runtime/state/PAUSE + reloj wall_clock_ms (TASK-0079) |
  SA.3 checkpoint humano por K turnos / fix-cycles, sin auto-resume (TASK-0080). TODO en SHADOW, invoker real
  --once INTACTO. SA.5 docs = TASK-0082 (ready, GO dado, sin reclamar hasta que Codex vuelva).
- DECISIONES: 24 en ledger (0001-0024). DECISION-0025 (integracion agent-teams/bridge) = DRAFT del OPERADOR en
  personal/operador/, AUN NO promovida ni entregada a mi. Proximos IDs: TASK-0083, SPEC-0065.

>>> PENDIENTES SUPERVISADOS (autorizados pero requieren al operador presente; NO en piloto automatico) <<<
1. ACTIVACION ESCRITOR-UNICO: re-genesis del repo VIVO (drift 0) + flip enforce=true+authoritative=true +
   ENSAYO DE ROLLBACK. El operador YA AUTORIZO (2026-06-08). GATEADO TECNICAMENTE: tras el flip, la siguiente
   transicion de CADA lazo DEBE ir por submit_intent o hard-failea -> ejecutar SUPERVISADO con rollback listo,
   tras verificar que el lazo de Codex realmente usa submit_intent. Es el switch de MAYOR RIESGO.
2. SA.4 (autonomia con invoker real multi-turno bajo el sobre): levanta el cerrojo --once SOLO con registro+
   caps; requiere GO del operador + ensayo de rollback. Unico paso con efecto real nuevo de la autonomia.
3. DECISION-0025 (agent-teams-bridge): esperar a que el operador la entregue/promueva.

LAZO DE TRABAJO (semi-automatico, CUANDO CODEX ESTE ACTIVO):
- Codex AUTONOMO (~100s): auto-reclama `ready`, ejecuta, poda, detecta anomalias (DECISION-0018). Release
  atomico = handoff + in-review msg + claim liberado + flip status juntos; a veces commitea su entrega en
  background. Si lo cazas mid-release: espera, no toques.
- Yo (Claude) reacciono via ScheduleWakeup (~270s): al ver in_review + claim liberado, RATIFICO ADVERSARIAL
  (corro YO el golden de la tarea + regresiones + validador/encoding/neutralidad + smoke especifico; leo el
  codigo nuevo), flip a done, in_review->archived + FYI accept, claim efimero, promuevo la SIGUIENTE de a una
  con GO+ETA, commit + push. Mantener a Codex en cola NON-GATED (lejos del ledger durante activaciones).

ANTI-COLISION (DECISION-0020) y LECCIONES DE PROCESO:
1. Preparar specs/tareas en personal/Claude/ mientras Codex ocupado; promover de a UNA con GO+ETA.
2. Escrituras del ledger en UN script python atomico (_tmp_*.py en personal/Claude/, lee-modifica-escribe).
3. PERMISOS (clave): el harness pide prompt para comandos COMPUESTOS (varios `&&`, multilinea) y `-m` con
   SALTOS DE LINEA. -> emitir UN comando por Bash; commits con DOS flags `-m` ("subject" y trailer Co-Authored)
   para que quede en UNA linea. `git add a b c` (multi-arg, una linea) pasa. `Bash(rm:*)` ya en allowlist.
4. STAGING: si Codex IDLE, `git add -A` + commit (TRAS add -A: `git restore --staged personal/operador/
   personal/Codex/` para no commitear areas ajenas). Si Codex puede tener WIP staged: paths explicitos.
5. DELIVERABLE REPOINT: Codex lista el mensaje in-review como DELIVERABLE del task; al archivarlo (open->
   archived) el validador falla 'deliverable missing' -> en el close, RE-APUNTAR ese deliverable a
   mailbox/archived/ tras mover el mensaje.
6. Aserciones en mailbox verdaderas: FYI 'DONE' TRAS el flip; GO 'X ready' TRAS registrar X.

QUE HACER AL ENTRAR:
1. Cold-start. Si es ANTES de las 9 AM: Codex sigue OFF -> no esperes entregas; revisa si el operador dejo
   instruccion; si no, trabajo de arquitecto (drafts/reportes) o espera. Si es DESPUES de las 9 AM y Codex
   volvio: revisa si entrego TASK-0082 (SA.5) -> ratifica + cierra.
2. Reportes HTML del operador (Area_comun/reports/REPORT-20260607-estado-proyecto.html y
   REPORT-20260607-inventario-metodologia.html): actualizar cuando cambie el estado, si el operador lo pide.
   (Son artefactos-hoja de mi autoria; commit con path explicito, sin tocar CLAIMS.json).
3. NADA gateado/supervisado (activacion escritor-unico, SA.4) sin el operador PRESENTE. Cambios de protocolo/
   boundary -> DECISION + aprobacion humana.
4. Si el operador entrega DECISION-0025: leerla, ayudarle a formalizarla (es nueva direccion).

Detalle/cronologia: MEMORY.md (linea project-state-snapshot, estado vigente) + semi-auto-collaboration-pattern.md
+ permission-auto-exec.md (lecciones de permisos) + operator-working-style.md.
