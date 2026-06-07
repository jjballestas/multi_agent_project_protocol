---
id: TASK-0074
owner: Codex
status: ready
type: implementation
priority: normal
created_at: 2026-06-07
updated_at: 2026-06-07
depends_on: [TASK-0073]
relates_to: [TASK-0071]
phase: P2
spec_id: Area_comun/specs/SPEC-0060-faseF7.3-provenance.md
linked_decisions: [DECISION-0001, DECISION-0019]
execution_pipeline: [scripts/generate_provenance.py (+ paridad/delegacion .ps1): atestacion canonica SLSA-lite con subject{name,digest.sha256=manifest.sbom_hash} + builder.id + invocation{commit,process} + metadata{timestamp,schema} PROVISTOS (sin reloj/red); verificacion de consistencia (extiende verify_release o check propio): subject.digest == manifest.sbom_hash, error legible si no; salida JSON canonica ASCII/sin BOM; golden examples/provenance_cases + CI]
acceptance_criteria: [generate_provenance produce atestacion canonica con subject.digest=manifest.sbom_hash + builder/commit/process/timestamp provistos; determinista (byte-identico); consistencia OK cuando subject.digest coincide con sbom_hash y FALLA (exit!=0) cuando no; neutral (metadatos/hashes, no contenido), sin secretos, sin firma; paridad/delegacion .ps1; golden provenance_cases + validador/encoding/neutralidad py/ps verdes]
expected_output: scripts/generate_provenance.py (+ .ps1) atestacion SLSA-lite enlazada al manifiesto + verificacion de consistencia + golden; gates verdes.
test_plan: [golden provenance: atestacion canonica esperada; determinismo; consistencia OK/FALLA por subject.digest vs sbom_hash; neutralidad; paridad py/ps; gates verdes]
question_to_resolve: ninguna (alcance F7.3 acotado en SPEC-0060). Firma/claves NO entran (F7.4). Si requiere secretos o inferir del entorno => blocked + pregunta.
closure_criterion: generate_provenance (SLSA-lite, subject=sbom_hash, builder/invocation/metadata provistos) + verificacion de consistencia + determinista + golden + paridad .ps1; gates verdes; handoff autocontenido; release atomico (DECISION-0018).
closure_criteria: [scripts/generate_provenance.py (+ .ps1); atestacion canonica con subject.digest=manifest.sbom_hash; verificacion de consistencia (OK/FALLA + exit code); determinista (provistos); neutral/sin secretos/sin firma; golden examples/provenance_cases + CI; paridad/delegacion .ps1; validador/encoding/neutralidad py/ps verdes; handoff autocontenido; release atomico (DECISION-0018)]
---

# TASK-0074 - Fase 7.3: provenance / atestacion (SLSA-lite)

> Tercera de 5 rebanadas de Fase 7 (release engineering). Promovida tras cerrar F7.2. Ver SPEC-0060.

## Contexto

F7.1 (SBOM) + F7.2 (manifiesto+verify, integridad) dan inventario e integridad por contenido. F7.3 agrega
PROCEDENCIA: quien/commit/proceso construyo el release, enlazado por hash al manifiesto (subject = sbom_hash).
Da trazabilidad; la autenticidad (firma) es F7.4. Ver SPEC-0060.

## Alcance (ver SPEC-0060 sec.2)

1. `scripts/generate_provenance.py` (+ `.ps1`): atestacion SLSA-lite (subject/builder/invocation/metadata
   provistos; subject.digest.sha256 = manifest.sbom_hash).
2. Verificacion de consistencia (subject.digest == sbom_hash) en verify_release o check propio.
3. Golden `examples/provenance_cases` + CI.

## Restricciones

- **Aditivo, determinista** (builder/commit/timestamp provistos; sin reloj/red). **Neutral, sin secretos,
  sin firma** (F7.4). ASCII (DECISION-0012). Paridad/delegacion .ps1.
- Cambio incompatible o necesidad de secretos/claves => `blocked`.
- **Handoff autocontenido**; **release atomico** (DECISION-0018); anti-colision (DECISION-0020, staging por paths).

## Nota

Tercera de 5 rebanadas de Fase 7 (F7.1 done -> F7.2 -> **F7.3** -> F7.4 firma [DECISION-0023, requiere
aprobacion humana] -> F7.5 docs). Writer-vivo en SOMBRA. Promovida de a una.
