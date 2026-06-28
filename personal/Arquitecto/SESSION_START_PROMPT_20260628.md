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
- **PUNTO DE INFLEXION:** el build read-only que queda NO llena los 358 restantes por si solo (decision de como
  llegar a 500 = mas adelante; NO ahora).

## FOCO AL REANUDAR: AJUSTAR EL FORK (Zeus-Aegis). NOVA-Budget = STAND-BY.
- **Decision del operador (2026-06-28): NO arrancar NOVA-Budget todavia.** "El fork necesita ajustes." NOVA queda
  en stand-by (el diseno de DB existe pero NO se ingiere aun; no redactar la DECISION de NOVA hasta nuevo GO).
- **PROXIMO: preguntar al operador QUE ajustes quiere en el fork** y priorizar. Candidatos conocidos (sugerir, el
  operador decide):
  1. **dev script Windows-safe** (bug REAL ya visto): `pnpm dev` falla en Windows por `NODE_OPTIONS="..." vite dev`
     (sintaxis Unix). Fix: `cross-env` en vendor/hermes-2.3.0/package.json -> tarea SDD a Codex (producto).
  2. **Reusar el conductor de Hermes** para lanzar/parar agentes desde la UI (en vez de crons a mano).
  3. Retirar bloat: aislar/quitar el subsistema de juego 3D (three/fiber/rapier) + empaquetado Electron.
  4. Resolver o re-waivar los 24 fallos upstream de Hermes (estaban "antes de F1/F2"; F1 ya cerrado con waiver).
  5. F3 chat (F3.1/3.2 shim runtime), F3.5 PWA/movil, F4.3 versionado/CHANGELOG del fork.
- Todo ajuste de producto = repo Zeus-Aegis, SDD Codex maker / Arquitecto checker, genera dataset igual. F2 sigue
  gateado post-TFM. NO tocar el core del protocolo ni el baseline congelado.

## Parqueado
- Hermes/Zeus-Aegis: F2 (post-TFM), F3 chat (F3.1/3.2, no read-only), F3.5 PWA, F4.3 versionado, F4.4 DECISION final.
- Skills Fase 1. Monitor de dataset (re-armar si se reanuda generacion).
