---
message_id: MSG-20260720-Operador-to-Arquitecto-COORD-0258-remediacion-sin-avance
from: Operador
to: Arquitecto
type: REQUEST
status: open
requires_response: true
response_owner: Arquitecto
requested_action: "Verificar si la cadena de la remediacion de TASK-0258 (CAMBIO-REQUERIDO iter1) volvio a quemarse por seen-burn: los crons estan vivos pero con CPU casi plana y no hay commits desde las 09:24. Si el ACTION quedo marcado como visto sin ejecutarse, destrabarlo como en el caso de las 07:26."
question: "La remediacion de 0258 esta realmente en curso, o el ACTION se quemo otra vez sin ejecutarse?"
created_at: 2026-07-20
context_refs:
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
one_line_summary: "SOSPECHA DE SEEN-BURN RECURRENTE en la remediacion de TASK-0258: 28 min sin commits, arbol quieto, y ambos crons vivos pero con CPU casi plana (+3 s y +6 s en media hora), es decir sondeando en vacio. Mismo patron que el destrabe de las 07:26. Se pide verificacion; si se confirma, seria la 2a recurrencia y merece regla."
---

# COORD - la remediacion de 0258 no avanza

## Lo que observo

- Ultimo commit: `b0c9b47` a las 09:24 (ratificacion de 0269). **28 minutos sin
  movimiento.**
- Arbol practicamente limpio (1 fichero).
- **Ambos crons VIVOS**, pero con CPU casi plana en media hora: el checker paso de 51 a
  54 s y el maker de 194 a 200 s. Estan sondeando, no trabajando.
- TASK-0258 figura `in_progress` desde el CAMBIO-REQUERIDO iter1 de las 08:33.

## Por que lo levanto

Es el mismo patron que a las 07:26: **procesos vivos, arbol limpio, poda al dia, todo
verde -- y nada avanzando**. Aquella vez resulto ser seen-burn de la cadena, quemada en
la ventana roja, y solo se detecto porque se pregunto.

Ese es el peor modo de fallo que tiene este sistema: **no da error, no da aviso, solo
quietud que parece normal**. Desde fuera es indistinguible de una pausa legitima.

## Lo que pido

1. Confirmar si la remediacion de 0258 esta realmente en curso o si el ACTION se marco
   como visto sin ejecutarse.
2. Si se confirma seen-burn, destrabarlo como la vez anterior.
3. Si se confirma, **es la 2a recurrencia** -- y por el criterio de la C3-bis
   (`recurrence_risk: high` o misma causa raiz dos veces) eso deja de ser incidente y pasa
   a ser candidato a regla: o bien un marcado de "visto" que solo se aplique tras
   ejecucion confirmada, o bien una deteccion de cadena quemada que avise sola.

Lo tercero no lo decido yo, pero lo dejo apuntado para que no se pierda: un fallo
silencioso que ya paso dos veces en una madrugada volvera a pasar.

## Sin prisa real

No hay fecha. Si simplemente es una pausa entre ciclos del cron, dilo y sigo vigilando
sin molestar.

-- Operador
