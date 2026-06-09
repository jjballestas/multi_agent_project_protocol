# MEMORY.md — Memoria privada de Claude (Arquitecto del protocolo)

> Para mi yo de la próxima sesión. NO es contrato (eso es `AGENTS.md`) ni estado canónico (eso es
> `Area_comun/state/`). Referencia los canónicos; no los duplico.
> Última actualización: 2026-06-05.

## 1. Qué es este repo
`multi_agent_project_protocol`: el **protocolo multiagente genérico reutilizable**, extraído del
proyecto de trading (`bot_spot_ai_strategy_pack`) por DECISION-0005/0006. Versión publicada
**v0.1.0** (tag). Este repo **se gestiona a sí mismo** con su propio protocolo (dogfooding).

## 2. Quién soy aquí
Arquitecto Orquestador. Diseño/descompongo el backlog de enriquecimiento, reviso de forma
adversarial, mantengo `Area_comun/` y la **neutralidad de dominio**. Codex implementa (validador,
CI, scripts, tests). El operador aprueba releases y cambios incompatibles.

## 3. Para retomar (en orden)
1. `AGENTS.md`; 2. `Area_comun/state/PROJECT_STATE.json` (fase P0, next_actions);
3. `TASK_INDEX.json`; 4. `CLAIMS.json`; 5. `mailbox/open/`; 6. `Area_comun/reports/`.

## 4. Estado al cierre de la sesión (2026-06-05)
- Instancié el `Area_comun/` del repo (dogfooding) + áreas privadas `Claude/`, `Codex/`,
  `.claude/`, `CLAUDE.md`. Tag `v0.1.0`. Todo commiteado y pusheado a `main`.
- Fase **P0 = enriquecimiento**. **TASK-0001** (roadmap, `done` → `ROADMAP-v0.2.0.md`) y
  **TASK-0002** (Codex: validador Python + CI, **revisado OK por mí → `done`**).
- **Backlog priorizado dejado para la próxima sesión:** TASK-0003 (Claude, SemVer+CHANGELOG) y
  TASK-0004 (Codex, scaffolding). Ambas `proposed`, paralelizables.
- Cold-start de la nueva sesión: `RESUME.md` (raíz). Mensaje de buzón a Codex → `answered`.
- **Codex colabora bien aquí:** creó su `Codex/` y entregó TASK-0002 en paralelo sin colisión.

## 5. Reglas que no olvido
- Núcleo **neutral de dominio** (sin trading/negocio/secretos). Cambios de protocolo →
  `decisions/`. `.template.*` = masters publicados; vivos = instancia dogfooding.
- Codex puede correr en paralelo: revisar `TASK_INDEX/CLAIMS/mailbox` antes de crear/editar.
- El otro repo (trading) NO recibe mejoras del protocolo automáticamente: se adoptan por DECISIÓN.

## 6. Lecciones del proyecto madre (trading)
Codex corre EN PARALELO sobre los mismos archivos; respetar claims; comunicación barata en
tokens (ID + deltas + ACK/OK/CHANGES/BLOCKED); JSON de estado pueden quedar con BOM (leer en
Python con `utf-8-sig`); el validador corre sin `-ExecutionPolicy Bypass`.

## 7. Estado vigente (2026-06-09, HEAD 262da2f)
> El detalle completo y vivo lo mantengo en la auto-memoria de Claude Code (MEMORY.md). Aqui solo el
> puntero de cierre de sesion. Fase **P2**. v1.1.0. Escritor-unico VIVO: event_state
> enabled/materialize/enforce/authoritative TODOS `true`; drift 0 (up_to_seq 166); validador verde.

**Re-fire SA.4 — 2 prerequisitos off-pilot (GO operador 2026-06-09), SA.4 sigue DE-ARMADO:**
- **(A) Sandbox de Codex:** VERDE host-side. SANDBOX_OK pasa; lectura sin escalado; validador sin
  `require_escalated`; sin `codex.exe app-server --listen stdio://` viejos (solo el app-server de la
  sesion VS Code reabierta 03:26). Caveat: la confirmacion *dentro del sandbox de Codex* la da Codex;
  no hubo heartbeat de su lazo tras el reinicio (ultima actividad seq158-160 a las 03:00).
- **(B) Gap-8 (claim no-op):** ENCOLADO. **SPEC-0070 + TASK-0093** (ready, owner **Codex**, GO en
  mailbox) via submit_intent (commit 262da2f, seq163->166, drift 0). Opcion 1 (operador): el paso
  `claim` del orquestador (orchestrator.py:482, hoy `trace.append("claim")` NO-OP) debe ADQUIRIR el
  claim del owner ruteado (**actor_id = owner ruteado** -> `owner==actor_id` pasa
  validate_scope_authority en submit_intent.py:512-516) ANTES de run_turn; scope cubre changed_paths;
  idempotente con pre-claim (byte-equivalente); conflicto con otro agente rechaza; reconciliacion del
  claim auto-reportado por el LLM (sin doble-acquire, SPEC-0070 2.3); release/handoff por outcome
  terminal. Decidi con el operador: **implementa Codex, yo (Claude) ratifico** adversarialmente +
  SMOKE REAL end-to-end.

**Mi pendiente (cuando Codex entregue TASK-0093 a in_review):** ratificar adversarialmente (golden +
byte-equivalencia + lectura de contrato) -> cerrar por submit_intent -> **SMOKE REAL** (orquestador
adquiere claim -> codex edita README -> gate ACEPTA con changed_paths+transicion+agent=Codex con claim
activo) -> reportar al operador -> esperar su **GO al re-fire** (re-armar registro: real_invoker+
supervised_autonomy enabled=true, verificar activation_error None / subprocess_multiturn_allowed True /
drift 0 / PAUSE ausente / replay==hot -> disparar orchestrator `--llm-preset codex` caps 2/1/180000,
checkpoint tras turno 1). El re-fire es **el unico multiplicador**; Capa C OFF; SA.4 y Capa C nunca
juntos.

**Riesgo a vigilar:** si el lazo de Codex revive, podria auto-reclamar TASK-0093 en carrera; es el
flujo esperado (ready+GO). Para el re-fire del piloto, usar el centinela `runtime/state/PAUSE` para
quiescer el lazo de Codex y evitar carrera con el orquestador. Proximos IDs: TASK-0094 / SPEC-0071.

**Higiene mailbox:** 2 FYI en open/ sin respuesta (anomalia-task0092-resuelta + sandbox de Codex) que
el validador sugiere archivar; las dejo (no son mias para archivar bajo claim ajeno / o pendientes de
prune). El nuevo GO de TASK-0093 requiere respuesta de Codex.

## 8. HECHO OPERATIVO (operador 2026-06-09): Codex es PUSH-DRIVEN
El lazo autonomo de **Codex NO ejecuta por su cuenta**; solo corre cuando el **operador lo empuja**.
Confirmado con TASK-0093: la encole ready+GO (commit 262da2f) y el lazo NO la tomo hasta que el
operador empujo a Codex; entonces SI la reclamo (CLAIM-20260609-task0093-codex, seq167-168) y la esta
implementando (ediciones sin commitear en runtime/orchestrator.py, apply.py, llm_adapter.py + golden).
**Implicacion:** "encolo ready+GO -> Codex auto-reclama y ejecuta" NO se cumple solo; el disparador es
el push del operador. NO asumir auto-claim; en reportes decir explicito que el avance de una tarea de
Codex requiere el push. Mi intento de re-reclamar TASK-0093 como Claude FALLO por diseno (guard de
solape de validate_scope_authority) = anti-colision funcionando; sin rastro (raise antes de escribir).
Por CLAUDE.md regla 3 estoy HANDS-OFF de TASK-0093 (in_progress, owner Codex); vuelvo a ROL
RATIFICADOR (plan original: Codex implementa, Claude ratifica). Espero su entrega a in_review ->
ratifico adversarial (byte-equiv de 9 goldens SA con pre-claim + contrato + drift + paridad .ps1) ->
SMOKE REAL (orquestador adquiere claim -> codex edita README -> gate ACEPTA) -> cierro + reporto -> GO
re-fire. PUNTOS A VIGILAR en la ratif. (mapeados en el codigo): (a) release-on-rejection (no dejar
claim huerfano; preservar cero-footprint del piloto); (b) handoff-release en in_review (§7; build_prompt
ya NO emite claims -> algo debe liberar); (c) byte-equiv de goldens con pre-claim (idempotencia keyea en
unit['owner'] ruteado = reviewer para in_review, casa case_fix_cycles); (d) bajo authoritative
acquire/release POR el log (submit_intent), nunca edicion directa de CLAIMS.json -> drift 0.

**MAILBOX LOCKEADO por Codex:** su auto_claim cubre mailbox/open + mailbox/archived ENTEROS -> NO puedo
coordinarme por mailbox mientras trabaja. Prepare la coordinacion del hecho push-driven como BORRADOR en
`personal/Claude/DRAFT-MSG-Claude-to-Codex-push-driven-execution.md` (FYI, sin respuesta requerida); lo
deposito en mailbox/open SOLO en ventana segura (cuando Codex libere su claim al entregar TASK-0093).
Follow-up recomendado: eximir el mailbox del auto-claim de Codex (smell DECISION-0020).

## 9. SANDBOX DE CODEX - CAUSA RAIZ VERIFICADA (2026-06-09, commit 720b417)
Fallo "windows sandbox: spawn setup refresh" = **os error 740 (ERROR_ELEVATION_REQUIRED)**. El binario
`codex-windows-sandbox-setup.exe` exige ELEVACION para el setup refresh; ni el app-server de la
extension (background) ni `codex exec` no interactivo consiguen UAC -> falla. **Correlacion con la
instalacion del CLI CONFIRMADA** (hipotesis del operador): `C:\Users\johnb\.codex\config.toml`
(reescrito HOY 03:23 al instalar el CLI) tiene `[windows] sandbox = "elevated"`; ese config es GLOBAL y
lo leen TANTO el CLI (`.local\bin\codex.cmd` v0.137.0-alpha.4) COMO la extension VS Code -> el fallo
aparece en ambos. La repro externa de Codex (`codex exec -s read-only` reproduce el fallo en reads)
descarta "solo app-server stale". El PONG funciono porque no usa tool sandboxed; cualquier read/tool
sandboxed dispara el setup refresh elevado -> 740. **FIX (verificado en https://developers.openai.com/codex/windows;
valores validos elevated|unelevated):** cambiar a `sandbox = "unelevated"` en
`C:\Users\johnb\.codex\config.toml` + restart (unelevated = ACL-based, NO requiere admin; revierte el
efecto del CLI). Alternativa: correr VS Code como Admin (conserva elevated). **Lo aplica el OPERADOR**
(config de su maquina + restart). Relevante para SA.4: el invoker `codex exec` del piloto chocaria con
740 bajo elevated -> aplicar el fix ANTES del re-fire. Coordinado con Codex por mailbox (RESPONSE a su
REQUEST verify-correlation). Mailbox AHORA libre (claims vacios).

## 10. TASK-0093 EN IN_REVIEW - PENDIENTE MI RATIFICACION (Codex entrego, commit d6569f4)
Codex IMPLEMENTO y entrego TASK-0093 (gap-8 claim-acquire) a `in_review`, claim liberado, drift 0
seq170; commit `d6569f4 fix(runtime): acquire routed claims before turns` (+253 inserc:
orchestrator.py+106, apply.py+53, llm_adapter.py+1, golden runtime_loop+102). Handoff:
`Area_comun/handoffs/HANDOFF-TASK-0093-codex-to-claude-1.md`. PENDIENTE (mi turno): RATIFICAR
adversarial (byte-equiv goldens con pre-claim + contrato: idempotencia/conflicto-rechazo/release-on-
rejection/handoff-release in_review/acquire-release por log bajo authoritative + validador + drift +
paridad .ps1) -> SMOKE REAL end-to-end (orquestador adquiere claim->codex edita->gate ACEPTA), que
NECESITA el sandbox arreglado (unelevated) primero -> cierro TASK-0093 (reviewer in_review->done por
submit_intent) -> reporto al operador para GO al re-fire SA.4. Proximos IDs TASK-0094/SPEC-0071.
