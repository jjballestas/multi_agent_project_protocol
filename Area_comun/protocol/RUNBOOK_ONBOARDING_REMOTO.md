# RUNBOOK_ONBOARDING_REMOTO.md - Onboarding remoto de un participante a una instancia de metodologia

> Version: 1.0 (TASK-0234, [VISION-NOVA][F2.5]). Dominio-neutral. ASCII puro.
> Objetivo MEDIDO: onboarding operable <= 1 dia (alimenta HP6). Depende del harness distribuido (F2.3) y el ciclo e2e (F2.2).

## 0. Que es esto y para quien

Runbook para que un participante NUEVO (empleado o agente) que **NO construyo la instancia** se una
en FRIO a una instancia de metodologia distribuida (p.ej. la instancia Aegis) usando SOLO Git, y
opere 1 tarea de principio a fin. Objetivo: estar operando en <= 1 dia sin pasos manuales ocultos
ni dependencias de dev. La prueba de que esto funciona es la transferibilidad fuerte (un agente
ajeno a la construccion opera); la MEDICION real (cronometrar a un empleado fresco) es la replica
employee-run pre-registrada, posterior a este doc.

## 1. Precondiciones (lo que el operador provee)

- URL del remoto PRIVADO de la instancia (repo git propio de la instancia; no el hub).
- Credenciales de acceso al remoto (solo lectura/escritura segun rol).
- Tu identificador de participante `<id>` (el que tendras en el registro de agentes de la instancia).
- Git instalado. En Windows: `git config --global core.longpaths true` (rutas largas).

## 2. Paso a paso (onboarding)

En una instancia runtime-authoritative, `python runtime/protocol_replay.py
--check-drift` es el gate de deriva: registra `verdict`, `up_to_seq` y exit 0. La
deriva o un argumento desconocido deben salir distinto de cero.

1. **Clonar la instancia** (no el hub): `git clone -c core.longpaths=true <URL-remoto-privado> <carpeta>`.
2. **Leer en frio** (orden de arranque, sin asumir contexto): `AGENTS.md` (s.0 How to Start), luego
   `Area_comun/README.md`, `Area_comun/protocol/TASK_PROTOCOL.md`, y el estado en
   `Area_comun/state/` (PROJECT_STATE, TASK_INDEX, CLAIMS) + `Area_comun/mailbox/open/`.
3. **Configurar tu agente** (Git es el adapter; config COMMITEADA): copia/edita tu config en
   `.agents/<id>/config.json` segun el template de la instancia (workspaceRoot, adapter=git,
   committedConfig=true). NO se instalan adapters multi-IDE ni herramientas externas de memoria.
4. **Verificar que el canonico valida verde** antes de tocar nada:
   `python scripts/validate_collaboration_state.py` exit 0 (y encoding/neutralidad).
5. **Registrar tu alta** (si aplica) via el flujo gobernado de la instancia (submit_intent), no a mano.

## 3. Operar 1 tarea completa (ciclo distribuido, solo via Git)

Usa el ciclo pull -> escribir -> push INMEDIATO. Cada transicion del ledger va por
`submit_intent`, nunca editando `Area_comun/state/*.json` a mano.

### 3.1 Comandos concretos (copy-paste, ajusta <id>/<TASK>/rutas)

```bash
# 0. Sincroniza
git pull --rebase --autostash

# 1. CLAIM (ventana segura: sin claim de peer sobre tus rutas). El claim va ANIDADO bajo "claim",
#    y su scope DEBE incluir su propia fila CLAIMS.json#<claim_id> + los fragmentos que tocas.
cat > /tmp/tx-claim.json <<'JSON'
{"idempotency_key":"tx-<id>-claim-<TASK>","intents":[
 {"type":"claim","op":"acquire","claim":{
   "claim_id":"CLAIM-<fecha>-<id>-<TASK>","owner":"<id>","task_id":"<TASK>","status":"active",
   "scope":["Area_comun/state/CLAIMS.json#CLAIM-<fecha>-<id>-<TASK>",
            "Area_comun/state/TASK_INDEX.json#<TASK>",
            "Area_comun/state/PROJECT_STATE.json#active_tasks/<TASK>",
            "Area_comun/tasks/<TASK>-*.md"],
   "started_at":"<ISO-UTC>","updated_at":"<ISO-UTC>","expires_at":"<ISO-UTC+Nh>"}},
 {"type":"task_status","task_id":"<TASK>","from":"ready","to":"claimed","timestamp":"<ISO-UTC>"},
 {"type":"task_status","task_id":"<TASK>","from":"claimed","to":"in_progress","timestamp":"<ISO-UTC>"}
]}
JSON
python runtime/submit_intent.py --actor-id <id> --timestamp "<ISO-UTC>" \
  --commit "$(git rev-parse HEAD)" --intents /tmp/tx-claim.json --output -

# 2. PUSH INMEDIATO (tu claim se hace visible a los otros clones)
git add Area_comun/state/ runtime/state/ Area_comun/tasks/<TASK>-*.md
git commit -m "claim(<TASK>): ..."   # y Task-Id: <TASK> en el parrafo final si el gate de trailers esta activo
git push

# 3a. Escribe el HANDOFF autocontenido (ejemplo minimo validator-valid) ANTES de la tx (artifacts-before-claim):
cat > Area_comun/handoffs/HANDOFF-<TASK>-<id>-to-<checker>-1.md <<'MD'
---
handoff_id: HANDOFF-<TASK>-<id>-to-<checker>-1
task_id: <TASK>
from: <id>
to: <checker>
date: 2026-01-01
status: for_review
requires_response: no
acceptance_criteria_verified: yes
tests_run:
  - python scripts/validate_collaboration_state.py
spec_deviations:
  - none
decisions_referenced:
  - none
---
# Handoff <TASK>
## 1. Minimal Context / ## 2. What Was Done / ## 4. Acceptance Criteria Verified / ## 7. Requested Action
(contenido real; el turno termina con el envelope 7 campos como TEXTO FINAL, nunca un tool call)
MD

# 3b. ENTREGA: task_status in_progress->in_review + RELEASE del claim, en UNA tx atomica. tx-deliver.json COMPLETO:
cat > /tmp/tx-deliver.json <<'JSON'
{"idempotency_key":"tx-<id>-deliver-<TASK>","intents":[
 {"type":"task_status","task_id":"<TASK>","from":"in_progress","to":"in_review","timestamp":"<ISO-UTC>"},
 {"type":"claim","op":"release","claim":{
   "claim_id":"CLAIM-<fecha>-<id>-<TASK>","owner":"<id>","task_id":"<TASK>","status":"released",
   "scope":["Area_comun/state/CLAIMS.json#CLAIM-<fecha>-<id>-<TASK>",
            "Area_comun/state/TASK_INDEX.json#<TASK>",
            "Area_comun/state/PROJECT_STATE.json#active_tasks/<TASK>",
            "Area_comun/tasks/<TASK>-*.md"],
   "started_at":"<ISO-UTC>","updated_at":"<ISO-UTC>","expires_at":"<ISO-UTC+Nh>"}}
]}
JSON
python runtime/submit_intent.py --actor-id <id> --timestamp "<ISO-UTC>" \
  --commit "$(git rev-parse HEAD)" --intents /tmp/tx-deliver.json --output -
git add Area_comun/state/ runtime/state/ Area_comun/tasks/<TASK>-*.md Area_comun/handoffs/ && \
  git commit -m "deliver(<TASK>): ..." && git push   # PUSH inmediato (Task-Id: <TASK> en el parrafo final)

# 3c. AVISA por mailbox (ejemplo minimo validator-valid; requires_response:true EXIGE response_owner):
cat > Area_comun/mailbox/open/MSG-<fecha>-<id>-to-<checker>-<TASK>-in-review.md <<'MD'
---
message_id: MSG-<fecha>-<id>-to-<checker>-<TASK>-in-review
from: <id>
to: <checker>
type: REVIEW
status: open
requires_response: true
response_owner: <checker>
created_at: 2026-01-01
one_line_summary: "<TASK> entregada a in_review; gate adversarial."
requested_action: "Revisa <TASK> en clon limpio y emite GO/NO-GO."
question: "GO o NO-GO sobre <TASK>?"
---
# REVIEW <TASK>
(cuerpo)
MD
git add Area_comun/mailbox/open/ && git commit -m "mailbox(REVIEW): <id> -> <checker> <TASK>" && git push

# 4. CIERRE: el checker hace pull, revisa, y su veredicto vuelve por pull (in_review->review_approved lo hace el
#    CHECKER con capability reviewer). El flip FINAL review_approved->done exige capability IMPLEMENTER: lo ejecuta
#    el implementer (NO el checker ni un owner sin implementer). OWNERSHIP: si TU no eres implementer, rutea un
#    ACTION al implementer para el done-flip; no intentes el ->done tu mismo (submit_intent lo rechaza: "lacks
#    capability implementer"). Ejemplo del flip final:
#    intents=[{"type":"task_status","task_id":"<TASK>","from":"review_approved","to":"done","timestamp":"<ISO-UTC>"}]
```

Regla anti-colision: escribe el ledger solo en ventana segura (peer sin lock en
`.protocol-tmp/*/*.lock`, tree sin half-write) y pushea INMEDIATO; nunca dejes cambios de ledger
sin pushear mientras otro clon opera. NUNCA hagas `git checkout` de `runtime/state/*` mientras un
peer escribe (corrompe el event log). Gatea el PUSH en `validate_collaboration_state.py` exit 0
POST-commit; con el gate de trailers activo, `Task-Id: <TASK>` va en el MISMO parrafo final que
`Co-Authored-By` (o `Task-Id: none` + `Ops-Reason:` para commits de coordinacion).

### 3.2 Harness distribuido (F2.3) y ciclo e2e (F2.2) -- rutas y comandos falsables

- Harness pull->write->push de la instancia: `scripts/distributed_git_harness.py` (en el repo de la
  instancia). Test: `python scripts/test_distributed_git_harness.py` (PASS = claim de un clon visible
  en otro tras pull).
- Ciclo e2e distribuido de una tarea completa (register->claim->deliver->review->done solo via Git):
  `python scripts/distributed_e2e_task_cycle.py --remote <ruta-remoto-bare> --keep-workdir`
  (PASS = la tarea recorre el ciclo completo entre clones sin colision).
- Verifica siempre en clon limpio: `git clone -c core.longpaths=true <remoto> <tmp>` y en el clon
  `python scripts/validate_collaboration_state.py` exit 0.

## 4. Troubleshooting

- **validate rojo en clon limpio:** hay drift (state sin materializar). Re-materializa desde el
  event log o pide al coordinador que reconcilie; no operes sobre canonico rojo.
- **push rechazado (non-ff):** `git pull --rebase --autostash` y re-push; otro clon escribio primero.
- **claim bloqueado:** otro clon tiene claim activo sobre tus rutas; espera y reintenta (no fuerces).
- **rutas largas (Windows):** `core.longpaths=true` al clonar.

## 5. Definition of Done del onboarding

Estas operando cuando: clonaste la instancia, tu `.agents/<id>/config.json` esta commiteado, el
canonico valida verde en tu clon, y completaste 1 tarea de prueba (claim -> entrega -> cierre) solo
via Git, con tu estado visible en otros clones. Objetivo: <= 1 dia. El tiempo real se registra
(alimenta HP6) cuando la instancia mide el onboarding (replica employee-run).

# Host-local scratch-discipline enforcement

Run `scripts/run_scratch_discipline_monitor.py` periodically from the host scheduler, never from
CI. Pass `--scan-root`, `--scratch-root`, `--known-repo`, the canonical repository homes through
repeatable `--allow-home`, and a deliberate `--max-depth`. Example scheduler command:

```text
python scripts/run_scratch_discipline_monitor.py -- --scan-root <host-root> --scratch-root <scratch-root> --known-repo <repository> --allow-home <canonical-home> --max-depth 2
```

Exit `0` means clean, `1` means actionable findings, and `2` means invocation or inspection error.
The scheduler must retain stdout/stderr and alert the responsible owner on any nonzero exit. Exit
`1` output is the host-local DECISION-0018 anomaly delivery; the owner records it in the governed
mailbox. The scanner and monitor never delete, move, or modify scanned paths. Runtime-specific
values may instead live in an unpinned config under `scratch_discipline.canonical_homes`; do not
alter an epoch-pinned protocol config to add them.

On Windows, install the periodic trigger with
`scripts/install_scratch_discipline_monitor.ps1`. It registers a host-local Scheduled Task with a
configurable interval; `-WhatIf` previews registration without changing host state. Configure the
host scheduler or its operational wrapper to retain the task's exit code and output and route
nonzero runs to the responsible owner. Installation is an explicit operator action because it
changes host scheduler state; normal scans remain read-only.
