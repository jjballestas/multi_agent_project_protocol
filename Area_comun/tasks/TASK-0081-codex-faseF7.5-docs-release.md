---
id: TASK-0081
owner: Codex
status: in_review
type: documentation
priority: normal
created_at: 2026-06-08
updated_at: 2026-06-08
depends_on: [TASK-0071, TASK-0073, TASK-0074, TASK-0075]
relates_to: [TASK-0064]
phase: P2
spec_id: Area_comun/specs/SPEC-0057-fase7-release-engineering.md
linked_decisions: [DECISION-0001, DECISION-0019, DECISION-0023]
objective: Documentar la cadena de release de Fase 7 (SBOM -> manifiesto -> provenance -> firma) y como generarla/verificarla, cerrando Fase 7. Neutral, sin secretos.
expected_output: Doc de release (p.ej. Area_comun/protocol/RELEASE_ENGINEERING.md o seccion en PACKAGE_VERSIONING/README_INSTANCIACION) que explique generate_sbom -> generate_manifest -> generate_provenance -> sign_release y verify_release; como firmar/verificar un release; el backend real de firma (cosign/minisign/gpg via comando externo) es del emisor y NUNCA se commitea (DECISION-0023); la clave fixture es solo de golden. Enlaces desde README_INSTANCIACION.
question_to_resolve: ninguna (alcance F7.5 = documentacion de la cadena ya implementada). Si la doc revela un gap funcional => blocked + nota.
closure_criterion: doc de la cadena de release (SBOM/manifiesto/provenance/firma) + guia de generar/verificar + nota de backend real sin secretos (DECISION-0023) + enlaces desde README_INSTANCIACION; neutralidad/encoding verdes; gates verdes; handoff autocontenido; release atomico (DECISION-0018). Cierra Fase 7.
sdd_required: false
---

# TASK-0081 (F7.5) - Docs de la cadena de release (cierra Fase 7)

> IN_REVIEW (entregada por Codex 2026-06-08). Quinta y ultima rebanada de Fase 7. Documenta la cadena ya
> implementada (F7.1-F7.4); no agrega codigo funcional. Neutral, sin secretos. Ver SPEC-0057 (umbrella).

## Contexto

Fase 7 entrego en codigo: F7.1 SBOM (`generate_sbom`), F7.2 manifiesto + verify (`generate_manifest` /
`verify_release`), F7.3 provenance (`generate_provenance`), F7.4 firma (`sign_release` + `verify_release`
extendido). Falta documentar la cadena de extremo a extremo y como verificar un release. Eso cierra Fase 7.

## Alcance

1. Doc de la cadena: SBOM -> manifiesto (sbom_hash) -> provenance (subject.digest = sbom_hash) -> firma
   (sobre el digest). Como generar cada artefacto (comandos, entradas provistas: version axes, commit,
   timestamp) y como verificar (`verify_release`, `generate_provenance --verify`, firma con `--pubkey`).
2. Nota de seguridad (DECISION-0023): el backend real de firma (cosign/minisign/gpg via comando externo) y las
   claves son del emisor/CI y **NUNCA** se commitean; el repo solo lleva la clave fixture (etiquetada) de golden.
   Off-by-default; sin material de firma `verify_release` valida integridad (F7.2) sin afirmar autenticidad.
3. Enlaces desde `README_INSTANCIACION.md` (y/o `PACKAGE_VERSIONING.md`).

## Restricciones

- Neutral de dominio; ASCII (DECISION-0012); **sin secretos** (ni siquiera ejemplos con claves reales).
- Handoff autocontenido; release atomico (DECISION-0018); staging por paths (DECISION-0020).

## Nota

Cierra Fase 7. La activacion del escritor-unico y SA.4 (autonomia real) son pistas separadas, gateadas.

## Entrega Codex

- Agregado `Area_comun/protocol/RELEASE_ENGINEERING.md` con la cadena SBOM -> manifiesto -> provenance -> firma.
- Documentados comandos de generacion/verificacion para `generate_sbom`, `generate_manifest`,
  `generate_provenance`, `sign_release` y `verify_release`.
- Explicada la semantica de `manifest.sbom_hash`, `provenance.subject.digest.sha256` y
  `signature.subject_digest`.
- Incluida nota de seguridad DECISION-0023: backend real/material de firma pertenece al emisor o CI y nunca se
  commitea; fixture HMAC solo para golden.
- Enlaces agregados desde `README_INSTANCIACION.md` y `Area_comun/protocol/PACKAGE_VERSIONING.md`.
