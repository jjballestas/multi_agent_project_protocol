# ANALISTA - TASK-0228 WS5 - Veredicto

Firma: Analista
Fecha: 2026-07-01
Veredicto: CAMBIO-REQUERIDO / NO-GO

## Ancla canonica

- Instruccion REVIEW: `Area_comun/mailbox/open/MSG-20260701-Arquitecto-to-Analista-REVIEW-TASK-0228-ws5.md` en protocolo HEAD `f7c92ba`.
- Implementacion bajo review: `7353070` (`feat(instancing): add analyst participant to new instances`).
- Producto `D:/Agentes/Zeus/Zeus-protocol`: la instruccion no cita commit de producto; control clean clone en `b2b2395da39090109db6de2dc50726dbaab1a11e`.
- Clean clone review: `C:/Users/johnb/AppData/Local/Temp/analista-0228-review-303773e8c6de4cf684bcd81b3576fc50`.

## Reproduccion

| Gate | Resultado |
|---|---|
| `git fetch origin` + `git status --short` vivo | Exit 0. Working tree tenia cambios ajenos/untracked fuera de esta entrega; no se tocaron. |
| Producto clean clone `b2b2395`, `npm test` | Exit 0. 109 tests, 87 pass, 22 skipped. |
| Protocolo clean clone checkout `7353070`, `new_instance.py --tier coordination` con Arquitecto/Codex/Analista/human_owner | Exit 0. Instancia creada en `nova-instance`. |
| `validate_collaboration_state.py --root nova-instance` | Exit 0. |
| TASK sintetica `owner: Analista` en `nova-instance` | Exit 0. |
| Probe `owner: Intruso` en la misma familia | Exit 0. El validador no prueba el registro del owner. |
| Probe `owner: Codex` + `reviewer: Codex` con `allow_self_review:false` | Exit 0. La politica no se aplica como gate. |
| `new_instance.py --tier attested` | Exit 0; roster de 4 agentes, pero solo 3 signers (`Arquitecto`, `Codex`, `Analista`); `human_owner` queda `tier: worker`. |
| Protocolo vivo gates | `validate_collaboration_state.py` exit 0; `scan_domain_neutrality.py` exit 0; `scan_encoding.py` exit 0; drift `has_drift=false up_to_seq=2842`. |
| Protocolo clean `7353070` gates | `validate_collaboration_state.py` exit 0; `scan_domain_neutrality.py` exit 0; `scan_encoding.py` exit 0; drift `has_drift=false up_to_seq=2825`. |
| `protocol.config.json` #4 byte-identica | Vivo y clean `7353070` sha256 `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`. |

## Vector por vector

| Vector / AC | Veredicto | Evidencia falsable |
|---|---|---|
| Instancia NOVA nueva valida exit 0 con 4 agentes | PASA | `new_instance.py --tier coordination` exige `--analyst`, crea `protocol.config.agent_roles.analyst=Analista`, `PROJECT_STATE.agents.analyst=Analista`, `TASK_INDEX.legend.owner` con 4 owners y `personal/{Arquitecto,Codex,Analista,human_owner}`; validator exit 0. |
| TASK `owner: Analista` valida | PASA, pero prueba debil | La TASK sintetica `owner: Analista` valida exit 0. Probe adversarial `owner: Intruso` tambien valida exit 0, por lo que el gate no demuestra que Analista este aceptado por registro; solo demuestra que no se rechaza. |
| Alta del Analista en roster/config/templates | PASA | Template y generated instance contienen `analyst` en `agent_roles`, `PROJECT_STATE.agents`, `TASK_INDEX.legend.owner`, `tool_policy.agent_policies` y `personal/Analista`. |
| Tier coordination por defecto | PASA | Generated `protocol.config.json` tiene `adoption_tier: coordination`; event_state off en la instancia generada. |
| Maker != checker garantizado por roster con `allow_self_review:false` / `allow_self_qa:false` | SLIPS | Probe con task `owner: Codex` y frontmatter `reviewer: Codex` valida exit 0 aun con `quality_policy.allow_self_review=false`. La garantia queda declarativa, no comprobable por validator ni por `new_instance`. |
| Decision de mapeo rol->agente con cita `NOVA-ARQ-001` | SLIPS | En el canon bajo review no encontre `NOVA-ARQ-001` fuera de la tarea/GO/REVIEW que piden la cita. Las decisiones 0072/0073/0077 sustentan la direccion, pero no materializan esa cita de mapeo como decision verificable. |
| "4 firmantes" del titulo/backlog | RIESGO DECLARADO | En tier coordination no hay firma por diseno. En tier attested la ceremonia genera 4 agentes pero 3 signers; `human_owner` queda `worker`. Si "4 firmantes" significa literalmente cuatro claves/firms, no esta cumplido; si significa cuatro participantes, si. |

## Bloqueo concreto

No cierro TASK-0228 porque una de las garantias pedidas no sobrevive prueba de comportamiento: `allow_self_review:false` no impide una tarea con mismo maker/reviewer, y el validator valida tambien un owner no registrado. Ademas, la cita `NOVA-ARQ-001` exigida por el AC no aparece como decision canonica verificable.

## Recomendacion

CAMBIO-REQUERIDO. Para volver a review: (1) hacer que el gate que se use para cerrar WS5 rechace self-review/self-qa cuando la politica este en false, o degradar explicitamente la afirmacion de "garantia" a regla disciplinaria no gateada en la decision; (2) anadir decision/mapeo canonico que cite `NOVA-ARQ-001` o corregir el AC para apuntar a DECISION-0072/0073/0077; (3) aclarar si "4 firmantes" significa cuatro participantes o cuatro signers, y ajustar codigo o texto.
