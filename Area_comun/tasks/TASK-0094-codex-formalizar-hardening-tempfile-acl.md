---
id: TASK-0094
owner: Codex
status: ready
type: implementation
priority: high
created_at: 2026-06-09
updated_at: 2026-06-09
depends_on: []
relates_to: [TASK-0093, SPEC-0070, MAINTENANCE-CODEX-SANDBOX-20260609]
phase: P2
spec_id: Area_comun/specs/SPEC-0071-tempfile-acl-hardening-writepath.md
linked_decisions: [DECISION-0022, DECISION-0020, DECISION-0007, DECISION-0006]
objective: (OFF-PILOT, no multiplicador) FORMALIZAR bajo flujo el hardening tempfile/ACL que ya implementaste como mantenimiento UNTRACKED (seq 190-195, sin commit) durante la re-entrega de TASK-0093. El cambio toca el WRITE-PATH AUTORITATIVO (runtime/temp_paths.py nuevo + apply.py/protocol_replay.py/submit_intent.py) bajo enforce+authoritative -> merece task+SPEC+DoD+handoff como todo lo demas (DECISION-0022). Reemplaza tempdirs del SO con ACL 0o700 (que dejan al token sandboxed de codex sin acceso, WinError 5) por tempdirs repo-local de ACL heredada para staging/backups de materializacion/rollback. NO re-armar SA.4 ni piloto.
expected_output: (1) runtime/temp_paths.py (helper repo-local de temp dirs, ACL heredada, limpieza tras uso, OS-neutral: degrada limpio fuera de Windows/sandbox) + cableado en apply.py/protocol_replay.py/submit_intent.py (puntos de staging/backup/rollback). NO cambiar semantica del write-path (idempotencia/drift0/rollback lossless/fencing); solo ubicacion/ACL de rutas temporales. (2) Golden determinista que ejercite el helper + materializacion/rollback via helper -> byte-equivalente (mismo canonical_hash) + drift 0; regresiones verdes (runtime_protocol_materialize_cases, materialize_cross_fs_cases, intent_flow, runtime_loop, runtime_real_adapter); paridad .ps1 donde aplique. Cross-platform (pasa en Linux/CI y dentro del sandbox de codex). (3) Postura de la regla "temp ACL" segun ratificacion del operador (Claude recomienda B): si B -> REVERTIR la edicion de AGENTS.md seccion 7 (hecha sin DECISION ni claim) y documentar como runbook en Area_comun/protocol/ (RUNBOOK-windows-sandbox-temp-acl.md); si A -> DECISION registrada + claim que cubra AGENTS.md. (4) Commit con rutas explicitas + handoff autocontenido. NO re-armar SA.4 (enabled=false) NI correr piloto.
question_to_resolve: Q1 postura de la regla ACL (A contrato+DECISION vs B runbook operativo) -> la ratifica el operador ANTES de pasar esta task a ready+GO; Claude recomienda B. Q2 confirmar por golden que la materializacion es byte-equivalente (mismo canonical_hash) antes/despues del helper y que las suites pasan TAMBIEN dentro del sandbox de codex. Si el helper choca con alguna invariante del write-path -> blocked + nota. Si submit_intent rechaza, NO editar *.json a mano.
closure_criterion: runtime/temp_paths.py + cableado commiteados bajo flujo; el write-path usa tempdirs repo-local de ACL heredada para staging/backup/rollback; semantica intacta (drift 0, materializacion byte-equivalente mismo canonical_hash, rollback lossless); golden determinista del helper + regresiones verdes (materialize, cross_fs, intent_flow, runtime_loop, real_adapter); cross-platform (Linux/CI + sandbox codex); postura ACL aplicada segun ratificacion del operador (B: AGENTS.md s7 revertido + runbook en Area_comun/protocol/; A: DECISION + claim); validador/neutralidad/encoding verdes; drift 0; vendor/OS-neutral; sin secretos; template intacto; SA.4 sigue DE-ARMADO; todo por submit_intent; handoff con evidencia.
sdd_required: true
---

# TASK-0094 - Formalizar el hardening tempfile/ACL del write-path (off-pilot)

> READY+GO (Claude 2026-06-09 via submit_intent). OFF-PILOT, no multiplicador. Formaliza bajo flujo el
> cambio que Codex implemento como mantenimiento UNTRACKED durante la re-entrega de TASK-0093 (ver
> anomalia DECISION-0018 en mailbox). SA.4 DE-ARMADO; NO re-armar ni piloto.
>
> >>> POSTURA ACL RATIFICADA POR EL OPERADOR (2026-06-09) = B. La regla "Windows sandbox temp ACL" NO
> queda en el contrato: dentro de esta task (1) REVERTIR la edicion de AGENTS.md seccion 7 (hecha sin
> DECISION ni claim), y (2) documentarla como RUNBOOK operativo en
> Area_comun/protocol/RUNBOOK-windows-sandbox-temp-acl.md (sin DECISION, sin edicion de contrato). El
> resto del alcance (helper temp_paths.py + cableado + golden byte-equivalente + handoff) sin cambios.

## Contexto

Ver SPEC-0071. El fix sandbox `unelevated` (cierra os740) destapo un 2do problema: tempdirs del SO con
ACL `0o700` dejan al token sandboxed de `codex exec` sin acceso (WinError 5). Codex hardeno el
write-path (temp_paths.py + cableado) PERO como mantenimiento untracked, sin task/SPEC/handoff/DoD, sin
commit, y editando AGENTS.md s7 sin DECISION ni claim. Esta task lo encauza por el flujo normal.

## Alcance (SPEC-0071 seccion 3-4)

1. `runtime/temp_paths.py` (helper repo-local ACL heredada, OS-neutral) + cableado en
   apply.py/protocol_replay.py/submit_intent.py. Semantica del write-path intacta.
2. Golden del helper + byte-equivalencia de materializacion (mismo canonical_hash) + drift 0 +
   regresiones + cross-platform + paridad .ps1 donde aplique.
3. Postura regla ACL segun ratificacion del operador (B recomendada: AGENTS.md s7 revertido + runbook).

## Restricciones (duras)

- OFF-PILOT: SA.4 de-armado; NO re-armar ni piloto. enforce+authoritative ON: cero edicion manual de
  *.json; todo por submit_intent. ASCII, sin secretos, determinista. Template intacto. 1 commit/turno con
  rutas explicitas. NO tocar el capability-gate ni la semantica de claims/intents. Capa C OFF.

## Cierre

Codex commitea bajo flujo con handoff; Claude ratifica adversarial (byte-equivalencia materializacion +
drift 0 + regresiones + postura ACL aplicada) y cierra por submit_intent.
