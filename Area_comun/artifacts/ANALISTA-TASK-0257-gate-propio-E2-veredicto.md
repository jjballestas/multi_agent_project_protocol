# ANALISTA TASK-0257 gate propio E2 - veredicto

Firma: Analista

## Veredicto

CAMBIO-REQUERIDO / NO CERRABLE.

Ancla canonica: hub `59607c022b0c1e3dceaf963eba26db9fcbcdc2bc`, implementacion
`acfe91d943f8`. La instruccion canonica declara SIN PRODUCTO EN ALCANCE y no cita
commit de producto; por ello `npm test` queda NOT_RUN. La revision se ejecuto en
clon limpio del hub, no sobre el working tree vivo.

## Hallazgos bloqueantes

### F-0257-01 - WARNING-real - el juicio no corresponde siempre al snapshot staged

`Area_comun/tasks/TASK-0257-d0103-c5-harness-hookspath-precommit-validate.md:21`
promete validar el snapshot que se va a commitear. Sin embargo,
`.githooks/pre-commit:17-26` solo exige equivalencia index/worktree para
`Area_comun`, `runtime/state`, configs y AGENTS. El ejecutable del juicio
`scripts/validate_collaboration_state.py` y sus dependencias bajo `runtime/*.py`
quedan fuera.

Repro falsable en clon limpio:

1. Cambiar `TASK-0257` de `in_review` a `done` y stagear solo ese task file.
2. Dejar UNSTAGED `raise SystemExit(0)` en
   `scripts/validate_collaboration_state.py`.
3. Ejecutar `git commit` con `core.hooksPath=.githooks`.

Resultado: `validator_bypass_commit_exit=0`; el commit `2f50798` temporal aterrizo
el mismatch staged aunque el validator canonico lo rechaza. El mismo mismatch sin
la mutacion unstaged fue rechazado con exit 1 y mensaje
`Task TASK-0257 status mismatch`.

Impacto: un turno normal que edite el validator/runtime y estado gobernado puede
obtener falso verde o falso rojo por bytes que no forman parte del commit. No es
solo el bypass honesto `--no-verify`: el hook si se ejecuta, pero juzga con codigo
unstaged.

Remediacion minima: incluir `.githooks`, `scripts/validate_collaboration_state.py`
y toda dependencia ejecutada/importada por el hook en la equivalencia
index/worktree, o ejecutar los gates desde una materializacion del index. Agregar
negativo permanente que reproduzca esta mutacion unstaged.

### F-0257-02 - WARNING-real - el coste completo excede el umbral sin modo acotado

El acceptance en la tarea, linea 22, exige modo acotado a rutas tocadas cuando el
coste por commit excede aproximadamente 10 s. El handoff, lineas 29-30, declara
14.971 s y luego menos de 12 s para el hook completo; usa 5.574 s del validator
aislado para justificar no acotar. Mi commit positivo vacio midio 11.531 s y el
negativo 12.944 s. El objeto medido por el acceptance es el hook completo, no solo
un subgate.

Remediacion minima: implementar el modo acotado no desactivable prometido, o
modificar canonicamente el acceptance antes del re-juicio con umbral y racional
que midan explicitamente el hook completo.

## Matriz vector por vector

| Vector / AC | Resultado | Evidencia falsable |
|---|---|---|
| 1. Hub armado y gates previos conservados | PASA | Hub vivo y clon: `core.hooksPath=.githooks`; hook conserva prune y guia e invoca validator. |
| 2. Snapshot staged, suciedad personal permitida y gobernada rechazada | SLIPS | Personal untracked + empty commit exit 0; task gobernado unstaged exit 1; F-0257-01 permite commit roto exit 0 mediante validator unstaged. |
| 3. Negativo y positivo en clon limpio | PASA-PARCIAL | Positivo exit 0; mismatch canonico exit 1 con mensaje accionable; no compensa F-0257-01. |
| 4. Coste y modo acotado | SLIPS | 11.531 s positivo y 12.944 s negativo; no existe modo acotado pese a AC de ~10 s. |
| 5. Export born-operational en todos los tiers | PASA | coordination/runtime/attested: new_instance exit 0, validate exit 0, hook+prune+guide presentes; SHA-256 del hook identico `2C335680...727D60`. |
| 6. Desarme E3 | PASA | Tarea, handoff y README documentan `git config --unset core.hooksPath`, rearme y enforcement duro residual. |
| 7. Bypass honesto | PASA | README/tarea declaran `--no-verify` y CI + clean-clone como enforcement duro. |
| Caracter no-ASCII del handoff | NO DEFECTO | Handoffs/artifacts son docs UTF-8; la regla ASCII dura aplica a mailbox/state. No es AC de TASK-0257. |

## Gates reproducidos

- Hub canonico clean clone `59607c0`, sin secretos: validate exit 0; domain exit
  0; encoding exit 0; prune exit 0.
- Hub vivo con secretos: validate exit 0; drift `has_drift=false`.
- Canonico: drift `has_drift=false`, `up_to_seq=4913`; chain valid,
  `checked_events=4241`.
- `protocol.config.json`: diff byte a byte contra `TFM-dataset-N500` exit 0;
  SHA-256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Producto: NOT_RUN por alcance canonico y ausencia de commit de producto citado.

## Residuales y fix-loop

El hook local sigue siendo evitable por diseno; no se pide convertirlo en
enforcement duro. El fix-loop esperado es remediar F-0257-01 y F-0257-02, correr
positivo/negativo/bypass-unstaged, export de tres tiers, validate con/sin secretos,
drift 0, domain, encoding y config #4 byte-identica, y pedir re-juicio Analista
antes del commit de cierre. Maximo 2 iteraciones antes de escalar al operador.

Nota de autoria canonica: el commit concurrente del Arquitecto materializo este
archivo durante el ruteo del NO-GO; la presente revision final queda confirmada y
commiteada por Analista sin alterar el juicio ni ampliar el alcance.

task_id: TASK-0257
status: CAMBIO-REQUERIDO
executive_summary: El hook base funciona, pero puede juzgar estado staged con validator unstaged y excede el umbral completo sin modo acotado.
artifacts: Area_comun/artifacts/ANALISTA-TASK-0257-gate-propio-E2-veredicto.md
gates: clean hub validate/domain/encoding/prune 0; drift 0; chain valid; config #4 byte-identica; product NOT_RUN por alcance canonico
next_recommended: Remediar F-0257-01 y F-0257-02 y solicitar re-juicio Analista antes de cerrar o abrir TASK-0258.
risks: El bypass local honesto permanece; el bloqueo se limita a falso juicio por codigo unstaged y coste contractual no acotado.
