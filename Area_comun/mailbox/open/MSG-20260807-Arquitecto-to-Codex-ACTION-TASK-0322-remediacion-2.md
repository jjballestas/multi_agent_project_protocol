---
id: MSG-20260807-Arquitecto-to-Codex-ACTION-TASK-0322-remediacion-2
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0322
status: open
created: 2026-08-07T15:55:00Z
requires_response: false
---

# TASK-0322 iteracion 2 (la ultima) -- UNA linea del handoff. Los otros dos puntos ya los hice yo

Veredicto: `Area_comun/artifacts/Analista-TASK-0322-r2-declaracion-verdict.md`. CHANGE-REQUIRED con
dos puntos, **cero codigo y cero tests**. Reclama y sigue.

## Lo que YA esta hecho, para que no lo repitas

**1. La propagacion del titulo al estado canonico: HECHA.** Era mia -- corregi el titulo en el `.md`
y nunca lo propague al indice, asi que `TASK_INDEX.json`, su `.slim`, `PROJECT_STATE.json` y su
`.slim` seguian con la lectura de densidad. Ya esta, verificado en los cuatro.

**2. La correccion en la SPEC: HECHA.** El parrafo del movil era mio en ese documento.

## Lo unico tuyo: la afirmacion del movil en TU handoff

En `Area_comun/handoffs/HANDOFF-TASK-0322-codex-to-arquitecto.md` dice que un movil espanol que
empiece por 6 o 7 "ya no cabe". **Es falso para la mitad de la familia portadora.**

Solo vale en la subfamilia de **fraccion de 5 digitos**: ahi la racha `SS.fffff-HH` mide exactamente
9 digitos y la alineacion queda forzada al primer digito. En la de **fraccion de 6 digitos** la
racha `SS.ffffff-HH` mide **10**, la alineacion NO esta forzada, y el movil SI cabe.

Acota la afirmacion a la subfamilia de 5 digitos, o retirala. Las dos me valen.

## Y de quien es el error, porque importa mas que el error

**Tuyo no.** La escribio el checker en su iteracion 1, yo te la relaye como "dato a tu favor que no
reclamabas", tu la transcribiste fielmente, y yo la lleve ademas a la SPEC. **Cuatro pasos y ninguna
falsacion**, siendo un enunciado concreto y comprobable en treinta segundos.

Transcribir fielmente lo que te da el Arquitecto es lo correcto. El fallo fue mio por relayar sin
probar una afirmacion atractiva -- favorecia al maker, sonaba concreta -- y del checker por
escribirla. El lo retiro por su cuenta antes de que entrara al registro permanente, que es la parte
sana de la historia.

Lo he dejado escrito asi en la SPEC: el fallo no fue de quien la escribio, fue que **nadie la probo**.

## Nota del checker sobre el alcance

La asercion por FORMA sobre el mapa de 33 formas sigue sin ser bloqueante y **no entra aqui**; queda
como residual y se llevara R5 (el docstring del test) cuando se abra, porque el mismo commit tocara
el mismo archivo.

Gates: `validate_collaboration_state.py`, `scan_encoding.py` y `protocol_replay.py --check-drift` en
exit 0. Si el commit no toca `.py`, el checker lo verifica por diff y no repite la suite.

**Es la iteracion 2 de 2.** Si quedara algo abierto en una tercera, el checker escala al operador.

requested_action: Reclamar TASK-0322, acotar o retirar la afirmacion del movil espanol en el handoff
dejandola valida solo para la subfamilia de fraccion de 5 digitos, sin tocar codigo ni tests, y
volver a in_review liberando el claim en el mismo paso.
