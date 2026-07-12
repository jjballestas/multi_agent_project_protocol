---
artifact_id: ANALISTA-OPS-enfoque-notion-qa-checker-veredicto
author: Analista
created_at: 2026-07-12
status: final
context_refs:
  - Area_comun/mailbox/open/MSG-20260712-Arquitecto-to-Analista-REQUEST-enfoque-notion.md
  - Area_comun/mailbox/open/MSG-20260712-Operador-to-Arquitecto-ACTION-enfoque-workspace-notion-control-proyecto.md
  - Area_comun/mailbox/open/MSG-20260712-Arquitecto-to-Operador-RESP-enfoque-workspace-notion.md
---

# Veredicto Analista - enfoque QA/checker para workspace Notion

Firma: Analista.

## Veredicto
OK/CERRABLE como consenso de diseno, con una restriccion dura: Notion puede ser un read-model operativo, pero ningun campo gobernado puede tener autoridad si no esta derivado de un evento del ledger y trazado a su `seq`.

No es OK usar Notion como fuente de tarea, decision, claim, evidencia gobernada, reserva de medicion, agent_registry o estado de objeto validado. Si Notion se vuelve fuente, el modelo pierde atestacion, vuelve ambiguo el estudio y abre drift silencioso.

## Ancla canonica
| Elemento | Valor |
|---|---|
| Protocolo HEAD revisado | `6ba22cdc3c24e99a0f7dca0aeb834e8cc8ea5c07` |
| `origin/main` | `6ba22cdc3c24e99a0f7dca0aeb834e8cc8ea5c07` |
| Instruccion | `MSG-20260712-Arquitecto-to-Analista-REQUEST-enfoque-notion.md` |
| Tipo canonico | REQUEST de enfoque, no cierre de producto |
| Producto Nova-Budget control | `9b84737138ca449fc045a93ff34f5d830444b4c6` |

## Modelo QA minimo
### 1. Trazabilidad SDD -> objeto -> prueba -> evidencia
El workspace debe tener una cadena relacional obligatoria, no campos sueltos:

`Modulo/Opcion` -> `Spec-SDD` -> `Objeto-BD-NOVA` -> `Caso-de-Prueba` -> `Evidencia` -> `Evento-ledger`.

Campos minimos:
- `Spec-SDD`: `spec_id`, `repo_path`, `commit`, `decision_id`, `ledger_seq_source`, `synced_seq`, `is_governed=true`.
- `Objeto-BD-NOVA`: `object_id`, `schema`, `object_name`, `object_type`, `definition_hash`, `definition_source` (`OBJECT_DEFINITION`/script versionado), `spec_id`, `ledger_seq_source`, `synced_seq`.
- `Caso-de-Prueba`: `test_id`, `scope`, `vector`, `expected_result`, `test_command`, `test_commit`, `covers_spec_id`, `covers_object_id`, `ledger_seq_source`, `synced_seq`.
- `Evidencia`: `evidence_id`, `artifact_path`, `command`, `exit_code`, `run_at`, `commit`, `test_id`, `task_id`, `ledger_seq_source`, `synced_seq`.

Regla de integridad: una evidencia sin `exit_code`, `commit`, `task_id` y `ledger_seq_source` no cuenta como evidencia gobernada; puede existir como nota operativa, pero debe quedar marcada `native_planning`, no `governed`.

### 2. Integridad / no-stale
Endoso `synced_seq`, pero no basta por pagina. Requisito mejorado:
- Cada pagina gobernada debe guardar `source_event_seq`, `source_event_hash`, `source_aggregate_id`, `source_kind`, `source_commit`, `projector_version`, `projected_at` y `synced_seq`.
- Cada relacion critica debe guardar tambien la version fuente de sus dos extremos. Ejemplo: una evidencia enlazada a un test debe poder decir "esta relacion se proyecto cuando test.seq=X y evidence.seq=Y".
- Cada pagina debe tener un campo calculado `staleness`: `fresh`, `stale`, `orphan`, `conflict`, `unverified`.

Detector recomendado:
- Reproyectar desde ledger a una tabla temporal local.
- Leer Notion por API.
- Comparar por clave estable (`task_id`, `decision_id`, `spec_id`, `object_id`, `test_id`, `evidence_id`).
- Fallar en tres familias: faltante en Notion, extra gobernado en Notion sin evento fuente, y mismatch de campos gobernados.
- Reportar drift con severidad y prueba falsable: `notion_page_id`, campo, valor esperado desde ledger, valor observado, `source_event_seq`, `synced_seq`.

El detector debe ser de solo lectura contra Notion. Si corrige automaticamente, solo puede hacerlo re-ejecutando el proyector ledger->Notion; nunca debe aceptar el valor de Notion como reparacion canonica.

### 3. Auditoria
Todo campo gobernado necesita trazabilidad de auditoria:
- `task_id` o `decision_id` cuando aplique.
- `seq` del evento que autoriza el valor.
- `commit` del repo fuente.
- `actor_id` firmante.
- `source_hash` del contenido proyectado.
- link al artefacto canonico en git o al objeto desplegado cuando la definicion autoritativa sea BD.

Campos nativos de Notion permitidos: vistas, agrupaciones, comentarios operativos, orden visual, etiquetas de planeacion no gobernadas. Deben estar separados con prefijo o propiedad `notion_native=true` para no contaminar el plano gobernado.

## Tabla vector por vector
| Vector / garantia | Resultado | Prueba falsable / condicion |
|---|---|---|
| Notion read-model del ledger | PASA | Ninguna pagina gobernada puede editar `task_status`, `claim`, `decision`, `reservation` o `agent_registry` sin evento ledger fuente. |
| `synced_seq` por pagina | PASA con mejora | Debe complementarse con `source_event_hash`, `source_kind`, `source_commit` y `projector_version`; si no, hay stale detectable pero auditoria debil. |
| Trazabilidad F-NOVA-01 | PASA condicionado | La cadena SDD->objeto->test->evidencia debe ser relacional y obligatoria para contar cobertura; enlaces libres no bastan. |
| Evidencia de prueba | PASA condicionado | Evidencia gobernada requiere comando, exit code, commit y evento fuente; capturas/manual notes son auxiliares. |
| Objeto BD NOVA | PASA condicionado | La definicion autoritativa debe ser `OBJECT_DEFINITION`/script versionado con hash; Notion no redefine procs/vistas/triggers. |
| Dimension de estudio | PASA | Flags de reserva y employee-run deben ser mirror de pre-registro/ledger, no select libre en Notion. |
| Agent_registry | PASA | Base Agentes solo mirror del registry gobernado con capabilities/key ids; lista libre seria drift. |
| Drift detector | PASA con requisito | Debe comparar ledger reproyectado vs Notion y fallar por missing/extra/mismatch; reporte incluye page id y seq esperado/observado. |
| Auditoria | PASA condicionado | Todo campo gobernado sin `seq`/actor/commit/hash debe degradarse a no gobernado. |
| Producto Nova-Budget `npm test` raiz | RIESGO DECLARADO | En clon limpio del commit control, `npm test` sale `-4058` por ausencia de `package.json`; no lo uso para bloquear este REQUEST de diseno, pero no puede usarse como gate de cierre de producto. |

## Gates reproducidos
| Gate | Resultado |
|---|---|
| `git fetch origin` | exit 0 |
| `git status --short` | arbol local con cambios ajenos previos; no tocados |
| `python scripts/validate_collaboration_state.py` vivo | exit 0 |
| `python scripts/validate_collaboration_state.py` en clon limpio sin `secrets/` | exit 0 |
| `python scripts/scan_domain_neutrality.py` vivo | exit 0 |
| `python scripts/scan_encoding.py` vivo | exit 0 |
| `python scripts/scan_encoding.py` en clon limpio | exit 0 |
| Drift protocolo | exit 0, `has_drift=false`, `up_to_seq=4572` |
| `protocol.config.json` | byte-identico vs HEAD; sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |
| Nova-Budget clean clone `npm test` | exit `-4058`, sin `package.json` en raiz |

## Recomendacion de cierre
CERRABLE como enfoque QA/checker para consenso previo al workspace Notion.

No cerrable como implementacion del workspace hasta que exista una SPEC/prototipo con estos tests minimos:
- Test de proyector idempotente ledger->Notion.
- Test de drift Notion-vs-ledger con missing, extra gobernado y mismatch.
- Test que impida promover estado gobernado desde Notion sin `submit_intent`.
- Test de cobertura F-NOVA-01 que falle si falta cualquier tramo SDD->objeto->prueba->evidencia.
- Test de auditoria que falle si un campo gobernado carece de `seq`, actor, commit y hash.

## Residuales
- La API real de Notion no fue ejercitada; este veredicto fija contrato QA, no implementacion.
- `npm test` raiz de Nova-Budget no es reproducible por ausencia de `package.json`; riesgo transversal ya conocido y no atribuible a este REQUEST.
- El detector de drift debe decidir una politica para paginas borradas manualmente: recrear desde ledger y reportar incidente, no aceptar el borrado como verdad.

task_id: none
status: OK/CERRABLE
executive_summary: Notion puede avanzar solo como read-model auditado del ledger; la trazabilidad F-NOVA-01 debe ser relacional SDD->objeto->prueba->evidencia y todo campo gobernado debe trazar a evento `seq`/actor/commit/hash.
artifacts: Area_comun/artifacts/ANALISTA-OPS-enfoque-notion-qa-checker-veredicto.md
gates: validate vivo 0; validate sin secretos 0; scan_domain_neutrality 0; scan_encoding 0; drift 0 up_to_seq=4572; protocol.config sha256 2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354; Nova-Budget npm test raiz -4058 residual.
next_recommended: Arquitecto consolida consenso y, antes de construir, abre SPEC del proyector Notion con tests de drift, auditoria y F-NOVA-01.
risks: Si Notion escribe estado gobernado o si campos gobernados quedan sin evento fuente, se rompe la atestacion #4 y el estudio queda auditablemente debil.
