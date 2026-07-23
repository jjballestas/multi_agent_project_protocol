---
task_id: TASK-0288
title: "[DECISION-0103][R1/follow-up] Manejo graceful de JSON gobernado MALFORMADO en validate + prune (hoy lanzan JSONDecodeError sin capturar)"
type: infra
status: ready
owner: Codex
phase: P2
priority: normal
created_at: 2026-07-23
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0103, TASK-0287, TASK-0265]
linked_decisions: [DECISION-0103]
file: Area_comun/tasks/TASK-0288-r1-graceful-malformed-json-validate-prune.md
intake:
  type: infra
  goal: "Residual R1 del veredicto del checker en TASK-0287. Ante un archivo de estado gobernado con JSON MALFORMADO (p.ej. Area_comun/state/TASK_INDEX.json = '{'), tanto scripts/validate_collaboration_state.py como scripts/prune_state.py --check lanzan un json.decoder.JSONDecodeError SIN CAPTURAR (traceback de Python) en vez de un fallo de validacion graceful y atribuible. Esto NO debilita C5 (el rechazo real sigue siendo el exit!=0; el crash de prune ocurre en el camino WARNING no-bloqueante del hook), pero es higiene de manejo de errores: convertir el traceback en un fallo graceful con mensaje claro que NOMBRE el archivo invalido y un exit no-cero. Es identico pre-fix de 0287; 0287 no lo toco (fuera de su scope)."
  acceptance:
    - "Un archivo de estado gobernado con JSON malformado (p.ej. TASK_INDEX.json = '{') pasado a validate_collaboration_state.py produce exit NO-CERO con un mensaje graceful que nombra el archivo como JSON invalido, SIN traceback de Python."
    - "prune_state.py --check sobre el mismo estado malformado produce un resultado graceful (exit no-cero o el comportamiento documentado) SIN traceback de Python."
    - "NO-REGRESION: un estado gobernado VALIDO-JSON pero semanticamente roto sigue rechazando como hoy; un estado limpio valido sigue pasando (exit 0); el full-hook (HOOK_FULL=1) sigue rechazando un estado gobernado GENUINAMENTE roto via validate (C5 intacta). Construir la evidencia por exit code."
    - "Neutralidad de dominio: no introducir terminos de negocio en los scripts del nucleo."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py -> exit 0 (arbol limpio)"
    - "estado gobernado con JSON malformado ('{') -> validate -> exit no-cero + mensaje graceful nombrando el archivo (SIN traceback); evidencia"
    - "prune_state.py --check sobre estado malformado -> graceful (SIN traceback); evidencia"
    - "python scripts/scan_encoding.py -> exit 0"
  scope_routes:
    - scripts/validate_collaboration_state.py
    - scripts/prune_state.py
    - examples/
  out_of_scope:
    - "Cambiar la SEMANTICA/umbrales de validacion o de poda -- FUERA; solo el manejo del JSON malformado (traceback -> graceful)."
    - "Debilitar el gate real / C5 -- FUERA (el rechazo debe conservarse; solo mejora el mensaje/atribucion)."
    - "El comportamiento de .githooks/pre-commit mas alla de lo que estos scripts producen -- FUERA."
    - "Fondo intocable: protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E), dataset N=500, reservadas N=6 -- FUERA."
  risk: low
  estimate: S
---

# TASK-0288 - [DECISION-0103][R1] Manejo graceful de JSON gobernado malformado

Origen: residual R1 declarado por el checker (Analista) en el veredicto de TASK-0287
(`Analista-TASK-0287-hook-fullmode-inventory-verdict.md`). Ante JSON gobernado malformado,
`validate_collaboration_state.py` y `prune_state.py --check` lanzan `JSONDecodeError` sin capturar
(traceback) en vez de un fallo graceful. No debilita C5 (el rechazo real es el exit!=0 y ocurre por
el camino no-bloqueante); es higiene de manejo de errores. Follow-up no bloqueante.
