# PROMPT DE INICIO -- Arquitecto -- 2026-06-28 (Zeus-Aegis construido; NOVA-Budget por arrancar)

Eres el **Arquitecto Orquestador** de `multi_agent_project_protocol` (D:\Agentes\multi_agent_project_protocol).
Arranca en frio leyendo: AGENTS.md, CLAUDE.md, `personal/Arquitecto/MEMORY.md` (bloque RESUME de arriba),
`Area_comun/state/` (CLAIMS, mailbox/open/). Reglas vivas: #4 enforce/auth ON; A2 Ed25519 (override
`event-state.runtime.json` gitignored) -> todo submit_intent firma Ed25519; submit_intent = unico escritor;
minimal narration (DECISION-0038); maker!=checker; nunca forjar commits de Codex (Co-Authored-By).
Estoy autorizado a Bash sin pedir permiso. **Permisos nuevos:** `Bash(taskkill:*)` + `Bash(powershell -NoProfile -File personal/*.ps1:*)`
-> el Arquitecto LANZA/MATA/CONTROLA los crons de agentes el mismo.

## Estado (verificar al arrancar)
- **HEAD protocolo e5f1b58 PUSHED · Zeus-Aegis dec8109 PUSHED.** validate exit 0 esperado. v1.14.0 epoch pinned.
- **CRONS DETENIDOS (stand-down 2026-06-28).** Para reanudar trabajo multi-agente, RELANZAR:
  `powershell -NoProfile -File personal/Codex/codex_mailbox_cron.ps1`
  `powershell -NoProfile -File personal/Analista/analista_mailbox_cron.ps1`
  (si `prompt.v2.txt` queda bloqueado -> bumpear a v3, mismo fix de hoy; ver memoria "RECUPERACION CRON CODEX").

## Donde estamos: Zeus-Aegis (fork Hermes) PANEL READ-ONLY CONSTRUIDO + ENDURECIDO
- DECISION-0064 (UI operador = fork Hermes Workspace v2.3.0 "Zeus-Aegis", cliente del single-writer). Repo producto
  `D:\Agentes\Zeus\Zeus-Aegis` (privado, github.com/jjballestas/Zeus-Aegis).
- F0 fork+seams (Gate0 verde, waiver upstream verificado) / F1 7 vistas read-only (GATE1 CERRABLE, 3 rondas
  adversariales del Analista: cazo falso-verde V3, PII V4, gate flaky V6 -> todo remediado) / F3-ro selector
  multiproyecto + dashboard metricas / F4a auth bearer + path-traversal + rate-limit 429 + e2e estable. Todo
  read-only, canonico (git show), salud/atestacion DERIVADAS, PII por construccion.
- **Falta F2 (Operate/write-through):** GATEADO post-TFM (anade writer-path al ledger MEDIDO -> contamina). F2 =
  capa que deja OPERAR desde la UI (GO/cerrar/decidir/claim via /api/governance/intent -> submit_intent).
- **PRINCIPIO DE REUSO escrito en Zeus-Aegis/pipeline.html:** chat/terminal/skills/conductor/auth/dashboard =
  REUSAR de Hermes (no reconstruir); el puente /api/governance/* a submit_intent = UNICO nuestro (Hermes no tiene
  #4/ledger/tasks). F2 = reusar conductor + UI-accion de Hermes, cablear a /intent, minimo codigo.
- **Correr el panel:** `cd D:/Agentes/Zeus/Zeus-Aegis/vendor/hermes-2.3.0` -> `$env:NODE_OPTIONS="--max-old-space-size=2048"; pnpm exec vite dev` -> http://127.0.0.1:3000/governance. (Bug: script `dev` no es Windows-safe; ENCOLAR fix cross-env para Codex.)

## Dataset TFM
- **142/500 elegibles** (Ed25519, seq>=2221; Arq 56 / Codex 78 / Analista 8 = 3 firmantes). Baseline canonico unico
  atestado (DATASET_START_SEQ=2221, N=500, stop-rule, pre-registro v2.0 FROZEN). Core congelado hasta fin de medicion.
- **PUNTO DE INFLEXION:** el build read-only que queda NO llena los 358 restantes. Para llegar a 500 (y desbloquear
  F2): recomendado **construir NOVA-Budget** (app real gobernada = coordinacion real = llena el dataset).

## NOVA-Budget (lo que sigue -- el operador lo quiere arrancar)
- El operador TIENE el diseno de DB listo y quiere construir NOVA-Budget (app de presupuesto). Es la instancia
  aplicada que llena el dataset.
- **GATE PII (DECISION-0040, app financiera):** esquema/diseno de DB (estructura) = PII-free -> puede ir al ledger
  gobernado; datos financieros reales = PII -> NUNCA al ledger (DB de la app, connector read-only DECISION-0048).
- **Camino:** DECISION (NOVA-Budget instancia aplicada; repo D:/Agentes/Zeus/NOVA-Budget; postura PII) proposed ->
  GO operador -> git-init repo producto -> ingerir el diseno de DB como 1er handover gobernado (PII-free) -> SDD
  (Codex maker / Arquitecto checker via submit_intent).
- El operador pidio ACLARAR dudas antes de fijar postura PII + modo de arranque. PROXIMO: resolver esas dudas ->
  redactar la DECISION.

## Parqueado
- Hermes/Zeus-Aegis: F2 (post-TFM), F3 chat (F3.1/3.2, no read-only), F3.5 PWA, F4.3 versionado, F4.4 DECISION final.
- Skills Fase 1. Monitor de dataset (re-armar si se reanuda generacion).
