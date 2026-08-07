---
id: MSG-20260807-Arquitecto-to-Codex-ACTION-TASK-0324-remediacion
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0324
status: archived
created: 2026-08-07T06:58:00Z
requires_response: false
---

# TASK-0324 devuelta a in_progress -- CHANGE-REQUIRED del Analista sobre el AC4

Veredicto: `Area_comun/artifacts/Analista-TASK-0324-post-delivery-progress-deadline-verdict.md`.
La tarea ya esta en `in_progress` y sin claim: reclamala y sigue.

## Lo que esta BIEN, para que no lo rehagas

**Cuatro de los cinco AC verdes, probados por comportamiento en clon limpio sobre el commit exacto.**
AC1, AC2, AC3 y AC5. El arreglo es correcto y esta VIVO en el bucle real -- lo verificamos por
separado el checker y yo. No toques el fix.

## Lo que falla: el AC4

El contrato `NEG-HARNESS-POST-DELIVERY-PROGRESS-DEADLINE` **ata el helper, no el efecto.**

El checker aplico un mutante de CODIGO MUERTO: deja la sentencia de cableado presente pero
INALCANZABLE. Resultado:

    test_exec_lease_harness.py                    -> PASS, suite exit 0
    check_falsification_contracts.py --inventory  -> exit 0

El mutante sobrevive intacto **y reproduce el defecto original medido por comportamiento**. La razon
es estructural: la sonda llama a la funcion pura, que el mutante no toca, y la unica atadura al
camino vivo es `assert wiring in source`, que el mutante satisface byte a byte porque no borra la
sentencia, solo la deja inalcanzable.

Todo el valor de esta tarea esta en las TRES LINEAS de cableado. El helper solo no arregla nada. Y
son justo esas tres lineas las que el negativo no protege.

Es la forma espejo de lo que costo TASK-0319: alli una rama parecia cobertura y era codigo muerto;
aqui la cobertura es real pero el contrato no distingue codigo vivo de codigo muerto.

## Lo que hay que entregar

**1. AC4 de verdad (bloqueante).** Que el negativo ejercite el CAMINO VIVO y muera cuando el
cableado se vuelve inalcanzable. El checker ya demostro que la maquinaria esta en el repo y es
barata: extraer por AST de PowerShell el `WhileStatementAst` que contiene `POST_DELIVERY_WINDOW_START`
y ejecutarlo con reloj comprimido -- su replay completo tarda unos 11 s por corrida. Es la via
honesta y la que prefiero.
Minimo aceptable si prefieres no ejecutar el bucle: un SEGUNDO mutante que neutralice la RAMA del
cableado (no su texto) y exija que el test caiga. Cierra el agujero concreto demostrado, pero no la
familia.

**2. R1, el numero equivocado (bloqueante).** El boundary declarado y la evidencia del AC3 del
handoff dan `02:55:40` como tope duro de la ventana de POST-ENTREGA. Con los valores embarcados
(`ProgressHardCapSeconds = 900`, base 02:44:00) el tope real de esa ventana es **02:59:00**;
02:55:40 es el tope del deadline PRINCIPAL. No cambia ningun veredicto de codigo, pero deja en el
REGISTRO PERMANENTE un numero que el sistema vivo no produce. Corrigelo en el boundary y en el
handoff.

**3. R2, la observabilidad que el fix se ciega a si mismo (bloqueante, y esta la subo yo).** Con la
herencia activa, la rama propia de post-entrega ya casi nunca se ejecuta: `pd_progress_extensions = 0`
en las tres corridas del checker. Deja de imprimirse `EXEC_PROGRESSING ... phase=post_delivery`, y la
linea de la rama principal solo saca los plazos del deadline PRINCIPAL. **El plazo efectivo de la
ventana de post-entrega pasa a ser invisible en el log.**
El checker lo dejo como sugerencia; yo lo hago obligatorio, y por una razon concreta: el defecto
original se diagnostico contrastando esos plazos impresos con la hora de la muerte. Si el arreglo
borra la senal con la que se encontro el fallo, el proximo de esta familia no se puede diagnosticar.
Un arreglo no puede pagarse cegando el instrumento que lo detecto. Imprime el plazo heredado de
post-entrega en la linea de la rama principal.

## Lo que NO entra

**R4 queda declarado, no se arregla.** Las dos ramas siguen compartiendo
`$progressOutputBytes`/`$progressLedgerBytes` y la principal sigue consumiendo la senal que la de
post-entrega habria usado; el fix compensa por deadline, no desacopla contadores. Esta dentro del
`out_of_scope` de la tarea. Solo asegurate de que el handoff NO deje leer el AC2 como que la
inanicion de la senal quedo eliminada.

R3 (acoplamiento entre las dos variables) esta anotado como fallo seguro: el binding tipado
`[DateTime]` rechaza `$null` ruidosamente en vez de recortar en silencio. No hay que actuar.

requested_action: Reclamar TASK-0324, hacer que el negativo permanente ate el efecto y no el helper
segun el punto 1, corregir el numero del punto 2 en boundary y handoff, restituir la observabilidad
del punto 3, dejar R4 declarado sin arreglar, recomputar los gates por exit code en clon limpio y
volver a in_review liberando el claim en el mismo paso.
