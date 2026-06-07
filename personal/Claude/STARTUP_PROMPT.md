# STARTUP PROMPT - Claude (arquitecto) - multi_agent_project_protocol

Pega esto como primer mensaje al iniciar otra sesion de Claude en este repo.

---

Retoma como arquitecto (Claude) de multi_agent_project_protocol.

COLD-START: lee AGENTS.md seccion 0 + Area_comun/state/*.json (con utf-8-sig: Codex escribe BOM+CRLF) +
Area_comun/mailbox/open/ + mi memoria (MEMORY.md + project-state-snapshot.md, ULTIMA entrada = estado
actual). CHEQEA CLAIMS.json antes de escribir cualquier ruta compartida. ASCII-only en mailbox/state
(DECISION-0012). Mi area personal es personal/Claude/ (DECISION-0016). Permisos del lazo ya estan en
.claude/settings.json (los comandos rutinarios read-only/loop no piden aprobacion).

CONTEXTO (cierre 2026-06-07, HEAD 9644736 en main, pusheado): se construye la metodologia como PRODUCTO
DISTRIBUIBLE = RELEASE v1.0 (alcance del operador, incluye el wrapper LLM real).

ESTADO v1.0:
- DONE: v0.10.0 (nucleo Fases 1-4 + Capa A) | Fase 5 completa (5.1 anti-inyeccion + 5.2 tool-policy + 5.3
  firma del envelope) | D0 motor (Fase 6.1 observabilidad trace_id/spans/summarize_nagent + 6.2 A10 budget/
  deadline) | D2.1 distribucion via TIERS de adopcion (DECISION-0019: new_instance --tier coordination|
  runtime, default coordination, motor off-by-default) | D2.2 upgrade_instance tier-aware + runtime_version |
  WRAPPER LLM REAL (TASK-0062, DECISION-0021: adapter CLI vendor-neutral presets claude/codex sobre
  SubprocessInvoker, off-by-default real_invoker.enabled=false+registro, sin secretos, NO autonomia) |
  D2.3 docs (TASK-0063: README_INSTANCIACION tiers/upgrade/operar-agentes-reales + Area_comun/protocol/
  N_AGENT_RUNTIME.md criterio 16).
- EN CURSO: D2.4 (TASK-0064 ready/in_progress: Area_comun/protocol/PACKAGE_VERSIONING.md = 4 ejes de version
  + migracion; ultima de D2; SPEC-0050).
- RESTANTE v1.0 (en orden): D2.4 -> DECISION-0020 (formalizar la regla anti-colision; el operador autorizo
  crearla 'si funciona') + fix prune (TASK-0065/SPEC-0051: prune debe condensar next_actions) -> RELEASE
  v1.0 (REQUIERE APROBACION HUMANA: bump protocol_version 1.0.0 + CHANGELOG + reporte humano + tag).
- POST-v1.0 GATEADO (no arrancar sin OK): Fase B (event log writer-vivo del ESTADO de protocolo, SPEC-0039),
  Fase 7 (release eng SBOM/provenance), autonomia supervisada.

LAZO DE TRABAJO (semi-automatico):
- Codex es AUTONOMO (reloj ~100s): auto-reclama `ready`, hace su prune, detecta anomalias (DECISION-0018).
- Yo (Claude) reacciono autonomo via ScheduleWakeup (~270s): al detectar entrega de Codex (in_review + sin
  claim activo), RATIFICO adversarial (corro YO el golden de la tarea + suite runtime + validador/encoding/
  neutralidad py), flip a done, in_review->answered + FYI a Codex, claim efimero, prune si due, commit + push,
  y encolo la siguiente rebanada. Si Codex sigue in_progress/claim activo/working tree sucio: NO toco el
  ledger (carrera), re-armo ~270s y espero.

METODO ANTI-COLISION (validado en 5.2/5.3/6.x/D2.x; se formaliza en DECISION-0020):
1. Preparar specs/tareas en personal/ (no reclamable por Codex) cuando Codex esta ocupado.
2. Escrituras del ledger (cierre/encolado) en UN script Python ATOMICO (minimiza la ventana de intercalado).
   Evita heredocs con triple-comillas (rompen bash); escribe los mensajes via Write tool.
3. ARCHIVOS-ANTES-DE-CLAIM: un claim no referencia archivos inexistentes (HALLAZGO #1).
4. STAGING EXPLICITO al commitear (paths, no dirs amplios) para no capturar trabajo concurrente del peer
   (commit torn) (HALLAZGO #2). Si los edits ya se intercalaron, commitea un SNAPSHOT consistente (gates verdes).
5. Toda ASERCION en mailbox debe ser verdadera en el ledger al escribirla: el FYI 'DONE' va TRAS el flip; el
   GO 'X ready' va TRAS registrar X en el ledger (HALLAZGO #3). Crea esos mensajes con Write DESPUES del
   script atomico.
6. GO + ETA a Codex; promover de a UNA tarea.

REGLAS: cambios de protocolo/boundary -> DECISION + aprobacion humana; releases -> aprobacion humana;
commit+push cuando verde; neutralidad de dominio innegociable; `.template.*` son los masters. Encolar a
Codex = tarea SDD + mensaje GO; Codex entrega con RELEASE ATOMICO (handoff+in-review+claim released+flip
juntos, DECISION-0018); si deja anomalia, notificar por mailbox y no tocar rutas bajo su claim.

QUE HACER AL ENTRAR:
1. Cold-start. Mira si Codex entrego TASK-0064 (D2.4): si in_review -> ratifica (documentacion: gates +
   coherencia + sin secretos) y cierra; con D2.4 done, D2 queda COMPLETO.
2. Tras D2.4: formaliza DECISION-0020 (regla anti-colision) + AGENTS.md sec.7 + .template + TASK_PROTOCOL
   (aditivo); encola fix prune (TASK-0065). Luego REPORTA al operador que v1.0 esta listo y PIDE APROBACION
   para el release (no hacerlo sin OK).
3. NO arranques release v1.0 ni nada gateado sin OK del operador.

Detalle/cronologia: project-state-snapshot.md (ultima entrada "v1.0 CASI LISTO") + semi-auto-collaboration-
pattern.md (metodo + hallazgos). Plan: C:\Users\johnb\.claude\plans\shimmering-strolling-tome.md.
