# ANALISTA TASK-0257 gate propio E2 - re-juicio final iteracion 2

Firma: Analista

## Veredicto

CAMBIO-REQUERIDO / NO CERRABLE / ESCALAR AL OPERADOR.

Ancla canonica evaluada: hub `f64dcbdf9080ce87d4722c50662bb375d9d3c57a`,
con remediacion `e2cadd822cd7`. La instruccion REVIEW quedo canonica en
`dc2dd70`, cita expresamente el snapshot `f64dcbd` y declara SIN PRODUCTO EN
ALCANCE. No existe commit de producto citable; `npm test` queda NOT_RUN.

El selector `ACMRTD` cierra el repro de borrado del validator: un commit real
que elimina `scripts/validate_collaboration_state.py` termina exit 1. Tambien
rechaza las eliminaciones reales de `runtime/protocol_replay.py` y
`Area_comun/state/TASK_INDEX.json`, y un cambio de tipo `T` del validator.
F-0257-01 y F-0257-02 no regresan. Sin embargo, la garantia completa sigue
rota por dos escapes reproducibles, incluido el borrado del propio hook que el
handoff declara cubierto.

## Hallazgos bloqueantes

### F-0257-03 persiste - borrar el propio hook permite el commit

Repro falsable en clon limpio de `f64dcbd`:

```text
git config core.hooksPath .githooks
git rm .githooks/pre-commit
git commit -m "adversarial delete hook"
```

Resultado: commit exit 0, commit `516e473` creado. Git no puede ejecutar un
hook que ya no existe en el working tree. El negativo permanente no prueba el
comportamiento prometido: despues de `git rm`, llama directamente a
`sh .githooks/pre-commit` y solo exige exit distinto de 0. El exit no cero
proviene de que el archivo a ejecutar no existe, no de que Git haya rechazado
el commit. Por ello el test pasa mientras el bypass real tambien pasa.

### F-0257-04 nuevo - R100 desde ruta gobernada a ruta externa evade el modo completo

Repro falsable en clon limpio de `f64dcbd`:

```text
git config core.hooksPath .githooks
git mv scripts/validate_collaboration_state.py docs/renamed-validator.py
git diff --cached --name-status
git commit -m "adversarial rename validator outside"
```

Resultado: el diff muestra
`R100 scripts/validate_collaboration_state.py docs/renamed-validator.py`, pero
el commit termina exit 0 y crea `eefd73a`. La seleccion usa
`git diff --cached --name-only --diff-filter=ACMRTD`; para el rename observa
solo el destino fuera de `scripts/` y pierde el origen gobernado. El hook entra
en modo acotado y no intenta invocar el validator que el snapshot esta
retirando de su ruta canonica.

## Matriz vector por vector

| Vector / AC | Resultado | Evidencia falsable |
|---|---|---|
| A - alta bajo ruta gobernada | PASA | Artefacto valido staged bajo `Area_comun/artifacts/`: hook exit 0, 42.922 s, con validator completo exit 0. |
| M - estado invalido y bypass unstaged F-0257-01 | PASA | Suite permanente exit 0; exige rechazo del estado roto staged y del `raise SystemExit(0)` unstaged. |
| D - validator | PASA | `git rm scripts/validate_collaboration_state.py` + commit real: exit 1. |
| D - dependencia runtime | PASA | `git rm runtime/protocol_replay.py` + commit real: exit 1 desde prune/import. |
| D - estado gobernado | PASA | `git rm Area_comun/state/TASK_INDEX.json` + commit real: exit 1 desde validator/drift. |
| D - propio hook | SLIPS | `git rm .githooks/pre-commit` + commit real: exit 0; F-0257-03 persiste. |
| R - origen gobernado hacia destino externo | SLIPS | R100 del validator a `docs/`: commit real exit 0; F-0257-04. |
| T - cambio de tipo del validator | PASA | Diff `T scripts/validate_collaboration_state.py`; commit real exit 1 por ambiguedad index/worktree. |
| 1. Hub armado y checks previos | PASA | El snapshot conserva prune, validator y gate de guia; `core.hooksPath=.githooks` se probo en fixtures. |
| 3. Positivo gobernado | PASA | Hook completo exit 0; validator exit 0. |
| 4. Coste y modo acotado | PASA | Completo 42.922 s; acotado 0.383 s; ambos exit 0. |
| 5. Export born-operational, tres tiers | PASA | Coordination/runtime `new_instance` y validate exit 0; attested golden y validate exit 0; hook byte-identico en los tres, SHA-256 `3C52D876F4EF6662F5E2C5F1937DF9F6609C05AF5216B1D119081A328C559225`. |
| 6. Desarme E3 | PASA | Tarea, handoff y README conservan desarme/rearme y enforcement externo. |
| 7. Bypass honesto `--no-verify` | PASA | El limite sigue declarado. No cubre el borrado invisible del hook ni el rename de salida. |

## Gates reproducidos

- `python scripts/test_precommit_hook.py`: exit 0, pero su oraculo de borrado
  del propio hook es insuficiente segun el repro de commit real.
- Clon limpio sin `secrets/` en `f64dcbd`: validate exit 0; domain exit 0;
  encoding exit 0; drift `has_drift=false`, `up_to_seq=4967`; chain valid,
  `checked_events=4295`.
- Hub vivo con secretos en `dc2dd70`: validate exit 0; domain exit 0; encoding
  exit 0; drift `has_drift=false`, `up_to_seq=4972`; chain valid,
  `checked_events=4300`.
- `protocol.config.json`: byte-identico al ancla pineada `64d44ad`; SHA-256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Producto: NOT_RUN por alcance canonico y ausencia de commit de producto.

## Residuales y salida del tope

H2 permanece ruteado a TASK-0267 y no fundamenta este NO-GO. El residual
`--no-verify` sigue aceptado por diseno. Los dos bloqueantes aqui son escapes
nuevos o persistentes dentro de la garantia expresa de TASK-0257.

Esta era la iteracion 2 de 2. El fix-loop automatico queda agotado: no se
recomienda otra remediacion ni otro re-juicio por iniciativa de los agentes.
Arquitecto debe escalar al Operador el historial completo. Si el Operador
autoriza una excepcion o una nueva iteracion, los gates afectados son: commit
real tras borrado del propio hook, rename en ambas direcciones cruzando la
frontera gobernada, suite A/M/D/R/T, exports de tres tiers y todos los gates del
protocolo; despues corresponderia un nuevo re-juicio Analista antes del cierre.

task_id: TASK-0257
status: CAMBIO-REQUERIDO
executive_summary: El selector ACMRTD cierra borrados de validator/runtime/state, pero borrar el propio hook y renombrar el validator fuera de scripts permiten commits reales con exit 0.
artifacts: Area_comun/artifacts/ANALISTA-TASK-0257-gate-propio-E2-rejuicio-final-iter2-veredicto.md
gates: suite 0 con oraculo D-hook insuficiente; delete-validator/runtime/state 1 esperado; delete-hook 0 inesperado; rename-out 0 inesperado; T 1 esperado; exports 3 tiers 0; validate con/sin secretos 0; drift 0; domain/encoding 0; config #4 byte-identica
next_recommended: Escalar al Operador porque se agoto la iteracion 2 de 2; no abrir otro fix-loop sin directiva explicita.
risks: El hook puede desaparecer o perder el validator por rename en un commit que Git acepta; la regresion permanente ofrece un falso verde para el borrado del propio hook.
