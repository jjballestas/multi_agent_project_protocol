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

# 3. Trabaja el entregable. ENTREGA: escribe el handoff + mueve a in_review
#    (task_status in_progress->in_review) y RELEASE del claim, en una tx atomica:
python runtime/submit_intent.py --actor-id <id> --timestamp "<ISO-UTC>" \
  --commit "$(git rev-parse HEAD)" --intents /tmp/tx-deliver.json --output -
#    tx-deliver.json = [{task_status in_progress->in_review},{claim op:release ...}]
git add Area_comun/... && git commit -m "deliver(<TASK>): ..." && git push   # PUSH inmediato

# 4. El checker hace pull, revisa, y su veredicto (GO/NO-GO) vuelve por pull en Area_comun/mailbox/.
#    Con GO, el cierre review_approved->done lo ejecuta quien tenga capability implementer.
```

Regla anti-colision: escribe el ledger solo en ventana segura (peer sin lock en
`.protocol-tmp/*/*.lock`, tree sin half-write) y pushea INMEDIATO; nunca dejes cambios de ledger
sin pushear mientras otro clon opera. NUNCA hagas `git checkout` de `runtime/state/*` mientras un
peer escribe (corrompe el event log).

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
