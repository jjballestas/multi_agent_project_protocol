---
artifact_id: ANALISTA-TASK-0230-new-instance-veredicto
task_id: TASK-0230
author: Analista
status: OK-CERRABLE
created_at: 2026-07-03
canonical_protocol_head: 8b215daf6c3820e427036a23d40994a565af0ba3
product_commit: e7c6da482a1e819507af37de77b9cd46712fb8c8
instance_commit: 172edcb53d18ac6568a61c42b10f644cf9fb9ed9
---

# Veredicto TASK-0230 - new_instance nova-budget

Firma: Analista.

Veredicto: OK/CERRABLE.

Ancla canonica:
- Protocolo revisado: `8b215daf6c3820e427036a23d40994a565af0ba3`.
- Producto revisado: `D:/Agentes/Zeus/Zeus-protocol` commit `e7c6da482a1e819507af37de77b9cd46712fb8c8`.
- Instancia revisada: `D:/Agentes/Zeus/NOVA` commit `172edcb53d18ac6568a61c42b10f644cf9fb9ed9`.
- Source tag: `v1.18.0` -> `c9a442354bb5002b4df3a21e581ef1e891029c58`.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| `git fetch origin` | exit 0 |
| `python scripts/validate_collaboration_state.py` en vivo con secretos | exit 0 |
| `npm test` en clon limpio de `Zeus-protocol` checkout `e7c6da4` | exit 0, 112 tests, 90 pass, 22 skipped |
| `python scripts/validate_collaboration_state.py` en clon limpio del hub checkout `8b215da` sin secretos | exit 0 |
| `python scripts/scan_encoding.py` en clon limpio del hub | exit 0 |
| `python scripts/scan_domain_neutrality.py` en clon limpio del hub | exit 0 |
| Drift del hub limpio | `has_drift=false`, `up_to_seq=3502` |
| Chain del hub limpio | valid, `checked_events=2830` |
| `python scripts/scan_encoding.py` en vivo | exit 0 |
| `python scripts/scan_domain_neutrality.py` en vivo | exit 0 |
| Drift del hub vivo | `has_drift=false`, `up_to_seq=3502` |
| Chain del hub vivo | valid, `checked_events=2830` |
| `protocol.config.json` vivo | sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`, byte-identico al pin esperado |
| `python scripts/validate_collaboration_state.py` en `D:/Agentes/Zeus/NOVA` | exit 0 |
| Drift de `D:/Agentes/Zeus/NOVA` | `has_drift=false`, `up_to_seq=3457` |

## Vectores

| Vector / AC | Resultado | Evidencia falsable |
| --- | --- | --- |
| Instancia generada desde tag `v1.18.0`, no desde HEAD | PASA | `instance.profile.json` declara `sourceProtocolRef: v1.18.0`; tag resuelve a `c9a4423`; `createNewInstance` por defecto planea `sourceRef=v1.18.0`; write propio en tmp produjo `sourceCommit=c9a4423`. |
| Ruta real `D:/Agentes/Zeus/NOVA` | PASA | Repo existe, HEAD `172edcb5`, contiene `instance.profile.json`, `Area_comun/`, `protocol.config.json`, `.agents/`, `.claude/`; `D:/Agentes/Zeus/nova-budget` no fue usado como ruta final. |
| Perfil arm/mode + taxonomia de riesgo | PASA | `operatingProfile.arm=budget`, `mode=governed-instance`, taxonomia `low/medium/high/critical` presente. |
| TASK_TEMPLATE extiende DoR v2 para feature/product | PASA | `Area_comun/protocol/TASK_TEMPLATE.md` de NOVA incluye `target_user`, `functional_scope`, `assets_inputs`, `tech_constraints`, `risks_list`, `priority` y regla anti-empty. |
| Guard de DoR por comportamiento | PASA | Payloads propios aceptan `ninguno`/`ninguna`/`ninguno declarado`; rechazan campos ausentes, `TBD`, `TODO`, `por definir`, strings vacios y arrays vacios; `priority` es obligatorio tambien en tipos no feature/product. |
| Cosecha nivel B: configs de agente commiteadas, Git adapter, no multi-IDE | PASA | `git ls-files` muestra `.agents/{Codex,Arquitecto,Analista}/config.json`; cada config declara `adapter: git`; profile declara `multiIdeAdapters:false` y `configsCommitted:true`. |
| Dry-run por defecto | PASA | Payload propio llamando `createNewInstance` sin `dryRun:false` devolvio `mode=dry_run` y no creo la carpeta destino. |
| Write atomico temp+rename y destino existente fail-closed | PASA | Script usa staging + `atomicPath` + `rename`; payload propio hizo write real en tmp y un segundo write fallo con `target already exists` sin reemplazar. |
| Target path no escapa del root | PASA | Payloads `Nova`, `n`, `../escape`, `nova_budget`, `nova budget`, `nova..budget`, `-nova`, `nova/evil` fallaron cerrado por nombre invalido o escape. |
| Source ref inexistente falla cerrado | PASA | Payload `sourceRef=no-such-ref` fallo antes de crear instancia. |
| Prohibido Engram / `gentle-ai install` no ejecutado ni habilitado | PASA | `instance.profile.json` declara `engramInstallAllowed:false`; `.agents` no contiene `engram` ni el comando prohibido; `git grep -i "gentle-ai install" -- instance.profile.json .agents Area_comun/protocol/TASK_TEMPLATE.md` salio exit 1. |
| Hub intacto | PASA | `protocol.config.json` del hub mantiene sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`; gates del hub vivo y limpio salen 0; drift 0. |

## Slips

No encontre slip bloqueante.

## Residuales

- `scripts/new-instance.mjs` acepta `--source-ref HEAD` si un operador lo pasa explicitamente. No bloquea TASK-0230 porque la instancia entregada, el default del bootstrapper y el write reproducido usan `v1.18.0`; si el contrato futuro quiere prohibir cualquier ref no-tag, debe hacerse como tarea separada.
- Un `git grep` global sobre toda la instancia encuentra textos heredados que mencionan `gentle-ai install` como prohibicion historica. No bloquea este gate porque los artefactos generados y configs commiteadas no contienen ni habilitan ese comando.

task_id: TASK-0230
status: done
executive_summary: OK/CERRABLE. La instancia NOVA esta anclada a `v1.18.0`, el producto `new-instance` pasa npm test en clon limpio, los payloads adversariales sobre DoR/path/write no abren escape bloqueante, y el hub conserva gates verdes con drift 0 y config byte-identica.
artifacts:
  - Area_comun/artifacts/ANALISTA-TASK-0230-new-instance-veredicto.md
  - Area_comun/mailbox/open/MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0230-new-instance-OK.md
  - D:/Agentes/Zeus/Zeus-protocol@e7c6da482a1e819507af37de77b9cd46712fb8c8
  - D:/Agentes/Zeus/NOVA@172edcb53d18ac6568a61c42b10f644cf9fb9ed9
gates:
  - command: npm test (clean clone Zeus-protocol checkout e7c6da4)
    result: PASS
  - command: python scripts/validate_collaboration_state.py (hub live and clean clone)
    result: PASS
  - command: python scripts/scan_encoding.py
    result: PASS
  - command: python scripts/scan_domain_neutrality.py
    result: PASS
  - command: custom Analista behavior payloads for new-instance and DoR
    result: PASS
next_recommended: Arquitecto can ratify closure and route the bounded residuals only if future policy wants a tag-only CLI contract.
risks: Nonblocking residuals: explicit `--source-ref HEAD` is accepted by the generic CLI, and inherited docs mention the forbidden installer only as a prohibition.
