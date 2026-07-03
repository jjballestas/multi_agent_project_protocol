# Veredicto Analista - TASK-0246 re-gate consolidado DD-01/DD-02/DD-03

Firma: Analista

## Veredicto

CAMBIO-REQUERIDO / NO CERRABLE.

Ancla canonica:
- Protocolo HEAD/origin revisado: `4e42d64e37c7110a7b123bdbddcb7f739382dfba`.
- Instruccion REVIEW: `Area_comun/mailbox/open/MSG-20260704-Arquitecto-to-Analista-REVIEW-TASK-0246-regate-consolidado-dd.md`.
- Commit citado de horneado DD-01/DD-02/DD-03: `01f05db`.
- Commit citado de THROW/db_verified_at ya OK: `070b533`.
- Producto Zeus-protocol probado en clon limpio: `e7c6da482a1e819507af37de77b9cd46712fb8c8` (`origin/main` del clon local).

No re-audite THROW/db_verified_at; el foco fue el estado actual de `Area_comun/specs/nova/` y las tres decisiones de dominio pedidas.

## Reproduccion

| Gate | Evidencia | Exit |
|---|---:|---:|
| `git fetch origin` + `git status --short` | HEAD = origin/main `4e42d64`; cambios ajenos solo en `.claude/settings.json`, `personal/Analista/MEMORY.md` y `personal/*` no tocados antes del veredicto | 0 |
| `python scripts/validate_collaboration_state.py` | `OK: collaboration state is valid.` | 0 |
| Zeus-protocol clean clone + `npm test` | 112 tests, 90 pass, 22 skipped | 0 |
| Hub clean clone secretless + `python scripts/validate_collaboration_state.py --root <tmp>` | `OK: collaboration state is valid.` | 0 |
| `python scripts/scan_domain_neutrality.py` | clean | 0 |
| `python scripts/scan_encoding.py` | `OK: encoding scan is clean.` | 0 |
| Drift vivo | `has_drift=False`, `up_to_seq=3670` | 0 |
| Chain #4 vivo | `valid=True`, `checked_events=2998` | 0 |
| `protocol.config.json` byte-identico | HEAD, `01f05db`, `070b533`, `v1.18.0` y working tree comparten SHA256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` | 0 |

## Vectores revisados

| Vector | Resultado | Evidencia falsable |
|---|---|---|
| DD-01, P3-001..005 campo 2 confirma autorizacion Sprint 1 | PASA parcial | Las cinco SPECs P3 contienen `CONFIRMADO por el Operador (DD-01)` en el campo de usuario/rol. |
| DD-01, no dejar texto stale "declarado" en las cinco aprobaciones | SLIPS | `SPEC-NOVA-P3-001-initial-budget-draft.md:102` conserva `Supuesto temporal declarado (campo 2)` en riesgos. Eso contradice el pedido "CONFIRMADO (no declarado)" y deja dos fuentes normativas dentro de la misma SPEC. |
| DD-02, P3-003 alcance p.3 | PASA | `SPEC-NOVA-P3-003-commitment-draft.md:35` dice `objeto (min. 20 chars...; 400 ProblemDetails si <20)`. |
| DD-02, P3-003 restriccion 6d | PASA | `SPEC-NOVA-P3-003-commitment-draft.md:65` dice `objeto min. 20 chars` y que la validacion de aplicacion rechaza `<20` con `400 ProblemDetails`. |
| DD-02, P3-003 criterio de aceptacion falsable | SLIPS | La seccion `## 7. Criterios de aceptacion` no contiene ningun Given/When/Then para objeto `<20`, min 20 chars ni `400 ProblemDetails`. El criterio nuevo existe en alcance/restricciones, pero no quedo como AC ejecutable en la tabla que el maker debe probar. |
| DD-03, P3-003 SECOP vacio | PASA | `SPEC-NOVA-P3-003-commitment-draft.md:35` documenta `referencia SECOP (vacia -> 'N/A', DD-03)`. |
| DD-03, no centinela legacy `0` | PASA | `SPEC-NOVA-P3-003-commitment-draft.md:65` fija default `'N/A' declarada` y `jamas el '0'`; `:94` lo refuerza como riesgo mitigado. |

## Hallazgos bloqueantes

### F-0246-DD01-STALE-CONTRADICTION - WARNING-real

`SPEC-NOVA-P3-001-initial-budget-draft.md` quedo internamente contradictoria: el campo 2 confirma DD-01, pero la tabla de riesgos aun prescribe "Supuesto temporal declarado". El uso normal lo dispara porque un maker que use el campo 9 como mitigacion puede reintroducir el estado anterior.

Remediacion esperada: reemplazar esa mitigacion por una frase consistente con DD-01, por ejemplo "Confirmado por el Operador para Sprint 1; policy por operacion via BR-C4 post-Sprint-1".

### F-0246-DD02-MISSING-AC - WARNING-real

DD-02 fue pedido como criterio falsable. La SPEC P3-003 lo incluye en alcance y restriccion 6d, pero no en `## 7. Criterios de aceptacion`. Un maker puede cumplir la lista de AC sin probar el rechazo de objeto `<20`.

Remediacion esperada: agregar un AC explicito en P3-003, por ejemplo: dado un RP con objeto de 19 chars o menos, cuando intento crear/actualizar el borrador, entonces la API rechaza en validacion de aplicacion con 400 ProblemDetails y no invoca aprobacion BD.

## Residuales

- Revision documental; no hubo EXECUTE contra DbsFinanciero porque el encargo excluyo re-auditar THROW/db_verified_at.
- P4-004 conserva `SUPUESTO TEMPORAL`, pero no lo uso como bloqueo porque DD-01 fue pedido para las cinco SPECs P3-001..005.
- Zeus-protocol se probo en `origin/main` del clon limpio local porque la instruccion no cito un nuevo commit de producto para este re-gate documental.

## Recomendacion

CAMBIO-REQUERIDO. No cerrar el baseline DD-01/DD-02/DD-03 hasta corregir P3-001 riesgo stale y P3-003 AC faltante. Fix-loop esperado: remediacion documental, re-gate de `validate` con y sin secretos, `scan_domain_neutrality`, `scan_encoding`, drift 0, #4 byte-identica, y re-juicio Analista antes de cualquier cierre. Maximo 2 iteraciones antes de escalar al operador.

task_id: TASK-0246
status: CAMBIO-REQUERIDO
executive_summary: NO CERRABLE: DD-01 conserva una contradiccion stale en P3-001 y DD-02 no esta en la seccion de criterios de aceptacion de P3-003.
artifacts: Area_comun/artifacts/ANALISTA-TASK-0246-regate-consolidado-dd-veredicto.md; Area_comun/mailbox/open/MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0246-regate-consolidado-dd-NOGO.md
gates: validate vivo exit 0; Zeus clean clone npm test exit 0; validate secretless exit 0; domain exit 0; encoding exit 0; drift false up_to_seq 3670; chain valid checked_events 2998; protocol.config byte-identico SHA256 2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354
next_recommended: Remediar P3-001 riesgo DD-01 stale y agregar AC explicito DD-02 en P3-003; luego pedir re-juicio antes de cierre.
risks: Sin re-auditoria THROW por alcance; revision documental; producto probado en origin/main local sin commit producto nuevo citado.
