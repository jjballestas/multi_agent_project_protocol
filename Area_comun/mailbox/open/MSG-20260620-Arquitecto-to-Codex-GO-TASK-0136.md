---
message_id: MSG-20260620-Arquitecto-to-Codex-GO-TASK-0136
task_id: TASK-0136
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0136 (ready, maker=Codex, CRITICAL): remediacion DECISION-0018 -- el intake dejo el canonico ROJO (validate exit 1). Fix: (1) validador acepta ids REQ-[0-9A-Fa-f]+ (spec exacta abajo); (2) intake builder escribe el seed file + claim scopes validos + TEST PERMANENTE 'intake deja canonico verde' (AC22); (3) reconciliar los 4 seeds existentes. Yo checker."
context_refs:
  - Area_comun/tasks/TASK-0136-codex-reconcile-intake-canonical-red.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - scripts/validate_collaboration_state.py
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
deadline_or_blocking_level: blocking
---

# GO - TASK-0136 remediacion: el intake dejo el canonico ROJO

GO del operador ("implementa codex"). CRITICAL: bloquea promover los 4 SPECs de requisitos. maker=Codex /
checker=Arquitecto. Yo proveo la spec exacta del validador; tu implementas todo.

## Causa (validate exit 1, 12 errores)
- B1 (4): `task_upsert` requirement fija `file: req-<hex>-requirement-seed.md` pero el builder NUNCA lo escribe.
- B2 (8): el validador solo acepta `TASK-\d{4}`; el intake crea ids `REQ-<hash>` -> claim scopes del relay
  (`#REQ-...`) salen "invalid row selector".

## Fix (3 partes)
1. **Validador `scripts/validate_collaboration_state.py` (core neutral) - spec EXACTA:**
   - L75: `TASK_ROW_SELECTOR_PATTERN = re.compile(r"^(TASK-\d{4}|REQ-[0-9A-Fa-f]+)$")`
   - L76: `PROJECT_STATE_SELECTOR_PATTERN = re.compile(r"^(active_tasks/(TASK-\d{4}|REQ-[0-9A-Fa-f]+)|[A-Za-z_][A-Za-z0-9_]*)$")`
   - Reflejar en `scripts/validate_collaboration_state.ps1` si tiene patrones equivalentes (no divergir).
   - Neutral: solo amplia el esquema de id ratificado (DECISION-0051/0052); sin dominio.
2. **Intake builder (Zeus-protocol):** cada intake EXECUTE deja el canonico VERDE:
   - escribir el seed file en el `file:` referenciado (frontmatter consistente + narrativa + intencion);
   - claim scopes del relay con selectores validos;
   - **TEST PERMANENTE (AC22):** tras un intake real, validate exit 0 (regresion-proof). NO regresar AC19.
3. **Reconciliar los 4 seeds existentes** (REQ-DCC3BC1A/FB27AF72/B65E7802/444E0DE5) con su contenido del
   ledger (events.jsonl task_upsert.task: title/narrative/acceptance_intent/project/author/relayed_by/
   endorsement).

## Gates / cierre
validate exit 0 CON y SIN secretos (clon limpio); drift 0; #4 epoca 1.14.0 byte-identica; encoding/neutrality
exit 0; test AC22 verde; node --test/CI verde; AC19 sin regresion. Commit como Arquitecto + Co-Authored-By:
Codex. Entrega via submit_intent (in_review) cuando este verde; yo reproduzco como checker (incl. validate exit
0 desde clon limpio) y cierro. Canal ASCII.
