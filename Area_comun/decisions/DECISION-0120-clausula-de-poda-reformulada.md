---
decision_id: DECISION-0120
title: "La clausula de poda se REFORMULA, no se deroga: la ventana no se espera, se abre dejando de rutear -- y remediacion del borrado sin decision del 16-ago"
status: accepted
date: 2026-08-18
author: Arquitecto
approved_by: "operador humano (FIRMADA 2026-08-18, en persona)"
relates_to: [DECISION-0014, DECISION-0273-TASK, DECISION-0096, DECISION-0118]
supersedes_wording_of: "Area_comun/protocol/TASK_PROTOCOL.md, seccion Coordinated Pruning Checkpoint, paso 2"
---

# DRAFT-DECISION-0120 -- la ventana de poda no se espera: se abre

> Borrador del Arquitecto a peticion del Operador (18-ago-2026, GO A2). **El Arquitecto no firma.**
> Cambio normativo: requiere decision registrada (AGENTS.md s.7) y firma del operador humano.

## 1. El incumplimiento que se remedia, y es mio

El commit **`3062214d`** (entrega de **TASK-0273**, `done`, ratificada) escribio la doctrina de poda
**en `Area_comun/protocol/TASK_PROTOCOL.md` y en el master de la skill, en el MISMO commit**.

El **16-ago**, el commit `cef48839` **borro esa clausula de la skill viva** y la sustituyo por la
secuencia de cuatro pasos. **Sin DECISION previa**, que CLAUDE.md regla 2 exige para cambios de
protocolo. Medido hoy:

    "Poda coordinada en el checkpoint"   MASTER=1   TASK_PROTOCOL=1   VIVO=0

**El outlier es el vivo.** Lo hice yo, y esta decision existe primero para regularizarlo y solo
despues para mejorar el texto. **Aunque la sustitucion sea mejor, el procedimiento fue incorrecto**:
una clausula ratificada no se deroga en una copia local.

## 2. Una sola propuesta: REFORMULAR el paso 2, no derogar la clausula

Descarto derogar, y doy las razones medidas:

1. **Las precondiciones del paso 1 son CORRECTAS y no son lo que fallo.** Arbol gobernado limpio y
   cero claims de peer siguen siendo exactamente lo que la poda necesita: su claim reclama
   `CLAIMS.json` entero y choca con cualquier claim activo. Derogar tiraria una regla acertada.
2. **Lo que fallo es el paso 2 como consejo TERMINAL.** *"If either precondition fails, defer
   pruning"* dice que esperes, y **no dice a que**. Con dos peones activos la ventana **no llega
   sola**: un peon solo arranca exec si hay mensaje que procesar, asi que la ventana **la abre el
   coordinador dejando de rutear**. El texto vigente omite el mecanismo -- no lo contradice -- y por
   eso el delta normativo es **pequeno**.
3. **Falta el orden que mas mueve la aguja.** Medido dos veces:

       open/ 61 mensajes  ->  cold_start_tokens 74130
       open/  5 mensajes  ->  cold_start_tokens 20277        (umbral 20000)
       2026-08-18, misma noche:      28029 -> 20962 solo con higiene

   **El mailbox era el 73 %.** Y la confirmacion inversa, el mismo dia: rutear tres reviews subio el
   gate de 20277 a **22201**. **Rutear engorda el mismo gate que la higiene adelgaza**, asi que el
   orden no es preferencia: es lo unico que converge.
4. **Y una correccion que debe quedar escrita porque estuvo medio dia en commits:** *correr la poda
   NO es hacer higiene de mailbox*. `prune_state.py` **si** poda mailbox, pero **recoge de
   `answered/`, no de `open/`**: la clasificacion de "consumido" es del ORQUESTADOR y no la hace
   ninguna herramienta.

### Texto propuesto para el paso 2 (delta minimo)

> 2. If either precondition fails, **do not wait for the window: open it.** The coordinator stops
>    routing new work; peers only start an exec when there is a message to process, so the idle
>    checkpoint arrives by itself once the queue drains. **Mailbox hygiene comes first and is the
>    largest lever** -- classifying consumed messages and archiving them is the orchestrator's job
>    and no tool does it; `prune_state.py` harvests `answered/`, never `open/`. An explicit peer
>    barrier remains exceptional. The full sequence is: **hygiene -> stop routing -> prune -> resume
>    routing.**

Los pasos 1, 3, 4 y 5 **no se tocan**. La frase de cierre (*"does not relax claim-as-lock"*) tampoco.

## 3. Marcador de revision FECHADO dentro del documento

Con la epoch **pineada en 1.14.0** y la re-genesis prohibida, **los cambios de metodologia son
invisibles al eje de version**: un adoptante no puede distinguir por ningun numero si su
`TASK_PROTOCOL.md` es pre o post esta reformulacion. Se anade, en la cabecera de la seccion:

    > Revision: 2026-08-18 (DECISION-0120). Antes de esta fecha el paso 2 decia "defer" sin
    > nombrar el mecanismo de apertura de la ventana.

Es la unica senal que viaja con el documento y que `upgrade_instance.py` reporta como delta.

## 4. El problema n-ario: cuatro superficies, y hay que nombrarlas

La misma norma vive hoy en **cuatro** sitios, y ninguna puerta comprueba que digan lo mismo:

    1. skill VIVA        .claude/skills/mailbox-hygiene/SKILL.md          <- hoy el outlier
    2. master exportable scripts/instance_assets/claude-skills/...        <- conserva el texto viejo
    3. doc NORMATIVO     Area_comun/protocol/TASK_PROTOCOL.md             <- conserva el texto viejo
    4. copia DESPLEGADA  <instancia>/.claude/skills/...                   <- un tercer estado

Esta decision **alinea 1 y 3** (el vivo recupera coherencia; el normativo recibe el delta minimo).
**No alinea 2 ni 4**, y lo declara expresamente:

- **La superficie 2** se alinea cuando exista el generador de masters (enmienda E1 de la revision
  del camino de subida, **pendiente de firma**). Hasta entonces, alinear el master a mano es
  trabajo manual y **queda fuera de esta decision** para no crear una obligacion sin detector.
- **La superficie 4** depende de **TASK-0417**: el informe de actualizacion compara la ruta de
  staging y nunca la consumida, asi que hoy **nadie puede verificar** que la copia desplegada
  coincida.

**Dependencia declarada, no resuelta.** Nombrarla es el punto: mientras 2 y 4 no tengan puerta, esta
norma viaja a medias y conviene saberlo.

## 5. Lo que esta decision NO hace

- **No crea obligacion sin detector.** No exige alinear las cuatro superficies, porque tres de
  ellas no tienen hoy control que lo compruebe. Este repo ya midio tres veces que la regla textual
  sin detector se incumple (0098->0104, 0036->0038, 0026->0110).
- **No toca `protocol.config.json`** ni la epoch. Sin re-genesis.
- **No re-audita** lo ya promovido.

## 6. Verificacion de que se aplico

    grep -c "hygiene -> stop routing -> prune"  Area_comun/protocol/TASK_PROTOCOL.md   -> 1
    grep -c "Revision: 2026-08-18"              Area_comun/protocol/TASK_PROTOCOL.md   -> 1
    la seccion "Poda coordinada en el checkpoint" vuelve a existir en la skill viva, con el
    mecanismo de apertura incorporado

-- Arquitecto, 2026-08-18 07:40 local (UTC+2). Pendiente de firma del operador humano.
