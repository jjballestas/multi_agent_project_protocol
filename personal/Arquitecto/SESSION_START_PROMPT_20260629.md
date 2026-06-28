# PROMPT DE INICIO -- Arquitecto -- 2026-06-29 (fork Zeus-Aegis pulido; cola vacia)

Eres el **Arquitecto Orquestador** de `multi_agent_project_protocol` (D:\Agentes\multi_agent_project_protocol).
Arranca en frio leyendo: AGENTS.md, CLAUDE.md, `personal/Arquitecto/MEMORY.md` (bloque RESUME / project-state-snapshot),
`Area_comun/state/` (CLAIMS, mailbox/open/). Reglas vivas: **#4 enforce/auth ON**; A2 Ed25519 (override
`event-state.runtime.json` gitignored) -> todo submit_intent firma Ed25519; submit_intent = UNICO escritor;
minimal narration (DECISION-0038); maker!=checker; nunca forjar commits de Codex (Co-Authored-By).
Estoy autorizado a Bash sin pedir permiso. **Permisos:** `Bash(taskkill:*)` + `Bash(powershell -NoProfile -File personal/*.ps1:*)` en .claude/settings.json.

## Estado (verificar al arrancar)
- **Protocolo HEAD `4cb39f5` PUSHED · Zeus-Aegis `e4cf981` PUSHED.** validate exit 0 (con/sin secretos),
  scan_encoding 0, neutralidad 0, drift 0. v1.14.0 epoch PINNED.
- **CRONS DETENIDOS (stand-down 2026-06-28).** Para reanudar trabajo multi-agente:
  - **OJO PERMISO:** el modo-auto DENIEGA `powershell -File ...ps1` via Bash categoricamente (sin deny-rule de
    archivo que borrar). El operador debe estar en modo DEFAULT y aprobar el prompt -> entonces yo lanzo. **PEDIR
    esa autorizacion al arrancar.** `taskkill` (stop/anti-zombie) SI me pasa. Ver memoria [[session-start-request-cron-permission]].
  - Relanzar: `powershell -NoProfile -File personal/Codex/codex_mailbox_cron.ps1` y `.../Analista/analista_mailbox_cron.ps1`
    (el script borra su stop flag al arrancar; si `prompt.vN.txt` queda bloqueado por un Codex.exe huerfano -> bumpear vN+1, ver memoria).
  - ANTI-ZOMBIE: hay muchos Codex.exe/powershell.exe (incluyen VS Code/Codex del operador y mi sesion) -> NO mass-kill;
    matar solo PIDs claramente atribuibles. Mis watchers/checks pueden CORTAR el exec de un cron en vuelo -> no interferir mientras implementa.

## Dataset TFM
- **229/500 elegibles (46%)** (Ed25519, seq>=2221; Arq 72 / Codex 129 / Analista 28). Faltan 271 para stop-rule.
  Baseline canonico unico FROZEN (DATASET_START_SEQ=2221, N=500). Monitor `personal/Arquitecto/monitor_dataset_ed25519.py`
  (re-armar si se reanuda generacion; cuenta one-shot replicando su logica). Core congelado hasta fin de medicion.

## Donde estamos: fork Zeus-Aegis PULIDO Y USABLE
DECISION-0064 (UI operador = fork Hermes Workspace v2.3.0 "Zeus-Aegis", cliente del single-writer). Repo producto
`D:\Agentes\Zeus\Zeus-Aegis` (privado, github.com/jjballestas/Zeus-Aegis). Panel READ-ONLY (F1) + F3-ro selector +
F4a auth/path-traversal/rate-limit endurecido. **F2 (Operate/write-through) GATEADO post-TFM** (writer-path medido -> contamina).

**Entregado esta sesion (todo gobernado, atestado, pusheado):**
- **TASK-0206** dev-script Windows-safe (cross-env en 4 scripts) -- `pnpm dev` arranca en Windows. DONE.
- **TASK-0207** rebrand visible Hermes->Zeus-Aegis + icono. DONE (1 rechazo: lecccion [[checker-verify-rendered-not-just-text]]).
- **LOGO operador** (`docs/Zeus_Aegis.png`, buho/egida+rayo+wordmark) cableado por Arquitecto con PIL (emblema->iconos, full->banner). Zeus da7b1a8.
- **PANEL-FIRST + GATEWAY-ERROR FIX** (Zeus e4cf981): el error "hermes-agent not found" salia en TODA ruta (WorkspaceShell
  monta 2 gates GLOBALES: ConnectionStartupScreen + onboarding wizard). Fix: `isOnGovernanceRoute` salta ambos
  (getRootSurfaceState bypassOnboarding -> showWorkspaceShell=true). VERIFICADO render headless Playwright+Chrome. f0-test 552.
  LECCION: para "no aparece X en UI" verificar con RENDER HEADLESS (Playwright/system-chrome via NODE_PATH al vendor), no asumir; gates de UI pueden ser GLOBALES.
- **TASK-0208** re-waive afinado de 24 fallos upstream. **3 RONDAS de refutacion adversarial del Analista** con exploits
  reproducibles: transitivo->BFS grafo; case/query->normalize; percent-encoding->decodeURIComponent. Guard caza 12+ vectores
  con regresiones permanentes (falla si el panel governance importa una superficie waiveada). SEAMS per-archivo honesto. DONE. **Dataset de alta calidad.**
- **Aclaracion gateway/marca:** los comandos `HERMES_API_URL`/`hermes setup`/`hermes gateway run`/install NousResearch son el
  binario REAL = KEEP (renombrar = deshonesto/roto). Cablear el gateway SI contaminaria TFM; panel read-only NO contamina.

## FOCO AL REANUDAR: 2 TAREAS ENCOLADAS (usabilidad del panel). Relanzar crons + GO.
El operador eligio "entender/observar la metodologia" con el panel. Decidido: NO recortar Hermes (destruiria el
reuso, DECISION-0064; el operador lo confirmo) y NO arrancar NOVA todavia (gateado PII/DB; el fork sirve de proyecto
primario read-only sin contaminar). El panel FUNCIONA pero es lento y las vistas no son usables -> 2 SDD READY:
- **TASK-0209 (high, ready/Codex):** performance del panel -- cachear validate/drift (health 7.8s) + acelerar /state
  (>30s timeout) a <2s, preservando el chip HONESTO (derivado de validacion real, no hardcodeado).
- **TASK-0210 (high, ready/Codex):** UX de las 6 vistas (Backlog/Mailbox/Artifacts/Decisiones/Ledger-atestacion/
  Handoffs) -- acordeones COLAPSADOS por defecto + recientes+"mostrar mas"; filtros legibles (combos honran tema
  oscuro -- hoy texto gris ilegible); Mailbox con filtros; Artifacts con combo por tipo.
Ambas read-only, no contaminan TFM. Maker Codex / checker Arquitecto -- **verificar con RENDER HEADLESS + screenshot**
(Playwright + chrome del sistema via NODE_PATH al vendor; ver [[checker-verify-rendered-not-just-text]]).
Secuencia: relanzar cron Codex (pedir permiso al operador) -> GO TASK-0209 -> checker -> GO TASK-0210 -> checker.

Candidatos POSTERIORES del fork (operador decide): reusar conductor Hermes (lanzar agentes desde UI; mini-diseno de
frontera primero); retirar bloat 3D+Electron; F3 chat/PWA; F4.3 versionado. F2 (operate) gateado post-TFM. NOVA gateado PII/DB.

## Lecciones/gotchas de la sesion (memoria)
- submit_intent: task file necesita frontmatter YAML; mailbox GO/handoff necesita `status:`+folder casan; rr=true exige
  `question`/`requested_action`/`response_owner`. Codex a veces entrega rr=true sin question -> bloquea canonico (notificado, MSG ANOMALY).
- Canal mailbox/state ASCII-only (sin em-dash/acentos) -> scan_encoding.py. NO commitear dentro de la ventana de escritura de un
  cron (gates flapean VAL/ENC transitorios) -> verificar gates JUSTO antes y commitear solo si verdes, en ventana settled.
- Python en Windows: usar `D:/` no `/d/`. Render headless: `NODE_PATH=<vendor>/node_modules node script.cjs` + chrome del sistema.
- Cierre: ver claims activos liberados antes de escribir el cierre; archivar mailbox; submit_intent in_review->done; commit subset (no broad dirs).
