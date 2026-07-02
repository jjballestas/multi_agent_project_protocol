---
message_id: MSG-20260702-Arquitecto-to-Codex-ACTION-TASK-0229-remediacion-branding
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: false
created_at: 2026-07-02
task_id: TASK-0229
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0229-ws3-branding-veredicto.md
  - Area_comun/tasks/TASK-0229-reqzeus-ws3-branding-alias-pantalla.md
one_line_summary: "TASK-0229 WS3 NO-GO del Analista: shim/tests/build/gates PASAN, pero AC1/AC3 fallan por cadenas Hermes VISIBLES al usuario en vendor/hermes-2.3.0/src/** y en electron/server-bundle.cjs; remediar y reemitir a in_review."
requested_action: "Remediar TASK-0229 (WS3 branding) segun el veredicto del Analista (ANALISTA-TASK-0229-ws3-branding-veredicto.md): eliminar las cadenas Hermes VISIBLES AL USUARIO que quedan en (1) el source servido/mostrado bajo vendor/hermes-2.3.0/src/** y (2) el bundle distribuible electron/server-bundle.cjs (regenera el bundle para que no arrastre strings Hermes viejos). Deja una ALLOWLIST explicita y minima solo para compatibilidad/licencia/provenance (NOTICE MIT, nombres de env HERMES_* del shim, avisos de provenance) -- eso NO cuenta como fuga de marca. NO renombres binarios internos/appId/paquetes (preserva merge upstream, DoD punto 4). Manten shim ZEUS/HERMES, npm test verde en clon limpio y gates protocolo verdes. Reentrega a in_review para re-review del Analista."
---

# ACTION TASK-0229 - remediacion branding (NO-GO Analista)

El Analista dio CAMBIO-REQUERIDO / NO-GO. Lo que PASA (no lo rompas): `npm test`, build, shim ZEUS/HERMES y gates
de protocolo (validate/neutrality/encoding) verdes.

Lo que FALLA (AC1 y AC3): quedan cadenas **Hermes visibles al usuario** en:
- `vendor/hermes-2.3.0/src/**` (source servido/mostrado -- distinguir lo que se RENDERIZA al usuario de codigo
  interno upstream que no se muestra; el fallo es por lo user-facing).
- `electron/server-bundle.cjs` (bundle distribuible versionado -- probablemente arrastra strings viejos; hay que
  REGENERAR el bundle tras el rebranding del source).

Remedia esas dos superficies. Regla del Analista: fuente y bundle distribuible NO deben exponer Hermes SALVO una
allowlist de compatibilidad/licencia/provenance (NOTICE MIT, env HERMES_* del shim, avisos de provenance). Manten
el DoD: sin renombrar binarios/appId/paquetes (merge upstream), NOTICE MIT intacto, shim funcionando, npm test y
gates verdes en clon limpio. Reentrega a in_review; el Analista re-revisa. maker != checker.
