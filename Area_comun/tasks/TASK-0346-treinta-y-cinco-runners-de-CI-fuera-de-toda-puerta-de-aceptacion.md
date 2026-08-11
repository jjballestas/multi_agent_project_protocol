---
id: TASK-0346
title: Treinta y cinco runners cableados en CI no estan en la puerta de aceptacion de ninguna tarea
status: done
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0346-treinta-y-cinco-runners-de-CI-fuera-de-toda-puerta-de-aceptacion.md
created: 2026-08-08
intake:
  type: fix
  goal: >
    Medido el 2026-08-08: de 66 runners de `examples/` cableados en `.github/workflows/validate.yml`,
    **35 no aparecen en el `verification_cmd` de ninguna tarea**. Nadie los ejecuta al entregar, asi
    que envejecen en silencio hasta que CI llega a ellos. Con CI en rojo desde el 2026-08-02, ninguno
    ha corrido en seis dias. Dos ya se han encontrado rotos por esta via -- el de status de mailbox
    (TASK-0344) y el de propiedades de runtime, que falla AHORA en local y en CI porque produccion
    exige un bloque `obstacles` que su generador no produce. Hay que arreglar el roto conocido,
    MEDIR cuantos mas lo estan, y cerrar el hueco estructural.
  acceptance:
    - "AC1 (el roto conocido, diagnostico primero): se mide y declara por escrito si el fallo de `run_runtime_property_cases.py` -- 'delivery turn is missing the obstacles block' con expected_valid true -- es defecto de produccion o generador obsoleto, y QUE cambio y en QUE tarea lo dejo obsoleto. No se toca nada antes de esa conclusion."
    - "AC2 (el censo real): se ejecutan LOS 66 runners y se declara, uno a uno, cuales pasan y cuales fallan. Esto convierte una rotura desconocida en una lista medida. Es el entregable principal."
    - "AC3 (se arregla el roto de AC1 y se declaran los demas): los fallos que aparezcan en el censo NO se arreglan aqui salvo el de AC1; se declaran con su sintoma para que el Arquitecto los particione."
    - "AC4 (el hueco estructural): se propone -- sin implementarlo unilateralmente -- como se garantiza que un runner cableado en CI quede alcanzable desde alguna puerta de aceptacion, o declarado explicitamente como de nivel protocolo con dueno. La propuesta se razona; la eleccion es del Arquitecto."
    - "AC5 (contrato): negativo permanente que muera si se anade a CI un runner que no queda cubierto por el mecanismo elegido en AC4, verificado por MUTACION. Si AC4 no se resuelve en esta tarea, este AC se declara diferido con su motivo."
    - "AC6 (cerrado en CI REAL): el paso `Run runtime property invariant cases` sale success en un run real de Actions, citando su id."
  verification_cmd:
    - "python examples/runtime_property_cases/run_runtime_property_cases.py"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/check_falsification_contracts.py --root ."
  scope_routes:
    - examples/runtime_property_cases/
    - runtime/turn_validate.py
    - Area_comun/protocol/FALSIFICATION_CONTRACTS.json
  out_of_scope:
    - "Arreglar los demas runners que el censo del AC2 revele rotos: se declaran y los particiona el Arquitecto."
    - "Implementar por tu cuenta el mecanismo del AC4: se propone y lo decide el Arquitecto."
    - "Codigo de producto."
  risk: high
  estimate: L
---

# TASK-0346 -- mas de la mitad de los verificadores no los ejecuta nadie al entregar

## Lo medido

    runners de examples/ cableados en validate.yml            66
    que NO aparecen en el verification_cmd de ninguna tarea    35

Y con CI en rojo desde el 2026-08-02, **ninguno de los 66 ha corrido en seis dias**.

## El roto conocido

`examples/runtime_property_cases/run_runtime_property_cases.py` -> **exit 1 en local y en CI**:

    errors: "semantic: delivery turn is missing the obstacles block; use [] when there was no friction"
    expected_valid: true
    error: "turn_validate returned unexpected validity"

El generador produce un parte de entrega que considera valido y `turn_validate` lo rechaza por
faltarle un bloque que produccion exige. Mismo patron que TASK-0344: produccion avanzo y el
generador se quedo atras.

## Por que el AC2 es el entregable principal

Hoy no sabemos cuantos de los 35 estan rotos. **El censo convierte una rotura desconocida en una
lista medida**, y eso vale mas que arreglar el que hoy nos molesta. Si salen ocho rotos, quiero los
ocho declarados con su sintoma, no ocho sorpresas repartidas por las proximas semanas.

## La relacion con TASK-0330

Es su tesis un nivel mas arriba. Alli eran 23 contratos declarados cuyo runner CI no ejecutaba;
aqui son 35 runners que CI si ejecuta y que **ningun maker corre al entregar**. En los dos casos, el
mecanismo existe y no actua sobre la decision de nadie hasta que es tarde.

## Diagnostico AC1 registrado antes del cambio

Medicion en HEAD `5d41c7eb`: `run_runtime_property_cases.py` salio 1. Los tres casos que el
generador declaraba validos omitian `obstacles`: dos entregas limpias y un rechazo de review con
friccion objetiva.

Clasificacion: **generador obsoleto, no defecto de produccion**. TASK-0259 remediation 1, commit
`c725e9bd`, hizo obsoletas esas tres suposiciones al establecer el contrato aprobado siguiente:

- toda entrega incluye el bloque `obstacles`, aunque una entrega sin friccion usa `[]`;
- un rechazo con `checks_failed` tiene friccion objetiva y usa una lista estructurada no vacia.

El refinamiento que cambio el contrato esta en
`MSG-20260722-Arquitecto-to-Codex-ACTION-TASK-0259-friccion-y-predicado.md`. Esta conclusion quedo
registrada en `personal/Codex/DIAG-TASK-0346-before-fix-20260809.md` antes de editar el generador.
El cambio de TASK-0346 agrega al fixture una lista vacia en las transiciones limpias y un obstaculo
estructurado cuando la propia transicion/review declara friccion. No cambia produccion.

## Censo AC2 - los 66 runners cableados

Fuente del universo: las 66 rutas unicas bajo `examples/` invocadas por `run:` en
`.github/workflows/validate.yml`; la invocacion duplicada del scanner de neutralidad cuenta una
sola vez y los dos validadores de `examples/minimal_instance` no son runners bajo `examples/`.
Todos se ejecutaron localmente el 2026-08-09. Resultado inicial: **48 PASS, 18 FAIL**. Tras el unico
arreglo autorizado por AC3, el numero 18 pasa y el saldo es **49 PASS, 17 FAIL**. Ningun otro fallo
fue corregido.

| # | Runner | Resultado medido y sintoma |
|---:|---|---|
| 1 | `neutrality_scan_cases/run_neutrality_scan_cases.ps1` | PASS |
| 2 | `neutrality_scan_cases/run_powershell_host_cases.py` | PASS |
| 3 | `hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py` | PASS; 384.7 s |
| 4 | `human_guide_cases/run_human_guide_cases.py` | PASS |
| 5 | `encoding_gate_cases/run_encoding_gate_cases.py` | PASS; pwsh 7 POSIX parity UNMEASURED locally as declared by el runner |
| 6 | `handoff_release_cases/run_handoff_release_cases.py` | PASS |
| 7 | `mailbox_status_cases/run_mailbox_status_cases.py` | PASS |
| 8 | `mailbox_claim_scope_cases/run_mailbox_claim_scope_cases.py` | PASS |
| 9 | `runtime_prune_cases/run_runtime_prune_cases.py` | PASS |
| 10 | `sdd_validation_cases/run_sdd_cases.ps1` | PASS |
| 11 | `compact_comms_validation_cases/run_compact_comms_cases.ps1` | PASS |
| 12 | `sbom_cases/run_sbom_cases.py` | PASS |
| 13 | `release_verify_cases/run_release_verify_cases.py` | PASS |
| 14 | `provenance_cases/run_provenance_cases.py` | PASS |
| 15 | `release_sign_cases/run_release_sign_cases.py` | PASS |
| 16 | `runtime_router_cases/run_runtime_router_cases.py` | PASS |
| 17 | `runtime_nagent_golden_cases/run_runtime_nagent_golden_cases.py` | PASS |
| 18 | `runtime_property_cases/run_runtime_property_cases.py` | FAIL inicial: tres reportes validos sin `obstacles`; PASS despues del arreglo AC1, 26 muestras |
| 19 | `runtime_concurrency_cases/run_runtime_concurrency_cases.py` | FAIL: la muestra execute de entrega omite `obstacles` |
| 20 | `runtime_guardrail_cases/run_runtime_guardrail_cases.py` | FAIL: entrega sin `obstacles` y rechazo con `checks_failed` sin obstaculo no vacio |
| 21 | `runtime_tool_policy_cases/run_runtime_tool_policy_cases.py` | PASS |
| 22 | `runtime_eventlog_cases/run_runtime_eventlog_cases.py` | PASS |
| 23 | `runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py` | PASS |
| 24 | `runtime_protocol_materialize_cases/run_runtime_protocol_materialize_cases.py` | FAIL: dos fixtures de entrega omiten `obstacles`; ademas fallan dos controles de limpieza por residuos bajo `.protocol-tmp/` |
| 25 | `materialize_cross_fs_cases/run_materialize_cross_fs_cases.py` | PASS |
| 26 | `intent_flow_cases/run_intent_flow_cases.py` | FAIL: prune deja drift en `TASK_INDEX_ARCHIVE.json` y `CLAIMS_ARCHIVE.json` |
| 27 | `intent_tx_cases/run_intent_tx_cases.py` | PASS |
| 28 | `cutover_loop_cases/run_cutover_loop_cases.py` | PASS |
| 29 | `runtime_protocol_enforce_cases/run_runtime_protocol_enforce_cases.py` | FAIL: dos entregas omiten `obstacles`; tambien hereda el fallo del runner 24 |
| 30 | `runtime_protocol_genesis_ref_cases/run_runtime_protocol_genesis_ref_cases.py` | FAIL: una entrega omite `obstacles`; tambien hereda el fallo del runner 24 |
| 31 | `runtime_event_auth_cases/run_runtime_event_auth_cases.py` | PASS |
| 32 | `actor_auth_ed25519_cases/run_actor_auth_ed25519_cases.py` | PASS |
| 33 | `event_auth_runtime_override_cases/run_event_auth_runtime_override_cases.py` | FAIL: `event_state` runtime override rechaza la clave `event_auth.method` como no soportada |
| 34 | `event_auth_secret_resolution_cases/run_event_auth_secret_resolution_cases.py` | PASS |
| 35 | `replay_secret_independent_cases/run_replay_secret_independent_cases.py` | PASS |
| 36 | `connector_sqlserver_readonly_cases/run_connector_sqlserver_readonly_cases.py` | PASS |
| 37 | `connector_git_cases/run_connector_git_cases.py` | PASS |
| 38 | `connector_ci_cases/run_connector_ci_cases.py` | PASS |
| 39 | `skills_loader_cases/run_skills_loader_cases.py` | PASS |
| 40 | `runtime_instantiation_cases/run_runtime_instantiation_cases.py` | FAIL: ocho casos detectan placeholder sin resolver en `scripts/memory/test_memory_db.py` |
| 41 | `runtime_upgrade_cases/run_runtime_upgrade_cases.py` | PASS |
| 42 | `runtime_eventlog_gate_cases/run_runtime_eventlog_gate_cases.py` | FAIL: una entrega omite `obstacles`; otro caso no encuentra la clave `eventlog_events` |
| 43 | `runtime_review_qa_cases/run_runtime_review_qa_cases.py` | FAIL: cuatro casos `fail_qa`/`checks_failed` omiten obstaculo no vacio |
| 44 | `agent_registry_cases/run_agent_registry_cases.py` | FAIL: `case_explicit_registry`, `AssertionError` sin mensaje |
| 45 | `runtime_turn_cases/run_runtime_turn_schema_cases.py` | PASS |
| 46 | `runtime_turn_cases/run_runtime_turn_semantic_cases.py` | PASS |
| 47 | `runtime_apply_cases/run_runtime_apply_cases.py` | PASS |
| 48 | `runtime_loop_cases/run_runtime_loop_cases.py` | FAIL: tres casos con asercion vacia; reuse no crea `events.jsonl`; conflicto de claim llega a pre-gate por claims solapados en vez del resultado esperado |
| 49 | `supervised_autonomy_cases/run_supervised_autonomy_cases.py` | FAIL: siete casos con `AssertionError` sin mensaje |
| 50 | `team_bridge_cases/run_team_bridge_cases.py` | PASS |
| 51 | `runtime_observability_cases/run_runtime_observability_cases.py` | FAIL: `case_enriched_log_and_summary` y `case_budget_exhausted`, `AssertionError` sin mensaje |
| 52 | `runtime_budget_cases/run_runtime_budget_cases.py` | FAIL: tres casos son rechazados antes de medir presupuesto porque la entrega omite `obstacles` |
| 53 | `runtime_cost_attribution_cases/run_runtime_cost_attribution_cases.py` | PASS |
| 54 | `chain_auth_combined_cases/run_chain_auth_combined_cases.py` | PASS |
| 55 | `attestation_health_cases/run_attestation_health_cases.py` | PASS |
| 56 | `attestation_negative_cases/run_attestation_negative_cases.py` | PASS |
| 57 | `experiment_h1h3_cases/run_experiment_h1h3_cases.py` | PASS |
| 58 | `readonly_enforcement_cases/run_readonly_enforcement_cases.py` | PASS |
| 59 | `runtime_observability_nagent_cases/run_runtime_observability_nagent_cases.py` | PASS |
| 60 | `llm_adapter_cases/run_llm_adapter_cases.py` | FAIL: cinco casos con `AssertionError` sin mensaje |
| 61 | `llm_turn_wrapper_cases/run_llm_turn_wrapper_cases.py` | PASS |
| 62 | `llm_turn_wrapper_cases/run_llm_turn_wrapper_cases.ps1` | PASS |
| 63 | `runtime_real_adapter_cases/run_runtime_real_adapter_cases.py` | FAIL: budget stand-in produce una entrega rechazada por ausencia de `obstacles` |
| 64 | `mailbox_retry_cases/run_mailbox_retry_cases.py` | PASS; 113.1 s |
| 65 | `runtime_turn_cases/run_runtime_turn_obstacle_cases.py` | PASS |
| 66 | `runtime_turn_cases/run_post_gate_obstacle_cases.py` | PASS |

## AC3 - limite del arreglo

Solo se corrigio el numero 18, que es el roto nombrado por AC1. Los otros 17 fallos post-arreglo
quedan declarados para particion del Arquitecto. Aunque varios comparten el mismo fixture obsoleto,
no se editaron porque AC3 los deja expresamente fuera de alcance.

## Propuesta AC4 - decision reservada al Arquitecto

Propuesta: introducir un registro versionado de cobertura de runners, con una fila por cada ruta
unica bajo `examples/` cableada en CI. Cada fila debe elegir exactamente una de dos clases:

1. `acceptance_gate`: identifica el perfil/puerta reutilizable que ejecuta el runner y las clases
   de tarea obligadas a incluir esa puerta en su `verification_cmd`.
2. `protocol_ci`: identifica owner, step bloqueante, plataforma, SLA de ultima ejecucion verde y
   regla de particion cuando el runner falla.

Un validador compara en ambas direcciones el conjunto derivado de `validate.yml` con el registro:
cada runner CI tiene exactamente una fila viva, ninguna fila apunta a un runner inexistente y toda
fila `acceptance_gate` es alcanzable desde la politica de aceptacion declarada. El mismo validador
debe ser un gate obligatorio del workflow y de la validacion canonica. Esto evita usar busqueda
textual historica sobre tareas cerradas como falsa prueba de que un maker actual lo ejecutara, y
permite que los runners lentos o exclusivos de plataforma tengan ownership explicito sin forzarlos
en cada entrega.

No se implementa esta propuesta: elegir el schema, las clases de tarea y el SLA cambia una regla de
proceso y corresponde al Arquitecto.

## AC5 diferido

AC5 queda diferido porque depende del mecanismo que el Arquitecto elija en AC4. Para la propuesta
anterior, el negativo adecuado agrega por mutacion un runner sintetico a `validate.yml` sin fila en
el registro y exige que el validador falle; una segunda mutacion elimina o vuelve inalcanzable una
fila existente y tambien debe fallar. Implementarlo ahora fijaria unilateralmente el mecanismo que
AC4 reserva al Arquitecto.

## AC6 - cerrado en CI real

Tras el punto de control coordinado del Arquitecto en `a669f82d`, el run real de Actions
`31291178449` completo `Check systematic state pruning` con success y ejecuto
`Run runtime property invariant cases` con success sobre ese mismo HEAD. El job `validate` fallo
despues, en `Run runtime concurrency simulation cases`, uno de los 17 fallos ya declarados por AC2
y expresamente fuera del alcance de AC3. Por tanto AC6 queda medido y satisfecho sin ampliar el
arreglo autorizado.
