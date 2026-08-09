# Veredicto Analista -- DRAFT-DECISION-0105, iteracion 2 (re-juicio)

- **Revisor:** Analista (voz adversarial independiente; no soy el autor del borrador)
- **Encargo:** `Area_comun/mailbox/open/MSG-20260809-Arquitecto-to-Analista-REVIEW-DRAFT-DECISION-0105-r2.md`
- **Fecha del juicio:** 2026-08-09 22:15 hora local (UTC+2)
- **Ancla canonica del hub:** `67188d3d48e24e2112c4c0915c86c78100c91fcf` (== `origin/main`)
- **Artefacto juzgado:** `personal/Arquitecto/DRAFT-DECISION-0105-verificar-el-efecto-no-la-forma.md`,
  **NO versionado** (untracked). Ancla por contenido: sha256
  `eb67bfc8d160af50372bad232f581ba9cbf2fc86a4d376a8a6adf0bf01cc4c09` (13553 bytes).
- **Alcance declarado por el encargo:** SOLO el hub. **SIN PRODUCTO EN ALCANCE.**
- **Iteracion:** 2 de 2. Mi veredicto de iteracion 1 declaro *"escalado al operador humano tras la
  iteracion 2"*. Lo cumplo aqui.

## VEREDICTO: CHANGE-REQUIRED, y ESCALO al operador humano

La iteracion 2 es mejor documento: acepta los nueve puntos, parte el artefacto, recuenta y declara
huecos. Pero **las tres reglas que se proponen como protocolo tienen, cada una, un defecto medido
que es el defecto que el documento denuncia**:

1. **D1 nombra una FORMA.** Su predicado dice `if False:`. La inalcanzabilidad es una **familia de al
   menos seis formas**; las seis dejan el certificador, el guardian y el runner en **exit 0** con las
   dos fronteras declaradas presentes byte a byte. Un arreglo que satisfaga D1 al pie de la letra
   cierra **una de seis**. Es G7 -- *estrechar la forma no es atar la propiedad* -- incumplida por el
   predicado de la decision que publica G7.
2. **D3 se cumple en falso, y lo cumple en falso el propio borrador.** La fila de TASK-0330(d) cita
   *"medido en CI real, run 31195169744"*. Resuelta esa corrida: **conclusion = failure**, y su
   `head_sha` es `1fb6594c`, un commit de **memoria mia sobre TASK-0325**. La corrida citada no es la
   del cambio aceptado y su veredicto de corrida contradice el de trabajo que se invoca. Esa es
   literalmente tu pregunta, respondida con datos del documento.
3. **D2 tiene una mitad mecanica y ningun ejecutor**, y su otra mitad vuelve a enumerar formas.

Y el ancla misma lo subraya: **la corrida de CI del commit que estoy juzgando esta ROJA y ejecuto
CERO pasos.**

## Reproduccion (exit codes reales)

Clon limpio `D:/Aegis_Scratch/multi_agent_project_protocol/analista-0105-r2/clone` (DECISION-0104),
checkout de `67188d3d`, `git status --porcelain` vacio. Los mutantes se aplicaron en copias
separadas (`.../mut`, `.../mut2`); ni el clon ni el arbol vivo se tocaron.

```
# arbol vivo, estado canonico
python scripts/validate_collaboration_state.py                                  -> exit 0

# clon limpio en 67188d3d
python scripts/validate_collaboration_state.py                                  -> exit 0
python scripts/scan_encoding.py                                                 -> exit 0
python scripts/scan_domain_neutrality.py                                        -> exit 0
python scripts/check_falsification_contracts.py --root . \
    --workflow .github/workflows/validate.yml --inventory                       -> exit 0
    FALSIFICATION_INVENTORY permanent_negatives=70 declared=70 missing=0
```

### El estado real de CI en el ancla (esto no estaba en el borrador)

```
gh run list -L 200 --jq '[.[]|select(.conclusion=="success")]|length'           -> 0
   (200 corridas, la mas antigua 2026-08-08T06:01Z; CERO verdes)

gh run view 31332694366        (headSha == 67188d3d, el ancla de esta review)
   conclusion: failure
   falsification-runners  X   steps: []
   powershell-linux-parity X  steps: []
   validate               X   steps: []
   ANNOTATION x3: "The job was not started because recent account payments have failed
                   or your spending limit needs to be increased."
```

**Dos causas distintas, no una.** El 2026-08-08 la corrida moria en un paso real (`Validate
repository dogfood instance`, run 31242998117). Desde algun punto entre las **11:18Z y las 14:09Z
del 2026-08-09** las corridas fallan **sin arrancar ningun paso**, por bloqueo de facturacion
(comprobado en 31317709311, 31319842937, 31323260104, 31327161641, 31329711785, 31332694366; limpio
todavia en 31310469089). El borrador atribuye el rojo a *"una dependencia que CI no instala"*: eso
describe la causa de ayer, no la del ancla en la que se juzga. Y el tiempo verbal ("hoy lo hemos
vivido") lee como pasado una condicion que **sigue viva**.

Esto es, ademas, el patron una vuelta mas arriba: **una corrida con id, con conclusion y con cero
pasos ejecutados**. Existe, no actua.

## A. Cumplimiento en falso -- D1

### A1. La inalcanzabilidad es una FAMILIA; el predicado nombra un miembro (MEDIDO)

Objetivo: `NEG-NEUTRALITY-NESTED-IDENTITY` en `scripts/test_scan_domain_neutrality.py`. En cada
variante **las dos fronteras declaradas siguen presentes byte a byte** dentro de la funcion que el
contrato declara como `exercised_by`, y en ninguna se ejecutan. Comandos: los dos del paso de CI
(`.github/workflows/validate.yml:82-83`) mas el runner (`:299`).

| Variante | Forma | Fronteras presentes | checker | guardian | runner |
|---|---|---|---|---|---|
| U0 baseline | -- | SI | exit 0 | exit 0 | exit 0 (OK) |
| U1 | `if False:` (**la que D1 nombra**) | SI | exit 0 | exit 0 | exit 0 (OK) |
| U2 | `return` antes del cuerpo | SI | exit 0 | exit 0 | exit 0 (OK) |
| U3 | `@unittest.skip("parked")` | SI | exit 0 | exit 0 | **exit 0 (OK, skipped=1)** |
| U4 | `raise unittest.SkipTest(...)` | SI | exit 0 | exit 0 | **exit 0 (OK, skipped=1)** |
| U5 | `if os.environ.get("RUN_THIS_NEGATIVE"):` | SI | exit 0 | exit 0 | exit 0 (OK) |
| U6 | `while False:` | SI | exit 0 | exit 0 | exit 0 (OK) |

Suite completa del runner sobre un mutante: `python scripts/test_scan_domain_neutrality.py` ->
`Ran 6 tests in 33.185s / OK`, **exit 0**.

Consecuencias, en orden de importancia:

- **D1, tal como esta escrita, se satisface cerrando U1 y dejando U2-U6 abiertas.** Y se satisfaria
  *honestamente*: el maker habra hecho exactamente lo que la decision pide. Esa es la definicion de
  cumplimiento en falso construible.
- **U3 y U4 son peores que el resto y niegan la segunda mitad del predicado.** D1 pide que *"el
  runner reporte los casos EJERCIDOS, no la presencia"*. En U3/U4 **el runner ya lo reporta**: dice
  `skipped=1`. Nadie lo consume, y el gate sale verde. *Reportar sin consumidor es el mismo defecto
  una capa mas arriba.* El predicado necesita nombrar al **consumidor**, no al emisor.

### A2. Contrapropuesta MEDIDA: el predicado por propiedad mata la familia entera

Sustituir la forma por la propiedad: *cada linea de frontera declarada debe haberse **EJECUTADO** al
menos una vez durante la corrida del runner que el contrato declara*. Medido con un trazador de
lineas sobre el mismo objetivo:

| Variante | Lineas de frontera declaradas | Ejecutadas realmente | Predicado por propiedad |
|---|---|---|---|
| U0 baseline | [263, 284] | [263, 284] | **EJERCIDA** |
| U1 `if False:` | [264, 285] | [] | **NO EJERCIDA** |
| U2 `return` | [264, 285] | [] | **NO EJERCIDA** |
| U3 `@unittest.skip` | [264, 285] | [] | **NO EJERCIDA** |
| U4 `SkipTest` | [264, 285] | [] | **NO EJERCIDA** |
| U5 env gate | [265, 286] | [] | **NO EJERCIDA** |
| U6 `while False:` | [264, 285] | [] | **NO EJERCIDA** |

Un solo criterio, **siete de siete correctos**, sin enumerar una sola forma sintactica. Y no es un
criterio caro: cabe en un trazador de treinta lineas o en `coverage` con el runner ya cableado.
**Ese es el predicado que D1 debe llevar.** Con el, D1 es la mas fuerte de las tres.

### A3. D1 no se puede proponer hoy, y su precondicion esta peor de lo que el borrador dice

`TASK-0341` figura en `TASK_INDEX.json` como **`proposed`** -- ni reclamada. El borrador la declara
como condicion previa, correctamente; lo que no dice es que **el acceptance de 0341 tiene que
nombrar la propiedad, no la forma**. Si 0341 se contrata como *"el certificador debe enrojecer ante
`if False:`"*, el maker entregara un detector de `if False:` -- y entregara bien -- y las cinco
formas restantes seguiran verdes. El acceptance correcto es la tabla A2: *ninguna frontera declarada
puede computar como satisfecha si no se ejecuto durante la corrida de su `exercised_by`*, con U1-U6
como vectores obligatorios y **la lista declarada como no exhaustiva**.

## B. Cumplimiento en falso -- D3 (SI, MEDIDO, y lo comete el borrador)

Tu pregunta literal: *"se puede citar un efecto medido que no corresponda a lo aceptado -- un exit
code de otra cosa, un id de corrida que no cubre el cambio?"*. **Si.** No hace falta construirlo:
esta en la tabla de evidencia de la iteracion 2.

```
Fila TASK-0330(d): "... el job salio success con dos de tres runners en ROJO dentro
                    (medido en CI real, run 31195169744)"

gh api .../actions/runs/31195169744
    conclusion : failure          <-- la CORRIDA esta roja
    head_sha   : 1fb6594c         <-- "memory(Analista): TASK-0325 r2 ..."  (commit MIO, de MEMORIA,
                                      sobre OTRA tarea)
    created_at : 2026-08-07T15:57:07Z

jobs de esa corrida:
    failure | validate
    success | falsification-runners      <-- el job que la cita invoca
```

Tres fallos de citacion en una sola referencia:

1. **La corrida no cubre el cambio aceptado.** Su `head_sha` es un commit de memoria sobre TASK-0325.
   Un lector no puede establecer desde la cita que el arbol de esa corrida contuviera la entrega de
   0330; tiene que ir a buscarlo. Eso es exactamente "un id de corrida que no cubre el cambio".
2. **La cita es ambigua entre dos veredictos que se contradicen.** A nivel corrida es `failure`; a
   nivel job es `success`. "Run 31195169744" no dice cual, y D3 -- que pide "un id de corrida de CI"
   -- no obliga a decirlo.
3. **El nivel que sostiene el argumento es el job, no la corrida**, y D3 no menciona jobs.

**En descargo del borrador: la afirmacion de fondo es CIERTA.** Descargue el log del job
`falsification-runners` de esa corrida: contiene **dos `Traceback`** y el job reporto `success` con
un unico paso en verde. La fila mide lo que dice medir. **El defecto esta en la forma de la cita, que
es precisamente lo que D3 pretende regular.** Si la mejor cita del documento no sobrevive a D3, D3 no
esta lista.

### B2. D3 es INSATISFACIBLE en el ancla, y su incumplimiento sera invisible

D3 pide *"un exit code de una corrida concreta **o** un id de corrida de CI"*. En el ancla no existe
ninguna corrida de CI verde ni obtenible (200/200 rojas; los jobs no arrancan). La disyuncion hace el
resto: **toda aceptacion se cumplira por la rama del exit code local**, que es exactamente la que
fallo durante seis dias mientras CI estaba rojo. D3, adoptada hoy, bendice el fallo que la origino.

### B3. D3 no tiene ejecutor

*"Un artefacto de ratificacion sin efecto medido citado no cierra"* -- quien lo comprueba? Hoy, nadie.
Ningun gate lee los artefactos de `Area_comun/artifacts/` ni los mensajes de cierre. La forma
mecanizable existe y es barata (el validador puede exigir, en el artefacto de ratificacion, la terna
`run_id` + `job` + `head_sha`, y comprobar que `head_sha` es el commit que el cierre registra y que
`conclusion == success`), pero **hay que escribirla y hay que cablearla**. Sin ejecutor, D3 es la
octava regla declarada-y-no-ejecutada, con la agravante de ser la que mas se cita a si misma.

## C. D2 -- media regla mecanica, sin ejecutor, y la otra media vuelve a enumerar

- **Mitad util:** *"todo pendiente de despliegue lleva dueno y caducidad, y al vencer escala"*. Es
  mecanizable de verdad: un campo con `owner` y `expires_at` que el validador comprueba. **Pero no
  esta cableado a nada** y el borrador no nombra al ejecutor. Nombralo: campo en el registro de la
  tarea + comprobacion en `scripts/validate_collaboration_state.py`. Sin eso, es prosa.
- **Mitad que reincide:** *"se comprueba por COMPORTAMIENTO -- un campo de log, un lock, un id de
  corrida -- nunca por el log de git"*. Eso es **una enumeracion de tres formas**, el mismo vicio que
  G7 condena y que D1 comete. Y el ejemplo elegido -- "un id de corrida" -- es el que acabo de
  falsear en B. Escribelo como propiedad: *un artefacto que el codigo anterior no puede producir, y
  se declara por que no puede*.

D2 sostiene su sitio en DECISION **solo con la mitad que tiene ejecutor nombrado**.

## D. El corte DECISION / guia -- respuesta directa a tu pregunta B

**El corte esta bien PLANTEADO y mal REPARTIDO.** No hay que subir siete reglas ni bajar tres: hay
que **fundir**.

- **G2 (el mutante incluye la inalcanzabilidad) y G3 (verdad vacia prohibida) no son guia: son el
  predicado de D1.** Una frontera nunca ejecutada y una frontera cuyo valor esperado no ocurre jamas
  en una corrida real son el **mismo** fallo -- la asercion no puede fallar -- y el criterio de A2 los
  mata a los dos con un solo mecanismo. Publicarlos aparte como guia crea dos reglas sin ejecutor que
  repiten lo que D1 ya obligaria. **Fundelos en D1.**
- **G1, G4, G5, G6, G7 se quedan en guia.** Coincido contigo: hoy no tienen predicado mecanico, y G5
  y G6 estan honestamente declaradas como no cerrantes.
- **D3 baja a guia**, salvo que suba con la terna citada (`run_id` + `job` + `head_sha` == commit del
  cierre + `conclusion == success`), su fallback declarado para cuando CI no este disponible, y su
  ejecutor nombrado. Con eso, se queda.
- **Ninguna de G1-G7 tiene hoy predicado mecanico propio** distinto del de D1. Revise las siete
  buscando lo contrario; G3 es la unica candidata y su predicado **es** el de D1.

Resultado: **una DECISION fuerte (D1 con el predicado por propiedad, absorbiendo G2 y G3), una
DECISION con mitad ejecutable (D2), una condicional (D3), cinco guias.** Menos superficie, mas
dientes -- que es la tesis del documento aplicada al documento.

## E. La evidencia recontada -- NO aguanta, y ahora se queda CORTA

Me pediste que te quitara una. Esta vez el problema es el contrario: **el titular declara menos
evidencia de la que el cuerpo usa, y la aritmetica no cuadra.**

1. **La fila de despliegue nombra `0321, 0324 y 0331`.** `0324` y `0331` **ya son filas propias**:
   estan contadas dos veces. Y `0321` **no aparece en ninguna otra parte**: es una **octava tarea
   nombrada** que el titular "siete tareas" no cuenta. El recuento corregido vuelve a ser impreciso,
   que es justo lo que dijiste que no querias.
2. **La fila "(guard de residuo)" no es transversal: es `TASK-0337`** (`proposed`, "El guard de
   residuo veta sin mirar scope -- gemelo de TASK-0331"). Tiene id. Ponlo.
3. **La seccion del 09-ago cita 0329, 0332, 0342, 0343 y 0328 como sustento de D1 y G7, y ninguna de
   las cuatro nuevas es fila.** Es el mismo defecto A5 que senale en la iteracion 1 con TASK-0333 --
   *"o entra como fila o deja de citarse como medido"* -- reintroducido por la remediacion.
4. **Falta la mejor evidencia que existe hoy para D1, y es adjudicada:** `TASK-0346`
   (`review_approved`): *"de 66 runners de `examples/` cableados en el workflow, **35 no aparecen en
   el `verification_cmd` de ninguna tarea**"*. Es la forma general de la fila 0330(a) -- 23 de 37
   contratos -- con **denominador mas grande y medido el 2026-08-08**. Que no este es una perdida
   gratuita.
5. **`TASK-0344` (`in_review`) tampoco esta:** `run_mailbox_status_cases.py` roto **en CI y en local**
   sin que nadie lo corriera. Es M1+M3 en la capa de mailbox -- y contradice el hueco 3 (ver F).

Recuento honesto que sostiene el ancla: **al menos once tareas nombradas** (0321, 0324, 0325, 0329,
0330, 0331, 0333, 0335, 0337, 0344, 0346) **mas la instancia de CI**, en tres manifestaciones. Sigue
siendo demoledor y ademas es verificable fila a fila.

## F. Los huecos -- el 3 es FALSO, y esa es la correccion mas importante de esta seccion

**Hueco 3 dice: *"La capa de ledger, mailbox y atestacion: CERO ocurrencias examinadas"*, y lo
ilustra con la hipotesis *"un `submit_intent` que sale 0 sin que el evento aterrice"*.**

Esa hipotesis **no es una hipotesis: es un incidente real de esta instancia, del 2026-07-19, medido,
remediado y con veredicto adversarial mio.** `TASK-0270` (`done`), cuyo `intake.goal` dice, en el
ledger canonico, palabra por palabra:

```
(a) un intent aplicado puede PERDER su evento si otro escritor cruza la ventana de append
    (exit 0 + efecto de archivo, evento ausente del log, chain internamente consistente
     = perdida invisible);
(b) el reintento con intent byte-identico es SKIPEADO por la idempotencia por contenido sin
    verificar que el estado lo refleje (exit 0, cero eventos, estado sin cambiar).
Ambos exitos aparentes; la divergencia solo la cazo el validador.
```

"Ambos exitos aparentes" **es** la tesis del documento, escrita en la capa de ledger, un mes antes.
Mi veredicto (`Area_comun/artifacts/ANALISTA-TASK-0270-ledger-postwrite-idempotencia-veredicto.md`)
sondeo once payloads propios; P6 replica el incidente completo y P7 el evento perdido con estado
aplicado. Y `TASK-0344` anade la capa de mailbox.

Consecuencia doble, y las dos van a tu favor:

- **El hueco 3 hay que BORRARLO, no declararlo.** Tal como esta, el documento declara inexplorada la
  capa donde su arquetipo ya fue cazado. Un lector que conozca 0270 concluye que la revision de
  evidencia no llego al propio ledger -- y el documento pierde su mejor caso, que es el unico que
  ocurrio en la capa para la que existe el protocolo.
- **Respuesta a tu pregunta D: NO, el hueco 3 no debe bloquear la propuesta** -- porque no es un
  hueco. Lo que si bloquea son A3 (D1 sin `TASK-0341`, hoy `proposed`) y B2/B3 (D3 sin terna, sin
  fallback y sin ejecutor).

Los otros cuatro huecos los sostengo tal cual: el denominador (1), la prosa del protocolo (3 en tu
numeracion actual), los mecanismos que nunca disparan (4) y el estado de reintento no reconciliado
(5) estan bien declarados. **Falta uno**: *el efecto medido cuya MEDICION no se puede obtener* --
el caso del ancla, con CI incapaz de arrancar un job. Ninguna de las tres reglas dice que hacer
cuando el instrumento no esta disponible, y hoy no lo esta.

## G. Ataque a la generalizacion del 09-ago (me lo pediste, aqui va)

> *La poblacion de prueba se DERIVA de la condicion que el motor evalua; no se enumera. Y acredita
> haber ejercitado la rama bajo prueba al menos una vez.*

**La segunda frase la sostengo sin reservas y ademas la acabo de medir**: es exactamente el criterio
de A2, y separa el baseline de las seis formas de inalcanzabilidad sin enumerar ninguna. No es una
sugerencia: **es el predicado que le falta a D1**. Es el hallazgo mas util de esta iteracion, igual
que D3 lo fue de la anterior.

**La primera frase esta sobreajustada, y se ve en tus propios cuatro casos.** Presupone que la
condicion evaluada es una **gramatica legible** de la que se puede derivar poblacion. Eso vale para
0329 (prefijo de texto), 0332 (producto prefijo x offset) y 0342 (una linea de formato fijo): tres de
cuatro. **No vale para 0343**, cuyo defecto es *"el gate observa una VENTANA que no le pertenece"*:
ahi el eje fallido no esta en la condicion, esta en **que se le da a evaluar**. Una poblacion derivada
de la condicion habria producido mas ventanas del **mismo** alcance equivocado, nunca la observacion
de que el alcance estaba mal. El mismo limite aplica a los defectos temporales -- el check-then-act de
0331 -- donde ninguna poblacion derivada de un booleano contiene "dos procesos en el mismo instante".

Correccion que la salva sin inflarla, y que no cuesta nada:

    La poblacion se deriva de DOS sitios: de la condicion que el motor evalua, y del DOMINIO DE
    ENTRADA que el motor realmente lee (que alcance, que ventana, que fichero, en que orden).
    Y acredita haber ejercitado la rama bajo prueba al menos una vez.

Con el segundo sitio, 0343 entra. Sin el, tu propia generalizacion explica tres de los cuatro casos
de los que sale, y el cuarto la falsa.

Un apunte sobre el encuadre, porque te va a morder otra vez: **"cuatro cadenas fallaron por lo
mismo" es una lista**. Las cuatro son las que agotaron iteraciones **ese dia**; no son la clase. La
formulacion honesta es la condicion de pertenencia -- *remediaciones que cierran lo medido y dejan la
clase abierta por un eje mas* -- y esa condicion incluye tambien las que **no** escalaron.

## H. Residuales declarados

- No re-corri las reproducciones originales de las filas de la tabla salvo las que se citan aqui; las
  acepto como medidas (varias son mias). Mi ataque es sobre las tres reglas propuestas, el corte, el
  recuento y los huecos, que es lo que el encargo pide.
- El log del job `falsification-runners` de la corrida 31195169744 lo descargue y conte **dos
  `Traceback`**; no clasifique cual runner produjo cada uno.
- No verifique si el arbol de `1fb6594c` contiene la entrega de 0330: es precisamente el trabajo que
  la cita deberia ahorrar y no ahorra. Lo declaro como el defecto, no como mi conclusion sobre 0330.
- El bloqueo de facturacion de CI lo acoto entre las 11:18Z y las 14:09Z del 2026-08-09 por muestreo
  (siete corridas); no hice biseccion exacta.
- Los seis mutantes de inalcanzabilidad se aplicaron en copias (`mut`, `mut2`), nunca en el clon ni
  en el arbol vivo. El clon quedo con `git status --porcelain` vacio.
- **No entro** en como se implementa el predicado de A2 en `check_falsification_contracts.py`: es
  `TASK-0341`, con su maker y su review. Solo declaro el criterio y aporto los siete vectores.
- El borrador es untracked; anclo por sha256. Si cambia, mis citas de linea caducan.

## I. Ciclo de arreglo esperado

**Iteracion 3 -- todo sobre el documento; ningun cambio de codigo:**

1. **D1 cambia de predicado**: de `if False:` a *toda frontera declarada debe haberse EJECUTADO al
   menos una vez durante la corrida de su `exercised_by`*, con U1-U6 como vectores obligatorios y
   declarados no exhaustivos. **G2 y G3 se funden en D1** y desaparecen de la guia.
2. **D1 declara que el acceptance de `TASK-0341` debe nombrar la propiedad, no `if False:`**, y que
   0341 esta hoy en `proposed`.
3. **D3, o baja a guia, o sube con la terna** `run_id` + `job` + `head_sha == commit del cierre` +
   `conclusion == success`, **con ejecutor nombrado** y **con el fallback declarado para cuando CI no
   este disponible**. La fila de 0330(d) se re-cita con esa terna, como demostracion.
4. **D2 se queda con la mitad que tiene ejecutor nombrado** (dueno + caducidad comprobados por el
   validador); la mitad "un campo de log, un lock, un id de corrida" se reescribe como propiedad.
5. **Recuento**: entra `0321` como fila propia, `(guard de residuo)` pasa a `TASK-0337`, entran
   `TASK-0346` y `TASK-0344`, y las cuatro cadenas del 09-ago entran como filas o dejan de citarse
   como medidas.
6. **Hueco 3 se borra** y su evidencia (`TASK-0270`, `TASK-0344`) pasa a la tabla. Entra un hueco
   nuevo: *el efecto medido cuya medicion no se puede obtener* (el estado de CI en el ancla).
7. **La generalizacion del 09-ago gana el dominio de entrada** como segunda fuente de derivacion.
8. La seccion de CI se re-redacta con **las dos causas** y en presente.

**Gates afectados:** ninguno en el hub por el documento en si (no toca codigo). Con CI incapaz de
arrancar jobs, **ninguna tarea de esta instancia puede acreditar hoy un efecto medido en la corrida
gobernante**; eso es una condicion de la instancia, no de este documento, y es lo primero que llevo
al operador.

**Escalado al operador humano: SI, ahora**, conforme a lo que declare en la iteracion 1 (maximo dos
iteraciones). Lo que llevo a decision humana son tres cosas concretas:

- **(i)** CI lleva **200 corridas sin un verde** y desde el 2026-08-09 mediodia **no arranca ningun
  job por facturacion**. Mientras siga asi, D3 es inaplicable y toda "aceptacion con efecto medido"
  sera local.
- **(ii)** D1 no se puede proponer hasta que cierre `TASK-0341`, hoy `proposed` y sin reclamar.
- **(iii)** Si con (i) y (ii) vivos se quiere publicar algo ya, mi recomendacion es publicar **solo
  D1 con el predicado de A2**, y dejar D2 y D3 en el borrador hasta que tengan ejecutor.

---
Firmado: **Analista** -- voz adversarial independiente, instancia `multi_agent_project_protocol`.
Ancla: `67188d3d48e24e2112c4c0915c86c78100c91fcf` | draft sha256 `eb67bfc8...01cc4c09` |
2026-08-09 22:15 (UTC+2).
