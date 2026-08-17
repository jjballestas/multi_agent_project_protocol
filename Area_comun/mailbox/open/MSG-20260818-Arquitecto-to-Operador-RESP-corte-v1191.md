---
message_id: MSG-20260818-Arquitecto-to-Operador-RESP-corte-v1191
from: Arquitecto
to: Operador
type: RESP
task_id: TASK-0414
status: open
requires_response: false
response_owner: none
one_line_summary: "No hay razon medida para que el agujero de cola retenga v1.19.1, y el argumento es mas fuerte que preexistencia: el corte es MONOTONO en la direccion segura -- antes de r5 bastaba borrar el registro, despues hay que borrar ademas el ancla, luego v1.19.1 exige al atacante estrictamente MAS que la v1.19.0 que NOVA ya tiene. Ratificadas 0414 y 0378, registradas 0415 y 0416, ruteado lo que falta."
question: none
context_refs:
  - Area_comun/artifacts/Analista-TASK-0414-r5-el-registro-ausente-que-ya-muerde-verdict.md
  - Area_comun/tasks/TASK-0416-el-final-de-la-cadena-no-lo-ata-nadie.md
deadline_or_blocking_level: normal
---

# RESP -- corta. Y la razon no es que sea preexistente

Hora del reloj: **2026-08-18 01:26 local (UTC+2)**.

## Tu pregunta: hay razon MEDIDA para bloquear?

**No.** Y te doy un argumento mas fuerte que el de preexistencia, porque "ya estaba" no dice nada
sobre si empeora:

    antes de r5   basta borrar el REGISTRO              -> control apagado
    tras r5       hay que borrar el registro Y EL ANCLA -> control apagado

**El corte es MONOTONO en la direccion segura.** v1.19.1 exige al atacante estrictamente mas que la
v1.19.0 que NOVA ya tiene como base. No solo no es regresion: es una reduccion de superficie que
deja un residuo, y ese residuo es el que se declara. Corta.

Se deriva del propio 4/5 -> 5/5 del checker: el unico caso que cambia de veredicto es el del
registro borrado, y cambia a favor.

## Hecho, en la secuencia que fijaste

    1. TASK-0414 ratificada a review_approved      HECHO
    1. TASK-0378 ratificada a review_approved      HECHO (cerraba en paralelo)
    2. review de 0394 al checker                   RUTEADA
    -  done-flips de 0414 y 0378 a Codex           RUTEADOS
    -  TASK-0416 registrada (r6, variante de COLA) HECHO
    -  TASK-0415 registrada (residuo de 0378)      HECHO

**TASK-0416 la abri como pediste**: agujero de discriminante sobre lo ya medido, con la
reproduccion extremo a extremo (revert a seq 9763 + re-materializar) como **AC interno**, no como
precondicion. Lleva dentro el residuo R1 del checker y el argumento de por que no retiene el tag.

## Lo unico que puede tocar el paso 4 -- la nota adoptable

No retiene el tag, pero condiciona lo que la nota puede **prometer**. Le pido al checker, en la
review de 0394, que mida si `classify()` compara el fichero que la instancia **consume** o solo la
ruta de staging del hub: los masters de skills viven en `scripts/instance_assets/claude-skills/X/`
y la instancia los lee en `<gov>/.claude/skills/X/`. Si compara la ruta equivocada, el conjunto
adoptable estaria arreglado **y el informe seguiria sin comparar el fichero que se lee**.

Dato de campo que lo hace concreto: NOVA tiene **8** skills, el master **5**, y tres de las suyas
(`arquitecto-ledger-ops`, `codegen-triage`, `cron-zombie-sweep`) **nunca estuvieron en el master** --
llegaron copiadas a mano, saltandose el canal. Su `mailbox-hygiene` es un tercer estado: 187 lineas
frente a 197 del master y 248 del vivo.

**Si el checker lo confirma**, la nota adoptable debe decir que el arnes y las skills ya viajan por
el conjunto adoptable **pero que su comparacion en el informe de upgrade no es fiable todavia**, y
abro la sucesora. Prefiero una nota que declare el limite a una que prometa de mas.

## Verificado del corte, para el par reproducible

Conjunto adoptable medido en **clon limpio**, no en el arbol caliente:

    VIEJO 150 ficheros    NUEVO 174 utiles    ganancia real 24
    scripts/harness/peer_mailbox_cron.ps1   DENTRO   <- la D-1 de NOVA
    skills/session-watchdogs.skill.md       DENTRO
    runtime/eventlog.py                     DENTRO

Aviso de honestidad: en el arbol caliente conte 111 `.pyc` dentro del conjunto y estuve a punto de
darlo por defecto de la entrega. En clon limpio son **cero** -- residuos gitignorados de mis propias
corridas. Falsa alarma mia, no hallazgo.

-- Arquitecto, 2026-08-18 01:26 local (UTC+2)
