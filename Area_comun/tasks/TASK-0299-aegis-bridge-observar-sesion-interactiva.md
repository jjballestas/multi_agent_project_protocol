---
task_id: TASK-0299
title: "Aegis Front MVP L1 unidad 2 (fast-follow de 0298): el bridge observa TAMBIEN la sesion INTERACTIVA del Arquitecto tailando su transcript jsonl de Claude Code (redactado, observation-only)"
type: feature
status: review_approved
owner: Codex
maker: Codex
checker: Analista
reviewer: Analista
phase: P2
priority: normal
created_at: 2026-07-27
code_repo: D:/Agentes/Zeus/Zeus-protocol
origin: TASK-0178 / DESIGN-0178 (Aegis Front) -- resuelve el riesgo E1 de TASK-0298 (fuente cron solo ve el modo cron); operador 2026-07-27 "haz lo necesario"
depends_on: TASK-0298
project: multi_agent_project_protocol
relates_to: [TASK-0178, TASK-0298, TASK-0187, DECISION-0050, DECISION-0095, DECISION-0040]
linked_decisions: [DECISION-0050, DECISION-0095, DECISION-0040]
file: Area_comun/tasks/TASK-0299-aegis-bridge-observar-sesion-interactiva.md
intake:
  type: feature
  goal: Fast-follow de TASK-0298 que cierra su riesgo declarado E1. TASK-0298 hace que el bridge observe al Arquitecto en modo CRON (tail de run-logs); pero cuando el Arquitecto corre INTERACTIVO (sesion Claude Code, el modo mas comun) no hay run-log del cron y el panel muestra "sin sesion viva". Esta unidad anade una SEGUNDA fuente de observacion: el TRANSCRIPT jsonl que Claude Code YA escribe en vivo por sesion en ~/.claude/projects/<project-slug>/<session-id>.jsonl (verificado: entradas type=assistant/user/system/attachment con message + timestamp + cwd + gitBranch; ~18k lineas/sesion). El bridge lo TAILEA (read-only), identifica la sesion VIVA (jsonl mas reciente cuyo cwd/gitBranch = el hub; maneja multiples/dual-session), parsea las entradas y emite eventos SSE de observacion REDACTADOS. Extiende el mismo bridge observation-only de 0298 (no lo rehace): misma plomeria SSE + audit + coalescing; se AGREGA un tipo de fuente. Observation-only, read-only, sin canal de control (I1), sin spawn (I3). Depende de 0298 (mismos archivos) -> se construye DESPUES de que 0298 cierre.
  acceptance:
    - AC1 SEGUNDA FUENTE - config/env selecciona la fuente de observacion: cron-run-log (0298) o session-transcript (esta unidad). observeSessionsDir por config/env (NO hardcode; el checker corre en clon limpio sin el ~/.claude del maker). Con un dir de transcripts + un jsonl "vivo" fixture, escribir entradas incrementales emite eventos SSE de observacion.
    - AC2 IDENTIFICACION DE SESION VIVA - elige el jsonl MAS RECIENTE cuyo cwd/gitBranch corresponde al proyecto observado; maneja el caso de multiples sesiones concurrentes (dual-session) de forma determinista y documentada; si no hay sesion viva, degrada a 'dormant' (nunca inventa).
    - AC3 PARSEO jsonl -> EVENTOS - parsea las entradas relevantes (assistant/user/system) y emite un evento de observacion por entrada con type/role/timestamp + un cuerpo REDACTADO; ignora el ruido (queue-operation/ai-title/file-history-*). Granularidad documentada (que se surfacea del assistant/tool-calls/user).
    - AC4 REDACCION PII FUERTE (critico, DECISION-0040) - el transcript contiene TODO: inputs/outputs de tools, contenido de archivos, estado gobernado, PII. La redaccion (reusa/endurece redactPublicText + el vector de TASK-0187) DEBE aplicarse a CADA cuerpo antes del SSE y del audit; test con PII inyectada en el transcript -> [*-REDACTED] en SSE y audit, literales AUSENTES. Documentar que la redaccion es best-effort y el panel queda tras operatorPresentRequired + localhost.
    - AC5 OBSERVATION-ONLY / READ-ONLY / SIN CONTROL - el bridge solo LEE el transcript + escribe su propio audit; cero escritura a estado gobernado; el canal de control sigue deshabilitado (I1, heredado de 0298); el manager sigue SIN spawn (I3). Snapshot byte-a-byte de estado gobernado de muestra ANTES/DESPUES = identico.
    - AC6 CONTRATO + GATES - se mantiene la lista contractual de endpoints del bridge; node --test verde en Zeus-protocol; tests nuevos de la segunda fuente (identificacion de sesion, parseo, redaccion, dormant).
  verification_cmd:
    - cd D:/Agentes/Zeus/Zeus-protocol
    - node --test
    - (checker en clon limpio; observeSessionsDir por config/env, JAMAS hardcode)
  scope_routes:
    - D:/Agentes/Zeus/Zeus-protocol/src/server.js
    - D:/Agentes/Zeus/Zeus-protocol/architect-bridge.config.json
    - D:/Agentes/Zeus/Zeus-protocol/public/app.js
    - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
  out_of_scope:
    - Reescritura a React -- FUERA (vanilla existente).
    - Cualquier escritura al ledger/estado gobernado del hub -- READ-ONLY.
    - Re-abrir el canal de control o el spawn -- PROHIBIDO (I1/I3 de 0298 se conservan).
    - protocol.config.json pineado del hub (2E35F26E) -- fondo intocable.
    - Empezar antes de que 0298 este DONE -- depende de 0298 (mismos archivos); el GO se emite tras cerrar 0298.
  risk: medium
  estimate: M
---

# TASK-0299 - Aegis L1 unidad 2 (fast-follow de 0298): observar la sesion INTERACTIVA via transcript jsonl

> maker=Codex / checker=Analista. Repo = Zeus-protocol. DEPENDE de TASK-0298 (mismos archivos del bridge)
> -> el GO se emite DESPUES de que 0298 cierre (done). Origen: cierra el riesgo E1 de 0298; el operador
> pidio "haz lo necesario" para observar la sesion interactiva (2026-07-27).

## Encuadre
0298 hace que el bridge observe al Arquitecto en modo CRON (tail de run-logs). Pero el Arquitecto suele
correr INTERACTIVO (Claude Code), y ahi no hay run-log del cron -> el panel diria "sin sesion viva". Esta
unidad anade una SEGUNDA fuente: el transcript jsonl que Claude Code YA escribe por sesion en
~/.claude/projects/<project-slug>/<session-id>.jsonl (verificado: ~18k lineas, entradas assistant/user/
system con message+timestamp+cwd+gitBranch). El bridge lo TAILEA read-only, identifica la sesion viva,
parsea y emite eventos SSE REDACTADOS. Extiende el bridge observation-only de 0298; no lo rehace.

## Lo que de verdad importa (para el maker y el checker)
1. **Redaccion PII es lo mas critico.** El transcript tiene TODO (tool inputs/outputs, contenido de
   archivos, estado gobernado, PII). CADA cuerpo se redacta antes del SSE y del audit (DECISION-0040).
   El panel queda tras operatorPresentRequired + localhost; la redaccion es best-effort declarada.
2. **observeSessionsDir por config/env, NUNCA hardcode** (el checker no tiene el ~/.claude del maker).
3. **Identificacion de sesion viva determinista** (jsonl mas reciente por cwd/gitBranch del proyecto;
   maneja dual-session).
4. **Se conservan I1 (sin control) e I3 (sin spawn) de 0298.** Esta unidad SOLO agrega una fuente de
   lectura; no reintroduce spawn ni el canal de control.

## Dependencia
Bloqueada por TASK-0298 (edita los mismos archivos del bridge). El Arquitecto emite el GO de 0299 recien
cuando 0298 este DONE. Ciclo gobernado normal (maker Codex -> recomputo Arquitecto -> review Analista clon
limpio Zeus -> ratifico -> done-flip). Tope 2 iteraciones.
