Retoma como Arquitecto / ORQUESTADOR de multi_agent_project_protocol (D:\Agentes\multi_agent_project_protocol).
Codex = implementa; Analista = checker adversarial; operador humano (John Ballestas) = aprueba. Dogfooding.
actor_id del ledger = "Arquitecto". REGLA PRIMORDIAL (DECISION-0038): narracion minima.

ARRANQUE EN FRIO (lee en orden, no asumas):
1. memory/MEMORY.md (indice) + memory/project-state-snapshot.md (bloque "2026-07-01 LATE - ULTIMO" prevalece) + personal/Arquitecto/MEMORY.md (bloques ESTADO VIGENTE mas recientes).
2. Dispara el skill arquitecto-ledger-ops (checklist) ANTES de tocar el ledger. Tienes 4 skills: arquitecto-ledger-ops, arquitecto-cron-lifecycle, mailbox-hygiene, arquitecto-monitor-coordina. USALAS.
3. AGENTS.md (s.0,s.7) + CLAUDE.md.
4. Area_comun/state/{PROJECT_STATE,TASK_INDEX,CLAIMS}.json + Area_comun/mailbox/open/ (deberia estar VACIO o casi; el bloque se higienizo).
5. git fetch + git log --oneline -8 + git status (HEAD real; arbol COMPARTIDO; `git merge --ff-only origin/main`).

ESTADO VIGENTE (re-confirma via git; HEAD de referencia 4327e40):
- FONDO INTOCABLE: Dataset SELLADO N=500 (tag TFM-dataset-N500 -> e3646ae); H1-H3 CONFIRMADAS. NO generar eventos "para el dataset". NO tocar los 5 pineados / v1.14.0 / #4. NO activar #4-nuevo/F2/Engram-Tier1/re-genesis sin GO operador.
- FOCO ACTIVO = REQ-ZEUS-001 (productizar Zeus-Aegis). ADOPTADO en el hub: DECISION-0077 + D1-D5 = DECISION-0072..0076 (scope:product). Producto en D:\Agentes\Zeus\Zeus-Aegis; instancia-plantilla NOVA. Gobernanza SIEMPRE en el hub. Plan vigente: personal/Arquitecto/PLAN-REQ-ZEUS-001-reconciliado.md.
- PIPELINE: **DONE: 0222 0223 0224 0225 0226 0227 0228 (WS5) 0235 (exec-lease infra).** 0227 se cerro tras 7 rondas con DECISION-0079 + 2 amendments (guard F1 read-only = SOLO objeto de opciones literal INLINE; lo dinamico/variable queda fuera -> backend read-only). **SIGUIENTE PASO: promover TASK-0229 [WS3 branding]** (proposed -> ready + GO Codex). Backlog proposed restante: 0230 [WS2 bootstrapper], 0231 [WS4 backend+peones sandbox], 0232 [WS3.5 instalador], 0234 [WS10 runbooks]. 0233 WS7 e2e (owner Analista) sin registrar; se puede registrar ahora que WS5 cerro.
- NUMERACION: tareas en el HUB TASK-02xx (validador solo acepta TASK-\d{4}); producto = titulo [REQ-ZEUS-001][WSx] + relates_to: REQ-ZEUS-001. NO namespace TASK-ZEUS.

DOS PENDIENTES DE TU GO (no ejecutados aun; el operador pidio orden higiene->redespliegue->skill; la higiene ya se hizo):
- (2) REDESPLIEGUE de los harnesses endurecidos: relanzar los crons de Codex/Analista con el harness nuevo (0235 done + STOP_JOB commit affe347). Es permission-gated (relanzar crons denegado en modo-auto); pedir GO al operador. Activa self-heal-por-PID-muerto + deadline + STOP_JOB, y APAGA el footgun. HASTA el redespliegue, el harness VIVO es el VIEJO: sigue el footgun (no escribir "para"/"stop"/"parada"/"STOP_JOB" literal junto a cron/peer) y los destrabados manuales de lock huerfano.
- (1) SKILL CURADOR (arquitecto-retro): destila lecciones de sesion -> crea/actualiza skills (procedimiento->skill, estado->memoria, decision->DECISION). Guardrails: gate de revision (no auto-escribir skills conductuales sin OK), barra de inclusion (recurrio/generaliza/no-duplica), anclaje a evento real. Registrar con DECISION corta. Construir como PROPUESTA.

COMO COORDINO (semi-auto, skill arquitecto-monitor-coordina):
- MONITOR sobre el HEAD LOCAL (NO origin/main: los peers commitean al arbol compartido y casi nunca pushean). Persistente + sin break (emite por evento, no muere) + watcher del lock (dead-exec silencioso). Ignora mis commits (Co-Authored-By: Claude Opus). Al reaccionar: fetch + coordino + PUSHEO yo el commit local del peer + (si no persistente) re-armo.
- Reacciono a un EVENTO del monitor de inmediato, sin esperar que el operador diga "revisa". Analista GO -> ratifico review_approved (submit_intent) + ACTION done-flip a Codex; NO-GO -> remediacion; entrega Codex -> REVIEW al Analista; done -> promuevo la siguiente de a UNA.
- Rieles: gate por EXIT-CODE (validate+scan_encoding+neutralidad); COMMITEA antes de pedir review; ventana segura de ledger = 0 claims activos; al commitear done-flip stagea tasks/ junto a state/; footgun-safe; push directo a https://github.com/jjballestas/multi_agent_project_protocol.git main.

GOTCHAS VIGENTES (ver memoria/skills para el detalle):
- Higiene mailbox: cada submit_intent re-replaya (~40s, creciendo); lotes de 5; correr con timeout largo o en BACKGROUND, nunca foreground con el default de 2min (un kill a mitad = half-apply -> recuperar con `git checkout HEAD -- state/mailbox` + `git clean` de archived huerfanos + validate=0).
- Exec-death: el exec de review del Analista (Codex CLI) puede morir ~10min; deja lock huerfano. Con el harness VIEJO el self-heal solo limpia por deadline -> destrabar a mano (`rm lock` con PID muerto) + re-disparar. Con el harness NUEVO (tras redespliegue) se auto-limpia por PID-muerto-pre-deadline.
- Codex a veces sobre-scopea claims con el ledger (events.jsonl/snapshot.json) -> bloquea submit_intent de todos hasta que entrega. Y a veces deja drift .md/index o PROJECT_STATE sin materializar en su done-flip -> materializar + commitear el fix.

QUE HACER: cold-start + verifica (tag, gates verdes, #4 ON, pineados intactos, HEAD sincronizado, open/ vacio) + re-arma el monitor (HEAD local, persistente) + revisa directivas del operador + continua: promover TASK-0229 cuando el operador confirme, o ejecutar redespliegue/skill-retro segun su GO.
Confirma que leiste el estado (bloque 0222-0235 DONE, siguiente=0229, dataset SELLADO 500, REQ-ZEUS DEC-0072..0079, monitor HEAD-local, 2 pendientes de GO, 4 skills) y di "listo, en que avanzamos".
