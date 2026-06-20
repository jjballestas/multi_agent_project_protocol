# HANDOFF TASK-0138 AC26 - Codex to Arquitecto

- task_id: TASK-0138
- from: Codex
- to: Arquitecto
- status: ready_for_review
- created_at: 2026-06-21T01:10:00Z

## Resultado

AC26 entregado:
- `runtime/submit_intent.py` ya no hardcodea identidades de instancia para `mailbox_archive`; `author` y `relayed_by` son obligatorios y caller-derived, con `endorsement` opcional/default `none`.
- `MAILBOX_MESSAGE_ID_RE` queda acotada a `MSG-[A-Za-z0-9._-]+`, manteniendo bloqueo de `/`, `\`, `..` y escape por `resolve`.
- `scan_domain_neutrality` Python/PowerShell ahora deriva literales de identidad desde `agent_registry`/`agent_roles` y los escanea en codigo core; el caso `identity_literal_in_core` queda como regresion permanente.
- Zeus-protocol commit `7619fd2` provee `author`/`relayed_by`/`endorsement` desde el builder server-side de `mailbox-archive`, sin confiar en payload cliente, y rechaza `:` en `messageId`.

## Legacy Declarado

El scanner evita fallar por leaks historicos fuera de este fix en archivos legacy ya existentes:
`runtime/apply.py`, `runtime/budget.py`, `runtime/context.py`, `runtime/eventlog.py`, `runtime/ledger_ops.py`,
`runtime/metrics.py`, `runtime/router.py` y `scripts/prune_state.py`. No fueron tocados; quedan para follow-up
explicito como pidio el RE-GO.

## Archivos

- `runtime/submit_intent.py`
- `scripts/scan_domain_neutrality.py`
- `scripts/scan_domain_neutrality.ps1`
- `examples/mailbox_archive_cases/run_mailbox_archive_cases.py`
- `examples/neutrality_scan_cases/run_neutrality_scan_cases.ps1`
- `examples/neutrality_scan_cases/identity_literal_in_core/protocol.config.json`
- `examples/neutrality_scan_cases/identity_literal_in_core/runtime/source.py`
- `D:/Agentes/Zeus/Zeus-protocol/src/server.js`
- `D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js`

## Commits

- Producto: `7619fd2 fix(mailbox): derive archive attribution in server builder`

## Evidencia

- `rg -n '"Operador"|"Arquitecto"' runtime/submit_intent.py`: sin matches.
- `python examples/mailbox_archive_cases/run_mailbox_archive_cases.py`: PASS 3/3.
- `powershell -NoProfile -ExecutionPolicy Bypass -File examples/neutrality_scan_cases/run_neutrality_scan_cases.ps1`: PASS.
- `python -m py_compile runtime/submit_intent.py scripts/scan_domain_neutrality.py examples/mailbox_archive_cases/run_mailbox_archive_cases.py`: OK.
- Zeus `npm test`: PASS 26/26.
- Zeus `node --check src/server.js`, `tests/staticContract.test.js`: OK.
- Protocolo: `validate_collaboration_state.py --root .`: OK.
- Protocolo: `validate_collaboration_state.ps1`: OK.
- Protocolo sin secretos: copia temporal sin `secrets/` OK.
- `scan_encoding.py --root .`: OK.
- `scan_domain_neutrality.py --root .`: OK.
- Drift antes del cierre: `has_drift=false`, `up_to_seq=887`.
- #4 byte-identica: `protocol.config.json`, `chain_manifest.json` y eventauth keys sin diff.

## Pendiente de checker

Reproducir desde clon limpio, pedir nueva pasada de Analista para neutralidad + bounding, y cerrar `TASK-0138`
a `done` si procede.
