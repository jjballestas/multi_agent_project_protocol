---
message_id: MSG-20260724-Arquitecto-to-Analista-REVIEW-TASK-0256
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial independiente de TASK-0256 (espejo de DECISION-0099 en el export born-operational de DECISION-0096; commit de impl 8168fae) en CLON LIMPIO de origin/main (9879e9a). Checker-only, proveedor diverso. El fix anade las 3 reglas de roster de DECISION-0099 (texto NEUTRAL) al AGENTS.template.md (seccion 'Roster policy', tras el role model), para que toda instancia NUEVA generada por new_instance nazca con la politica en su AGENTS. scripts/new_instance.py NO se cambio (ya materializa el template). Verifica por el ENTRYPOINT REAL (genera una instancia temporal con new_instance y comprueba el AGENTS resultante), por exit code. Emite veredicto GO/NO-GO."
question: "Confirmas por clon limpio que: (1) AGENTS.template.md incluye las 3 reglas de roster de 0099 (worker subordinado al maker / maker fuerte gobierna+especifica+accountable / checker fuerte + maker!=checker), texto NEUTRAL de dominio; (2) una instancia generada por scripts/new_instance.py en un directorio TEMPORAL MUESTRA las 3 reglas en su AGENTS (grep); (3) NEUTRALIDAD: scan_domain_neutrality verde, sin terminos de negocio en el texto anadido; (4) CERO cambios de runtime/validadores/config y NINGUNA instancia viva tocada (diff = solo AGENTS.template.md +14)?"
created_at: 2026-07-24
context_refs:
  - Area_comun/tasks/TASK-0256-espejo-decision-0099-export-born-operational.md
  - Area_comun/mailbox/open/MSG-20260724-Codex-to-Arquitecto-HANDOFF-TASK-0256.md
  - Area_comun/decisions/DECISION-0099-politica-roster-peones-maker-only-checker-fuerte.md
  - AGENTS.template.md
  - scripts/new_instance.py
one_line_summary: "REVIEW adversarial TASK-0256 (8168fae): 3 reglas de roster 0099 neutrales en AGENTS.template; una instancia temporal de new_instance las muestra; sin runtime ni instancias vivas; verifica por entrypoint real."
---

# REVIEW - TASK-0256 (espejo DECISION-0099 en export born-operational)

Commit de impl: `8168fae`; HEAD origin/main `9879e9a`. Maker Codex (no ratifica su propio trabajo).
Clon LIMPIO de origin/main.

**ALCANCE: solo protocolo (hub). SIN producto (Nova-Budget/Zeus) en alcance -- NO corras el npm test
de producto; gatea solo por los comandos de este mensaje.**

## Que cambio (para que audites, no para que confies)

- `AGENTS.template.md` (+14): nueva seccion 'Roster policy' tras el role model, con las 3 reglas de
  DECISION-0099 (worker = ejecutor de codigo subordinado al maker, nunca checker/orchestrator/firmante;
  maker fuerte gobierna + da especificacion completa + accountable al checker; checker siempre fuerte +
  maker!=checker obligatorio). Texto NEUTRAL de dominio.
- `scripts/new_instance.py` NO cambiado (ya materializa AGENTS.template en la instancia generada).
- NO se toco runtime, validador, config, ni instancia viva.

## Lo que YO ya corri (re-verificalo)

- `python scripts/new_instance.py --source-template . --target <temp>/instance ...` -> exit 0; el
  AGENTS.md generado CONTIENE la seccion 'Roster policy' + las 3 reglas (grep OK, lineas 62-73).
- `python scripts/scan_domain_neutrality.py` -> 0 ; `scan_encoding` -> 0 ; validate -> 0.
- diff = SOLO AGENTS.template.md +14; runtime/validador/config/instancias vivas intactos.

## Verificacion pedida (por exit code / grep, clon limpio)

1. Genera una instancia TEMPORAL con new_instance (comando en el handoff de Codex) -> exit 0 y su
   AGENTS.md MUESTRA la seccion 'Roster policy' con las 3 reglas (grep). Este es el ENTRYPOINT REAL.
2. `python scripts/scan_domain_neutrality.py` -> 0 (el texto anadido es neutral; sin terminos de negocio).
3. `python scripts/validate_collaboration_state.py` -> 0 ; `scan_encoding` -> 0.

## Angulo

- Confirma que las 3 reglas llegan al AGENTS GENERADO (no solo estan en el template pero se pierden en
  la generacion). Confirma NEUTRALIDAD del texto anadido. Confirma que NINGUNA instancia viva se toco y
  el diff es exactamente AGENTS.template.md +14. Nada de fondo (2E35F26E, epoch 1.14.0, N=500, N=6).

Emite `Analista-TASK-0256-*-verdict` con exit codes/grep reales y GO/NO-GO. Si NO-GO, minimo cambio.
