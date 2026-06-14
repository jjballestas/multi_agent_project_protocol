# MEMORY - Claude (arquitecto) - multi_agent_project_protocol

> Runbook in-repo de Claude (DECISION-0026: actualizar tras cada commit). La cronologia completa vive en la
> memoria auto (`memory/project-state-snapshot.md`). Aqui = estado vigente + reglas + lecciones, conciso.
> Ultima actualizacion: 2026-06-14, HEAD 60465f1, v1.6.0.

## Estado vigente (2026-06-14)
- **v1.6.0 PUBLICADO.** HEAD `60465f1` en main. protocol_version 1.6.0, runtime_version 0.12.0. drift 0.
- **Escritor unico VIVO:** event_state {enabled, materialize, enforce, authoritative} = true. enforce con dientes
  (drift B.3 hard-fail si se edita state a mano). Toda transicion por `runtime/submit_intent.py`.
- **#3 cost-attribution ACTIVO:** `metrics.cost_attribution_enabled=true` vivo (template false). Evento `cost.attributed`
  applied:false (no muta estado, no drift; via append_cost_attribution fuera de submit_intent). cost_schema=2
  (cost_tokens=total productor autoreportado + context_tokens=assembled proxy chars/div). Hot-verified seq 445. Reversible.
- **TASK-0111 (cost-attribution) + TASK-0113 (fix chain+auth) DONE.** chain_auth_combined golden en CI.
- **Gateado OFF:** #4 (chain/agent_signatures/anchor), SA.4 (real_invoker+supervised_autonomy), subagents, Capa C (team_bridge).
- **Codex:** push/cron-driven por el operador; en STAND-DOWN (sin trabajo no-gateado).

## Capabilities (clave operativa)
- Claude = [architect, orchestrator, qa, reviewer] -- NO implementer. Codex = [implementer, test_engineer].
- Claude PUEDE: task_upsert, in_review->done (reviewer), claims propias, project_narrative, protocol_prune, decision,
  analysis-tasks propias in_progress->done (DECISION-0032). Claude NO PUEDE hop ->in_review (exige implementer=Codex).
- Cierre de IMPLEMENTACION = dos partes: Codex in_progress->in_review (su atestacion), Claude in_review->done.

## Backlog (GATEADO; no promover sin GO)
- TASK-0095/0096/0100 proposed (TASK-0100 .gitattributes eol=lf espera GO). Fase 0 (E5/E6), Fase 1 (E1 skills),
  Fase 2 (E2 connectors): no existen, requieren decision+GO. SA.4 piloto (DECISION-0027): sin disparar.
- Mapa real reconciliado: `Area_comun/artifacts/RECONCILIACION-hoja-de-ruta-20260614.md` (#4 hecho off-by-default; E9 worktrees=NO).

## Lecciones no-obvias (persisten)
- **claim en submit_intent tx = forma ANIDADA** `{op, claim:{...scope...}}`; la plana pierde el scope al avanzar el estado
  in-memory (apply_claim_event reconstruye sin scope) => "write outside active claim scope".
- **Config: edit PUNTUAL** (nunca json.dump -> reformatea todo el archivo). protocol.config.json = fuente unica de version.
- **`.protocol-tmp/` leftovers** (gitignored) hacen fallar el golden de materialize: `rm -rf .protocol-tmp/.protocol-state-materialize-* .protocol-tmp/.submit-intent-runtime-backup-*`.
- **`utf-8-sig`** para leer state JSON (Codex escribe BOM+CRLF). Canal mailbox/state = ASCII-only (DECISION-0012).
- **Staging EXPLICITO por path** (DECISION-0020); nunca `git add -A` (barre personal/operador|Codex). index.lock huerfano: `rm -f .git/index.lock` si no hay proceso git.
- **maker != checker REAL:** reproducir el fix del peer (no confiar). En esta sesion Codex hallo un bug latente de #4
  (chain+auth) que yo no habia visto -> el doble gate (Codex + analista) atrapo lo que un solo revisor no.
- **Fail-closed:** ante fallo (golden rojo / drift != 0 / hot != real), deja estado consistente (flag false) + reporta. No fuerces.

## Reglas de riesgo
- UN multiplicador por ventana. Activaciones gateadas solo con operador PRESENTE + rollback armado, nunca en tick desatendido.
- enforce protege el LEDGER JSON, NO la prosa-contrato (AGENTS.md/decisions/specs) -> anti-colision MANUAL ahi (git diff + staging explicito).
- Narracion minima (DECISION-0005 addendum): encadena, UN reporte final; no recortes contenido sustantivo.

Detalle/cronologia completa: `memory/project-state-snapshot.md` (memoria auto) + semi-auto-collaboration-pattern + permission-auto-exec + operator-working-style + cutover-risk-staging + commit-then-memory.
