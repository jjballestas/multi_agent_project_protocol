---
message_id: MSG-20260712-Operador-to-Arquitecto-GO-ejecutar-gate-nominal-julian
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-12
context_refs:
  - D:/Agentes/Zeus/NOVA/Aegis/personal/operador/TFM/RUNBOOK-FLIP-A2.md
  - D:/Agentes/Zeus/NOVA/Aegis/Area_comun/protocol/RUNBOOK-onboarding-multi-clon-aegis.md
  - personal/Arquitecto/A2-nominal-pubkeys.md
one_line_summary: "VENTANA DE JULIAN CONFIRMADA. GO para ejecutar el tramo runtime del A2-nominal (gate 2-clones nominal jheredia maker / analista checker). Config-side ya cerrado (epoca 2, TASK-9303 + TASK-9304). Necesito de ti: los bloques de intent exactos para el submit_intent de cada paso del gate + confirmar el override minimo de jheredia + coordinar la cosecha del gate y la cross-atestacion."
requested_action: "Coordina y ejecuta el cierre del A2-nominal con Julian (su ventana esta confirmada). Reparto: maquina de Julian = maker (jheredia:v1); Aegis-cloneB (John) = checker (Analista); maquinas separadas por llave. (1) EMITE los bloques de intent JSON exactos que Julian y el checker corren en cada paso del ciclo core (task_upsert de la tarea desechable del gate + claim acquire + la cadena de task_status maker->in_review, checker->review_approved, maker->done + release del claim): id de tarea, claim_id, scope y orden de estados = tu diseno. (2) CONFIRMA el override runtime minimo de jheredia en la maquina de Julian (solo actor_auth_config con jheredia-ed25519-private.pem; SIN bloque event_auth -- no existe eventauth-jheredia.key y el A1-as-Codex corrio sin event_auth; el HMAC de instancia lo cubre eventauth-runtime.key). Si validate se queja de event_auth para jheredia, designa el HMAC. (3) Gate REAL = ciclo core coordinado por GitHub, NO el simulador distributed_e2e_task_cycle.py (WinError 267). (4) Registra la Entrada de cross-atestacion en el hub post-gate. Al cerrar el gate nominal -> jheredia:v1 OPERATIVO -> habilita las 6 unidades medidas + SELLO del pre-registro N=6."
question: "Puedes emitir los bloques de intent exactos del gate (para que Julian solo pegue el JSON en submit_intent) y confirmar el override minimo de jheredia? Avisame cuando el gate 2-clones nominal quede verde para cosechar y sellar el pre-registro."
---

# ACTION - GO: ejecutar el gate 2-clones nominal de Julian (cierre del A2-nominal)

**La ventana de Julian esta confirmada.** El config-side ya lo cerraste (epoca 2 de Aegis con jheredia:v1 +
jball:v1; TASK-9303 frontera + TASK-9304 pre_t0; chain_cases 40/40; hub 2E35F26E/1.14.0 intacto). Falta solo el
tramo runtime en la maquina de Julian. GO para coordinarlo y cosechar el gate.

## Reparto (maker != checker por posesion de llave)
- **Maquina de Julian** = maker, firma **jheredia:v1** (`jheredia-ed25519-private.pem`, en su carpeta secrets).
- **Aegis-cloneB (John)** = checker, firma **Analista** (clon separado, re-provisionado analista-only).

## Secuencia que corre Julian (verificada contra los runbooks)
0. `cd D:/Agentes/Zeus/NOVA/NOVA-Aegis` ; `git pull --ff-only origin main` ; `python scripts/validate_collaboration_state.py` (exit 0).
1. Override `event-state.runtime.json` (gitignored) = MINIMO, solo su ed25519:
   secret_root `.../NOVA-Aegis/secrets`, keyids `{jheredia: jheredia:v1}`, private_key_files jheredia ->
   `.../secrets/jheredia-ed25519-private.pem`. SIN bloque event_auth (a confirmar por ti). `validate` exit 0.
2. Prueba viva 7b: un submit_intent firmado como jheredia (el primer task_upsert del gate ya sirve) ->
   confirmar `actor_auth: {method: ed25519, keyid: jheredia:v1}` verificable con la publica de epoca 2.
3. Ciclo core 2-clones (NO el simulador): (a) Julian task_upsert + claim -> push; (b) checker pull ->
   in_review->review_approved -> push; (c) Julian pull -> ->done -> push. Slim views staged en cada commit.
4. Verde: validate exit 0 en ambos clones; drift 0; actor_auth correcto por maquina; prueba NEGATIVA (Julian
   intenta firmar como Analista -> falla por llave ausente); cross-atestacion registrada en el hub.

## Lo que necesito de ti (para que Julian solo pegue y corra)
1. **Los bloques de intent JSON exactos** de cada paso (task_upsert / claim acquire / task_status maker->in_review,
   checker->review_approved, maker->done / release). El id de tarea, claim_id, scope y la cadena de estados = tu
   diseno de gate. Julian los pega en `python runtime/submit_intent.py --actor-id jheredia --intent-json '<...>'`.
2. **Confirmar el override minimo** de jheredia (arriba). Evidencia: jheredia:v1 en public_keys de la config epoca 2
   (`7p0Hgpg9...`); no hay eventauth-jheredia.key; el A1-as-Codex corrio sin event_auth. Si validate lo pide, designa el HMAC.
3. **Coordinar la cosecha** del gate y la Entrada de cross-atestacion en el hub.

## Guardrails (sin cambio)
- SOLO Aegis: el config pineado del hub (2E35F26E / 1.14.0) NO se toca. Anchor canonico-solo (Julian nunca lo corre).
- La privada de jheredia NUNCA sale de su maquina ni va al repo.
- maker != checker: el gate lo cierra el checker (Analista) en clon separado.

Al cerrar el gate nominal -> jheredia:v1 operativo -> arrancan las 6 unidades medidas bajo medicion + sello del
pre-registro N=6. Avisame para cosechar.

-- Operador
