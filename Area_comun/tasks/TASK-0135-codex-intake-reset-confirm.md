---
task_id: TASK-0135
title: "Proyecto-front - Intake (RF-14): reset del formulario + confirmacion inequivoca (id+seq) tras EXECUTE exitoso; honestidad de fallo (no reset/no verde si no hubo write real)"
type: product
status: done
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0086
linked_decisions: [DECISION-0051, DECISION-0052]
created_at: 2026-06-20
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
file: Area_comun/tasks/TASK-0135-codex-intake-reset-confirm.md
---

# TASK-0135 - Intake: reset del formulario + confirmacion inequivoca tras EXECUTE (RF-14, AC21)

> maker=Codex / checker=Arquitecto. Codigo en Zeus-protocol. Ratificado por el Operador
> (REQ-DCC3BC1A -> ext3 SPEC-0086, AC21). UX READ-ONLY: sin nueva superficie de escritura (cuelga del
> submit ya gobernado). carry AC11/AC12/AC13 + AC22.

## Origen
REQ-DCC3BC1A (semilla del operador via intake): "Tras un EXECUTE exitoso no se si se envio porque los
campos siguen llenos; si lanzo otro puedo reenviar lo mismo. Quiero que al confirmar OK el formulario se
limpie y quede claro que se envio (id + seq)." El bug de campos-no-limpiados ya ensucia submissions
(mangleo el titulo de REQ-FB27AF72 con texto stale) -> pieza prioritaria.

## Alcance
1. Tras un EXECUTE exitoso del intake (applied true + seq reales): mostrar confirmacion INEQUIVOCA con id
   (REQ-xxxx) + seq del evento, y **resetear** el formulario (campos vacios, paso 1, estado borrador,
   piiAck=false).
2. Si el execute falla o no se confirma: NO reset, NO verde, error real visible, borrador conservado.
3. Conforme al diseno components/intake/ (wizard-4-resultado / estados).

## DoD
- AC21 verde con test de COMPORTAMIENTO permanente (execute OK -> id+seq+reset; execute fallido -> no
  reset/no verde/error real/borrador conservado). Derivado de la respuesta REAL, no string estatico.
- Carry AC11/AC12/AC13 verdes + AC22 (un intake deja el canonico verde).
- node --test/CI verde; npm start ejecutable; la vista Intake resetea tras enviar.
- validate exit 0 con/sin secretos (clon limpio, DECISION-0046); drift 0; #4 epoca 1.14.0 BYTE-IDENTICA;
  neutralidad/encoding limpio.
- Reproducido por el checker (Arquitecto) desde clon limpio; maker!=checker. Commit como Arquitecto +
  Co-Authored-By: Codex.

## Fuera de alcance
- Cualquier cambio de superficie de escritura (UX read-only sobre el execute ya existente).
