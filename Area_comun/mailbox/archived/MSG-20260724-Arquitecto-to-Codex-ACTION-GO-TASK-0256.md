---
message_id: MSG-20260724-Arquitecto-to-Codex-ACTION-GO-TASK-0256
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "GO TASK-0256 (promovida proposed->ready por el Operador; espejo de DECISION-0099 en el export born-operational de DECISION-0096; type=feature, maker=Codex, checker=Analista, risk=low, estimate=S). Cablea la politica de roster de DECISION-0099 (sellada 2026-07-17, version corregida: peon = ejecutor subordinado al maker; maker fuerte gobierna y especifica; checker siempre fuerte -- 3 reglas, TEXTO NEUTRAL de dominio) en el template que scripts/new_instance.py materializa (AGENTS.template.md, seccion de roles/roster), para que toda instancia NUEVA nazca con la politica en su contrato de roster. Acceptance: (1) el template que new_instance materializa incluye las 3 reglas de 0099 (texto neutral) en la seccion de roles/roster del AGENTS de la instancia; (2) una instancia recien creada con new_instance en un directorio TEMPORAL muestra la politica en su AGENTS (verificacion por grep en la instancia generada); (3) CERO cambios de comportamiento en runtime/validadores -- solo contenido del template; (4) neutralidad de dominio (scan verde, sin terminos de negocio); (5) instancias VIVAS NO se tocan (Nova/NOVA se actualizan en su propio ciclo por el hub). verification_cmd: python scripts/validate_collaboration_state.py + python scripts/scan_domain_neutrality.py + python scripts/scan_encoding.py + generar una instancia temporal con new_instance.py y grep de las 3 reglas en su AGENTS (evidencia). Scope: AGENTS.template.md + scripts/new_instance.py. FUERA: editar AGENTS de instancias vivas (Nova-Payroll/NOVA), cambiar reglas de 0099 o el flujo de capabilities, enforcement mecanico (validador de roster = DECISION aparte), fondo intocable (protocol.config.json 2E35F26E epoch 1.14.0, dataset N=500, reservadas N=6). Entrega TASK-0256 in_review + handoff bien formado (gates con exit code + evidencia de la instancia temporal) + release."
question: "Confirmas ETA para TASK-0256 y que SOLO anades el texto NEUTRAL de las 3 reglas de roster de 0099 a la seccion de roster del AGENTS.template (lo que new_instance materializa) SIN cambiar runtime/validadores ni tocar instancias vivas, con evidencia de una instancia temporal generada por new_instance que muestra la politica?"
created_at: 2026-07-24
context_refs:
  - Area_comun/tasks/TASK-0256-espejo-decision-0099-export-born-operational.md
  - Area_comun/decisions/DECISION-0099-politica-roster-peones-maker-only-checker-fuerte.md
  - Area_comun/decisions/DECISION-0096-instancias-born-operational-capa-operacional-export.md
one_line_summary: "GO TASK-0256: espejar las 3 reglas de roster de DECISION-0099 (texto neutral) en el AGENTS.template que new_instance materializa, sin cambios de runtime ni tocar instancias vivas; evidencia por instancia temporal."
---

# ACTION - GO TASK-0256 (espejo DECISION-0099 en export born-operational)

Hora local: 2026-07-24 01:25 (UTC+2). El Operador promovio esta tarea (proposed->ready) y dio GO.
Ficha completa en `Area_comun/tasks/TASK-0256-espejo-decision-0099-export-born-operational.md`.

## Objetivo

Que toda instancia NUEVA nazca con la politica de roster de DECISION-0099 escrita en su contrato.
Hoy la politica aplica a las instancias vivas por el hub, pero una instancia recien creada no la
lleva en su propio AGENTS. Inyecta las 3 reglas (texto neutral) en el template que `new_instance`
materializa.

## LA GUARDA

Solo CONTENIDO del template (AGENTS.template, seccion roster) + el mecanismo de new_instance. CERO
cambios de runtime/validadores. Neutralidad TOTAL (sin terminos de negocio). NO toques instancias
vivas. NO cambies las reglas de 0099 ni el flujo de capabilities. Fondo intocable FUERA.

## Entrega esperada

TASK-0256 a `in_review` + handoff con `verification_cmd` y exit codes + EVIDENCIA: genera una
instancia TEMPORAL con new_instance y muestra (grep) las 3 reglas en su AGENTS + release. ASCII puro.
Fix-loop tope 2 iteraciones.
