---
id: TASK-0119
title: Guard de enforcement - rechazar claim acquire con scope de directorio de mailbox (DECISION-0042)
type: security
status: done
owner: Codex
phase: P2
priority: high
spec_id: none
linked_decisions: [DECISION-0042, DECISION-0020]
created_at: 2026-06-19
---

# TASK-0119 - Guard: mailbox claims file-scoped

## Objective

Implementar el guard de enforcement de DECISION-0042: `scripts/validate_collaboration_state.py` y/o
`runtime/submit_intent.py` **RECHAZAN** un `claim acquire` cuyo `scope` contenga una **ruta de directorio
del mailbox** (entrada bajo `Area_comun/mailbox/` que no termine en un `MSG-*.md` concreto). Asi un claim
dir-level sobre el canal -- que bloquea la respuesta del peer (incidente 2026-06-19) -- es **imposible**,
no solo desaconsejado.

## Motivacion (operador: "eso no puede pasar")

Un claim de coordinacion con scope dir-level sobre `Area_comun/mailbox/` bloqueo la respuesta de Codex en
el canal compartido (deadlock auto-infligido). Addendum a DECISION-0020 (anti-colision).

## Alcance

- Guard en validador + submit_intent (rechazo en `acquire`); mensaje de error claro
  ("mailbox claim must be file-scoped: <entry>").
- Golden: claim dir-level de mailbox RECHAZADO; claim file-scoped ACEPTADO.
- Solo el mailbox (canal); NO aplica a `Area_comun/state/*.json` ni otras rutas. Aditivo; no re-valida
  claims ya released. Paridad py/ps si aplica.

## DoD

Guard + golden verdes; aditivo; SemVer MINOR + CHANGELOG; sin romper claims historicos.

## Implementation Notes

- `runtime/submit_intent.py` rechaza `claim acquire` con scope bajo `Area_comun/mailbox/` si la entrada no
  termina en un archivo concreto `MSG-*.md`.
- `scripts/validate_collaboration_state.py` y `.ps1` reportan el mismo guard para claims activos, sin
  re-fallar claims historicos `released`.
- Golden agregado: `examples/mailbox_claim_scope_cases/run_mailbox_claim_scope_cases.py`.

## Verification

- `python examples\mailbox_claim_scope_cases\run_mailbox_claim_scope_cases.py`
- `python -m py_compile runtime\submit_intent.py scripts\validate_collaboration_state.py examples\mailbox_claim_scope_cases\run_mailbox_claim_scope_cases.py`
- `python scripts\validate_collaboration_state.py --root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .`
- `python scripts\scan_encoding.py --root .`
- `python scripts\scan_domain_neutrality.py --root .`
