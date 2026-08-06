---
task_id: TASK-0318
file: Area_comun/tasks/TASK-0318-enum-status-extensible-por-instancia.md
title: "Vocabulario de estado extensible por instancia: sacar los 6 valores de instancia que quedan en STATUS_VALUES sin perder validacion, via MEMORY_INDEX_POLICY.json con contrato de falsacion"
status: in_progress
type: infra
owner: Codex
reviewer: Analista
priority: normal
project: multi_agent_project_protocol
spec_id: SPEC-MEMORIA-HIBRIDA
relates_to:
  - TASK-0314
  - TASK-0316
  - SPEC-MEMORIA-HIBRIDA
created_at: 2026-08-06
intake:
  type: infra
  goal: >
    Cerrar el "medio purgado" que dejo TASK-0316. Su AC4 saco de `STATUS_VALUES` los 2 valores de
    vocabulario de instancia que la regla de identidad podia cazar, pero **quedan 6 del mismo
    vocabulario** (`GO-PROMOVER-OFF`, `OK-CERRABLE`, `OK_CERRABLE`, `cambio-requerido`,
    `hallazgo-confirmado`, `draft-reviewed-informal`) que sobreviven solo porque no son nombres de
    agente. El nucleo neutral no queda neutral: queda ARBITRARIO. Ademas la purga parcial devolvio el
    conteo de warnings del build de 219 a 227 sobre 8 borradores del area personal. La salida no es
    elegir entre las dos cosas: es que el vocabulario de instancia se DECLARE en la politica
    gobernada de la instancia y el nucleo se quede solo con el vocabulario del ciclo de vida de
    AGENTS.md s.6.
  acceptance:
    - "AC1 (nucleo neutral de verdad): STATUS_VALUES del nucleo queda SOLO con vocabulario del ciclo de vida de AGENTS.md s.6 y equivalentes genericos. Los 6 valores de instancia listados en el goal salen, junto con los 2 que ya salieron. La lista final del nucleo se declara explicita en el handoff."
    - "AC2 (restriccion i, aditivo y cerrado en carga): la union se calcula UNA sola vez desde Area_comun/protocol/MEMORY_INDEX_POLICY.json, artefacto gobernado, atestado y ya dentro del conjunto escaneado por neutralidad. Declarar un valor es un acto auditable. PROHIBIDO: variables de entorno, flags de CLI, o aprender valores del corpus."
    - "AC3 (restriccion ii, el mecanismo debe ser MATABLE): contrato de falsacion permanente que mute la politica quitando un valor declarado y EXIJA que el artefacto que lo usa vuelva a warnear. Sin ese negativo, extra_status_values es indistinguible de desactivar la comprobacion. Declarado en el registro de contratos (check_falsification_contracts --inventory) y cableado en CI, igual que se hizo en TASK-0316."
    - "AC4 (restriccion iii, todo el vocabulario): la via absorbe los 6 + los 2, no solo los 2. Si al terminar queda un solo valor de instancia dentro del nucleo, el AC no se cumple."
    - "AC5 (template vacio): MEMORY_INDEX_POLICY.template.json envia extra_status_values VACIO; el archivo vivo del hub declara los suyos. Una instancia nueva nace sin vocabulario heredado."
    - "AC6 (el conteo vuelve y se deja escrito): el build del corpus real vuelve a 219 warnings SIN reintroducir vocabulario de instancia en el nucleo, medido en CLON LIMPIO y declarado en el handoff. El exito de esta tarea se mide exactamente en eso."
    - "AC7 (sin regresion): suite completa verde, drift --fast y --full exit 0, scan_domain_neutrality y scan_encoding exit 0, validate exit 0, todo por exit code en clon limpio."
  verification_cmd:
    - "python scripts/memory/test_memory_db.py"
    - "python scripts/memory/build_memory_db.py --root ."
    - "python scripts/check_falsification_contracts.py --root . --inventory"
    - "python scripts/scan_domain_neutrality.py --root ."
  scope_routes:
    - scripts/memory/build_memory_db.py
    - scripts/memory/test_memory_db.py
    - Area_comun/protocol/MEMORY_INDEX_POLICY.json
    - Area_comun/protocol/MEMORY_INDEX_POLICY.template.json
  out_of_scope: >
    Reintroducir en el nucleo cualquiera de los 8 valores de instancia; extender el mecanismo a otros
    enums (type, priority, canonicality, retention_class) sin decision propia; TASK-0317; los
    residuales R1, R2, R3, R6 y R5-0316 del ledger de la SPEC s.16.7.
  risk: medium
  estimate: M
notes: >
  Encargo C2 del veredicto r2 del Analista sobre TASK-0316
  (Area_comun/artifacts/Analista-TASK-0316-remediacion-r1-verdict.md s.4.2 y s.5.3). La propuesta
  `extra_status_values` la puso el Arquitecto y el checker la ACEPTO EN SU FORMA advirtiendo que, tal
  como estaba enunciada, si abre la puerta que el propio Arquitecto temia: un enum extensible sin
  limite deja de ser validacion y pasa a ser documentacion, porque la pregunta "es este un estado
  conocido?" respondera que si por construccion. Las tres restricciones de AC2, AC3 y AC4 son suyas y
  son lo que lo devuelve a ser validacion. La de AC3 es la que de verdad muerde: sin un negativo
  permanente que demuestre que quitar un valor declarado vuelve a producir el warning, el mecanismo y
  apagar la comprobacion son indistinguibles desde fuera. C1 (registrar el delta 219 -> 227) ya esta
  hecho en SPEC-MEMORIA-HIBRIDA s.16.7.
