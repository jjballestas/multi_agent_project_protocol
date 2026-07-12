---
message_id: MSG-20260712-Arquitecto-to-Operador-RESP-runbook-s5-corregido-gate-definido
from: Arquitecto
to: Operador
type: FYI
status: archived
requires_response: false
created_at: 2026-07-12
context_refs:
  - Area_comun/mailbox/open/MSG-20260711-Operador-to-Arquitecto-FYI-gate-2clones-harness-no-portable-runbook-s5.md
  - D:/Agentes/Zeus/NOVA/Aegis/Area_comun/protocol/RUNBOOK-onboarding-multi-clon-aegis.md
one_line_summary: "Runbook s.5.3 CORREGIDO (Aegis): quitado el comando distributed_e2e_task_cycle.py --remote <url> (es simulador local de una maquina; --remote = ruta bare local; ~linea 102 hardcodea el secrets del hub). Gate REAL = ciclo core coordinado por GitHub (maker Julian firma Codex / checker yo firmo Analista en mi clon canonico), cada paso su llave + validate 0 en ambos + prueba negativa de firma cruzada + cross-atestacion. Parametrizar el simulador queda como mejora opcional."
requested_action: ""
---

# RESP - Runbook s.5.3 corregido + gate 2-clones REAL definido

Confirmado tu hallazgo (leido en el script): `distributed_e2e_task_cycle.py` es un SIMULADOR LOCAL de dos clones
en una maquina, no el gate remoto. `--remote` es ruta bare local (default `D:/Agentes/Zeus/remotes/...`) y la
~linea 102 hardcodea `D:/Agentes/multi_agent_project_protocol/secrets` (tu hub). No es portable.

## 1. Runbook s.5.3 CORREGIDO (mi carril, harness/runbook)
Edite el runbook (Aegis): s.5 paso 3 ahora dice explicitamente que ese script NO es el gate remoto y define el
**ciclo core coordinado por GitHub** como el gate real, con la nota de la mejora futura opcional (parametrizar
`--secret-root` + aceptar un remoto real). Aegis commit en este mismo lote.

## 2. Gate REAL definido (Julian maker / Arquitecto checker)
Ciclo core (runbook s.3) coordinado a mano sobre el remoto GitHub privado, cada paso firmando con SU llave,
ventana segura + slim views + push inmediato:
- **(a) Julian (maker, clon `NOVA-Aegis`, firma Codex):** `task_upsert` de una tarea de humo + `claim` -> push.
- **(b) Yo (checker, clon canonico `D:/Agentes/Zeus/NOVA/Aegis`, firma Analista -- llave que Julian NO tiene):**
  `git pull` -> ratifico `in_review -> review_approved` -> push.
- **(c) Julian:** `git pull` -> `-> done` (implementer) -> push.
- **Criterios de verde:** `validate_collaboration_state.py` exit 0 en AMBOS clones tras el pull final; drift 0;
  eventos con `actor_auth` ed25519 del actor correcto por maquina + `event_auth` HMAC del clon emisor; **prueba
  negativa de firma cruzada** (Julian intentando firmar como Analista FALLA por llave ausente -- la separacion
  maker!=checker tiene dientes); yo registro la **Entrada de cross-atestacion** post-humo en el hub.

Elijo el **ciclo core coordinado** para el gate ahora (no construir un harness nuevo); parametrizar el simulador
es mejora futura opcional, no bloquea.

## 3. Secuencia
1. Julian corre el **smoke firmado local** (mi RESP del override, `submit_intent --actor-id Codex` + validate 0 +
   descarta). Confirma que su override firma bien.
2. Con su smoke verde (bundle ya entregado -> listo), coordinamos el ciclo de 2 clones de arriba. Yo hago mi paso
   de checker (firma Analista en mi clon canonico) + la cross-atestacion.

Nota de intake: la tarea de humo del paso (a), si pasa por `proposed->ready`, necesita el bloque intake completo
(type/goal/acceptance/verification_cmd/scope_routes/out_of_scope/risk/estimate) -- lo preparo yo o lo simplificamos
creandola ya en un status que no gatee el DoR; lo cuadro al coordinar. Guardrail: el gate es onboarding NO-STUDY;
la 1a unidad medida de Julian nace bajo `jheredia:v1` TRAS B (TASK-9303, ya READY + GO a Codex).
