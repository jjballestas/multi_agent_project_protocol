---
message_id: MSG-20260621-Arquitecto-to-Operador-RESP-fix-neutralidad-TASK-0138
task_id: TASK-0138
type: DECISION
from: Arquitecto
to: Operador
status: archived
requires_response: false
response_owner: Operador
one_line_summary: "SI, reabro TASK-0138 (sigue in_review) para el fix de NEUTRALIDAD del core. Confirmo el veredicto del Analista: bounding AC25 PASA, pero el core hardcodea Operador/Arquitecto (grep=2) = regresion silenciosa, viola regla 1. Plan: atribucion CALLER-DERIVED (grep=0), regex acotada [A-Za-z0-9._-], scan_domain_neutrality extendido (regresion-proof, EN ALCANCE) + leaks preexistentes como follow-up explicito. Formalizado como AC26 PERMANENTE. Re-GO a Codex; nueva pasada del Analista (grep=0) antes de cerrar."
context_refs:
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/artifacts/ANALISTA-DECISION-0053-mailbox-archive-veredicto-adversarial.md
  - Area_comun/tasks/TASK-0138-codex-mailbox-archive.md
deadline_or_blocking_level: normal
---

# RESP - reabro TASK-0138 para el fix de neutralidad del core (AC26)

Respondo tu pregunta (rr=true): **SI**. TASK-0138 sigue `in_review`; NO la cierro hasta resolver el cambio del
Analista. Verifique el defecto en canonico: `runtime/submit_intent.py` L337-338 hardcodea `author:"Operador"`
y `relayed_by:"Arquitecto"` (grep=2) -- identidades de ESTA instancia en el runtime generico, mientras el resto
del core usa roles. `scan_domain_neutrality` no lo atrapa (solo dominio) -> regresion SILENCIOSA, viola regla 1.
El bounding anti-impersonacion (AC25) y AC24 SIGUEN verdes; esto es solo neutralidad del core.

## Plan (formalizado como AC26 PERMANENTE en SPEC-0086 ext5)
1. **Atribucion CALLER-DERIVED:** el caller (front/Zeus) provee `author`/`relayed_by`; el core sin literales de
   agente (igual que el intake). Falsable: `grep '"Operador"|"Arquitecto"' runtime/submit_intent.py` = 0 (hoy 2).
   Cierra tambien el #5 (archive directo no-via-front no se mis-atribuye).
2. **Regex del `message_id`** acotada a `[A-Za-z0-9._-]` (sin `:` NTFS ADS), manteniendo la guarda de path.
3. **scan_domain_neutrality EXTENDIDO** para atrapar literales de identidad de agente en el core -> regresion-
   proof (EN ALCANCE de esta task; filosofia AC11/AC22).
4. **Follow-up EXPLICITO (aparte):** leaks analogos preexistentes (`apply.py` owner default, `context.py`
   implementer->nombre) -- no en esta task, declarado.

Mantengo verde: AC25 bounding, AC24 idempotente/honesto, hard-gate EXACTAMENTE {requirement-intake,
mailbox-archive}, #4 byte-identica, validate con/sin secretos exit 0, drift 0, un archive deja el canonico verde,
npm test.

**Cierre:** grep=0 + AC26 verde + NUEVA pasada del Analista (neutralidad + bounding intacto). Emito el re-GO a
Codex (maker); yo checker. Canal ASCII.
