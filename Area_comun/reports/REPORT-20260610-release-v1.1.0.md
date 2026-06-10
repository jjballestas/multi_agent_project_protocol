# Session report - Release v1.1.0 FIRMADO (cadena verificable + autenticidad cosign keyless)

- Date: 2026-06-10 (re-cut firmado; corte previo integrity-only 2026-06-09)
- Phase: P2 (Adopcion y expansion)
- Process status: closed (firmado y verificado; pendiente solo el tag git con sign-off del operador)
- Ratification: ratified by agents (Claude architect/reviewer) + firma keyless del operador (sign-off humano)
- Release commit (manifest.commit): 04436c3c93f9aaddd7167cf2f7d4a4529e7ebe4d
- Version axes: protocol_version 1.1.0 - runtime_version 0.11.0 - turn_schema 1.2.0

## 1. In One Sentence

v1.1.0 (MINOR, aditivo, reversible) empaqueta el escritor-unico event-sourced en vivo
(enforce+authoritative), los intents de submit_intent, el guard anti-false-secure, el piloto acotado de
autonomia supervisada SA.4 VALIDADO end-to-end con el invoker real y luego DE-ARMADO, el fix gap-8 del
claim-acquire, el hardening tempfile/ACL, el bridge Agent Teams A+B, la DECISION-0028 (postura B), la guia
humana operativa neutral + su generador HTML determinista, y el backend de firma external-command
vendor-neutral que habilita la AUTENTICIDAD real del release (cosign keyless).

## 2. What Was Done

- **Escritor-unico VIVO:** event_state.enforce=true luego authoritative=true; el event log es fuente de
  verdad, el estado se reconstruye por replay(log), editar a mano Area_comun/state/*.json hard-failea por
  drift (gate B.3). Toda transicion por submit_intent. Reversible (flags->false).
- **Intents nuevos:** project_narrative y protocol_prune; prune reencauzado bajo enforce.
- **Guard event_state_config_error:** rechaza la cadena incoherente
  (authoritative=>enforce=>materialize=>enabled); mata el false-secure.
- **SA.4 (autonomia supervisada):** lock-lift off-by-default + piloto acotado validado end-to-end con el
  invoker real codex exec y luego DE-ARMADO a off-by-default (el default publicado).
- **gap-8 fix (TASK-0093):** el paso claim del orquestador adquiere el claim ruteado por submit_intent
  antes del adapter; idempotente; libera en outcomes terminales y de rechazo (sin orphan).
- **Hardening tempfile/ACL (TASK-0094):** write-path autoritativo con tempdirs repo-local de ACL heredada;
  materializacion byte-equivalente. Runbook documentado.
- **Bridge Agent Teams A+B** (gate-enforcement + audit append-only), off-by-default; Capa C diferida.
- **DECISION-0028 (postura B):** enforce ES el mecanismo de escritor-unico; authoritative es el marcador
  declarativo. Cierra TASK-0087 (ultimo bloqueante de ADOPCION).
- **Guia humana operativa neutral + generador HTML determinista (TASK-0037/0098, SPEC-0072):** plantilla
  master de 21 secciones (Area_comun/protocol/HUMAN_GUIDE.template.md) + scripts/generate_human_guide.py
  (+ .ps1, stdlib-only, .md->.html byte-deterministico, --check de drift, validacion de esquema, tier-aware,
  sin red/JS/CDN); fuente de verdad = .md, HTML = artefacto generado (banner GENERADO-NO EDITAR). La guia
  dogfooding de la raiz (HUMAN_GUIDE.md/.html) y el ejemplo (examples/human_guide_instance/) se generan via
  el generador.
- **Backend de firma external-command vendor-neutral (TASK-0099, SPEC-0073, DECISION-0023 sec.4):**
  sign_release.py/verify_release.py ganan el backend external-command (config por flags CLI, nada del backend
  persiste en el repo) que envuelve/verifica el esquema protocol_release_signature.v1 conservando
  subject_digest == manifest.sbom_hash y el fixture HMAC byte-equivalente. Ningun proveedor hardcodeado; el
  binding del digest se chequea ANTES de ejecutar el comando; golden fake/recorded determinista (sin red, sin
  claves). El SBOM ahora excluye dist/** (anadir signature/bundle a dist/ no cambia el sbom_hash firmado).

## 3. SDD Summary

- Specs: SPEC-0064, SPEC-0065, SPEC-0066, SPEC-0067, SPEC-0070, SPEC-0071, SPEC-0072 (guia humana),
  SPEC-0073 (backend firma external-command).
- Tasks done: TASK-0083/0085/0086/0088/0089/0090/0091/0092/0093/0094/0087 + TASK-0037 (guia humana),
  TASK-0098 (generador), TASK-0099 (backend firma external-command).
- Acceptance: ratificacion adversarial de Claude en cada cierre; smoke real + re-pilot SA.4 verdes;
  byte-equivalencia de materializacion; drift 0 sostenido; firma del release verificada end-to-end.
- Deviations: ninguna. Follow-ups menores: TASK-0095/0096 (proposed).

## 4. Decisions

- DECISION-0022 (runtime escritor autoritativo), DECISION-0025 (bridge A+B; C diferida),
  DECISION-0026 (memoria post-commit), DECISION-0027 (SA.4 piloto), DECISION-0028 (postura B),
  DECISION-0023 sec.4 (firma de release vendor-neutral; implementada por TASK-0099).

## 5. Quality Gates

- Goldens: suite completa verde (incl. release tooling sbom/manifest/provenance/sign/verify, human_guide,
  runtime_loop, supervised_autonomy, real_adapter, intent_flow, materialize/cross_fs/replay, runtime_turn).
- Validador colaboracion: valid. Neutralidad de dominio: 0 hallazgos. Encoding: limpio.
- Drift: 0 (replay == hot). Worktree limpio. prune --check: verde (ledger compactado).

## 6. Cadena de release verificable (SBOM -> manifiesto -> provenance -> FIRMA cosign keyless)

Generada de forma determinista sobre el HEAD estable (commit + timestamp fijos), salida en dist/v1.1.0/:

- SBOM: dist/v1.1.0/sbom.json (757 archivos del paquete; **excluye dist/** por diseno). Ejes de version
  protocol 1.1.0 / runtime 0.11.0 / turn_schema 1.2.0.
- Manifiesto: dist/v1.1.0/manifest.json
  - sbom_hash:  0083c1c9a5bd4f6f568bbc6988b0ac9003518ab854feb01f9b1ae7814ddcb8e6
  - commit:     04436c3c93f9aaddd7167cf2f7d4a4529e7ebe4d
  - timestamp:  2026-06-10T00:00:00Z
- Provenance: dist/v1.1.0/provenance.json (builder ci:release; subject.digest.sha256 == manifest.sbom_hash).
- **FIRMA: cosign keyless (sigstore), AUTENTICIDAD VERIFICADA.**
  - Backend: external-command (TASK-0099); archivo de firma: dist/v1.1.0/signature.json
    (schema protocol_release_signature.v1; signature-field = bundle).
  - Bundle sigstore: dist/v1.1.0/cosign.bundle.json
    (mediaType application/vnd.dev.sigstore.bundle.v0.3+json).
  - subject_digest firmado == manifest.sbom_hash (0083c1c9...).
  - Identidad del firmante: john.ballestas@gmail.com
  - Issuer OIDC: https://accounts.google.com
  - Transparencia (Rekor): logIndex 1777945271 - integratedTime 1781087006 -
    logId keyId wNI9atQGlz+VWfO6LRygH4QUfY/8W4RFwiT5i5WRbamY9PQ=  (kind hashedrekord 0.0.1).
    Entrada: https://search.sigstore.dev/?logIndex=1777945271
- **Verificacion (ok:true GLOBAL = integridad + procedencia + autenticidad):**
  - Integridad (dist/v1.1.0/verify.integrity.json): ok=true, diff vacio (changed/extra/missing []), 757 files.
  - Provenance (dist/v1.1.0/verify.provenance.json): ok=true.
  - cosign verify-blob directo: "Verified OK".
  - Cadena del protocolo (verify_release --backend external-command): ok=true GLOBAL, signature.ok=true,
    subject match=true.

### Receta de verificacion publica (reconocible por terceros)

```text
# 1) cosign directo (autenticidad):
cosign verify-blob --bundle dist/v1.1.0/cosign.bundle.json \
  --certificate-identity john.ballestas@gmail.com \
  --certificate-oidc-issuer https://accounts.google.com \
  dist/v1.1.0/manifest.json

# 2) cadena del protocolo (integridad + procedencia + autenticidad):
python scripts/verify_release.py --root . --manifest dist/v1.1.0/manifest.json \
  --signature dist/v1.1.0/signature.json --backend external-command \
  --verify-command "cosign verify-blob --bundle dist/v1.1.0/cosign.bundle.json \
    --certificate-identity john.ballestas@gmail.com \
    --certificate-oidc-issuer https://accounts.google.com {manifest}"
```

## 7. Ratificacion

Ratificado adversarialmente por Claude (arquitecto/reviewer): gates verdes, drift 0, cadena de release
integra + con procedencia + AUTENTICA (cosign keyless verificada end-to-end), neutralidad limpia, defaults
del template intactos (off-by-default), enforce/authoritative intactos, SA.4 y Capa C OFF, sin secretos en
el repo (la firma es keyless: no hay clave privada que guardar; bundle + cert son publicos). PENDIENTE:
unico paso restante = tag git v1.1.0 sobre el commit de release con sign-off del operador.

## 8. Estado seguro post-release

enforce/authoritative ON (intactos) - SA.4 (real_invoker + supervised_autonomy) OFF - Capa C (team_bridge)
OFF - drift 0 - sin claims activos - worktree limpio. Aditivo, MINOR, reversible. Sin secretos en el repo.
