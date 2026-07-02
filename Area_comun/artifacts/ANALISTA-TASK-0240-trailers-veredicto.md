---
artifact_id: ANALISTA-TASK-0240-trailers-veredicto
task_id: TASK-0240
author: Analista
created_at: 2026-07-02
status: final
verdict: CAMBIO-REQUERIDO
---

# ANALISTA VEREDICTO - TASK-0240 trailers

Firma: Analista.

## Veredicto

CAMBIO-REQUERIDO / NO-GO.

La construccion esta inactiva en el canonico vivo y no auto-DoSea el pipeline, pero el parser acepta una linea exacta `Task-Id:` fuera de la seccion final de trailers git. Eso viola SPEC-F1-exception-trailers B.1 ("trailers git estandar, ultima seccion del mensaje") y deja pasar un commit gobernado cuyo linkage puede vivir como texto de cuerpo, no como trailer.

## Ancla canonica

- Protocolo instruccion REVIEW: `ae016274d547c2c3ae9d77c1c5e32da08a425451`.
- Implementacion citada: `6360569 feat(validation): build commit trailer gate`.
- Entrega coordinacion: `08b00ec coord(TASK-0240): deliver trailer gate`.
- Producto control: `D:/Agentes/Zeus/Zeus-protocol` commit `b2b2395da39090109db6de2dc50726dbaab1a11e` (la instruccion TASK-0240 no cita commit de producto nuevo; handoff dice producto limpio y sin tocar).
- Clon limpio producto: `C:/Users/johnb/AppData/Local/Temp/analista-0240-product-4f9b6aec7b0a445abc36389f5318671e`.
- Clon limpio protocolo: `C:/Users/johnb/AppData/Local/Temp/analista-0240-protocol-707ca64ec143438f8a0d0498577ab34a`.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| `npm --prefix <producto-clon> test` | EXIT 0, 109 tests, 87 pass, 22 skipped |
| `python scripts/test_trailers.py` en vivo | EXIT 0, 8 casos |
| `python <protocolo-clon>/scripts/test_trailers.py` | EXIT 0, 8 casos |
| `python scripts/validate_collaboration_state.py` | EXIT 0 |
| `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_collaboration_state.ps1 -Root .` | EXIT 0 |
| `python <protocolo-clon>/scripts/validate_collaboration_state.py --root <protocolo-clon>` | EXIT 0 |
| `powershell ... validate_collaboration_state.ps1 -Root <protocolo-clon>` | EXIT 0 |
| `python scripts/scan_domain_neutrality.py` | EXIT 0 |
| `python scripts/scan_encoding.py` | EXIT 0 |
| Drift vivo | `has_drift=false`, `up_to_seq=3342` antes de mi claim |
| `protocol.config.json` | SHA256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`, diff vacio contra `ae01627` |

## Vectores B.3 y probes propios

| Vector | Resultado | Evidencia falsable |
| --- | --- | --- |
| N1 gobernado sin `Task-Id` | PASA | Fixture oficial falla con `without exact Task-Id`. Probe propio con texto libre `fixes the task from yesterday` tambien falla. |
| N2 `fix` sin `Fixes-Task` | PASA | Fixture oficial falla con `without exact Fixes-Task`. |
| N3 `Fixes-Task` inexistente | PASA | Fixture oficial falla con `unknown Fixes-Task TASK-9999` en subject `fix`. |
| N4 `Task-Id: none` sin `Ops-Reason` | PASA | Fixture oficial falla con `without Ops-Reason`. |
| P1 gobernado con `Task-Id` valido | PASA | Fixture oficial verde. |
| P2 `fix` con ambos trailers | PASA | Fixture oficial verde. Probe propio `fix!:` con ambos trailers verdes. |
| P3 pre-arranque exento | PASA | Fixture oficial verde. |
| P4 `personal/**` exento | PASA | Fixture oficial verde. |
| F-2 trailer_start_seq inactivo | PASA | `protocol.config.json` no contiene `commit_trailers`; no existe `Area_comun/protocol/COMMIT_TRAILERS.json`; `validate` vivo y clean salen 0. |
| V5 texto libre ambiguo | PARCIAL | Texto libre sin linea exacta no cuenta. Pero una linea exacta `Task-Id: TASK-0240` en parrafo no final cuenta como trailer. |

## Slip bloqueante

### F-0240-01 - `Task-Id` fuera de la seccion final pasa

Payload minimo:

```text
subject:
feat: governed

body:
Task-Id: TASK-0240

extra paragraph after trailer-looking line
```

Archivo tocado: `scripts/x.py`. Config de fixture: `commit_trailers.enabled=true` y `start_commit=<base>`.

Resultado observado:

```text
non_final_exact_taskid_line: PASS_NO_ERRORS
```

Resultado esperado bajo SPEC B.1: rechazo. Esa linea no esta en la ultima seccion de trailers git; esta seguida por otro parrafo. El validador actual usa `trailer_values(message)` sobre todas las lineas del mensaje y no verifica que `Task-Id`, `Fixes-Task` y `Ops-Reason` pertenezcan al bloque final.

Impacto: el gate puede dar falso verde a commits gobernados con linkage escrito como cuerpo del mensaje. Eso debilita justo V5: mata texto libre ambiguo, pero no mata "linea exacta fuera de trailer".

## Residuales no bloqueantes

- Probe adicional: `feat: governed` con `Task-Id: TASK-0240` y `Fixes-Task: TASK-9999` pasa porque el subject no matchea `fix|revert|hotfix`. No lo uso como bloqueo principal porque B.3/N3 exige la familia `fix`, aunque conviene decidir si cualquier `Fixes-Task` presente debe referir una tarea existente.
- La activacion sigue diferida correctamente; no encontre auto-DoS vivo.

## Recomendacion

CAMBIO-REQUERIDO.

Endurecer el parser para extraer solo trailers git de la seccion final del mensaje (por ejemplo via reglas equivalentes a `git interpret-trailers`) y agregar un test negativo permanente: linea exacta `Task-Id: TASK-0240` seguida por otro parrafo debe fallar como ausencia de trailer exacto. Tras eso, re-gatear los 8 B.3, F-2 inactivo, gates de protocolo y producto control.
