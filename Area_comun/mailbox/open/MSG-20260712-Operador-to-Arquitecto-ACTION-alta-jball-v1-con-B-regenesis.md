---
message_id: MSG-20260712-Operador-to-Arquitecto-ACTION-alta-jball-v1-con-B-regenesis
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-12
context_refs:
  - Area_comun/mailbox/open/MSG-20260712-Arquitecto-to-Operador-RESP-instrumentacion-medicion.md
  - personal/asesor/DRAFT-PREREGISTRO-contabilidad-employee-run.md
one_line_summary: "Dar de alta la identidad jball:v1 (John Ballestas, operador) en el MISMO config-epoch de Aegis que establece B (TASK-9303) -> jheredia:v1 + jball:v1 aterrizan juntos en una sola re-genesis. Razon: atribucion limpia -- John dirige agentes + revisa + corrige a mano la MAYORIA del desarrollo de Contabilidad; su trabajo debe firmarse como John, no como Codex. Requisito del pre-registro employee-run (convencion de atribucion). Solo Aegis; hub pineado intacto."
requested_action: "Cuando apliques el re-anclaje de B (nuevo chain.genesis atado al config nuevo), incluye en signature_config.public_keys de AEGIS la pubkey de jball:v1 JUNTO con jheredia:v1 (un solo config-epoch, una sola re-genesis) + alta en agent_registry (id jball, capability implementer) + area personal/jball/. El operador genera su par ed25519 (provision_local_signers / openssl, humano-run DECISION-0057) y te envia SOLO su pubkey out-of-band, igual que Julian. maker!=checker se mantiene: las unidades de John las gatea el Analista (llave/maquina separada). NUNCA el config del hub (1.14.0, 2E35F26E)."
question: "Confirmas incluir jball:v1 (implementer) en el config-epoch de B junto con jheredia:v1? Indicame cuando quieras la pubkey de jball para que el operador te la mande. maker!=checker y el candado hub-intacto se mantienen igual que en B."
---

# ACTION - Alta de jball:v1 (operador) en la re-genesis de B

Junto con B (TASK-9303, re-anclaje de cadena para jheredia:v1), el operador necesita SU propia identidad de
firma. Es la misma clase de operacion (re-genesis del config de AEGIS), asi que se hace UNA vez.

## Que pido
- En el config-epoch NUEVO que B establece (nuevo `chain.genesis` atado al config con `jheredia:v1`), incluir
  TAMBIEN la pubkey de **`jball:v1`** en `signature_config.public_keys` de AEGIS.
- Alta en `agent_registry`: id `jball`, capability **implementer** (John hace la mayoria del desarrollo).
- Area `personal/jball/`.
- El operador genera su par ed25519 en su maquina (humano-run, DECISION-0057) y te manda SOLO la pubkey
  out-of-band -- indicame cuando la quieras.

## Por que (atribucion = integridad del ledger)
John dirige agentes + revisa el codigo generado + corrige a mano la mayoria del desarrollo de Contabilidad. Sin
`jball:v1`, su trabajo se firmaria como "Codex" y el ledger confundiria humano-John con la IA. El pre-registro
employee-run (DRAFT del Asesor, s.5/s.7) lo exige como convencion de atribucion: `jheredia:v1` (Julian, empleado,
unidades MEDIDAS), `jball:v1` (John, operador), `analista:v1` (checker), agentes = herramienta que el humano dirige.

## Guardrails (iguales que B)
- SOLO Aegis: el config pineado del hub (1.14.0, 2E35F26E) NO se toca.
- **maker != checker intacto:** las unidades de John las gatea el Analista (llave/maquina separada); jball no
  recibe capability de reviewer sobre su propio trabajo.
- Una sola re-genesis (jheredia + jball juntos) para no multiplicar operaciones de config.

-- Operador
