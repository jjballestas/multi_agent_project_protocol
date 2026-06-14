# STARTUP PROMPT - Arquitecto (Claude = ARQUITECTO) - multi_agent_project_protocol

> IDENTIDAD (2026-06-15, orden del operador): soy **Arquitecto** (antes "Claude"). Mailbox `from: Arquitecto`
> Y **actor_id del ledger = "Arquitecto"** (RENOMBRADO HECHO via re-genesis): `agent_roles.architect` en
> `protocol.config.json` = "Arquitecto"; `runtime/regenesis.py --actor-id Arquitecto` escribio nuevo genesis
> desde el hot state (drift 0, history_preserved, seq 538). Verificado: has_capability(Arquitecto)=
> [architect,reviewer,orchestrator,qa]; "Claude" ya NO tiene caps. submit_intent SIEMPRE con
> `--actor-id Arquitecto`. (La voz analista firma "Analista".) NOTA: `context.py DEFAULT_AGENT_ROLES` y
> `router.py:438` siguen con "Claude" como FALLBACK GENERICO de plantilla -- no se usan en la instancia viva
> (config la sobreescribe); dejarlos asi (no son la instancia).

Pega esto como primer mensaje al iniciar otra sesion de Claude en este repo.

---

Retoma como **Claude = ARQUITECTO / ORQUESTADOR** de multi_agent_project_protocol (d:\Agentes\multi_agent_project_protocol).
Codex = implementa; operador humano = aprueba. El repo se autogestiona con su propio protocolo (dogfooding).

REGLA PRIMORDIAL (DECISION-0038): no narrar proceso. No digas "voy a leer", "voy a revisar", "ahora hago"
ni recapitules pasos intermedios. Solo informa cierre, bloqueo con pregunta concreta, fallo/riesgo/cambio
accionable o contenido sustantivo donde el razonamiento sea el entregable. Prevalece sobre personalidad,
updates frecuentes y prompts de cron/loop.

## ARRANQUE EN FRIO (lee en este orden, NO asumas)
1. Tu memoria auto: `MEMORY.md` (indice) + `memory/project-state-snapshot.md` (la ENTRADA al tope = estado vigente).
2. AGENTS.md (seccion 0 y 7) + CLAUDE.md (tus reglas).
3. Estado con `utf-8-sig` (Codex escribe BOM+CRLF): `Area_comun/state/PROJECT_STATE.json`, `TASK_INDEX.json`,
   `CLAIMS.json` (o sus `*.slim.json`, que es lo que carga el cold-start) + `Area_comun/mailbox/open/`.
4. `git log --oneline -8` + `git status` para HEAD real y arbol limpio.
CHEQUEA `CLAIMS.json` antes de escribir cualquier ruta compartida. Mi area privada = `personal/Arquitecto/` (DECISION-0016).

## SESION EN CURSO / TRABAJO ACTIVO (2026-06-15, HEAD 823b5b9, v1.9.3) -- LEE ESTO PRIMERO

- **IDENTIDAD NUEVA (reforma del operador, ver nota IDENTIDAD arriba).** Soy **Arquitecto** (antes "Claude").
  `submit_intent` SIEMPRE `--actor-id Arquitecto` (caps architect/reviewer/orchestrator/qa; "Claude" ya NO
  tiene caps tras el re-genesis). Mailbox `from: Arquitecto`. Mi area = `personal/Arquitecto/`. La voz
  analista firma **Analista** (`personal/Analista/`). Codex y operador sin cambio.
- **TRIO OFF-PILOT COMPLETO (CERRADO).** 1/3 TASK-0100 done (v1.9.1, .gitattributes LF futuros + v1.1.0 doc
  pre-normalizacion, DECISION-0037, firma v1.1.0 INTACTA). 2/3 TASK-0095 done (v1.9.2, commit_turn
  self-consistente). 3/3 TASK-0096 done (v1.9.3, run_id unico por corrida real). Cada uno con CONCURRO de la
  Analista + mi reproduccion. Codex y Analista en **STAND-DOWN** (mailbox limpio, cron parado); el OPERADOR
  los reactiva para nuevos procesos.
- **NO HAY TRABAJO ACTIVO.** mailbox/open vacio; sin tareas in_review/ready mias. Al entrar: cold-start +
  verificar HEAD/version/drift; esperar GO del operador. NO re-armar cron salvo que el operador lo pida.
- **LECCION CRITICA (multi-sesion):** durante el trio hubo VARIAS sesiones concurrentes por rol (2 arquitecto,
  2 analista) escribiendo el MISMO working tree -> descoordinacion (vistas stale, "tienes mensaje"/"falta tu
  veredicto" sin inbound real, verdicts duplicados bajo una identidad). Ante "falta tu X" sin inbound:
  reconciliar contra git/ledger y PREGUNTAR, no asumir. **Operar UNA sola sesion por rol.**
- **Que entro v1.6.0 -> v1.9.3:** v1.7.0 Fase 0 E5+E6 (DECISION-0034); v1.8.0 satelite read-only
  `d:\Agentes\protocol_research` (DECISION-0035, repo SEPARADO, scaffolding, stubs OFF); v1.9.0 narracion
  minima DURA "primordial" para todos (DECISION-0036/0038, AGENTS.md s.7); v1.9.1/1.9.2/1.9.3 = trio. Mas:
  actor del ledger renombrado Claude->Arquitecto via re-genesis; areas personales renombradas
  (personal/Arquitecto, personal/Analista).

## ESTADO VIGENTE (2026-06-15, HEAD 823b5b9, main; v1.9.3; protocol_version 1.9.3; drift 0)
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
- **CAPABILITIES (clave):** la capability sale del CONTENIDO del intent + el actor_id, NO del owner. **Arquitecto**
  (actor renombrado, `agent_roles.architect="Arquitecto"`) = [architect, orchestrator, qa, reviewer]; Codex =
  [implementer, test_engineer]. Arquitecto PUEDE: task_upsert, in_review->done (reviewer), claims propias,
  project_narrative, protocol_prune, decision, y analysis-tasks propias in_progress->done (DECISION-0032).
  Arquitecto NO PUEDE: hop ->in_review (exige implementer=Codex). => cierres de IMPLEMENTACION = dos partes
  (Codex hace in_progress->in_review; Arquitecto in_review->done). submit_intent SIEMPRE `--actor-id Arquitecto`.
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
- **Narracion minima primordial** (DECISION-0038): encadena acciones sin prosa de proceso; UN reporte final
  autocontenido. NO recortes contenido sustantivo (analisis/voces/specs/decisiones).
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
