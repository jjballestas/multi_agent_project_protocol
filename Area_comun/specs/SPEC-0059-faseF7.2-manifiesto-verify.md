---
spec_id: SPEC-0059-faseF7.2-manifiesto-verify
task_id: TASK-0073
type: implementation
status: accepted
created_at: 2026-06-07
author: Claude (arquitecto)
linked_decisions: [DECISION-0001, DECISION-0019]
relates_to: [SPEC-0057]
---

> Segunda rebanada de Fase 7 (release engineering). Construye sobre F7.1 (SBOM, TASK-0071). Aditivo,
> determinista, neutral, sin secretos, sin firma (la firma es F7.4). Promover de a una (DECISION-0020).

# SPEC-0059 - Fase 7.2: manifiesto de release + verificacion de integridad

## 1. Objetivo

Dar un **manifiesto de release** verificable y un comando **verify** que confirme, por hash, que un arbol
(p.ej. un release recibido por un adoptante) coincide exactamente con lo declarado. Es integridad por
CONTENIDO (sin claves externas todavia; la firma cripto es F7.4).

## 2. Alcance (aditivo, determinista, sin secretos)

1. **`scripts/generate_manifest.py`** (+ paridad/delegacion `.ps1`): produce un manifiesto canonico del
   release que envuelve el SBOM de F7.1:
   - `version_axes` (protocol/runtime/schema/profile), `commit` y `timestamp` PROVISTOS (sin reloj/red).
   - `sbom` (reusa `generate_sbom`) o referencia + `file_count`.
   - `manifest_hash` / `sbom_hash`: hash canonico (sha256) del SBOM canonico => un unico digest que pinea
     todo el release.
   - Salida JSON canonica (ASCII/sin BOM, orden estable).
2. **`scripts/verify_release.py`** (+ paridad/delegacion `.ps1`): dado `--root <arbol>` + `--manifest <path>`,
   recomputa el SBOM del arbol y:
   - compara contra `manifest.sbom_hash` => OK si coincide;
   - si difiere, reporta **que archivos** cambiaron/faltan/sobran (diff por path+hash) y sale con codigo != 0.
   - Determinista; no usa red ni claves.
3. Golden `examples/release_verify_cases` + CI.

## 3. Tests (golden determinista, sin red)

1. `generate_manifest` de un arbol fijo => manifiesto canonico esperado (con `sbom_hash` estable).
2. `verify_release` con el manifiesto de su propio arbol => **OK** (exit 0).
3. Modificar un archivo del arbol => `verify_release` **FALLA** (exit != 0) y lista ese archivo como diferente.
4. Anadir/quitar un archivo => detectado (sobra/falta).
5. Determinismo: `generate_manifest` dos corridas (mismo commit/timestamp) => byte-identico.
6. Neutralidad: el manifiesto lista rutas/hashes/version axes (no contenido ni estado de dominio); gates verdes.

## 4. Fuera de alcance

- Firma criptografica / claves (F7.4). Provenance/atestacion (F7.3). Integracion al flujo de release y docs
  completas (F7.5). Cualquier secreto. Cambios al contrato de coordinacion o al turn schema.

## 5. SemVer

- MINOR (herramienta aditiva de release engineering; no cambia contrato ni nucleo).

## 6. Secuencia

Tras F7.2: F7.3 (provenance) -> F7.4 (firma, probable DECISION) -> F7.5 (docs+integracion). Promover de a una.
