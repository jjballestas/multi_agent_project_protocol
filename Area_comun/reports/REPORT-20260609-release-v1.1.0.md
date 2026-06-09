# Session report - Release v1.1.0 (runtime-authoritative writer + SA.4 pilot + adoption blocker closed)

- Date: 2026-06-09
- Phase: P2 (Adopcion y expansion)
- Process status: closed (pendiente sign-off del operador para el tag)
- Ratification: ratified by agents (Claude architect/reviewer) + pendiente human sign-off del tag
- Release commit: 928e5dd7c3b0dce0a997a3112e5cd99acdac7226
- Version axes: protocol_version 1.1.0 - runtime_version 0.11.0 - turn_schema 1.2.0

## 1. In One Sentence

v1.1.0 (MINOR, aditivo, reversible) empaqueta el escritor-unico event-sourced en vivo
(enforce+authoritative), los intents de submit_intent, el guard anti-false-secure, el piloto acotado de
autonomia supervisada SA.4 VALIDADO end-to-end con el invoker real y luego DE-ARMADO a off-by-default, el
fix gap-8 del claim-acquire, el hardening tempfile/ACL del write-path, el bridge Agent Teams A+B, y la
DECISION-0028 (postura B) que cierra el ultimo bloqueante de adopcion.

## 2. What Was Done

- **Escritor-unico VIVO:** event_state.enforce=true luego authoritative=true en la instancia viva; el
  event log es fuente de verdad, el estado se reconstruye por replay(log), y editar a mano
  Area_comun/state/*.json hard-failea por drift (gate B.3). Toda transicion por submit_intent. Reversible
  (flags->false).
- **Intents nuevos:** project_narrative (next_actions/risks/open_questions) y protocol_prune; prune
  reencauzado bajo enforce.
- **Guard event_state_config_error:** rechaza la cadena incoherente (authoritative=>enforce=>materialize=>
  enabled) en validador + submit_intent + apply; mata el false-secure.
- **SA.4 (autonomia supervisada):** lock-lift off-by-default + piloto acotado. El piloto se VALIDO
  end-to-end con el invoker real codex exec (orquestador adquiere el claim, codex edita la nota de prosa
  objetivo, gate ACCEPT, claim-lifecycle limpio sin orphan, checkpoint tras turno 1) y se DE-ARMO de vuelta
  a off-by-default (el default que se publica).
- **gap-8 fix (TASK-0093):** el paso claim del orquestador adquiere el claim del owner ruteado por
  submit_intent antes del adapter; idempotente con pre-claim; conflicto rechaza pre-adapter; libera el
  claim adquirido en outcomes terminales y de rechazo (sin orphan).
- **Hardening tempfile/ACL (TASK-0094):** el write-path autoritativo usa tempdirs repo-local de ACL
  heredada (no %TEMP% 0o700 que bloqueaba el token sandboxed); materializacion byte-equivalente (mismo
  canonical_hash). Runbook operativo documentado.
- **Bridge Agent Teams A+B** (gate-enforcement + audit append-only), off-by-default; Capa C diferida.
- **DECISION-0028 (postura B):** enforce ES el mecanismo de escritor-unico; authoritative es el marcador
  declarativo del modo; sin teeth propias; el guard de TASK-0086 mata el false-secure. Cierra TASK-0087
  (ultimo bloqueante de ADOPCION).

## 3. SDD Summary

- Specs: SPEC-0064 (autonomia supervisada), SPEC-0065 (bridge), SPEC-0066 (intents), SPEC-0067 (guard),
  SPEC-0070 (gap-8 claim-acquire), SPEC-0071 (hardening tempfile/ACL).
- Tasks done: TASK-0083 (bridge A+B), TASK-0085 (intents), TASK-0086 (guard), TASK-0088 (lock-lift),
  TASK-0089/0090 (wrapper vendor-neutral + resolucion cross-platform), TASK-0091 (objetivo del piloto
  SA.4), TASK-0092 (invoker codex), TASK-0093 (gap-8), TASK-0094 (hardening), TASK-0087 (postura B).
- Acceptance: ratificacion adversarial de Claude en cada cierre; smoke real + re-pilot SA.4 verdes;
  byte-equivalencia de materializacion; drift 0 sostenido.
- Test plans: ver seccion 5.
- Deviations: ninguna. Follow-ups menores registrados (TASK-0095 commits de turno self-consistentes,
  TASK-0096 run_id unico por corrida).

## 4. Decisions

- DECISION-0022 (runtime escritor autoritativo) - cableado en vivo.
- DECISION-0025 (bridge Agent Teams) - Capas A+B; Capa C diferida.
- DECISION-0026 (memoria post-commit) - regla de oro.
- DECISION-0027 (activacion SA.4 piloto) - piloto acotado validado y luego de-armado.
- DECISION-0028 (postura B) - enforce=mecanismo, authoritative=marcador; cierra el bloqueante de adopcion.

## 5. Quality Gates

- Goldens: 43+ suites verdes (incl. release tooling sbom/provenance/sign/verify, runtime_loop,
  supervised_autonomy, real_adapter, intent_flow, materialize/cross_fs/replay, runtime_turn).
- Validador colaboracion: valid. Neutralidad de dominio: 0 hallazgos. Encoding: limpio.
- Drift: 0 (replay == hot). Worktree limpio.
- Smoke real + re-pilot SA.4: ACCEPT, claim-lifecycle limpio, sin orphan, sin re-auth, checkpoint tras
  turno 1; luego SA.4 DE-ARMADO (verificado subprocess_multiturn_allowed=False).

## 6. Cadena de release verificable (SBOM -> manifiesto -> provenance -> firma)

Generada de forma determinista (commit + timestamp provistos), salida en dist/v1.1.0/:

- SBOM: dist/v1.1.0/sbom.json (747 archivos del paquete; ejes de version protocol 1.1.0 / runtime 0.11.0
  / turn_schema 1.2.0 / profile dotnet_enterprise 0.1.0).
- Manifiesto: dist/v1.1.0/manifest.json
  - sbom_hash:     92113b4a882dc32feebc9d24e197f936f2f3bdd57158cb382a62c88d6b7e2fac
  - manifest_hash: 2026dde03bc6ab52e78290111415c5adafcd4c9e2828431669c9f65aff54ac64
  - commit:        928e5dd7c3b0dce0a997a3112e5cd99acdac7226
- Provenance: dist/v1.1.0/provenance.json (builder ci:release; subject.digest.sha256 == manifest.sbom_hash).
- Verificacion:
  - Integridad (dist/v1.1.0/verify.integrity.json): ok=true, diff vacio (changed/extra/missing []).
  - Provenance (dist/v1.1.0/verify.provenance.json): ok=true.
- **Firma: DIFERIDA (release integrity-only).** sign_release.py del core solo soporta el backend fixture
  (fixture-hmac-sha256), que NO debe usarse para releases reales (DECISION-0023 sec.4). La firma autentica
  requiere el backend REAL del emisor con material de clave que NUNCA entra al repo. Por la politica
  off-by-default (RELEASE_ENGINEERING.md), este release publica integridad + procedencia verificadas y NO
  afirma autenticidad. La firma se anade cuando el emisor provea el backend/material; el digest a firmar es
  manifest.sbom_hash = 92113b4a882dc32feebc9d24e197f936f2f3bdd57158cb382a62c88d6b7e2fac.

## 7. Ratificacion

Ratificado adversarialmente por Claude (arquitecto/reviewer): gates verdes, drift 0, cadena de release
integra y con procedencia verificada, neutralidad limpia, defaults del template intactos (off-by-default),
enforce/authoritative intactos, SA.4 y Capa C OFF. PENDIENTE: sign-off explicito del operador para el tag
v1.1.0 (MINOR no estrictamente gateado por DECISION-0001, pero empaqueta la activacion de autonomia).

## 8. Estado seguro post-release

enforce/authoritative ON (intactos) - SA.4 (real_invoker + supervised_autonomy) OFF - Capa C (team_bridge)
OFF - drift 0 - sin claims activos. Aditivo, MINOR, reversible. Sin secretos en el repo.
