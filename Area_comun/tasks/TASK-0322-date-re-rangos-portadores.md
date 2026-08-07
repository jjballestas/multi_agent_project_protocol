---
task_id: TASK-0322
file: Area_comun/tasks/TASK-0322-date-re-rangos-portadores.md
title: "Estrechar DATE_RE con validacion de rangos de componente: el conjunto de confianza se reduce ~3,7e3 veces (la densidad de portadoras NO baja; 2,9/0,05 pct son relativos al muestreador del AC1)"
status: review_approved
type: infra
owner: Codex
reviewer: Analista
priority: normal
project: multi_agent_project_protocol
spec_id: SPEC-MEMORIA-HIBRIDA
relates_to:
  - TASK-0317
  - SPEC-MEMORIA-HIBRIDA
created_at: 2026-08-06
intake:
  type: infra
  goal: >
    TASK-0317 anclo la exencion del heuristico de telefono en `DATE_RE`, que es la decision correcta y
    esta cerrada. Pero `DATE_RE` acepta hoy combinaciones que no son fechas reales (no valida rangos:
    admite meses, dias, horas o minutos fuera de dominio), y toda cadena que la gramatica acepta queda
    EXENTA del chequeo. Estrechar la gramatica con validacion de rangos reduce el lenguaje aceptado
    unas 3.695 veces y el cardinal absoluto de portadoras unas 3.699 veces (3,6 ordenes de magnitud).
    La densidad de portadoras del lenguaje no baja: las cifras 2,9 y 0,05 por ciento pertenecen solo
    al muestreador determinista del AC1. El residual estructural son 2 de las 33 formas del lenguaje:
    forma con dos puntos, fraccion de 5 o 6 digitos y offset numerico negativo.
  acceptance:
    - "AC1 (medicion de partida): se reproduce la cifra del checker sobre la gramatica actual (2,9 por ciento de portadoras dentro del muestreador determinista, no como densidad del lenguaje) y se declara el metodo, para que el despues sea comparable."
    - "AC2 (rangos): DATE_RE valida dominios reales -- mes 01-12, dia 01-31, hora 00-23, minuto y segundo 00-59, offset con horas 00-14 -- sin dejar de aceptar ningun formato legitimo."
    - "AC3 (sin regresion en el corpus): los valores de created_at/updated_at/closed_at del corpus real que hoy se aceptan siguen aceptandose, medido en CLON LIMPIO. Cero warnings nuevos de claves de fecha."
    - "AC4 (F2 sigue cerrada): los 11 vectores de cola del veredicto de 0314 siguen rechazados, y la exencion sigue sin permitir que una cadena con PII pase entera."
    - "AC5 (medicion final declarada): se declara el 0,05 por ciento dentro del mismo muestreador determinista, se nombra el residual como 2 de 33 formas (dos puntos + fraccion de 5 o 6 digitos + offset negativo) y se declara la reduccion absoluta aproximada de 3,7e3 veces; ninguna de las dos cifras muestrales se presenta como densidad del lenguaje."
    - "AC6 (sin regresion general): suite completa verde, build y drift exit 0, todo por exit code en clon limpio."
  verification_cmd:
    - "python scripts/memory/test_memory_db.py"
    - "python scripts/memory/build_memory_db.py --root ."
  scope_routes:
    - scripts/memory/build_memory_db.py
    - scripts/memory/test_memory_db.py
  out_of_scope: >
    Mover la exencion fuera del bloque del heuristico de telefono (eso lo fija el contrato R-N2, que
    entra en TASK-0317); reabrir nada de lo cerrado en 0314, 0317 o 0318; TASK-0320.
  risk: low
  estimate: S
notes: >
  Residuales R-N1 y R-N3 del veredicto r2 del Analista sobre TASK-0317
  (Area_comun/artifacts/Analista-TASK-0317-r2-anclaje-date-re-verdict.md). Va aparte y no como
  iteracion de 0317 porque es un cambio sustantivo de la gramatica con impacto medible, no un hueco
  del fix entregado: merece su propio contrato y su propia revision.
  El criterio de reparto que aplico el Arquitecto: si el hueco es SOBRE el fix recien entregado,
  entra en la tarea (asi entro R-N2, que fija la colocacion de la exencion); si tiene vida propia,
  sale a tarea nueva (asi salio S4 a TASK-0321, en otra funcion, y asi sale esto).
