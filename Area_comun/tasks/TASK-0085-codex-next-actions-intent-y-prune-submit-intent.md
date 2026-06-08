---
id: TASK-0085
owner: Codex
status: ready
type: implementation
priority: high
created_at: 2026-06-08
updated_at: 2026-06-08
depends_on: [TASK-0084]
relates_to: [TASK-0065, TASK-0038]
phase: P2
spec_id: Area_comun/specs/SPEC-0066-next-actions-intent-y-prune-submit-intent.md
linked_decisions: [DECISION-0022, DECISION-0017, DECISION-0014, DECISION-0026]
objective: Cerrar el GAP congelado al encender enforce=true - agregar un intent propio para next_actions/narrativa en submit_intent y reencauzar el prune para que emita por submit_intent (no por edicion manual de *.json), de modo que se pueda re-habilitar maintenance.enabled en la instancia viva sin romper enforce. Template intacto.
expected_output: (1) nuevo kind de intent (p.ej. project_narrative) en runtime/submit_intent.py que actualiza next_actions (y narrativa) idempotente/determinista, capability orchestrator, required_scopes PROJECT_STATE.json; (2) scripts/prune_state.py --apply deja de editar *.json a mano y emite sus cambios via submit_intent --intents (condensado de next_actions via el intent nuevo; archivado de terminales via intents apropiados); (3) maintenance.enabled re-habilitado SOLO en protocol.config.json vivo tras verificar; (4) golden de replay-identidad (narrativa + prune -> replay==hot, drift 0, idempotente); (5) regresiones verdes + paridad .ps1/CI.
question_to_resolve: ninguna (alcance fijado por SPEC-0066/operador). Si una transicion submit_intent rechaza (capability/scope/from/drift), NO editar a mano -> blocked + error + transaccion intentada.
closure_criterion: intent de narrativa + prune-via-submit_intent VERIFICADOS EN VIVO con drift 0 (no solo golden) + golden de replay-identidad verde + template intacto; el intent nuevo validado aparte como deliverable (golden/uso); maintenance.enabled re-habilitado en la instancia viva solo tras verificacion; todo emitido por submit_intent (enforce ON); handoff autocontenido; release atomico.
sdd_required: true
---

# TASK-0085 - Intent de next_actions/narrativa + prune via submit_intent (cierra el gap de enforce)

> READY (encolada por Claude 2026-06-08 VIA submit_intent --intents bajo enforce=true). Cierra el GAP que
> congelamos al encender enforce: next_actions sin intent + prune que edita *.json a mano. Ver SPEC-0066.
> enforce ON: TODA transicion por submit_intent. authoritative sigue OFF.

## Contexto

Al encender `event_state.enforce=true` (authoritative OFF) congelamos el prune (`maintenance.enabled=false`,
solo instancia viva) porque `prune --apply` reescribe `PROJECT_STATE`/`next_actions` a mano -> hard-fail bajo
enforce. Y `next_actions` no tiene intent en submit_intent, asi que quedo materializado/congelado. Esta tarea
agrega el camino faltante para descongelar el prune sin romper enforce. DECISION-0026 (memoria post-commit) NO
autoriza edicion manual de `state/*.json`: este es el camino correcto.

## Alcance (SPEC-0066)

1. **Intent nuevo de narrativa** (p.ej. `project_narrative`) en `runtime/submit_intent.py`: actualiza
   `next_actions` (y narrativa) idempotente/determinista; capability `orchestrator`; required_scopes
   `Area_comun/state/PROJECT_STATE.json`; materializa con replay==hot (drift 0).
2. **Prune via submit_intent**: `scripts/prune_state.py --apply` emite condensado de next_actions (via el intent
   nuevo, centinela determinista existente) y archivado de terminales por intents apropiados; NO edita `*.json`
   a mano. `--check` sigue read-only.
3. **Re-habilitar** `maintenance.enabled=true` SOLO en `protocol.config.json` vivo, **tras** verificar en vivo.
   **Template intacto** (no cambia el default del master).
4. **Verificacion EN VIVO** (no solo golden): narrativa + un prune real con drift 0 + validador verde bajo
   enforce. **Golden de replay-identidad** (round-trip = identidad, idempotente). Regresiones verdes + .ps1/CI.

## Restricciones (duras)

- **enforce ON**: CERO edicion manual de `Area_comun/state/*.json`. TODO por `submit_intent --intents` /
  `runtime/ledger_ops.py`. Si rechaza -> blocked + error + transaccion, por mailbox; NO toques JSON a mano.
- **Template intacto**: el master `protocol.config.template.json` no cambia su default.
- Neutral, ASCII, sin secretos. Determinista/idempotente. Release/handoff conforme DECISION-0018/0020.
- authoritative/SA.4/Capa C NO se tocan aqui (cada uno en su ventana posterior).

## Ventana de observacion (enforce)

El ciclo de vida de ESTE task (auto-claim + handoff-release por submit_intent, ambos lazos) **cuenta hacia el
>=6 transiciones reales sin hard-fails falsos**. El intent nuevo se valida **aparte como deliverable** (su
golden/uso), no como parte del conteo de la ventana.

## Cierre

Claude ratifica adversarialmente (intent + prune en vivo drift 0 + golden replay-identidad + template intacto) y
cierra por submit_intent. Tras esto, prune descongelado. Siguen en ventanas separadas: authoritative, SA.4, Capa C.
