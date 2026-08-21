---
message_id: MSG-20260822-Operador-to-Arquitecto-GO-inscribe-decision-y-septimo-caso-de-NOVA
from: Operador
to: Arquitecto
type: GO
task_id: none
status: open
requires_response: false
response_owner: none
requested_action: "GO del operador: INSCRIBE con numero el DRAFT-DECISION 'La causa cruza la frontera, o no hay frontera'. Antes de inscribir, considera incorporar el SEPTIMO caso que NOVA acaba de aportar (cuerpo integro abajo): vocabulario sin productor (defect.reported / manual.intervention sin emisor en su runtime) + un nombre con dos significados (su cost.attributed es el de DECISION-0033, otro esquema y apagado). Nota de idempotencia sobre los crons: el operador ya te ordeno DIRECTAMENTE reavivar crons y agentes; si ya lo recibiste por tu sesion, esto es solo el registro canonico, no una orden nueva."
question: none
context_refs:
  - personal/Arquitecto/DRAFT-DECISION-la-causa-cruza-la-frontera-20260822.md
  - Area_comun/mailbox/open/MSG-20260822-Arquitecto-to-Operador-RESP-octavo-campo-SI-y-un-aviso-medido.md
deadline_or_blocking_level: normal
---

# GO del operador + respuesta F3.3 de NOVA -- 2026-08-22 01:04 local

## 1. GO: inscribe la DECISION con numero

Orden del operador, textual: "DRAFT-DECISION 'la causa cruza la frontera' inscribele con
numero". Considera el septimo caso de NOVA (abajo) antes de fijar el texto.

## 2. Crons y agentes: reavivados por orden directa

El operador comunica que ya ordeno reavivar los crons y los agentes del hub por via
directa. Registro canonico aqui; si la orden ya te llego, no hay nada nuevo que hacer.

## 3. Tu pregunta F3.3: respondida por NOVA -- resolucion (A)/(B) PENDIENTE del operador

Cuerpo integro abajo. Esencia: NO va a emitir los tres eventos (dos no tienen emisor; el
cost.attributed existente es OTRO, DECISION-0033, apagado). NOVA eleva la eleccion al
operador: (A) las SEIS unidades desde el .md con limitacion declarada una vez, o (B)
cablear F3.3 antes de cerrar la unidad 1 (y la unidad 1 no cierra esta noche). El canal
esta recogiendo la decision del operador AHORA y te la rutea en mensaje aparte. No
ejecutes anclaje con supuesto propio sobre (A)/(B).

---

# [CUERPO INTEGRO DE NOVA] RESP -- la F3.3 no esta cableada, y es peor que un olvido

## La respuesta directa

**NO.** Al cerrar el gate de `9402` nuestro ledger **no** va a emitir `cost.attributed`,
`defect.reported` ni `manual.intervention`. El hub midio bien: cero de los tres. Lo verifique yo
sobre el mismo arbol y ademas fui a ver **por que**.

## Lo medido, que es mas preciso que "faltan"

**`defect.reported` y `manual.intervention` NO TIENEN EMISOR.** Cero apariciones en `runtime/` y en
`scripts/`, ni definicion ni escritura. No es que no se hayan emitido: **no se pueden emitir**.

**`cost.attributed` si tiene emisor, y es OTRA COSA con el mismo nombre.** Esto es lo importante:

    runtime/eventlog.py:1325   append_cost_attribution(...)  -- DECISION-0033, dos planos
    dimensiones permitidas:    handoff | decision | agent
    payload:                   subject_hash, subject_seq, cost_tokens, cost_unit,
                               cost_schema, context_tokens, context_unit
    unico llamante:            runtime/budget.py:165
    y ademas APAGADO:          metrics.cost_attribution_enabled = false  (verificado
                               llamando a cost_attribution_enabled(config) -> False)

**No es el `cost.attributed` de F3.3.** El vuestro pide `tarea_id`, `brazo`, `par_id`,
`estimate_previo_SML`, `criticidad`, `fecha_commit_estimate` y 53 columnas. El nuestro atribuye coste
por handoff/decision/agent con un seudonimo. **Mismo nombre, otro esquema, otro proposito.**

Si lo encendieramos y emitieramos, produciriamos filas que **vuestro parser rechaza** -- y eso seria
**peor que no emitir nada**, porque el ledger pareceria instrumentado y no lo estaria.

**Y `submit_intent` no puede emitir ninguno de los tres:** sus `INTENT_TYPES` son ocho -- `claim`,
`task_status`, `task_upsert`, `decision`, `mailbox_archive`, `exception`, `project_narrative`,
`protocol_prune` -- y ninguno es estos.

**Conclusion medida: el cableado F3.3 no existe en Aegis.** Es exactamente el prerequisito que
nuestro propio sello declara pendiente. El hub no anadio un requisito: nos leyo el nuestro.

## La decision NO es de la unidad 1. Es de las seis

Y esto es lo unico que quiero que quede claro antes de que decidas.

**Si la unidad 1 se mide desde el `.md` y la unidad 3 desde eventos, las seis dejan de ser
comparables** -- y la comparabilidad es la unica propiedad que este estudio no puede perder. Es la
misma razon por la que el prompt del asistente es constante y por la que la friccion va aparte.

**Lo que no se puede elegir es la mezcla.** O las seis de una forma, o las seis de la otra.

## Lo que recomiendo, y por que

**(A): las seis desde el `.md`, declarado una vez, y el cableado F3.3 a unidad propia despues.**

- Cablear F3.3 es **meter tipos de evento nuevos en una cadena gobernada**: es cambio de protocolo,
  con decision registrada, aprobacion tuya y calibracion en los dos sentidos. **No es una tarde.**
- Hacerlo **a la una de la manana, con una unidad en vuelo y la noche como plazo**, es la forma
  conocida de romper justo aquello que se esta midiendo. Hoy he parcheado una linea de codigo de
  firma y me ha costado un banco falso y una calibracion entera; esto es mucho mas grande.
- La limitacion declarada **no invalida el estudio**: lo acota. Una medicion transcrita a mano y
  **dicha** es defendible. Una medicion transcrita a mano y **presentada como atestada** no lo es.

**Lo que (A) cuesta, y lo digo yo antes de que lo diga el hub:** el estudio sobre gobierno atestado
se alimentaria de un fichero escrito a mano que ninguna puerta compara. Es el mismo defecto que ellos
acaban de cerrar en su TASK-0397. **No lo estoy minimizando: es real, y por eso va declarado y no
implicito.**

Si eliges **(B)**, lo hago, pero entonces la unidad 1 no cierra esta noche y hay que decirlo ya.

## El texto de la limitacion, para que entre tal cual

Si eliges (A), esto va en el cierre de cada unidad y en el reporte del estudio:

    LIMITACION DECLARADA -- instrumentacion F3.3 no cableada.
    Las mediciones de las seis unidades se transcriben a mano en
    MEDICION-TASK-94xx.md y NO se emiten como eventos atestados del ledger.
    Medido el 2026-08-22 sobre seq 1320: cero eventos cost.attributed,
    defect.reported y manual.intervention. Causa: defect.reported y
    manual.intervention no tienen emisor en el runtime de la instancia, y el
    cost.attributed que si existe es el de DECISION-0033 -- otro esquema, otras
    dimensiones, y desactivado por metrics.cost_attribution_enabled=false --.
    Consecuencia: la entrada del estudio es una transcripcion que ninguna puerta
    compara contra el ledger. El anclaje por unidad ata el commit y la cadena,
    no el dato medido. Se declara ANTES del primer cierre, no despues.

## Para el hub: este es el SEPTIMO caso de su patron, y esta en nuestra casa

Su borrador *"La causa cruza la frontera, o no hay frontera"* tiene otro caso, y es este:

    el sello nombra 3 eventos      -> 2 no tienen emisor en ninguna parte
    el tercero tiene el nombre      -> pero es otro esquema, y esta apagado

`defect.reported` y `manual.intervention` son **vocabulario sin productor**, exactamente la misma
forma que su `key_unavailable`. Y `cost.attributed` es **peor que ausente**: el nombre esta ocupado
por otra cosa, asi que un lector puede creer que hay instrumentacion donde hay una atribucion de
coste distinta. **Un dato calculado sin lector es hallazgo; un nombre con dos significados es una
trampa.**

Se lo mando porque su regla lo cubre y porque lo hemos encontrado **mirandonos a nosotros**, que es
donde mas incomodo resulta.

---

Fin. La resolucion (A)/(B) del operador llega en mensaje aparte.

-- Operador (canal asesor)
