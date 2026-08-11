---
id: TASK-0360
title: El guarda puede excluir sin pasar por la politica, y el contrato observa el conjunto en vez de la decision
status: proposed
owner: Codex
file: Area_comun/tasks/TASK-0360-el-guarda-puede-excluir-sin-pasar-por-la-politica.md
type: fix
intake:
  type: fix
  goal: "Que ninguna ruta pueda quedar fuera del escaneo sin que la decision sea visible para el contrato, y que el negativo deje de morir por texto incidental de produccion. Hoy una linea cableada dentro de `Should-Scan` excluye ficheros sin tocar `$ScanPolicy`: el volcado sale intacto, el contrato no ve nada, y `runtime/state` -- el ledger atestado -- puede caer del canal de PowerShell en silencio."
  acceptance:
    - "AC1 (falsacion previa): se reproduce que una exclusion cableada dentro del guarda deja el negativo en exit 0 con divergencia VIVA, y se acredita con el conjunto ONLY_PY resultante. Medido, no argumentado."
    - "AC2 (se observa la DECISION, no el conjunto): tras el cambio, lo que el contrato compara es la decision por fichero de los dos escaneres, no el conjunto excluido sobre un universo elegido de antemano. Cualquier ruta sobre la que los dos difieran mata al negativo, venga la diferencia de la politica o del guarda."
    - "AC3 (la poblacion se DERIVA de la condicion): los vectores de prueba no son una lista de rutas escrita a mano. Se derivan del dominio que el guarda lee, e incluyen al menos una coordenada FUERA del universo que hoy se muestrea -- el escape de E1 vivia precisamente ahi. Se declara la regla de derivacion."
    - "AC4 (el contrato no depende de texto incidental): reescribir un comentario, reordenar dos flags equivalentes (`-File -Force` <-> `-Force -File`) o renombrar una variable local NO puede poner el gate rojo. Se acredita con esos tres cambios exactos, divergencia CERO medida, gate en exit 0."
    - "AC5 (el negativo sigue matando lo que ya mataba): los siete vectores que TASK-0342 dejo verdes (G9a-d rojos, G6six/ord/ws verdes) siguen dando el mismo resultado. Sin regresion de cobertura."
    - "AC6 (sin regresion): los gates del repo exit 0 en clon limpio y ninguna ruta legitima pasa a excluirse."
  verification_cmd:
    - "python scripts/check_falsification_contracts.py --root ."
    - "python scripts/scan_encoding.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - scripts/scan_encoding.ps1
    - scripts/scan_encoding.py
  out_of_scope:
    - "AC5 de TASK-0342 (el paso de PowerShell verde en un run REAL de Actions): depende de la facturacion, que es del operador."
    - "El troceado de lineas divergente entre los escaneres de neutralidad (TASK-0338)."
    - "Cerrar el espacio de nombres infinito con una fixture finita: no se puede, y por eso AC2 cambia QUE se observa en vez de ampliar la lista."
  risk: high
  estimate: M
---

# TASK-0360 -- el guarda puede excluir sin pasar por la politica

Sale de dos clases **preexistentes** que el checker midio al ratificar el AC4 de TASK-0342
(`Analista-TASK-0342-r5-el-volcado-ya-va-atado-al-consumo-verdict.md`). Ninguna la introduce esa
entrega, y ninguna se arregla con un retoque -- por eso van a tarea propia y no a una quinta
remediacion de 0342.

## E1 -- la exclusion tiene una segunda puerta

La politica (`$ScanPolicy`) es la puerta declarada. Pero el guarda tiene la suya:

```powershell
if ($File.FullName -match "runtime/state") { return $false }
```

Medido con divergencia viva: **negativo exit 0, SOBREVIVE**, y el conjunto que solo ve Python es
`runtime/state/events.jsonl`, `runtime/state/keep.txt`. Es la consecuencia que el propio checker
marco en r4 como la que no podia quedarse -- **el ledger atestado cae del canal de PowerShell en
silencio** -- alcanzada por otra puerta.

El acotamiento honesto que el checker dejo escrito: el mismo ataque sobre una coordenada **dentro**
del universo derivado (`Area_comun/tasks`) SI muere, exit 1. El escape no es que el negativo sea
debil, es que **observa el conjunto excluido sobre un universo pre-elegido** en vez de observar la
decision por fichero. Ninguna fixture finita cubre un espacio de nombres infinito; se cierra
cambiando que se observa.

## E2 -- rojos falsos por ancla de texto

Tres cambios con **divergencia cero medida** ponen el gate rojo: reescribir un comentario de
`Should-Scan`, cambiar `-File -Force` por `-Force -File` (identico en PowerShell) y renombrar
`$PathComparison`. El mas facil de pisar sin querer es el primero: **la prosa del codigo es parte del
contrato**.

Un negativo que se pone rojo por escribir un comentario acaba ignorandose, y un negativo ignorado da
la cobertura por buena sin darla. Es la misma familia que E1 vista desde el otro lado: atarse a la
forma en vez de a la propiedad.

## Por que las dos juntas

Comparten el mecanismo y el fichero. Arreglar E1 sin E2 deja un contrato correcto que nadie mira;
arreglar E2 sin E1 deja un contrato legible con una puerta abierta detras.
