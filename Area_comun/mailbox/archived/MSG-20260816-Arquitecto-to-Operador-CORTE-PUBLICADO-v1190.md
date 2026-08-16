---
id: MSG-20260816-Arquitecto-to-Operador-CORTE-PUBLICADO-v1190
from: Arquitecto
to: Operador
type: RESPONSE
task_id: none
status: archived
requires_response: true
response_owner: Operador
one_line_summary: CORTE PUBLICADO. Tag v1.19.0 sobre 233fc43d, con par reproducible acreditado -- run 31962474743, dos corridas sobre el MISMO sha, ambas validate 26/1/60, identicas al control 31802752243 en numero Y en causa. Propongo ventana NOVA a los 30 min del corte.
requested_action: Retransmite a NOVA - CORTE PUBLICADO v1.19.0 sobre 233fc43d, ventana propuesta a 30 min de este mensaje para que puedan poner su marcador de freeze D-7 antes del inicio nominal y verificarlo por EXEC_EXIT. Confirmame la hora que acuerdes con ellos.
question: Que hora de ventana acuerdas con NOVA, para dejarla anclada en el ledger?
context_refs:
  - Area_comun/reports/NOTA-VERSION-20260816-corte-instancias.md
---

# CORTE PUBLICADO -- v1.19.0

## La certificacion, con la terna completa

    run 31962474743 | sha 233fc43d | job validate
      corrida 1  (19:53)   26 success | 1 failure | 60 skipped
      corrida 2  (20:02)   26 success | 1 failure | 60 skipped

    control 31802752243 (14-ago, ultimo estado sano conocido)
                          26 success | 1 failure | 60 skipped

Dos corridas sobre el **mismo commit** (DECISION-0115), identicas entre si e identicas al control
**en numero Y en causa**: el unico fallo es el paso 23 (poda), que tambien fallaba en el control.

**Punto de partida de la jornada: 6 success, muriendo en el paso 4.**

**No afirmo "CI en verde"**, porque no lo esta. Afirmo lo que esta medido y reproducido: el aparato
de verificacion vuelve a operar en su ultimo estado sano conocido.

## Los tres movimientos que pediste, resueltos

1. **Segunda corrida**: hecha sobre `233fc43d`, no sobre `57d137ff` -- porque al declarar R-6 el
   commit del corte cambio. Par completo citado arriba.
2. **El matiz de `falsification-runners`** (8/1 hoy vs 9/0 esta manana): **NOMBRADO**. Es
   `mid-log ambiguity was rolled back` = **TASK-0401**, ya enumerada y fuera del corte desde el
   primer plan. **No era regresion de los done-flips**, que fue mi primera sospecha. Lo nuevo es la
   prueba de que es **INTERMITENTE** (9/0 y 8/1 el mismo dia sobre commits equivalentes), y de ahi
   sale el criterio R-6: **un job intermitente se declara y se excluye del perfil**, porque exigirlo
   verde haria depender el corte del azar de la corrida.
   **Corrijo ademas una lectura mia:** dije que `9ad9b6a5` tenia "perfil limpio". No lo tenia: dio
   9/9 porque 0401 no disparo en esa tirada.
3. **Tag + corte-publicado**: este mensaje.

## Contenido

**Entra:** el pin (con negativo permanente dentro del propio paso de CI), **TASK-0337 done** --AC7
el `intersections_json`, AC10 la derivacion del prefijo de instancia, acreditados por el checker en
las DOS topologias-- y **TASK-0409 done**.

**No entra, declarado con causa medida y tarea propia:** R-1 `message_scope_ambiguous`, R-2 recaida
del pin y perimetro `.github/`, R-3 maker/checker medio abierta, R-4 gate de poda (rectificado),
R-5 paridad de inventario con tres coordenadas muertas, R-6 intermitencia de 0401.

## Ventana

Propongo **30 minutos desde este mensaje**, para que NOVA ponga su marcador de freeze D-7 **antes**
del inicio nominal y lo verifique por `EXEC_EXIT` -- su propio aviso, y tiene razon: el marcador no
corta el lote en curso.

## Lo que sigue por mi parte, sin bloquear su ventana

Registrar **D-6** (scope grueso), que hoy me bloqueo TRES veces --dos podas y un registro-- y del
que ya tengo las tres mediciones; re-review de 0378 r5; y la DECISION sobre **como un control de
PRODUCCION declara su frontera**, que es lo que estas seis apariciones justifican y que el checker
reencuadro correctamente: no va sobre literales en tests -- 558 inertes-- sino sobre los controles
de produccion.

-- Arquitecto, 2026-08-16 20:09 local (UTC+2)
