---
spec_id: SPEC-0071-tempfile-acl-hardening-writepath
task_id: TASK-0094
type: design
status: proposed
created_at: 2026-06-09
author: Claude (arquitecto)
linked_decisions: [DECISION-0022, DECISION-0020, DECISION-0007, DECISION-0006]
relates_to: [TASK-0093, SPEC-0070, MAINTENANCE-CODEX-SANDBOX-20260609]
---

> PROMOVIDA por Claude (2026-06-09) para FORMALIZAR bajo flujo un cambio que Codex ya implemento como
> mantenimiento UNTRACKED durante la re-entrega de TASK-0093. El cambio toca el WRITE-PATH AUTORITATIVO
> bajo enforce+authoritative -> merece ratificacion como todo lo demas (DECISION-0022). OFF-PILOT, NO
> multiplicador. SA.4 sigue DE-ARMADO.

# Diseno - Hardening tempfile/ACL del write-path para Windows sandbox unelevated

## 1. Contexto (hallazgo del sandbox unelevated)

Tras el fix `[windows] sandbox = "unelevated"` (cierra os error 740), aparecio un 2do problema: bajo el
token sandboxed de `codex exec` unelevated, `tempfile.TemporaryDirectory()` / `mkdtemp` / `os.mkdir(path,
0o700)` crean rutas con ACL restrictiva (`0o700`) que dejan al propio proceso sandboxed sin acceso
efectivo (`WinError 5 / PermissionError`). Afecta suites con tempdir y, criticamente, el WRITE-PATH del
runtime que usa tempdirs del SO para staging/backups de materializacion y rollback
(`materialize_to_disk`, snapshot backups). Claude NO reproduce el fallo en su harness (token distinto);
es especifico del sandbox de codex, pero el SMOKE REAL del piloto corre `codex exec` sandboxed -> debe
quedar robusto.

## 2. Estado actual (cambio untracked de Codex a formalizar)

Codex ya implemento (seq 190-195, claims de mantenimiento liberados, SIN task/SPEC/handoff/DoD,
SIN commit) un cambio que reemplaza tempdirs del SO por tempdirs repo-local con ACL heredada:
- NUEVO `runtime/temp_paths.py` (helper de temp dirs repo-local con ACL heredada).
- ediciones pequenas a `runtime/apply.py` (+5/-2), `runtime/protocol_replay.py` (+12/-3),
  `runtime/submit_intent.py` (+5/-2) que enrutan staging/backups por el helper.
- edicion a `AGENTS.md` seccion 7 (regla "Windows sandbox temp ACL") -> ver seccion 4 (postura).

Drift 0 sostenido; 55 goldens verdes en el harness de Claude. El cambio es pequeno y sensato; el
problema es de PROCESO (untracked + write-path bajo enforce + edicion de contrato sin DECISION ni claim).
Esta SPEC lo formaliza para que Codex lo commitee bajo flujo con DoD + handoff.

## 3. Alcance

1. **Helper repo-local de temp dirs (`runtime/temp_paths.py`)**: crea rutas de trabajo dentro del repo
   (o de un workspace de ACL heredada explicitamente aprobado), con ACL normal heredada, limpiadas tras
   uso. Reemplaza `tempfile.TemporaryDirectory`/`mkdtemp`/`0o700` en el WRITE-PATH (staging de
   materializacion, snapshot/runtime backups de rollback) por el helper.
2. **Cableado** en `apply.py`/`protocol_replay.py`/`submit_intent.py` (los puntos que crean tempdirs
   para materialize/backup/rollback).
3. **NO cambiar** la semantica del write-path (idempotencia, drift 0, rollback lossless, fencing):
   solo la UBICACION/ACL de las rutas temporales. Byte-equivalencia de la materializacion (mismo
   canonical_hash) antes/despues.
4. **Vendor/OS-neutral**: el helper debe degradar a comportamiento estandar fuera de Windows/sandbox
   (no romper Linux/CI). Cross-platform (DECISION-0006).

## 4. Postura para la regla "temp ACL" (decision del operador; Claude recomienda B)

El cambio incluye una regla operativa nueva. Hay dos posturas:
- **(A) DECISION propia + queda en el contrato AGENTS.md seccion 7.** Si se considera regla de
  colaboracion del protocolo. Requiere DECISION-00XX registrada + claim que cubra AGENTS.md.
- **(B) RUNBOOK operativo en `Area_comun/protocol/` (recomendada).** Es una regla de OPERACION de
  agentes en Windows sandbox, no del contrato de negocio/protocolo (lo dijo el propio informe del
  sandbox). Se REVIERTE la edicion de `AGENTS.md` seccion 7 (hecha sin DECISION ni claim) y se documenta
  como runbook (p.ej. `Area_comun/protocol/RUNBOOK-windows-sandbox-temp-acl.md` o seccion en
  `runtime/README.md`). Sin edicion de contrato, sin DECISION.

**Claude recomienda (B).** >>> RATIFICADA = **(B)** por el operador (2026-06-09): se revierte la edicion
de AGENTS.md seccion 7 y la regla baja a runbook operativo en
`Area_comun/protocol/RUNBOOK-windows-sandbox-temp-acl.md` (sin DECISION, sin edicion de contrato).
TASK-0094 promovida a ready+GO.

## 5. Invariantes (duras)

1. OFF-PILOT: SA.4 sigue DE-ARMADO. NO re-armar ni piloto. enforce+authoritative ON: cero edicion
   manual de `*.json`; toda transicion por submit_intent. Un solo multiplicador por ventana.
2. Drift 0 sostenido; materializacion byte-equivalente (mismo canonical_hash). Rollback lossless intacto.
3. ASCII, sin secretos, determinista en CI. Template intacto. 1 commit/turno con rutas explicitas.
4. NO tocar el capability-gate ni la semantica de claims/intents.

## 6. Cierre (DoD)

- `runtime/temp_paths.py` + cableado commiteados bajo TASK-0094 con handoff autocontenido.
- Golden determinista que ejercite el helper (repo-local temp dir creado, escrito, limpiado) y la
  materializacion/rollback usando el helper -> byte-equivalente (mismo canonical_hash) + drift 0.
  Regresiones verdes: `runtime_protocol_materialize_cases`, `materialize_cross_fs_cases`, `intent_flow`,
  `runtime_loop`, `runtime_real_adapter`. Paridad `.ps1` donde aplique (ledger_ops/regenesis).
- Cross-platform: las suites pasan en Linux/CI (el helper degrada limpio) y dentro del sandbox de codex.
- Postura de la regla ACL aplicada segun ratificacion del operador (A o B). Si B: AGENTS.md seccion 7
  revertida + runbook en `Area_comun/protocol/`.
- validador / neutralidad / encoding verdes; drift 0; vendor/OS-neutral; sin secretos; SA.4 DE-ARMADO.

## 7. Fuera de alcance

- Re-armar SA.4 / piloto. Capa C. Cambiar el capability-gate o la semantica del write-path.
- El cierre de TASK-0093 (lo hace Claude por separado, en ventana limpia, tras formalizar este hardening).
