---
message_id: MSG-20260621-Arquitecto-to-Operador-CHECKER-VERDE-TASK-0138-neutralidad
task_id: TASK-0138
type: FYI
from: Arquitecto
to: Operador
status: archived
requires_response: false
response_owner: Operador
one_line_summary: "CHECKER VERDE del fix de neutralidad (AC26) de TASK-0138. grep '\"Operador\"|\"Arquitecto\"' runtime/submit_intent.py = 0; atribucion caller-derived; regex message_id acotada; scan_domain_neutrality ATRAPA el literal (golden identity_literal_in_core, regresion-proof); AC24/AC25 bounding intactos; #4 byte-identica; validate con/sin secretos exit 0; drift 0; Zeus npm test 26/26. NO cierro: falta la NUEVA pasada del Analista (tu la activas) confirmando neutralidad + bounding; tras su OK, cierro a done."
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0138-codex-to-arquitecto-2.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - runtime/submit_intent.py
  - scripts/scan_domain_neutrality.py
deadline_or_blocking_level: normal
---

# CHECKER VERDE - fix de neutralidad de TASK-0138 (AC26)

Reproduje la entrega de Codex (commit 39a2f9b en este repo; Zeus 7619fd2). Todas las condiciones de cierre del
operador CUMPLIDAS salvo la pasada final del Analista:

## Verificacion (checker, maker!=checker)
- **Gate falsable grep=0:** `grep '"Operador"|"Arquitecto"' runtime/submit_intent.py` -> 0 matches (antes 2).
- **Atribucion CALLER-DERIVED:** `mailbox_archive_accountability` exige `author`/`relayed_by` del payload (los
  provee el server Zeus, validados server-side); el core sin literales de agente. `endorsement` default "none"
  (constante neutral). Cierra tambien el #5 (archive directo no-via-front no se mis-atribuye).
- **Regex `message_id`** acotada a `^MSG-[A-Za-z0-9._-]+$` (sin `:` NTFS ADS), guarda de path intacta.
- **scan_domain_neutrality REGRESION-PROOF:** rc=1 (FALLA) sobre el fixture `identity_literal_in_core` =
  atrapa el literal; rc=0 sobre `clean`. Golden permanente.
- **AC25 bounding INTACTO** + **AC24 idempotente/honesto:** mailbox_archive golden 3/3; hard-gate EXACTAMENTE
  {requirement-intake, mailbox-archive}; Zeus npm test 26/26 (incl. "mailbox archive cannot reopen raw
  execution" + "UI moves messages only after real governed execute" + no-bypass).
- **#4 epoca 1.14.0 BYTE-IDENTICA:** `git diff ecc0dad..HEAD` de config/manifest/keys = vacio.
- **Gates:** validate exit 0 CON secretos Y clon-limpio SIN secretos (DECISION-0046); drift 0; encoding/neutrality 0.

## Follow-up declarado (NO en esta task, como pediste)
Leaks analogos preexistentes en legacy: `runtime/apply.py`, `budget.py`, `context.py`, `eventlog.py`,
`ledger_ops.py`, `metrics.py`, `router.py`, `scripts/prune_state.py`. El scanner los exime explicitamente (no
fueron tocados); quedan para follow-up.

## Siguiente (tu accion)
**Activa al Analista** para la pasada final (neutralidad grep=0 + bounding intacto, anclado en canonico). Con su
OK, cierro TASK-0138 a `done` (in_review->done, reviewer). Empujo la entrega para que el Analista ancle en el
commit pushed. Canal ASCII.
