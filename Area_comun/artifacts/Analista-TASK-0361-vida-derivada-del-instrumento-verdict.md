# Veredicto Analista -- TASK-0361 (el gate del harness estaba rojo por una constante menor que su instrumento)

- Revisor: Analista (voz adversarial independiente)
- Fecha: 2026-08-11, 22:41 hora local (UTC+2)
- Ancla protocolo: `2144d4330afee3ec8e07ad6bc596f5351036bf33` (= `origin/main` al abrir la review)
- Implementacion juzgada: `0205c0568a21e72b3d8049423ed9e98eb6440366`
- Equivalencia ancla/implementacion: `git diff --stat 0205c056 HEAD -- scripts/test_exec_lease_harness.py
  scripts/harness/peer_mailbox_cron.ps1` sale VACIO. Lo que mido en el ancla ES lo que entrego el maker.
- Alcance declarado por el Arquitecto: SOLO hub, sin producto (no se gatea `npm test`)
- Vuelta: 1
- Recomendacion de cierre: **OK-CLOSABLE**, con tres residuales declarados

---

## 0. Resumen en una linea

La vida del workload **se deriva de verdad** del coste medido del instrumento, y lo acredito por
conducta y no por el nombre del test: encarecido el instrumento x2 y x6, la vida crecio de 12,2 s a
18,8 s y a 36,4 s y el caso siguio midiendo lo que dice medir, mientras la version anterior **se
rompe** bajo esa misma perturbacion; ademas el campo nuevo de AC3 convierte en fallo diagnosticado el
delta cero mudo que costo dos corridas enteras en 0359 r2.

---

## 1. Reproduccion (por exit code, en clon limpio)

Hicieron falta dos clones, porque el primero me mintio.

    clon A (lab adversarial):  git clone --depth 1 file://D:/Agentes/multi_agent_project_protocol
    clon B (evidencia limpia): git clone -s ... + git checkout 2144d433
                               git status --short VACIO (untracked_before=0)

En el clon A el validador salio EXIT=1, y **el rojo era mio, no de la entrega**:

    - commit_trailers could not scan git history from 57f6250f...:
      git rev-list --reverse 57f6250f..HEAD returned non-zero exit status 128

`--depth 1` no trae la historia que el gate de trailers necesita. Lo dejo escrito porque es
exactamente la clase de falso rojo que un revisor puede firmar sin mirar: fallo el instrumento, no lo
medido. Repeti todo en el clon B, con historia completa y arbol pristino.

Gates en el clon B (`D:/Aegis_Scratch/multi_agent_project_protocol/analista-0361/clone2`, DECISION-0104):

    python scripts/validate_collaboration_state.py --root .   EXIT=0   OK: collaboration state is valid.
    python scripts/scan_encoding.py --root .                  EXIT=0
    python scripts/scan_domain_neutrality.py --root .         EXIT=0
    python runtime/protocol_replay.py --check-drift --root .  EXIT=0   verdict=CLEAN up_to_seq=8846
    python scripts/test_exec_lease_harness.py                 EXIT=0   x3 (ver AC5)

**AC5, tres corridas consecutivas, con los casos ejecutados en cada una:**

    corrida 1  EXIT=0  157 s  SUMMARY total=30 passed=30 failed=0
    corrida 2  EXIT=0  149 s  SUMMARY total=30 passed=30 failed=0
    corrida 3  EXIT=0  153 s  SUMMARY total=30 passed=30 failed=0

(Tres corridas mas, en el clon A, salieron igual: 147/146/150 s, 30 de 30.)

---

## 2. AC por AC, probado por conducta

| AC | Veredicto | Como lo probe |
|----|-----------|---------------|
| AC1 falsacion previa | PASS con matiz -- ver 4a | Hoy **no** consigo reproducir el rojo: el test PRE-FIX (workload fijo de 8 s) contra el mismo harness, en el mismo clon limpio, sale **GREEN 2 de 2**. No refuta el diagnostico: lo confirma, y obliga a discriminar de otra manera (4b). |
| AC2 la vida se DERIVA | PASS | Encareci el instrumento **simetricamente** y mire si la vida seguia: 1363 ms -> 12225 ms; 3578 ms -> 18810 ms; 7968 ms -> 36370 ms. La vida sigue al coste; no es otra cifra disfrazada. |
| AC3 se acredita lo que se mide | PASS | Fabrique el escenario que el campo debe delatar en vez de creerme su nombre: con la medicion ciega al coste real el hijo muere antes de la segunda muestra, la sonda devuelve `after == before` EXACTO -- la firma original -- y ahora lo acompana `child_alive_at_second_sample: false`, que es la PRIMERA asercion del test y falla con el dict entero en el mensaje. |
| AC4 el rojo no tapa al resto | PASS parcial, declarado (R3) | `main()` captura por test y sigue: `SUMMARY total=30 passed=30 failed=0` y traceback por fallo a stderr. La granularidad es el test, no la asercion. |
| AC5 verde estable | PASS | Tres corridas consecutivas, gateadas por exit code, con el numero de casos de cada una (punto 1). |
| AC6 sin regresion | PASS | La lista de tests tiene 30 entradas antes y despues del commit; ninguna desactivada ni relajada; el diff solo anade aserciones y cambia el runner. La cobertura **sube**: antes el runner abortaba en el test 11 y los 19 posteriores no llegaban a ejecutarse. |

---

## 3. Las dos preguntas que hiciste: el 4500 y el suelo de 5000

Son cosas distintas y merecen respuesta distinta.

**El suelo de 5000 es margen, y es sano.** La formula es `max(5000, 2 * coste medido)`: cuando el
instrumento es barato manda el 5000, que sobra; cuando es caro manda el `2 * coste`, que escala. El
suelo solo ata cuando ya no hace falta. Medido: con coste ~1,2 s el margen fue 5000; encareciendo el
instrumento paso solo a 7155 y a 15935, sin que yo tocara nada.

**El 4500 es geometria de la sonda -- pero es un duplicado a mano, y lo puedo desincronizar.** El
4500 pretende ser `1500 + 3000`, los dos `Start-Sleep` que la sonda ejecuta entre el arranque del
hijo y la segunda muestra. Como son esperas de reloj, no dependen de la velocidad de la maquina: por
eso **no** son la clase de defecto que cierras. Pero no estan derivados de esos sleeps, estan
copiados. Lo demuestro cambiando **solo** el segundo sleep de la sonda de 3000 a 9000 ms:

    [second-sleep 3000 -> 9000]  workload_lifetime_ms = 11844   (NO se mueve)
                                 child_alive_at_second_sample = false
                                 after == before == 26718750    (delta cero, la firma original)

La proxima edicion de cualquiera de los dos sleeps reintroduce el defecto que esta tarea cierra. Con
un atenuante que es merito de esta misma entrega: ya no reaparece mudo, canta por AC3. Un
`$fixedProbeDelayMs = $firstSleepMs + $secondSleepMs`, con los dos sleeps emitidos desde esas mismas
variables, lo cerraria del todo y es una linea. Va como residual R1, no como bloqueo, porque la
propiedad que AC2 exige -- que el veredicto no cambie cuando el instrumento cueste el doble -- se
cumple y la medi.

---

## 4. Lo que intente romper

### 4a. El verde de hoy, solo, no discrimina

Antes de creerme las seis corridas verdes hice la prueba que faltaba: correr el test **PRE-FIX** (el
de los 8 s fijos) contra el mismo harness, en el mismo clon limpio, ahora.

    attempt 1: GREEN
    attempt 2: GREEN

La maquina esta hoy mas tranquila que cuando medi 0359 r2: el instrumento cuesta ~1,2 s por muestra
en vez de ~2,2 s, y `4500 + 2*1200 = 6,9 s` todavia cabe en 8000. O sea que tres verdes del codigo
nuevo, hoy, son por si solos compatibles con no haber arreglado nada. Esto no debilita la entrega:
**es la propiedad que AC2 denuncia**, el verde del codigo viejo depende de la carga de la maquina. Lo
que discrimina es 4b.

### 4b. La prueba decisiva: el mismo instrumento encarecido, los dos codigos

Retardo dentro de `Get-ExecTreeCpuSample`, pagado por todos los llamantes (coste real ~3,75 s), y las
dos versiones de la sonda contra ese mismo harness:

    [PRE-FIX/busy]            BROKEN  after=null, before=48125000, progressing=false
    [PRE-FIX/retiring_child]  BROKEN  after=null, before=15156250, progressing=false
    [POST-FIX/busy]           OK      lifetime=19506 ms, child_alive=true, progressing=true
    [POST-FIX/retiring_child] OK      lifetime=19526 ms, child_alive=true, progressing=true

El `after: null` del PRE-FIX es el hijo ya muerto: `Test-LeaseProcessMatches` falla, la muestra sale
`$null` y el caso reporta "no progresa" siendo mentira. **La entrega hace el trabajo; el verde no es
suerte.** Esta es la respuesta a tu pregunta: si, el verde sobrevive a un cambio de maquina.

### 4c. Escalado simetrico, hasta x6

    coste medido   vida derivada   hijo vivo en la 2a muestra   el caso mide progreso
    1363 ms        12225 ms        si                            si
    3578 ms        18810 ms        si                            si
    7968 ms        36370 ms        si                            si

### 4d. La cota del margen, medida y declarada

El margen no es infinito y conviene saber donde cede. Medicion **ciega** al coste real (retardo solo
cuando el lease no es el proceso que mide, para que la estimacion se quede corta a proposito):

    coste extra NO medido   resultado
    +3000 ms por muestra    child_alive=false, after == before EXACTO, el test falla con diagnostico
    +5000 ms por muestra    idem

Con margen 5000 ms la sonda tolera que el coste real supere al estimado en ~2,5 s **por muestra**
(unas 3x el coste de hoy) antes de ceder, y cede **diciendolo**. Esa es la cota real.

### 4e. Que la medicion se tome contra `$PID` y no contra el hijo, es fiel

Era mi objecion mas seria contra AC2: si el coste del instrumento escalara con el tamano del arbol,
medir contra un proceso solo subestimaria sistematicamente lo que luego se paga contra el hijo. Lo
medi, alternando las dos llamadas con un arbol hijo real de 4 nodos vivo:

    self_ms  = [778, 660, 867]     (arbol de 1 nodo)
    child_ms = [692, 929, 956]     (arbol de 4 nodos)

Indistinguibles. Cuadra con el codigo: el termino dominante es `Get-CimInstance Win32_Process`, que
recorre la tabla de procesos entera y no depende del lease; el recorrido por nodo son unos pocos
`Get-Process`. La objecion queda cerrada: **medir contra `$PID` es un proxy fiel**. Lo que si puede
pasar de verdad es que la carga cambie entre la medicion y la segunda muestra; para eso esta 4d.

### 4f. Si el parametro no llegara

Si el binding posicional de `$LifetimeMilliseconds` fallara, el workload viviria 0 ms y volveriamos
al delta cero. Ya no se puede colar: es lo primero que detecta la asercion de AC3.

---

## 5. Residuales declarados

- **R1 -- el 4500 es un duplicado, no una derivacion.** Demostrado en el punto 3: cambiar un
  `Start-Sleep` de la sonda no mueve la vida derivada y reintroduce el delta cero. Falla
  ruidosamente gracias a AC3. Cierre sugerido: emitir los dos sleeps y `fixedProbeDelayMs` desde las
  mismas dos variables. No bloquea.
- **R2 -- la vida del worker de `retiring_child` sigue siendo un 3500 fijo, y nadie acredita que se
  retirara antes de la segunda muestra.** El caso solo afirma que el **padre** llego vivo; no hay
  ninguna asercion de que el nieto estuviera muerto, que es la otra mitad de la propiedad que el caso
  dice probar. Hoy el nieto muere a ~3,9 s y la segunda muestra cae a ~6,9 s: se cumple por holgura,
  no por construccion. En una maquina donde el instrumento fuera muy barato y el arranque de
  PowerShell caro, el nieto seguiria vivo, el caso pasaria igual y ya no estaria midiendo un hijo
  retirado: **verde silencioso, no rojo**. Es la misma clase de defecto que esta tarea cierra, un
  nivel mas abajo. No bloquea el gate.
- **R3 -- AC4 es a nivel de test, no de asercion.** Dentro del negativo permanente las tres sondas
  sanas se ejecutan antes de las aserciones, pero la sonda del MUTANTE va despues: un fallo en una
  asercion sana sigue impidiendo que el mutante llegue a correr. El AC admite declarar el limite por
  escrito; queda declarado.

---

## 6. Recomendacion

**OK-CLOSABLE.** El gate compartido esta verde y, lo que importa mas, esta verde **por una razon que
sobrevive a la maquina**: la vida sigue al coste medido hasta x6, la version anterior se rompe bajo
esa misma perturbacion, y el delta cero mudo -- el fallo que me costo dos corridas enteras en 0359 r2
-- ya no puede presentarse como "no progresa". Los tres residuales van declarados y ninguno cambia el
veredicto del gate. De los tres, el unico que recomiendo convertir en unidad propia es R2.

-- Analista
