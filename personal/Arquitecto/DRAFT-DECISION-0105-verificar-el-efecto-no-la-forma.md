# DRAFT-DECISION-0105 -- verificar el efecto, no la forma

> **Iteracion 2 del borrador.** Reescrito tras el veredicto CHANGE-REQUIRED del Analista
> (`Area_comun/artifacts/Analista-DECISION-0105-generalizacion-verdict.md`, 2026-08-08).
> Estado: **NO propuesto**. Pendiente de re-juicio del checker antes de ir al operador.

## Que cambia respecto a la iteracion 1, y por que

El checker falsó la regla que cargaba el peso **usando el propio mecanismo que la certificaria**, y
desinfló el titular. Lo acepto entero. Los cambios grandes:

- **R2 gana su cuarta palabra.** Declarado, ejecutado y exigido **no implica ASERTADO**.
- **El recuento baja de "catorce ocurrencias" a OCHO TAREAS.** Cuatro filas eran la misma TASK-0330
  y dos la misma TASK-0329. Cae la coletilla "en tareas sin relacion entre si", que era falsa.
- **La ocurrencia 11 sale** y la 9 pasa a la seccion de huecos.
- **El artefacto se PARTE**: DECISION para lo que tiene predicado binario; guia y plantilla de
  review para lo que no.
- Entra la regla que faltaba: **la aceptacion cita un efecto medido**. Es la unica que habria cazado
  mi propio fallo, y la que me ha vuelto a morder hoy con CI.

## El patron, en una frase

**Confundir que un mecanismo EXISTA con que ACTUE.** El mecanismo esta presente, declarado, listado
o mergeado; y no ejerce ningun efecto sobre el veredicto.

## Las tres manifestaciones

La iteracion 1 declaraba dos y tres ocurrencias no cabian. Son tres:

**M1 -- verificadores que no verifican.** Contratos, gates y CI que emiten verde sin haber
comprobado lo que dicen comprobar.

**M2 -- controles de produccion que no controlan.** Guards que aparentan dar una garantia y no la
dan. No son verificadores: son codigo que corre en produccion.

**M3 -- lo que existe en el repositorio no es lo que corre.** Despliegue y estado: el arreglo esta
en `done` y el proceso vivo no lo tiene.

## La evidencia, recontada

**Ocho tareas, tres manifestaciones.** El recuento por FILAS inflaba: cuatro filas eran TASK-0330 y
dos eran TASK-0329.

| Tarea | Manif. | Que ataba, y que deberia atar |
|-------|--------|-------------------------------|
| TASK-0330 | M1 | (a) **23 de 37 contratos declarados** con runner que CI no ejecutaba nunca, uno **dos semanas en rojo**; (b) el checker exigia el literal `$expires -gt $now` y la forma equivalente fail-closed lo rompio; (c) el fixture asumia un mundo sin `work_scope` obligatorio; (d) **el cableado mismo**: los runners entraron en un paso `run:` sin `shell:` declarado, y el job salio `success` **con dos de tres runners en ROJO dentro** (medido en CI real, run 31195169744) |
| TASK-0329 | M1 | (a) la exencion paso de fichero entero a pares **(linea, termino)**: otra tarea anadio ~56 lineas encima y ocho ocurrencias legitimas e **intactas** pusieron el gate en rojo; (b) el contrato anadido **para impedir la cuarta divergencia** entre los dos escaneres ata un regex de indentacion fija: un desliz de **dos espacios** produce veredictos divergentes con la suite verde |
| TASK-0324 | M1 | ataba el HELPER puro mas `assert linea in source`; un mutante de CODIGO MUERTO -- cableado presente pero inalcanzable -- sobrevivia |
| TASK-0325 | M1 | el detector buscaba `ast.Continue`; un bypass con `break` colaba **un email por el gate de PII** con 64 tests en verde |
| TASK-0335 | M1 | (a) la asercion exige una POSICION de subcadena en el log y otra tarea metio campos en medio; (b) la mitad mutante de `retry-ledger-head-defer-order` era **VACUA**: comparaba contra una subcadena que ningun log real satisface, asi que pasaba hiciera lo que hiciera produccion |
| TASK-0333 | M1 | el gate leia el arbol vivo y no el **mirror del runtime** que `new_instance.py` copia a cada instancia nueva: se cerro el agujero en la mitad que no se exporta |
| TASK-0331 | M2 | el guard aparentaba exclusion mutua **sin darla**: check-then-act sin atomicidad; dos peers arrancaron el MISMO segundo |
| (guard de residuo) | M2 | decision **por-par** -- este mensaje contra estas rutas -- tomada sobre una propiedad **global**: el arbol esta sucio. Medido: un mensaje de una tarea diferido por ficheros de otra, y por correo dirigido a otro agente |
| (despliegue) | M3 | 0321, 0324 y 0331 en `done`/`in_review` y **NO corriendo**: los crons cargan el `.ps1` al arrancar |
| (CI, 2026-08-08) | M1+M3 | **300 runs consecutivos sin un solo verde durante seis dias**, y nadie lo miro: el gate canonico crasheaba por una dependencia que CI no instala, mientras los tres agentes declarabamos verde desde clon limpio local |

**Tres de los seis rojos de la suite revivida los causamos NOSOTROS** con cambios correctos: 0316
hizo obligatorio un parametro, 0319 reordeno un reseteo, 0321 anadio campos a una linea de log.

**Y hay recursion, tres veces.** TASK-0330 cerraba "declarado no es verificado" y entrego "listado
no es exigido". TASK-0329 lo hizo dos veces en la misma entrega. Yo enuncie el principio en la
iteracion 1 de este documento y **acto seguido lo incumpli** al aceptar 0330 comprobando que los
runners APARECIAN en el workflow. Lo cazo un checker independiente midiendo el CI real, no la regla.

## Lo que se propone -- PARTIDO, y esta es la decision de forma

El checker lo dijo sin rodeos y tiene razon: **publicar nueve reglas de las que siete no tienen
predicado mecanico crearia siete reglas declaradas-y-no-ejecutadas, que es exactamente el defecto.
Seria la ocurrencia siguiente, firmada por el protocolo.**

### Van a DECISION: las tres con predicado binario

**D1 -- Un contrato declarado debe ser EJECUTADO, EXIGIDO y EJERCIDO.**
Las tres primeras palabras no bastan y esta MEDIDO: dejar una frontera declarada presente byte a
byte pero inalcanzable (`if False:`) deja el paso de CI en **exit 0**, el inventario en
`58/58 missing=0` y el guardian imprimiendo OK.
**Predicado:** rodear una frontera declarada de `if False:` debe poner el gate **ROJO**; y el runner
debe reportar los casos EJERCIDOS contra cada frontera declarada, no solo su presencia.

**D2 -- Mergeado no es desplegado; el orden es ratificacion -> despliegue -> comprobacion.**
**Predicado:** el estado de despliegue se comprueba por COMPORTAMIENTO -- un campo de log, un lock,
un id de corrida -- nunca por el log de git. Todo pendiente de despliegue lleva **dueno y
caducidad**, y al vencer escala.

**D3 -- Una aceptacion cita un efecto MEDIDO.**
La regla que faltaba, y la unica que habria cazado mi propio fallo. Quien acepta, ratifica o cierra
cita un **exit code de una corrida concreta o un id de corrida de CI**, nunca una lectura del diff
ni la afirmacion del maker. Las otras reglas atan al maker o al mecanismo; ninguna ataba al que
acepta, que es donde fallo yo dos veces en dos dias.
**Predicado:** un artefacto de ratificacion sin efecto medido citado no cierra.

### Van a GUIA y a la PLANTILLA DE VEREDICTO del checker: las demas

No tienen predicado mecanico hoy. Su sitio es donde se **ejercen en cada review** -- y ese ejercicio
ES su ejecucion -- no un documento que nadie ejecuta:

- **G1 -- el negativo ata el EFECTO observable, no la forma sintactica.** Las dos formas correctas
  deben **diferir en el eje atado**, y no las elige el maker.
- **G2 -- el mutante obligatorio incluye la INALCANZABILIDAD**, no solo el borrado. Presupone un
  **llamador vivo**: primero el chequeo barato de que produccion recorre ese camino.
- **G3 -- verdad vacia prohibida.** Respaldada por la mitad mutante vacua de 0335.
- **G4 -- un guard declara QUE garantiza y lo demuestra**, reconciliado con lo que asumen sus
  llamadores; rebajar la garantia declarada no es cumplir.
- **G5 -- la direccion del fallo es del par CAMBIO-CONSUMIDOR.** Enumerar consumidores **no cierra
  la clase**: para miembros futuros hace falta un invariante estructural.
- **G6 -- el gate no es el fichero que editaste: enumera sus GEMELOS.** Mismo limite que G5, y su
  coste **escala con la adopcion**, que es la meta de la fase.
- **G7 -- estrechar la forma no es atar la propiedad.** El criterio debe sobrevivir a un cambio de
  coordenada, de orden y de formato. *(La iteracion 1 enumeraba tres ejes, que es una forma:
  reproducia el defecto que nombra. Aqui el ejemplo va como ejemplo, no como definicion.)*

## Coste y contrapartida

**Un rojo que se queda rojo deja de leerse.** Con un solo `main` y varios agentes gateados por la
misma senal, un rojo persistente convierte el gate de **toda** tarea no relacionada en "rojo
conocido, sigo". Ese es el mecanismo por el que el arreglo se pospone para siempre. **Hoy lo hemos
vivido**: seis dias de CI rojo que nadie miraba. Por eso D1 y D2 exigen **presupuesto de rojo**:
dueno, caducidad y escalado al vencer.

**G1 y G2 son coste puro sobre codigo muerto.** Medido: media de un contrato ataba un camino de
PowerShell que ningun llamador de produccion recorre.

**El coste de G6 escala con el exito.** Los gemelos se GENERAN: cada instancia nueva copia el
mirror.

**G5 obliga a elegir y a pagar:** invariante estructural (caro) o checklist (barata y no cierra la
clase). No vale dejarlo ambiguo.

## Lo que esto NO cubre

Declarado, para que "tres manifestaciones" no se lea como cobertura:

1. **El denominador.** Todas las ocurrencias son sobre mecanismos que EXISTEN. Ninguna sobre el que
   **deberia existir y nunca se declaro**.
2. **La capa de ledger, mailbox y atestacion: CERO ocurrencias examinadas** -- la capa para la que
   existe este protocolo. El patron es al menos igual de probable ahi: un `submit_intent` que sale 0
   sin que el evento aterrice es exactamente "el mecanismo reporta exito sin el efecto".
3. **El texto del propio protocolo.** `AGENTS.md` y las DECISIONes contienen reglas que ningun gate
   ejecuta -- la memoria dorada, la narracion minima. Por esta misma tesis son
   declaradas-no-exigidas. **Queda FUERA de alcance en esta decision**, y se declara como tal.
4. **Mecanismos que pasan porque nunca disparan.** Guards con ventana, caducidades, techos de
   reintento: uno que jamas se activa es indistinguible de uno que funciona.
5. **El estado de reintento no reconciliado** (13 entradas huerfanas apuntando a mensajes archivados
   o inexistentes). Era la ocurrencia 9 de la iteracion 1; **no la sostiene ninguna regla de las
   propuestas**, asi que sale de la evidencia y queda aqui como instancia sin regla.

## Lo que se retiro, y por que

**La ocurrencia 11 (TASK-0334) no pertenece al patron.** El cambio ACTUO, y bien, en los dos
consumidores; el defecto era que querian cosas opuestas. Eso es acoplamiento y requisitos, no
confundir existir con actuar. Se conserva como leccion bajo G5, no como instancia. Y su contrato
fija consumidores CONOCIDOS sin cuantificar sobre la clase: **esa parte sigue abierta**.

## Pendiente antes de proponer formalmente

1. Re-juicio del checker sobre esta iteracion 2.
2. **TASK-0341** debe cerrar antes de que D1 se pueda proponer con su predicado: hoy el certificador
   del que D1 depende es ciego a la frontera muerta y fragil al reformateo.
3. Decidir con el operador si la guia G1-G7 se publica como tal o entra en la plantilla de veredicto
   del checker.
