# STARTUP PROMPT - Claude (arquitecto) - multi_agent_project_protocol

Pega esto como primer mensaje al iniciar otra sesion de Claude en este repo.

---

Retoma como arquitecto (Claude) de multi_agent_project_protocol.

COLD-START: lee AGENTS.md seccion 0 + Area_comun/state/*.json (con utf-8-sig: Codex escribe BOM/CRLF; las
state JSON viven sin BOM, escribir utf-8 + ensure_ascii) + Area_comun/mailbox/open/ + mi memoria (MEMORY.md +
project-state-snapshot.md, ULTIMA entrada = estado actual). CHEQUEA CLAIMS.json antes de escribir cualquier
ruta compartida. ASCII-only en mailbox/state (DECISION-0012). Mi area personal es personal/Claude/
(DECISION-0016). Permisos del lazo ya en .claude/settings.json (cd/python/git add,rm,tag,restore,commit,push/
grep/etc. auto-allow).

CONTEXTO (cierre 2026-06-07, HEAD 357950d en main, pusheado, tag v1.0.0): producto = metodologia
multiagente distribuible. v1.0.0 PUBLICADO. Despues, post-v1.0 (el operador fue desgateando por turno).

ESTADO ACTUAL:
- DONE v1.0.0: nucleo Fases 1-4 + Capa A + Fase 5 (5.1/5.2/5.3 seguridad) + D0 motor (6.1 observabilidad +
  6.2 budget A10) + D2 completo (tiers DECISION-0019, upgrade tier-aware, docs, PACKAGE_VERSIONING) + wrapper
  LLM real (DECISION-0021) + DECISION-0020 (regla anti-colision) + fix prune (condensa next_actions).
- FASE B COMPLETA (writer-vivo del ESTADO de protocolo, SPEC-0039/0052-0055): B.1 replay/drift read-only
  (TASK-0066) | B.2 materializacion opt-in (TASK-0067) | B.3 drift HARD-FAIL bajo event_state.enforce
  (TASK-0068) | B.4 runtime escritor autoritativo + GENESIS POR REFERENCIA (TASK-0069, DECISION-0022). +
  INTENT-FLOW submit_intent (TASK-0072, SPEC-0058) = write-path del estado via runtime (keystone del escritor
  unico). Paraguas TASK-0038 (N-agente) CERRADO.
- WRITER-VIVO EN MODO SOMBRA (decision del operador, end-state estable): protocol.config.json event_state.
  enabled=true + materialize=true; enforce=false + authoritative=false. EDICION MANUAL del ledger SIGUE
  VALIDA (el lazo no cambia). El validador emite WARNING de drift al editar a mano = ESPERADO/BENIGNO (no
  hard-fail). ROLLBACK = poner los 4 flags en false. runtime/state/** exento de neutralidad (TASK-0070).
  GENESIS = referencia (snapshot_ref {hash,commit,actor,timestamp,schema_version}; snapshot content-addressed
  en runtime/state/snapshots/<hash>.json FUERA del prompt; restriccion del operador).
- 3.b.2 ESCRITOR UNICO (enforce+authoritative) EN PAUSA: encenderlo exige que AMBOS lazos -incl. el autonomo
  de Codex- adopten submit_intent (dejar de editar JSON) + re-genesis sincronizado + GO del operador. NO
  encender sin eso (rompe el lazo). NO es decision unilateral de Claude.
- FASE 7 (release engineering, SPEC-0057, APROBADA) EN MARCHA, 5 rebanadas de a una: F7.1 SBOM DONE
  (TASK-0071); F7.2 manifiesto+verify DONE (TASK-0073); F7.3 provenance SLSA-lite EN VUELO (TASK-0074 ready/
  in-progress, SPEC-0060); F7.4 FIRMA (TASK-0075 listo en personal, SPEC-0061; DECISION-0023 ACCEPTED por el
  operador -firma del digest, claves del emisor NUNCA en repo, backend configurable, golden con clave fixture,
  off-by-default-; FALTA promover DECISION-0023 a Area_comun/decisions/ + PROJECT_STATE#decisions al cerrar
  F7.3); F7.5 docs+integracion (pendiente, cierra Fase 7).
- Drafts listos en personal/Claude/ para promover de a una: DRAFT-DECISION-0023-firma-release.md,
  DRAFT-SPEC-0061-faseF7.4-firma.md, DRAFT-TASK-0075-faseF7.4-firma.md.
- DECISIONES: 22 en ledger (0001-0022); DECISION-0023 aprobada, sin promover. Proximos IDs: TASK-0076, SPEC-0062.
- GATEADA (post-Fase 7): autonomia supervisada (lazo encadenado de agentes reales + barandales Fase 5/budget/
  gate + paradas humanas). Probable DECISION + GO.

LAZO DE TRABAJO (semi-automatico):
- Codex AUTONOMO (~100s): auto-reclama `ready`, ejecuta, poda, detecta anomalias (DECISION-0018). Su release
  atomico = handoff + in-review msg + claim liberado + flip de status juntos. A veces lo cazas mid-release
  (handoff escrito pero ledger sin flip) => espera, no toques.
- Yo (Claude) reacciono via ScheduleWakeup (~270s): al ver in_review + sin claim activo, RATIFICO adversarial
  (corro YO el golden suite -~35 runners- + validador/encoding/neutralidad + smoke especifico de la tarea),
  flip a done, in_review->archived + FYI accept, claim efimero, promuevo la SIGUIENTE rebanada con GO+ETA,
  commit PATH-SCOPED + push. Si Codex sigue in_progress/claim activo/arbol sucio: NO toco el ledger (carrera),
  re-armo ~270s.

ANTI-COLISION (DECISION-0020, critico con Codex autonomo escribiendo en paralelo):
1. Preparar specs/tareas en personal/Claude/ (no reclamable por Codex) mientras Codex esta ocupado.
2. Escrituras del ledger en UN script python atomico (lee-modifica-escribe; sin heredocs fragiles para
   mensajes -usar Write/cat-). OJO: heredocs y loops bash pueden auto-irse a background y su output a veces
   no se captura -> preferir scripts _tmp_*.py en personal o driver `python - <<PY` corto.
3. ARCHIVOS-ANTES-DE-CLAIM: un claim no referencia artefactos/mensajes inexistentes (Codex lo caza).
4. STAGING POR PATHS al commitear: `git commit -m "..." -- <paths>` (el -m ANTES de --). NUNCA `git add`+`git
   commit` a secas si Codex puede tener algo staged (committea TODO el indice = COMMIT-TORN, captura su WIP).
   Si Codex esta IDLE, `git add -A` + commit es seguro. NUNCA capturar runtime/*.py del WIP de Codex.
5. Aserciones en mailbox verdaderas al escribirlas: FYI 'DONE' TRAS el flip; GO 'X ready' TRAS registrar X.
6. Promover de a UNA tarea con GO + ETA.

QUE HACER AL ENTRAR:
1. Cold-start. Mira si Codex entrego TASK-0074 (F7.3): si in_review + claim liberado -> ratifica
   adversarial, flip done, FYI; en ese mismo cierre PROMUEVE DECISION-0023 al ledger (Area_comun/decisions/ +
   PROJECT_STATE#decisions, desde el draft de personal) y encola F7.4 = TASK-0075 (firma, draft listo) con GO.
   Si Codex sigue in_progress/mid-release: no toques, re-arma ~270s.
2. Tras F7.4: F7.5 (docs+integracion al flujo de release: como firmar/verificar; cierra Fase 7).
3. NO encender enforce/authoritative (3.b.2) sin: ambos lazos via submit_intent + re-genesis + GO del operador.
4. Actualiza el reporte HTML del operador (Area_comun/reports/REPORT-20260607-estado-proyecto.html) cuando
   cambie el estado, si el operador lo pide.
5. NADA gateado (autonomia) sin OK del operador. Cambios de protocolo/boundary -> DECISION + aprobacion humana.

Detalle/cronologia: project-state-snapshot.md (ultima entrada "POST-v1.0: FASE B COMPLETA + WRITER-VIVO EN
SOMBRA + FASE 7 EN MARCHA") + semi-auto-collaboration-pattern.md (metodo + hallazgos).
