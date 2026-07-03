# ANALISTA - Re-juicio TASK-0234 runbook onboarding remoto

Firma: Analista
Fecha: 2026-07-03
Task: TASK-0234
Decision: CAMBIO-REQUERIDO
Recomendacion de cierre: NO CERRABLE

## Ancla canonica

- Instruccion REVIEW: `MSG-20260703-Arquitecto-to-Analista-REVIEW-TASK-0234-rejuicio-runbook.md`, commit protocolo `9e90a02`.
- Remediacion revisada: `645cb78`, doc-only sobre `Area_comun/protocol/RUNBOOK_ONBOARDING_REMOTO.md`.
- Entrega previa bloqueada: `64d44ad`, con veredicto Analista `75741ad`.
- Producto: la instruccion no cita commit de producto nuevo; se mantuvo el control canonico anterior `e7c6da482a1e819507af37de77b9cd46712fb8c8`.
- Instancia Aegis usada para comprobar rutas F2.3/F2.2: `814365a702ff45752bb68f7b68b9506b41ffafa4`.
- #4 / core pineado: `protocol.config.json` byte-identico entre `645cb78` y `HEAD`, git blob `70d4c027a35b9d7d406bdfbe1cfcd427f203fc14`, sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| `git fetch origin` + `git status --short` | exit 0; arbol local tenia cambios ajenos/untracked preexistentes fuera de este veredicto. |
| JSON state con `utf-8-sig` | exit 0; `Area_comun/state/*.json` parsea OK. |
| `python scripts/validate_collaboration_state.py` | exit 0; warning no bloqueante sobre FYI stale. |
| `python scripts/validate_collaboration_state.py` en clon limpio sin `secrets/` | exit 0. |
| `python scripts/scan_domain_neutrality.py` | exit 0. |
| `python scripts/scan_encoding.py` | exit 0. |
| Drift #4 | exit 0; `has_drift=false`, `up_to_seq=3605`. |
| Clon limpio producto + `npm test` en `e7c6da482a1e819507af37de77b9cd46712fb8c8` | exit 0; 112 tests, 90 pass, 22 skipped. |
| Aegis clean clone `python scripts/test_distributed_git_harness.py` | exit 0; ruta F2.3 existe y test pasa. |
| Aegis clean clone `python scripts/distributed_e2e_task_cycle.py --remote <bare> --keep-workdir` | timeout local a 304 s; proceso hijo detenido. No lo uso como bloqueo nuevo porque TASK-0234 es doc-only y el cierre de F2.2 ya fue gateado en TASK-0233, pero queda como riesgo operativo si se pretende que este comando sea el smoke test rapido del runbook. |

## Vector por vector

| Vector / AC | Veredicto | Evidencia adversarial |
| --- | --- | --- |
| Onboarding en frio: clonar instancia remota privada | PASA | El runbook mantiene `git clone -c core.longpaths=true <URL-remoto-privado> <carpeta>` y aclara que no es el hub. |
| Configurar agente con config commiteada y Git como adapter | PASA | Declara `.agents/<id>/config.json`, `adapter=git`, `committedConfig=true`; no introduce adapters multi-IDE. |
| F-0234-01: comandos/payloads gobernados para claim/status | PASA PARCIAL | La seccion 3.1 agrega un `tx-claim.json` parseable y comando `runtime/submit_intent.py` con claim anidado, scope, `ready->claimed` y `claimed->in_progress`. |
| F-0234-01: entrega/handoff/cierre ejecutable de punta a punta | SLIPS | La entrega no da payload concreto: solo dice `tx-deliver.json = [{task_status in_progress->in_review},{claim op:release ...}]`. No hay JSON completo, `claim_id`, `idempotency_key`, ejemplo de handoff/mailbox ni comando de cierre `review_approved->done`. Un participante no-constructor todavia no puede copiar y ejecutar el ciclo completo prometido por el AC. |
| F-0234-02: ruta/comando falsable del harness F2.3 | PASA | El runbook referencia `scripts/distributed_git_harness.py` y `python scripts/test_distributed_git_harness.py`; en clon limpio de Aegis el test sale 0. |
| F-0234-02: ruta/comando falsable del ciclo e2e F2.2 | PASA CON RIESGO | El runbook referencia `python scripts/distributed_e2e_task_cycle.py --remote <ruta-remoto-bare> --keep-workdir`, que existe en Aegis. Mi ejecucion local no cerro antes de 304 s, asi que no lo uso como prueba positiva de operabilidad rapida. |
| Transferibilidad fuerte para agente que no construyo la instancia | SLIPS | La parte inicial ya es transferible, pero el primer handoff y el cierre siguen dependiendo de conocimiento tacito del protocolo: estructura exacta de `tx-deliver.json`, mensaje/handoff minimo y quien/como ejecuta el cierre. |
| Objetivo medido `<=1 dia` y medicion HP6 posterior | PASA | Declara objetivo, cronometraje posterior y que la medicion real no forma parte del doc. |
| ASCII, neutralidad y hub pineado | PASA | `scan_encoding.py`, `scan_domain_neutrality.py`, validate con/sin secretos y #4 byte-identica salen verdes. |

## Hallazgos

F-0234-01 sigue abierto en alcance reducido (WARNING-real, D3/S4): el runbook remedio el claim inicial, pero no entrega un payload concreto y completo para `tx-deliver.json`, ni ejemplo minimo de handoff/mailbox, ni cierre `review_approved->done`. Reproduccion falsable: abrir la seccion 3.1 y copiar los bloques disponibles; solo existe JSON completo para `tx-claim.json`, mientras la entrega queda como pseudo-lista y el cierre queda delegado en texto.

F-0234-02 queda mayormente cerrado (WARNING-theoretical residual): las rutas y comandos F2.3/F2.2 ya estan en el doc y la ruta F2.3 pasa en clon limpio. El comando F2.2 existe, pero en mi reproduccion local no completo antes de 304 s; si se quiere usarlo como smoke test del runbook, conviene documentar duracion esperada o timeout.

## Residuales

- La instruccion de re-juicio sigue sin citar commit de producto nuevo; use el control canonico anterior `e7c6da4`.
- El timeout del e2e no prueba por si solo un defecto del runbook doc-only, pero no permite contar ese comando como evidencia positiva de operabilidad rapida en esta pasada.

## Fix-loop esperado

Remediacion restante dentro de la iteracion 2/2 antes de escalar al operador:

1. Reemplazar el pseudo `tx-deliver.json` por JSON completo copy-paste con `idempotency_key`, `task_status in_progress->in_review`, release del claim y rutas de handoff/mailbox/artifacto que se deben commitear.
2. Agregar un ejemplo minimo de handoff o MSG de entrega validator-valid.
3. Aclarar el cierre: comando/payload `review_approved->done` si lo ejecuta el implementer con capability, o marcarlo explicitamente como paso del checker/coordinador y ajustar la DoD para no prometer que el nuevo participante lo ejecuta.
4. Re-gatear validate con/sin secretos, drift 0, domain, encoding, #4 byte-identica y re-juicio Analista previo al cierre.

task_id: TASK-0234
status: CAMBIO-REQUERIDO
executive_summary: "NO CERRABLE: la remediacion cierra la ruta/comando F2.3 y agrega el claim inicial, pero el ciclo completo prometido sigue sin payload concreto de entrega/handoff/cierre."
artifacts: "Area_comun/artifacts/ANALISTA-TASK-0234-runbook-onboarding-rejuicio-veredicto.md; Area_comun/mailbox/open/MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0234-rejuicio-NOGO.md"
gates: "validate=0; validate_no_secrets=0; domain=0; encoding=0; drift=0; product_npm_test_clean_clone=0; harness_f23_clean_clone=0; protocol_config_byte_identical=true"
next_recommended: "Remediar el payload completo de entrega/handoff/cierre y pedir re-juicio Analista iteracion 2/2 antes del commit de cierre."
risks: "Si se cierra asi, una employee-run externa puede depender de asistencia tacita justo en el primer write gobernado y en el cierre."
