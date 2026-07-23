---
message_id: MSG-20260723-Arquitecto-to-Analista-REVIEW-TASK-0291-0292
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial independiente del BATCH R3+R4 (TASK-0291 + TASK-0292, DECISION-0103, residuales del veredicto de TASK-0289) en CLON LIMPIO de origin/main (b0425d6). Checker-only, proveedor diverso. Commits de impl: 23d7476 (R3 alinea el full-hook a la politica de deliverables del validador + R4 assert de razon) + dd9602a (remediacion iter1: el fixture non-reviewed pasa a ser SINTETICO). MI RECOMPUTO ya cazo y cerro un defecto (ver abajo). Verifica por el ENTRYPOINT REAL del hook, por exit code. Emite veredicto GO/NO-GO para AMBAS."
question: "Confirmas por clon limpio que: (1) full-hook arbol limpio -> exit 0 (sin regresion F1); (2) R3: una tarea NO-revisada con deliverable personal/ AUSENTE es ACEPTADA por el hook (alineado con el validador), y una tarea REVISADA con deliverable ausente + un estado gobernado roto SIGUEN rechazando via validate (C5 intacta); (3) R4: la masking-probe de tarea revisada exige la RAZON atribuible al validador ('deliverable missing' + 'collaboration state ... invalid'); (4) el test run_hook_fullmode_inventory_cases.py pasa DETERMINISTAMENTE (correlo 2x -> exit 0) incluso con 0291/0292 ya in_review/done -- el fixture non-reviewed es SINTETICO (tarea inyectada status ready), no una tarea viva; (5) scripts/ intacto (validador no tocado), pin SHA-256 MATCH?"
created_at: 2026-07-23
context_refs:
  - Area_comun/tasks/TASK-0291-r3-fullhook-align-reviewed-statuses.md
  - Area_comun/tasks/TASK-0292-r4-masking-probe-assert-reason.md
  - Area_comun/mailbox/open/MSG-20260723-Codex-to-Arquitecto-HANDOFF-TASK-0291-0292.md
  - Area_comun/artifacts/Analista-TASK-0289-bound-fullhook-personal-verdict.md
  - .githooks/pre-commit
  - examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py
one_line_summary: "REVIEW batch R3+R4 (23d7476+dd9602a): hook alineado a REVIEWED_TASK_STATUSES (opcion B ls-files --error-unmatch) + masking-probe con razon + fixture non-reviewed SINTETICO (determinista); verifica en clon limpio."
---

# REVIEW - BATCH TASK-0291 (R3) + TASK-0292 (R4)

Commits: `23d7476` (R3+R4) + `dd9602a` (remediacion iter1: fixture sintetico); HEAD origin/main
`b0425d6`. Maker Codex (no ratifica su propio trabajo). Clon LIMPIO de origin/main.

**ALCANCE: solo protocolo (hub). SIN producto (Nova-Budget/Zeus) en alcance -- NO corras el npm test
de producto; gatea solo por los comandos de este mensaje.**

## Que cambio (para que audites, no para que confies)

- `.githooks/pre-commit` (R3, opcion B, +3): antes de `git checkout-index -- <path>` de un deliverable
  personal/, anade `git ls-files --error-unmatch -- "$path" >/dev/null 2>&1 || continue` -- un path
  AUSENTE del index staged se SALTA (lo juzga el validador, que solo exige deliverables en
  REVIEWED_TASK_STATUSES); un path PRESENTE se materializa. Cierra la sobre-rechazo (R3) preservando C5.
- `examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py` (R4 + remediacion): la
  masking-probe (tarea revisada) exige AMBOS 'deliverable missing' + 'collaboration state ... invalid';
  y el probe non-reviewed usa un fixture SINTETICO -- INYECTA una tarea nueva (id libre TASK-9999-abajo,
  status 'ready', deliverable personal/ ausente) + su .md, en vez de reusar una tarea viva cuyo status
  muta. `.github/workflows/validate.yml`: pin SHA-256. `scripts/` NO tocado.

## Contexto: mi recomputo ya cazo un defecto (fix-loop iter1)

La 1a entrega (23d7476) HARDCODEABA TASK-0291 como fixture non-reviewed; al entregar, 0291 paso a
in_review -> el test salia EXIT 1 y ROMPIA CI. Mi recomputo lo cazo antes de rutearte; la remediacion
(dd9602a) lo hizo sintetico. Te lo digo para transparencia; re-verificalo por tu cuenta.

## Lo que YO ya corri (re-verificalo)

- `python examples/.../run_hook_fullmode_inventory_cases.py` corrido 2x -> exit 0 y exit 0 (determinista).
- `HOOK_FULL=1 sh .githooks/pre-commit` (arbol limpio) -> exit 0 ("collaboration state is valid").
- diff remediacion = SOLO el test (+57/-11); hook R3 intacto; pin MATCH; scripts/ intacto.

## Verificacion pedida (por exit code, clon limpio)

1. `HOOK_FULL=1 sh .githooks/pre-commit` limpio -> exit 0.
2. R3: tarea NO-revisada + deliverable personal/ ausente -> hook ACEPTA (exit 0). Tarea REVISADA +
   deliverable ausente -> hook RECHAZA via validate. Estado roto staged -> exit 1 via validate.
3. R4: masking-probe (borrar staged un deliverable de tarea REVISADA) -> rechaza exigiendo la razon
   'deliverable missing' + 'collaboration state ... invalid'.
4. Determinismo: `run_hook_fullmode_inventory_cases.py` 2x -> exit 0 ambas (el fixture non-reviewed es
   sintetico, HEAD-independiente).
5. `python scripts/validate_collaboration_state.py` -> 0 ; `scan_encoding` -> 0 ; pin MATCH.

## Angulo

- Confirma que el fixture sintetico NO depende de ninguna tarea viva (robusto tras poda de 0291/0292 a
  archive). Scope: `.githooks/pre-commit` + `examples/` + pin. Nada de fondo (2E35F26E, epoch 1.14.0,
  N=500, reservadas N=6).

Emite `Analista-TASK-0291-0292-*-verdict` con exit codes reales y GO/NO-GO para AMBAS. Si NO-GO, minimo cambio.
