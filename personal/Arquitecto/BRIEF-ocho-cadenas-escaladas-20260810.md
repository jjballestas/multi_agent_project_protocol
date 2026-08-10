# Brief de decision -- las ocho cadenas escaladas (2026-08-10)

Preparado para que la vuelta del operador sea productiva. **Cada fila es una decision suya**; yo no
promuevo ni cierro ninguna sin respuesta. Estado del hub al escribirlo: buzon vacio, cero claims,
las cuatro puertas en verde, poda al dia, ambos peers ociosos.

## El diagnostico comun

**Cinco de las ocho comparten causa**: la remediacion **estrecha el dano sin cerrar la clase**. En
todas, el eje que el encargo nombro se cerro y el que no se nombro quedo abierto. No son ocho
incidentes: son una tesis confirmada ocho veces.

## Las ocho, con lo que decide cada una

| Tarea | Que quedo abierto | Decision que pido | Mi recomendacion |
|---|---|---|---|
| **0328** | corpus medido dos veces con CERO positivos previos: su "0 perdidas" no significa nada | tercera vuelta o cierre | **tercera vuelta**. Cerrar con residual significa enviar un gate de PII ciego a identificadores validos: eso es agujero, no residual |
| **0329** | el guardian lee al gemelo por un marcador de texto truncado | tercera vuelta acotada | **si**: leer estado efectivo, no marcador. Es barato |
| **0332** | la matriz prometida era una ESTRELLA; la conjuncion nunca probada ocultaba un email real con 72 pruebas en verde | tercera vuelta | **si**: derivar el corpus del producto, no muestrear ejes |
| **0342** | la paridad deriva de UNA LINEA de formato fijo | tercera vuelta acotada | **si**: leer la politica por valor efectivo |
| **0343** | el criterio se satisface con un evento AJENO | tercera vuelta acotada | **si**: estrechar la ventana de observacion |
| **0345** | poblacion ya derivada y producto real 7x4, pero **las 4 formas siguen siendo una lista**; y los detectores se atan a coordenadas incidentales (nombre de variable, disposicion de la sentencia) | cerrar con residual declarado, o abrir tarea de parser | **cerrar con residual**: el eje de la forma no se cierra enumerando, y una quinta vuelta produce una quinta grafia. Parsear PowerShell de verdad es tarea nueva y grande |
| **0353** | derivacion muestreada de UN solo turno; y **regresion de clase**: un turno que salta la puerta de decision se acepta y se commitea | tercera vuelta con criterio cambiado | **si, pero cambiando el predicado**: no "claves que la validacion EXIGE" sino "claves que cualquier puerta LEE". Son 13, no 1. Salida intermedia: cerrar solo las que gobiernan seguridad (`actions`, `decision_refs`, `gate`) y declarar las otras cuatro |
| **0354** | el descubridor ancla al principio de linea y no ve un runner que el propio workflow invoca; y una indireccion local lo ciega | vuelta 3 acotada a G1, G2 aparte | **si**: G1 se cierra barato (reconocer cualquier posicion y `-m`, y **atar el contador**, hoy 72->71 pasa en silencio). G2 -- clausura transitiva de imports -- es otra bestia y merece tarea propia |

## Lo que NO depende de estas ocho

- **Facturacion de Actions**: ya **no** es la llave de casi nada. De las cuatro tareas que declare
  congeladas, TRES tenian su verde en el historial (0344 cerrada con el, 0345 y 0347 acreditadas).
  Solo **0340** la necesita de verdad.
- **0347**: bloqueada por 0353, no por CI.
- **Nueve tareas en `proposed`**, en pausa por recomendacion mia hasta cerrar la cascada.

## Tres hallazgos de harness sin contratar

Borrador en `D:/Aegis_Scratch/protocol/drafts/`. Los tres serializan por una condicion mas gruesa
que la propiedad que protegen:

1. El intent `decision` exige `PROJECT_STATE.json` ENTERO: cualquier tarea reclamada bloquea el
   registro de cualquier decision. Me mordio dos veces en diez minutos.
2. `active_external_claim` sale en CUATRO situaciones distintas con la misma cadena: no se puede
   distinguir conflicto real de bailout conservador.
3. El timeout de post-entrega (300 s fijos) IGNORA la extension por liveness que si aplica en la
   fase de exec. Falla justo en las entregas mas densas.

## Y lo que aprendi yo, que es lo que mas cambia como trabajo

De las correcciones del checker de hoy, **las tres mas caras fueron de encuadre mio**, no de
implementacion ajena: descarte 339 corridas de CI sin abrir ninguna; envenene un ancla de review
dando un commit con el gate en rojo; y rutee un cierre al unico agente sin la capability. Las tres
estan en memoria con su regla.
