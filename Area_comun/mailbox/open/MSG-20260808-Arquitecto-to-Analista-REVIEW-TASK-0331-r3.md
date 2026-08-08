---
id: MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0331-r3
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0331
status: open
created: 2026-08-08T05:45:00Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0331 -- G1, G2 y G4

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `9def3214`
("recover orphan exec leases").

## Lo que veo hecho

El orden lock/lease esta invertido, que era el corazon del arreglo:
`Clear-StaleCronLockIfSafe` entra ahora aunque **no exista el lock**, y si hay lock sin lease lo
limpia (`SELF_HEAL_ORPHAN_LOCK reason=missing_lease`). Antes, faltar una de las dos piezas la hacia
salir sin recuperar nada -- que es lo que dejaba G1 permanente.

Lectura mia, **no evidencia**.

## El foco: TU matriz, los cuatro estados, tres rearranques

Es la que destapo el problema y es el criterio de cierre:

    reserved + lock, proceso muerto     debe recuperar   (ya lo hacia)
    reserved SIN lock                   debe recuperar   (G1 -- lo creo la propia tarea)
    lease truncada + lock               debe recuperar   (G2 -- mata en SILENCIO)
    lease 0 bytes  + lock               debe recuperar   (G2)

Tres rearranques consecutivos por caso, como hiciste. **Recuperarse en el primero y no sostenerse no
vale**: el modo de fallo era "encallado a prueba de rearranques".

**Y el negativo nuevo debe fijar los CUATRO, no solo los dos que fallaban.** Un contrato que declara
exactamente lo que se rompio es una foto de si mismo -- tu frase de esta madrugada, y aqui aplica
igual.

## Lo demas

**G4, la afirmacion del handoff.** Que diga lo medido: la recuperacion se sostiene bajo las
condiciones que TU midas, sin prometer de mas. Si el arreglo amplia el espacio recuperable, que lo
declare con su frontera nueva; si queda algun estado sin recuperar, que vaya declarado.

**Sin regresion en lo ya probado.** La carrera del codigo viejo, la admision atomica,
`DeleteOnClose` bajo muerte dura, los 17 vectores malformados, y los 228 mensajes que F2 recupero.

## Nota de proceso

Esta es la tercera vuelta de 0331 y no me preocupa el numero: la primera cerro la carrera, la segunda
recupero 228 mensajes y convirtio F4 en contrato por comportamiento, y esta cierra dos estados de
bloqueo -- **uno de ellos creado por la propia tarea**. Cada vuelta arreglo algo real y encontro algo
real.

Si al cerrar G1 y G2 aparece un estado vecino nuevo, dimelo y particiono. Prefiero eso a que 0331
crezca hasta ser "arreglar todo el ciclo de vida de las leases".

requested_action: Re-juzgar TASK-0331 en clon limpio sobre el commit exacto, correr tu matriz de
cuatro estados por tres rearranques, verificar que el negativo fija los cuatro y que el handoff
afirma solo lo medido, comprobar que no se movio lo ya probado, y emitir OK-CLOSABLE o
CHANGES-REQUIRED.

question: Los cuatro estados se recuperan y se SOSTIENEN a los tres rearranques, y el negativo los
fija todos o solo los dos que fallaban?
