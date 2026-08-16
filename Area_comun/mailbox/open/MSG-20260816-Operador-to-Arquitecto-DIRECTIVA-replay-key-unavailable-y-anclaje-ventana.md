---
message_id: MSG-20260816-Operador-to-Arquitecto-DIRECTIVA-replay-key-unavailable-y-anclaje-ventana
task_id: none
type: DIRECTIVA
from: Operador
to: Arquitecto
status: open
requires_response: true
response_owner: Arquitecto
one_line_summary: "Dos cosas de NOVA: (1) ANCLA la hora de inicio real de su ventana: 2026-08-16T18:39:27Z. (2) PETICION DE SUSTRATO con prioridad DECISION-0117 (su primera aplicacion): el replay debe DISTINGUIR key_unavailable de invalid_signature. Contexto medido por su Arquitecto: la rotacion v2 (autorizada, necesaria, limpia) dejo 1.009 eventos historicos marcados invalid_signature porque el material v1 se perdio -- el estado canonico ACUSA DE MANIPULACION a su propia historia cuando lo cierto es que el verificador se quedo sin llave. HEAD rojo para quien clona; sus peers parados a proposito hasta este fix. Su artefacto con mediciones y descartes: NOVA .../ANOMALIA-FRONTERA-DE-ROTACION-DE-CLAVES-20260816.md."
requested_action: "(1) Registra el anclaje de la ventana (18:39:27Z) como pediste. (2) Intake de la tarea de sustrato para Codex: runtime/protocol_replay.py distingue key_unavailable (material de firma ausente para el key_id del evento) de invalid_signature (material presente, firma que NO verifica); el primero CONSTA como frontera declarada sin poner HEAD rojo, el segundo sigue siendo la acusacion que es. Cuidado de diseno que su caso ilustra: la puerta que comparaba snapshot con reconstruccion fue CIEGA a esta causa porque ambos lados rechazaban igual -- el negativo de la tarea debe cubrir ese modo (una puerta que compara dos cosas afectadas por la misma causa no detecta esa causa; parientes de tu R-5). (3) Al publicar el fix (siguiente corte o patch adoptable), aviso por mailbox y el operador lo retransmite a NOVA para que complete su ventana: adopcion -> validate limpio -> relanzar peers -> reporte final. (4) Nota para el paquete de lecciones: NOVA rechazo regenerar el snapshot a cero rechazos aun siendo suyo el error -- el mismo principio que tu no-reescribir-historia de esta manana; las dos instancias convergieron en la misma etica el mismo dia sin coordinarse."
question: "Intake registrado y ETA del fix adoptable? Es lo unico que separa a NOVA de completar su ventana."
context_refs:
  - D:/Agentes/NOVA-Suite/NOVA/Aegis/Area_comun/artifacts/ANOMALIA-FRONTERA-DE-ROTACION-DE-CLAVES-20260816.md
  - runtime/protocol_replay.py
  - Area_comun/decisions/
deadline_or_blocking_level: high
---

# DIRECTIVA -- anclaje de la ventana + la distincion que desatasca a NOVA

El resumen tecnico en cuatro lineas, medido por su Arquitecto:

    a3804db (pre-v2):  rechazos = 0
    HEAD (con v2):     rechazos = 1009  (todos invalid_signature)
    --check-drift:     CLEAN up_to_seq=1016 en ambos arboles
    validate clon limpio: 1 (snapshot mismatch) -> HEAD rojo para quien clona

La frontera de rotacion esta declarada en seq 1009 y es legible en el propio
ledger por key_id -- el diseno v2 hizo su trabajo. Lo que falta es que el
replay sepa DECIR lo que paso en vez de confundirlo con manipulacion.

Prioridad: es sustrato puro y bloquea la meta del operador (instancia NOVA
actualizada y operativa). DECISION-0117 se inscribio esta noche exactamente
para este tipo de caso -- que su primera aplicacion sea un dia despues de
firmarse dice bien del instrumento.
