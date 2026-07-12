---
message_id: MSG-20260712-Arquitecto-to-Codex-GO-TASK-9304-jball-reanchor
from: Arquitecto
to: Codex
type: GO
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-12
context_refs:
  - D:/Agentes/Zeus/NOVA/Aegis/Area_comun/tasks/TASK-9304-jball-config-epoch-reanchor.md
one_line_summary: "GO TASK-9304 (Aegis, ready, owner Codex): aplica el re-anclaje de config-epoch para jball:v1 (epoca 2) usando el tooling YA gateado de B (reanchor_config_epoch). jheredia:v1 ya esta registrado por B (epoca 1, boundary seq 3808); jball entra en su PROPIA epoca sobre la 1 (NO reescribir la epoca 1). Tu determinas el segment_start_seq exacto del encadenamiento. F-9303-01 hardening aplica a la epoca nueva. SOLO Aegis; jball-live diferida a la maquina de John."
requested_action: "Toma TASK-9304 (ready, owner Codex) en el repo AEGIS (D:/Agentes/Zeus/NOVA/Aegis): claim + task_status ready->in_progress via submit_intent. Aplica el re-anclaje: (1) agrega jball:v1 a signature_config.public_keys (raw pSGHuZPbQQF4aJn4dBhyRSiCUn1DKrMwhAUjjLVyWd0=, ed25519 32B verificado) Y a agent_registry (id jball, capability implementer); (2) invoca reanchor_config_epoch con el segment_start_seq CORRECTO de la epoca 2 (el arranque tras el boundary de la epoca 1, seq 3808; NO re-sellar [672,N] que solaparia la epoca 1 -- tu conoces el valor exacto, aplicaste la epoca 1 en B); (3) verifica que el hardening F-9303-01 (sello recomputado + cruce boundary<->config_epoch_history) aplica a la epoca 2 y agrega/extiende los negativos permanentes de chain_cases para la epoca 2. Gates: validate + chain_cases (todos verdes) + scan_encoding + scan_domain_neutrality + drift 0. Entrega a in_review + release. Guardrails DUROS: SOLO Aegis (el config pineado del HUB 1.14.0 / 2E35F26E NUNCA se toca); epoca 1 (jheredia) y pre_t0 byte-identicas (NO reescribir); jball-live (firma real de jball) se DIFIERE a la maquina de John (esta tarea prueba el MECANISMO con test-signer, como crit.7a). Las areas personal/jheredia/ + personal/jball/ NO son tuyas (las crea el Arquitecto)."
question: "Confirmas TASK-9304 (re-anclaje de jball:v1 en epoca 2) con el segment_start_seq correcto del encadenamiento multi-epoca y el hardening F-9303-01 en la epoca nueva?"
---

# GO - TASK-9304 re-anclaje de config-epoch para jball:v1 (A2-nominal, epoca 2)

## Contexto (autocontenido)
El operador dio GO al A2-nominal. B (TASK-9303, DONE) dejo jheredia:v1 registrado en el config VIVO de Aegis (epoca
1: boundary `config-epoch-000672-003807-to-003808` seq 3808; jheredia en public_keys Y agent_registry; config sha
`3E93CABD`). Falta jball:v1. Como la epoca 1 ya esta commiteada en la cadena viva, jball entra en su PROPIA epoca
(epoca 2) sobre la 1 -- NO se reescribe la epoca 1. Es una APLICACION del tooling que TU construiste y gateo el
Analista en B.

## Contrato
`Area_comun/tasks/TASK-9304-jball-config-epoch-reanchor.md` (Aegis, ready, owner Codex, 8 acceptance). pubkey
verificada `jball:v1` = `pSGHuZPbQQF4aJn4dBhyRSiCUn1DKrMwhAUjjLVyWd0=`.

## Puntos criticos
- **segment_start_seq de la epoca 2:** el arranque tras el boundary de la epoca 1 (seq 3808). NO re-sellar [672,N]
  (solaparia la epoca 1). Tu conoces el valor exacto (aplicaste la epoca 1 en B); si hay duda, es un blocker
  concreto, no una adivinanza.
- **F-9303-01 en la epoca nueva:** el sello de la epoca 2 se RE-VERIFICA recomputando contra las lineas reales; los
  negativos permanentes de chain_cases deben cubrir la epoca 2 (tamper del sello/frontera -> FALLA).
- **Epocas previas byte-identicas:** epoca 1 (jheredia) + pre_t0 NO se reescriben ni re-firman.
- **jball-live DIFERIDA:** la firma real de jball corre en la maquina de John (como jheredia 7b); aqui pruebas el
  mecanismo con un test-signer throwaway (crit.7a).
- **HUB intacto.** Announce de coordinacion en el hub sobre esta tarea de Aegis: usa Task-Id: none Y Ops-Reason.

-- Arquitecto
