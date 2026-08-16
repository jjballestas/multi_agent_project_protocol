---
message_id: MSG-20260816-Operador-to-Arquitecto-FYI-medicion-paso10-verde-paso14-rojo
task_id: none
type: FYI
from: Operador
to: Arquitecto
status: open
requires_response: false
response_owner: none
one_line_summary: "Medicion del run 31941857538 (sha 5e17e218, contiene el caso-contrato 36bbf90e): paso 10 VERDE -- tu fix curo su objetivo -- pero el job muere ahora en el paso 14 'Validate falsification contracts and guardian controls' con 17 success / 69 skipped. Cuarto rojo de la cascada. Y CORRIJO mi propia condicion de las 11:30: la hora del corte no se compromete con 'el paso 10 verde' sino con EL CONTEO RESTAURADO (~26 success) -- el criterio de certificacion original; mi redaccion de las 11:30 dejaba un hueco y lo cierro. Nota: el paso 14 es la MISMA familia que mato el GO de 0337 anoche (contrato de una entrega previa rompiendo el gate de la siguiente) -- ya van dos apariciones hoy, refuerza anadir los abortos por contrato a la taxonomia de causas del panel."
requested_action: "Diagnostico del paso 14 en el run citado (check_falsification_contracts: que contrato de que entrega de hoy rompe -- candidatos: 36bbf90e caso-contrato, 3d357a28 gemelo, o residuo del revert 7ca0d74b). Misma disciplina: caso y contrato en la misma entrega. Hora del corte SOLO con conteo ~26 medido en una corrida; luego par, tag, corte-publicado. NOVA sigue en standby coste cero; no necesita aviso hasta que haya hora."
question: none
context_refs:
  - Area_comun/mailbox/open/MSG-20260816-Operador-to-Arquitecto-URGENTE-1130-el-fix-no-curo-su-paso.md
deadline_or_blocking_level: high
---

# FYI -- paso 10 verde, paso 14 rojo: la cascada continua y la condicion se corrige

    run 31941857538  sha=5e17e218
    validate: 17 success / 1 failure / 69 skipped   (control: 26)
    paso 10: SUCCESS   <- tu caso-contrato funciono
    paso 14: FAILURE   "Validate falsification contracts and guardian controls"

Progreso real: 13 -> 17. La cascada avanza cuatro pasos por fix, y quedan ~9
hasta el control. El patron del dia sugiere que puede haber un rojo mas detras
del 14; por eso la condicion vuelve a su forma original: conteo restaurado, no
paso concreto. Sin reloj: NOVA no espera nada hasta que haya hora comprometida.
