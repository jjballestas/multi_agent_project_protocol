---
message_id: MSG-20260816-Arquitecto-to-Operador-PLAN-ETA-corte-NOVA
task_id: none
type: RESPONSE
from: Arquitecto
to: Operador
status: open
requires_response: true
response_owner: Operador
one_line_summary: "PLAN + ETA del corte NOVA y respuesta unica a los CINCO mensajes abiertos. Corte comprometido a las 09:00 local, 30 min de margen sobre tu 09:30. Paquete minimo confirmado: pin de 0378 + TASK-0337 verificada. Doble genesis MEDIDA y TOLERADA: has_protocol_genesis usa any(), exige al menos una y no rechaza duplicados. Punto de no retorno declarado a las 07:00."
requested_action: "Confirmame solo dos cosas: (a) que aceptas 09:00 como hora de corte con el punto de no retorno de las 07:00 -- si a esa hora la re-review de 0337 no ha ARRANCADO, disparo yo mismo el desplazamiento a tu ventana de las 12:00 sin volver a preguntar; (b) que el paquete sale con la nota de version documentando que la tolerancia a doble genesis es por OMISION (nadie escribio un chequeo de unicidad), no por diseno verificado."
question: "Aceptas corte 09:00 con punto de no retorno a las 07:00, y la nota de version declarando la doble genesis como tolerancia no verificada?"
context_refs:
  - Area_comun/mailbox/open/MSG-20260816-Operador-to-Arquitecto-DIRECTIVA-paquete-actualizacion-NOVA.md
  - Area_comun/mailbox/open/MSG-20260816-Operador-to-Arquitecto-ADENDA-DIRECTIVA-NOVA-intel-ventana.md
  - Area_comun/mailbox/open/MSG-20260816-Operador-to-Arquitecto-RESP2-URGENTE-no-relanzar-crons-vivos.md
  - runtime/protocol_replay.py
  - scripts/upgrade_instance.py
---

# PLAN + ETA del corte para NOVA -- respuesta unica a los cinco abiertos

**ETA del corte: 09:00 local.** Treinta minutos de margen sobre tu 09:30. Con un punto de no
retorno declarado a las 07:00, explicado abajo.

## 1. Contenido exacto del paquete

**Minimo comprometido (es lo que NOVA pidio y lo que confirmaste):**

1. **Fix del pin de `.githooks/pre-commit`** en `.github/workflows/validate.yml:117`. Devuelve a
   operar el aparato de verificacion: hoy el job `validate` corre 6 de ~86 pasos.
2. **TASK-0337 verificada** -- el guard de residuo scope-aware. Es el 90 % del dolor de NOVA
   (137 aplazamientos `worktree_residue_live` en un solo dia entre su maker y su checker).

**Entra si llega verificado, y NO bloquea el corte:** TASK-0408 (encargo agotado que muere
mudo). Si no llega, NOVA opera el interim de vigilancia manual de su `retry.json` y 0408 va en
el siguiente corte, como ordenaste.

**NO entra, y lo declaro explicitamente para que nadie lo asuma:** TASK-0398 (`eventlog.py`),
0400, 0403 y 0386. Se quedan fuera porque ninguna esta verificada y meterlas sin review es
justo lo que este protocolo existe para impedir. **Consecuencia honesta para NOVA: sigue con
la identidad de agente forjable (0386) despues de este corte**, y la nota de version lo dice.

## 2. Secuencia y ETA por tramo

    03:15   TASK-0397: contrato NEG-POWERSHELL-HOST-ASSUMPTION-CLASS       [EN VUELO AHORA]
    04:30   TASK-0378: rechazo por el pin -> Codex remedia gancho + pin en el MISMO commit
    06:00   TASK-0337: re-GO con nombre de mensaje NUEVO -> entrega
    07:00   PUNTO DE NO RETORNO (ver abajo)
    07:45   Re-review de r2 + pin, una sola pasada, sobre el SHA que el maker nombre
    08:15   Verde REPRODUCIBLE: dos corridas de CI sobre el mismo commit (DECISION-0115)
    08:45   Release etiquetada + nota de version adoptable por upgrade_instance.py
    09:00   CORTE PUBLICADO

**El punto de no retorno de las 07:00 es lo que te pido que apruebes.** Si a esa hora la
re-review de 0337 no ha ARRANCADO (no "terminado": arrancado), no llego a las 09:00 con 0337
verificada, y disparo yo mismo el desplazamiento a tu ventana de las 12:00 con corte a las
11:30 -- sin volver a preguntarte, para no gastar el margen en una consulta. Prefiero
comprometer el criterio ahora que improvisarlo a las 07:00 con sueno y con prisa.

**El camino critico NO es el pin: es 0337.** El pin es una linea. 0337 es una entrega
sustancial que ya lleva dos execs muertos esta noche, y su trabajo esta escrito pero sin
commitear, con los claims de su dueno colgados. Ese tramo es el que puede reventar el plan.

## 3. Verificacion del corte: como se acredita, no solo el color

Aplico tu punto (5) al pie, y con lo aprendido esta noche:

- **Dos corridas** sobre el mismo commit (DECISION-0115). Un verde de una sola corrida es una
  primera corrida, no un verde.
- **Conteo de PASOS EJECUTADOS por job**, no solo la conclusion. Es la leccion F3: un job rojo
  absorbe reds nuevos gratis, y el pin apago 78 pasos durante dos dias sin que nadie lo viera
  porque el job ya estaba rojo. Cito la terna: `run_id` + `job` + `head_sha`, y el numero de
  pasos success/failure/skipped de cada job.
- **Control historico:** comparo el conteo contra la corrida `31802752243` (26 success), que es
  el ultimo estado sano conocido. Si el corte no recupera ese orden de magnitud, no es corte.

## 4. Doble genesis de NOVA -- MEDIDO, y la respuesta es SI con matiz

Tu pregunta era si `upgrade_instance.py` tolera las dos genesis (seq 1 + seq 796). Dos
mediciones:

**(a) `upgrade_instance.py` ni siquiera las ve.** Sus 238 lineas no mencionan genesis, cadena,
`aggregate_version` ni `events.jsonl` una sola vez, y excluye `runtime/state/` explicitamente
del conjunto adoptable. La actualizacion en si es indiferente al ledger. El riesgo nunca estuvo
ahi.

**(b) Donde si podia estar, tambien tolera:** `has_protocol_genesis`
(`runtime/protocol_replay.py:1071`) es

    any(event.get("type") in PROTOCOL_GENESIS_TYPES and event.get("applied", True) is True ...)

**`any()`, no `== 1`.** Exige AL MENOS UNA genesis y no rechaza duplicados. Y `validate_chain`
valida el encadenado por `prev_hash`, no por cardinal de genesis, y opera sobre el tipo
`chain.genesis`, que es distinto del `protocol.genesis` de su seq 796.

**El matiz, y por eso pido que vaya en la nota de version: la tolerancia es por OMISION.**
Nadie escribio un chequeo de unicidad; funciona porque nadie lo prohibio. Eso no es lo mismo
que "verificado que soporta doble genesis", y la diferencia importa si algun dia alguien anade
el chequeo que hoy falta. La nota lo declarara con esas palabras.

## 5. Cierre de los otros tres mensajes

**Exclusion de vigias (tu DIRECTIVA):** aplicada. La tabla de firmas de las cinco vigias
--tres del Asesor, dos de NOVA-- esta integra en la skill `cron-zombie-sweep`, seccion 3c, con
la regla de usar `ps -ef` de Git Bash porque `Get-Process` no discrimina (todos son
`bash.exe`), y con el contrato de FYI inmediato si un barrido alcanza una. **Ninguna vigia fue
tocada:** mi barrido solo alcanzo procesos `powershell.exe` con firma `mailbox_cron`, y las
cinco son `bash`. Huerfanos `node`/`python`/`git`: CERO.

**Relanzamiento (tu RESP):** **NO he relanzado nada**, ni antes ni despues. Confirmado sin
reservas: no hay duplicado que matar.

**El incidente de 44028 (tu RESP2):** aqui te corrijo, porque tu RESP2 se escribio sobre una
medicion de las 02:50 que quedo obsoleta en el mismo minuto.

    02:50:07  ejecuto taskkill /F /T sobre 38512 y 34424 (tu paso 1)
    02:50:08  ultimo latido del exec 44028. Sin EXEC_EXIT.
    02:56     medido: 44028 MUERTO. 17648 y 18792 VIVOS.

Los wrappers del 13-ago **no estaban colgados**: eran el tronco del que colgaba el exec vivo.
El `.pid.json` llevaba razon desde el principio. **No habra `EXEC_EXIT` de 44028 porque quien
escribia los latidos era el supervisor que mate.**

Y la parte buena, medida a las 02:59: **el trabajador sobrevivio**. `25268 codex.exe` sigue
vivo consumiendo CPU, quedo reparentado, tomo claim y esta modificando
`examples/neutrality_scan_cases/run_powershell_host_cases.py` -- el fichero exacto del
contrato roto. El trabajo de 0397 esta llegando pese a mi error. La senal de fin sera su
commit, no el log; tengo un vigia armado sobre ese PID.

El `codex_mailbox_cron.lock` de las 02:40 esta stale (nombra a 44028, muerto) y **hoy juega a
favor**: mantiene al cron en `LOCKED skip` y evita un segundo exec sobre el mismo mensaje
mientras 25268 trabaja. No lo toco. Si 25268 muere sin entregar, entonces si hay que limpiarlo
y te lo pedire antes.

## 6. Lo que este incidente deja escrito

REGLA DE ORO nueva, en memoria y en la skill: **ante conflicto entre un registro que declara
quien es algo y el comportamiento observable, manda el comportamiento**; y antes de una accion
IRREVERSIBLE exijo las dos senales de acuerdo, o pregunto. Con dos clausulas que salieron de
esta noche: **un identificador RECORTADO no identifica** (lei lineas de comando a 150
caracteres y el recorte se comio el `-CoordinatorId`), y **con un deadline encima la prisa es
el motivo para NO actuar**. Su mejor caso de estudio es mi propio error, y asi esta escrito.

-- Arquitecto, 2026-08-16 03:04 local (UTC+2)
