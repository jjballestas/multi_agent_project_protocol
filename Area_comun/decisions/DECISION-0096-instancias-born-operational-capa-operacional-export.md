---
decision_id: DECISION-0096
title: Instancias born-operational - la capa OPERACIONAL (harness de peers + skills de metodologia) es parte del contrato de instanciacion
status: accepted
ratified_at: 2026-07-14
date: 2026-07-14
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0061, DECISION-0095, DECISION-0057, DECISION-0002, DECISION-0050]
phase: P2
---

# DECISION-0096 - Instancias born-operational (export de la capa operacional)

> ACCEPTED por el operador (GO en chat, 2026-07-14: "dale las armas a NOVA y prepara el
> arsenal de la metodologia para que una proxima instancia no tenga estos problemas").
> NO toca #4: epoch 1.14.0 pineado, config byte-identico, genesis intactos. Todo lo
> shippeado vive FUERA del config pineado.

## Contexto (falla real, vivida dos veces)

Una instancia nueva nacia con el esqueleto de gobierno (ledger, validadores, config,
genesis, CI) pero SIN la capa operacional que corre a los agentes:

1. 2026-07-13: las 4 skills de metodologia (`.claude/skills/`) tuvieron que neutralizarse
   y copiarse A MANO a la instancia NOVA (commit NOVA 5dea820).
2. 2026-07-14: el Arquitecto de la instancia NOVA solicito los harnesses de cron de los
   peers (`codex_mailbox_cron.ps1` / `analista_mailbox_cron.ps1`), inexistentes en su
   instancia; tambien reporto la ausencia de `.protocol-tmp/` (que NO es un gap: es
   estado de runtime que el harness crea en su primera corrida).

Causa raiz: **infraestructura operacional archivada en areas privadas** (`personal/<peer>/`
del hub). `new_instance.py` excluye correctamente el contenido personal (crea las areas del
roster vacias), asi que el harness caia silenciosamente fuera de todo export. Dos
ocurrencias de la misma clase = error de capas, no accidente.

## Decision

1. **La capa operacional es parte del contrato de instanciacion.** Una instancia nace
   OPERATIVA, no solo validable.
2. **Harness generico compartido** en `scripts/harness/` del protocolo:
   `peer_mailbox_cron.ps1` (UN runner parametrizado -PeerId/-CoordinatorId/-AcceptedTypes/
   -PromptFile/-Root/-AgentExe/-AgentArgs que unifica los mirrors por-peer del hub,
   preservando la mecanica endurecida: single-instance por PID+start-time, lock, exec-lease
   con heartbeat, tree-kill con deny-list que jamas mata escrituras de ledger/git/tests,
   self-heal de lock stale, seen.json por firma, STOP_JOB por igualdad exacta, deadline por
   exec, prompt por STDIN) + plantillas de prompt de rol NEUTRALES
   (`prompts/implementer.prompt.md`, `prompts/reviewer.prompt.md`) + `README.md`.
   `new_instance.py` lo shippea a los tiers **runtime y attested** (`copy_peer_harness`).
3. **Masters de las skills de metodologia** en `scripts/instance_assets/claude-skills/`
   (neutralizados: sin rutas/valores del hub, frontera de instancia en el header).
   `new_instance.py` los shippea al scaffold `.claude/skills/` de las instancias
   **attested encapsuladas** (extension de `scaffold_governance_claude`). Esto cierra el
   cableado pendiente de DECISION-0061 para la capa `.claude` de agente-coordinador; el
   registro/loader neutral `skills/` de DECISION-0061 sigue igual y ya se shippeaba.
4. **Tokens de runtime `@@...@@`** en archivos shippeados (p.ej. `@@MESSAGE_PATH@@`):
   `{{...}}` queda RESERVADO al renderer de instanciacion, que falla con placeholders sin
   resolver. El runner valida al arrancar que su plantilla tenga `@@MESSAGE_PATH@@`.
5. **`.protocol-tmp/` NO se shippea.** Es estado local de runtime (locks, leases, seen,
   runs) que el runner crea en la primera corrida; queda documentado en el README para que
   ningun adoptante lo espere pre-existente ni lo cree a mano.
6. **El hub conserva sus copias vivas** en `personal/Codex|Analista/` como layout legacy de
   SU instancia dogfooding (crons apagados hoy; sus rutas estan cableadas en watchdogs y
   comandos del operador). El master shippeado es el runner generico; migrar el hub a
   `scripts/harness/` es opcional y no bloqueante.
7. **Trabajo futuro (no bloqueante):** port POSIX/Python del runner manteniendo el contrato
   de runtime-state (mismas rutas `.protocol-tmp/<peer>_mailbox_cron/`) para que los
   watchdogs sigan compatibles; migracion opcional del hub al runner generico.

## Verificacion (evidencia, 2026-07-14)

- `scripts/test_attested_instancing.py` extendido con `assert_operational_layer` (runner +
  README + prompts con token intacto y sin `{{` + paridad masters<->instancia de skills):
  **exit 0**.
- `examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py`: **5 casos +
  ps1 parity, exit 0** (el tier runtime tambien recibe el harness sin romper nada).
- **Smoke real del runner** sobre la instancia scratch generada: deteccion del mensaje,
  render del prompt con tokens sustituidos (0 residuales), exec con prompt por STDIN,
  seen.json firmado, stop-marker -> salida graceful, `EXEC_EXIT code=0` (fix `$process.Handle`
  para execs sub-segundo). Estructura `.protocol-tmp/` nace correcta en primera corrida.
- Gates del hub: validate + scan_encoding + scan_domain_neutrality **exit 0** (el scan de
  neutralidad cazo y forzo a eliminar nombres de agente hardcodeados del test: la asercion
  es ahora paridad dinamica, sin nombres).
- Revision adversarial informal del runner (subagent checker, mandato de refutar) previa al
  commit; hallazgos incorporados o descartados con razon documentada en el mensaje de commit.

## Entrega inmediata a NOVA (las "armas")

El mismo runner + prompts + README se entrega a la instancia NOVA en
`Aegis/scripts/harness/` (push directo a NOVA.git, patron de la entrega de skills 5dea820;
NO toca su ledger -- frontera dos-trios DECISION-0095). La decision de montar un Analista
PERMANENTE en NOVA (custodia, override analista-only, escritor-unico, watchdogs) sigue
siendo una DECISION de SU trio con SU operador.
