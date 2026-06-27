---
decision_id: DECISION-0064
title: UI del operador = fork de Hermes Workspace (MIT) "Zeus-Aegis", cliente del single-writer; contrato /api/governance/*; F0 ACTIVABLE ya, F2 (writer-path vivo) GATEADO a post-TFM
status: accepted
ratified_at: 2026-06-27
date: 2026-06-27
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0050, DECISION-0022, DECISION-0028, DECISION-0020, DECISION-0040, DECISION-0062, DECISION-0066, DECISION-0067]
phase: P2
---

# DECISION-0064 - UI del operador sobre un fork de Hermes ("Zeus-Aegis"), cliente del single-writer

> PROPUESTA (revisada 2026-06-27 tras verificacion en internet + creacion del repo). El operador investigo y
> RATIFICO el nombre **Zeus-Aegis** para montar la UI del panel sobre un fork de **Hermes Workspace**
> (`outsourc-e/hermes-workspace`, MIT) en vez de construir el chrome desde cero. Plan detallado del operador en
> `personal/operador/Hermes/` (README + PLAN_INTEGRACION + PROMPT + control.html). **Repo de producto creado:**
> `D:\Agentes\Zeus\Zeus-Aegis` -> `https://github.com/jjballestas/Zeus-Aegis.git` (privado recomendado).

## Contexto

DECISION-0050 fijo el front como panel del operador (codigo en repo producto bajo `D:\Agentes\Zeus\`). En vez de
seguir construyendo el chrome (shell/chat/terminal/skills/memoria/layout/movil), se forkea Hermes (MIT, ya provee
ese chrome) y se monta ENCIMA la gobernanza especifica de la metodologia. La direccion sana es **"su UI sobre tu
metodologia"**: el runtime es la fuente de verdad / single-writer; la UI **lee** slim views y **escribe solo** via
`submit_intent`.

**Verificacion a fondo (2026-06-27, fuentes primarias GitHub/raw):**
- Hermes `outsourc-e/hermes-workspace` EXISTE, **MIT** (c) 2026 Eric; ultimo release **v2.3.0**; 5.8k estrellas,
  ~3 meses de vida, autor unico, cadencia rapida (churn -> pin a v2.3.0, no seguir `main`).
- **Stack real NO es Next.js** (como decia el material): es **TanStack Start + Vite 7 + React 19 + Electron 40**,
  y arrastra un motor de juego 3D (`three`/`@react-three/fiber`/rapier) que se retira. El port "casi directo desde
  zeus si es Next.js" NO aplica: hay que reescribir la capa de datos para hablar `submit_intent`/ledger.
- Seams asumidos (gateway :8642, dashboard :9119, UI :3000, `/api/sessions`, conductor spawn/stop,
  `HERMES_API_URL`, `HERMES_API_TOKEN`) son REALES. "capability gates" NO es concepto de Hermes (es termino propio).

## Decision

1. **Nombre/repo:** el fork se llama **Zeus-Aegis** (la egida = el escudo de Zeus sobre el ledger). Repo de
   producto separado del core neutral (DECISION-0050), creado en `D:\Agentes\Zeus\Zeus-Aegis`.

2. **La UI es CLIENTE del single-writer (DECISION-0022/0028).** Toda mutacion de estado pasa por
   `runtime/submit_intent.py` (transaccion atomica); el hard-gate B.3 rechaza ediciones manuales del ledger como
   drift. **Ningun camino UI/Node escribe `Area_comun/state/*.json`.** La inversa romperia `enforce/authoritative`.

3. **Contrato `/api/governance/*`:** lectura (health/state/backlog/mailbox/decisions/handoffs/ledger) sobre slim
   views (read-only, cold-start barato); escritura `POST /api/governance/intent` -> `submit_intent --intents`
   (kinds `task_status`/`task_upsert`/`claim`/`decision`). Anti-colision DECISION-0020 + manejo legible de B.3.

4. **Reuso de zeus-protocol:** se portan las **vistas/logica de gobernanza** (Intake RF-14, Mailbox, Backlog,
   Artifacts, consola agente-a-agente, Operate); se **descarta el chrome** que Hermes ya hace mejor. **Zeus-protocol
   se CONGELA en su MVP actual** (sirve de panel read-only para la demo del TFM); no se le agregan features de
   producto nuevas (seria trabajo desechable si Zeus-Aegis lo suplanta).

5. **Licencia:** conservar `LICENSE` MIT + avisos de copyright de Hermes; renombrar el fork (copyright != marca);
   anadir copyright propio a archivos nuevos; mantener el protocolo propietario como **backend separado** (no
   mezclar core propietario con archivos MIT). Ver `Zeus-Aegis/NOTICE.md`. *No es asesoria legal.*

6. **Fases con gates** (del plan del operador): F0 fork+seams+inventario -> F1 read-only -> F2 write-through ->
   F3 chat/multiproyecto -> F4 hardening. SDD por fase, maker=Codex / checker=Arquitecto.

7. **GATE de orden (clave, reconciliado con el TFM):**
   - **F0 (fork privado + pin v2.3.0 + seams + inventario + rebrand) = ACTIVABLE YA.** Esta fuera del core, no toca
     el ledger ni anade writer-path; es seguro durante la ventana de medicion.
   - **F2 (write-through: cablear la UI a `submit_intent` contra el ledger VIVO) = GATEADO a post-TFM.** Es el
     unico paso que anade un **writer-path nuevo al ledger vivo** -> cambia el sistema bajo medicion y el modelo de
     amenaza A2 (DECISION-0066) tendria que re-contemplarlo -> contaminaria el experimento. NO arrancar hasta que la
     medicion (H1-H3) este congelada/capturada.
   - **F1 (panel read-only sobre slim views)** no anade writer-path; es admisible pero de baja prioridad (Zeus ya
     cubre la observacion). Queda a criterio del operador; por defecto se difiere para no dispersar foco del TFM.

8. **Motor de dataset (aclaracion, NO cambia el aparato):** el dataset Ed25519 crece con la **gobernanza de
   construir el fork** (tasks/claims/decisiones/handoffs de F0 via `submit_intent`, maker=Codex/checker=Arquitecto
   -> ambos firman -> avanza el hito >=2 agentes), que es **uso normal del protocolo**, NO un cambio del aparato. El
   dataset **no** depende de cablear la UI al ledger (eso es F2, gateado). **Pendiente de confirmar:** si esos
   eventos de construir Zeus-Aegis caen dentro del alcance del **pre-registro v2.0 FROZEN**; si exigiera ampliar el
   alcance, eso es un **pre-registro v2.x ANTES de mirar resultados**, no un cambio en caliente.

9. **Gentleman ecosystem (verificado, no adoptar como dependencia):** **engram RECHAZADO** (SQLite/FTS5 no
   atestado = 2a fuente de verdad + sync cloud = fuga PII; rompe single-writer/#4 y DECISION-0040). **gentle-ai /
   Gentleman.Dots = solo inspiracion** (convenciones SDD convergentes para citar en el escrito; el "estimador de
   costos -> budget.py" NO existe; "model-por-fase" es OpenCode-only; "harness_test_runner.go" no existe). El
   material original inflaba capacidades; esta decision fija los hechos verificados.

## Alcance / No-alcance

- **En alcance:** Zeus-Aegis como cliente del single-writer sobre un fork de Hermes v2.3.0; contrato
  `/api/governance/*`; reuso de la gobernanza de zeus; licencia/atribucion; activar **F0** ya.
- **Fuera de alcance:** cambiar el core neutral; tocar el mecanismo #4; arrancar **F2** (writer-path vivo) antes de
  congelar el TFM; medir el TFM (eso es el pre-registro + DECISION-0066); cualquier escritura directa al ledger
  desde la UI; adoptar engram/gentle-ai/Dots como dependencia.

## Consecuencias

- El operador obtiene un panel ergonomico sin reinventar shell/chat/terminal, sobre un protocolo ya probado, y la
  **gobernanza de construirlo alimenta el dataset** sin contaminar el aparato (mientras no se cablee F2 al vivo).
- El trabajo de gobernanza de zeus-protocol se reusa (no se pierde); su chrome se sustituye por lo nativo de Hermes;
  Zeus-protocol se congela en MVP.
- Riesgos: romper single-writer (mitiga guard F2.2 + GATE F2 post-TFM), churn del API de Hermes (pin v2.3.0),
  sandbox stale (ejecutar desde entorno real), contaminacion de licencia (backend separado), bloat (retirar juego
  3D + Electron), sobre-alcance (respetar gates; F2 gateado).

## Alternativas consideradas

- **Seguir construyendo el chrome en zeus-protocol:** mas trabajo, peor ergonomia, desechable si Zeus-Aegis lo
  suplanta; descartado salvo como fuente de componentes de gobernanza a portar.
- **UI como escritor del estado:** rompe single-writer/enforce; descartado (la UI es cliente, nunca escritor).
- **Adoptar engram como capa de persistencia:** 2a fuente de verdad no atestada; descartado (rompe #4/PII).
- **Arrancar F1+ en cualquier momento (parking total post-TFM, version previa de esta decision):** demasiado
  conservador; F0 es demostrablemente segura fuera del core. Se libera F0; se mantiene el gate solo donde hay
  writer-path vivo (F2).
