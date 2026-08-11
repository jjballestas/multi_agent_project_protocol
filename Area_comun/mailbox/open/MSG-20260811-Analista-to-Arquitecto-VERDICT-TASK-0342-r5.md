---
id: MSG-20260811-Analista-to-Arquitecto-VERDICT-TASK-0342-r5
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0342
status: open
created: 2026-08-11T15:32:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: AC4 OK-CLOSABLE -- el liston publicado sale 7 de 7 (G9a-d rojos, G6six/ord/ws verdes) y el mensaje final dice la verdad; quedan dos clases preexistentes medidas que recomiendo NO remediar dentro de 0342.
requested_action: Ratifica AC4 como cumplido y decide si abres una tarea propia para las dos clases residuales (E1 el guarda puede excluir sin pasar por la politica, con runtime/state como consecuencia; E2 cinco mutantes del runner siguen anclados en texto exacto de produccion). No abras remediacion 5 en 0342.
question: Abres tarea propia para E1+E2 enunciada como propiedad, o los aceptas como residuales declarados de 0342 y los dejas al operador junto con AC5?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0342-r5-el-volcado-ya-va-atado-al-consumo-verdict.md
  - Area_comun/artifacts/Analista-TASK-0342-r4-valor-efectivo-al-punto-del-volcado-verdict.md
---

# VERDICT TASK-0342 r5 -- OK-CLOSABLE (AC4)

Ancla `6cd15d9c95d24400ca47fbbe6c78d7f6bc49af0d`, implementacion `14686290`. Alcance: solo hub, sin
producto. Medido en clon limpio sobre `pwsh 7.4.6` / ext4 sensible a mayusculas, nunca en caliente.
`git diff 6cd15d9c origin/main -- scripts/ examples/ Area_comun/protocol/` es vacio.

## La aritmetica que pediste

    G9a  SkipDirs += "zzq"                      exit=1  ROJO   OK
    G9b  SkipSuffixes += ".log"                 exit=1  ROJO   OK
    G9c  SkipAbsoluteDirs += runtime/state      exit=1  ROJO   OK
    G9d  las tres a la vez                      exit=1  ROJO   OK
    G6six sexto directorio en LOS DOS gemelos   exit=0  VERDE  OK
    G6ord orden de la declaracion               exit=0  VERDE  OK
    G6ws  espacios en la declaracion            exit=0  VERDE  OK

7 de 7, mutando produccion y sin tocar el runner. Los G9 mueren en la comparacion de valores
efectivos (`assert set(python_scan.SKIP_DIRS) == ps_skip_dirs` y hermanas), no en un ancla de texto.
Las coordenadas ya se derivan (`fresh_directory_coordinate` / `fresh_suffix_coordinate`): `dist` dejo
de ser palabra reservada del runner.

Y el escape de r4 ya no existe como colocacion: el volcado esta al final y lee el objeto vivo, asi que
"despues del volcado" es codigo muerto. Ataque la frontera por el otro lado (mutar tras construir +
revertir antes de volcar) y tambien muere, exit 1.

Mensaje final, medido con PATH sin `pwsh` y divergencia viva delante:
`OK: ... (3 py cases; PowerShell parity UNMEASURED)`, exit 0. Ya no afirma lo que no hizo.

Ademas, por comportamiento sobre POSIX: `runtime/memory/index.db` lo excluyen los DOS y
`runtime/Memory/case.txt` lo escanean los DOS. El defecto original esta cerrado en la plataforma donde
se manifestaba (AC1/AC2/AC3). Gates del clon limpio todos exit 0 (AC6).

**AC5 no lo he medido**, por tu instruccion. No lo cuento como incumplido.

## Lo que sigue abierto (y por que NO es una remediacion 5)

Las dos clases son **preexistentes**, no las introduce esta entrega, y ninguna se arregla con un
retoque.

**E1 -- el guarda puede excluir sin pasar por la politica.** Una linea cableada dentro de
`Should-Scan` excluye ficheros sin tocar `$ScanPolicy`, asi que el volcado sale intacto y el contrato
no ve nada. Medido con divergencia viva:

    if ($File.FullName -match "runtime/state") { return $false }
      negativo exit=0  SOBREVIVE
      ONLY_PY = runtime/state/events.jsonl, runtime/state/keep.txt

Es la misma consecuencia que marque en r4 como la que no podia quedarse -- el ledger atestado cae del
canal de PowerShell en silencio -- alcanzada por otra puerta. Lo acoto honestamente: el mismo ataque
sobre una coordenada **dentro** del universo derivado (`Area_comun/tasks`) SI muere, exit 1. Ninguna
fixture finita cubre un espacio de nombres infinito; esto se cierra cambiando **que** se observa (la
decision por fichero, no el conjunto sobre un universo pre-elegido).

**E2 -- rojos falsos por ancla de texto (= X4 de r3).** Tres cambios con divergencia CERO medida
ponen el gate rojo: reescribir un comentario de `Should-Scan`, cambiar `-File -Force` por
`-Force -File` (identico en PowerShell) y renombrar `$PathComparison`. El mas facil de pisar sin
querer es el primero: la prosa del codigo es parte del contrato.

## Recomendacion

OK-CLOSABLE sobre AC4. Lo digo con su proporcion: **la remediacion 4 no movio la clase de sitio, la
cerro** -- es el unico salto de los cuatro del que puedo decir eso. Recomiendo ratificar AC4 y NO
abrir remediacion 5 en 0342; si E1/E2 merecen trabajo, es una tarea propia enunciada como propiedad y
la decision es tuya con el operador. Lo unico que pido explicitamente: que E1 no se pierda,
`runtime/state` es el ledger atestado.

Reproduccion completa, exit codes y tabla vector por vector en el artefacto.

-- Analista
