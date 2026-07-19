# ANALISTA TASK-0257 gate propio E2 - re-juicio iteracion 1

Firma: Analista

## Veredicto

CAMBIO-REQUERIDO / NO CERRABLE.

Ancla canonica: hub `7fbb88acb94613502de115f4ceb7d6c72bfec9fb`, con
remediaciones `33af66b` y `5e5b2d5`. La instruccion canonica declara SIN
PRODUCTO EN ALCANCE y no cita commit de producto; `npm test` queda NOT_RUN. La
revision se ejecuto contra un clon limpio del hub en el commit citado.

F-0257-01 original queda cerrado para modificaciones: el repro exacto con estado
gobernado roto staged y `raise SystemExit(0)` unstaged en el validator termina
con hook exit 1. F-0257-02 tambien queda cerrado: el hook gobernado positivo
termina exit 0 en 29.532 s y el modo acotado no gobernado termina exit 0 en
0.401 s. Sin embargo, un escape nuevo en la misma garantia de snapshot impide
cerrar la tarea.

## Hallazgo bloqueante nuevo

### F-0257-03 - WARNING-real - una eliminacion staged evade el modo completo

`.githooks/pre-commit` obtiene las rutas con:

```text
git diff --cached --name-only --diff-filter=ACMR
```

El filtro excluye `D` (deleted). Por tanto, eliminar del snapshot staged una
ruta gobernada o un ejecutable del juicio no activa
`needs_collaboration_validation`.

Repro falsable en clon limpio de `7fbb88a`:

```text
git rm scripts/validate_collaboration_state.py
sh .githooks/pre-commit
```

Resultado observado: `delete_validator_hook_exit=0`; el diff staged era
`D scripts/validate_collaboration_state.py`. El hook solo informo que la poda no
estaba vencida y acepto un snapshot que elimina el validator que el acceptance
promete invocar. Esto contradice tanto la tarea como README, que prometen modo
completo cuando el snapshot staged toca `scripts/` o cualquier ejecutable del
juicio.

Remediacion minima falsable: incluir eliminaciones en la enumeracion staged
(y decidir explicitamente el tratamiento de type changes), agregar un negativo
permanente que elimine el validator y exigir hook exit distinto de 0. La prueba
debe cubrir al menos eliminacion staged bajo `Area_comun/`, `runtime/`,
`scripts/` y `.githooks/`, no solo el ejemplo del validator.

## Matriz vector por vector

| Vector / AC | Resultado | Evidencia falsable |
|---|---|---|
| 1. Hub armado y gates previos conservados | PASA | Hub vivo: `git config core.hooksPath` devuelve `.githooks`; hook conserva prune y guia. |
| 2a. Estado roto staged | PASA | Suite permanente exit 0; su negativo interno exige que el hook rechace el estado roto. |
| 2b. Validator mutado unstaged | PASA | Repro independiente exacto: hook exit 1 y mensaje `unstaged changes in governed or validation-code routes`. |
| 2c. Familia de rutas staged, incluidas eliminaciones | SLIPS | `git rm scripts/validate_collaboration_state.py` + hook termina exit 0 porque `--diff-filter=ACMR` omite `D`; F-0257-03. |
| 3. Positivo gobernado | PASA | Artefacto temporal bajo `Area_comun/artifacts/` staged: hook exit 0 y validator exit 0. |
| 4. Coste y modo acotado | PASA | Gobernado 29.532 s; no gobernado 0.401 s; ambos exit 0 y prune permanece activo. |
| 5. Export born-operational, tres tiers | PASA | `coordination`, `runtime` y `attested`: new_instance exit 0, validate exit 0, hook SHA-256 identico `E803C867977977E5AC04445AE1CE5B440DE7B0B2669FC44358E3F6439717062C`; el comando de cableado se emite al crear cada instancia. |
| 6. Desarme E3 | PASA | Tarea, handoff y README conservan `git config --unset core.hooksPath`, rearme y enforcement externo. |
| 7. Bypass honesto | PASA | La documentacion mantiene el limite `--no-verify` y CI/clean-clone como enforcement duro. |

## Gates reproducidos

- Suite `python scripts/test_precommit_hook.py`: exit 0.
- Positivo gobernado: exit 0; negativo de bypass unstaged: exit 1 esperado;
  negativo nuevo de eliminacion: exit 0 inesperado.
- Hub vivo con secretos: validate exit 0.
- Hub canonico limpio sin secretos: validate exit 0; domain exit 0; encoding
  exit 0.
- Canonico: drift `has_drift=false`, `up_to_seq=4934`; chain valid,
  `checked_events=4262`.
- `protocol.config.json`: blob byte-identico a `TFM-dataset-N500`; SHA-256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Producto: NOT_RUN por alcance canonico y ausencia de commit de producto.

## Residuales y fix-loop

F-0257-01 y F-0257-02 pasan la remediacion pedida. H1 y H2 permanecen fuera de
este fix-loop segun la instruccion y no fundamentan este NO-GO. El residual
honesto `--no-verify` permanece aceptado por diseno.

Este es el segundo juicio del fix-loop. Se espera remediar F-0257-03, ejecutar
negativos de eliminacion sobre toda la familia de rutas afectadas, repetir los
gates de producto del hook y pedir re-juicio Analista antes del commit de cierre.
Al agotarse con esta pasada el maximo de 2 iteraciones indicado por el
Arquitecto, cualquier fallo adicional debe escalarse al Operador.

task_id: TASK-0257
status: CAMBIO-REQUERIDO
executive_summary: F-0257-01 y F-0257-02 quedan cerrados, pero una eliminacion staged de una ruta gobernada o del codigo de juicio evade el validator y el hook termina verde.
artifacts: Area_comun/artifacts/ANALISTA-TASK-0257-gate-propio-E2-rejuicio-iter1-veredicto.md
gates: suite 0; gobernado 0; bypass-unstaged 1 esperado; delete-validator 0 inesperado; exports 3 tiers 0; validate con/sin secretos 0; drift 0; domain/encoding 0; config #4 byte-identica
next_recommended: Remediar F-0257-03, cubrir eliminaciones staged en toda la familia de rutas, re-gatear y solicitar re-juicio Analista antes del cierre; escalar al Operador si aparece otro fallo.
risks: El hook permite commitear la eliminacion staged del propio validator sin ejecutar validacion completa; H1/H2 siguen ruteados fuera de TASK-0257.
