---
message_id: MSG-20260816-Operador-to-Arquitecto-ADENDA-DIRECTIVA-NOVA-intel-ventana
task_id: none
type: DIRECTIVA
from: Operador
to: Arquitecto
status: archived
requires_response: true
response_owner: Arquitecto
one_line_summary: "ADENDA a la DIRECTIVA del paquete NOVA: el Arquitecto de NOVA ya respondio con coste medido y ventana. El corte debe estar publicado ANTES de las 09:30 local de manana (su ventana de upgrade es 10:00-11:00, fallback 12:00). 0337 confirmada en el minimo del corte (paga el 90 por ciento de su dolor: 137 aplazamientos worktree_residue_live solo hoy). Pista de implementacion de campo para 0337 y aviso critico: la instancia NOVA tiene DOS genesis firmadas -- verificar que upgrade_instance lo tolera ANTES del corte."
requested_action: "(1) ETA: publica el corte (release tag + nota de version) antes de las 09:30 local de manana; si no llegas, dilo YA por mailbox para desplazar la ventana de NOVA a las 12:00 (corte a las 11:30 como muy tarde). (2) 0337: incorpora la pista de campo de NOVA -- en instancias con gobierno ANIDADO la exencion de area personal ancla mal: su Get-StagedResidueState excluye personal/<peer>/** con regex ^personal/ pero git status emite Aegis/personal/...; es la misma familia que TASK-0405 (exencion anclada en raiz) y que la derivacion de prefijo de instancia de eb440d6. El maker debe derivar el prefijo de instancia y el checker debe verificar con layout anidado, no solo plano. (3) upgrade_instance: NOVA reporta DOS genesis firmadas en su ledger (seq 1 original c157fe00 intacta + seq 796 aggregate_version 2, actor Codex, por su incidente D-9 de esta madrugada). Si upgrade_instance asume genesis unica, o se tolera o la nota de version documenta el paso manual -- confirmalo ANTES del corte, no durante la ventana. (4) Sigo esperando tu PLAN + ETA de la DIRECTIVA original por mailbox."
question: "Confirmas corte publicado antes de las 09:30 local, y que upgrade_instance tolera la doble genesis (seq 1 + seq 796) de NOVA?"
context_refs:
  - Area_comun/mailbox/open/MSG-20260816-Operador-to-Arquitecto-DIRECTIVA-paquete-actualizacion-NOVA.md
  - D:/Agentes/NOVA-Suite/NOVA/Aegis/Area_comun/mailbox/open/MSG-20260816-Arquitecto-Operador-RESPONSE-VENTANA-ACTUALIZACION.md
  - scripts/upgrade_instance.py
deadline_or_blocking_level: high
---

# ADENDA a la DIRECTIVA -- inteligencia de campo de NOVA y ventana cerrada

Resumen de la respuesta del Arquitecto de NOVA (mensaje completo en su open/, ref arriba):

- Pin adoptado: protocol_version 1.14.0, tier runtime, config sha8 c2de91f9.
- Dolor medido HOY (18h): D-1 (=0337) con 73 aplazamientos en su maker y 64 en su
  checker; su coordinador hace de desatascador manual. D-9 segundo (ledger 1h parado,
  drift de dos filas). D-8 tercero (mitigacion interina ya operando).
- Su peticion textual: si solo entra UNO en el primer corte, que sea 0337.
  CONFIRMADO por el operador: el minimo del corte es pin + 0337 verificada.
- Ventana de upgrade: manana 10:00-11:00 local, 60 min + 30 de holgura; fallback
  12:00 si su review critica de producto (9431) sigue abierta a las 10:00.
- Aviso D-7 (suyo): el marcador de parada de crons no corta el lote en curso;
  pondran el marcador antes del inicio nominal y verificaran por EXEC_EXIT.

Con su ventana, tu deadline concreto queda: **corte publicado 09:30 local**.
Responde ETA por este canal.
