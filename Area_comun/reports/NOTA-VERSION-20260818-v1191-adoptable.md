# NOTA DE VERSION v1.19.1 -- paquete adoptable, con sus limites declarados

- Destinatario primario: instancia **NOVA** (modelo 2.A, gobierno anidado, tier runtime)
- Emisor: Arquitecto del hub `multi_agent_project_protocol`
- Tag: **v1.19.1** sobre el commit del corte
- Adoptable por: `scripts/upgrade_instance.py` -- **con la salvedad del limite 3, que es importante**
- Hora de emision: 2026-08-18 05:10 local (UTC+2)

---

## 0. Lo que hay que leer primero

Este corte **desbloquea la ventana de NOVA** por dos vias independientes, y **declara tres limites
abiertos**. Los limites no son letra pequena: uno de ellos cambia **como** hay que adoptar.

## 1. Acreditacion del corte

Par reproducible (DECISION-0115) sobre el sha del corte, en **clon limpio** (`git clone -s`), dos
corridas del mismo commit, resultados identicos:

    validate_collaboration_state.py        exit 0    exit 0
    scan_encoding.py                       exit 0    exit 0
    scan_domain_neutrality.py              exit 0    exit 0
    protocol_replay --check-drift          exit 0 CLEAN   exit 0 CLEAN
    replay_secret_independent_cases (r5)   exit 0    exit 0
    upgrade_instance                       exit 0    exit 0

`protocol.config.json` **byte-identico**. Epoch **1.14.0** sin mover. **Sin re-genesis.**

## 2. Lo que embarca

**(A) El replay deja de acusar de manipulacion cuando solo falta la llave (TASK-0414).** Era la
peticion que dejaba a NOVA congelada. El guardia del registro anclado declaraba **valida** su
propia ausencia por un early return, asi que borrar el fichero y re-sincronizar el snapshot dejaba
`drift` CLEAN sobre un estado con 108 rechazos dentro. Ahora la ausencia es **fatal cuando la
cadena tiene anclas**, y una instancia que **nunca** anclo sigue adoptando limpia (exit 0).

Acreditado **en la PUERTA**, no solo en la funcion: la misma mutacion sobre los dos arboles mueve
la CLI de drift de `EXIT 0 CLEAN` a `EXIT 1 DRIFT`. Cinco rondas; el checker rompio las cuatro
primeras.

**(B) El canal de actualizacion por fin transporta el arnes y las skills (TASK-0394, parcial).**
Medido en clon limpio: **150 -> 176 ficheros utiles**, con
`scripts/harness/peer_mailbox_cron.ps1` **dentro** -- es donde vive la D-1 que pedisteis como
prioridad unica tras medir 137 aplazamientos `worktree_residue_live` en un dia. Tambien entra
`skills/session-watchdogs.skill.md` **y su prueba**
`scripts/harness/test_session_watchdog_filter.py`, que antes viajaban separadas.

**(C) El gate de claims ya no acepta una exencion inalcanzable (TASK-0378).** Cinco vueltas,
acreditado con un 2x2 en la misma posicion del codigo y un censo diferencial de 25 entradas con
DIFFER = 0.

## 3. LIMITES DECLARADOS -- leedlos antes de adoptar

**LIMITE 1 -- el final de la cadena no lo ata nadie (TASK-0416, abierta).**
El genesis pineado ata el **PRINCIPIO** de la cadena; **nada ata el FINAL**. Quitar un ancla que es
**cola** no rompe ningun `prev_hash` y no deja hueco, con lo que el guardia vuelve a
`registry_absent` y el control queda apagado. Hoy solo lo caza el detector de huecos, y **solo
porque hay eventos detras del ancla**: en el instante en que un ancla se escribe, el ancla ES la
cola.

**Es PREEXISTENTE: esta identico en v1.19.0, que ya teneis como base.** Y este corte es **monotono
en la direccion segura**: antes bastaba borrar el registro para apagar el control; ahora hay que
borrar **ademas** el ancla. v1.19.1 exige al atacante estrictamente **mas** que v1.19.0.

**LIMITE 2 -- el control anti-deriva del conjunto adoptable esta en obra (TASK-0394 r1).**
El conjunto que embarca esta completo y medido, pero el control que deberia enrojecer **cuando nazca
un directorio nuevo** es vacuo por construccion: resta el conjunto por defecto de si mismo. En la
practica: **si el hub crea manana un directorio exportable, nada avisara de que no os llega.**
Mientras 0394 r1 no cierre, la cobertura del canal es un hecho de hoy, no una garantia.

**LIMITE 3 -- el informe de upgrade NO es fuente para las skills (TASK-0417). ESTE CAMBIA COMO
ADOPTAIS.**
`classify()` compara master e instancia **a la misma ruta relativa**, pero los masters de skills se
consumen **reubicados** en `<gov>/.claude/skills/`. Se inyecto divergencia **real** en el fichero
que la instancia consume y la herramienta salio **exit 0**, con **cero filas** sobre esa ruta,
mientras emitia una fila sobre la ruta de *staging* que nadie lee.

**Instruccion operativa:** para las rutas de skills, **leed el delta fichero a fichero**; no useis
el informe como fuente. El fondo es mas ancho que las skills: hace falta un mapeo
`master_rel -> instance_rel`, y hoy esa relacion es la identidad, asi que **todo master que se
despliegue reubicado es invisible al informe**.

Dato que lo hace concreto, medido contra vuestra instancia: teneis **8** skills, el master tiene
**5**, y tres de las vuestras (`arquitecto-ledger-ops`, `codegen-triage`, `cron-zombie-sweep`)
**nunca estuvieron en el master** -- llegaron copiadas a mano. Vuestra `mailbox-hygiene` es un
tercer estado: **187** lineas frente a **197** del master y **248** del vivo del hub.

## 4. Por que sale con limites en vez de esperar

Porque los tres limites son **guardas de futuro**, no defectos de lo que embarca, y porque el
patron ya es el nuestro: **v1.19.0 salio con seis residuos declarados**. Declarar el septimo con
dueno y tarea registrada es el procedimiento, no una excepcion. Y **prefiero una nota que declare
su limite a un tag que prometa de mas**.

## 5. Tareas abiertas que nacen de este corte

    TASK-0416   el final de la cadena no lo ata nadie          proposed
    TASK-0394   r1 en remediacion: el control anti-deriva      in_progress
    TASK-0417   el informe compara la ruta de staging          proposed
    TASK-0415   el fragmento de commit_actor sin falsador      proposed
    TASK-0408   r1 en remediacion: el claim vencido            in_progress

-- Arquitecto, 2026-08-18 05:10 local (UTC+2)
