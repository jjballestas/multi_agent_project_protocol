---
spec_id: SPEC-0063-cutover-submit-intent-codex-loop
task_id: TASK-0077
type: implementation
status: ready
created_at: 2026-06-08
author: Claude (arquitecto)
linked_decisions: [DECISION-0022, DECISION-0017, DECISION-0020]
relates_to: [SPEC-0062, TASK-0076, TASK-0072]
---

> Cutover (rebanada de adopcion) de la migracion al escritor-unico. Habilita que el LAZO AUTONOMO DE CODEX deje
> de editar los `*.json` a mano y emita TODAS sus transiciones del ledger via `submit_intent --intents`. SHADOW:
> enforce/authoritative siguen OFF (sin flip). El flip es la rebanada de ACTIVACION posterior (re-genesis vivo +
> GO + rollback ensayado). Claude hace su lado (mandato en AGENTS.md/TASK_PROTOCOL + adopcion propia) en paralelo.

# SPEC-0063 - Cutover: el lazo de Codex adopta submit_intent --intents

## 1. Objetivo

Que el lazo autonomo de Codex emita sus transiciones del ledger (auto-claim, handoff-release, cierres) **solo**
via `submit_intent --intents` (transaccional, TASK-0076), no por edicion directa de `TASK_INDEX/PROJECT_STATE/
CLAIMS`. Es el prerrequisito para encender `enforce+authoritative` sin romper el lazo (si Codex siguiera editando
a mano, una vez en enforce su proxima edicion hard-failearia).

## 2. Alcance (aditivo, shadow, sin flip)

1. **Mapear cada transicion del lazo de Codex a una transaccion de intents:**
   - auto-claim: `claim`(acquire) + `task_status`(ready->in_progress) en una transaccion.
   - handoff-release: `task_status`(in_progress->in_review) + `claim`(release) [+ `task_upsert` si aplica] atomico.
   - (otras: block, etc. segun el ciclo.)
2. **Helper/receta** `runtime/ledger_ops.py` (o documentada) que construya estos sobres de intents comunes a
   partir de parametros, para reducir errores al armar el JSON de `--intents`.
3. **Golden** `examples/cutover_loop_cases`: una secuencia tipica del lazo (acquire -> in_progress -> in_review
   + release) aplicada via `submit_intent --intents` sobre un fixture con **drift 0** (clean base) -> materializa
   el ledger esperado, drift 0, idempotente. Demuestra la ruta sin tocar el repo vivo.
4. **Paridad** `.ps1` donde aplique + CI.

## 3. Fuera de alcance

- **NO** encender `enforce`/`authoritative` ni re-genesisar el repo vivo (eso es la ACTIVACION, rebanada
  siguiente: re-genesis vivo + flip + rollback ensayado, con GO del operador ya otorgado pero ejecutada por el
  arquitecto tras verificar ambos lados).
- El mandato en AGENTS.md/TASK_PROTOCOL (submit_intent = unico write-path bajo enforce) lo redacta el arquitecto.
- Mailbox sigue fuera de submit_intent (archivos bajo claim, SPEC-0062).

## 4. Invariantes

1. Off/shadow => byte-equivalente; sin registro de enforce, nada cambia.
2. submit_intent exige drift 0 -> el golden parte de un fixture clean-base (re-genesis del fixture), no del vivo.
3. Atomicidad todo-o-nada (heredada de TASK-0076). Determinista; sin secretos; neutral.
4. Reversible.

## 5. Cierre (DoD)

El lazo de Codex tiene una ruta PROBADA (golden, drift 0) para emitir auto-claim y handoff-release via
`submit_intent --intents`; helper/receta + golden cutover_loop_cases + paridad .ps1 + CI; SIN flip; gates verdes;
handoff autocontenido; release atomico (DECISION-0018); staging por paths (DECISION-0020).

## 6. Secuencia

Tras SP-0063 + el lado de Claude (mandato + adopcion): ACTIVACION = re-genesis del repo vivo (drift 0) + flip
enforce+authoritative + ensayo de rollback (flags->false restaura sombra). Ambos lados deben usar submit_intent
ANTES del flip.
