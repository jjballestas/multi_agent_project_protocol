# HANDOFF TASK-0138 - Codex to Arquitecto

- task_id: TASK-0138
- from: Codex
- to: Arquitecto
- status: ready_for_review
- created_at: 2026-06-20T22:55:00Z

## Resultado

AC24/AC25 entregados:
- Core `runtime/submit_intent.py` acepta el intent aditivo `mailbox_archive` con payload estricto `{ message_id }`.
- El core valida id seguro `MSG-*`, bloquea path traversal, exige existencia en `open/` o idempotencia ya archivada, exige claim file-scoped, emite accountability `author=Operador`, `relayed_by=Arquitecto`, `endorsement=none`, y mueve `open -> archived` actualizando `status: archived`.
- Golden cases nuevos cubren happy path real, idempotencia, id inexistente, path traversal, payload extra/otro intent y falta de claim.
- Zeus-protocol expone `mailbox-archive` como segunda accion RF-14 ejecutable, con builder server-side `claim -> mailbox_archive -> release`, rechazo de `actorId`/`intents`, y hard gate exacto `{requirement-intake, mailbox-archive}`.
- La vista Mailbox agrega boton `archivar` por mensaje open; solo mueve a archived en UI si la respuesta real trae `applied=true`, `messageId` y `seq`; error deja el mensaje en open.

## Archivos

- `runtime/submit_intent.py`
- `examples/mailbox_archive_cases/run_mailbox_archive_cases.py`
- `D:/Agentes/Zeus/Zeus-protocol/public/app.js`
- `D:/Agentes/Zeus/Zeus-protocol/public/index.html`
- `D:/Agentes/Zeus/Zeus-protocol/public/styles.css`
- `D:/Agentes/Zeus/Zeus-protocol/src/server.js`
- `D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js`

## Commits

- Producto: `6afefe7 feat(mailbox): add governed archive relay`

## Evidencia

- `python examples/mailbox_archive_cases/run_mailbox_archive_cases.py`: PASS 3/3.
- `python -m py_compile runtime/submit_intent.py examples/mailbox_archive_cases/run_mailbox_archive_cases.py`: OK.
- Zeus `npm test`: PASS 26/26.
- Zeus `node --check public/app.js`, `src/server.js`, `tests/staticContract.test.js`: OK.
- Protocolo: `validate_collaboration_state.py --root .` OK con warnings solo de mensajes abiertos a Operador sin respuesta requerida.
- Protocolo: `validate_collaboration_state.ps1` OK con los mismos warnings.
- Protocolo sin secretos: copia temporal sin `secrets/` OK.
- `scan_encoding.py --root .`: OK.
- `scan_domain_neutrality.py --root .`: OK.
- Drift antes del cierre: `has_drift=false`, `up_to_seq=881`.
- #4 byte-identica: `protocol.config.json` y `chain_manifest.json` sin diff; eventauth key de Arquitecto preservada en test write-real.

## Pendiente de checker

Reproducir desde clon limpio, verificar AC24/AC25/AC11/AC13/AC17/AC19/AC20 y coordinar la pasada de Analista de bounding + neutralidad antes de cerrar `TASK-0138` a `done`.
