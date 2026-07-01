Retoma como Arquitecto / ORQUESTADOR de multi_agent_project_protocol (D:\Agentes\multi_agent_project_protocol).
Codex = implementa; Analista = checker adversarial; operador humano (John Ballestas) = aprueba. Dogfooding.
actor_id del ledger = "Arquitecto". REGLA PRIMORDIAL (DECISION-0038): narracion minima. HORA en cada informe.

ARRANQUE EN FRIO (lee en orden, no asumas):
1. memory/MEMORY.md (indice) + memory/project-state-snapshot.md + personal/Arquitecto/MEMORY.md (bloques mas nuevos primero: "REDESPLIEGUE + REMEDIACION JAMS 2026-07-02").
2. Dispara el skill arquitecto-ledger-ops ANTES de tocar el ledger. 4 skills del Arquitecto: arquitecto-ledger-ops, arquitecto-cron-lifecycle, mailbox-hygiene, arquitecto-monitor-coordina. Skill global: session-checkpoint (guardar estado). USALAS.
3. AGENTS.md (s.0,s.7) + CLAUDE.md.
4. Area_comun/state/{PROJECT_STATE,TASK_INDEX,CLAIMS}.json + Area_comun/mailbox/open/ (~4 mensajes vivos).
5. git fetch + git log --oneline -8 + git status (HEAD real; arbol COMPARTIDO; los peers commitean-a-veces-sin-pushear; `git merge --ff-only origin/main`).

ESTADO VIGENTE (re-confirma via git; HEAD de referencia cc1dac4, 2026-07-02 01:32 local):
- FONDO INTOCABLE: Dataset SELLADO N=500 (tag TFM-dataset-N500 -> e3646ae); H1-H3 CONFIRMADAS. NO generar eventos "para el dataset". NO tocar los 5 pineados / v1.14.0 / #4. NO activar F2/re-genesis sin GO operador.
- FOCO = REQ-ZEUS-001 (productizar Zeus-Aegis, D:\Agentes\Zeus\Zeus-Aegis). Adoptado: DECISION-0077 + D1-D5 (0072-0076). Plan vigente: PLAN-REQ-ZEUS-001-reconciliado.md. SUPERADOS: PLAN-cierre-dataset-lote-panel.md, REQZEUS-backlog-map.md.
- PIPELINE: **DONE: 0222 0223 0224 0225 0226 0227 (F1, DECISION-0079 inline-only) 0228 (WS5) 0235 (exec-lease).** **EN CURSO: 0237 (in_progress) = hang-proof del npm test en Zeus-Aegis (PRIORIDAD, la causa raiz de los jams).** **ready en cola de Codex: 0236 (remediacion 0235: 4 fixes al harness).** **0229 (WS3 branding) = BLOCKED** (su work ya esta en producto commit 980445c pero el npm test cuelga; re-habilitar tras 0237). **proposed: 0230[WS2] 0231[WS4] 0232[WS3.5] 0233[WS7 e2e, owner Analista] 0234[WS10].**
- MAILBOX: open/ higienizado (el bloque 0222-0235 se archivo, 60 msgs). Vivos: GO-0236, GO-0237, review A/B al Analista, y GO-0229 (diferido).

EN VUELO (trabajo con dueño, esperando):
- **0237** -> Codex construyendo. Al entregar -> REVIEW al Analista (con repro del cuelgue). GO -> ratifico + done-flip. Con 0237 verde, RE-HABILITO 0229 (nuevo GO o unblock).
- **0236** -> Codex lo toma tras 0237. Igual ciclo.
- **review A/B politica cron-zombie** -> Analista. GO/NO-GO sobre A (barrido quirurgico) + B (baja graceful); C ya cerrada por 0235. **Con GO del Analista -> REDACTA la DECISION correspondiente** (pendiente).
- **0233 [WS7]** proposed, NO promover hasta que WS1-WS6 esten done.

INFRA DE CRONS (CRITICO, leelo):
- **Crons REDESPLEGADOS 2026-07-02 con el harness endurecido de 0235.** STOP_JOB es el UNICO token de parada (`-cmatch "\bSTOP_JOB\b"`): **footgun OFF** -- ya puedes escribir kill/deadline/parada/stop en mensajes SIN auto-detener el cron (solo el token literal STOP_JOB detiene). Lanzar/relanzar crons: `powershell -NoProfile -File personal/<peer>/<peer>_mailbox_cron.ps1` run_in_background -- SOLO en modo NO-AUTO (en auto el clasificador deniega); si deniega, handoff al operador.
- **DOS MONITORES PERSISTENTES (arma AMBOS al coordinar, no solo el de entregas):** (1) entregas sobre HEAD LOCAL + MSG *-to-Arquitecto-* nuevos, self-filter Co-Authored-By Claude (los peers commitean sin pushear; un watcher de origin no los ve); (2) WATCHDOG de salud: lock retenido + run-log CONGELADO >8min = exec colgado (falla silenciosa que el de entregas no ve). Comandos exactos en arquitecto-monitor-coordina.
- **Reacciono al EVENTO del monitor de inmediato, sin esperar "revisa" del operador.** Al reaccionar: fetch + coordino + PUSHEO yo el commit local del peer.

GOTCHAS VIGENTES (detalle en arquitecto-cron-lifecycle):
- CAUSA RAIZ de los jams: el npm test de Zeus-Aegis SE CUELGA en clon limpio (arbol node/esbuild) y cada tarea WS lo corre -> TASK-0237 lo arregla en origen; TASK-0236 endurece el harness (prompt por-exec, tree-kill /T, guard instancia-unica, enforcement lease huerfana).
- Destrabe manual de un exec colgado: who_locks.py (Restart Manager) pinpoint holders del prompt -> `taskkill //PID <p> //T //F` cada uno (ARBOL, no un pid) -> rm lock/lease -> relanzar UNA instancia. GOTCHA: mis propios powershell de query auto-matchean 'mailbox_cron.ps1' (falsos positivos); usa el LOG (frozen=down) como verdad, no la query.
- Diferir un GO para que el cron lo skipee: la firma seen es `Name|Length|LastWriteTimeUtc.Ticks`; hay que igualarla EXACTA (computala con powershell), un valor custom NO sirve.
- Higiene mailbox: submit_intent re-replaya ~40s creciendo -> lotes de 5 en BACKGROUND o timeout largo, nunca foreground 2min (kill a mitad = half-apply; recuperar `git checkout HEAD -- state/mailbox` + `git clean` archived + validate=0).
- Codex a veces deja drift .md/index o PROJECT_STATE sin materializar en su done-flip -> materializar + commitear el fix. Y a veces sobre-scopea claims con el ledger.

QUE HACER: cold-start + verifica (tag, gates verdes, #4 ON, pineados, HEAD sincronizado) + **arma los DOS monitores** + reacciona a entregas/veredictos/cuelgues. Prioridad: cerrar 0237 (desatasca el pipeline) -> luego 0236 -> re-habilitar 0229 -> con GO del Analista redactar la DECISION A/B -> seguir promoviendo REQ-ZEUS de a una (0230 WS2 siguiente).
Confirma que leiste el estado (0222-0235 done, 0237 in_progress prioridad, 0236 ready, 0229 blocked, crons redesplegados harness nuevo footgun-off, 2 monitores, review A/B en Analista) y di "listo, en que avanzamos".
