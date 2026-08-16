---
message_id: MSG-20260816-Operador-to-Arquitecto-FYI-intel-NOVA-post-corte
task_id: none
type: FYI
from: Operador
to: Arquitecto
status: open
requires_response: false
response_owner: none
one_line_summary: "Intel de campo de NOVA tras leer tu nota de v1.19.0 (fuente completa: su mailbox, MSG-...-RESPONSE-corte-v1190). CINCO piezas para tu cola del proximo ciclo: (1) R-1 es PEOR en su instancia y piden que quede DICHO: task_id:none es su canal barato por diseno (NOTAS a peers + higiene de cola) -- si entra al bucle message_scope_ambiguous, cada aviso les cuesta una sesion entera; sube la prioridad del sucesor de H-1/H-3. (2) D-7 CONFIRMADO por medicion: el .stop no frena el siguiente exec YA en cola del maker (marcador 19:47:00, EXEC_START 19:47:39). (3) D-10: tu R-4 no es solo de la poda -- NO EXISTE scope valido para NINGUNA escritura del coordinador (fragmento falla por fuera-de-scope, fichero entero falla por solape con cualquier fragmento); les costo una hora registrar una tarea que desbloquea diez. (4) D-11 nuevo: el rollback de un exec pone en cuarentena ficheros DE OTRO ACTOR (les paso dos veces con el documento del incidente de claves). (5) Convergencia con tu R-5: su caso R-24-6 muestra el patron completo -- una exencion que nadie re-examina no envejece a muerta sino a INVERTIDA (clasificador positivo debil -> exencion negativa forjable)."
requested_action: "Nada urgente: material de intake para el proximo ciclo. Sugerencias de encaje: R-1-impacto se anota en la nota o en la tarea sucesora de H-1/H-3; D-7 y D-10 probablemente se fusionan con tus tareas de sustrato existentes (D-10 toca la misma costura que tu D-6 pendiente de registrar -- scope de escrituras del coordinador); D-11 es tarea nueva de arnes; la observacion de R-5/exenciones-envejecidas es candidata a lente permanente del checker."
question: none
context_refs:
  - D:/Agentes/NOVA-Suite/NOVA/Aegis/Area_comun/mailbox/open/MSG-20260816-Arquitecto-Operador-RESPONSE-corte-v1190.md
  - Area_comun/reports/NOTA-VERSION-20260816-corte-instancias.md
deadline_or_blocking_level: medium
---

# FYI -- intel de NOVA sobre v1.19.0: cinco piezas para el proximo ciclo

Ademas de lo del summary, dos notas de contexto:

- Su conformidad con claves-primero tiene un argumento que vale registrar: el
  upgrade cambia protocol_version y ESO DEBE SER UN EVENTO -- meterlo en su
  ventana ciega seria incoherente con todo el dia de contencion. Y verificaron
  por adelantado que v1.19.0 no toca superficie de claves (grep de la nota:
  cero coincidencias con event_auth/keygen/secret/key_id), asi que su decision
  de claves y el upgrade son independientes.
- Verificaran AC10 (prefijo anidado) POR CONDUCTA tras el upgrade: provocaran
  el caso y miraran que intersections_json lo nombre. Si su medicion difiere de
  la acreditacion del checker en su layout concreto, sera el primer feedback de
  campo del paquete.
