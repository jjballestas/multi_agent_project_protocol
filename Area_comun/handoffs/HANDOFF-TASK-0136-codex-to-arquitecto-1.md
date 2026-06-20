# HANDOFF TASK-0136 - Codex to Arquitecto

- task_id: TASK-0136
- from: Codex
- to: Arquitecto
- status: ready_for_review
- created_at: 2026-06-20T20:22:00Z

## Resultado

Remediacion entregada para el canonico rojo del intake:
- `scripts/validate_collaboration_state.py` y `.ps1` aceptan selectores `REQ-[0-9A-Fa-f]+` en `TASK_INDEX` y `PROJECT_STATE.active_tasks`.
- Se reconciliaron los 4 seed files existentes: `REQ-DCC3BC1A`, `REQ-FB27AF72`, `REQ-B65E7802`, `REQ-444E0DE5`.
- `Zeus-protocol/src/server.js` ahora incluye el seed file en el claim scope del relay y escribe el markdown del requirement seed en el `file:` declarado.
- `Zeus-protocol/tests/staticContract.test.js` agrega AC22 permanente: execute real del intake + seed file escrito + `validate_collaboration_state.py` exit 0 en el fixture de protocolo.

## Evidencia

- Protocolo: `validate_collaboration_state.py --root .` OK; `.ps1 -Root .` OK.
- Protocolo sin secretos: copia temporal sin `secrets/` OK.
- `scan_encoding.py --root .` OK.
- `scan_domain_neutrality.py --root .` OK.
- Drift antes del cierre: `has_drift=false`, `up_to_seq=850`.
- #4: `protocol.config.json` y `chain_manifest.json` sin diff; `eventauth-arquitecto.key` sin cambio de estado Git.
- Zeus-protocol: `node --check src/server.js` OK; `node --check tests/staticContract.test.js` OK.
- Zeus-protocol: `npm test` PASS 22/22.
- Diff check: protocolo OK; Zeus-protocol OK.

## Pendiente de checker

Reproducir desde clon limpio, verificar AC22 y cerrar `TASK-0136` a `done` si procede. Commit esperado por Arquitecto con `Co-Authored-By: Codex`.
