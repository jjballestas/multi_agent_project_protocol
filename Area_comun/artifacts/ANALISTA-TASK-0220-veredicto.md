# ANALISTA-TASK-0220-veredicto

Firma: Analista

Veredicto final: NO-GO.

Ancla canonica de protocolo: 0401ade20bc370e30fb8938564e558548c498fe7.
Instruccion REVIEW: Area_comun/mailbox/open/MSG-20260629-Arquitecto-to-Analista-GO-TASK-0220.md.
Producto Zeus-protocol: la instruccion no cita commit de producto; por control clone limpio de D:/Agentes/Zeus/Zeus-protocol quedo en b5675e5213f04b7bbd19aa3ff0160a54b747afcf y `npm test` salio exit 0.

Bloqueante canonico: los dos artefactos bajo review no existen en HEAD. `git ls-tree -r HEAD -- personal/Arquitecto` no devuelve los paths v2; `git show HEAD:personal/Arquitecto/DRAFT-DECISION-engram-memory-backend-v2.md` y `git show HEAD:personal/Arquitecto/PATCH-engram-observation-intent-v2.md` salen exit 1. En el working tree aparecen como untracked. Por tanto no son canonico revisable ni promovible.

## Reproduccion

| Gate | Resultado |
|---|---|
| `git fetch origin` | exit 0 |
| `git status --short` inicial | cambios ajenos solo en `personal/Arquitecto/*` y borradores personales; no tocados |
| JSON state con `utf-8-sig` | exit 0; todos los `Area_comun/state/*.json` parsean |
| `python scripts/validate_collaboration_state.py` canon vivo inicial | exit 0 |
| Claim Analista TASK-0220 | `submit_intent` exit 0, seq 2641, drift false |
| Protocolo clean clone `0401ade` validate | exit 0 |
| Protocolo clean clone `0401ade` neutrality | exit 0 |
| Protocolo clean clone `0401ade` encoding | exit 0 |
| Protocolo clean clone `0401ade` drift | exit 0, `has_drift=false`, `up_to_seq=2640` |
| `protocol.config.json` clean clone sha256 | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |
| Zeus-protocol clean clone `npm test` | exit 0, 109 tests, 87 pass, 22 skipped |
| Protocolo vivo post-claim validate/neutrality/encoding | exit 0 / exit 0 / exit 0 |
| Protocolo vivo post-claim drift | exit 0, `has_drift=false`, `up_to_seq=2641` |

## Canonicalidad

| Vector | Estado | Evidencia falsable |
|---|---|---|
| Artefactos v3 revisables | CAMBIO-REQUERIDO | La GO y TASK-0220 citan `personal/Arquitecto/DRAFT-DECISION-engram-memory-backend-v2.md` y `personal/Arquitecto/PATCH-engram-observation-intent-v2.md`; `git grep` solo encuentra esas rutas como referencias, no como blobs en HEAD. `git show HEAD:<path>` sale exit 1. |
| Ancla de producto | RIESGO DECLARADO | TASK-0220 es proyecto `multi_agent_project_protocol` y no cita commit de producto. Por mandato general hice clone de Zeus-protocol y `npm test` en HEAD clonado; no lo uso como gate sustantivo de la decision Engram. |

## Matriz de etiquetas

| Bloqueante / etiqueta declarada | Veredicto | Evidencia |
|---|---|---|
| A-activacion: `ESTRUCTURAL-SI-PRECONDICION(adoption_tier=='runtime')`, pendiente impl+tests | HONESTA en el borrador, pero no canonica | El borrador declara sin codigo merged ni tests en `DRAFT...:218-230` y la precondicion runtime/tier en `DRAFT...:243-253`. La fuente real confirma `event_state_config_error` short-circuit por tier en `runtime/protocol_replay.py:125-127`. |
| A-flip: `ESTRUCTURAL-SI-PRECONDICION(chain_enabled=true)`, pendiente impl+tests | HONESTA en el borrador, pero no canonica | `DRAFT...:232-241` declara la precondicion `chain_enabled`; fuente real: `runtime/eventlog.py:180-185` y `runtime/protocol_replay.py:155-162` atan el genesis hash a `protocol.config.json` solo si chain esta enabled. |
| B-PII / cero-prosa: `ESTRUCTURAL-PENDIENTE-IMPL+TESTS` | AUN-SOBRE-AFIRMA | El texto baja honestamente a "cero-PROSA" y declara residual de PII semantica corta en slug (`DRAFT...:137-158`, `PATCH...:438-446`), pero la fila sigue rotulada "B-PII / cero-prosa". Payload falsable contra la propia regex de la spec: `topic_key="nit-900123456"` y `supersedes="nit-900123456"` pasan `^[A-Za-z0-9][A-Za-z0-9._/:-]{0,127}$`; eso puede meter identificador sensible sin prosa. La etiqueta honesta debe ser "B-cero-prosa", no "B-PII hermetico". |
| C-atomicidad | HONESTA en el borrador, pero no canonica | `DRAFT...:179-203` y `PATCH...:438-463` declaran outbox/ACK/reconciliador abierto, no existencia inmediata en Engram, y el hueco `body_ref`. |
| D-reconstruccion | HONESTA en el borrador, pero no canonica | `DRAFT...:84-96` baja a cache no autoritativa y `DRAFT...:280-282` deja ENG-IMPORT diferido. |
| E-identidad | HONESTA en el borrador, pero no canonica | `DRAFT...:160-177` declara `actor_auth_enforce` como precondicion; fuente real confirma early-return si no esta activo en `runtime/submit_intent.py:773-779` y override gitignored en `runtime/eventlog.py:294-296`. |
| H-parche / suite + chokepoint + config | HONESTA en el borrador, pero no canonica | `PATCH...:413-447` declara SPEC, no probado; fuente real confirma no existe `engram_observation` en `INTENT_TYPES` (`runtime/submit_intent.py:84`) y el chokepoint unico `validate_intent` se llama en single y transaction (`runtime/submit_intent.py:524-536`, `999`, `1127`). |
| Premisa P1 | HONESTA en el borrador, pero no canonica | El borrador corrige "observaciones sin autor, relations con marked_by_actor" en `DRAFT...:50-58`. |
| Premisa P2 | HONESTA en el borrador, pero no canonica | El borrador corrige chunks append-only vs merge semantico en `DRAFT...:60-68`. |

## Payloads adversariales B

| Campo | Payload | Resultado contra la spec v3 | Lectura |
|---|---|---|---|
| `scope` | `persona@example.com NIT 900123456` | Rechazado por enum `{project, personal}` (`PATCH...:187-191`) | Cierra prosa libre. |
| `task_id` | `ver bug de Juan` | Rechazado por `^TASK-[0-9]{1,8}$` (`PATCH...:201-205`) | Cierra prosa libre. |
| `supersedes` | `la memoria vieja con el NIT` | Rechazado por slug regex (`PATCH...:207-214`) | Cierra prosa libre con espacios. |
| `topic_key` | `nit-900123456` | Aceptado por slug regex (`PATCH...:162`) | PII semantica corta puede entrar. Esta declarado como residual, pero contradice el rotulo "B-PII". |
| `supersedes` | `nit-900123456` | Aceptado por regex (`PATCH...:164`, `207-214`) | Mismo residual que `topic_key`. |
| `memory_project` | `map-codex` emitido por Analista | Rechazado por enforcement de actor (`PATCH...:236-247`) | Anti-typo por diseno; anti-impersonacion depende de `actor_auth_enforce`. |

## API/config inventada vs fuente

| Claim del patch | Estado | Evidencia |
|---|---|---|
| `event_state_runtime_override` no admite `engram` | PASA | Fuente real `runtime/eventlog.py:243-277`, allowlist `actor_auth_enforce`, `actor_auth_config`, `event_auth`. |
| `event_state_config_error` existe y corre antes de intent | PASA | Fuente real `runtime/protocol_replay.py:125-152`; `submit_intent.py:810-814`. |
| `protocol.config.json -> event_state.engram` | PENDIENTE, no existente | Fuente real `protocol.config.json` no tiene `event_state.engram`; el patch lo propone como campo nuevo. Honesto si se mantiene como SPEC OFF, no como implementado. |
| `dataset_seal` | PENDIENTE, no existente | No existe en fuente real; el patch propone guard nuevo en `event_state_config_error`. |
| `adoption_tier` | PASA | Fuente real `protocol.config.json:6`, runtime. |

## Recomendacion

NO-GO.

Correcciones minimas:

1. Materializar en canonico los dos artefactos bajo review o moverlos a una ruta compartida versionada antes de pedir cierre.
2. Cambiar la fila B de "B-PII / cero-prosa" a "B-cero-prosa / PII semantica corta disciplinaria" o anadir un guard estructural para PII corta en `topic_key` y `supersedes`.
3. En la siguiente GO, citar explicitamente el commit canonico de protocolo bajo review y declarar si no hay commit de producto aplicable.
