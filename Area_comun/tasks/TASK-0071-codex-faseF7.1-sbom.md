---
id: TASK-0071
owner: Codex
status: in_review
type: implementation
priority: normal
created_at: 2026-06-07
updated_at: 2026-06-07
depends_on: []
relates_to: [TASK-0064]
phase: P2
spec_id: Area_comun/specs/SPEC-0057-fase7-release-engineering.md
linked_decisions: [DECISION-0001, DECISION-0019]
execution_pipeline: [scripts/generate_sbom.py (+ paridad o delegacion .ps1) que genera un SBOM canonico del paquete: inventario determinista de archivos FUENTE del paquete (globs explicitos; excluir runtime/state, runtime/runs, .git, __pycache__ y efimeros) con ruta posix + sha256 + tamano por archivo; cabecera con los 4 ejes de version (protocol/runtime/schema/profile) + commit + timestamp PROVISTOS como argumento (sin reloj/red); salida JSON canonica ASCII/sin BOM (orden estable); golden examples/sbom_cases + CI]
acceptance_criteria: [generate_sbom.py produce SBOM canonico (rutas+sha256+tamano + 4 ejes + commit/timestamp provistos); determinista (dos corridas identicas => byte-identico); cambio de un archivo => cambia su hash; excluye runtime/state, runtime/runs, .git, __pycache__; el SBOM lista rutas/hashes (no contenido, no estado de dominio) => neutralidad limpia; paridad o delegacion .ps1; golden + validador/encoding/neutralidad/prune py/ps verdes]
expected_output: scripts/generate_sbom.py (+ .ps1) genera SBOM canonico determinista del paquete + golden examples/sbom_cases; gates verdes.
test_plan: [golden sbom: arbol fijo => SBOM esperado; determinismo byte-identico; archivo cambiado => hash cambia; exclusiones (state/runs/.git/pycache); neutralidad del SBOM; paridad py/ps; gates verdes]
question_to_resolve: ninguna (alcance F7.1 acotado en SPEC-0057). Firma/provenance/verificacion de release publicado NO entran (F7.2-F7.4). Si requiere secretos o tocar el turn schema => blocked + pregunta.
closure_criterion: SBOM canonico determinista del paquete (rutas+sha256+version axes+commit/timestamp provistos) + exclusiones + golden + paridad/delegacion .ps1 + gates verdes; handoff autocontenido; release atomico (DECISION-0018).
closure_criteria: [scripts/generate_sbom.py (+ .ps1) determinista/canonico; inventario con sha256+tamano+4 ejes+commit/timestamp provistos; exclusiones state/runs/.git/pycache; SBOM neutral (rutas/hashes); golden examples/sbom_cases + CI; paridad o delegacion .ps1; validador/encoding/neutralidad/prune py/ps verdes; handoff autocontenido; release atomico (DECISION-0018)]
---

# TASK-0071 - Fase 7.1: SBOM determinista del paquete

> Primera rebanada de Fase 7 (release engineering), aprobada por el operador. Promovida a ready en ventana
> segura tras cerrar TASK-0070 y re-aplicar la activacion sombra. Ver SPEC-0057.

## Contexto

Fase 7 endurece la cadena de suministro del paquete (SBOM + provenance + firma + verificacion). F7.1 es la
base: un SBOM determinista (inventario verificable de archivos + 4 ejes de version + hashes), sin firma aun.
Aditivo, neutral, sin secretos.

## Alcance (ver SPEC-0057 sec.3)

1. `scripts/generate_sbom.py` (+ paridad/delegacion `.ps1`): SBOM canonico del paquete.
2. Inventario determinista de archivos FUENTE (excluye runtime/state, runtime/runs, .git, __pycache__) con
   ruta posix + sha256 + tamano; cabecera con 4 ejes de version + commit + timestamp PROVISTOS.
3. Salida JSON canonica (ASCII/sin BOM, orden estable). Golden `examples/sbom_cases` + CI.

## Restricciones

- **Aditivo, determinista** (sin reloj/red; commit/timestamp provistos). **Sin secretos** (el SBOM lista
  rutas/hashes, no contenido ni estado). **Neutralidad** (no incrusta estado de dominio). ASCII (DECISION-0012).
- Firma/provenance/verificacion de release publicado NO entran (F7.2-F7.4). Cambio incompatible => `blocked`.
- **Handoff autocontenido**; **release atomico** (DECISION-0018); anti-colision (DECISION-0020).

## Nota

Primera de 5 rebanadas de Fase 7 (F7.1 SBOM -> F7.2 manifiesto+verify -> F7.3 provenance -> F7.4 firma
[probable DECISION] -> F7.5 docs+integracion). Promovida de a una.

## Progreso

- 2026-06-07 Codex reclamo la tarea tras GO de Claude. Anomalia previa sobre ledger queda resuelta por la
  regularizacion posterior (TASK_INDEX + GO presentes). Writer-vivo en modo sombra: drift warning esperado.
- 2026-06-07 Codex entrega a `in_review`: `generate_sbom.py` + wrapper ps1 + golden `examples/sbom_cases` +
  CI; gates verdes con warning de drift esperado por modo sombra.
