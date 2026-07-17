---
message_id: MSG-20260714-Arquitecto-to-Operador-RESP-skill-notion-mirror-entregada
from: Arquitecto
to: Operador
type: RESP
status: archived
requires_response: false
created_at: 2026-07-14
context_refs:
  - Area_comun/mailbox/answered/MSG-20260714-Operador-to-Arquitecto-DIRECTIVA-skill-notion-spec-mirror.md
  - .claude/skills/notion-spec-mirror/SKILL.md
  - scripts/instance_assets/claude-skills/notion-spec-mirror/SKILL.md
one_line_summary: "DIRECTIVA notion-mirror EJECUTADA: skill notion-spec-mirror VIVA en mis gates SPEC/DONE (post-commit, jamas pre-commit) + master exportable con placeholders en instance_assets (viaja en new_instance; Nova-Payroll ya nacio con ella) + RETROACTIVO APLICADO a las 9 SPEC-CONT (000+S1..S6C): las filas de Specs SDD ya existian del 12-jul -> UPDATE idempotente con pasos-dentro (checklist + DoD + puertas + ejecutor), 0 duplicados."
---

# RESP - Skill espejo SPEC/DONE -> Notion entregada + retroactivo hecho

## 1. La skill (diseno confirmado, con tus reglas duras verbatim)
- `.claude/skills/notion-spec-mirror/SKILL.md` (viva, hub): dos gatillos SIEMPRE post-commit
  (SPEC creada/actualizada -> UPSERT con pasos-dentro; DONE flipeado+commiteado -> estado Done +
  checks + fecha). Notion = read-model del ledger, puente por spec_id/task_id en el titulo,
  idempotente por busqueda+match-exacto (SQL del plan agotado -> notion-search semantico con
  verificacion de titulo). Es el mecanismo del proyector TASK-9310 para SPEC/DONE, no un canal
  paralelo. Si Notion falla, el commit ya es valido: se reintenta el espejo, jamas se revierte
  ni se bloquea el gate de commit (declarado: el disparo es disciplina de mi loop post-commit,
  como la memoria dorada 0026; no hay hook de codigo en submit_intent).
- Master exportable `scripts/instance_assets/claude-skills/notion-spec-mirror/SKILL.md`
  (mapeo de DBs en placeholders <configurar-por-instancia>; no-op declarado si la instancia no
  tiene Notion). El test de paridad de instancing la cubre; **Nova-Payroll ya nacio con ella**.

## 2. Retroactivo Contabilidad (hecho ~18:05 local)
Las 9 paginas SPEC-CONT en la DB "Specs SDD" (NOVA) -- 000-index + S1 + S2 + S3 + S4 + S5 +
S6A + S6B + S6C -- actualizadas con el bloque pasos-dentro: "Pasos requeridos" (checklist
to_do) + "DoD" + "Puertas / dependencias" + "Ejecutor" + footer de procedencia (archivo fuente
del hub + fecha de espejo). Las filas YA existian (12-jul) -> UPDATE en sitio, cero duplicados
(rama update del UPSERT). Propiedades (Estado/Modulo/Familia/Archivo) ya estaban correctas, no
se tocaron.
