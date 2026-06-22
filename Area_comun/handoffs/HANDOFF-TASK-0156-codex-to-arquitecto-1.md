---
handoff_id: HANDOFF-TASK-0156-codex-to-arquitecto-1
task_id: TASK-0156
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-06-22T17:05:00Z
product_commit: 560a226
---

# TASK-0156 - Handoff Codex -> Arquitecto

## Entrega

- Producto `D:/Agentes/Zeus/Zeus-protocol` commit `560a226 feat(intake): sign extractor candidates`.
- `extractors.config.json` registra el worker de PRODUCTO `Extractor`, rol `extraccion`, provider `local-vlm`, modelo por defecto `qwen3-vl:4b-instruct`, endpoint loopback por defecto `http://127.0.0.1:11434/api/chat` y clave publica Ed25519.
- La clave privada de producto fue generada fuera del repo y queda gitignored en `D:/Agentes/Zeus/Zeus-protocol/.secrets/extractor_ed25519_private.pem`.
- `local-vlm` toma por defecto el modelo/endpoint del registro de workers cuando el runtime no los sobrescribe.
- Cada candidata escrita por el extractor lleva `extractor_worker_id: Extractor` y `extractor_signature` Ed25519 sobre un payload canonico de contenido/procedencia. La aprobacion de candidatas rechaza firma ausente o forjada antes del intake gobernado.
- No se toco `protocol.config.json`, `chain_manifest.json` ni `secrets/`; el Extractor no queda registrado como firmante #4.
- No se encendio uso vivo del Extractor. La capacidad sigue OFF-by-default y requiere GO posterior del operador + pasada del Analista.

## Keypair

La privada actual de producto esta en:

```powershell
D:/Agentes/Zeus/Zeus-protocol/.secrets/extractor_ed25519_private.pem
```

Para rotar, generar un nuevo par Ed25519 fuera del repo, escribir la privada en `.secrets/extractor_ed25519_private.pem`, y actualizar solo `publicKeyPem` en `extractors.config.json`. La carpeta `.secrets/` esta gitignored.

## Evidencia

- `node --check src/server.js` OK.
- `node --check tests/staticContract.test.js` OK.
- `git diff --check` OK.
- `npm test` PASS 48/48 en el producto.
- Smoke local OK en puerto 4184: `/healthz` y `/api/protocol/observe`.
- Clon limpio de `Zeus-protocol`: `npm test` PASS 48/48.
- Protocolo: `scan_encoding.py` OK; `scan_domain_neutrality.py` OK; `validate_collaboration_state.py` OK con warning no relacionado de `MSG-20260622-Arquitecto-to-Operador-ESTADO-cola-vacia.md`; drift false `up_to_seq=1206` antes de la claim de entrega.
- #4 byte-identica: `protocol.config.json`, `chain_manifest.json` y `secrets/` sin diff.

## Revision sugerida

- Verificar que `extractors.config.json` vive solo en producto y no altera el config #4.
- Verificar firma valida en candidatas producidas y rechazo de firma ausente/forjada.
- Verificar que la private key no aparece en `git status` salvo como ignorada bajo `.secrets/`.
