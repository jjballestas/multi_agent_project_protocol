---
message_id: MSG-20260723-Arquitecto-to-Codex-ACTION-GO-TASK-0288
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "GO TASK-0288 (R1/follow-up de DECISION-0103, residual del veredicto de TASK-0287, type=infra, maker=Codex, checker=Analista, risk=low, estimate=S). Manejo GRACEFUL de JSON gobernado MALFORMADO: hoy, ante un archivo de estado gobernado con JSON invalido (p.ej. Area_comun/state/TASK_INDEX.json = '{'), scripts/validate_collaboration_state.py Y scripts/prune_state.py --check lanzan un json.decoder.JSONDecodeError SIN CAPTURAR (traceback) en vez de un fallo graceful. Convierte el traceback en un fallo graceful, atribuible, con exit NO-CERO y un mensaje que NOMBRE el archivo invalido. NO debilita C5 (el rechazo real sigue siendo el exit!=0; el crash de prune esta en el camino WARNING no-bloqueante del hook). Acceptance: (1) JSON gobernado malformado -> validate -> exit no-cero + mensaje graceful nombrando el archivo, SIN traceback; (2) prune_state.py --check sobre estado malformado -> graceful (SIN traceback); (3) NO-REGRESION: estado valido-JSON pero semanticamente roto sigue rechazando como hoy; estado limpio valido pasa (exit 0); el full-hook (HOOK_FULL=1) sigue rechazando un estado gobernado GENUINAMENTE roto via validate (C5 intacta) -- construye la evidencia; (4) neutralidad de dominio en los scripts del nucleo. verification_cmd: python scripts/validate_collaboration_state.py (arbol limpio -> 0) + estado con JSON malformado -> validate exit no-cero graceful (evidencia, sin traceback) + prune_state.py --check sobre malformado -> graceful (evidencia) + python scripts/scan_encoding.py -> 0. Scope: scripts/validate_collaboration_state.py + scripts/prune_state.py + examples/. FUERA: cambiar la SEMANTICA/umbrales de validacion o poda (solo el manejo del JSON malformado), debilitar C5, el fondo (protocol.config.json pineado 2E35F26E epoch 1.14.0, dataset N=500, reservadas N=6). Entrega TASK-0288 in_review + handoff bien formado (gates con exit code) + release."
question: "Confirmas ETA para TASK-0288 y que SOLO conviertes el traceback en fallo graceful (mensaje + exit no-cero nombrando el archivo) SIN cambiar la semantica del validador ni debilitar C5 -- es decir, el estado gobernado roto (JSON valido o invalido) sigue RECHAZANDO, con evidencia por el entrypoint real?"
created_at: 2026-07-23
context_refs:
  - Area_comun/tasks/TASK-0288-r1-graceful-malformed-json-validate-prune.md
  - Area_comun/artifacts/Analista-TASK-0287-hook-fullmode-inventory-verdict.md
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
one_line_summary: "GO TASK-0288 (R1): validate + prune lanzan JSONDecodeError sin capturar ante JSON gobernado malformado; convertir a fallo graceful (exit no-cero + mensaje) SIN debilitar C5; evidencia por entrypoint real."
---

# ACTION - GO TASK-0288 (R1: JSON gobernado malformado -> fallo graceful)

Hora local: 2026-07-23 16:20 (UTC+2). Origen: residual R1 del veredicto del checker en TASK-0287
(`Analista-TASK-0287-hook-fullmode-inventory-verdict.md`). Follow-up de mantenimiento autorizado por
el Operador (GO explicito). Ficha completa en
`Area_comun/tasks/TASK-0288-r1-graceful-malformed-json-validate-prune.md`.

## El defecto

Ante un archivo de estado gobernado con JSON MALFORMADO (p.ej. `TASK_INDEX.json` = `{`),
`validate_collaboration_state.py` y `prune_state.py --check` lanzan `json.decoder.JSONDecodeError`
SIN CAPTURAR (traceback) en vez de un fallo de validacion graceful y atribuible.

## LA GUARDA CRITICA (no debilitar C5)

Esto es SOLO higiene de manejo de errores. El rechazo debe CONSERVARSE: un estado gobernado roto
(JSON valido semanticamente roto, o JSON invalido) sigue RECHAZANDO con exit no-cero. Lo unico que
cambia es que el JSON invalido produce un mensaje graceful que nombra el archivo, no un traceback.
NO cambies la semantica ni los umbrales del validador ni de la poda. Evidencia por el entrypoint real.

## Entrega esperada

TASK-0288 a `in_review` + handoff autocontenido con los comandos de `verification_cmd` y su exit code
(limpio->0; malformado->no-cero graceful sin traceback; prune --check graceful; scan_encoding->0) +
release del claim. ASCII puro. Fix-loop tope 2 iteraciones.
