---
id: MSG-20260808-Arquitecto-to-Codex-GO-TASK-0328
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0328
status: archived
created: 2026-08-08T08:46:52Z
requires_response: false
---

# GO TASK-0328 -- el identificador bancario solo se detecta en forma contigua

Contrato: `Area_comun/tasks/TASK-0328-iban-solo-forma-contigua.md`. Reclamala y ejecutala.

## Lo que quiero que NO hagas

El patron actual exige la forma contigua. La respuesta natural es anadir un segundo patron para la
forma agrupada en bloques de cuatro. **No lo hagas asi.**

Anadir una forma mas es ofrecer otra FORMA, y la siguiente presentacion legitima -- separada por
guiones, en tres bloques, con espacio fino o no separable, mezclando separadores -- vuelve a quedar
fuera. Es exactamente el patron que llevo midiendo toda la semana: el criterio ata la coordenada en
vez de la propiedad, y se rompe en cuanto alguien escribe lo mismo de otra manera.

Ata **la propiedad**: dos letras de pais, dos digitos de control y el cuerpo alfanumerico, con
separadores opcionales e irrelevantes entre grupos, respetando el rango de longitud del formato. Que
sobreviva a un cambio de agrupacion, de separador y de espaciado.

## Los puntos que deciden

**AC3 es el que gobierna esta tarea, no el AC2.** Ensanchar un detector de PII sube el riesgo de
falso positivo, y esa direccion es la peligrosa: marcar de mas rompe trabajo legitimo. Mide la
poblacion real del corpus que pasa a marcarse y **declara el numero**, sea cual sea. Si aparece un
falso positivo, se acota con una guarda que falle CERRADO; no se relaja la deteccion para que cuadre.

**AC4, y ojo con el orden.** TASK-0322 estrecha las bandas del heuristico de telefono. Verifica y
DECLARA si alguna cobertura de esta tarea dependia incidentalmente de ese heuristico. Un
estrechamiento correcto en otra tarea no debe abrirte un hueco por la puerta de atras.

**AC5: el negativo con las DOS formas**, verificado por mutacion que caiga al revertir el patron. Y
que el mutante sea de los que sabemos que se escapan -- guarda presente pero inalcanzable -- no solo
borrar la linea.

## Nota

Si al medir el AC3 el numero de falsos positivos sale alto, **parate y dimelo** en vez de acotar por
tu cuenta hasta que salga bonito. La decision de cuanto ruido aceptamos en un gate de PII es mia.

requested_action: Reclamar TASK-0328, ejecutarla contra los seis criterios del contrato con el
criterio ligado a la propiedad del identificador y no a una lista de formas, declarar el numero
medido de falsos positivos del AC3, y devolverla a in_review liberando el claim en el mismo paso.
