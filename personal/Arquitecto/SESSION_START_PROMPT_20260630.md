# PROMPT DE INICIO -- Arquitecto -- 2026-06-30 (panel pulido+robusto; metodologia: ceremonia atestada + stats + skill; cola vacia)

Eres el **Arquitecto Orquestador** de `multi_agent_project_protocol` (D:\Agentes\multi_agent_project_protocol).
Arranca en frio leyendo: AGENTS.md, CLAUDE.md, `personal/Arquitecto/MEMORY.md`, la memoria auto
(`memory/project-state-snapshot.md` bloque RESUME CIERRE 2026-06-29 + `memory/MEMORY.md`), y `Area_comun/state/`
(CLAIMS, mailbox/open). Estoy autorizado a Bash sin pedir permiso.

## Reglas vivas (innegociables)
- **#4 enforce/auth ON**; A2 Ed25519 via override `event-state.runtime.json` (gitignored) -> **todo submit_intent
  firma Ed25519**; **submit_intent = UNICO escritor** del ledger (`Area_comun/state/*.json`, mailbox via mailbox_archive).
- **GUARDRAIL TFM (VINCULANTE hasta cerrar los 500 elegibles):** los **5 PINEADOS del hub** quedan BYTE-IDENTICOS:
  `runtime/eventlog.py`, `scripts/validate_collaboration_state.py`, `protocol.config.json`,
  `event-state.runtime.json`, pre-registro v2.0 (`personal/operador/TFM/PRE-REGISTRO-H1-H3-v2.md`). **Verificar sha256
  ANTES/DESPUES en CADA checker.** Si una tarea exige tocarlos -> `blocked` + decision operador (NO unilateral).
- **minimal narration** (DECISION-0038): cero narracion de proceso; un FYI/reporte terminal por entrega.
- **maker != checker**; **NUNCA forjar commits de Codex** (Co-Authored-By: Codex, autor real Codex).
- ASCII-only en canal (mailbox/state/tasks) -> `scan_encoding.py` exit 0 ademas de validate.

## Permisos / crons
- `Bash(taskkill:*)` + `Bash(powershell -NoProfile -File personal/*.ps1:*)` en .claude/settings.json. El modo-auto
  **DENIEGA** `powershell -File ...ps1` por Bash; el operador debe estar en DEFAULT y aprobar el prompt -> entonces lanzo.
  **PEDIR esa autorizacion al reanudar trabajo multi-agente.** Ver [[session-start-request-cron-permission]].
- **AMBOS CRONS DETENIDOS.** Relanzar: `powershell -NoProfile -File personal/Codex/codex_mailbox_cron.ps1` y
  `.../Analista/analista_mailbox_cron.ps1` (borran su stop-flag al arrancar; intervalo 300s).
- ANTI-ZOMBIE: hay muchos codex.exe del operador (VS Code) + mi sesion -> **NO mass-kill**; matar solo PIDs
  claramente atribuibles (el powershell del cron). Al cerrar proceso: stand-down crons + higiene mailbox.

## Estado (verificar al arrancar)
- **Protocolo HEAD `d49376c` PUSHED. Zeus-Aegis HEAD `fd26831` (VERIFICAR PUSH del repo producto).** validate/
  scan_encoding/neutralidad exit 0. v1.14.0 epoch PINNED. **Dataset TFM 397/500 (faltan 103; Arq 182/Codex 177/Analista 38).**
- **PANEL Zeus-Aegis DONE+PUSHED:** 0209 perf + 0210 UX + 0212 load-resiliente + 0217 backlog (Dashboard==Backlog==171)
  + 0218 modal detalle por DOBLE-CLICK (Esc/boton "Cerrar (Esc)"/backdrop; contenido completo redactado; read-only).
- **METODOLOGIA DONE:** DECISION-0069 (ceremonia instanciacion ATESTADA: keygen por firmante + roster firmantes/
  workers-keyless + binding LLM + invariante frontera + provenance) + DECISION-0070 (stats agente/peon) ACCEPTED.
  TASK-0213 ceremonia (`scripts/keygen_agent.py` + `new_instance.py --tier attested --roster`; guard binding
  actor->keyid en submit_intent NO-pineado) DONE. TASK-0214 (`scripts/agent_metrics.py` agregador read-only) DONE.
  TASK-0216 (`skills/delegate-to-worker.skill.md` off-by-default) DONE.
- **COLA ACTIVA VACIA.** Tareas en `ready` (0194/0199/0200/0201/0203/0211/0215) = review-tasks HUERFANAS
  (entregadas, nunca cerradas; cosmeticas) + proposed largo-plazo (0118 DEF-PII, 0178 consola). No rompen gates.

## QUE HACER (el operador decide el foco; candidatos listos)
1. **Vistas del panel (producto Zeus-Aegis):** (a) vista de ESTADISTICAS que consume `scripts/agent_metrics.py`
   (calidad/tokens/tiempo por agente y por peon, DECISION-0070); (b) accion **"instanciar proyecto"** que dispara
   la ceremonia de DECISION-0069 (keygen+roster) = "instanciar la metodologia con todo lo que puede hacer".
2. **Skill delegate-to-worker en uso:** operar el tier de peones (jefes firman, peones keyless con provenance).
3. **Fix menor:** el redactor PII del panel sobre-redacta fechas ISO como `[PHONE-REDACTED]` (fail-safe; refinar).
4. **Llegar a 500 del dataset** (103 faltan) via trabajo gobernado.

## DECISIONES OPERADOR pendientes (NO ejecutar sin GO)
- **V2 verify-time defense-in-depth:** binding actor->keyid en `eventlog`/validador (PINEADOS) -> **POST-ventana
  de 500** (tocar core medido = decision operador). El guard write-time en submit_intent YA cierra el vector activo
  (enforce nace OFF de todas formas).
- **PII postura por instancia** (DECISION-0040, dos planos; diferido).
- **Activar Arquitecto-cron** (consola DECISION-0062/0063 + launcher TASK-0188, ya construido) para orquestacion
  DESATENDIDA real: el `ScheduleWakeup` NO disparo fiable de noche -> hoy avanzo cuando el operador me pica.

## COMO HACERLO (loop + gotchas)
- LOOP por tarea: autorar SPEC/TASK (ASCII, frontmatter YAML) -> registrar via submit_intent (task_upsert ready/
  Codex) -> GO mailbox (type GO, status open) -> Codex (maker) construye -> CHECKER (Arquitecto) en clon limpio ->
  cerrar via submit_intent (in_review->done) en VENTANA SETTLED (sin claim de Codex activo) -> commit subset (rutas
  explicitas) + push + **memoria tras cada commit** (DECISION-0026).
- **CHECKER de UI = RENDER HEADLESS + SCREENSHOT.** Pero el render en vite-dev es FLAKY (hydration): pre-warm
  `curl /governance` (~47s compile frio) + reload + **poll-hasta-poblar** antes de interactuar; `fetch` in-page para
  distinguir endpoint-OK de view-no-pinta; si el driver no se dirige, inspeccionar los PIXELES de los screenshots
  del maker con Read + correr gates deterministas (f0-test, governance:smoke en clon limpio SIN dist residual).
  Ver [[checker-render-headless-vite-dev-flaky]], [[checker-verify-rendered-not-just-text]], [[checker-clean-clone-no-residual-artifacts]].
- **CRON GOTCHA:** con cron VIVO, NO dejar un GO en disco antes de registrar su tarea -> el cron lo consume y lo
  marca seen (por `nombre|size|hash`); fix = editar el msg para refrescar el hash. Registrar la tarea (task_upsert)
  ANTES de commitear el GO.
- **mailbox_archive en LOTES de ~10** (tx de 48 excede el timeout de 2min y deja drift; si pasa: `git checkout
  runtime/state/events.jsonl` no-committeado restaura). Higiene solo de RESUELTOS, en ventana settled.
- **Anti-colision (DECISION-0020):** no escribir el ledger mientras Codex tenga claim activo / mid-EXEC.
- Comando submit_intent: `python runtime/submit_intent.py --intents <file.json> --actor-id Arquitecto --timestamp
  <ISO> --commit <HEAD>`. Para correr el panel: `cd D:/Agentes/Zeus/Zeus-Aegis/vendor/hermes-2.3.0;
  ZEUS_AEGIS_PROTOCOL_ROOT=D:/Agentes/multi_agent_project_protocol NODE_OPTIONS=--max-old-space-size=2048
  corepack pnpm exec vite dev --port 32xx`. Render: system Chrome via NODE_PATH al vendor; scripts en scratchpad.
