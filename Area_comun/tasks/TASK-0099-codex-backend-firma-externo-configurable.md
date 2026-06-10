---
id: TASK-0099
owner: Codex
status: done
type: implementation
priority: normal
created_at: 2026-06-10
updated_at: 2026-06-10
depends_on: []
relates_to: [SPEC-0073, SPEC-0061, TASK-0075, DECISION-0023]
phase: P2
spec_id: Area_comun/specs/SPEC-0073-backend-firma-externo-configurable.md
linked_decisions: [DECISION-0023, DECISION-0021, DECISION-0001, DECISION-0006]
deliverables:
  - scripts/sign_release.py
  - scripts/verify_release.py
  - scripts/sign_release.ps1
  - scripts/verify_release.ps1
  - examples/release_sign_cases/run_release_sign_cases.py
  - README_INSTANCIACION.md
relevant_files:
  - scripts/sign_release.py
  - scripts/verify_release.py
  - scripts/sign_release.ps1
  - scripts/verify_release.ps1
  - examples/release_sign_cases/run_release_sign_cases.py
  - README_INSTANCIACION.md
blocked_by_questions: []
objective: (IMPLEMENTADOR, bajo SPEC-0073 / DECISION-0023 sec.4) Anadir un backend de firma "external-command" configurable a scripts/sign_release.py y scripts/verify_release.py para habilitar firmas de AUTENTICIDAD reconocibles por terceros (objetivo del emisor=cosign keyless, NO hardcodeado), conservando subject_digest = manifest.sbom_hash, el fixture HMAC intacto, y el core vendor-neutral. Hoy ambos scripts rechazan cualquier backend != fixture-hmac-sha256 (sign_release.py:46, verify_release.py:49) -> no existe camino de autenticidad real. Aditivo, MINOR, off-by-default; sin secretos; sin red en CI.
expected_output: (1) scripts/sign_release.py - backend "external-command": el emisor provee el comando de firma por FLAGS CLI (recomendado por SPEC-0073 sec.8/11: nada del backend se persiste en el repo), que recibe el subject_digest (o el blob manifest.json) y devuelve firma/bundle por stdout; sign_release lo envuelve en protocol_release_signature.v1 con {subject_digest, backend, key_id|identity, signature|bundle}; material/identidad NUNCA al repo. (2) scripts/verify_release.py - backend "external-command" simetrico: invoca el comando de verificacion del emisor (p.ej. cosign verify-blob --certificate-identity <id> --certificate-oidc-issuer <issuer> --bundle <bundle> manifest.json) y chequea subject_digest == manifest.sbom_hash + backend declarado coincide + el comando retorna exito; falla cerrada con error claro; sin firma/material sigue validando integridad+procedencia (off-by-default, no afirma autenticidad). (3) Esquema extendido aditivamente (sin romper el fixture): el fixture-hmac-sha256 sigue byte-equivalente. (4) Golden DETERMINISTA en examples/release_sign_cases/ con un backend fake/recorded (un script python local que simula firma/verificacion, SIN red, SIN claves reales): round-trip OK + binding subject_digest==manifest.sbom_hash; backend-mismatch -> rechazo; subject_digest-mismatch -> rechazo; sin material/comando -> integridad-only sin error; fixture HMAC pre-existente sigue verde; paridad .py/.ps1. (5) Paridad scripts/sign_release.ps1 + scripts/verify_release.ps1 (delegan al .py; pasan los nuevos flags). (6) Docs: receta de verificacion publica (identidad del firmante + issuer OIDC + comando exacto) en README_INSTANCIACION.md y en el patron del reporte de release.
question_to_resolve: Q1 (SPEC-0073 sec.8/11) backend por FLAGS CLI explicitos (recomendado: --backend external-command --sign-cmd/--verify-cmd, nada se persiste) vs preset en config analogo a llm_cli_presets; el implementador decide con ratificacion del arquitecto, preferencia por flags. Q2 transporte del subject_digest al comando (stdin vs placeholder {digest}/{input} en el template del comando vs blob manifest.json): elegir el mas neutral y ergonomico para envolver cosign/minisign/gpg; documentarlo. Si el esquema v1 no admite la salida del backend sin romper el fixture -> blocked + nota al arquitecto (NO debilitar el binding subject_digest ni la neutralidad).
closure_criterion: backend external-command operativo en sign+verify; esquema protocol_release_signature.v1 extendido sin romper el fixture (fixture HMAC byte-equivalente, golden pre-existente verde); golden fake/recorded 100% verde (round-trip + binding subject_digest + backend-mismatch + subject-mismatch + integridad-only-sin-material); paridad .py/.ps1; neutralidad 0 (ningun proveedor hardcodeado; cosign solo en docs/ejemplos como configuracion del emisor); encoding limpio; sin secretos (scan limpio; el repo no gana claves/identidad reales); determinismo en CI (sin red); docs con la receta de verificacion publica; handoff con evidencia. Ratificacion adversarial del arquitecto: neutralidad + sin-secretos + binding subject_digest==manifest.sbom_hash + determinismo. NO re-armar SA.4 ni piloto; NO runtime flip.
sdd_required: true
---

# TASK-0099 - Backend de firma externo configurable (uso real, DECISION-0023 sec.4)

> READY+GO (Claude 2026-06-10, bajo SPEC-0073, GO del operador). Aditivo MINOR off-by-default.
> Implementa el backend de firma REAL configurable que DECISION-0023 sec.4 ya manda (hoy sign/verify son
> fixture-only). NO requiere decision nueva (DECISION-0023 cubre la politica). NEUTRAL innegociable;
> sin secretos; claim + staging por paths. enforce/authoritative intactos; SA.4/Capa C OFF; NO runtime flip.

## Alcance (SPEC-0073 sec.2, 4)

Backend "external-command" en scripts/sign_release.py + scripts/verify_release.py (config por flags CLI, sin
persistir nada del backend en el repo), envolviendo/verificando protocol_release_signature.v1 con
subject_digest = manifest.sbom_hash. cosign keyless es la CONFIGURACION del emisor, NO hardcodeado
(neutralidad: el core trae la capacidad de comando generico; cualquier backend minisign/gpg/cosign/sigstore
encaja proveyendo su comando). El fixture HMAC permanece intacto para golden/CI. Ver el frontmatter de esta
task y SPEC-0073 para el detalle (esquema, invariantes sec.5, tests sec.6, docs sec.9).

## Restricciones (duras)

- Invariantes de SPEC-0073 sec.5 (no negociables): fixture HMAC sigue verde y byte-equivalente;
  subject_digest siempre == manifest.sbom_hash; sin secretos en el repo; CI/golden deterministas sin red ni
  claves reales (backend fake/recorded); off-by-default; vendor-neutral (ningun proveedor hardcodeado).
- Aditivo, MINOR, reversible. Paridad .py/.ps1. enforce+authoritative ON: todo cambio de estado por
  submit_intent; 1 commit/turno con rutas explicitas. Si el esquema v1 no admite la salida del backend sin
  romper el fixture -> blocked + nota al arquitecto. NO re-armar SA.4 ni piloto.
