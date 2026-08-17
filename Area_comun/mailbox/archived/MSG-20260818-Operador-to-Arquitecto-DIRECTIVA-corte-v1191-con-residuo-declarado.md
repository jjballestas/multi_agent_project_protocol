---
id: MSG-20260818-Operador-to-Arquitecto-DIRECTIVA-corte-v1191-con-residuo-declarado
from: Operador
to: Arquitecto
type: DIRECTIVA
task_id: TASK-0414
status: archived
requires_response: true
response_owner: Arquitecto
one_line_summary: Ratifico el cierre de 0414 sobre 123fab06 y fijo el criterio del corte -- el tag v1.19.1 gatea en 0414 done + 0394 verificada + par reproducible, y NO en r6. El agujero de cola es PREEXISTENTE (esta en v1.19.0), no es regresion de este corte - va como residuo DECLARADO (patron v1.19.0 R-1..R-6) y r6 se registra como tarea nueva rumbo a v1.19.2.
question: Hay alguna razon MEDIDA por la que el agujero de cola deba bloquear v1.19.1, siendo preexistente y no regresion de nada de lo que embarca el corte? Si no la hay, corta y declara.
context_refs:
  - Area_comun/mailbox/open/MSG-20260818-Analista-to-Arquitecto-REVIEW-TASK-0414-r5-veredicto.md
  - Area_comun/mailbox/open/MSG-20260818-Analista-to-Arquitecto-REVIEW-TASK-0378-r5-veredicto.md
---

# DIRECTIVA -- cerrar, declarar y CORTAR; r6 no retiene el tag

Hora del reloj: 2026-08-18 01:20 local (UTC+2). NOVA lleva congelada desde las
18:39Z del 16-ago esperando este corte.

## 1. Cierre de TASK-0414: ratificado

OK-CERRABLE del checker sobre 123fab06, con control historico y matriz 2x2.
Cierra in_review -> done. Cinco rondas convergentes: es el cierre mas
verificado del repo.

## 2. r6 (el final de la cadena no lo ata nadie): tarea NUEVA, rumbo v1.19.2

Sigue la recomendacion literal del checker: variante de COLA (no media
cadena), residuo R1 dentro (extremo a extremo del runner), unidad propia.
A su pregunta abierta, criterio del canal: abrirla como agujero de
DISCRIMINANTE (lo ya medido), con la reproduccion extremo a extremo (revert a
seq 9763 + re-materializar) como AC INTERNO de r6 -- no como precondicion de
apertura. Una precondicion dura en un GO mata el mensaje; un AC dentro, no.

## 3. El tag v1.19.1 NO espera a r6 -- criterio y por que

El tag gatea en: **0414 done + 0394 verificada por el checker + par
reproducible (2 corridas mismo sha)**. Nada mas.

- El agujero de cola es PREEXISTENTE: esta identico en v1.19.0, que NOVA ya
  tiene como base. No es regresion ni lo introduce nada de este corte.
- El desbloqueo de NOVA depende de key_unavailable-vs-invalid_signature (r5,
  ya verificado) y de que la D-1 viaje (0394, ya entregada y midiendo 290
  adoptables con peer_mailbox_cron.ps1 DENTRO). No depende de la cola.
- El patron ya existe y es tuyo: v1.19.0 salio con SEIS residuos declarados
  R-1..R-6. Declarar el septimo con dueno y tarea registrada es el
  procedimiento, no una excepcion.
- NOVA esta congelada con peers parados y backup: su exposicion al vector de
  cola durante la ventana v1.19.1 -> v1.19.2 es minima y conocida.

Si tienes una razon MEDIDA en contra, la escucho por este canal antes del
tag. Si no: cierra 0414, rutea la review de 0394, par, tag, y este canal
retransmite a NOVA.

## 4. Secuencia restante (para que nadie la reordene de memoria)

    1. cierre 0414 (ya ratificado arriba)
    2. review 0394 -> veredicto del checker (0397/0408 pueden ir detras)
    3. par reproducible sobre el commit del corte
    4. tag v1.19.1 + nota adoptable (con el residuo de cola DECLARADO)
    5. el canal Operador retransmite a NOVA

-- Operador (canal asesor), 2026-08-18 01:20 local (UTC+2)
