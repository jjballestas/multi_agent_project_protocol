---
message_id: MSG-20260712-Arquitecto-to-Analista-REVIEW-TASK-9304-F9304-01-rejuicio
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
created_at: 2026-07-12
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-9304-jball-reanchor-veredicto.md
  - D:/Agentes/Zeus/NOVA/Aegis/Area_comun/handoffs/HANDOFF-TASK-9304-codex-to-arquitecto-2.md
  - D:/Agentes/Zeus/NOVA/Aegis/runtime/protocol_replay.py
one_line_summary: "RE-JUICIO de F-9304-01 (iteracion 1/2). Codex remedio: validate_chain ahora RECOMPUTA el sha256 del export pre_t0 (events-pre-t0-000001-000671.jsonl) y devuelve valid=false on hash/count/range drift. chain_cases 40/40 (subio de 39 -> negativo pre_t0). in_review, 0 claims, Aegis validate/scan/neutralidad 0, drift false seq 3856. VERIFIQUE yo mismo: pre_t0 tampereado en clon limpio -> validate exit 1."
requested_action: "Re-juzga F-9304-01 en un CLON LIMPIO del repo AEGIS (D:/Agentes/Zeus/NOVA/Aegis) en el HEAD entregado (8159716c; fix en 7f80e481 protocol_replay.py). Confirma que el hallazgo esta CERRADO: repite tu repro (Add-Content al export pre_t0 events-pre-t0-000001-000671.jsonl) y verifica que AHORA validate_collaboration_state.py exit != 0 Y validate_chain valid=false (antes exit 0 / valid=true). Verifica que el negativo pre_t0 es PERMANENTE en chain_cases (40/40) y REAL, que el sello pre_t0 se RE-VERIFICA recomputando el sha256 (no se confia el declarado), y que NO se debilito nada previo (epoca 2 + F-9303-01 + epocas 1/pre_t0 byte-identicas siguen igual). SIN producto Nova-Budget en alcance. Es la iteracion 1/2 del fix-loop."
question: "GO o NO-GO para TASK-9304 tras la remediacion de F-9304-01? (jball-live sigue DIFERIDA a la maquina de John por diseno; no lo marques como faltante.)"
---

# REVIEW - re-juicio F-9304-01 (TASK-9304, iteracion 1/2)

## Que remedio Codex
Tu NO-GO cazo F-9304-01: el sello pre_t0 (`pre_t0_provenance.sealed_export`) no se recomputaba -> mutar el export
`events-pre-t0-000001-000671.jsonl` no hacia fallar validate/validate_chain, contra AC5. Decidi FIXear (no reducir
la AC). Codex remedio en Aegis (fix `7f80e481 protocol_replay.py`): `validate_chain` ahora RECOMPUTA el sha256 del
export pre_t0 y devuelve `valid=false` on hash/count/range drift; negativo permanente en chain_cases (40/40).

## Verificacion propia (adversarial informal, antes de rutearte)
Clone limpio de Aegis, `Add-Content pre_t0_ledger_seal/events-pre-t0-000001-000671.jsonl 'tamper'`,
`validate_collaboration_state.py` -> **exit 1** (antes exit 0). El hard-gate funciona.

## Estado verificado (mi lado)
in_review, owner Codex, 0 claims activos (handoff-release limpio), Aegis HEAD `8159716c`, validate/scan/neutralidad
0, chain_cases 40/40, drift false up_to_seq 3856. Hub intacto.

## Nota operacional (transparencia)
Codex reporto que durante la sesion se crearon 2 filas de claim malformadas por un error de serializacion JSON de
PowerShell; las libero y podo via runtime events antes de la validacion final. Verifique: 0 claims activos, validate
0 en vivo. Tu gateas en clon limpio de todos modos.

## Foco del re-juicio
1. **F-9304-01 CERRADO:** repite tu repro (tamper del export pre_t0) -> AHORA validate exit != 0 y validate_chain
   valid=false.
2. **Negativo PERMANENTE y REAL:** el nuevo caso de chain_cases ejerce el tamper pre_t0 y falla (no stub).
3. **RE-VERIFICACION del sello:** el sello pre_t0 se recomputa (sha256 del export), no se confia el declarado.
4. **Sin regresion:** epoca 2 (jball) + F-9303-01 + epoca 1/pre_t0 byte-identicas + tamper multi-epoca siguen OK.

Iteracion 1/2. Si sobrevive la misma clase de slip tras la 2a, escalo al operador.

-- Arquitecto
