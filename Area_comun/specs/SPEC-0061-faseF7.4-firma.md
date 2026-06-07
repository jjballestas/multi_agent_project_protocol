---
spec_id: SPEC-0061-faseF7.4-firma
task_id: TASK-0075
type: implementation
status: ready
created_at: 2026-06-07
author: Claude (arquitecto)
linked_decisions: [DECISION-0023, DECISION-0021, DECISION-0001, DECISION-0019]
relates_to: [SPEC-0057, SPEC-0059, SPEC-0060]
---

> PROMOVIDA por Claude (2026-06-07) tras cerrar F7.3 y promover DECISION-0023 al ledger. F7.4: firma del release,
> off-by-default, SIN secretos en el repo, vendor-neutral, golden con clave fixture (no-secreta).

# SPEC-0061 - Fase 7.4: firma de releases (autenticidad)

## 1. Objetivo

Dar AUTENTICIDAD al release: firmar su digest (`manifest.sbom_hash`) y permitir que `verify_release` valide
la firma con material publico. Conforme a DECISION-0023: off-by-default, claves del emisor (NUNCA en el repo),
backend configurable, golden con clave fixture.

## 2. Alcance (aditivo, off-by-default, sin secretos)

1. **`scripts/sign_release.py`** (+ paridad/delegacion `.ps1`): firma el digest del release.
   - Entrada: `--manifest <path>` (usa `sbom_hash`) o `--digest`, `--key <material>` (ruta a clave local del
     emisor, NUNCA commiteada), `--backend <id>` (configurable).
   - Salida: artefacto de firma canonico `{ subject_digest, backend, signature, key_id/pubkey_ref }` (ASCII).
   - **Backend fixture determinista** integrado para golden/CI: HMAC-SHA256 con clave de PRUEBA explicita
     (marcada `fixture`, no-secreta) => firma+verificacion reproducibles sin red ni claves reales. Backends
     reales (cosign/minisign/gpg) via comando externo, NO ejercitados en golden.
2. **`verify_release` extendido**: `--signature <f> --pubkey/--key <material> [--backend <id>]` valida que la
   firma cubre el `sbom_hash` del release; **OK/FALLA** con exit code. Falla cerrada: sin material valido NO
   afirma autenticidad (mantiene el comportamiento de integridad F7.2 si no se pide firma).
3. **Sin secretos**: el repo NO contiene claves privadas reales; solo la clave fixture de PRUEBA (claramente
   etiquetada) para golden. Scan de secretos limpio. Docs: las claves reales son del emisor/CI.
4. Golden `examples/release_sign_cases` + CI (solo backend fixture).

## 3. Tests (golden determinista, sin red, sin claves reales)

1. `sign_release` (backend fixture) sobre un manifiesto => artefacto de firma canonico esperado; determinista.
2. `verify_release --signature --pubkey` (fixture) con firma valida => **OK** (exit 0).
3. Firma sobre un digest que no coincide con el release / firma alterada => **FALLA** (exit != 0).
4. `verify_release` sin material de firma => sigue validando integridad (F7.2) sin afirmar autenticidad.
5. Sin secretos: scan de secretos/neutralidad limpio; el repo no gana claves privadas reales.
6. Determinismo + paridad py/.ps1.

## 4. Fuera de alcance

- Mandatar un proveedor de firma unico (queda configurable). Commitear claves reales (prohibido). Integracion
  completa al flujo de release + docs extensas (F7.5). Cambios al turn schema.

## 5. SemVer

- MINOR (aditivo, off-by-default, opt-in; mantiene el boundary "no secretos"). DECISION-0023.

## 6. Secuencia

Tras F7.4: F7.5 (docs + integracion al flujo de release: como firmar/verificar; cierra Fase 7).
