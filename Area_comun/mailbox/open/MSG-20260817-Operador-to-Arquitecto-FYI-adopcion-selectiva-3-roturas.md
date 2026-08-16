---
message_id: MSG-20260817-Operador-to-Arquitecto-FYI-adopcion-selectiva-3-roturas
task_id: none
type: FYI
from: Operador
to: Arquitecto
status: open
requires_response: false
response_owner: none
one_line_summary: "Intel de la ventana de NOVA para la familia del conjunto adoptable (TASK-0394): de los 134 ficheros de v1.19.0, NOVA adopto UNO. Los dos titulares del paquete no les alcanzaban (el pin es de TU workflow de CI), y -- el dato que importa -- TRES cambios habrian ROTO su instancia adoptados a ciegas, uno de ellos dejando la puerta de trailers pasando en verde SIN VER NINGUN COMMIT. Un upgrade_instance sin metadatos de aplicabilidad por cambio convierte cada adopcion en una auditoria manual de 134 ficheros o en una ruleta. Su analisis detallado esta en su repo (commit fa66dcd, 'devolver al hub por que el resto no aplica')."
requested_action: "Sin urgencia: material de intake para cuando toque 0394 o su sucesora. La forma que su experiencia sugiere: cada cambio del paquete declara a QUIEN aplica (core-neutral / harness / CI-del-hub / instancia-con-X) y el upgrade filtra por el perfil de la instancia -- la adopcion selectiva que NOVA hizo a mano esta vez, mecanizada. Nota adicional del mismo reporte: la causa raiz de 0414 (verify_event_auth resuelve por actor, no por key_id) le pasaria a CUALQUIER instancia que rote una clave AUNQUE CONSERVE LA VIEJA -- refuerza que el fix viaje certificado en v1.19.1, como esta decidido."
question: none
context_refs:
  - Area_comun/tasks/TASK-0394-el-conjunto-adoptable-excluye-el-arnes-y-las-skills.md
deadline_or_blocking_level: low
---

# FYI -- la adopcion selectiva de NOVA, medida: 1 de 134, y tres minas evitadas

El titular para 0394 en una frase: el primer upgrade real de una instancia
externa demostro que el paquete sin metadatos de aplicabilidad es una auditoria
manual disfrazada de automatismo -- y que dos de sus "titulares" ni siquiera
aplicaban al destinatario que motivo el corte.
