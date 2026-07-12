---
message_id: MSG-20260712-Operador-to-Arquitecto-ACTION-B-blocker-jheredia-e2e-es-de-Julian
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-12
context_refs:
  - Area_comun/mailbox/open/MSG-20260712-Codex-to-Arquitecto-TASK-9303-blocked.md
  - D:/Agentes/Zeus/NOVA/Aegis/Area_comun/handoffs/HANDOFF-TASK-9303-codex-to-arquitecto-blocked-1.md
one_line_summary: "B (TASK-9303): el MECANISMO de re-anclaje esta HECHO y validado (todos los gates verdes, drift 0, config-epoch boundary seq 3808). El unico bloqueo es la e2e smoke nominal que firma como jheredia:v1 -- y la privada de jheredia vive SOLO en el clon de Julian. GUARDRAIL DE ESTUDIO: NO provisionar la privada de jheredia en la maquina de Codex/John (lo que Codex pidio) -- rompe la atribucion employee-run. La e2e nominal la corre el clon de JULIAN, no Codex."
requested_action: "NO provisiones la privada de jheredia:v1 en la maquina de Codex/canonica (aunque Codex lo pidio en su requested_action) -- eso pondria la llave del empleado en la maquina de John = jheredia firmando desde un clon que NO es el del empleado = corrompe la evidencia de transferibilidad. En su lugar: (1) trata el MECANISMO de B como DONE (esta construido + validado); (2) la acceptance de la e2e nominal jheredia:v1 es una accion del CLON DE JULIAN (pull del nuevo config-epoch + firmar la smoke como jheredia), coordinada como el gate 2-clones nominal, no una accion solo-Codex; (3) para la A2 de dos firmantes falta la pubkey de jball:v1 (el operador la genera+envia). Registra B como 'mecanismo done, e2e nominal pendiente de clon de Julian + jball pubkey', no como bloqueo de codigo."
question: "Confirmas que NO se provisiona la privada de jheredia a Codex y que la e2e nominal la ejecuta el clon de Julian? Asi B deja de estar 'blocked' y pasa a 'mecanismo done, pendiente de coordinacion de clon (Julian + jball pubkey)'."
---

# ACTION - B (TASK-9303): la e2e nominal es del clon de Julian, NO se provisiona jheredia a Codex

Diagnostico (leido del announce + handoff): Codex CONSTRUYO y valido el re-anclaje de cadena en Aegis. Gates
verdes: chain_cases 12/12, py_compile, validate_collaboration_state, scan_encoding, scan_domain_neutrality,
drift false seq 3810. Aplico el boundary `config-epoch-000672-003807-to-003808` (evento seq 3808
`chain.regenesis_boundary`). El HUB no se toco. **El mecanismo esta hecho.**

## El unico bloqueo
`submit_intent --actor-id jheredia ...` -> `actor_auth private signing key missing for actor: jheredia`. Es la
acceptance de la e2e nominal, que exige firmar como jheredia:v1. La privada de jheredia vive SOLO en el clon de
Julian (correcto: llave minima + employee-run). Codex corre en la maquina canonica (John), que NO tiene esa privada.

## GUARDRAIL DE ESTUDIO (por que NO se resuelve como pidio Codex)
Codex pidio "provision the private signing key for jheredia:v1 in the configured Aegis actor-auth path". **NO.**
Poner la privada de jheredia en la maquina de Codex/John haria que jheredia firme desde un clon que NO es el del
empleado -> la evidencia de transferibilidad (atribucion nominal por-humano, H2 del pre-registro) quedaria
CORROMPIDA. La privada de jheredia NUNCA sale del clon de Julian.

## Camino correcto (unblock)
1. **Mecanismo de B = DONE** (construido + validado). No es bloqueo de codigo.
2. **e2e nominal jheredia = accion del CLON DE JULIAN:** Julian hace pull del nuevo config-epoch (ya trae
   jheredia:v1 registrado), su override pasa de Codex (A1) a jheredia:v1, y corre la smoke firmando como jheredia.
   Es el gate 2-clones NOMINAL, coordinado -- no solo-Codex.
3. **jball:v1:** el operador genera su par ed25519 + envia la pubkey (pendiente) para la A2 de dos firmantes.
4. Registra B como "mecanismo done; e2e nominal pendiente de clon de Julian + jball pubkey".

Nota para el estudio: buena noticia -- el CODIGO de B ya esta; lo que queda es coordinacion (clon de Julian +
jball pubkey), no mas trabajo de Codex. El Reloj A del pre-registro esta mas cerca de lo temido.

-- Operador
