---
decision_id: DECISION-0023
title: Politica de firma de releases (autenticidad de la cadena de suministro, sin secretos en el repo)
status: proposed
date: 2026-06-07
ratified_at: null
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0001, DECISION-0019, DECISION-0021, DECISION-0017]
phase: P2
---

# DECISION-0023 - Politica de firma de releases (F7.4)

> PROPOSED (2026-06-07). Borrador en personal/Claude/, adelantado para revision del operador. F7.4 (firma) es
> la unica rebanada de Fase 7 que toca politica de seguridad/release => requiere DECISION + aprobacion humana
> antes de implementarse/encolarse. Off-by-default, sin secretos en el repo, vendor-neutral. SemVer MINOR.

## Contexto

Fase 7 da SBOM (F7.1), integridad por contenido (F7.2) y procedencia (F7.3). Falta **autenticidad**: que un
adoptante pueda verificar que el release fue firmado por un emisor legitimo y no manipulado. Firmar implica
material de clave, lo que choca con el boundary "no secretos en el repo". Esta decision fija como hacerlo sin
violar ese boundary.

## Decision

1. **Que se firma:** el digest del release (`manifest.sbom_hash` / la atestacion de provenance), no los
   archivos uno a uno. Una firma cubre todo el release via su hash.
2. **Sin secretos en el repo (boundary innegociable, AGENTS.md sec.4):** las claves privadas/material de firma
   son **locales del emisor / del CI**, NUNCA commiteadas (analogo a DECISION-0021 para el wrapper real).
   La firma producida (publica) y la clave PUBLICA de verificacion si pueden acompanar el release.
3. **Off-by-default + opt-in:** firmar es un paso explicito del emisor al publicar; `verify_release` valida la
   firma **solo si** se le provee el material publico/firma. Sin material => verifica integridad (F7.2) sin
   autenticidad, como hasta F7.3.
4. **Vendor-neutral + backend configurable:** el mecanismo de firma es un backend configurable (p.ej.
   minisign/cosign/gpg/sigstore en uso real, via comando provisto, analogo a los presets del wrapper). El repo
   NO fija un proveedor unico ni incrusta claves.
5. **Determinismo en golden/CI sin secretos:** los golden usan un **backend fixture determinista** (p.ej.
   HMAC-SHA256 con una clave de PRUEBA explicitamente no-secreta, marcada como fixture) para probar
   firma+verificacion sin red ni claves reales. CI nunca usa claves reales. El backend real (asimetrico) se
   ejercita fuera de los golden.
6. **Verificacion:** `verify_release --signature <f> --pubkey <k>` valida que la firma cubre el `sbom_hash`
   del release con la clave publica dada; OK/FALLA con exit code. Falla cerrada (sin material valido => no
   afirma autenticidad).

## Aplicacion

- Implementacion = Fase 7.4 (SPEC + TASK aparte): `scripts/sign_release.py` (backend configurable, fixture en
  golden) + `verify_release` extendido (validar firma) + golden con clave fixture + docs. NO commitear claves.
- Nota en README_INSTANCIACION / PACKAGE_VERSIONING: como firmar/verificar un release; las claves son del
  emisor, no del repo.

## Versionado y neutralidad (DECISION-0001)

- Aditivo, off-by-default, opt-in => **MINOR**. Neutral de dominio. Mantiene el boundary "no secretos".

## Pendiente antes de ACCEPTED

- [ ] Aprobacion del operador (politica de firma = boundary de seguridad/release).
- [ ] Confirmar backend(s) real(es) preferido(s) (p.ej. cosign/minisign/gpg) para documentar, sin atar el core.
- [ ] Numero de decision confirmado (0023) + enlazar en PROJECT_STATE#decisions al ratificar.
