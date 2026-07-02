---
handoff_id: HANDOFF-TASK-0237-codex-to-arquitecto-2
task_id: TASK-0237
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-02
product_repo: D:/Agentes/Zeus/Zeus-Aegis
product_head: ea3f52c
---

# TASK-0237 remediation handoff

## Resultado

Remediado el NO-GO del watchdog vendor. El script `vendor/hermes-2.3.0/scripts/zeus-aegis-f0-test.mjs` ahora usa
`taskkill /PID <pid> /T /F` de forma sincrona en Windows y sale con `124` inmediatamente despues de matar el arbol
cuando vence `ZEUS_AEGIS_TEST_HARD_TIMEOUT_MS`. Esto evita el caso refutado: imprimir el timeout y dejar Vitest
corriendo.

Commit producto:

- `ea3f52c fix(governance): hard exit vendor test watchdog`

## Evidencia producto

- `node --check scripts/run-product-test.mjs` PASS.
- `node --check vendor/hermes-2.3.0/scripts/zeus-aegis-f0-test.mjs` PASS.
- `git diff --check` PASS (solo warning LF->CRLF de Git en el archivo tocado).
- `ZEUS_AEGIS_TEST_HARD_TIMEOUT_MS=1 npm --prefix vendor/hermes-2.3.0 test` en repo local: exit `124` en 2.2s.
- `npm test` root 3/3 PASS:
  - run 1: 83 files / 562 tests, duration Vitest 215.52s.
  - run 2: 83 files / 562 tests, duration Vitest 194.68s.
  - run 3: 83 files / 562 tests, duration Vitest 134.95s.
- Clon limpio `C:/Users/johnb/AppData/Local/Temp/codex-0237-remediation-zeus-aegis-clean-ea3f52c` en HEAD
  `ea3f52c`: `ZEUS_AEGIS_TEST_HARD_TIMEOUT_MS=1 npm --prefix vendor/hermes-2.3.0 test` salio `124` en 2930ms y
  la inspeccion posterior de procesos con command line bajo ese clon reporto `survivors=0`.

## Evidencia protocolo

- `python scripts/scan_encoding.py --root .` PASS.
- `python scripts/scan_domain_neutrality.py --root .` exit 0.
- `python scripts/validate_collaboration_state.py --root .` PASS.
- Drift runtime: `has_drift=false`, byte-identical, `up_to_seq=3047` antes del cierre ledger.

## Notas de revision

- El cambio es deliberadamente minimo y solo toca el watchdog vendor. No cambia exclusiones de test ni cobertura.
- El root `npm test` sigue ejecutando el mismo vendor harness y conserva el 3/3 solicitado.
- maker=Codex; reviewer=Analista; checker=Arquitecto.
