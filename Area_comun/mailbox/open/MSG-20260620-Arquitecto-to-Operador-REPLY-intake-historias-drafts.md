---
message_id: MSG-20260620-Arquitecto-to-Operador-REPLY-intake-historias-drafts
task_id: none
type: DECISION
from: Arquitecto
to: Operador
status: open
requires_response: false
response_owner: Operador
in_reply_to: MSG-20260620-Operador-to-Arquitecto-GO-front-intake-historias
one_line_summary: "Confirmo el modelo (intake -> yo autoro la SPEC). Por metodo: SI exige DECISION (nueva superficie EXECUTE del operador desde el front) pero NO nuevo intent kind (el intake = task_upsert requirement). SPEC = EXTENSION de SPEC-0086 (RF-11 + AC14-AC17), no SPEC nueva. 3 drafts listos para ratificacion."
context_refs:
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0051-operator-execute-write-surface-front.md
  - personal/Arquitecto/carril_A/DRAFT-SPEC-0086-ext-intake-historias.md
  - personal/Arquitecto/carril_A/DRAFT-TASK-0133-front-intake-historias.md
deadline_or_blocking_level: normal
---

# REPLY - intake gobernado de historias (drafts para ratificacion)

Confirmado el modelo: **intake = SEMILLA; el Arquitecto autora la SPEC.** Roles intactos (operador =
que + GO; yo = autor de la SPEC bajo SDD, maker=Codex/checker=yo). Resuelvo las dos preguntas de
metodo que pediste:

## 1. Nuevo intent kind? -> NO
El intake se modela como `task_upsert` de una tarea `type:requirement` (status proposed,
author=Operador), idempotente. Reusa kind/capability/required_scopes existentes; NO toca
INTENT_TYPES del runtime -> superficie minima, **#4 epoca 1.14.0 PINNED intacta, sin re-genesis**.

## 2. Nueva superficie de escritura del operador? -> SI (nucleo de la DECISION)
Hoy el front es read-only + dry_run; nunca escribio el ledger. Habilitar EXECUTE del front (acotado
al intake, `actorId:"Operador"`, con confirmacion visible) ES una nueva superficie de escritura ->
por CLAUDE.md regla 2 exige **DECISION primero**. El front sigue sin escribir directo
(directLedgerWrites:false; toda escritura via submit_intent; sin confirm -> 409 = prueba negativa).

## SPEC: EXTENSION de SPEC-0086 (no SPEC nueva)
El intake es superficie de OPERAR del mismo MVP single-operator (vecina de RF-10). Agrego **RF-11**
+ **AC14** (intake->artefacto gobernado, atribuido Operador, idempotente), **AC15** (EXECUTE exige
confirmacion; prueba negativa), **AC16** (redaccion PII del texto libre, canal ASCII, coherente con
DECISION-0040), **AC17** (no-bypass). Carry permanente AC11/AC12/AC13.

## PII (innegociable)
Texto libre redactado en todo plano publicable; TASK-0118/DEF-PII SIGUE como gate antes de captura
viva de PII real -- el intake opera con redaccion best-effort + confirmacion, NO levanta ese gate.

## Drafts (en personal/Arquitecto/carril_A/, sin promover)
- DRAFT-DECISION-0051 (superficie EXECUTE del operador; intake=task_upsert requirement)
- DRAFT-SPEC-0086-ext (RF-11 + AC14-AC17)
- DRAFT-TASK-0133 (front intake, ready/Codex; codigo en Zeus-protocol)

Espero tu ratificacion para promover (DECISION-0051 -> extension SPEC-0086 -> GO TASK-0133 a Codex).
Etapa 5 roster sigue DEFERIDA. Drift 0, canonico limpio.
