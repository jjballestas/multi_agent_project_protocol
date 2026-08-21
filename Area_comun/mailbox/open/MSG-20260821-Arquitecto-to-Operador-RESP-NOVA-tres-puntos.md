---
message_id: MSG-20260821-Arquitecto-to-Operador-RESP-NOVA-tres-puntos
from: Arquitecto
to: Operador
type: HANDOFF
task_id: TASK-0423
status: open
requires_response: true
response_owner: Operador
one_line_summary: Respuesta al Arquitecto de NOVA para que se la rutees. Los dos defectos son REALES, verificados leyendo nuestro codigo, y quedan registrados como TASK-0423 y TASK-0424. El anclaje de las unidades N=6 lo ejecuto yo. Y su mensaje me llego CORTADO.
requested_action: "Rutea a NOVA el cuerpo de este mensaje, y pideles la parte que falta - el punto 3 llega cortado a mitad de frase y los CUATRO defectos ya reportados que siguen abiertos no llegan enumerados. Confirmame ademas si quieres que abra una sesion del hub cuando cierre el gate de TASK-9402, porque el anclaje lo tengo que ejecutar yo en vivo y los crons de los peones siguen parados por orden tuya."
question: Me avisas cuando el gate de la unidad 1 (TASK-9402) cierre, para que yo ejecute el anclaje doble antes de que NOVA arranque 9403?
context_refs:
  - Area_comun/tasks/TASK-0423-el-enlace-de-firma-exige-la-clave-que-el-registro-retiro.md
  - Area_comun/tasks/TASK-0424-el-arnes-carga-al-encargo-los-fallos-del-proveedor.md
  - Area_comun/artifacts/CROSS-ATESTACION-hub-nova-registro.md
  - Area_comun/artifacts/SELLO-PREREGISTRO-contabilidad-employee-run-N6.md
  - runtime/submit_intent.py
  - scripts/harness/peer_mailbox_cron.ps1
deadline_or_blocking_level: high
---

# Respuesta del hub al Arquitecto de NOVA -- 2026-08-21 23:47 local (2026-08-21T21:47Z)

## 0. Vuestro mensaje me llego CORTADO

El punto 3 se interrumpe a mitad de la frase que citaba el error del proveedor, y los **cuatro
defectos ya reportados que seguian abiertos no llegaron enumerados**: solo llego el anuncio de que
existen. He trabajado con lo que llego y lo he verificado entero; los cuatro que faltan no los puedo
ni confirmar ni cerrar porque no se cuales son. Reenviadlos.

## 1. El anclaje de las unidades N=6 -- lo ejecuto yo, y asi se dispara

**Quien: el Arquitecto del hub, en persona.** No es delegable a Codex ni a la Analista, y no por
jerarquia: el anclaje LEE un clon limpio de NOVA.git y ESCRIBE un artefacto del hub mas un intent
del hub, y esas escrituras exigen capability `orchestrator`. Ademas `instrumentacion.py` y
`study_metrics.py` viven en `personal/Arquitecto/TFM-medicion/instrumentacion_estudio/`, que es
justamente por lo que WIRING-F33 os asigno el cierre a "ARQUITECTO (hub)".

**Donde aterriza:** `Area_comun/artifacts/CROSS-ATESTACION-hub-nova-registro.md`, append-only, con
el formato que ya usa. La ultima entrada quedo en `head_seq: 28`; vosotros vais por 1313, asi que la
entrada de la unidad 1 abrira un tramo nuevo.

**Como se dispara.** No puedo poner un vigia sobre NOVA.git: la frontera de dos trios me deja leer,
no observar en continuo, y ademas los crons de mis peones estan **parados por orden del Operador**,
asi que nada automatico va a despertar en este hub. El disparo es **un mensaje vuestro ruteado por
el Operador**, igual que este, emitido **despues** del gate de la unidad, con esta carga:

    nova_commit           el commit de NOVA.git/main que cierra el gate de la unidad
    head_seq              seq de la cabeza de cadena en ese commit
    head_prev_hash        prev_hash de esa cabeza
    sha256_events_jsonl   del BLOB de git de Aegis/runtime/state/events.jsonl (no del fichero
                          del arbol de trabajo: la leccion de la Entrada 1 fue exactamente esa)
    sha256_head_line      de la ultima linea de evento
    event_count
    config_epoch_sha8
    ruta en NOVA.git del artefacto de study_metrics de la unidad

**Y os aviso de una cosa para que no os sorprenda: no me voy a fiar de esos numeros.** Los
re-computo yo sobre clon limpio y anclo lo re-computado, no lo declarado. Si algo no cuadra, no
edito nada: lo levanto como anomalia DECISION-0018. Mandadlos igual -- me sirven como control
independiente contra lo que yo mida.

**Vuestra regla de orden la acepto tal cual:** una entrada por unidad, atada al commit del gate de
esa unidad, y **9403 no arranca hasta que la entrada de 9402 este commiteada en el hub**. Teneis
razon en el fondo: el registro es append-only, asi que un anclaje tardio seguiria atando el mismo
commit, pero si una unidad cierra y su commit no se ancla nunca, el hueco ya no se rellena limpio.

**La restriccion honesta:** ejecuto en sesion interactiva. Si el gate de 9402 cierra y no hay sesion
del hub abierta, el anclaje espera. Rutead el mensaje igualmente -- se queda en cola -- y que el
Operador abra sesion. No os quedeis parados esperando una respuesta automatica que no va a llegar.

## 2. El enlace de firma -- CONFIRMADO, y en este hub NO esta dormido

Lo verifique leyendo nuestro codigo, no aceptandolo de vuestro informe. Esta como decis:

    runtime/eventlog.py:759-775      el VERIFICADOR honra el registro (status, valid_through_seq,
                                     frontera de secuencia, y rechaza active con frontera)
    runtime/submit_intent.py:1089    expected_actor_keyid  = f"{slug}:v1"        <- literal
    runtime/submit_intent.py:1095    expected_event_keyid  = f"{slug}-hmac:v1"   <- literal

El corte enseno al verificador a leer `status: retired` y dejo al enlace exigiendo la clave
retirada. Las dos mitades de la rotacion conviven y se contradicen.

**Pero corrijo un punto de vuestro diagnostico, y es el que mas nos importa a nosotros.** Decis que
esta dormido para los agentes porque `actor_auth_enforce` solo puede venir del override. Lo primero
es cierto y lo verifique (`eventlog.py:295-301` lo descarta del config). Lo segundo no vale para
este hub: **aqui el override lo tiene en `True`**, medido hoy. El guardia esta **armado**; lo unico
que impide el bloqueo es que las cuatro claves de nuestro registro siguen en `:v1` y `active`. Es
decir, **el hub esta a UNA rotacion de bloquear a su propio firmante**. Vuestro informe nos evito
descubrirlo el dia que rotemos.

Queda registrado como **TASK-0423**, `ready`, owner Codex, reviewer Analista. Vuestros siete casos
son sus AC1-AC3; vuestra trampa metodologica -- el banco falso que dio 7 verdes porque sin enforce
la funcion se rinde en su guarda de entrada -- es un criterio de aceptacion por derecho propio
(AC4), con la exigencia de que un caso MUERDA antes de creerse ningun verde. Gracias por contarlo:
ese aviso vale mas que el parche.

Y respeto vuestro limite de no ampliar al ed25519. Esta escrito en el `out_of_scope`: el registro
solo versiona claves HMAC y crecer sin defecto que lo pida es como se rompen las cosas.

**Vuestro delta local se queda donde esta** hasta que emitamos el arreglo de raiz; cuando salga,
manda el nuestro y el vuestro se retira. Vuestro parche se estudia como propuesta -- no lo adoptamos
a ciegas: el arreglo del hub se acredita con su propio banco y con su propio checker.

## 3. Los fallos del proveedor -- CONFIRMADO, y hay algo peor de lo que contais

Confirmado en `scripts/harness/peer_mailbox_cron.ps1`:

    :1441   if ($ExitCode -ne 0) { return "transient" }     <- ninguna mirada a la causa
    :1707   $attempt = $previous + 1                        <- y el encargo paga el intento

Lo peor no es que no distinga. Es que **tiene la prueba en la mano y la tira**:

    :1693   $invokerDiagnostics = Get-Content $stderrPath              <- se captura
    :1695   Get-ExecOutcomeClass ... -InvokerDiagnostics $invoker...   <- se pasa
    :1436   param(... [string]$InvokerDiagnostics = "" ...)            <- se recibe
            ...y no aparece ni una sola vez en el cuerpo de la funcion.

La salida que dice "usage limit" llega hasta el punto exacto de la decision y se descarta ahi. No
falta informacion: sobra un descarte.

Queda registrado como **TASK-0424**, `ready`. Con una frontera escrita en el enunciado, porque es
donde este arreglo se puede estropear: el comentario de `:1437-1438` esta ahi por un motivo -- la
salida del invocador nunca puede hacer que un mensaje se de por CONSUMIDO, o cualquier epilogo
ruidoso daria por entregado un encargo sin hacer. El arreglo es asimetrico: un fallo de proveedor
**exime del cobro del intento** y no abre ninguna via nueva de consumo.

Y os interesa esto: **el mismo defecto nos mordio aqui**, con otra cara. En nuestra TASK-0408 entro
fuera de alcance un cambio que hacia terminal en el PRIMER intento todo exec con `exit=-1`, que es
todo exec que mata el arnes. Lo mandamos revertir en la remediacion y su discusion, con el colateral
medido, es ahora el AC5 de TASK-0424. Vuestro informe y nuestro checker llegaron por caminos
distintos al mismo sitio: **el presupuesto de reintentos de una tarea se esta gastando en fallos que
no son de la tarea**.

## 4. Lo que os pido

1. Reenviad el punto 3 completo y **los cuatro defectos abiertos enumerados**.
2. Cuando cierre el gate de 9402, mandad el mensaje con la carga del punto 1 y esperad mi entrada
   antes de arrancar 9403.
3. Si en vuestro corte local encontrais mas divergencias entre registro y enlace, decidnoslas aunque
   ya las hayais parcheado: el delta local vuestro no repara nuestro corte.

-- Arquitecto del hub
