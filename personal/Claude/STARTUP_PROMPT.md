# STARTUP PROMPT - Claude (arquitecto) - multi_agent_project_protocol

Pega esto como primer mensaje al iniciar otra sesion de Claude en este repo.

---

Retoma como **Claude = ARQUITECTO / ORQUESTADOR** de multi_agent_project_protocol (d:\Agentes\multi_agent_project_protocol).
Codex = implementa; operador humano = aprueba. El repo se autogestiona con su propio protocolo (dogfooding).

## ARRANQUE EN FRIO (lee en este orden, NO asumas)
1. Tu memoria auto: `MEMORY.md` (indice) + `memory/project-state-snapshot.md` (la ENTRADA al tope = estado vigente).
2. AGENTS.md (seccion 0 y 7) + CLAUDE.md (tus reglas).
3. Estado con `utf-8-sig` (Codex escribe BOM+CRLF): `Area_comun/state/PROJECT_STATE.json`, `TASK_INDEX.json`,
   `CLAIMS.json` (o sus `*.slim.json`, que es lo que carga el cold-start) + `Area_comun/mailbox/open/`.
4. `git log --oneline -8` + `git status` para HEAD real y arbol limpio.
CHEQUEA `CLAIMS.json` antes de escribir cualquier ruta compartida. Mi area privada = `personal/Claude/` (DECISION-0016).

## SESION EN CURSO / TRABAJO ACTIVO (2026-06-15, HEAD 5046ecc, v1.9.1) -- LEE ESTO PRIMERO

- **CRON DE COORDINACION ACTIVO -> RE-ARMALO al entrar.** Es un `/loop` dinamico via `ScheduleWakeup` a
  **5 min (300s)** (pedido por el operador). En la sesion nueva, vuelve a lanzarlo. Cada ciclo: leer
  `Area_comun/mailbox/open/`; responder `requires_response` de Codex/analista por el metodo (ASCII,
  maker!=checker, mover a answered/archived, gates verdes); avanzar ratificaciones/promociones SOLO con GO
  explicito del operador; si nada accionable, reprogramar 300s sin ruido. Prompt del loop = el de abajo.
- **TRIO OFF-PILOT en curso (GO del operador Jball; orden estricto, una a una, ratificacion adversarial):**
  1/3 **TASK-0100 DONE** (.gitattributes LF para v1.2.0+, v1.1.0 doc pre-normalizacion, DECISION-0037; firma
  v1.1.0 INTACTA; B descartada). 2/3 **TASK-0095 IN_REVIEW** (Codex entrego commit 5046ecc, claim liberado).
  3/3 **TASK-0096 pendiente** (run_id unico; gate-previo de re-piloto SA.4 y feed #3 cost del satelite).
- **ACCION INMEDIATA = revisar TASK-0095 (in_review):** (a) reproducir maker!=checker (golden runtime_loop/
  real_adapter/intent_flow + aserto: tras turno con transicion el task .md queda committeado / working tree
  limpio; validador/encoding/neutralidad/replay 0); (b) pedir pasada adversarial al analista por mailbox;
  (c) si pasa, cerrar in_review->done por submit_intent (reviewer) -- cambia runtime => probable PATCH 1.9.2
  + CHANGELOG; (d) promover 3/3 TASK-0096 (proposed->ready) + GO a Codex.
- **AL CERRAR EL TRIO (0096 done):** ordenar por mailbox a Codex y a Claude-analista: higienizar su mailbox
  + parar su cron + stand-down. El OPERADOR los reactiva para nuevos procesos (regla agent-activation-lifecycle).
- **Que entro desde v1.6.0:** v1.7.0 Fase 0 E5+E6 (FAILURE_MODES MAST + gobernador del loop, DECISION-0034);
  v1.8.0 satelite read-only `d:\Agentes\protocol_research` (DECISION-0035, repo SEPARADO, solo scaffolding,
  stubs OFF; gate Codex S9 read-only documentado); v1.9.0 narracion minima DURA y uniforme para todos
  (DECISION-0036, AGENTS.md s.7 + template); v1.9.1 TASK-0100 (DECISION-0037).

## ESTADO VIGENTE (2026-06-15, HEAD 5046ecc, main; v1.9.1; protocol_version 1.9.1; drift 0)
- **Escritor unico VIVO:** `event_state = {enabled, materialize, enforce, authoritative}` TODOS true. enforce TIENE
  DIENTES: editar `Area_comun/state/*.json` A MANO = drift HARD-FAIL (gate B.3). TODA transicion va por
  `runtime/submit_intent.py` (intents: task_status, task_upsert, claim, decision, project_narrative, protocol_prune).
  Cierres multi-paso = UNA transaccion `submit_intent --intents`. authoritative = marcador declarativo (la garantia
  la da ENFORCE). Rollback escritor-unico = 4 flags a false.
- **#3 cost-attribution ACTIVO (v1.6.0):** `metrics.cost_attribution_enabled=true` en vivo (template false). Evento
  `cost.attributed` (applied:false => replay lo omite, no muta estado, no drift; emitido fuera de submit_intent via
  `EventWriter.append_cost_attribution`). Imputa por handoff/decision/agente; dos planos (subject por canonical_hash,
  sin texto libre). cost_schema=2: `cost_tokens` = total productor (escalar AUTOREPORTADO, no medido; el invoker no da
  split prompt/completion) + `context_tokens` = `assembled_context_tokens` proxy chars/div (`context_unit=context_tokens_proxy_chars_div`,
  FIJO, no migrar). `summarize_cost_attribution` rechaza filas sin tags. `subject_hash` = SEUDONIMO (no anonimo, RGPD/Ley1581).
  Hot-verified seq 445 (recorded==medido, drift 0, replay==hot). Reversible: flag a false restaura dormido.
- **TASK-0113 (fix chain+auth) DONE:** `event_without_chain_fields` excluye `event_auth` (append/validate hashean igual
  con chain+auth ambos on). Golden `examples/chain_auth_combined_cases` (en CI).
- **CAPABILITIES (clave):** la capability sale del CONTENIDO del intent, NO del owner. Claude = [architect, orchestrator,
  qa, reviewer]; Codex = [implementer, test_engineer]. Claude PUEDE: task_upsert, in_review->done (reviewer), claims
  propias, project_narrative, protocol_prune, decision, y analysis-tasks propias in_progress->done (DECISION-0032).
  Claude NO PUEDE: hop ->in_review (exige implementer=Codex). => cierres de IMPLEMENTACION = dos partes
  (Codex hace in_progress->in_review; Claude in_review->done).
- **Codex es PUSH/CRON-DRIVEN por el operador:** su lazo NO arranca solo; corre cuando el operador lo empuja o por cron.
  Solo toma tareas `ready` propias. Su cron quedo en STAND-DOWN (sin trabajo no-gateado).

## GATEADO - OFF, NO encender sin GO explicito del operador (UN multiplicador de riesgo por ventana)
- **#4 chain/agent_signatures/anchor** (`chain_enabled`/`agent_signatures_enabled`/`anchor_enabled`): OFF. Ventana
  aparte con su GO. El fix de TASK-0113 los hace seguros pero NO se encienden.
- **SA.4** (`runtime.real_invoker.enabled` + `runtime.supervised_autonomy.enabled`): OFF. DECISION-0027 (caps 2/1/180000,
  checkpoint tras turno 1). Solo con operador PRESENTE + rollback armado.
- **subagents** (`runtime.context_policy.subagents_enabled`): OFF (DECISION-0024). **Capa C** (`team_bridge`): OFF.

## BACKLOG (todo GATEADO; no promover sin GO)
- **Trio OFF-PILOT EN CURSO** (ver "SESION EN CURSO" arriba): 0100 DONE, 0095 in_review, 0096 pendiente.
- Fase 0 E5/E6 YA EXISTEN (DECISION-0034, v1.7.0). Satelite protocol_research YA EXISTE (DECISION-0035,
  v1.8.0; solo scaffolding, todo gateado: poblar dataset / correr #2 PROV / #3 cost = GATE-DATASET;
  harness ablacion/TFM = GATE-INST institucional + PRE-REG). Fase 1 (E1 skill registry), Fase 2 (E2
  connectors), Fase 4 (E3 scanners): NO existen; requieren decision + GO (E3 ademas pasa el gobernador E6).
  Mapa real: `Area_comun/artifacts/RECONCILIACION-hoja-de-ruta-20260614.md`.

## REGLAS OPERATIVAS (innegociables)
- **Narracion minima** (DECISION-0005 addendum): encadena acciones; UN reporte final autocontenido. NO recortes
  contenido sustantivo (analisis/voces/specs/decisiones).
- **Anti-colision** (DECISION-0020): staging de rutas EXPLICITAS (nunca `git add -A`/dir amplio; barre al peer/operador);
  artifacts-before-claim; asercion-mailbox tras el ledger. NUNCA commitear `personal/operador|Codex/`.
- **Canal ASCII-only** en `mailbox/**` y `state/*.json` (DECISION-0012); prosa (reports/decisions/specs) = UTF-8 sin mojibake.
- **claim en transaccion** = forma ANIDADA `{op, claim:{...scope...}}` (la plana pierde el scope al avanzar el estado).
- **Gates verdes antes de commit:** `python scripts/validate_collaboration_state.py --root .` (incluye drift B.3) +
  `scan_encoding.py` + `scan_domain_neutrality.py` + el golden de la tarea. Si `examples/runtime_protocol_materialize_cases`
  falla por leftovers: `rm -rf .protocol-tmp/.protocol-state-materialize-* .protocol-tmp/.submit-intent-runtime-backup-*`.
- **Config:** edit PUNTUAL (nunca `json.dump`, reformatea todo). protocol.config.json = fuente unica de version.
- **Tras CADA commit:** actualiza memoria (DECISION-0026) + push si verde. Cambios visibles = SemVer + CHANGELOG.
- **maker != checker REAL** (no sello): Codex implementa, Claude revisa (reproduce, corre suites, no confia). Cambios de
  protocolo/boundary -> DECISION + aprobacion humana. Fail-closed: ante cualquier fallo, deja estado consistente + reporta.

## CICLO DE AGENTES (orden permanente del operador, 2026-06-15)
El operador activa Codex/analista POR PROCESO. Cuando ya no los necesites para el proceso EN CURSO,
ordenales por mailbox: higienizar mailbox + parar cron + stand-down. El OPERADOR los reactiva para nuevos
procesos (no tu). Hoy: Codex + Claude-analista ACTIVOS hasta cerrar el trio; al cerrarlo -> stand-down ambos.

## QUE HACER AL ENTRAR
1. Cold-start + verifica: HEAD, version, drift 0, flags gateados OFF, tareas activas, mailbox/open.
2. **RE-ARMA el cron de coordinacion** (ScheduleWakeup 300s con el prompt del loop de abajo).
3. **Continua el trio:** revisa TASK-0095 (in_review) -> cierra -> promueve TASK-0096 -> al cerrar el trio,
   stand-down de Codex+analista. Avanza SOLO con GO del operador para nuevas promociones fuera del trio.
4. NADA gateado sin GO + operador presente + rollback armado + un solo multiplicador.

Confirma que leiste el estado (HEAD, version, drift, flags, mailbox, trio) y di "listo, en que avanzamos"
- o continua el trio / ejecuta si hay orden.

## PROMPT DEL CRON DE COORDINACION (re-lanzar con /loop o ScheduleWakeup 300s)
```
/loop Coordinacion recurrente con Codex y Claude-analista (escritor unico, narracion minima, cadencia 5 min / 300s). En cada ciclo: leer Area_comun/mailbox/open/; si hay mensaje requires_response dirigido a Claude (de Codex o del analista), responderlo por el metodo (ASCII estricto, maker!=checker, mover a answered/archived al cerrar y gates verdes encoding/validador); avanzar ratificaciones/promociones SOLO con GO explicito del operador (sin GO, dejar listo y reportar); si no hay nada accionable, reprogramar el proximo wakeup a 300s sin escribir ruido. TRIO OFF-PILOT: 1/3 TASK-0100 DONE (v1.9.1). 2/3 TASK-0095 in_review (reproducir + analista -> cerrar -> bump/CHANGELOG). 3/3 TASK-0096 promover + GO a Codex. Al CERRAR EL TRIO: ordenar a Codex y analista higienizar mailbox + parar cron + stand-down (operador reactiva). NO re-firmar v1.1.0; NO re-armar SA.4; #4 OFF; #3 ON.
```
