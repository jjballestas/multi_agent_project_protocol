---
decision_id: DECISION-0105
title: "Un mecanismo de verificacion debe atar el EFECTO y debe EJECUTARSE: declarado no es verificado, y mergeado no es desplegado"
status: draft
proposed_by: Arquitecto
requires: aprobacion del operador humano
created_at: 2026-08-07
supersedes: none
relates_to:
  - DECISION-0020
  - TASK-0324
  - TASK-0325
  - TASK-0330
  - TASK-0331
  - TASK-0335
---

# DECISION-0105 (borrador) -- verificar el efecto, y verificar que se verifica

## Por que existe este borrador

Entre el 2026-08-07 y el 2026-08-08 el mismo defecto de fondo aparecio **catorce veces**, en cinco capas
distintas del sistema, encontrado por tres agentes distintos y en tareas sin relacion entre si.
Cuando un patron se repite asi, seguir contratandolo caso por caso es tratar el sintoma.

Ninguna de las catorce es una hipotesis: todas tienen reproduccion medida.

## El patron, en una frase

**Confundimos que algo EXISTA con que algo ACTUE.**

Y se manifiesta en dos formas complementarias:

1. **El verificador ata la FORMA, no el efecto.** Comprueba como esta escrito hoy el codigo, no lo
   que el codigo hace. Sobrevive a la siguiente refactorizacion legitima sin protegerla.
2. **El verificador existe pero no CORRE.** Esta declarado, contado e incluso citado como evidencia
   de rigor, y ningun gate lo ejecuta.

## Las ocurrencias medidas

| # | Donde | Que ataba, y que deberia atar |
|---|-------|-------------------------------|
| 1 | TASK-0324 | ataba el HELPER puro + `assert linea in source`; un mutante de CODIGO MUERTO -- cableado presente pero inalcanzable -- sobrevivia y reproducia el defecto original |
| 2 | TASK-0325 | el detector buscaba `ast.Continue`; un bypass con `break` colaba **un email por el gate de PII** con la suite de 64 tests en verde |
| 3 | TASK-0330 r3 | el checker exigia el literal `$expires -gt $now`; la forma equivalente fail-closed de 0331 lo rompio |
| 4 | TASK-0330 r4 | el fixture asumia un mundo sin `work_scope` obligatorio |
| 5 | TASK-0335 | la asercion exige una POSICION de subcadena en el log; 0321 metio campos en medio |
| 6 | TASK-0330 | **23 de 37 contratos declarados** con runner que CI no ejecutaba nunca; uno llevaba **dos semanas rojo** |
| 7 | TASK-0331 | el guard aparentaba exclusion mutua **sin darla**: check-then-act sin atomicidad; dos peers arrancaron el MISMO segundo |
| 8 | despliegue | 0321, 0324 y 0331 en `done`/`in_review` y **NO corriendo**: los crons cargan el `.ps1` al arrancar |
| 9 | estado de reintento | 13 entradas huerfanas apuntando a mensajes archivados o inexistentes, generando falsas alarmas |
| 10 | TASK-0330 **el cableado mismo** | los tres runners entraron en un paso `run:` de un job `windows-latest` **sin `shell:` declarado**: en `pwsh` el codigo no-cero de un ejecutable INTERMEDIO no aborta el bloque, y GitHub anade `exit $LASTEXITCODE`, asi que el paso hereda el del ULTIMO comando. **El job sale `success` con DOS de los tres runners en ROJO dentro** (medido en el CI real, run 31195169744). Y al job le faltaba `jsonschema`, asi que uno de los "verdes" no ejecutaba ni un caso |

| 11 | TASK-0334 | descubrir repos embebidos **protege** al veto por claim (sobre-detectar evita matar trabajo vivo) y **bloquea** a los lectores que comparan, que deben honrar el `.gitignore` del padre. **El mismo cambio, direcciones de seguridad opuestas segun el consumidor** |

| 12 | TASK-0329 (su REMEDIACION) | la exencion de neutralidad paso de eximir un FICHERO ENTERO a fijar pares **(numero_de_linea, termino)**. El 08-ago otra tarea anadio ~56 lineas por encima en el mismo fichero y las ocho ocurrencias exentas se desplazaron: `scan_domain_neutrality` exit 1 sobre **ocho lineas legitimas e INTACTAS**. La exencion no describe QUE exime ("esta ocurrencia nombra la CLI de un tercero"); describe **DONDE estaba el dia que se escribio** |
| 13 | guard de residuo (-> TASK-0337) | veta el mensaje de una tarea por suciedad del arbol perteneciente a OTRA. Decision **por-par** (este mensaje contra estas rutas) tomada sobre una propiedad **global** (el arbol esta sucio). Es el gemelo exacto de la ocurrencia 7 en el guard de al lado del mismo fichero: cerrar la admision de claims no cerro la familia |
| 14 | TASK-0329 (su CONTRATO DE PARIDAD) | el negativo anadido **para impedir la cuarta divergencia** entre los dos escaneres ata (a) un regex de indentacion fija sobre una ventana de texto y (b) un fixture de siete ficheros. Un **desliz de dos espacios** en la clave de ruta -- o declarar la ampliacion fuera de la ventana parseada -- produce veredictos divergentes (Python exit 1, gemelo exit 0) **con la suite entera en verde**. El discriminante no es la gravedad del cambio: es su indentacion |

**Las ocurrencias 10, 12 y 14 son RECURSIVAS: son remediaciones de este mismo patron que
reintrodujeron el patron.** Tres de catorce ya no es anecdota. El caso mas claro es TASK-0329, que
lo hizo DOS VECES en la misma entrega: existia para arreglar "la exencion de fichero entero ciega el
gate" y cambio un gate CIEGO por uno FRAGIL; y el contrato que anadio **para impedir la cuarta
divergencia entre los dos escaneres** ata como se escribe la tabla -- con un regex de indentacion
fija -- en vez de atar que los dos escaneres coincidan.

Lectura para calibrar la regla: cuando pedimos "ata la propiedad, no la forma", la respuesta natural
del implementador es **ofrecer otra forma mas estrecha** -- una linea en vez de un fichero, una
etiqueta `shell: bash` en vez de nada. Estrechar la forma reduce el dano y por eso parece un
arreglo; pero no cambia la clase del defecto. Por eso R1 debe pedir explicitamente que el criterio
**sobreviva a un cambio de coordenada, de orden y de formato**, y no solo que sea mas estrecho que
el anterior.

**Tres de los seis rojos de la suite revivida los causamos NOSOTROS** con cambios correctos: 0316
hizo obligatorio un parametro, 0319 reordeno un reseteo, 0321 anadio campos a una linea de log. Cada
uno bien por separado. Ninguno detectado.

**Y la ocurrencia 10 es la que mejor justifica esta decision, porque es RECURSIVA.** La tarea cuyo
proposito era cerrar "declarado no es verificado" entrego un arreglo que era "listado no es
exigido": el gate nuevo distinguia declarado de listado, pero no listado de EJECUTADO. Y el
Arquitecto -- yo -- lo dio por bueno tras comprobar que los runners APARECIAN en el workflow, que es
exactamente la comprobacion floja que la propia tarea denunciaba, un nivel mas arriba.

Ese detalle importa para calibrar la regla: **no basta con enunciar el principio.** Yo lo tenia
escrito en este mismo borrador y aun asi verifique la existencia en vez del efecto. Lo que lo cazo
no fue la regla: fue un checker independiente midiendo el CI real.

## Lo que se propone

**R1 -- Un negativo permanente ata el EFECTO observable, no la forma sintactica.**
Prohibido, como unica atadura: `assert <literal> in source`, exigir una posicion de subcadena, o
comprobar un keyword concreto cuando la propiedad admite otras formas. La prueba de que un contrato
cumple R1: **al menos dos formas distintas y correctas del codigo deben pasarlo, y una rota debe
caer.** Si solo pasa la forma actual, ata sintaxis.

**R2 -- Todo contrato declarado debe ser EJECUTADO Y EXIGIDO por un gate, y el mecanismo debe
fallar solo.**
Un contrato cuyo runner no este cableado es un ERROR del gate, no una linea de inventario. Y
"cableado" no basta: el fallo del runner tiene que **romper el job**. Ningun recuento de contratos
puede citarse como cobertura sin declarar cuantos se EXIGEN.
La ocurrencia 10 obliga a esta redaccion: una version previa de esta regla decia que TASK-0330 ya lo
implementaba. No lo implementaba -- cableaba sin exigir -- y yo lo di por bueno. La regla se escribe
con las tres palabras separadas a proposito: **declarado, ejecutado, exigido.**

**R3 -- El mutante obligatorio incluye la INALCANZABILIDAD.**
No basta con borrar la linea: hay que dejarla presente y muerta. Es la forma que se escapo en 0324 y
la que 0326 si mato. Todo negativo sobre codigo de produccion debe morir ante ella.

**R4 -- Verdad vacia prohibida.**
Un verificador que no encuentra su objetivo debe FALLAR, nunca devolver "no hay problema". Selectores
por AST, busquedas de bloque y recorridos deben afirmar que encontraron exactamente lo que buscaban
antes de juzgarlo.

**R5 -- Un guard debe declarar QUE garantiza, y demostrarlo.**
Prohibido dejar que un mecanismo aparente una garantia que no da. Si un guard no excluye, se dice.
La exclusion real exige un primitivo atomico, no una relectura.

**R6 -- Mergeado no es desplegado. Se verifica por COMPORTAMIENTO.**
Una tarea que modifica un runtime activo no esta operativa hasta que el runtime se relanza. Al
cerrarla se declara explicitamente que queda pendiente de despliegue, y el despliegue se comprueba
buscando un artefacto que solo el codigo nuevo produciria -- un fichero de lock, un campo nuevo en el
log. "Esta en `done`" no es evidencia de nada operativo.

**R8 -- El gate no es el fichero que editaste. Enumera sus GEMELOS antes de darlo por cerrado.**
Un mecanismo con implementaciones paralelas -- escaner Python y escaner PowerShell en paridad
declarada, runtime vivo y mirror enviado a instancias, dos lectores del mismo `git status` -- no
queda arreglado al arreglar una. Antes de cerrar: **enumera las implementaciones, no los casos**, y
fija la PARIDAD con un negativo permanente, de modo que si manana una se acota y la otra no, el
contrato caiga.
Medido tres veces el mismo dia: el mirror de `examples/full_runtime_instance/` (0333), los dos
lectores con consumidores opuestos (0334) y los dos escaneres de neutralidad (0329). En este ultimo
el gemelo sin acotar era **el que CI ejecuta y el que `new_instance.py` copia a toda instancia
nueva**: se cerro el agujero en la mitad que no se exporta.
Corolario para quien encarga el trabajo: **si preguntas por "los otros ocho FICHEROS", te contestan
por ficheros.** La familia hay que nombrarla en el eje correcto -- y a veces hay dos ejes.

**R7 -- La direccion del fallo es del par CAMBIO-CONSUMIDOR, no del cambio.**
Antes de ensanchar o estrechar lo que un lector compartido observa, se enumeran **todos** sus
consumidores y se declara la direccion para cada uno. El mismo dato de mas puede PROTEGER a quien
decide a quien no matar y ENCALLAR a quien decide cuando empezar. Cuando las direcciones difieren,
se separan los conjuntos y **la separacion se clava con un negativo permanente**: si alguien unifica
los lectores "por coherencia" -- que es la tentacion natural tras cerrar una familia -- el contrato
tiene que caer.

**Contrapeso honesto a R6, medido el 2026-08-08.** La brecha "mergeado no es desplegado" que R6
persigue cerrar **nos protegio por accidente**: la remediacion 2 de TASK-0331 introdujo un
autocurado que borra la lease de un exec VIVO -- fallo abierto y destructivo -- y no causo dano
porque ese codigo no estaba corriendo. R6 sigue siendo correcta: una brecha que a veces salva y a
veces perjudica es una brecha, no una salvaguarda, y confiar en ella es confiar en el azar. Pero al
aplicarla conviene recordar por que existe el retraso: **desplegar rapido lo revisado es bueno;
desplegar rapido lo NO ratificado es como se pierde trabajo vivo.** R6 pide declarar el estado de
despliegue, no acelerarlo por defecto.

## Coste y contrapartida

R1 y R3 encarecen escribir un contrato: obligan a construir dos formas correctas y un mutante de
alcanzabilidad. R2 puede poner CI en rojo al encender verificadores dormidos -- de hecho **hoy lo
esta**, deliberadamente, por el sexto rojo de 0330.

Se acepta a proposito. Un rojo visible con tarea abierta y dueno es un estado sano; un verde que
oculta un fallo conocido no lo es. Toda la evidencia de esta jornada apunta a que el coste de la
segunda opcion se paga entero y mas tarde.

## Lo que NO propone

No cambia DECISION-0020 ni el modelo de claims. No impone contratos por comportamiento donde hoy no
hay ninguno -- solo regula los que existan. No obliga a reescribir los contratos vigentes de golpe:
R1 y R3 aplican a los NUEVOS y a los que se toquen.

## Pendiente antes de proponer formalmente

Que el Analista revise este borrador como cualquier otro artefacto. Catorce ocurrencias medidas son
una base solida, pero la generalizacion a regla es mia y merece la misma capa de verificacion
adversarial que exijo al resto.

Y hay un motivo concreto, no ceremonial: la ocurrencia 10 demuestra que **yo enuncie el principio en
este mismo documento y a continuacion lo incumpli** al validar 0330 comprobando existencia en vez de
efecto. Un borrador escrito por quien acaba de tropezar con su propia regla necesita que lo lea
alguien que no la escribio.
