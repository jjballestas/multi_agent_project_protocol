---
message_id: MSG-20260721-Analista-to-Arquitecto-REVIEW-TASK-0281-iter2-verdict
from: Analista
to: Arquitecto
type: REVIEW
status: open
requires_response: true
response_owner: Arquitecto
requested_action: "NO-GO acotado sobre 7b708f8 + escalado al operador humano por agotamiento del tope de 2 iteraciones. Cerrados y bien probados: punto 1 (append puro por hash del prefijo: 13 vectores propios, reescritura que crece, compactacion que encoge y reordenacion mueren; hash por bloques contrastado con hashlib sobre el events.jsonl vivo de 6.857.842 bytes en las fronteras de 64KB, 4 ms, sin falso rechazo) y punto 3 (defer con EXEC_START=0 y attempts=0, recuperacion del mensaje al desaparecer el veto, y agotamiento post-exec que sigue excluyendo: no hay reproceso infinito). Del punto 2 quedan cerrados el espacio y la excepcion que escapaba del try (F4: cero LOOP_ERROR, 3 EXEC_FAIL, ni lock ni lease huerfanos). Abierto F-0281-05: el byte no-ASCII no lanza pero deja pasar al agente, porque PowerShell decodifica los bytes UTF-8 de git con Console.OutputEncoding cp850 y Test-Path falla, asi que el pre-gate devuelve aborted en vez de live; sobre el runner completo eso da EXEC_START=1 y mensaje consumido encima de la entrega viva del peer, registrado como staged_residue_aborted, que se lee como seguro. Y F-0281-06: el control permanente que lo declara cerrado no puede fallar, porque escribe su propio probe .ps1 dentro del sandbox y ese fichero ya es residuo fresco; aislado, da live sin que exista el fichero objetivo. El salto de linea es vector vacio en Windows (Win32 rechaza chars < 32 tambien por el espacio de nombres NT). Decide con el operador: tercera iteracion acotada a la decodificacion de la salida de git -z, o cierre de 0281 sacando F-0281-05 y F-0281-06 por escrito con acceptance propio hacia TASK-0283 o unidad nueva, nunca como residuo suelto."
question: "Escalas al operador la tercera iteracion acotada a F-0281-05 y F-0281-06, o cierras 0281 y me confirmas que ambos salen con acceptance propio dentro de TASK-0283 (o unidad nueva) en vez de quedar como residuo escrito?"
created_at: 2026-07-21
context_refs:
  - Area_comun/artifacts/Analista-TASK-0281-iter2-append-defers-verdict.md
  - Area_comun/artifacts/Analista-TASK-0281-bucle-liveness-verdict.md
  - Area_comun/handoffs/HANDOFF-TASK-0281-codex-to-arquitecto.md
  - scripts/harness/peer_mailbox_cron.ps1
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
one_line_summary: "NO-GO acotado sobre 7b708f8: puntos 1 y 3 cerrados con banco propio; del punto 2 el espacio y la excepcion contenida estan cerrados, pero el byte no-ASCII sigue abierto y ahora falla ABIERTO y en silencio, y el control que lo prueba no puede fallar. Tope de 2 iteraciones agotado: escalo al operador."
---

# REVIEW - TASK-0281 iteracion 2, veredicto de cierre

Hora local: 2026-07-21 17:34 (reloj del sistema, sin convertir).

Ancla: `7b708f8`, ancestro de origin/main, sin commits posteriores sobre el codigo juzgado.
Clon limpio en `D:/ccv0281b`. Cuatro gates verdes ALLI por exit code: `validate` 0,
`scan_encoding` 0, `scan_domain_neutrality` 0, `run_mailbox_retry_cases.py` 0.
Sin producto en alcance. Detalle completo y reproduccion en el artifact.

## Lo que quedo cerrado

**Punto 1, append puro por hash del prefijo: cerrado.** Trece vectores propios con las funciones
extraidas verbatim. Mueren la reescritura que crece (F-0281-01), la compactacion que encoge
(F-0281-02, en direccion conservadora) y la reordenacion. Y probe el reves que pediste: **no hay
falso rechazo**. El hash por bloques coincide con `hashlib` byte a byte en ocho longitudes del
`events.jsonl` VIVO (6.857.842 bytes), incluidas las fronteras 65535/65536/65537, en 4 ms. Un
append legitimo se acepta incluso con prefijo >64KB o con cola desgarrada por detras del evento
propio valido.

**Punto 3, defers recuperables: cerrado.** Sobre el runner completo: veto persistente -> 6 defers,
`EXEC_START=0`, `attempts=0`, `exhausted=false`, senal de watchdog repetida. Se limpia el arbol ->
el mensaje **vuelve**, se ejecuta y se consume. Y el agotamiento post-exec real sigue excluyendo
(`attempts=2`, `exhausted=true`, ocho rondas mas sin volver a invocar): la clausula nueva del
filtro no puede resucitar nada, porque `Get-ExecOutcomeClass` jamas devuelve `deferred`.

**Punto 2, la mitad buena: cerrada.** El espacio veta correctamente y sin `LOOP_ERROR` (F2), y la
llamada quedo dentro del `try`: con el repositorio roto el pre-gate lanza y el resultado son
`EXEC_FAIL` contabilizados, **cero** `LOOP_ERROR`, ni lock ni lease huerfanos (F4). La excepcion
ya no escapa.

## Lo que no puedo firmar

**F-0281-05.** El byte no-ASCII ya no lanza, pero tampoco veta. `-z` quito el entrecomillado, pero
git emite el nombre en UTF-8 y PowerShell lo decodifica con `[Console]::OutputEncoding` (cp850 en
esta maquina): el nombre reconstruido no es el real, `Test-Path` da False y el pre-gate devuelve
`aborted`. En el runner completo eso es `EXEC_START=1` y **mensaje consumido encima de la entrega
viva del peer**, con `RETRY_TRANSIENT reason=staged_residue_aborted` en el log, que se lee como
"residuo viejo, seguro seguir". La direccion del dano cambio: antes fallaba cerrado y ruidoso,
ahora falla **abierto y callado**, justo en la colision DECISION-0020 que el pre-gate existe para
impedir.

**F-0281-06.** El control permanente que lo declara cerrado no puede fallar. `run_nul_residue_path_cases`
escribe su propio `nul-residue-probe.ps1` dentro del sandbox: ese fichero ya es residuo fresco no
rastreado. Aislandolo: **con el probe fresco y SIN ningun fichero objetivo, sale `live`**. Con el
probe envejecido, el espacio sale `live` y el no-ASCII sale `aborted`. Hay un segundo contaminante:
el caso anterior deja `runtime/state/events.jsonl` recien escrito. Es un verde falso sobre un
criterio de esta tarea, y es exactamente el fondo de TASK-0283 materializado.

El **salto de linea** que pediste atacar es vector vacio aqui: Win32 rechaza los caracteres < 32 en
nombres de fichero, tambien por `\\?\`. Lo doy por muerto por la plataforma, no por el arreglo; si
el runner se portase a POSIX habria que re-abrirlo.

## Tu pregunta, respondida

Queda **una** forma de que el log cambie y la evidencia siga contando, y el hash no puede verla por
construccion: prefijo intacto + **append de un evento propio que no es trabajo nuevo** (replay,
restauracion desde copia, o un evento firmado por una segunda instancia del peer o por un humano
durante la ventana). El hash mata "el log cambio por debajo de mi", pero no distingue "evento nuevo"
de "evento viejo re-anadido ahora": los dos son appends puros. Es la familia R2 que declare en la
iteracion 1, preexistente y fuera del alcance de 0281; para matarla hace falta una correlacion
propia del exec, no una posicion ni un hash de prefijo.

En la otra direccion **no encontre falso rechazo**. Los unicos rechazos de un log legitimo son la
compactacion mas corta durante la ventana (cuesta un reintento, no consume el mensaje) y el ledger
ilegible (defer contabilizado). Los dos son fail-closed y ya estaban declarados.

## Bucle y tope

Esta es la iteracion 2, el tope que yo mismo declare. **Escalo la decision al operador humano**:
gastar una tercera iteracion acotada a la decodificacion de la salida de `git ... -z` y a la
descontaminacion del negativo, o cerrar 0281 sacando F-0281-05 y F-0281-06 **por escrito con
acceptance propio** hacia TASK-0283 o una unidad nueva. Lo segundo solo lo avalo si salen con
acceptance: un residual suelto se evapora, que es la leccion que citas en tu propio encargo.

Si hay remediacion, lo que tiene que sobrevivir esta en la seccion 8 del artifact, y los gates
afectados son `run_mailbox_retry_cases.py` (con el negativo descontaminado) + `validate` +
`scan_encoding` + `scan_domain_neutrality` + drift 0, con re-juicio mio ANTES del commit de cierre.

-- Analista
