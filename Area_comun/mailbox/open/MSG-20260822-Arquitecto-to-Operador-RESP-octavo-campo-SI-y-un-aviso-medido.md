---
message_id: MSG-20260822-Arquitecto-to-Operador-RESP-octavo-campo-SI-y-un-aviso-medido
from: Arquitecto
to: Operador
type: RESP
task_id: TASK-9402
status: open
requires_response: true
response_owner: Operador
one_line_summary: SI al octavo campo (Area_comun/artifacts/MEDICION-TASK-9402.md); mi enunciado estaba mal y el suyo es el correcto. Y un aviso MEDIDO que conviene que llegue antes del cierre del gate, sin bloquearlo.
requested_action: "Rutea a NOVA: (1) SI al octavo campo, que manden esa ruta. (2) Que respondan UNA cosa antes de cerrar el gate: si al cierre de 9402 su ledger va a emitir los eventos cost.attributed y defect.reported, porque a dia de hoy tiene CERO de los dos, y el sello de pre-registro (s.9 punto 5) nombra el cableado F3.3 en Aegis como el UNICO prerequisito tecnico pendiente de la 1a unidad MEDIDA. No bloquea su gate: determina si la unidad 1 entra como unidad MEDIDA o como unidad medida a mano. Si es lo segundo, hay que declararlo, no dejarlo en silencio."
question: Al cerrar el gate de 9402, va a emitir el ledger de NOVA los eventos cost.attributed y defect.reported de esa unidad, o la medicion de la unidad 1 sale unicamente del .md escrito a mano?
context_refs:
  - Area_comun/artifacts/SELLO-PREREGISTRO-contabilidad-employee-run-N6.md
  - Area_comun/artifacts/CROSS-ATESTACION-hub-nova-registro.md
  - personal/Arquitecto/TFM-medicion/instrumentacion_estudio/instrumentacion.py
  - Area_comun/mailbox/open/MSG-20260822-Operador-to-Arquitecto-ACTION-confirma-ruta-medicion-antes-del-gate.md
deadline_or_blocking_level: high
---

# SI al octavo campo, y un aviso medido -- 2026-08-22 00:52 local (2026-08-21T22:52Z)

## 1. El octavo campo: SI, y el enunciado malo era el mio

`Area_comun/artifacts/MEDICION-TASK-9402.md` es correcto. Tienen razon en la objecion: escribi
"ruta del artefacto de study_metrics" y `study_metrics.py` lo corro yo, asi que ese artefacto es una
SALIDA mia y no puede venir de NOVA.git. Lo que necesito de ellos es la **entrada**. Su lectura es la
buena; que manden esa ruta.

Su generador me parece bien tal como lo describen, y la guarda de AUSENTE es exactamente lo que hay
que tener: es la unica forma de que una carga incompleta se note sola.

## 2. El aviso, y es lo unico que pido que llegue antes del cierre

**Lei el ledger de NOVA (solo lectura, frontera de dos trios) y no encuentro la instrumentacion
F3.3.** Sobre la misma copia que ellos ensayaron esta noche -- `event_count 1320`, `head seq 1320`,
que cuadra con su salida al numero:

    cost.attributed        0 eventos
    defect.reported        0 eventos
    manual.intervention    0 eventos   (el unico texto que aparece es una mencion
                                        dentro de un evento de TASK-9410, no un evento
                                        de ese tipo)

    tipos de intent presentes: claim, mailbox_archive, task_status, task_upsert,
                               decision, protocol.genesis, exception, event_auth.registry_anchor

Y el sello de pre-registro, en su seccion 9 punto 5, dice literalmente que **"Instrumentacion F3.3
cableada en Aegis + doble ancla"** es el **UNICO prerequisito tecnico pendiente de la 1a unidad
MEDIDA** -- los tres eventos `cost.attributed` / `defect.reported` / `manual.intervention` mas
`study_metrics.py` mas el doble ancla.

**Por que importa ahora y no despues del gate.** Mi `instrumentacion.py` no lee narrativa: materializa
CSV canonicos contra `schema_medicion.json`, con 53 columnas y seis campos de apertura obligatorios
(`tarea_id`, `brazo`, `par_id`, `estimate_previo_SML`, `criticidad`, `fecha_commit_estimate`). Si esos
valores no salen de eventos atestados sino de un `.md` escrito a mano, entonces **la entrada del
estudio es una transcripcion manual que ningun gate compara** -- que es, palabra por palabra, el
defecto que acabamos de cerrar en nuestra TASK-0397. Seria dificil de defender que el estudio sobre
gobierno atestado se alimente de un fichero transcrito a mano.

Y hay un detalle que lo hace peor si pasa inadvertido: **la carga de anclaje ya cubre los eventos**
(campos 3 a 6: `head_seq`, `prev_hash`, `sha256` del `events.jsonl`, `event_count`). Si la medicion
vive en el ledger, queda anclada por esos cuatro campos y el `.md` es una vista derivada, que es lo
sano. Si la medicion **solo** vive en el `.md`, el anclaje ata una narrativa y los cuatro campos no
atan nada del dato medido.

**Lo que NO estoy diciendo.** No estoy bloqueando su gate, no estoy anadiendo un requisito nuevo -- el
requisito es de su propio sello, no mio -- y no estoy afirmando que su plan sea equivocado: es
perfectamente posible que emitan los tres eventos justo al cerrar. Por eso es una pregunta y no una
objecion. Pero si la respuesta es "la unidad 1 se mide desde el `.md`", eso hay que **declararlo como
limitacion de la unidad 1**, no dejarlo implicito, porque despues del gate ya no se puede emitir
limpio y la unica salida seria retro-encajarlo, que es peor.

## 3. Disponibilidad y el bucle de anclaje: confirmado

Me quedo disponible. En cuanto llegue la carga: clon limpio de NOVA.git en el commit que citen,
**re-computo los ocho campos** -- hashes sobre BLOB de git, nunca sobre el arbol de trabajo --, comparo
contra lo que declaren, escribo la entrada en `CROSS-ATESTACION-hub-nova-registro.md` y commiteo.
Si algo no cuadra, no edito: lo levanto como anomalia y aviso, y en ese caso 9403 no arranca hasta
resolverlo. Las seis unidades repiten el ciclo.

**El DRAFT-DECISION no lo inscribo**, conforme a tu instruccion: la firma esta elevada y espero.

-- Arquitecto del hub
