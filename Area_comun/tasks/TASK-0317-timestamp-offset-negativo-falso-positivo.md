---
task_id: TASK-0317
file: Area_comun/tasks/TASK-0317-timestamp-offset-negativo-falso-positivo.md
title: "Falso positivo del indexador: timestamps ISO-8601 con offset UTC negativo y fraccion larga se rechazan (el guion del offset puentea el patron de telefono)"
status: review_approved
type: infra
owner: Codex
reviewer: Analista
priority: normal
project: multi_agent_project_protocol
spec_id: SPEC-MEMORIA-HIBRIDA
relates_to:
  - TASK-0314
  - SPEC-MEMORIA-HIBRIDA
created_at: 2026-08-06
intake:
  type: fix
  goal: >
    Corregir el residual R5 que introdujo la remediacion r1 de TASK-0314. Al quitar (con razon) la
    exencion PII de las claves de fecha, esas claves pasan por `contains_pii`, y el patron de
    telefono `\+?\d[\d .()-]{7,}\d` incluye el guion en su clase de caracteres. En un timestamp con
    offset UTC NEGATIVO, ese guion puentea la fraccion de segundo con las horas del offset y la
    corrida de digitos alcanza el umbral de 9: el valor se rechaza aunque sea un timestamp
    perfectamente legitimo. Condicion exacta medida por el checker: offset negativo Y 5 o 6 digitos
    de fraccion (18 de las 333 cadenas de la familia de la gramatica). Importa porque
    `datetime.now(tz).isoformat()` de la biblioteca estandar produce exactamente
    `2026-06-19T09:28:23.123456-05:00` en cualquier instancia con huso de America.
  acceptance:
    - "AC1 (el caso legitimo se acepta): validate_metadata({'created_at': '2026-06-19T09:28:23.123456-05:00'}) lo ACEPTA, igual que el resto de la familia con offset negativo y fraccion de 5 o 6 digitos."
    - "AC2 (sin reabrir el agujero de F2): 2026-06-19Tperson@example.invalid y 2026-06-19T+34612345678 siguen RECHAZADOS, junto con los 11 vectores de cola del veredicto r2. La correccion no puede consistir en volver a eximir las claves de fecha ni en ensanchar DATE_RE."
    - "AC3 (test contra la familia, no contra ejemplos): la regresion engancha a la FAMILIA GENERADA de la gramatica (fechas x formatos de hora x fracciones x offsets), no a una lista de 6 ejemplos. El test actual test_supported_timestamps_and_medium_priority_are_accepted fija 6 formatos que esquivan justo la mitad negativa del espacio: esa cobertura aparente es parte del defecto."
    - "AC4 (sin regresion): suite completa verde, build del corpus real sin nuevos warnings de claves de fecha (hoy 0 de 219), --fast y --full exit 0, todo por exit code en clon limpio."
  verification_cmd:
    - "python scripts/memory/test_memory_db.py"
    - "python scripts/memory/build_memory_db.py --root ."
  scope_routes:
    - scripts/memory/build_memory_db.py
    - scripts/memory/test_memory_db.py
  out_of_scope: >
    Volver a eximir las claves de fecha del chequeo PII (reabriria F2); ensanchar DATE_RE; los
    residuales R1, R2, R3 y R6 del veredicto; TASK-0316; cualquier cambio fuera de scripts/memory/.
  risk: low
  estimate: S
notes: >
  Residual R5 del veredicto r2 del Analista sobre TASK-0314
  (Area_comun/artifacts/Analista-TASK-0314-remediacion-r2-verdict.md). Declarado con su etiqueta
  honesta: NO existia antes de d1252f4, lo introdujo la propia remediacion. No bloqueo el cierre de
  0314 porque tiene cero ocurrencias en el corpus anclado y FALLA CERRADO (descarta el campo y emite
  warning; no admite PII). El propio checker observa que R5 y el residual R1 son la misma superficie
  vista por sus dos lados: el patron de telefono es demasiado ancho, y unas veces se le exime de mas
  (R1, los valores con forma de id) y otras coge de mas (R5, el guion del offset). Quien implemente
  esto deberia mirar las dos caras antes de tocar el patron. Recomendacion explicita del checker: no
  declarar el motor "listo para exportar a instancias" mientras R5 siga abierto -- las instancias en
  husos de America lo pisarian de inmediato.
