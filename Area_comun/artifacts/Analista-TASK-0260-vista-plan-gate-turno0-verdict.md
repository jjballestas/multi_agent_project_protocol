# VEREDICTO Analista - TASK-0260 (C1 vista de plan + gate de aprobacion de turno 0)

- Reviewer: Analista (voz adversarial independiente / checker)
- Fecha local: 2026-07-22 22:15 (UTC+2)
- Veredicto: **OK-CLOSABLE (GO)** con 3 residuales DECLARADOS (ninguno bloquea C1)
- Anclaje canonico: impl commit `b7d29c1` (deliver `5cfeb47`); protocolo origin/main HEAD `1ab1be1`.
  Verificado que `runtime/*.py` y `examples/runtime_plan_approval_cases/` son IDENTICOS entre
  `b7d29c1` y `1ab1be1` (git diff --stat vacio), asi que las puertas corridas en `b7d29c1`
  representan el HEAD vivo.

## Metodo (no confio en el arbol caliente ni en los nombres de test)

Clon LIMPIO `file://D:/Agentes/multi_agent_project_protocol` -> `D:/ccv0260`, `git checkout b7d29c1`.
Todas las puertas por EXIT code EN EL CLON. Ademas extraje los guardas `render_plan` /
`plan_approval_error` / `run_loop` del CLON y corri MIS PROPIOS payloads (28 aserciones, no las
del maker) contra toda la familia de cada criterio, buscando un escape nuevo.

## Puertas (clon limpio, b7d29c1, exit code)

| Puerta | EXIT |
|---|---|
| examples/runtime_plan_approval_cases/run_runtime_plan_approval_cases.py | 0 |
| examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py | 0 |
| examples/runtime_turn_cases/run_runtime_turn_schema_cases.py | 0 |
| examples/runtime_turn_cases/run_runtime_turn_semantic_cases.py | 0 |
| scripts/validate_collaboration_state.py | 0 |
| scripts/scan_encoding.py | 0 |
| scripts/scan_domain_neutrality.py --root . | 0 |
| git diff --check | 0 |

Estado canonico del hub (validate_collaboration_state) VERDE al arrancar y al cerrar. Drift 0.

## Vector por vector (payloads propios, 28/28 PASS)

| # | Criterio | Prueba adversarial | Resultado |
|---|---|---|---|
| 1 | Proyeccion pura (DEC-0009) | campo `risk` ausente -> queda `null` (no default) | PASS |
| 1 | Proyeccion pura | valor raro `risk: banana-XYZ` -> se muestra verbatim (no sanea) | PASS |
| 1 | Proyeccion pura | acceptance de forma rara -> passthrough sin coercion | PASS |
| 1 | Proyeccion pura | `.md` ausente -> unidad EXCLUIDA del plan (no fabrica fila con nulls) | PASS |
| 2 | Gate rehusa turno 0 | sin aprobacion: guarda devuelve error | PASS |
| 2 | Gate rehusa turno 0 | sin aprobacion: run_loop `ok:false`, reason "turn-zero plan approval required" | PASS |
| 2 | Gate rehusa turno 0 | el rehuse NO escribe eventos (cero efecto colateral) | PASS |
| 2 | Gate desactivado | `plan_approval.enabled:false` -> `None` (no rehusa) | PASS |
| 2 | CON aprobacion arranca | guarda `None` Y run_loop ya no rehusa por aprobacion (integral) | PASS |
| 3 | Autenticacion actor | plan.approved de actor NO human_owner (Codex) + hash OK -> RECHAZADO | PASS |
| 3 | Autenticacion hash | actor human + `approval_hash` rancio -> RECHAZADO | PASS |
| 3 | Autenticacion tipo | actor+hash OK pero `type` != plan.approved -> RECHAZADO | PASS |
| 3 | Baseline valido | human + hash + tipo correctos -> ACEPTADO | PASS |
| 3 | Sin falso-seguro | `agent_signatures_enabled:true` + evento SIN `actor_auth` -> RECHAZADO | PASS |
| 4 | Display no invalida | cambiar SOLO `goal`: `render_hash` cambia, `approval_hash` ESTABLE, NO invalida | PASS |
| 4 | Display no invalida | cambiar `verification_cmd`/`required_capability`/`estimate`: approval ESTABLE | PASS |
| 4 | Material invalida | cambiar `acceptance` -> `approval_hash` cambia -> INVALIDA | PASS |
| 4 | Material invalida | cambiar `risk` -> INVALIDA | PASS |
| 4 | Material invalida | anadir unidad ligada a la decision -> INVALIDA | PASS |
| 4 | Sin invalidacion falsa | reordenar unidades en TASK_INDEX -> `approval_hash` ESTABLE (orden por id) | PASS |
| 5 | Independencia | fuente del gate NO referencia `supervised_autonomy`/`human_checkpoint_every_k` | PASS |
| 6 | Seguridad hub | orchestrator NO corrido en el hub (ver abajo) | PASS |

La separacion `render_hash` (todo el render) vs `approval_hash` (solo id/acceptance/risk) es
exactamente la que hace que display no invalide y material si. Confirmado en AMBAS direcciones,
como pedia el punto 4.

## Punto 6 - seguridad hub (verificado en el ledger)

Los 5 eventos que anade `b7d29c1` en `runtime/state/events.jsonl` son `intent.applied` de Codex
(12 refs a TASK-0260, 16 `claim`, 4 `task_status`): es el flujo gobernado NORMAL via
`submit_intent`, NO ejecucion del orchestrator. Cero artefactos `runtime/runs/RUN-*.jsonl`.
`protocol.config.json` (epoch 1.14.0 / genesis 2E35F26E), dataset N=500 y las 6 unidades
RESERVADAS del preregistro NO estan en el filelist del commit. Fondo intocable, intacto.

## Residuales DECLARADOS (no bloquean; candidatos a endurecimiento futuro)

- **R1 (alcance por decision).** El gate se scoping por `runtime.plan_approval.decision_id`.
  Una unidad gobernada NUEVA ligada a OTRA decision (o sin decision) queda EXCLUIDA del plan
  decision-scoped y NO invalida la aprobacion de ese plan (probado: approval estable, unit-count
  sin cambiar). Con `decision_id` sin configurar (None) el plan incluye TODAS las unidades y
  cualquier alta invalida. Coherente con DEC-0103 C1 ("el conjunto" de una decision), pero
  implica: si el runtime seleccionara una unidad fuera de la decision configurada, esa unidad no
  esta cubierta por la aprobacion de este gate. Off-by-default en el hub.
- **R2 (fuerza de auth = postura del event-log).** La autenticacion del human_owner se apoya en
  `verify_event_auth` (HMAC, si `event_auth.enabled`) y `verify_actor_auth` (ed25519, si
  `agent_signatures_enabled`). Con AMBAS off (default scratch/hub actual) el chequeo de human_owner
  confia en el campo `actor` en texto plano; y con firmas ON, un evento con
  `actor_auth.method:"not_enforced_phase2"` sigue pasando (escotilla de fase 2 GLOBAL del runtime,
  no introducida por esta tarea). El gate se APILA correctamente sobre la auth existente pero
  HEREDA su debilidad off-by-default. No es un escape nuevo de TASK-0260.
- **R3 (slip de doc, no de comportamiento).** El intake `verification_cmd` (linea 25) nombra
  `examples/runtime_turn_cases/run_runtime_turn_cases.py`, que NO existe; los runners reales y
  verdes son los 3 split (`run_runtime_turn_obstacle_cases.py`, `_schema_`, `_semantic_`) +
  `run_runtime_plan_approval_cases.py`, todos correctos en el HANDOFF y todos exit 0. Es
  staleness cosmetica del intake; la cobertura por comportamiento esta completa.

## Anomalia de higiene (DECISION-0018, ajena a esta tarea)

`prune_state.py --check` = DUE (released_ratio 92.59 >= 90, exit 1). El pre-commit acotado (E6-A)
solo advierte y continua; CI es la frontera dura. La poda `--apply` muta `state/*.json` -> bajo
`enforce:true` es op del orchestrator (Arquitecto), no del checker. La senalo para el proximo
checkpoint del Arquitecto; NO la ejecuto.

## Recomendacion de cierre

**OK-CLOSABLE.** Los 6 puntos del encargo se cumplen por comportamiento; ninguno de los 28
payloads adversariales abrio un escape. R1/R2/R3 quedan declarados y no falsan ningun criterio de
aceptacion de C1. El Arquitecto puede ratificar el GO y cerrar TASK-0260 (flip a done). R1 y R2
son notas de endurecimiento futuro (opcionales); R3 es un fix cosmetico opcional del intake.

-- Analista
