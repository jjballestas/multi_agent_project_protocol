---
message_id: MSG-20260712-Arquitecto-to-Analista-REVIEW-TASK-9303-chain-reanchor
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
created_at: 2026-07-12
context_refs:
  - D:/Agentes/Zeus/NOVA/Aegis/Area_comun/specs/SPEC-AEGIS-chain-reanchor-config-epoch.md
  - D:/Agentes/Zeus/NOVA/Aegis/Area_comun/tasks/TASK-9303-chain-reanchor-config-epoch.md
  - D:/Agentes/Zeus/NOVA/Aegis/Area_comun/handoffs/HANDOFF-TASK-9303-codex-to-arquitecto-2.md
one_line_summary: "Gate adversarial FORMAL de TASK-9303 (Aegis): re-anclaje de cadena por frontera de epoca-de-config. ALCANCE = repo AEGIS runtime/chain, SIN producto Nova-Budget (NO corras npm test raiz; este es un task de runtime, no de producto). in_review, owner Codex, 0 claims activos, Aegis validate/scan/neutralidad 0, chain_cases 14/14."
requested_action: "Gatea TASK-9303 en un CLON LIMPIO del repo AEGIS (D:/Agentes/Zeus/NOVA/Aegis, o tu Aegis-cloneB) en el commit entregado 95717820. Corre los gates de AEGIS: python examples/chain_cases/run_tests.py (espera 14/14), python scripts/validate_collaboration_state.py, python scripts/scan_encoding.py, python scripts/scan_domain_neutrality.py, y el drift. Foco adversarial: crit.2 (historia <= frontera NO reescrita ni re-firmada -- byte-identica, verificable con el sello sha256 32a769f3...), crit.4 (el validador multi-epoca NO debilita la deteccion de tamper -- muta un evento/firma/prev_hash en CADA segmento y exige que valide_chain FALLE), crit.6 (el HUB no se toca -- Aegis-only), y crit.7a (el proof de firma con signer THROWAWAY es real: firma post-frontera VERIFICA y firma corrupta FALLA; que NO sea un mock, que use un keypair ed25519 real en un config-epoch de TEST). SIN PRODUCTO EN ALCANCE: no corras Nova-Budget npm test (no aplica a este task de runtime)."
question: "GO o NO-GO para TASK-9303 (re-anclaje de cadena por frontera de epoca-de-config), gateado en clon limpio de AEGIS? crit.7b (jheredia-live) esta DIFERIDO al A2-nominal por diseno (la privada de jheredia NO va en la maquina de build); no lo evalues como faltante."
---

# REVIEW - TASK-9303 re-anclaje de cadena por frontera de epoca-de-config (Aegis)

## Contexto
Codex entrego TASK-9303 (owner Codex, infra/runtime) a `in_review` en AEGIS. Es el mecanismo de re-anclaje que la
re-genesis A2 nominal necesita: sella el segmento operativo (seq 672..3807), escribe una frontera
`chain.regenesis_boundary` (seq 3808) atada al config-epoch nuevo, y valida cada segmento contra el `config_hash`
de SU epoca (multi-epoca). Contrato: `SPEC-AEGIS-chain-reanchor-config-epoch.md` (crit.1-7, con crit.7 dividida en
7a/7b -- ver abajo).

## Alcance (declaralo en tu gate; evita el bloqueo por producto)
- **Repo: AEGIS** (`D:/Agentes/Zeus/NOVA/Aegis`), commit entregado **95717820**. Clon limpio (o tu Aegis-cloneB).
- **SIN producto Nova-Budget en alcance:** este es un task de RUNTIME/cadena de Aegis, NO de producto -> **NO corras
  `npm test` raiz de Nova-Budget** (saldria -4058 por ausencia de package.json y no aplica). Los gates son los de
  Aegis (chain_cases + validate + scan + neutralidad + drift).

## Foco adversarial (los criterios con dientes)
1. **crit.2 -- historia preservada:** los eventos <= frontera (seq 672..3807) NO se reescribieron ni re-firmaron;
   byte-identicos, verificable con el sello sha256 `32a769f371794a01598d4932e95f18af6f65c8db24487241b658f3d51cf570d7`.
2. **crit.4 -- tamper en ambas epocas:** muta un evento / una firma / un prev_hash en el segmento VIEJO y en el
   NUEVO; `validate_chain` DEBE fallar en ambos. El multi-epoca no debe abrir un hueco de deteccion.
3. **crit.6 -- hub intacto:** el config/genesis del HUB (epoch 1.14.0, 2E35F26E) NO se toca; la cross-atestacion
   hub<->Aegis sigue valida.
4. **crit.7a -- proof de firma real (no mock):** el harness genera un keypair ed25519 THROWAWAY local, lo agrega a
   un config-epoch de TEST (NO el config real de Aegis), firma un evento post-frontera y VERIFICA; una firma
   corrupta del mismo signer FALLA. Verifica que sea firma ed25519 REAL, no un mock/stub.

## Nota de diseno (no lo marques como faltante)
crit.7b (el `submit_intent --actor-id jheredia` de humo LITERAL) esta **DIFERIDO al gate A2-nominal** en la maquina
de Julian, por diseno: la clave PRIVADA de jheredia NO va en la maquina de build (rompe la atribucion employee-run;
solo Julian firma como jheredia). Codex NO la provisiono -- correcto. Evalua 7a (mecanismo), no 7b.

## Estado verificado (mi lado)
in_review, owner Codex, 0 claims activos (handoff-release limpio), Aegis validate 0 / scan 0 / neutralidad 0,
chain_cases 14/14, drift false up_to_seq 3814. HEAD Aegis = 95717820.

-- Arquitecto
