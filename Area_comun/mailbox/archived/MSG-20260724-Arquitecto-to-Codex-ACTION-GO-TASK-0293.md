---
message_id: MSG-20260724-Arquitecto-to-Codex-ACTION-GO-TASK-0293
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "GO TASK-0293 (registrada proposed->ready por el Operador; pulido de los residuales ACCIONABLES de TASK-0256; type=infra, maker=Codex, checker=Analista, risk=low, estimate=S). Cierra 4 residuales de TEXTO/DOC en el bloque 'Roster policy' de AGENTS.template.md + la muestra generada, sin runtime ni instancias vivas: (a) POLISH+RES-5: la 1a oracion acota a 'agent participants that execute code' -> un checker que solo lee podria argumentarse fuera de alcance; reformula a un alcance que EXCLUYA al human owner (un humano no es un agente) SIN estrechar a la ejecucion de codigo (sugerencia del checker: 'This policy governs the agent participants of the roster.'); (b) RES-7: la 2a oracion referencia 'the registry's signer/worker key-possession tiers', pero coordination/runtime generan config SIN agent_registry -> suaviza a exencion condicional ('...where the registry defines them' o equivalente) para que no cuelgue; (c) RES-3: anade una clausula breve con la RAZON de la regla 3 (un checker incapaz de refutar convierte el gate en rubber-stamp), texto neutral; (d) RES-1: examples/generated_minimal_instance/AGENTS.md no tiene la politica (grep -c 'Roster policy' -> 0) -> dejalo COHERENTE (regenera la muestra para reflejar el template, O anade nota de snapshot congelado); gates/CI verdes. Las 3 reglas conservan su sentido; neutralidad total. verification_cmd: generar attested-default + grep de las 3 reglas + alcance corregido + generar coordination/runtime y confirmar que la ref al registry no cuelga + coherencia de la muestra + validate/scan_domain_neutrality/scan_encoding/protocol_replay --check-drift/test_attested_instancing/run_runtime_instantiation_cases -> 0. Scope: AGENTS.template.md + examples/generated_minimal_instance/. FUERA: RES-2 (upgrade a instancias vivas = directiva aparte), RES-4 (enforcement de strong-capability = DECISION aparte), RES-6 (record-only, ya corregido), cambiar el sentido de las 3 reglas, runtime/validador/config, instancias vivas, fondo intocable (2E35F26E epoch 1.14.0 N=500 N=6). Entrega TASK-0293 in_review + handoff con exit codes + evidencia de instancia temporal + release."
question: "Confirmas ETA para TASK-0293 y que cierras los 4 residuales de texto (polish/RES-5, RES-7, RES-3, RES-1) SOLO en AGENTS.template.md + la muestra generada, sin tocar runtime/instancias vivas ni el sentido de las 3 reglas, con evidencia por instancias temporales de los 3 tiers?"
created_at: 2026-07-24
context_refs:
  - Area_comun/tasks/TASK-0293-pulido-residuales-roster-policy-0256.md
  - Area_comun/artifacts/Analista-TASK-0256-roster-policy-remediation1-verdict.md
  - Area_comun/artifacts/Analista-TASK-0256-roster-policy-born-operational-verdict.md
  - AGENTS.template.md
one_line_summary: "GO TASK-0293: pulir 4 residuales de texto de 0256 (alcance sin 'execute code' + ref registry no colgante + razon regla 3 + muestra coherente) en AGENTS.template + examples; sin runtime ni instancias vivas."
---

# ACTION - GO TASK-0293 (pulido residuales accionables de 0256)

Hora local: 2026-07-24 04:40 (UTC+2). El Operador ordeno completar los residuales+polish de TASK-0256.
Ficha completa en `Area_comun/tasks/TASK-0293-pulido-residuales-roster-policy-0256.md`.

## Los 4 accionables (texto/doc)

- POLISH+RES-5: alcance de la 1a oracion sin 'that execute code' (excluye human owner, no al checker).
- RES-7: referencia a los tiers del registry como exencion condicional (no cuelga en coordination/runtime).
- RES-3: anadir la RAZON de la regla 3 (checker debil -> rubber-stamp).
- RES-1: muestra examples/generated_minimal_instance/AGENTS.md coherente (regenerar o nota de snapshot).

## Fuera (con motivo)

RES-2 (instancias vivas = directiva aparte), RES-4 (enforcement = DECISION aparte), RES-6 (record-only).
NO cambies el sentido normativo de las 3 reglas ni runtime/config/instancias vivas. Fondo intocable FUERA.

## Entrega

TASK-0293 a `in_review` + handoff con verification_cmd y exit codes + evidencia de instancias temporales
(3 tiers) + release. ASCII puro. Fix-loop tope 2 iteraciones.
