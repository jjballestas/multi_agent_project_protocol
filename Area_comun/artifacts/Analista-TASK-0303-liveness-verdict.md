# VEREDICTO ADVERSARIAL - TASK-0303 (harness: revisar liveness antes de matar + post-delivery en in_review)

Reviewer: Analista (voz independiente / checker)
Fecha (hora local UTC+2): 2026-07-29 03:12
Recomendacion de cierre: **OK-CLOSABLE**

## Ancla canonica (no arbol caliente)
- Producto bajo revision: HUB (multi_agent_project_protocol). Sin producto Zeus/Nova en alcance (instruccion).
- Commit de implementacion: `e266d07` (fix: gate kills on bounded liveness). Entrega `c5a71eb`. Protocol HEAD origin/main `3b2d66a`.
- Epoch pineado 1.14.0. `protocol.config.json` byte-identico: `git diff --exit-code adb1dfa e266d07 -- protocol.config.json` = **exit 0**.
- Fix vive SOLO en: `scripts/harness/peer_mailbox_cron.ps1` + `examples/mailbox_retry_cases/run_mailbox_retry_cases.py`.

## Reproduccion (clon LIMPIO, no in-place)
Clonado a ruta corta bajo el scratch root designado: `D:/Aegis_Scratch/protocol/ccv0303`, `git checkout e266d07`, arbol limpio.
Gate por EXIT code:

| Gate | Comando | Exit |
|------|---------|------|
| Banco de regresion (AC4, 17 casos) | `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py` | **0** |
| Estado colaboracion | `python scripts/validate_collaboration_state.py` | **0** |
| Encoding | `python scripts/scan_encoding.py` | **0** |
| Neutralidad de dominio | `python scripts/scan_domain_neutrality.py` | **0** |
| Sintaxis .ps1 (PSParser Tokenize) | `[PSParser]::Tokenize(<ps1>,[ref]$e)` | **0 errores (PS1_SYNTAX_OK)** |
| Alcance (config intocable) | `git diff --exit-code adb1dfa e266d07 -- protocol.config.json` | **0** |

Diff de `e266d07`: solo las 2 rutas del fix + bookkeeping gobernado del propio TASK (CLAIMS/PROJECT_STATE/TASK_INDEX/events/snapshot/TASK-0303.md). Ningun otro archivo de codigo.

## No confie en el nombre del test: mutacion adversarial propia
No me fie de que el banco pase; mute el harness `.ps1` yo mismo y re-corri los casos afectados. Cada mutante DEBE
matar su caso, o la falsabilidad seria falsa. Los 4 mutantes MUEREN; el pristine restaura a PASS y byte-identico.

| # | Mutacion inyectada en peer_mailbox_cron.ps1 | Caso ejercido | Resultado |
|---|---------------------------------------------|---------------|-----------|
| a | `Get-OwnDeliveryEvidence` -> `Get-OwnEvidence` (gatillar-en-cualquier-escritura) | run_pre_delivery_and_liveness_cases | **FAIL (muere)** |
| b | `$progress.progressing -and ...ExecHardDeadline` -> `$false` (kill-incondicional al deadline) | run_pre_delivery_and_liveness_cases | **FAIL (muere)** |
| c | `...UtcNow -lt $execHardDeadlineUtc` -> `$true` (tope duro removido) | run_pre_delivery_and_liveness_cases | **FAIL (muere)** |
| c' | post-delivery `progressing -and ...HardDeadline` -> `$true` (exec CONGELADO nunca matado) | run_post_delivery_timeout_case | **FAIL (muere)** |
| - | pristine restaurado | ambos | **PASS** |

## Vector por vector (AC del intake)

| AC | Garantia | Como la probe (comportamiento + mutacion) | PASS/SLIP |
|----|----------|-------------------------------------------|-----------|
| AC1 | Post-delivery arranca SOLO en la transicion a `in_review` de una tarea que el actor POSEE; no en el reclamo ready->in_progress ni en claim/memoria previos | Codigo: `Get-OwnDeliveryEvidence` exige `payload.intent_type=task_status` AND `transitions.task_status.to -cne "in_review"` AND `task_id` con owner==PeerId en TASK_INDEX, ademas de firma ed25519/keyid/applied. El fixture escribe un evento de reclamo (ready->in_progress) y el test asevera `POST_DELIVERY_WINDOW_START` AUSENTE. Mutacion (a) -> window arranca en el reclamo -> caso muere. | **PASS** |
| AC2 | Al vencer el deadline (ExecTimeout o post-delivery) el harness REVISA liveness (heartbeat fresco AND/OR run-log creciendo AND/OR ledger/arbol) y solo TREE_KILL si esta COLGADO; si progresa extiende ACOTADO con TOPE DURO | Codigo: `Get-ExecProgressState` (3 senales OR) + extension `ProgressExtensionSeconds` topada por `$execHardDeadlineUtc = deadline + ProgressHardCapSeconds`; logs `EXEC_PROGRESSING`/`EXEC_HUNG(reason=hard_cap|no_progress)`. Comportamiento: exec que escribe stderr sobrevive el ExecTimeout=2 (extiende, elapsed>=4) y muere en el hard cap. Mutaciones (b) kill-incondicional y (c) tope-duro-removido -> ambos casos mueren. | **PASS** |
| AC3 | Tests falsables: los 3 mutantes mueren | Ejecute yo las 4 mutaciones (a,b,c,c'); TODAS matan su caso; pristine PASS. Falsabilidad load-bearing sobre comportamiento real del harness, no solo presencia de texto. | **PASS** |
| AC4 | Sin regresion: tree-kill de arbol completo (0300), RETRY/backoff, entrega gobernada, flujo maker/checker; tope duro evita correr infinito | Banco completo exit 0: incluye `run_complete_tree_kill_case` (root/child/grandchild), `run_unstaged_residue_case` (RETRY/backoff terminal), `run_post_delivery_timeout_case` (0300), y el flujo confirmado/rollback de main(). El hard cap acota el peor caso. | **PASS** |
| AC5 | Alcance: solo las 2 rutas + config byte-identico + gates hub verdes | `git diff --name-only adb1dfa e266d07` = 2 rutas del fix + bookkeeping del TASK; config diff exit 0; validate/encoding/neutralidad exit 0. | **PASS** |
| CRIT | Sintaxis .ps1 valida (un .ps1 roto tumbaria crons vivos al relanzar) | `PSParser::Tokenize` -> 0 errores. | **PASS** |

## Residuos declarados (no bloquean el cierre)
- **R1 (cobertura, no correctitud):** la senal `heartbeat_fresh` de `Get-ExecProgressState` NO esta falsificada por comportamiento. Ambos casos nuevos fijan `ProgressFreshSeconds=0`, de modo que el progreso se prueba via `run_log_growing`/`ledger_growing`, nunca via una ventana heartbeat-fresco sola. Un exec VIVO con heartbeat fresco pero sin salida stdout/stderr ni crecimiento de ledger dependeria unicamente de esa rama, que no tiene test que mate su mutante. Nota: en el incidente originante (0299) el err.log SI crecia (2MB), asi que la rama run-log cubre ese incidente; heartbeat-fresco es senal OR adicional. Gap de test, no defecto.
- **R2 (cobertura partida):** en `run_pre_delivery_and_liveness_cases` el kill "hung" es `reason=hard_cap` sobre un exec que AUN progresa (valida el tope duro), no un exec genuinamente congelado. El kill del exec congelado (`no_progress`) se ejercita aparte en `run_post_delivery_timeout_case` (sleep 30s, `ProgressFreshSeconds=0` -> no_progress -> TREE_KILL), cuya falsabilidad confirme con la mutacion (c'). Ambas ramas quedan cubiertas, en dos funciones.
- **R3 (alcance):** revision HUB-only; sin producto Zeus/Nova (instruccion). El churn de state/ledger en e266d07 es el bookkeeping gobernado del propio TASK; validate exit 0 confirma coherencia.

## Conclusion
Los 2 defectos quedan cerrados de forma correcta y verificable: (A) el post-delivery gatilla SOLO en la entrega
(`in_review` de tarea propia), y (B) el harness revisa liveness antes de terminar y solo mata si esta colgado, con
TOPE DURO para no correr infinito. La falsabilidad es genuina (4 mutantes mueren), sin regresion del tree-kill 0300
ni del RETRY/entrega, sintaxis .ps1 valida, alcance limitado y fondo del hub intocable. Recomiendo **OK-CLOSABLE**.

-- Analista
