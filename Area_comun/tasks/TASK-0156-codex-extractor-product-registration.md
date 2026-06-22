---
task_id: TASK-0156
title: "Proyecto-front: registro del worker Extractor a nivel PRODUCTO + keypair de producto + firma de candidatas + provider default qwen3-vl:4b-instruct (AC54, SPEC-0086, DECISION-0058 Opcion 2), off-by-default"
type: product
status: in_review
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0086
linked_decisions: [DECISION-0058]
created_at: 2026-06-22
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
file: Area_comun/tasks/TASK-0156-codex-extractor-product-registration.md
---

# TASK-0156 - Registro del Extractor a nivel producto + firma + modelo instruct (AC54)

> GO del operador (Opcion 2, DECISION-0058): el Extractor es worker de PRODUCTO, SIN re-genesis #4. maker=Codex /
> checker=Arquitecto + PASADA DEL ANALISTA (firma/PII). NO enciendas el uso vivo (GO aparte del operador).

## Alcance (AC54)
1. **Registro de workers a nivel PRODUCTO** (Zeus, FUERA de protocol.config.json; tipo `extractors.config.json` o
   un registro de workers): record del Extractor -- id `Extractor`, rol=extraccion, modelo default
   **`qwen3-vl:4b-instruct`** (variante no-thinking; el tag thinking no se desactiva), endpoint loopback
   (default `http://127.0.0.1:11434/api/chat`). Apunta el provider local-vlm a este default.
2. **Keypair de PRODUCTO del Extractor** (Ed25519): clave privada FUERA del repo (gitignored / dir de secretos
   de producto), publica en el registro de workers. NO en `signature_config` #4 (no firma el ledger).
3. **Firma de candidatas:** cada candidata producida por el Extractor lleva firma valida (Ed25519) + el id del
   firmante -> autoria honesta. Behavior-test: candidata con firma valida; firma forjada/ausente detectada.

## DoD
- AC54 verde con behavior-tests deterministas (firma valida/forjada; registro de workers fuera del config #4).
  Carry AC51/AC52/AC53. OFF-by-default. El registro NO toca protocol.config.json (#4 byte-identica, pinned 1.14.0).
- node --test/CI verde EN CLON LIMPIO; validate con/sin secretos exit 0; drift 0; neutralidad+encoding 0.
- Reproducido por el checker DESDE CLON LIMPIO; maker!=checker. PASADA DEL ANALISTA antes de cerrar.
- **NO enciende el uso vivo** del Extractor (GO aparte del operador + Analista al encender).

## Notas
- La generacion/colocacion de la clave privada de producto: documenta el comando y la ruta (dir de secretos de
  producto, gitignored); la clave NO se commitea. Si requiere accion del operador, dejalo en el handoff.
- Tras cerrar: el operador da el GO de USO VIVO (encender el flag) con la pasada del Analista sobre la config viva.
