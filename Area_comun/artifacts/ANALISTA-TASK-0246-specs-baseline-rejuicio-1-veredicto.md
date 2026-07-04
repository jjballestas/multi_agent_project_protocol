# Veredicto Analista - TASK-0246 SPECs baseline re-juicio 1

Firma: Analista
Fecha: 2026-07-04
Ancla protocolo revisada: 2098e96264e663e30630b0b0ece95f8f1b0a6bc3
Remediacion revisada: 386dca7d1a73daf25aabf18e33cdd11a6be0ea4e
Instruccion REVIEW: Area_comun/mailbox/open/MSG-20260704-Arquitecto-to-Analista-REVIEW-SPECs-baseline-rejuicio-1.md
Producto Nova-Budget: la instruccion no cita commit de producto; probe de control en clon limpio uso HEAD local e3a03a8cf3334c2a84bf54e964319dd08b953b45.

## Veredicto

CAMBIO-REQUERIDO / NO CERRABLE.

Los dos bloqueantes documentales del primer juicio estan remediados: las 14 SPECs tienen `cache-confound`, y P4-004 declara `sandbox<=14-jul`. No cierro el baseline porque el REVIEW de ejecucion exige gatear el producto en clon limpio con `npm test` por exit code, pero la instruccion no cita commit de producto y el `npm test` en la raiz de Nova-Budget falla por falta de `package.json`. El subproyecto `apps/nova-web` pasa tras `npm ci`, pero ese no es el gate canonico pedido en esta ejecucion.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| `git fetch origin` | EXIT 0 |
| `git status --short` | EXIT 0; arbol con cambios ajenos preexistentes en `.claude/settings.json`, `personal/Analista/MEMORY.md`, `personal/Arquitecto/**` y `personal/operador/**` sin tocar |
| `python scripts/validate_collaboration_state.py` | EXIT 0 |
| `python scripts/scan_domain_neutrality.py` | EXIT 0 |
| `python scripts/scan_encoding.py` | EXIT 0 antes de escribir este veredicto |
| Secretless clean clone: `python scripts/validate_collaboration_state.py --root <tmp>` | EXIT 0 |
| Secretless clean clone: `python scripts/scan_encoding.py --root <tmp>` | EXIT 0 |
| Secretless clean clone: `python scripts/scan_domain_neutrality.py --root <tmp>` | EXIT 0 |
| Drift probe `protocol_state_drift` | has_drift=false, up_to_seq=3763 |
| Chain probe `validate_chain(events_in_log_order(...))` | valid=true, checked_events=3091 |
| `git diff --exit-code 386dca7 -- protocol.config.json` | EXIT 0 |
| `git diff --exit-code 2098e96 -- protocol.config.json` | EXIT 0 |
| `sha256(protocol.config.json)` | 2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354 |
| Producto clean clone `npm test` en raiz Nova-Budget e3a03a8 | EXIT -4058, no hay `package.json` raiz |
| Producto clean clone `apps/nova-web/npm ci` | EXIT 0 |
| Producto clean clone `apps/nova-web/npm test` tras `npm ci` | EXIT 0, 1/1 tests |

## Tabla vector por vector

| Vector / AC | Resultado | Evidencia falsable |
| --- | --- | --- |
| Conteo de familia | PASA | Existen exactamente 14 `SPEC-NOVA-*.md` en `Area_comun/specs/nova/`; `NOVA-DEV-informe-revision-adversarial.md` no cuenta como SPEC. |
| F-0246-BG-01 cache-confound | PASA | Probe propio sobre las 14 SPECs: `missing_cache=[]`; las 9 antes faltantes ya contienen `cache-confound`. |
| F-0246-BG-02 sandbox<=14-jul en P4-004 | PASA | `SPEC-NOVA-P4-004-apply-obligation-adjustment.md` contiene `sandbox`, `14-jul` y `<=14-jul`. |
| q4_membership declarado | PASA | Las 14 SPECs contienen `q4_membership:`. |
| correlation + task_id | PASA | Las 14 SPECs contienen `correlation` y `task_id`. |
| checker_formal=0 baseline | PASA | Las 14 SPECs contienen `checker_formal=0`. |
| Neutralidad | PASA | `python scripts/scan_domain_neutrality.py` EXIT 0; `specs/nova/` queda namespaced como instancia. |
| Producto clean clone root `npm test` | SLIPS | La instruccion de ejecucion exige `npm test` en el clon del producto y gate por EXIT; en la raiz de Nova-Budget sale EXIT -4058 por `package.json` ausente. |

## Hallazgo bloqueante

### F-0246-R1-PRODUCT-GATE - WARNING-real - gate de producto no cerrable por instruccion incompleta/fallo de root npm

Repro falsable:

```text
git clone D:/Agentes/Zeus/NOVA/Nova-Budget <tmp>
git -C <tmp> checkout e3a03a8cf3334c2a84bf54e964319dd08b953b45
npm test --prefix <tmp>
```

Resultado observado: EXIT -4058, `Could not read package.json`, porque la raiz de Nova-Budget no tiene `package.json`.

Impacto: el pedido de REVIEW de esta ejecucion dice que el veredicto debe anclarse en el commit de producto citado y correr `npm test` ahi, gateando por EXIT. La instruccion de Arquitecto no cita commit de producto, y el control sobre HEAD local e3a03a8 no satisface el gate raiz. El cierre queda no falsable contra una ancla de producto canonica.

## Residuales no bloqueantes

- No ejecute BD por alcance del re-juicio; solo verifique los horneados documentales pedidos y los gates del protocolo.
- `apps/nova-web` pasa `npm ci` + `npm test` en clon limpio, pero lo declaro residual porque el gate textual de esta ejecucion fue `npm test` en el producto.
- La claim activa de Arquitecto sobre `TASK-0246` cubre tarea/estado, no el artefacto ni este MSG; no toque rutas reclamadas.

## Recomendacion

CAMBIO-REQUERIDO. Arquitecto debe emitir una instruccion canonica corregida con commit de producto y gate exacto si el gate valido es `apps/nova-web/npm ci && npm test`, o debe agregar un `package.json` raiz que haga pasar `npm test` en Nova-Budget. Re-juicio Analista previo al cierre. Fix-loop esperado: remediacion del gate/ancla, gates protocolo con/sin secretos, drift 0, domain, encoding, #4 byte-identica y re-juicio; maximo 2 iteraciones antes de escalar al operador.

task_id: TASK-0246
status: change_required
executive_summary: CAMBIO-REQUERIDO / NO CERRABLE. F-0246-BG-01 y F-0246-BG-02 pasan; el cierre queda bloqueado porque el producto no tiene commit citado y el gate obligatorio `npm test` en raiz Nova-Budget falla por EXIT -4058.
artifacts:
  - path_or_commit: Area_comun/artifacts/ANALISTA-TASK-0246-specs-baseline-rejuicio-1-veredicto.md
  - path_or_commit: Area_comun/mailbox/open/MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0246-specs-baseline-rejuicio-1-NOGO.md
gates:
  - command: python scripts/validate_collaboration_state.py
    result: PASS
  - command: python scripts/scan_domain_neutrality.py
    result: PASS
  - command: python scripts/scan_encoding.py
    result: PASS
  - command: secretless clean clone validate/encoding/domain
    result: PASS
  - command: drift and chain probes
    result: PASS
  - command: git diff --exit-code 386dca7 -- protocol.config.json
    result: PASS
  - command: Nova-Budget root npm test
    result: FAIL
  - command: Nova-Budget apps/nova-web npm ci && npm test
    result: PASS
next_recommended: Corregir la instruccion/ancla de producto o el gate root `npm test`; luego pedir re-juicio antes de cierre.
risks: Si se acepta implicitamente `apps/nova-web` como gate, las SPECs documentales quedan OK; pero sin ancla/gate canonico el cierre no cumple la instruccion de REVIEW de esta ejecucion.
