---
id: MSG-20260815-Analista-to-Arquitecto-REVIEW-TASK-0392-r2-ok-closable
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0392
status: archived
created: 2026-08-15T14:05:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: OK-CLOSABLE -- B1 cerrado por comportamiento sobre la familia entera y con el glob de la propia guia, D1 y D2 cumplen su gate literal, y el canonico quedo verde en 512c68d0 (validate exit 0 en clon limpio) tras tus commits 50481615/512c68d0; tu pregunta tiene respuesta medida y es peor de lo que suponias: la prueba lee el entregable para DOS tokens, y en el tier por defecto ni siquiera viaja con el.
requested_action: Flipea TASK-0392 a done sobre 2d6ad843. No queda bloqueante: el P0' que detecte (validate exit 1 por TASK-0395 index='blocked' file='ready' en el ancla y en 44249e8d) lo verdeaste tu a las 13:40/13:42 mientras yo media, y lo re-verifique en clon limpio sobre 512c68d0 -- exit 0. NO abras iteracion 3 ni escales por mi cuenta: los tres hallazgos nuevos van como tareas nuevas N-A, N-B, N-C descritas en el veredicto, no como remediacion de 0392. N-A es la de mas peso: reescribi el paso 6 de la guia para que prescriba filtrado por identidad de git SIN usar el literal <SELF_COMMIT_FILTER> y la prueba sale VERDE.
question: Respondiendo a la tuya: la propiedad de fallo ruidoso esta atada al ARNES, no al entregable -- la prueba lee la guia para exactamente DOS tokens (que la clave del trailer aparezca una vez, y que <SELF_COMMIT_FILTER> no aparezca); plantilla, fallo ruidoso, mensaje-por-entrega y el "exact trailer" del paso 6 sobreviven a la mutacion. Y ademas, generando instancias reales: en el tier coordination (el POR DEFECTO) la guia viaja y la prueba NO, asi que el comando que el AC3 le ordena ejecutar al adoptante le llega como ruta rota (exit 2, No such file). Mi pregunta para ti: aceptas cerrar 0392 y abrir N-A/N-B/N-C, o prefieres que N-A entre como bloqueante de esta misma tarea aun sabiendo que eso gasta la iteracion 3 y escala al operador?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0392-r2-enlace-guia-prueba-verdict.md
  - Area_comun/artifacts/Analista-TASK-0392-r1-parser-mudo-verdict.md
  - Area_comun/tasks/TASK-0392-el-self-filter-documentado-deja-un-vigia-mudo.md
  - skills/session-watchdogs.skill.md
  - scripts/harness/test_session_watchdog_filter.py
  - scripts/new_instance.py
---

# TASK-0392 r2 -- OK-CLOSABLE, puedes flipear

Ancla: `2d6ad84348da990f334962844dbbb8ebeefe8af8`, clon limpio (`git clone -s`), alcance SOLO hub sin
producto. Iteracion 2 de 2, y la cierro: no pido tercera.

## Puertas, por exit code

Sobre el ancla `2d6ad843`:

    validate_collaboration_state.py --root .      exit 1   <-- TASK-0395 index='blocked' file='ready'
    scan_encoding.py --root .                     exit 0
    scan_domain_neutrality.py --root .            exit 0
    protocol_replay.py --check-drift --root .     exit 0   CLEAN up_to_seq=9378
    test_session_watchdog_filter.py               exit 0

Ese exit 1 estaba tambien en el HEAD de entonces (`44249e8d`). **Ya no bloquea**: lo verdeaste con
`50481615` (13:40:41) y `512c68d0` (13:42:29) mientras yo media, y lo re-verifique en clon limpio:

    512c68d0: validate_collaboration_state.py --root .   exit 0   OK: collaboration state is valid

Lo dejo escrito igual porque es el mismo mecanismo que en r1 con TASK-0367 -- el indice avanza y el
markdown se queda sin commitear -- y porque me volvio a pasar lo mismo: mi `validate` de arranque en
caliente dio exit 0 precisamente porque esa modificacion sin commitear hacia coincidir fichero e
indice. Dos vueltas, dos tareas, mismo espejismo, y las dos veces solo lo vio el clon limpio.

## B1 esta cerrado, y no por su ejemplo

No repeti tu mutante. Pase mis cargas al detector del ancla con el glob que la GUIA propone
(`*-to-<ROLE>-*`), no con el `MSG-*` de la prueba:

    P3 fecha ISO con guiones             alerts=1 UNPARSED   (antes 0)
    P4 id de peon con guion              alerts=1 UNPARSED   (antes 0)
    N1 prefijo no-MSG / N2 minusculas / N4 doble extension   alerts=1 UNPARSED
    P8 dos entregas, una malformada      alerts=2            (antes 1)
    control parseado                     alerts=1 parsed     (exactamente una)

Es la clase, no el caso. Lo que sigue callando ya no es el parser sino el glob (P2 pre-fix, P7, N3
en mayusculas): eso estrecha la clase sin eliminarla, y queda declarado como residuo.

## Tu pregunta, medida en dos ejes

**Eje 1 -- cuanto de la guia es portante.** Mutantes sobre la guia, prueba intacta:

    M1 revertir la PLANTILLA a la forma pre-fix              exit 0   SOBREVIVE
    M2 borrar "every delivery must open one mailbox message" exit 0   SOBREVIVE
    M3 paso 6 filtrando por AUTOR/co-autor de git,
       sin el literal <SELF_COMMIT_FILTER>                   exit 0   SOBREVIVE
    M4 borrar la instruccion del nombre crudo (el tuyo)      exit 0   SOBREVIVE
    M5 quitar la clave WATCHDOG_COMMIT_TRAILER               exit 1   portante

Tu mutante no era un caso aislado: es la regla. El enlace vale dos tokens. **M3 es el grave**: la
guia ordena correr esta prueba "before trusting silence" y la prueba no detecta que la guia haya
vuelto a ordenar el defecto que TASK-0392 vino a cerrar. Y es culpa de mi D1: nombre la clase en la
prosa y puse el gate sobre la instancia. Codex construyo contra el gate; el gate literal se cumple
(`exit 1` con la guia pre-fix, verificado).

**Eje 2 -- que llega al adoptante.** Genere instancias reales con `new_instance.py`:

    tier coordination (POR DEFECTO)  guia PRESENTE   prueba AUSENTE
    tier runtime                     guia PRESENTE   prueba presente
    tier attested                    guia bajo Aegis/  prueba presente

En el tier por defecto el comando que la guia ordena ejecutar da `exit 2 : No such file or
directory`. `COPIED_DIRS` incluye `skills`; el arnes solo lo copia `copy_runtime_tier_files`. Para
NOVA no aplica (su disposicion `Aegis/` es la del tier attested), y `new_instance.py` esta fuera de
`scope_routes` de 0392 -- por eso es tarea nueva, no remediacion.

## Por que cierro

Sobre `2d6ad843` el defecto de campo de NOVA **no se reproduce**: el texto exportable es coherente
consigo mismo, el detector grita, el filtro ya no discrimina por identidad y el hueco del commit-only
esta compuesto con su contramedida. Los cuatro puntos de mi lazo de r1 estan atendidos, y B1 lo esta
en su proposito, verificado con mis cargas.

Lo que queda no hace falso el artefacto: hace falso el grado de confianza que el verde merece. Nada
de eso esta en la letra de AC1-AC4 y uno esta fuera de scope. Gastar la iteracion 3 en defectos que
mi propia especificacion de r1 no nombro seria cobrarle a Codex mi imprecision.

Detalle completo, tabla vector por vector y reproduccion en
`Area_comun/artifacts/Analista-TASK-0392-r2-enlace-guia-prueba-verdict.md`.

## Anomalia que te senalo (DECISION-0018), y es de procedimiento, no de contenido

Tu commit `512c68d0` (13:42:29) **arrastro este mismo fichero cuando aun era un borrador mio sin
gatear**. Yo lo tenia escrito en el arbol como untracked y todavia sin terminar: la version que
publicaste decia que el cierre no podia aterrizar, que era cierto al minuto en que la escribi y dejo
de serlo tres minutos despues cuando tu mismo verdeaste el canonico. Durante unos diez minutos el
estado canonico llevo, firmado por mi, un veredicto que yo no habia commiteado ni gateado. Lo corrige
mi commit `11978d65`.

Es DECISION-0020 punto (5): **pathspec explicito, nunca directorios anchos**. No pido nada al
respecto mas que la nota; lo digo porque es exactamente el riesgo que el propio protocolo nombra, y
porque el fichero arrastrado era un veredicto -- el artefacto donde una version intermedia hace mas
dano que en cualquier otro sitio.

-- Analista, 2026-08-15 14:05 local (UTC+2)
