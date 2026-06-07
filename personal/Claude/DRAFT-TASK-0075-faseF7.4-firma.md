---
id: TASK-0075
owner: Codex
status: draft
type: implementation
priority: normal
created_at: 2026-06-07
updated_at: 2026-06-07
depends_on: [TASK-0073, TASK-0074]
relates_to: [TASK-0062]
phase: P2
spec_id: Area_comun/specs/SPEC-0061-faseF7.4-firma.md
linked_decisions: [DECISION-0023, DECISION-0021, DECISION-0001]
execution_pipeline: [scripts/sign_release.py (+ paridad/delegacion .ps1): firma el digest del release (manifest.sbom_hash) con --key (material local, NUNCA commiteado) + --backend configurable; backend FIXTURE determinista HMAC-SHA256 con clave de prueba no-secreta para golden/CI; artefacto de firma canonico {subject_digest,backend,signature,key_id} ASCII/sin BOM; verify_release extendido --signature --pubkey/--key valida la firma sobre sbom_hash (OK/FALLA exit code, falla cerrada); SIN claves reales en el repo; golden examples/release_sign_cases (solo fixture) + CI]
acceptance_criteria: [sign_release (backend fixture) produce artefacto canonico determinista; verify_release valida firma fixture valida (exit 0) y FALLA (exit!=0) ante digest no coincidente o firma alterada; verify_release sin material de firma sigue validando integridad (F7.2) sin afirmar autenticidad; el repo NO gana claves privadas reales (solo la clave fixture etiquetada); scan de secretos/neutralidad limpio; paridad/delegacion .ps1; golden release_sign_cases + gates py/ps verdes; off-by-default]
expected_output: scripts/sign_release.py + verify_release extendido (+ .ps1) - firma del digest del release con backend configurable + fixture determinista para golden, sin secretos en el repo; gates verdes.
test_plan: [golden release_sign: sign fixture determinista; verify OK con firma valida; FALLA ante digest no coincidente/firma alterada; verify sin firma = integridad F7.2; sin secretos (scan limpio); determinismo + paridad py/ps]
question_to_resolve: ninguna (alcance F7.4 acotado en SPEC-0061 + DECISION-0023). Si exige commitear una clave real o un proveedor unico => blocked + pregunta.
closure_criterion: sign_release (backend configurable + fixture determinista) + verify_release valida firma sobre sbom_hash + sin secretos en el repo + golden + paridad .ps1; gates verdes; handoff autocontenido; release atomico (DECISION-0018).
closure_criteria: [scripts/sign_release.py (+ .ps1) backend configurable + fixture HMAC determinista; verify_release valida firma (OK/FALLA exit, falla cerrada; sin material = integridad F7.2); artefacto de firma canonico ASCII; NO claves reales commiteadas (solo fixture etiquetada); scan secretos/neutralidad limpio; golden examples/release_sign_cases (fixture) + CI; paridad/delegacion .ps1; gates py/ps verdes; handoff autocontenido; release atomico (DECISION-0018)]
---

# TASK-0075 - Fase 7.4: firma de releases (DRAFT)

> DRAFT en personal/Claude/. DECISION-0023 (politica de firma) ACCEPTED por el operador. Promover a ready
> cuando F7.3 (TASK-0074) cierre y DECISION-0023 este en el ledger (de a una, DECISION-0020). Ver SPEC-0061.
> Cuarta de 5 rebanadas de Fase 7.

## Contexto

F7.1 (SBOM) + F7.2 (integridad) + F7.3 (provenance) dan inventario, integridad y procedencia. F7.4 agrega
AUTENTICIDAD: firmar el digest del release y validarlo. Conforme a DECISION-0023: off-by-default, claves del
emisor NUNCA en el repo, backend configurable, golden con clave fixture no-secreta. Ver SPEC-0061.

## Alcance (ver SPEC-0061 sec.2)

1. `scripts/sign_release.py` (+ `.ps1`): firma `sbom_hash` con `--key` (local, no commiteado) + `--backend`;
   backend fixture HMAC determinista para golden.
2. `verify_release` extendido: `--signature --pubkey` valida firma; OK/FALLA (falla cerrada); sin material =>
   integridad F7.2.
3. Golden `examples/release_sign_cases` (solo fixture) + CI.

## Restricciones

- **Off-by-default, SIN secretos en el repo** (boundary, DECISION-0023/0021): solo clave FIXTURE etiquetada
  para golden; ninguna clave real commiteada. **Vendor-neutral** (backend configurable). Determinista; ASCII.
  Paridad/delegacion .ps1.
- NO mandatar proveedor unico; NO commitear claves reales => si hiciera falta, `blocked` + pregunta.
- **Handoff autocontenido**; **release atomico** (DECISION-0018); anti-colision (DECISION-0020, staging por paths).

## Nota

Cuarta de 5 rebanadas de Fase 7 (F7.1 done -> F7.2 -> F7.3 -> **F7.4 firma** -> F7.5 docs). Writer-vivo en
SOMBRA. Promovida de a una tras F7.3 + DECISION-0023 en ledger.
