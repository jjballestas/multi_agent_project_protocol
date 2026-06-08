---
id: TASK-0083
owner: Codex
status: done
type: integration
priority: normal
created_at: 2026-06-08
updated_at: 2026-06-08
depends_on: []
relates_to: [TASK-0038]
phase: P2
spec_id: Area_comun/specs/SPEC-0065-team-bridge-capas-AB.md
linked_decisions: [DECISION-0025, DECISION-0022, DECISION-0018, DECISION-0017]
objective: Implementar el bridge Agent Teams -> protocolo en Capas A+B (gate enforcement + audit append-only), off-by-default y neutral, reusando los gates y mecanismos existentes. NO Capa C (mapeo autoritativo: diferida a precondiciones DECISION-0022). NO encender nada en la instancia viva.
expected_output: runtime/team_bridge.py (Capas A+B) que lee el payload del hook por stdin y, segun runtime.team_bridge.layers, corre los gates existentes (validador + neutralidad [+ turn_validate]) con exit 2 si fallan (Capa A) y/o anexa cada evento a Area_comun/state/team_audit.jsonl sin mutar estado (Capa B); bloque runtime.team_bridge {enabled:false,layers:[],activation_decision,approved_by,approved_at} en protocol.config.template.json (master) y protocol.config.json (instancia viva), off-by-default; alta de runtime/team_bridge.py en scan_globs de neutralidad; golden examples/team_bridge_cases/ deterministas; regresiones verdes.
question_to_resolve: ninguna (alcance A+B fijado por SPEC-0065/DECISION-0025). Si surge ambiguedad de scope o un gap => blocked + una pregunta concreta.
closure_criterion: team_bridge.py Capas A+B + bloque off-by-default en template e instancia + alta en scan_globs + golden team_bridge_cases verdes (off-byte-equivalente, audit-only, gate-pass, gate-fail->exit2, A+B, evento con [TASK-XXXX] solo audita) + validador/neutralidad/regresiones verdes; Capa C ausente (diferida); off => byte-equivalente; handoff autocontenido; release atomico (DECISION-0018/0020).
sdd_required: true
---

# TASK-0083 - Bridge Agent Teams <-> protocolo, Capas A+B

> READY (encolada por Claude 2026-06-08). Implementa DECISION-0025 (ACCEPTED, alcance A+B) segun
> SPEC-0065. Off-by-default, aditivo, neutral. **Capa C (mapeo autoritativo via submit_intent) NO se
> implementa aqui**: diferida a precondiciones DECISION-0022. Esta tarea NO enciende el bridge en la
> instancia viva (el bloque se entrega `enabled:false, layers:[]`).

## Contexto

Anthropic distribuye Agent Teams (motor de ejecucion en vivo con hooks `TaskCreated`/`TaskCompleted`/
`TeammateIdle`). DECISION-0025 lo posiciona como motor en vivo y a este protocolo como ledger durable
encima; el puente reusa los gates y mecanismos existentes. El operador aprobo **Capas A+B** en sombra
(aditivo, off-by-default, drift benigno). Ver SPEC-0065 para el diseno completo.

## Alcance (Capas A+B)

1. **C1 - Registro/config:** bloque `runtime.team_bridge {enabled:false, layers:[], activation_decision:"",
   approved_by:"", approved_at:""}` en `protocol.config.template.json` (master) y `protocol.config.json`
   (instancia viva), off-by-default. `team_bridge_activation_error(config)` analoga a las existentes.
2. **C2 - Entrypoint:** `runtime/team_bridge.py --event <TaskCreated|TaskCompleted|TeammateIdle>`,
   payload por **stdin** (JSON). Sin registro valido o `enabled:false` => no-op de estado, sale 0.
3. **Capa A - gate enforcement:** si `"gate"` en `layers`, en `TaskCompleted`/`TeammateIdle` corre los
   gates existentes (`validate_collaboration_state.py` + `scan_domain_neutrality.py` [+ `turn_validate.py`
   si aplica]); si alguno falla, detalle a **stderr** y **exit 2** (Agent Teams bloquea/mantiene al
   teammate). Si pasan, exit 0.
4. **Capa B - audit append-only:** si `"audit"` en `layers`, anexa una linea JSON
   `{observed_at, hook, ...payload}` a `Area_comun/state/team_audit.jsonl` (ensure_ascii=True), sin mutar
   `state/*.json`. Crea archivo/dir si falta.
5. **Fail-closed:** error en Capa B no revienta el team (se captura; nunca propaga excepcion no
   controlada). Capa A es el unico retorno 2 intencional.
6. **Neutralidad:** alta de `runtime/team_bridge.py` en `scan_globs` del scan de neutralidad.

## No-alcance (explicito)

- **Capa C** (mapeo `[TASK-XXXX]` + claim -> `submit_intent`): NO implementar. En A+B, un evento con
  `[TASK-XXXX]` solo se audita (Capa B). Diferida a precondiciones DECISION-0022.
- **No encender** el bridge en la instancia viva: el bloque va `enabled:false, layers:[]`.
- **No tocar** `.claude/settings.json` vivo (los hooks se cablean al activar, paso separado).

## Tests (deterministas)

Golden `examples/team_bridge_cases/` con payloads grabados: (1) off-sin-flag => no-op byte-equivalente;
(2) audit-only; (3) gate-pass => exit 0; (4) gate-fail => exit 2 + stderr (fixture aislado, no el repo
vivo); (5) A+B; (6) evento con `[TASK-XXXX]` => solo audita. Regresiones validador/neutralidad/runtime
verdes. Reloj/IDs deterministas via fixture.

## Restricciones

- Neutral de dominio; **ASCII**; **sin secretos**; off => byte-equivalente.
- Handoff autocontenido; release atomico (DECISION-0018); staging por paths explicitos (DECISION-0020);
  no listar artefactos en el claim antes de crearlos (#1).

## Cierre

Tras done: Claude ratifica adversarialmente. La activacion A+B en la instancia viva es un paso separado
registrado en `runtime.team_bridge` (operador). Capa C queda diferida.

## Entrega Codex

- Implementado `runtime/team_bridge.py`.
- Agregado `runtime.team_bridge` apagado en `protocol.config.json` y `protocol.config.template.json`.
- Agregado `runtime/team_bridge.py` explicitamente a `domain_neutrality.scan_globs`.
- Agregado `examples/team_bridge_cases/run_team_bridge_cases.py` con 7 golden cases.
- Agregado el harness a `.github/workflows/validate.yml`.
- No se implemento Capa C, no se activo el bridge y no se toco `.claude/settings.json`.
