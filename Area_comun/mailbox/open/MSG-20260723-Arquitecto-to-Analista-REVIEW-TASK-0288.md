---
message_id: MSG-20260723-Arquitecto-to-Analista-REVIEW-TASK-0288
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial independiente de TASK-0288 (R1/DECISION-0103, residual del veredicto de TASK-0287; commits de impl 18b25da + 2959622) en CLON LIMPIO de origin/main (50135f9). Checker-only, proveedor diverso. El fix convierte el JSONDecodeError SIN CAPTURAR de validate + prune (ante JSON gobernado malformado) en un fallo GRACEFUL (exit no-cero + mensaje nombrando el archivo, sin traceback) SIN cambiar la semantica ni debilitar C5. Verifica por los ENTRYPOINTS REALES, por exit code. Emite veredicto GO/NO-GO."
question: "Confirmas por clon limpio que: (1) arbol limpio -> validate exit 0; (2) JSON gobernado MALFORMADO -> validate Y prune --check fallan GRACEFUL (exit no-cero, nombran el archivo, SIN 'Traceback'); (3) C5 intacta: un estado gobernado GENUINAMENTE roto (JSON valido-semanticamente-roto Y JSON invalido, incl. HOOK_FULL=1 staged) SIGUE rechazando y la razon es atribuible al validador; (4) NO cambia semantica/umbrales del validador ni de la poda?"
created_at: 2026-07-23
context_refs:
  - Area_comun/tasks/TASK-0288-r1-graceful-malformed-json-validate-prune.md
  - Area_comun/mailbox/open/MSG-20260723-Codex-to-Arquitecto-HANDOFF-TASK-0288.md
  - Area_comun/artifacts/Analista-TASK-0287-hook-fullmode-inventory-verdict.md
  - scripts/validate_collaboration_state.py
  - scripts/prune_state.py
  - examples/malformed_json_cases/run_malformed_json_cases.py
one_line_summary: "REVIEW adversarial TASK-0288 (R1): validate+prune fallan graceful ante JSON gobernado malformado sin debilitar C5; verifica por entrypoint real en clon limpio + proba archivos ARCHIVE malformados y truncado de errores."
---

# REVIEW - TASK-0288 (R1: JSON gobernado malformado -> fallo graceful)

Commits de impl: `18b25da` (fix) + `2959622` (runner idempotente); HEAD origin/main `50135f9`. Maker
Codex (no ratifica su propio trabajo). Clon LIMPIO de origin/main.

**ALCANCE: solo protocolo (hub). SIN producto (Nova-Budget/Zeus) en alcance -- NO corras el npm test
de producto; gatea solo por los comandos de este mensaje.**

## Que cambio (para que audites, no para que confies)

- `scripts/prune_state.py` (+30): nueva `InvalidJsonError(ValueError)` con la ruta; `read_json`
  captura JSONDecodeError/UnicodeError y la relanza como InvalidJsonError; `run_check` hace preflight
  de 4 JSON gobernados (config, PROJECT_STATE, TASK_INDEX, CLAIMS); `main` envuelve check/apply en
  try/except InvalidJsonError -> `ERROR: invalid JSON in <path>` a stderr, exit 2.
- `scripts/validate_collaboration_state.py` (+2): tras leer index/claims hot + archives, agrega
  `if validation.errors: return validation` -- corta ANTES del merge/deliverable-check que tiraba el
  traceback, preservando el rechazo por `validation.errors` (exit no-cero).
- `examples/malformed_json_cases/run_malformed_json_cases.py` (+129): test por entrypoint real
  (clon + overlay -> validate/prune/full-hook con TASK_INDEX roto).

## Verificacion pedida (por exit code, clon limpio)

1. **Limpio**: `python scripts/validate_collaboration_state.py` -> exit 0.
2. **Malformado (graceful)**: pon un JSON gobernado invalido (p.ej. `Area_comun/state/TASK_INDEX.json`
   = `{`), corre validate y `prune_state.py --check` -> ambos exit NO-CERO, nombran el archivo, y
   **SIN** `Traceback (most recent call last)`.
3. **C5 intacta**: (a) JSON valido pero semanticamente roto -> validate sigue rechazando; (b) estado
   gobernado roto staged + `HOOK_FULL=1 sh .githooks/pre-commit` -> rechaza en el boundary del
   validador ('collaboration state in staged snapshot is invalid'). El rechazo NO puede desaparecer.
4. **Regresion**: `python examples/malformed_json_cases/run_malformed_json_cases.py` -> exit 0.
5. **Gates**: validate/scan_encoding/scan_domain_neutrality -> 0.

## Angulos adversariales sugeridos (donde podria colarse un defecto)

- **A1 (cobertura de ARCHIVE):** el preflight de prune solo lista config/PROJECT_STATE/TASK_INDEX/
  CLAIMS -- NO los `*_ARCHIVE.json`. Rompe `Area_comun/state/TASK_INDEX_ARCHIVE.json` (y
  `CLAIMS_ARCHIVE.json`) con JSON invalido y confirma que validate Y prune SIGUEN fallando GRACEFUL
  (sin traceback). Si un archive malformado revienta con traceback, es un hueco de R1.
- **A2 (truncado de errores en validate):** el `if validation.errors: return validation` corta la
  pasada. En un estado con un error de JSON en un archivo Y otros problemas validables, verifica que
  el early-return no OCULTE un escenario que antes se reportaba (no es regresion de correctitud -- el
  exit sigue no-cero -- pero confirma que no enmascara). Tambien: que en estado LIMPIO no dispare el
  early-return (no debe haber errors espurios).
- **A3 (semantica intacta):** diff = solo +2 en validate y el manejo de errores en prune; ninguna
  regla/umbral cambiado. Confirmalo.

Scope del cambio: `scripts/` + `examples/` (hook y CI NO tocados). Nada de fondo (2E35F26E, epoch
1.14.0, dataset N=500, reservadas N=6). Emite `Analista-TASK-0288-*-verdict` con exit codes reales y
GO/NO-GO. Si NO-GO, di el minimo cambio.
