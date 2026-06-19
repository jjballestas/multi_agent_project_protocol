---
spec_id: SPEC-0084
task_id: TASK-0122
type: security
status: accepted
linked_decisions:
  - DECISION-0046
  - DECISION-0045
  - DECISION-0043
created_at: 2026-06-19
updated_at: 2026-06-19
author: Arquitecto
---

# SPEC-0084 - Replay secret-independiente (verificacion-no-disponible != verificacion-fallo)

## Context

DECISION-0046: con #4 ON, `replay_events` trata `unresolved_key`/`missing_key` (secreto ausente = entorno)
igual que `invalid_signature` (tamper) -> rejection state-afectante + skip -> el estado materializado depende
de los secretos -> `assert_snapshot_matches` no puede pasar a la vez en la instancia viva (con secretos) y en
un clon limpio (sin secretos). Esta SPEC fija el fix verificable. maker=Arquitecto, checker=Codex.

## Scope

- `runtime/eventlog.py:replay_events` (~428-440): clasificar el resultado de `verify_event_auth`.
- Constante/helper para la particion de razones (UNVERIFIABLE vs TAMPER).
- Goldens que prueban secret-independencia + deteccion de tamper intacta.
- Reconciliar el snapshot del head a su forma secret-independiente.

## Out Of Scope

- Flags de #4, boundary T0/sello (DECISION-0045), formato de firma / cargador (DECISION-0043).

## Diseno

`verify_event_auth` ya devuelve `reason` en {`event_auth_disabled`, `missing_signature`, `unresolved_key`,
`missing_key`, `invalid_signature`, `valid`}. Particion:

- **UNVERIFIABLE_HERE** = {`unresolved_key`, `missing_key`}: verificacion NO disponible en este entorno
  (no hay secreto). El evento se APLICA normalmente (no skip, no rejection state-afectante). Opcional:
  acumulador NO-canonico `unverified_here` (no entra en `canonical_hash(state)`) para reporte.
- **TAMPER** = {`missing_signature`, `invalid_signature`}: rechazo real `security.unauthenticated_event`
  (skip + rejection state-afectante), como hoy.
- `valid` / `event_auth_disabled`: aplicar normal.

Cambio puntual en el loop (pseudo):
```
res = verify_event_auth(event, config, root=root)
reason = res.get("reason")
if res.get("valid") is not True and reason in TAMPER_REASONS:
    state["rejections"].append({... UNAUTHENTICATED_EVENT, reason ...}); events_applied++; continue
# unresolved_key / missing_key -> caer a la aplicacion normal (NO rejection, NO skip)
... (aplicar idempotency_keys / aggregate_versions / leases como evento valido) ...
```

El gate del validador para event_auth (si existe uno que falle duro) debe tratar UNVERIFIABLE_HERE como
info ("no verificado: faltan secretos en este entorno"), nunca exit!=0.

## acceptance_criteria

- **AC1 - Secret-independencia del estado.** Para el log T0 sellado (eventos firmados), `rebuild_snapshot`
  produce el MISMO `canonical_hash(state)` con secretos presentes y sin secretos. Golden determinista
  (mismo fixture, runner con y sin secret_file -> hash identico).
- **AC2 - Tamper aun detectado y state-afectante.** Un evento con `invalid_signature` (firma alterada) se
  registra como `security.unauthenticated_event` y NO se aplica; un evento sin firma con event_auth ON
  (`missing_signature`) idem. Golden negativo (>=2 vectores).
- **AC3 - Validate desde clon limpio sin secretos = exit 0.** `validate_collaboration_state --root .` sobre
  un clon del head T0 SIN `secrets/` da exit 0 (estado reproducible) y reporta event_auth como
  "no verificado aqui" (no fallo). Golden / verificacion de instancia.
- **AC4 - Sin regresion #4.** Suites #4 verdes con secretos: `attestation_health_cases` (AC2 health,
  rollback), `attestation_negative_cases` (6 vectores), `chain_auth_combined_cases`, `agent_signature_cases`,
  `event_auth_secret_resolution_cases`. La deteccion de falsificacion no se debilita.
- **AC5 - Reconciliacion del snapshot del head.** Tras el fix, el snapshot canonico del head T0 = forma
  secret-independiente; `validate` exit 0 desde clon limpio (sin secretos) Y desde D: (con secretos), MISMO
  hash. drift 0.
- **AC6 - Gates.** `validate` + `scan_encoding` + `scan_domain_neutrality` + el nuevo
  `replay_secret_independent_cases` en CI.

## test_plan

- `examples/replay_secret_independent_cases/run_*.py`:
  - fixture con eventos firmados (event_auth ON); rebuild con secret_file presente vs ausente ->
    `canonical_hash(state)` IDENTICO (AC1).
  - vector `invalid_signature` (mutar firma) + `missing_signature` -> rejection + no aplicado, con y sin
    secreto (AC2); el tamper se detecta incluso sin secreto? (no: sin secreto invalid_signature no es
    distinguible -> documentar: el tamper-detection requiere secreto; sin secreto, unverifiable; el golden
    corre el caso tamper CON secreto). Aclarar en el golden.
  - reporte JSON determinista (timestamps fijos), exit 0/1.
- Suites #4 existentes verdes (AC4).
- Verificacion de instancia: clon del head T0 sin secrets/ -> validate exit 0 (AC3/AC5).

## closure_criteria

- AC1-AC6; maker=Arquitecto implementa, checker=Codex reproduce independiente (maker!=checker); SemVer
  PATCH/MINOR + CHANGELOG; memoria actualizada; snapshot del head reconciliado a forma secret-independiente.
  #4 sigue ON; boundary T0 intacto.

## Risks

- **Reclasificar mal -> aceptar tamper.** Mitigacion: la particion es explicita; TAMPER (invalid/missing
  signature) sigue rechazando; goldens negativos. UNVERIFIABLE solo cubre clave-ausente (entorno).
- **Aclaracion honesta:** sin secreto, un entorno NO puede distinguir un evento autentico de uno forjado
  (no tiene la clave); por eso "no verificado aqui" no es una garantia de seguridad, solo de reproducibilidad
  de estado. La garantia de no-forja la da el entorno CON secretos (la instancia viva).

## Traceability

| Requirement | Task | Test | Closure |
|-------------|------|------|---------|
| Estado secret-independiente | TASK-0122 | replay_secret_independent_cases (AC1) | AC1/AC5 |
| Tamper aun rechazado | TASK-0122 | goldens negativos | AC2 |
| Validate clon-limpio sin secretos exit 0 | TASK-0122 | verificacion instancia | AC3 |
| Sin regresion #4 | TASK-0122 | suites #4 | AC4 |
