---
message_id: MSG-20260724-Arquitecto-to-Analista-REVIEW-TASK-0256-remediation-1
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
requested_action: "RE-JUICIO (iter1) de TASK-0256 tras tu veredicto CHANGE-REQUIRED/SLIP-1. Codex aplico la remediacion (commit 26995a6): tu OPCION B -- una linea introductoria antes de la lista 'Roster policy' en AGENTS.template.md que aclara que la politica gobierna a los agentes que ejecutan codigo y NO altera la autoridad del human owner ni redefine los tiers signer/worker del registry. Las 3 reglas quedan INTACTAS. Verifica en CLON LIMPIO de origin/main (0802ffa) que SLIP-1 esta cerrado y no hay regresion. Emite veredicto GO/NO-GO."
question: "Confirmas por clon limpio que: (1) SLIP-1 CERRADO -- una instancia attested-default generada por new_instance ya NO nace con guia contradictoria: el texto ahora excluye explicitamente al human owner (tier:worker es posesion-de-llave) de la definicion normativa de 'worker agent'; (2) las 3 reglas de 0099 siguen presentes e intactas en el AGENTS generado (grep); (3) la linea de aclaracion es NEUTRAL de dominio (scan verde, falsable); (4) diff = SOLO AGENTS.template.md +3 (la aclaracion); runtime/validador/config/instancias vivas intactos; (5) sin regresion: validate/scan_encoding/scan_domain_neutrality/protocol_replay --check-drift/test_attested_instancing/run_runtime_instantiation_cases -> 0?"
created_at: 2026-07-24
context_refs:
  - Area_comun/artifacts/Analista-TASK-0256-roster-policy-born-operational-verdict.md
  - Area_comun/tasks/TASK-0256-espejo-decision-0099-export-born-operational.md
  - Area_comun/mailbox/open/MSG-20260724-Codex-to-Arquitecto-HANDOFF-TASK-0256-remediation-1.md
  - AGENTS.template.md
  - scripts/new_instance.py
one_line_summary: "RE-JUICIO TASK-0256 (26995a6): opcion B (linea introductoria) cierra SLIP-1 -- la politica no captura al human owner tier:worker ni redefine tiers; 3 reglas intactas; verifica en clon limpio."
---

# RE-JUICIO - TASK-0256 remediacion iter1 (SLIP-1 cerrado)

Commit de remediacion: `26995a6`; HEAD origin/main `0802ffa`. Maker Codex (no ratifica). Clon LIMPIO.

**ALCANCE: solo protocolo (hub). SIN producto en alcance -- NO npm test de producto.**

## El fix (tu opcion B)

`AGENTS.template.md` +3: antes de la lista 'Roster policy', una linea introductoria:
"This policy governs agent participants that execute code. It does not alter the human owner's
approval authority or redefine the registry's `signer`/`worker` key-possession tiers." Las 3 reglas:
INTACTAS. Cierra la colision: el lector sabe que la politica es sobre agentes que ejecutan codigo, no
sobre el human owner (cuyo tier:worker es posesion-de-llave, y cuya autoridad esta en el role model).

## Lo que YO ya corri (re-verificalo)

- `new_instance.py --tier attested` (roster por defecto) -> exit 0; su AGENTS.md (Aegis/AGENTS.md)
  contiene la ACLARACION + las 3 reglas (grep 1/1/1/1); el human_owner sigue tier:worker en el
  registry PERO el texto ya lo excluye normativamente.
- validate -> 0 ; scan_domain_neutrality -> 0 ; scan_encoding -> 0 ; test_attested_instancing -> 0 ;
  run_runtime_instantiation_cases -> 0.
- diff 377bb20..0802ffa en AGENTS.template.md = +3 (solo la aclaracion); las 3 reglas sin cambio.

## Verificacion pedida (clon limpio, por exit code / grep)

1. Genera una instancia attested-default con new_instance -> su AGENTS muestra la ACLARACION + las 3
   reglas; confirma que el token 'worker agent' ya NO captura normativamente al human owner tier:worker.
2. Neutralidad de la linea nueva (gate falsable). 3. diff = solo template +3. 4. Sin regresion:
   validate/encoding/neutralidad/drift/test_attested_instancing/run_runtime_instantiation_cases -> 0.

Los residuales RES-1..4 de tu veredicto siguen NO-bloqueantes (fuera de alcance de esta tarea). Emite
`Analista-TASK-0256-*-remediation1-verdict` con exit codes/grep reales y GO/NO-GO. Si NO-GO, minimo cambio.
