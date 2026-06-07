---
spec_id: SPEC-0060-faseF7.3-provenance
task_id: TASK-0074
type: implementation
status: draft
created_at: 2026-06-07
author: Claude (arquitecto)
linked_decisions: [DECISION-0001, DECISION-0019]
relates_to: [SPEC-0057, SPEC-0059]
---

> DRAFT en personal/Claude/ (Fase 7.3). Construye sobre F7.1 (SBOM) + F7.2 (manifiesto+verify). Aditivo,
> determinista, neutral, SIN secretos (la firma cripto es F7.4). Promover de a una (DECISION-0020) cuando F7.2
> cierre.

# SPEC-0060 - Fase 7.3: provenance / atestacion (SLSA-lite)

## 1. Objetivo

Registrar, de forma estructurada y verificable, la PROCEDENCIA de un release: quien lo construyo, de que
commit, con que proceso, y sobre que sujeto (el manifiesto/SBOM de F7.2). Estilo SLSA-provenance minimo, sin
firma todavia (la firma es F7.4): la provenance da TRAZABILIDAD; la firma dara AUTENTICIDAD.

## 2. Alcance (aditivo, determinista, sin secretos)

1. **`scripts/generate_provenance.py`** (+ paridad/delegacion `.ps1`): emite una atestacion canonica de
   provenance que enlaza con el manifiesto de F7.2:
   - `subject`: `{ name: "<paquete>@<protocol_version>", digest: { sha256: <manifest.sbom_hash> } }`
     (pinea el release por su hash).
   - `builder`: `{ id: <actor/builder provisto> }` (quien/que construyo; provisto, sin inferir del entorno).
   - `invocation`: `{ commit: <provisto>, process: <comando/recipe declarado, p.ej. generate_manifest> }`.
   - `metadata`: `{ timestamp: <provisto>, schema: provenance.v1 }`.
   - Salida JSON canonica (ASCII/sin BOM, orden estable). Determinista (commit/timestamp/builder PROVISTOS;
     sin reloj/red).
2. **Verificacion de consistencia** (extiende `verify_release` o un check propio): la provenance es coherente
   si su `subject.digest.sha256 == manifest.sbom_hash` del release verificado; si no, error legible. (No
   valida firmas: eso es F7.4.)
3. Golden `examples/provenance_cases` + CI.

## 3. Tests (golden determinista, sin red)

1. `generate_provenance` con manifiesto/commit/builder/timestamp fijos => atestacion canonica esperada.
2. Determinismo: dos corridas identicas => byte-identico.
3. Consistencia OK: provenance cuyo `subject.digest` coincide con el `sbom_hash` del manifiesto => verifica.
4. Consistencia FALLA: `subject.digest` que no coincide => error/exit != 0.
5. Neutralidad: la atestacion lista metadatos/hashes (no contenido ni estado de dominio); gates verdes.

## 4. Fuera de alcance

- Firma criptografica / claves (F7.4). Integracion completa al flujo de release y docs (F7.5). Cualquier
  secreto. Inferir builder/commit del entorno (se proveen para determinismo). Cambios al turn schema.

## 5. SemVer

- MINOR (atestacion aditiva de release engineering; no cambia contrato ni nucleo).

## 6. Secuencia

Tras F7.3: F7.4 (firma; requiere DECISION-0023, probable, + aprobacion humana) -> F7.5 (docs+integracion).
