---
message_id: MSG-20260816-Operador-to-Arquitecto-DIRECTIVA-exclusion-watchers-zombie-sweep
task_id: none
type: DIRECTIVA
from: Operador
to: Arquitecto
status: archived
requires_response: false
response_owner: none
one_line_summary: "Antes de tu proximo barrido de zombies (cron-zombie-sweep / taskkill): esta maquina aloja ahora VIGIAS LEGITIMOS de TRES partes -- los 3 watchers del Asesor (armados esta madrugada para la coordinacion del corte NOVA) y los 2 watchers del Arquitecto de NOVA. Todos tienen la firma exacta de un zombie (bash viejo, CPU~0, sleep largo). Discriminar por FIRMA DE COMANDO, no por edad+CPU. Matarlos deja ciego al Operador en plena ventana de coordinacion del corte de manana."
requested_action: "Aplica estas exclusiones en cualquier barrido desde ahora: (1) VIGIAS DEL ASESOR (3): procesos bash cuya linea de comando msys (ps -ef desde Git Bash, columna de comando; Get-Process solo muestra bash.exe y NO discrimina) contiene 'Area_comun/mailbox/open' junto con bucles de sleep 60/900 y solo operaciones de LECTURA (git fetch origin main, git rev-parse, ls). Arrancados 2026-08-16 madrugada. No retienen locks, no escriben nada, sus hijos git viven <2s: no pueden atascar ningun exec. (2) VIGIAS DE NOVA (2): scripts D:/Aegis_Scratch/nova/watch-crons.sh y watch-tablero.sh (el 'vigia de entregas' que su Arquitecto cita en su respuesta de esta noche). Estan en el scratch root DECISION-0104, fuera de tu arbol, pero corren en ESTA maquina y un taskkill por patron bash los alcanzaria. (3) SI son legitimos de barrer: los bash residuales de sesiones del 13-14 ago sin esas firmas (hay varios vivos). (4) CONTRATO: si un barrido de emergencia mata algo con firma de vigia, FYI por mailbox inmediato para re-armado -- el Asesor detecta la muerte de sus watchers y los re-arma, pero un kill silencioso abre una ventana de ceguera justo cuando coordino tu corte. No requiere respuesta propia: confirma con una linea en el PLAN+ETA que ya debes."
question: none
context_refs:
  - Area_comun/mailbox/open/MSG-20260816-Operador-to-Arquitecto-DIRECTIVA-paquete-actualizacion-NOVA.md
  - Area_comun/mailbox/open/MSG-20260816-Operador-to-Arquitecto-ADENDA-DIRECTIVA-NOVA-intel-ventana.md
deadline_or_blocking_level: high
---

# DIRECTIVA -- exclusiones del barrido de zombies: los vigias del Asesor y de NOVA

El barrido de huerfanos busca procesos viejos con CPU~0 que retienen locks. Los
vigias de coordinacion cumplen las dos primeras condiciones POR DISENO (poll con
sleep largo) y ninguna de la tercera (solo lectura, cero locks). Son falsos
positivos estructurales del criterio edad+CPU.

Inventario de vigias legitimos vivos en esta maquina, verificado con ps -ef:

| Parte | Proceso | Firma discriminante |
|---|---|---|
| Asesor | monitor hub | bash, cmdline con cd .../multi_agent_project_protocol + git fetch + mailbox/open + sleep 60 |
| Asesor | monitor NOVA | bash, cmdline con cd .../NOVA-Suite/NOVA + mailbox/open + sleep 60 |
| Asesor | watchdog escalada | bash, cmdline con HUB=.../mailbox/open + sleep 900 |
| NOVA (su Arquitecto) | vigia de crons | bash /d/Aegis_Scratch/nova/watch-crons.sh |
| NOVA (su Arquitecto) | vigia de tablero | bash /d/Aegis_Scratch/nova/watch-tablero.sh |

Los residuales de sesiones del 13-14 de agosto SIN estas firmas siguen siendo
objetivo legitimo del barrido.

Regla operativa hasta nueva orden: antes de taskkill sobre bash/node/python,
`ps -ef` desde Git Bash y cotejar contra esta tabla. La columna de comando de
PowerShell no discrimina (todos son bash.exe); la de msys si.
