# Veredicto Analista - TASK-0246 SPECs baseline pre-Sprint 1

Firma: Analista
Fecha: 2026-07-04
Ancla protocolo revisada: 45ab4fc3bfd774a1ab24e478256f2179e1f55618
Instruccion REVIEW: 673c259 / Area_comun/mailbox/open/MSG-20260704-Arquitecto-to-Analista-REVIEW-SPECs-baseline-gate-pre-sprint1.md
Producto Nova-Budget: la instruccion no cita commit de producto; probe de control en clon limpio uso HEAD local e3a03a8cf3334c2a84bf54e964319dd08b953b45.

## Veredicto

CAMBIO-REQUERIDO / NO CERRABLE como baseline atestado.

La familia de 14 SPECs ya cubre q4_membership, estructura NOVA-SPEC-T-001, citas BD plausibles, aislamiento de pares y neutralidad namespaced. No queda cerrable porque dos horneados pedidos por el REVIEW no estan declarados de forma completa en el baseline: cache-confound falta en nueve SPECs medidas/gobernadas, y la precondicion sandbox<=14-jul falta en P4-004, aunque P4-004 es un mutador P4.x.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| `git fetch origin` | EXIT 0 |
| `git status --short` | EXIT 0; arbol con cambios ajenos preexistentes en `.claude/settings.json`, `personal/Analista/MEMORY.md` y `personal/Arquitecto/**`/`personal/operador/**` sin tocar |
| `python scripts/validate_collaboration_state.py` | EXIT 0 |
| `python scripts/scan_domain_neutrality.py` | EXIT 0 |
| `python scripts/scan_encoding.py` | EXIT 0 antes de escribir este veredicto |
| Secretless clean clone: `python scripts/validate_collaboration_state.py` | EXIT 0 |
| Secretless clean clone: `python scripts/scan_encoding.py` | EXIT 0 |
| Secretless clean clone: `python scripts/scan_domain_neutrality.py` | EXIT 0 |
| Drift probe `runtime.protocol_replay.protocol_state_drift` | has_drift=false, up_to_seq=3763 |
| Chain probe `validate_chain(events_in_log_order(...))` | valid=true, checked_events=3091 |
| `git diff --exit-code 673c259 -- protocol.config.json` | EXIT 0 |
| `git diff --exit-code 45ab4fc -- protocol.config.json` | EXIT 0 |
| `sha256(protocol.config.json)` | 2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354 |
| Producto clean clone `npm test` en raiz Nova-Budget e3a03a8 | EXIT -4058, no hay `package.json` raiz |
| Producto clean clone `apps/nova-web/npm test` antes de instalar deps | EXIT 1, `tsc` ausente |
| Producto clean clone `apps/nova-web/npm ci` | EXIT 0 |
| Producto clean clone `apps/nova-web/npm test` tras `npm ci` | EXIT 0, 1/1 tests |

## Tabla vector por vector

| Vector / AC | Resultado | Evidencia falsable |
| --- | --- | --- |
| Conteo de familia | PASA | Existen exactamente 14 `SPEC-NOVA-*.md` en `Area_comun/specs/nova/`; el informe aparte no cuenta como SPEC. |
| Formato NOVA-SPEC-T-001 | PASA | Las 14 SPECs tienen `Preambulo de gobierno (DoR)` y secciones `## 1` a `## 10`. |
| q4_membership declarado | PASA | Las 14 SPECs contienen `q4_membership:`. Valores: P2-001 FUERA, P2-002 FUERA, P2-003 DENTRO, P2-004 DENTRO, P3-001 FUERA, P3-002/003/004 CONDICIONAL, P3-005 FUERA, P4-001 FUERA, P4-002/003/004 DENTRO, P6-003 DENTRO. |
| Citas BD plausibles y F-NOVA-01 | PASA con residual | Los objetos citados estan namespaced (`Budget.*`, `Treasury.*`, `treasury.*`, `Core.*`) o declarados como procs a crear. Los THROW de P4-002/P4-003 quedan correctamente marcados como RE-VERIFICAR; P4-004 cita set real y excluye 50254/50256. No ejecute BD por alcance del REVIEW. |
| Aislamiento PAR-D / PAR-1 / pattern-setter | PASA | P2-004 declara PAR-D y `leyo_codigo_hermano = NO`; P4-002/P4-003 declaran PAR-1 y `leyo_codigo_hermano = NO`; P4-001 se declara pattern-setter fuera de contraste. |
| Adversarial separado / contexto limpio | PASA con advertencia | Todas las SPECs declaran `contexto limpio` o `SESION SEPARADA / contexto limpio`. Advertencia: la formula exacta no es homogenea entre baseline/P4 y P2-003/P2-004/P3/P4-004/P6-003. |
| checker_formal=0 baseline | PASA | P2-001, P2-002, P4-001, P4-002 y P4-003 declaran checker_formal=0 para el brazo baseline donde aplica. |
| cache-confound | SLIPS | Falta en 9 SPECs: P2-003, P2-004, P3-001, P3-002, P3-003, P3-004, P3-005, P4-004 y P6-003. Repro: buscar `cache-confound` en esos archivos devuelve 0 ocurrencias. El REVIEW pidio hornear cache-confound en el baseline. |
| correlation + task_id | PASA | Las 14 SPECs contienen `correlation` y `task_id`. |
| sandbox<=14-jul en mutadores P4.x | SLIPS | P4-001/P4-002/P4-003 declaran sandbox<=14-jul; `SPEC-NOVA-P4-004-apply-obligation-adjustment.md` no contiene `sandbox` ni `14-jul`, aunque es mutador P4.x (`Budget.Apply_Obligation_Adjustment`). |
| deuda front | RIESGO DECLARADO | Ninguna de las 14 SPECs contiene `deuda front`. No lo elevo a bloqueo independiente porque el REVIEW no define en que SPEC debe vivir, pero debe quedar resuelto o declarado fuera de alcance antes del sello de baseline. |
| Neutralidad | PASA | `python scripts/scan_domain_neutrality.py` EXIT 0; `specs/nova/` esta namespaced como instancia. |

## Hallazgos bloqueantes

### F-0246-BG-01 - WARNING-real - cache-confound incompleto

Repro falsable:

```text
Archivos sin cache-confound:
- Area_comun/specs/nova/SPEC-NOVA-P2-003-exploration-ui-shell.md
- Area_comun/specs/nova/SPEC-NOVA-P2-004-get-document-lists-brc3.md
- Area_comun/specs/nova/SPEC-NOVA-P3-001-initial-budget-draft.md
- Area_comun/specs/nova/SPEC-NOVA-P3-002-availability-certificate-draft.md
- Area_comun/specs/nova/SPEC-NOVA-P3-003-commitment-draft.md
- Area_comun/specs/nova/SPEC-NOVA-P3-004-obligation-draft.md
- Area_comun/specs/nova/SPEC-NOVA-P3-005-payment-draft.md
- Area_comun/specs/nova/SPEC-NOVA-P4-004-apply-obligation-adjustment.md
- Area_comun/specs/nova/SPEC-NOVA-P6-003-opentelemetry-observability.md
```

Impacto: el baseline pre-Sprint 1 queda con una condicion de medicion no simetrica. Si unas SPECs declaran la dinamica de cache y otras no, el cierre del baseline no demuestra que el confound fue tratado para toda la familia medida.

### F-0246-BG-02 - WARNING-real - P4-004 omite sandbox<=14-jul

Repro falsable:

```text
Select-String Area_comun/specs/nova/SPEC-NOVA-P4-004-apply-obligation-adjustment.md -Pattern 'sandbox|14-jul'
```

Resultado observado: sin ocurrencias.

Impacto: P4-004 es mutador P4.x y depende de `Budget.Apply_Obligation_Adjustment`; el REVIEW pidio confirmar `sandbox<=14-jul en los mutadores P4.x`. P4-001/P4-002/P4-003 lo declaran; P4-004 queda asimetrico.

## Residuales no bloqueantes

- No ejecute contra BD por alcance explicito del REVIEW; las citas BD quedan como plausibilidad documental + obligacion F-NOVA-01 de re-verificacion por maker.
- La instruccion REVIEW no cita commit de producto. El gate de producto se corrio como control en HEAD local e3a03a8, no como ancla canonica de cierre.
- `npm test` en raiz Nova-Budget sigue fallando por falta de `package.json`; el gate efectivo de `apps/nova-web` pasa tras `npm ci`.
- `deuda front` no aparece en las 14 SPECs; queda como riesgo de baseline si Arquitecto pretendia que ese horneado fuera textual por SPEC.

## Recomendacion

CAMBIO-REQUERIDO. Remediar F-0246-BG-01 y F-0246-BG-02 en las SPECs, re-gatear validate con/sin secretos, encoding, domain, drift 0, #4 byte-identica y pedir re-juicio de Analista antes de declarar el baseline atestado. Fix-loop maximo: 2 iteraciones antes de escalar al operador.

task_id: TASK-0246
status: change_required
executive_summary: CAMBIO-REQUERIDO / NO CERRABLE. La familia de 14 SPECs pasa estructura, q4_membership, citas plausibles, aislamiento y neutralidad, pero no deja baseline atestado porque cache-confound falta en nueve SPECs y P4-004 omite sandbox<=14-jul siendo mutador P4.x.
artifacts:
  - path_or_commit: Area_comun/artifacts/ANALISTA-TASK-0246-specs-baseline-pre-sprint1-veredicto.md
  - path_or_commit: Area_comun/mailbox/open/MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0246-specs-baseline-NOGO.md
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
  - command: git diff --exit-code 673c259 -- protocol.config.json
    result: PASS
  - command: Nova-Budget root npm test
    result: FAIL
  - command: Nova-Budget apps/nova-web npm ci && npm test
    result: PASS
next_recommended: Arquitecto remedia cache-confound en las nueve SPECs listadas y sandbox<=14-jul en P4-004; luego solicita re-juicio antes del cierre.
risks: Producto no tenia commit citado por la instruccion; BD no ejecutada por alcance explicito del REVIEW; deuda front queda como riesgo declarado si debia estar textual en las SPECs.
