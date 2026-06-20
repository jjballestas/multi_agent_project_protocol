---
task_id: TASK-0136
title: "Remediacion (DECISION-0018): el intake dejo el canonico ROJO (validate exit 1) -> validador acepta ids REQ-, builder escribe seed + scopes validos + test regresion-proof, reconciliar los 4 seeds"
type: product
status: done
owner: Codex
phase: P2
priority: critical
spec_id: SPEC-0086
linked_decisions: [DECISION-0018, DECISION-0051, DECISION-0052]
created_at: 2026-06-20
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
file: Area_comun/tasks/TASK-0136-codex-reconcile-intake-canonical-red.md
---

# TASK-0136 - Remediacion: el intake dejo el canonico ROJO (validate exit 1)

> maker=Codex / checker=Arquitecto. Anomalia DECISION-0018: el intake ya mergeado (TASK-0133/0134) produjo
> estado que rompe `validate_collaboration_state` (exit 1, 12 errores). PRIORIDAD: bloquea promover los 4
> SPECs de requisitos. Implementa Codex (GO del operador "implementa codex"); Arquitecto provee la spec del
> regex y es checker.

## Causa (canonico 5c918d2/31078be)
- **B1 (4 err):** cada `task_upsert` requirement fija `file: Area_comun/tasks/req-<hex>-requirement-seed.md`
  pero el builder NUNCA lo escribe -> "references missing task file".
- **B2 (8 err):** el validador solo reconoce ids `TASK-\d{4}`; el intake crea ids `REQ-<hash>`
  (DECISION-0051/0052) -> los claim scopes del relay (`#REQ-...`, ya released) salen "invalid row selector".

## Alcance
1. **Validador del protocolo (core neutral) - spec EXACTA del Arquitecto:**
   en `scripts/validate_collaboration_state.py`:
   - L75: `TASK_ROW_SELECTOR_PATTERN = re.compile(r"^(TASK-\d{4}|REQ-[0-9A-Fa-f]+)$")`
   - L76: `PROJECT_STATE_SELECTOR_PATTERN = re.compile(r"^(active_tasks/(TASK-\d{4}|REQ-[0-9A-Fa-f]+)|[A-Za-z_][A-Za-z0-9_]*)$")`
   - Reflejar el mismo cambio en el validador PowerShell paralelo (`scripts/validate_collaboration_state.ps1`)
     si tiene patrones equivalentes, para no divergir.
   - NEUTRAL: sin terminos de dominio; solo amplia el esquema de id ya ratificado.
2. **Intake builder (Zeus-protocol):** que cada intake EXECUTE deje el canonico VERDE:
   - escribir el seed file en el `file:` referenciado (frontmatter consistente con el index + narrativa +
     intencion de aceptacion);
   - construir los claim scopes del relay con selectores que el validador acepte;
   - **TEST PERMANENTE (AC22):** tras un intake EXECUTE real, correr el validador y asertar exit 0
     (regresion-proof). Conserva la disciplina anti-impersonacion (AC19) intacta.
3. **Reconciliar los 4 requisitos existentes:** crear los 4 seed files (REQ-DCC3BC1A, REQ-FB27AF72,
   REQ-B65E7802, REQ-444E0DE5) con su contenido recuperado del ledger (events.jsonl, task_upsert.task:
   title/narrative/acceptance_intent/project/author/relayed_by/endorsement).

## DoD / cierre (AC22)
- `validate_collaboration_state` exit 0 CON y SIN secretos (clon limpio, DECISION-0046); drift 0; #4 epoca
  1.14.0 byte-identica; `scan_encoding`/`scan_domain_neutrality` exit 0 (neutralidad del cambio del validador).
- Test permanente "un intake deja el canonico verde" verde; node --test/CI verde.
- AC19 anti-impersonacion sigue verde (no regresion).
- Reproducido por el checker (Arquitecto) desde clon limpio; maker!=checker. Commit como Arquitecto +
  Co-Authored-By: Codex.

## Fuera de alcance
- Los 4 SPECs de requisitos (se retoman tras cerrar 0136 con canonico verde).
