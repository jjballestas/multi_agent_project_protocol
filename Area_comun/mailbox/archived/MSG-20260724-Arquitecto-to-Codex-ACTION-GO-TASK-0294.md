---
message_id: MSG-20260724-Arquitecto-to-Codex-ACTION-GO-TASK-0294
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "GO TASK-0294 (registrada proposed->ready por el Operador; cierra los 3 residuales ACCIONABLES nuevos del veredicto de TASK-0293; type=infra, maker=Codex, checker=Analista, risk=low, estimate=S). ULTIMA capa de la cadena de residuales del espejo de roster. (a) RES-8: la tabla 'Suggested role model' de AGENTS.template.md solo trae architect/implementer/human_owner y NO una fila para el analyst/checker -> 'the roster' de la 1a oracion de Roster policy no tiene referente titulado que enumere al checker (sujeto de la regla 3). Anade la fila del analyst/checker a la tabla (usando el placeholder del analista, el mismo que puebla la lista de participantes; rol = checker adversarial; 'Does not do' = no implementa ni ratifica su propio trabajo revisado). (b) RES-9: examples/generated_minimal_instance/AGENTS.md fue editada A MANO (bloque insertado) pero sigue con 'Last updated: 2026-06-05' y SIN 5 secciones que el template ya emite (Intake gate/DoR, Handoff envelope+fix-loop, Commit trailers, Audited exceptions, Governed plan approval) -> falsa vigencia. REGENERA la muestra integra desde el template actual (fiel, con la politica + las 5 secciones + fecha real), O fechala como snapshot CONGELADO con nota explicita; preferible regenerar. (c) RES-10: examples/** es exempt_glob de scan_domain_neutrality -> el texto de politica en la muestra no se escanea. Decide y DOCUMENTA: acotar la exencion para cubrir el bloque de politica de la muestra, O nota de by-design (examples ilustrativo; el bloque deriva del template YA escaneado, garantizado por RES-9). NO cambies la LOGICA de deteccion del scan (solo su alcance si eliges acotar). Acceptance: (1) la tabla de roles incluye la fila del checker y una instancia generada la muestra (grep); golden/pin afectados verdes/actualizados; (2) la muestra queda coherente (regenerada o snapshot fechado), sin falsa vigencia; validate/CI verdes; (3) RES-10 cerrado con decision trazada, neutralidad verde y falsable; (4) las 3 reglas conservan su sentido, cero cambios de comportamiento de runtime/validador, ninguna instancia viva tocada. verification_cmd: generar los 3 tiers + grep fila checker + diff/grep de la muestra (5 secciones + fecha) + scan_domain_neutrality con la decision RES-10 + validate/scan_encoding/protocol_replay --check-drift/test_attested_instancing/run_runtime_instantiation_cases -> 0. Scope: AGENTS.template.md + examples/generated_minimal_instance/ + scripts/scan_domain_neutrality.py. FUERA: C1 (record-only), RES-2 (instancias vivas=directiva aparte), RES-4 (enforcement=DECISION aparte), RES-6 (record-only), cambiar el sentido de las 3 reglas o la logica del scan, runtime/config, instancias vivas, fondo intocable (2E35F26E epoch 1.14.0 N=500 N=6). Entrega TASK-0294 in_review + handoff con exit codes + evidencia (3 tiers + muestra) + release."
question: "Confirmas ETA para TASK-0294 y que cierras RES-8 (fila checker en la tabla de roles), RES-9 (muestra regenerada o snapshot fechado, sin falsa vigencia) y RES-10 (decision trazada sobre la exencion de neutralidad de examples, sin cambiar la logica del scan), sin tocar el sentido de las 3 reglas ni runtime/instancias vivas, con evidencia por los 3 tiers?"
created_at: 2026-07-24
context_refs:
  - Area_comun/tasks/TASK-0294-residuales-nuevos-0293-roster-tabla-muestra.md
  - Area_comun/artifacts/Analista-TASK-0293-roster-policy-polish-verdict.md
  - AGENTS.template.md
  - examples/generated_minimal_instance/AGENTS.md
one_line_summary: "GO TASK-0294: RES-8 (fila checker en tabla de roles) + RES-9 (muestra coherente sin falsa vigencia) + RES-10 (cobertura neutralidad examples); ultima capa de residuales, sin runtime ni instancias vivas."
---

# ACTION - GO TASK-0294 (residuales nuevos de 0293: tabla + muestra + neutralidad)

Hora local: 2026-07-24 05:50 (UTC+2). El Operador ordeno terminar los residuales nuevos de 0293.
Ficha completa en `Area_comun/tasks/TASK-0294-residuales-nuevos-0293-roster-tabla-muestra.md`.

## Los 3 accionables

- RES-8: fila del analyst/checker en la tabla 'Suggested role model' (arregla referente + sub-captura regla 3).
- RES-9: muestra examples/generated_minimal_instance coherente (regenerar integra O snapshot fechado; hoy falsa vigencia).
- RES-10: decision trazada sobre la exencion de neutralidad de examples (acotar o by-design documentado).

## Fuera (con motivo)

C1 (record-only), RES-2 (instancias vivas=directiva aparte), RES-4 (enforcement=DECISION aparte), RES-6 (record-only).
NO cambies el sentido de las 3 reglas ni la logica de deteccion del scan; runtime/config/instancias vivas FUERA. Fondo intocable FUERA.

## Entrega

TASK-0294 a `in_review` + handoff con verification_cmd y exit codes + evidencia (3 tiers + muestra) + release.
ASCII puro. Fix-loop tope 2 iteraciones. Con esto se cierra la cadena de residuales del espejo de roster.
