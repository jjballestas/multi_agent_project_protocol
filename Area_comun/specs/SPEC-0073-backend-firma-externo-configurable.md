---
spec_id: SPEC-0073-backend-firma-externo-configurable
task_id: TASK-0099
type: design
status: ready
created_at: 2026-06-10
author: Claude (arquitecto)
linked_decisions: [DECISION-0023, DECISION-0021, DECISION-0001, DECISION-0006]
relates_to: [TASK-0099, SPEC-0061]
---

> Implementa el backend de firma REAL configurable que DECISION-0023 sec.4 ya manda (hoy sign/verify son
> fixture-only). Habilita firmas de autenticidad reconocibles por terceros (cosign-keyless como
> configuracion del emisor). Aditivo, off-by-default, vendor-neutral. NO toca runtime ni defaults.
> NO requiere decision nueva: DECISION-0023 cubre la politica.

# Diseno - Backend de firma externo configurable (uso real)

## 1. Objetivo

Permitir firmar el digest del release (`manifest.sbom_hash`) con un **backend externo configurable** (un
comando provisto por el emisor, analogo a los presets del wrapper LLM), y verificar esa firma, manteniendo
el core **vendor-neutral** y el CI **determinista sin red ni claves**. Resuelve que hoy `sign_release.py`
(linea 46) y `verify_release.py` (linea 49) **rechazan cualquier backend != fixture-hmac-sha256**, por lo que
no existe un camino de autenticidad real. Backend objetivo del emisor: **cosign keyless** (sigstore: identidad
OIDC + log de transparencia Rekor), pero NO se hardcodea: es la configuracion del operador.

## 2. Alcance

- Un backend "external-command" en `sign_release.py` y `verify_release.py` (config por comando, sin secretos
  en el repo).
- Esquema `protocol_release_signature.v1` extendido para portar la salida del backend externo (firma/bundle +
  identidad + issuer) conservando `subject_digest = manifest.sbom_hash`.
- Golden determinista con un backend fake/recorded (sin red, sin claves reales).
- Docs: receta de verificacion para terceros (identidad + issuer + comando), en el reporte de release y
  README_INSTANCIACION.md.

## 3. No-alcance

- NO hardcodear cosign/sigstore en el core (neutralidad: el repo trae la CAPACIDAD; el emisor cablea el
  backend). minisign/gpg/otros deben encajar por el mismo mecanismo.
- NO commitear material de clave/identidad real (boundary DECISION-0023 sec.2). Keyless no tiene clave
  privada que guardar; bundle + cert son publicos.
- NO red ni claves reales en CI/golden. El path real es del emisor/adoptante.
- NO cambia el runtime, ni los defaults del template, ni el contenido del release v1.1.0 (el `sbom_hash` ya
  esta fijado; firmarlo despues es valido).

## 4. Diseno

### 4.1 Esquema de firma (extension aditiva de protocol_release_signature.v1)

Campos: `schema_version`, `subject_digest` (= manifest.sbom_hash, inalterado), `backend` (id del backend,
p.ej. "external-cosign"), `key_id` o `identity` (identidad/issuer publica del firmante), `signature`
(firma o referencia al bundle). El fixture existente sigue valido (backend "fixture-hmac-sha256").

### 4.2 sign_release.py

- Nuevo modo backend "external-command": el emisor provee un COMANDO (via flag/preset, analogo a
  `llm_cli_presets`) que recibe el `subject_digest` (o el blob `manifest.json`) y devuelve firma/bundle.
- `sign_release` invoca el comando (subprocess), recoge la salida y la envuelve en el esquema v1 con
  `subject_digest`, `backend`, `identity`, `signature/bundle`. Material/identidad NUNCA al repo.
- El fixture HMAC permanece para golden/CI.

### 4.3 verify_release.py

- Simetrico: backend "external-command" que invoca el comando de verificacion del emisor (p.ej.
  `cosign verify-blob --certificate-identity <id> --certificate-oidc-issuer <issuer> --bundle <bundle>
  manifest.json`).
- Chequea: `signature.subject_digest == manifest.sbom_hash`; el backend declarado coincide; el comando de
  verificacion retorna exito. Si falla cualquiera -> error claro.
- Sin firma/material -> sigue validando integridad+procedencia (off-by-default; no afirma autenticidad).

### 4.4 Neutralidad

cosign es la CONFIGURACION del operador, no codigo del core. El core expone un mecanismo de comando
generico; cualquier backend (minisign/gpg/cosign/sigstore) encaja proveyendo su comando. Sin proveedor
mandado (DECISION-0023 sec.4).

## 5. Invariantes (no negociables)

1. El fixture HMAC sigue funcionando (golden/CI); byte-equivalente donde aplique.
2. `subject_digest` siempre == `manifest.sbom_hash`; una firma cubre todo el release via ese hash.
3. Sin secretos en el repo; claves/identidad son locales del emisor/CI (DECISION-0021/0023).
4. CI/golden deterministas, sin red ni claves reales (backend fake/recorded).
5. Off-by-default: sin firma, verify_release valida integridad+procedencia, no autenticidad.
6. Vendor-neutral: ningun proveedor hardcodeado.

## 6. Tests (golden determinista, sin red)

- Firma+verifica con un backend fake/recorded (external-command simulado) -> round-trip OK; `subject_digest`
  ligado a `manifest.sbom_hash`.
- backend declarado != backend de verificacion -> rechazo.
- `subject_digest` != `manifest.sbom_hash` -> rechazo.
- Sin material/comando -> verify integridad-only (no afirma autenticidad), sin error.
- El fixture HMAC pre-existente -> sigue verde. Paridad .py/.ps1.

## 7. SemVer y neutralidad

MINOR (aditivo, off-by-default, opt-in, reversible). Neutral de dominio. DECISION-0023/0001.

## 8. Configuracion del backend (emisor)

- El comando del backend se provee por flag CLI (`--backend external-cosign --sign-cmd <...>` /
  `--verify-cmd <...>`) o por un preset en config analogo a `llm_cli_presets`, a decidir en implementacion
  (preferible: flags CLI explicitos para no persistir nada del backend en el repo).
- Para cosign keyless el emisor corre `cosign sign-blob --bundle ... manifest.json` (OIDC en navegador) y
  `cosign verify-blob --certificate-identity <id> --certificate-oidc-issuer <issuer> --bundle ...`.

## 9. Docs (lo que habilita el reconocimiento por terceros)

Anadir al reporte de release y a README_INSTANCIACION.md la **receta de verificacion** publica: identidad
del firmante, issuer OIDC, y el comando exacto de verificacion. Sin esa receta publicada, un tercero no
puede reconocer la firma. (Keyless: verify consulta Rekor -> requiere red, o bundle offline con `--offline`.)

## 10. Criterios de completitud / validacion / cierre

- Completitud: backend external-command en sign+verify; esquema extendido; golden (fake/recorded) verde;
  fixture intacto; paridad .ps1; docs con la receta de verificacion.
- Validacion: golden 100% verde; encoding/neutralidad verdes; sin secretos; determinismo CI.
- Cierre: TASK-0099 -> done, ratificado adversarialmente (neutralidad + sin-secretos + determinismo + binding
  subject_digest). Habilita la Fase 2 (el emisor firma v1.1.0 con cosign keyless y publica la receta).

## 11. Decisiones / preguntas

- NO requiere decision nueva (DECISION-0023 sec.4 ya manda el backend configurable). Unica eleccion de
  implementacion: backend por flags CLI (recomendado, nada del backend se persiste) vs preset en config.
  Decide el implementador con ratificacion del arquitecto.
