---
message_id: MSG-20260712-Operador-to-Arquitecto-FYI-jball-v1-pubkey-para-A2-nominal
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-12
context_refs:
  - Area_comun/mailbox/open/MSG-20260712-Operador-to-Arquitecto-ACTION-alta-jball-v1-con-B-regenesis.md
one_line_summary: "El operador genero su par ed25519. Pubkey de jball:v1 abajo, para registrarla en el config-epoch del A2-nominal (junto a jheredia:v1). Capability implementer. Alta ya aceptada por el Arquitecto (e7cbbc2)."
requested_action: "Registra la pubkey de jball:v1 en signature_config.public_keys de AEGIS en el config-epoch del A2-nominal (junto con jheredia:v1) + alta en agent_registry (id jball, capability implementer) + area personal/jball/. Con jheredia:v1 (7b) + jball:v1 registrados, se puede correr el gate 2-clones nominal de dos firmantes en la maquina de Julian. SOLO Aegis; hub pineado intacto; maker!=checker (las unidades de John las gatea el Analista)."
question: "Confirmas jball:v1 registrada en el config-epoch del A2-nominal? PUBKEY jball:v1 (ed25519, base64) = pSGHuZPbQQF4aJn4dBhyRSiCUn1DKrMwhAUjjLVyWd0="
---

# ACTION - Pubkey de jball:v1 para el A2-nominal

El operador genero su par ed25519 (humano-run, DECISION-0057). La privada se queda en su maquina; envia solo
la publica.

**PUBKEY jball:v1 (ed25519, base64):**

```
pSGHuZPbQQF4aJn4dBhyRSiCUn1DKrMwhAUjjLVyWd0=
```

## Que hacer
- Registrar en `signature_config.public_keys` de AEGIS como `jball:v1` en el config-epoch del A2-nominal (el mismo
  que registra jheredia:v1 tras B).
- Alta en `agent_registry`: id `jball`, capability **implementer**.
- Area `personal/jball/`.

## Guardrails (iguales que jheredia/B)
- SOLO Aegis: el config pineado del hub (1.14.0, 2E35F26E) NO se toca.
- maker != checker: las unidades de John (jball) las gatea el Analista (llave/maquina separada); jball no recibe
  reviewer sobre su propio trabajo.
- Con jball:v1 + jheredia:v1 registrados -> gate 2-clones NOMINAL de dos firmantes (maquina de Julian) = la
  acceptance 7b de B.

-- Operador
