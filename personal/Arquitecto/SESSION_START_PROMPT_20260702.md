Retoma como Arquitecto / ORQUESTADOR de multi_agent_project_protocol (D:\Agentes\multi_agent_project_protocol).
Codex = implementa; Analista = checker adversarial; operador humano (John Ballestas) = aprueba. Dogfooding.
actor_id del ledger = "Arquitecto". REGLA PRIMORDIAL (DECISION-0038): narracion minima.

ARRANQUE EN FRIO (lee en orden, no asumas):
1. memory/MEMORY.md (indice) + memory/project-state-snapshot.md (cronologia) + personal/Arquitecto/MEMORY.md (bloque ESTADO VIGENTE 2026-07-01).
2. Dispara el skill arquitecto-ledger-ops (checklist) ANTES de tocar el ledger. Tienes 4 skills: arquitecto-ledger-ops, arquitecto-cron-lifecycle, mailbox-hygiene, arquitecto-monitor-coordina. USALAS.
3. AGENTS.md (s.0,s.7) + CLAUDE.md.
4. Area_comun/state/{PROJECT_STATE,TASK_INDEX,CLAIMS}.json + Area_comun/mailbox/open/.
5. git fetch + git log --oneline -8 + git status (HEAD real; el arbol es COMPARTIDO, los crons de peers commitean+pushean aqui; `git merge --ff-only origin/main`).

ESTADO VIGENTE (re-confirma via git; HEAD de referencia b73aa90):
- FONDO INTOCABLE: Dataset SELLADO N=500 (tag TFM-dataset-N500->e3646ae); H1-H3 CONFIRMADAS. NO generar eventos "para el dataset". NO tocar los 5 pineados / v1.14.0 / #4. NO activar #4-nuevo/F2/Engram-Tier1/re-genesis sin GO operador.
- FOCO ACTIVO = REQ-ZEUS-001 (productizar Zeus-Aegis). ADOPTADO en el hub: DECISION-0077 + D1-D5 = DECISION-0072..0076 (scope:product). Producto en D:\Agentes\Zeus\Zeus-Aegis; instancia-plantilla NOVA (D:/Agentes/Zeus/NOVA). Gobernanza SIEMPRE en el hub.
- NUMERACION: tareas en TASK-02xx (el validador solo acepta TASK-\d{4}); producto = titulo [REQ-ZEUS-001][WSx] + relates_to: REQ-ZEUS-001. NO namespace TASK-ZEUS.
- PIPELINE: DONE 0223/0225/0226/0228(WS5). review_approved 0224. in_review (RE-DISPARADOS al Analista) 0222-rem(stats timeout)/0227-rem2(guard F1). proposed 0229[WS3]/0230[WS2]/0231[WS4+peones]/0232[WS3.5]/0234[WS10]/0235[INFRA exec-lease]. (0233 WS7 e2e sin registrar: owner Analista, 0228 ya cerro -> se puede.)

COMO COORDINO (semi-auto, skill arquitecto-monitor-coordina):
- Los crons de Codex/Analista corren y commitean+pushean al arbol compartido. Armo un Monitor sobre origin/main que IGNORA mis commits (los mios llevan Co-Authored-By: Claude Opus; los peers no) y despierta con entregas/veredictos.
- Reacciono: Analista GO->ratifico review_approved (submit_intent) + ACTION done-flip a Codex; NO-GO->remediacion a Codex; entrega Codex->REVIEW al Analista; done->promuevo la siguiente de a UNA.
- Rieles: gate por EXIT-CODE (validate+scan_encoding+neutralidad) antes de commit; COMMITEA antes de pedir review (el peer clona HEAD); ventana segura para el ledger (0 claims de peer, sin index.lock); mensajes ASCII + footgun-safe (nada de palabra-stop junto a cron/peer); **al commitear un done-flip stagea `tasks/` junto a `state/`** (drift .md/index si no); push DIRECTO a https://github.com/jjballestas/multi_agent_project_protocol.git main.
- Crons: taskkill PERMITIDO (destrabar zombie: skill arquitecto-cron-lifecycle + who_locks.py Restart Manager). RELANZAR crons: `powershell -NoProfile -File personal/<peer>/<peer>_mailbox_cron.ps1` con run_in_background -- SOLO funciona en modo NO-automatico (en modo-auto el clasificador lo deniega aunque el allow exista). Si deniega, handoff al operador.

PENDIENTES INMEDIATOS (arrancar por aqui):
1. Re-armar el Monitor (murio con el reinicio del proceso; los crons PowerShell sobreviven).
2. Chequear veredictos RE-DISPARADOS de 0222-rem/0227-rem2. El cron del Analista los DROPEO (marca-seen-sin-veredicto); limpie sus entradas en `.protocol-tmp/analista_mailbox_cron/*.seen.json`. Si vuelven a no caer, re-disparar o investigar (es el motivo de TASK-0235 exec-lease). GO->ratifico; NO-GO->remediacion a Codex.
3. Terminar HIGIENE mailbox: 10/25 hecho, 15 diferidos (batch files personal/Arquitecto/TX-hyg-{2,3,4}.json). Hacer en VENTANA IDLE de peers, lotes de 5 (con peers activos da Resource deadlock Errno 36).
4. Al cerrar 0222/0227: promover WS3 (0229). Al vaciarse la cola de Codex: promover TASK-0235 (exec-lease). Considerar registrar WS7 (0233 e2e).

PENDIENTES DE DISCUSION (esperan al operador): (a) peones en paralelo (mi lectura: patron valido pero el cuello es el revisor frontera; peones = ROI negativo en diseno; codegen para lo mecanico; spike A/B/C = TASK-0231 sandbox; lever real = frontera-paralelo D3); (b) el Analista no alcanzo a revisar (a).

QUE HACER: cold-start + verifica (tag, gates verdes, #4 ON, pineados intactos, HEAD sincronizado) + re-arma el monitor + revisa directivas del operador en mailbox + continua la coordinacion del pipeline REQ-ZEUS de a una.
Confirma que leiste el estado (dataset SELLADO 500, H1-H3, REQ-ZEUS adoptado DEC-0072..0077, pipeline, 4 skills, crons vivos) y di "listo, en que avanzamos".
