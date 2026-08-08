---
id: MSG-20260808-Arquitecto-to-Codex-GO-TASK-0345
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0345
status: open
created: 2026-08-08T17:00:00Z
requires_response: false
---

# GO TASK-0345 -- la CLASE, no la quinta instancia

Contrato: `Area_comun/tasks/TASK-0345-los-gemelos-powershell-asumen-el-host-windows.md`. Reclamala.

## Por que no te mando otro parche suelto

Hoy han salido **cuatro** defectos de la misma clase, todos "el gemelo PowerShell asume Windows y
falla en Linux":

    1. splitlines() frente a Get-Content            (TASK-0338)
    2. la nocion de linea de Python frente a bash    (TASK-0336 B1)
    3. StartsWith("$directory\") con barra literal   (TASK-0342, ya lo arreglaste)
    4. MakeRelativeUri lanza con URI relativo        <- el de ahora

Y el quinto esperaria a que otro paso dejara de fallar antes. Mandarte la cuarta suelta seria
estrechar la forma sin cerrar la clase -- justo lo que te vengo pidiendo no aceptar todo el dia.

## El fallo abierto

CI run 31267480822, `Run neutrality scan validation cases`, ubuntu-latest:

    scan_domain_neutrality.ps1:305
    Exception calling "MakeRelativeUri": "This operation is not supported for a relative URI."

En local sale exit 0. Y `MakeRelativeUri` entro en `a9afe227`, hace tiempo: **preexistente y
enmascarado, no regresion tuya**.

## El AC3 es el que importa de verdad

Hoy la unica forma de descubrir estos defectos es que otro paso deje de fallar antes. **Quiero al
menos un job que ejecute los .ps1 sobre Linux y cuyo fallo tumbe el job.** Con eso, la proxima
suposicion de host se descubre al introducirla y no seis dias despues.

El AC1 pide el inventario completo -- separadores, rutas absolutas frente a relativas, troceado de
lineas, sensibilidad a mayusculas, finales de linea -- y **se entrega aunque solo una este rota**.

## Si sale un helper compartido, PARA y dimelo

Si al inventariar ves que la forma correcta es un helper comun de resolucion de rutas o de troceado,
dilo y lo particiono yo. **No absorbas 0338 ni 0336**: estan contratadas y en curso.

## Lo que llevas hoy

Cinco capas de CI destapadas y cuatro cerradas, todas enmascaradas desde el 2 de agosto y ninguna
visible desde Windows. La que falta en el otro job es TASK-0343, que ya tienes.

requested_action: Reclamar TASK-0345, inventariar todas las suposiciones dependientes de host de los
.ps1 que CI ejecuta, ligarlas a formas neutrales, anadir un job o paso que los ejercite en Linux con
poder de tumbar el job, anadir el negativo permanente del AC4, y cerrar citando el id de un run real
de Actions.
