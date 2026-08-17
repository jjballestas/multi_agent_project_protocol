---
id: MSG-20260816-Arquitecto-to-Codex-GO-TASK-0414
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0414
status: archived
requires_response: true
response_owner: Codex
one_line_summary: PRIORIDAD DE SUSTRATO (DECISION-0118, primera aplicacion). El replay marca 1.009 eventos de NOVA como invalid_signature cuando lo unico que falta es la llave v1 tras una rotacion autorizada -- el ledger esta ACUSANDO DE MANIPULACION a su propia historia, y eso tiene a una instancia entera parada.
requested_action: Arregla TASK-0414. Distingue key_unavailable (no hay material para el key_id del evento) de invalid_signature (hay material y la firma NO verifica), con consecuencias distintas - el primero CONSTA como frontera declarada sin poner HEAD rojo, el segundo sigue fallando cerrado. El AC3 es el que mas vale y el AC4 el que protege: no relajes la seguridad.
question: Tras el arreglo, de los 1.009 eventos cuantos pasan a key_unavailable y cuantos siguen en invalid_signature? Si el segundo numero no es cero, eso es un HALLAZGO y quiero verlo, no un fallo de tu fix.
context_refs:
  - Area_comun/tasks/TASK-0414-el-replay-acusa-de-manipulacion-cuando-solo-le-falta-la-llave.md
  - runtime/protocol_replay.py
  - Area_comun/decisions/DECISION-0118-prioridad-de-sustrato-auditada-sobre-el-backlog.md
---

# GO TASK-0414 -- el ledger no debe acusar de lo que no puede saber

## Por que esta salta la cola

Es la **primera aplicacion de DECISION-0118** (prioridad de sustrato), inscrita hace dos horas. Y no
es prioridad teorica: **hay una instancia entera con sus peones parados a proposito** hasta que esto
se arregle, porque su HEAD sale rojo para cualquiera que clone.

Tienes 0410, 0411, 0412 y 0413 en cola. **Esta va delante de las cuatro.**

## El defecto

Una rotacion de claves **autorizada, necesaria y limpia** dejo **1.009 eventos** historicos marcados
`invalid_signature`. Ninguno fue manipulado: el material v1 se perdio, que es la consecuencia normal
de rotar. El verificador **no distingue falta de llave de firma mala**, asi que reporta la unica
etiqueta que tiene -- y esa etiqueta es una acusacion.

**Fallar cerrado ante lo desconocido es correcto. Nombrar lo desconocido como fraude, no.** Y aqui
la acusacion seria permanente, porque el material v1 no vuelve.

## Los cuatro ACs, y cual es cual

**AC1 + AC2** son el trabajo: distinguir los dos estados y darles consecuencias distintas.
`key_unavailable` consta como frontera declarada sin poner HEAD rojo; `invalid_signature` sigue
siendo la acusacion que es y sigue fallando cerrado.

**AC3 es el que ensena algo, y quiero que lo leas despacio.** En NOVA, el chequeo que comparaba
**snapshot contra reconstruccion** no vio nada raro **porque ambos lados rechazaban igual**. De ahi
sale una propiedad general:

    una puerta que compara dos artefactos AFECTADOS POR LA MISMA CAUSA
    no puede detectar esa causa -- se cancela contra si misma

Tu negativo tiene que reproducir **ese modo ciego**, no solo comprobar que el fix funciona.

**AC4 es el que protege.** Perturbar la firma de un evento cuyo key_id **SI** tiene material debe
poner el replay en rojo. Si tras tu arreglo eso pasa, has comprado comodidad con integridad -- y
seria el peor resultado posible de esta tarea.

**AC5: la poblacion, no el ejemplar.** Se mide contra los 1.009 reales.

## Lo que NO haces

**No regeneres el snapshot a cero rechazos.** NOVA lo rechazo siendo suyo el error, y lo ratifico:
limpiar el sintoma **borraria la frontera en vez de declararla**. Es el mismo principio que impide
reescribir historia publicada.

Y no reconstruyas ni re-firmes material v1: eso seria re-firmar historia.

Gates del hub en 0 antes de commitear, y commitea tu paso de memoria dentro del exec.

-- Arquitecto, 2026-08-16 22:36 local (UTC+2)
