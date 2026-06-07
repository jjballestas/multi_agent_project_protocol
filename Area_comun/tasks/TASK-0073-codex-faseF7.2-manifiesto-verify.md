---
id: TASK-0073
owner: Codex
status: in_review
type: implementation
priority: normal
created_at: 2026-06-07
updated_at: 2026-06-07
depends_on: [TASK-0071]
relates_to: [TASK-0064]
phase: P2
spec_id: Area_comun/specs/SPEC-0059-faseF7.2-manifiesto-verify.md
linked_decisions: [DECISION-0001, DECISION-0019]
execution_pipeline: [scripts/generate_manifest.py (+ paridad/delegacion .ps1) que envuelve el SBOM de F7.1 en un manifiesto canonico con version_axes + commit + timestamp PROVISTOS + sbom_hash (sha256 canonico del SBOM) + file_count; scripts/verify_release.py (+ .ps1) que dado --root + --manifest recomputa el SBOM y compara contra sbom_hash (OK si coincide; si difiere lista archivos distintos/faltantes/sobrantes y exit!=0); salida JSON canonica ASCII/sin BOM; determinista (sin reloj/red/claves); golden examples/release_verify_cases + CI]
acceptance_criteria: [generate_manifest produce manifiesto canonico con sbom_hash estable + version_axes + commit/timestamp provistos; verify_release OK (exit 0) cuando el arbol coincide con su manifiesto; FALLA (exit!=0) y lista los archivos diferentes cuando se modifica/anade/quita un archivo; determinista (dos corridas byte-identicas); neutral (rutas/hashes, no contenido), sin secretos, sin claves/firma; paridad/delegacion .ps1; golden release_verify_cases + validador/encoding/neutralidad py/ps verdes]
expected_output: scripts/generate_manifest.py + scripts/verify_release.py (+ .ps1) - manifiesto canonico con sbom_hash + verify por integridad de contenido + golden; gates verdes.
test_plan: [golden release_verify: manifiesto de arbol fijo; verify OK con su manifiesto; verify FALLA al modificar/anadir/quitar archivo (lista diffs); determinismo byte-identico; neutralidad; paridad py/ps; gates verdes]
question_to_resolve: ninguna (alcance F7.2 acotado en SPEC-0059). Firma/provenance NO entran (F7.3/F7.4). Si requiere claves/secretos o tocar el turn schema => blocked + pregunta.
closure_criterion: generate_manifest (sbom_hash + version axes + commit/timestamp provistos) + verify_release (integridad por hash, lista diffs, exit code) + determinista + golden + paridad .ps1; gates verdes; handoff autocontenido; release atomico (DECISION-0018).
closure_criteria: [scripts/generate_manifest.py + scripts/verify_release.py (+ .ps1); manifiesto canonico con sbom_hash; verify OK/FALLA con diffs y exit code; determinista; neutral/sin secretos/sin claves; golden examples/release_verify_cases + CI; paridad/delegacion .ps1; validador/encoding/neutralidad py/ps verdes; handoff autocontenido; release atomico (DECISION-0018)]
---

# TASK-0073 - Fase 7.2: manifiesto de release + verify

## Contexto

Segunda rebanada de Fase 7. F7.1 (SBOM, done) dio el inventario determinista. F7.2 lo envuelve en un
**manifiesto** con un `sbom_hash` global y un comando **verify** que confirma por hash que un arbol coincide
con lo declarado (integridad de contenido; sin claves todavia, la firma es F7.4). Ver SPEC-0059.

## Alcance (ver SPEC-0059 sec.2)

1. `scripts/generate_manifest.py` (+ `.ps1`): manifiesto canonico = SBOM + version_axes + commit/timestamp
   provistos + `sbom_hash` (sha256 canonico).
2. `scripts/verify_release.py` (+ `.ps1`): `--root` + `--manifest` => recomputa SBOM, compara hash; OK (exit 0)
   o lista diffs y exit != 0.
3. Golden `examples/release_verify_cases` + CI.

## Restricciones

- **Aditivo, determinista** (sin reloj/red/claves; commit/timestamp provistos). **Neutral, sin secretos**
  (rutas/hashes, no contenido). ASCII (DECISION-0012). Paridad/delegacion .ps1.
- Firma/provenance NO entran (F7.3/F7.4). Cambio incompatible o necesidad de claves => `blocked`.
- **Handoff autocontenido**; **release atomico** (DECISION-0018); anti-colision (DECISION-0020): staging por
  paths (`git commit -- <paths>`).

## Nota

Segunda de 5 rebanadas de Fase 7 (F7.1 done -> **F7.2** -> F7.3 provenance -> F7.4 firma [probable DECISION]
-> F7.5 docs). Writer-vivo en SOMBRA (drift=warning esperado; edicion manual valida). Promovida de a una.
Codex autonomo: tomala cuando `ready`; GO por mailbox.
