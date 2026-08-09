# DRAFT-DECISION-0105 -- verificar el efecto, no la forma

> **Iteracion 3 del borrador.** Reescrito tras el veredicto CHANGE-REQUIRED de la iteracion 2
> (`Area_comun/artifacts/Analista-DECISION-0105-r2-verdict.md`, 2026-08-09 22:15).
> Estado: **NO propuesto**. El checker agoto sus dos iteraciones y escalo al operador; esta version
> existe para que esa decision sea barata, no para saltarsela.

## Que cambia respecto a la iteracion 2, y por que

El checker falso **las tres reglas** que la iteracion 2 proponia, cada una con el defecto que el
propio documento denuncia. Lo acepto entero. Los cambios grandes:

- **D1 cambia de predicado.** Nombraba una FORMA (`if False:`). La inalcanzabilidad es una familia
  de al menos seis formas, y las seis dejan certificador, guardian y runner en exit 0. El predicado
  nuevo es por **propiedad**: *toda frontera declarada debe haberse EJECUTADO al menos una vez
  durante la corrida de su `exercised_by`*. Medido: separa el baseline de las seis variantes,
  **7 de 7**, sin enumerar ninguna.
- **G2 y G3 se funden en D1 y desaparecen de la guia.** Frontera nunca ejecutada y frontera cuyo
  valor esperado no ocurre jamas son el mismo fallo -- la asercion no puede fallar -- y un solo
  mecanismo los mata.
- **D3 baja a CONDICIONAL.** Se cumplia en falso, y quien la incumplia era este documento: la mejor
  cita de su tabla no sobrevivia a la regla que propone.
- **D2 se queda solo con la mitad que tiene ejecutor nombrado.** La otra mitad enumeraba tres
  formas, que es el vicio que G7 condena.
- **El recuento sube a diecisiete tareas nombradas mas la instancia de CI**, y cada una es una fila.
- **El hueco 3 se BORRA**: la capa de ledger no esta inexplorada, es donde el arquetipo se cazo
  primero (TASK-0270, hace un mes). Entra un hueco nuevo: *el efecto medido cuya medicion no se
  puede obtener*.
- **Entra la evidencia de la noche del 09-ago**, que es la mas fuerte del corpus y la mas incomoda.

## El patron, en una frase

**Confundir que un mecanismo EXISTA con que ACTUE.** El mecanismo esta presente, declarado, listado,
mergeado o cableado; y no ejerce ningun efecto sobre el veredicto.

## Las tres manifestaciones

**M1 -- verificadores que no verifican.** Contratos, gates y CI que emiten verde sin haber
comprobado lo que dicen comprobar.

**M2 -- controles de produccion que no controlan.** Guards que aparentan dar una garantia y no la
dan. No son verificadores: es codigo que corre en produccion.

**M3 -- lo que existe en el repositorio no es lo que corre.** El arreglo esta en `done` y el proceso
vivo no lo tiene.

## La evidencia

**Diecisiete tareas nombradas mas la instancia de CI**, repartidas en tres manifestaciones. Cada
fila tiene id: si algo se cita como medido, entra como fila o deja de citarse.

| Tarea | Manif. | Que ataba, y que deberia atar |
|-------|--------|-------------------------------|
| TASK-0347 | M1+M3 | **el caso limite del corpus**: el job `validate` no sale verde desde el 2026-06-05, cuando ejecutaba DOS gates reales; hoy declara **77 pasos**. Un rojo aborta el job, asi que **ninguno de los 75 anadidos en dos meses ha sido observado pasar en CI**. Replica local a HEAD: 55 OK / 17 FAIL, y **doce** de los 17 por una sola causa medida por mutacion |
| TASK-0346 | M1 | de **66 runners cableados en el workflow, 35 no aparecen en el `verification_cmd` de ninguna tarea**: existen, corren, y ninguna aceptacion los mira. Es la forma general de la fila 0330(a), con denominador mayor |
| TASK-0330 | M1 | (a) **23 de 37 contratos declarados** con runner que CI no ejecutaba nunca, uno dos semanas en rojo; (b) el checker exigia el literal `$expires -gt $now` y la forma equivalente fail-closed lo rompio; (c) el fixture asumia un mundo sin `work_scope` obligatorio; (d) el cableado mismo: los runners entraron en un paso sin `shell:` y el **job** salio `success` con dos `Traceback` dentro |
| TASK-0344 | M1+M3 | `run_mailbox_status_cases.py` roto **en CI y en local** sin que nadie lo corriera, y su fixture llevaba tres semanas obsoleta por un cambio de TASK-0273 |
| TASK-0332 | M1 | el contrato prometia una matriz `prefijo x offset`; lo entregado variaba **un eje cada vez desde un centro** -- una estrella. La conjuncion de dos valores ya muestreados por separado nunca se probo y ocultaba un email real con **72 pruebas en verde** |
| TASK-0342 | M1 | la paridad entre los dos escaneres se deriva de **una linea de texto de formato fijo**; ademas el runner decia `OK` y salia 1 |
| TASK-0343 | M1 | el criterio del gate se satisfacia con un evento **ajeno**: observaba una ventana que no le pertenece. El eje fallido no esta en la condicion, esta en **que se le da a evaluar** |
| TASK-0329 | M1 | (a) la exencion paso de fichero entero a pares (linea, termino) y ocho ocurrencias legitimas e intactas pusieron el gate en rojo; (b) el contrato anadido para impedir la cuarta divergencia ata un regex de indentacion fija: **dos espacios** bastan para escapar |
| TASK-0328 | M1 | la medicion bidireccional se corrio **dos veces sobre corpus con cero positivos previos**: su "0 perdidas" no significaba nada. El instrumento media su propia ausencia |
| TASK-0324 | M1 | ataba el HELPER puro mas `assert linea in source`; un mutante de **codigo muerto** -- cableado presente pero inalcanzable -- sobrevivia |
| TASK-0325 | M1 | el detector buscaba `ast.Continue`; un bypass con `break` colaba **un email por el gate de PII** con 64 tests en verde |
| TASK-0335 | M1 | (a) la asercion exige una POSICION de subcadena en el log y otra tarea metio campos en medio; (b) la mitad mutante era **VACUA**: comparaba contra una subcadena que ningun log real satisface |
| TASK-0333 | M1 | el gate leia el arbol vivo y no el **mirror del runtime** que `new_instance.py` copia a cada instancia nueva |
| TASK-0270 | M1 | **la capa de ledger, y es de hace un mes**: un intent aplicado puede PERDER su evento si otro escritor cruza la ventana de append (exit 0, efecto en disco, evento ausente); y el reintento byte-identico es **skipeado por idempotencia de contenido** sin comprobar que el estado lo refleje (exit 0, cero eventos, estado sin cambiar). Su `intake.goal` dice, literal: *"ambos exitos aparentes"* |
| TASK-0331 | M2 | el guard aparentaba exclusion mutua **sin darla**: check-then-act sin atomicidad; dos peers arrancaron el MISMO segundo |
| TASK-0337 | M2 | el guard de residuo toma una decision **por-par** -- este mensaje contra estas rutas -- sobre una propiedad **global**: el arbol esta sucio. Medido dos veces, la segunda esta misma noche |
| TASK-0321 | M3 | anadio campos a una linea de log, quedo en `done`, y **no corria**: los crons cargan el `.ps1` al arrancar |
| (CI) | M1+M3 | **cero corridas verdes desde el 2026-06-05**. Dos causas distintas y consecutivas: hasta el 09-ago mediodia moria en un paso real; desde entonces **no arranca ningun paso** por bloqueo de facturacion |

**Tres de los seis rojos de la suite revivida los causamos NOSOTROS** con cambios correctos: 0316
hizo obligatorio un parametro, 0319 reordeno un reseteo, 0321 anadio campos a una linea de log.

**Y hay recursion, cuatro veces.** TASK-0330 cerraba "declarado no es verificado" y entrego "listado
no es exigido". TASK-0329 lo hizo dos veces en la misma entrega. Enuncie el principio en la
iteracion 1 y **acto seguido lo incumpli** al aceptar 0330 comprobando que los runners APARECIAN en
el workflow. Y en la iteracion 2 cite un `run_id` como efecto medido **sin abrirlo**, en el
documento que propone citar efectos medidos.

## La evidencia de la noche del 09-ago -- el caso limite

Es posterior al veredicto de la iteracion 2 y es la instancia mas fuerte del corpus, porque el
mecanismo que "existe sin actuar" no es un contrato ni un guard: **es el job de CI entero**.

```
gh run list --status success -L 3
2026-06-05T13:20   fb0d0f07   run 27017313818   success
   validate  success  (8 pasos)
      Validate repository dogfood instance     <- gate real
      Validate minimal example instance        <- gate real
```

Dos gates reales. El job de hoy declara **77 pasos `run:`**. Los otros 75 se anadieron despues y el
job no ha vuelto a salir verde. Como un rojo aborta el job, **ninguno de esos 75 ha sido observado
pasar**. Estan cableados, se citan en criterios de aceptacion, y no estan ejercitados.

Replica local del job a HEAD en checkout limpio: **55 OK / 17 FAIL**. De los runners que construyen
turnos de entrega:

    26 construyen turnos
       4 mencionan obstacles   ->   0 en rojo
      22 no lo mencionan       ->  15 en rojo

Un cambio **correcto** de produccion (`c725e9bd`, TASK-0259) endurecio una regla semantica y dejo
obsoletas **doce** fixtures a la vez. Nadie lo vio en dos meses.

**Y el numero lleva su propia leccion.** Escribi "quince" en el contrato, derivado de la
correlacion: construyen turnos, no mencionan `obstacles`, estan rojos. Al neutralizar la regla en
produccion y volver a correr los diecisiete, **doce** se vuelven verdes y **cinco** siguen rojos.
La correlacion **se parece** a la causa. Es el defecto de este documento cometido al escribir la
evidencia de este documento, y lo cazo la mutacion, no el razonamiento.

### Y el subcaso que da el predicado de D1 su mejor argumento

Siete de esos quince parecian de **causa independiente**. Fallan asi:

```json
{"case": "case_explicit_registry", "error": ""}
```

Un `assert` sin mensaje produce `AssertionError()` vacio y el runner reporta `str(exc)` -- cadena
vacia. **La puerta falla y no dice nada.** Ejecutada la linea a mano, la causa es la misma de los
otros ocho. El coste no fue tiempo de depuracion: fue que el censo se particiono mal y yo firme esa
particion en el alcance de una tarea.

**Una puerta que puede fallar sin decir por que no es una puerta.** Es el patron una capa mas
arriba: el diagnostico existe -- el runner tiene un campo `error` -- y no actua.

## Lo que se propone

### Va a DECISION con predicado por propiedad

**D1 -- Un contrato declarado debe ser EJECUTADO, EXIGIDO y EJERCIDO.**

**Predicado:** *ninguna frontera declarada puede computar como satisfecha si no se EJECUTO durante
la corrida del runner que su contrato declara como `exercised_by`.*

Medido sobre `NEG-NEUTRALITY-NESTED-IDENTITY`, con las dos fronteras presentes byte a byte en las
siete variantes:

| Variante | Forma | Fronteras presentes | Ejecutadas | Predicado por forma (`if False:`) | Predicado por propiedad |
|---|---|---|---|---|---|
| U0 | baseline | SI | SI | -- | **EJERCIDA** |
| U1 | `if False:` | SI | NO | detecta | **NO EJERCIDA** |
| U2 | `return` antes del cuerpo | SI | NO | **no detecta** | **NO EJERCIDA** |
| U3 | `@unittest.skip` | SI | NO | **no detecta** | **NO EJERCIDA** |
| U4 | `raise SkipTest` | SI | NO | **no detecta** | **NO EJERCIDA** |
| U5 | guarda por variable de entorno | SI | NO | **no detecta** | **NO EJERCIDA** |
| U6 | `while False:` | SI | NO | **no detecta** | **NO EJERCIDA** |

Un solo criterio, **siete de siete**, sin nombrar una sola forma sintactica. U1-U6 son vectores
obligatorios de la verificacion y **se declaran NO exhaustivos**: si manana aparece U7, el criterio
ya la cubre y la lista no hay que tocarla.

**Absorbe G2 y G3.** El mutante de inalcanzabilidad y la verdad vacia son el mismo fallo -- la
asercion no puede fallar -- y este predicado los mata a los dos.

**Absorbe tambien el subcaso de esta noche:** un caso que reporta fallo con diagnostico vacio no
acredita haber ejercido nada. Ejercida significa **ejecutada y observable**.

**Precondicion, y hay que decirla:** D1 no se puede proponer hasta que cierre **TASK-0341**, hoy en
`proposed` y sin reclamar. Y su acceptance debe nombrar **la propiedad, no la forma**: si se
contrata como *"el certificador debe enrojecer ante `if False:`"*, el maker entregara un detector de
`if False:` -- y lo entregara bien -- y las cinco formas restantes seguiran verdes.

### Va a DECISION solo la mitad con ejecutor nombrado

**D2 -- Mergeado no es desplegado.**

**Predicado (la mitad mecanizable):** todo pendiente de despliegue lleva **dueno y caducidad** en el
registro de la tarea, y el validador lo comprueba. **Ejecutor nombrado:** campo en el registro +
comprobacion en `scripts/validate_collaboration_state.py`. Sin cablearlo, es prosa, y no entra.

La otra mitad de la iteracion 2 decia *"se comprueba por comportamiento -- un campo de log, un lock,
un id de corrida"*. Eso es **una enumeracion de tres formas**. Reescrita como propiedad:

    El estado de despliegue se acredita con un artefacto que el codigo ANTERIOR no puede
    producir, y se declara por que no puede.

### Va a DECISION solo si sube con terna, ejecutor y fallback

**D3 -- Una aceptacion cita un efecto MEDIDO.**

La iteracion 2 la propuso asi: *"un exit code de una corrida concreta o un id de corrida de CI"*. Se
cumple en falso, y **lo cumplio en falso este documento**. Su fila de TASK-0330(d) citaba
`run 31195169744`. Resuelto:

```
run 31195169744    conclusion (corrida) : failure
                   conclusion (job)     : success   <- el nivel que sostiene el argumento
                   head_sha             : 1fb6594c  <- commit de MEMORIA sobre TASK-0325
```

Tres fallos en una sola referencia: la corrida no cubre el cambio aceptado; la cita es ambigua entre
dos veredictos que se contradicen; y el nivel que sostiene el argumento es el job, que D3 ni
menciona. **La afirmacion de fondo era cierta** -- el log de ese job contiene dos `Traceback` --
pero el defecto esta en la forma de la cita, que es justo lo que D3 pretende regular.

Re-citada con la terna que D3 deberia exigir, para que se vea la diferencia:

    run_id   31195169744
    job      falsification-runners  (conclusion: success)
    head_sha 1fb6594c  ->  NO es el commit del cierre de TASK-0330

La terna hace el defecto **visible en la propia cita**, que es todo lo que se le pide.

**Para subir a DECISION, D3 necesita tres cosas que hoy no tiene:**

1. **La terna:** `run_id` + `job` + `head_sha`, con `head_sha` == el commit que el cierre registra y
   `conclusion == success` **a nivel de job**.
2. **Un ejecutor:** hoy ningun gate lee los artefactos de ratificacion. La forma es barata -- el
   validador exige la terna en el artefacto y comprueba la correspondencia -- pero hay que
   escribirla y cablearla. Sin ejecutor, D3 seria la regla declarada-y-no-ejecutada numero ocho,
   con el agravante de ser la que mas se cita a si misma.
3. **Un fallback declarado para cuando el instrumento no esta.** Y hoy no esta: en el ancla, CI no
   arranca un solo job. La disyuncion "exit code **o** id de corrida" hace que toda aceptacion se
   cumpla por la rama local -- exactamente la que fallo durante seis dias mientras CI estaba rojo.
   **D3 adoptada tal cual bendice el fallo que la origino.**

Mientras no las tenga, **D3 se queda en guia**.

### Van a GUIA: cinco, no siete

G2 y G3 dejan de existir como guia: son el predicado de D1.

- **G1 -- el negativo ata el EFECTO observable, no la forma sintactica.** Las dos formas correctas
  deben diferir en el eje atado, y no las elige el maker.
- **G4 -- un guard declara QUE garantiza y lo demuestra**, reconciliado con lo que asumen sus
  llamadores; rebajar la garantia declarada no es cumplir.
- **G5 -- la direccion del fallo es del par CAMBIO-CONSUMIDOR.** Enumerar consumidores no cierra la
  clase: para miembros futuros hace falta un invariante estructural.
- **G6 -- el gate no es el fichero que editaste: enumera sus GEMELOS.** Mismo limite que G5, y su
  coste **escala con la adopcion**, que es la meta de la fase.
- **G7 -- estrechar la forma no es atar la propiedad.** El criterio debe sobrevivir a un cambio de
  coordenada, de orden y de formato.

## La generalizacion, corregida

La iteracion 2 la enunciaba asi: *"la poblacion de prueba se DERIVA de la condicion que el motor
evalua; no se enumera"*. **Esta sobreajustada**, y se ve en sus propios casos: vale para 0329, 0332
y 0342 -- tres de cuatro -- y **no vale para 0343**, cuyo defecto es que el gate observa una ventana
que no le pertenece. Ahi el eje fallido no esta en la condicion, esta en **que se le da a evaluar**;
una poblacion derivada de la condicion habria producido mas ventanas del mismo alcance equivocado.
El mismo limite aplica a los defectos temporales -- el check-then-act de 0331 -- donde ninguna
poblacion derivada de un booleano contiene "dos procesos en el mismo instante".

Formulacion que la salva:

    La poblacion se deriva de DOS sitios: de la CONDICION que el motor evalua, y del DOMINIO DE
    ENTRADA que el motor realmente lee -- que alcance, que ventana, que fichero, en que orden.
    Y acredita haber ejercitado la rama bajo prueba al menos una vez.

**Y un apunte sobre el encuadre, porque me ha mordido dos veces:** *"cuatro cadenas fallaron por lo
mismo"* **es una lista**. Las cuatro son las que agotaron iteraciones **ese dia**; no son la clase.
La formulacion honesta es la condicion de pertenencia -- *remediaciones que cierran lo medido y
dejan la clase abierta por un eje mas* -- y esa condicion incluye tambien las que **no** escalaron.

## Coste y contrapartida

**Un rojo que se queda rojo deja de leerse.** Con un solo `main` y varios agentes gateados por la
misma senal, un rojo persistente convierte el gate de **toda** tarea no relacionada en "rojo
conocido, sigo". Es el mecanismo por el que el arreglo se pospone para siempre, y esta instancia
lleva **dos meses** dentro de el. Por eso D1 y D2 exigen presupuesto de rojo: dueno, caducidad y
escalado al vencer.

**G1 es coste puro sobre codigo muerto.** Medido: media de un contrato ataba un camino de PowerShell
que ningun llamador de produccion recorre.

**El coste de G6 escala con el exito.** Los gemelos se GENERAN: cada instancia nueva copia el mirror.

**G5 obliga a elegir y a pagar:** invariante estructural (caro) o checklist (barata y no cierra la
clase). No vale dejarlo ambiguo.

## Lo que esto NO cubre

1. **El denominador.** Todas las ocurrencias son sobre mecanismos que EXISTEN. Ninguna sobre el que
   **deberia existir y nunca se declaro**.
2. **El texto del propio protocolo.** `AGENTS.md` y las DECISIONes contienen reglas que ningun gate
   ejecuta -- la memoria dorada, la narracion minima. Por esta misma tesis son declaradas-no-exigidas.
   Queda FUERA de alcance, y se declara.
3. **Mecanismos que pasan porque nunca disparan.** Guards con ventana, caducidades, techos de
   reintento: uno que jamas se activa es indistinguible de uno que funciona.
4. **El estado de reintento no reconciliado** (13 entradas huerfanas). No lo sostiene ninguna regla
   de las propuestas; queda como instancia sin regla.
5. **NUEVO -- el efecto medido cuya MEDICION no se puede obtener.** Ninguna de las tres reglas dice
   que hacer cuando el instrumento no esta disponible. Hoy no lo esta: CI no arranca un job. Es la
   condicion que hace a D3 inaplicable, y es una condicion de la instancia, no del documento.

*(El hueco 3 de la iteracion 2 -- "la capa de ledger: cero ocurrencias examinadas" -- se BORRA. Era
falso: TASK-0270 cazo el arquetipo en esa capa hace un mes, con veredicto adversarial, y TASK-0344
anade la de mailbox. Ambas pasan a la tabla.)*

## Lo que se retiro, y por que

**TASK-0334 no pertenece al patron.** El cambio ACTUO, y bien, en los dos consumidores; el defecto
era que querian cosas opuestas. Eso es acoplamiento y requisitos. Se conserva como leccion bajo G5.

## Pendiente antes de proponer formalmente

1. **TASK-0341 debe cerrar antes de que D1 se pueda proponer**, y su acceptance debe llevar el
   predicado por propiedad de la tabla U0-U6, no la forma. Hoy esta en `proposed`.
2. **D3 no sube sin terna, ejecutor y fallback.** Los tres son trabajo, no redaccion.
3. **D2 no sube sin el campo y su comprobacion en el validador.**
4. **Decision del operador**, que es donde el checker lo dejo: con CI incapaz de arrancar un job y
   0341 sin reclamar, la recomendacion del checker es **publicar solo D1 con el predicado por
   propiedad** y dejar D2 y D3 en el borrador hasta que tengan ejecutor. La comparto.
