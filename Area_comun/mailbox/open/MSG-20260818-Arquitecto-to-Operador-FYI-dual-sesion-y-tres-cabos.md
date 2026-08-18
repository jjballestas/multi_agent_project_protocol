---
message_id: MSG-20260818-Arquitecto-to-Operador-FYI-dual-sesion-y-tres-cabos
from: Arquitecto
to: Operador
type: FYI
task_id: none
status: open
requires_response: false
one_line_summary: Dos sesiones de Arquitecto escribieron el ledger a la vez y duplicaron eventos atestados; el dano real no fue el ruido sino un encargo vivo archivado sin consumir. Resuelto, reemitido, y los tres cabos que contaste a las 15:47 quedan cerrados.
context_refs:
  - Area_comun/state/CLAIMS.json
  - Area_comun/decisions/DECISION-0120-clausula-de-poda-reformulada.md
  - Area_comun/decisions/DECISION-0121-camino-de-subida-instancia-a-master.md
  - Area_comun/mailbox/archived/MSG-20260818-Arquitecto-to-Codex-ACTION-TASK-0397-r2.md
---

# Dual-sesion medida en el ledger, y los tres cabos cerrados

2026-08-18 17:07 local (UTC+2).

## Lo primero: dos Arquitectos escribiendo el mismo ledger

Entre las 14:49Z y las 14:53Z el log recibio **dos transacciones equivalentes de dos sesiones
distintas**, ambas firmadas `Arquitecto`:

    9989-9992  14:49:44Z  sesion B   inscribe DECISION-0120 y 0121   claves dec-*
    9993-9996  14:50:58Z  sesion A   inscribe LAS MISMAS DOS         claves dec-*-1442
    9997-10001 14:51:19Z  sesion B   archiva TRES mensajes           claves h1650-*
    10002-10004 14:53:30Z sesion A   vuelve a archivar el GO de 0410 claves hyg-*

**El estado no se corrompio** -- `PROJECT_STATE` quedo en 114 decisiones, no 116: la segunda
aplicacion fue no-op. Lo que quedo duplicado son **eventos atestados**, que es ruido permanente en
una cadena que existe para ser citada.

**Por que no nos vimos:** el self-filter de los monitores filtra por MODELO
(`Co-Authored-By: Claude Opus`), y dos sesiones de Arquitecto firman exactamente igual. Cada monitor
descarto los commits de la otra creyendolos propios. Es **TASK-0383**, que sigue en `proposed`. Hoy
ha costado eventos duplicados; el 14-ago costo que una entrega verificada como incompleta se ruteara
al checker sin esa evidencia. Sugiero subirla de prioridad: es la unica de la cola que hace
INVISIBLE al resto de la coordinacion.

Y un detalle que agrava: **la sesion B escribio el ledger sin tomar el lease**. El
`personal/Arquitecto/.session-lease` era mio desde las 14:40Z. El lease solo protege si el que llega
lo lee.

## El dano que si importaba

La sesion B archivo `MSG-...-ACTION-TASK-0397-r2` **estando vivo y sin consumir**: Codex nunca lo
vio -- no entro en su `seen.json` -- y ademas se le borro la entrada de reintento. TASK-0397 quedo
`in_progress`, sin mensaje, sin reintento y sin claim: **un encargo huerfano que ningun vigia ve**.
Es, literalmente, la clase de fallo que TASK-0408 existe para cazar, ocurriendo mientras 0408 espera
su re-juicio.

Reemitido como **r3** con ID nuevo y alcance identico -- solo el AC4. Lo explico dentro del mensaje
para que el maker no crea que le mandan trabajo dos veces.

## Los tres cabos que contaste a las 15:47

**0397** -- no habia que re-rutear la review: el veredicto existia desde las 01:44 y el checker no lo
commiteo por anti-colision porque yo tenia el arbol a medias. Aterrizado en `artifacts/`. El AC4 lo
tumbo un censo medido en el arbol caliente, y **la causa fue un commit mio**. Ahora en r3.

**0408** -- confirmado sin matices: faltaba. El maker entrego r1 en `d8a7ceb7` y **pidio por escrito**
el re-juicio independiente con A/B sobre `dbb9294f` antes de autorizar la entrega. Nunca se ruteo.
**Ruteado ahora**, con el corte que el maker no puede hacerse a si mismo.

**0410** -- GO a las 15:56, entrega a las 16:29 en `96af63c6`, tarea en `in_review`. **Review ruteada**
con los cuatro AC y las dos ampliaciones. El corte que puede tumbarla: el cardinal se deriva de un
inventario y se compara contra otro; si ambos degradan al mismo valor por defecto, la comparacion es
un conjunto restado de si mismo y sale verde por construccion.

## Estado

Cola del maker: 1 (0397 r3). Cola del checker: 2 (0408 r1, 0410). Dentro del limite.
`validate` en 0, `open/` en 4, fondo intocable verificado: config sha8 `2E35F26E`, epoch 1.14.0.

Y tus dos decisiones **estan inscritas**. Tardaron porque el intent `decision` exige
`PROJECT_STATE.json` como ruta completa y eso solapa con cualquier fragmento de un peon: una firma
tuya no se puede inscribir mientras el maker trabaje. Es TASK-0411 en su forma mas pura, y hoy se ha
reproducido por quinta vez.
