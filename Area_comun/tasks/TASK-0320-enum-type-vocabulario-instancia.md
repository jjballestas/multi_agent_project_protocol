---
task_id: TASK-0320
file: Area_comun/tasks/TASK-0320-enum-type-vocabulario-instancia.md
title: "El enum hermano TYPE_VALUES conserva fichas de ceremonia de instancia (6 en castellano): sacarlas por la misma via ya probada en TASK-0318"
status: ready
type: infra
owner: Codex
reviewer: Analista
priority: normal
project: multi_agent_project_protocol
spec_id: SPEC-MEMORIA-HIBRIDA
relates_to:
  - TASK-0318
  - SPEC-MEMORIA-HIBRIDA
created_at: 2026-08-06
intake:
  type: infra
  goal: >
    TASK-0318 saco de `STATUS_VALUES` todo el vocabulario de instancia y construyo el mecanismo para
    declararlo en la politica gobernada. Su enum HERMANO no se toco por estar fuera de alcance, y
    conserva el mismo defecto: `TYPE_VALUES` (69 valores) incluye fichas de CEREMONIA de ESTA
    instancia -- `CAMBIO`, `CONSULTA`, `DIRECTIVA`, `FIRMA`, `REPORTE`, `RESPUESTA` en castellano,
    mas `COORD`, `GO`, `RECONCILE`, `RESP`. Sobreviven por la misma razon que sobrevivieron los 6 de
    `status`: no son nombres de agente y ninguna regla los ve. El nucleo neutral no queda neutral,
    queda arbitrario, y ademas una instancia en otro idioma hereda ceremonia castellana que no usa.
    El mecanismo curativo ya existe, esta probado sobre el corpus real y tiene contrato de falsacion
    con dientes: esta tarea lo aplica al segundo enum.
  acceptance:
    - "AC1 (inventario declarado): antes de tocar nada, se clasifica cada uno de los 69 valores de TYPE_VALUES en NUCLEO (vocabulario generico del ciclo de vida y tipos de trabajo: feature, fix, infra, doc, review, handoff...) o INSTANCIA (ceremonia local de este hub). La lista se declara en el handoff. Los 10 del goal son el punto de partida, NO la lista cerrada: si hay mas, salen tambien."
    - "AC2 (misma via, no una nueva): el vocabulario de instancia se declara en Area_comun/protocol/MEMORY_INDEX_POLICY.json en un campo hermano de extra_status_values, con las MISMAS tres restricciones ya probadas: union cerrada en carga desde el artefacto gobernado (sin entorno, sin flags, sin aprender del corpus), template VACIO, y guardas de tamano y contenido heredadas."
    - "AC3 (mecanismo matable): contrato de falsacion permanente que mute la politica quitando un valor declarado y EXIJA que el artefacto que lo usa vuelva a warnear. Declarado en el registro y cableado en CI, exactamente como quedo el de status."
    - "AC4 (sin vocabulario muerto): se declara SOLO lo que el corpus usa de verdad. El handoff fija la linea base <declarados>/<en uso>/<muertos> igual que hizo TASK-0318 con 8/8/0, para que una deriva futura sea visible."
    - "AC5 (el conteo no empeora): el build del corpus real en CLON LIMPIO no gana warnings frente a la linea base vigente (219). Si sacar un valor del nucleo destapa artefactos que lo usaban, se declara en la politica; si el conteo sube y se queda arriba, el AC no se cumple."
    - "AC6 (sin regresion): suite completa verde, drift --fast y --full exit 0, scan_domain_neutrality, scan_encoding y validate exit 0, todo por exit code en clon limpio."
  verification_cmd:
    - "python scripts/memory/test_memory_db.py"
    - "python scripts/memory/build_memory_db.py --root ."
    - "python scripts/check_falsification_contracts.py --root . --inventory"
  scope_routes:
    - scripts/memory/build_memory_db.py
    - scripts/memory/test_memory_db.py
    - Area_comun/protocol/MEMORY_INDEX_POLICY.json
    - Area_comun/protocol/MEMORY_INDEX_POLICY.template.json
  out_of_scope: >
    Extender el mecanismo a otros enums (priority, canonicality, retention_class) sin decision
    propia; TASK-0317; los residuales R2 y R6 del ledger de SPEC s.16.7; y reabrir nada de lo que
    TASK-0318 cerro para `status`.
  risk: low
  estimate: M
notes: >
  Encargo R1 del veredicto OK-CERRABLE del Analista sobre TASK-0318
  (Area_comun/artifacts/Analista-TASK-0318-enum-instancia-verdict.md). Pidio explicitamente que
  fuera tarea propia y no residual dormido, con este argumento que comparto: es el mismo defecto que
  se acaba de cerrar y el mecanismo para curarlo ya existe, esta probado sobre el corpus real y tiene
  el negativo permanente que lo hace matable. Dejarlo como residual seria haber construido la cura y
  no aplicarla.
  Riesgo bajo precisamente porque no hay que disenar nada: se replica una via ya verificada. El
  trabajo real esta en AC1, la clasificacion honesta de los 69 valores, que es juicio y no mecanica.
  El ledger de residuales del port (SPEC s.16.7) registra que el motor no se declara listo para
  exportar a instancias mientras esta tarea y TASK-0317 sigan abiertas.
