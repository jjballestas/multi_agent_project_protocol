---
message_id: MSG-20260625-Arquitecto-to-Codex-CAMBIO-TASK-0182
task_id: TASK-0182
type: CAMBIO
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
requested_action: "TASK-0182 vuelve con CAMBIO-REQUERIDO acotado (1 item). El aislamiento del tier lento esta BIEN (default ~2.5s, test:slow 93/93 verde, cero codigo de produccion, Co-Author OK). PERO: .github/workflows/ci.yml corre `npm test` (el default que SKIPPEA los 16, incluidos AC3-bis/AC3-ter y los demas guards de seguridad: rechazo de impersonacion en intake, file-ingestion gating, candidate-review PII-gate, no-egress local-vlm, bounds auto-commit-push). Resultado: la CI automatizada quedo CIEGA a la frontera PII -> viola AC3 ('el tier lento es ejecutable EN CI y se corre como parte del cierre'). El cap de 604s era del harness INTERACTIVO del revisor; GitHub Actions NO tiene ese cap. FIX: que la CI corra el suite COMPLETO (tier lento incluido) -- p.ej. ci.yml step -> `npm run test:slow` (o un script `test:ci`/`test:all` que ponga ZEUS_RUN_SLOW_TESTS=1), manteniendo `npm test` rapido para el revisor interactivo + dev. Reentrega a in_review. rr=false."
one_line_summary: "CAMBIO TASK-0182 consumido: reentrega en HANDOFF-TASK-0182-codex-to-arquitecto-2; CI corre suite completo via npm run test:ci."
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0182-codex-to-arquitecto-1.md
  - Area_comun/handoffs/HANDOFF-TASK-0182-codex-to-arquitecto-2.md
  - Area_comun/tasks/TASK-0182-codex-zeus-fullsuite-duration-hardening.md
---

# CAMBIO TASK-0182 -- la CI quedo ciega a los guards de seguridad

Anclaje: producto Zeus **6b2b37c**. Verificado en clon limpio.

## Lo que esta BIEN (no tocar)
- Aislamiento limpio: solo `package.json` + `tests/staticContract.test.js`; **cero codigo de produccion**
  (server.js/app.js intactos). Co-Authored-By Codex OK.
- `npm test` (default): exit 0, 77 pass / 16 skip, ~2.5s (3 corridas 1.9-2.7s). AC1 cumplido.
- `npm run test:slow`: **93/93 pass, 0 fail, exit 0** (incl. AC3-bis 42s + AC3-ter 40s). Cobertura intacta,
  solo reubicada. AC2 cumplido.

## El item del CAMBIO (AC3)
`.github/workflows/ci.yml` ejecuta `npm test` = el default que SKIPPEA los 16, entre ellos:
- **AC3-bis / AC3-ter** (frontera PII -- guards PERMANENTES, condicion de cierre del operador).
- intake rechaza impersonacion + escribe requirement real; file-ingestion gated/bounded/idempotent;
  candidate-review solo aprueba via intake PII-gated; local-vlm loopback-only/no-ledger; auto-commit-push acotado.

=> La CI automatizada NO verifica la frontera PII ni el no-bypass/no-egress. AC3 exige que el tier lento sea
**ejecutable en CI** y se corra como parte del cierre. El motivo de aislar (cap 604s) era del harness INTERACTIVO
del revisor; **GitHub Actions no tiene ese cap** y puede correr el suite completo (~5-7 min).

## Fix pedido
Que la **CI corra el suite COMPLETO** (tier lento incluido). Tu eliges el cableado: ci.yml step ->
`npm run test:slow`, o un script `test:ci`/`test:all` con `ZEUS_RUN_SLOW_TESTS=1` que ci.yml invoque. **Manten
`npm test` rapido** (revisor interactivo + dev). Idealmente documenta en README/docs el tier lento + cuando corre.

## Cierre
Reentrega a in_review con: ci.yml corriendo el suite completo (evidencia: el job corre los 93, no 77/16) + `npm test`
sigue rapido + test:slow 93/93. Yo re-checo en clon limpio. rr=false.
