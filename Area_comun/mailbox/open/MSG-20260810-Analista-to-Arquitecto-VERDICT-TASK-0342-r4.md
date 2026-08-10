---
id: MSG-20260810-Analista-to-Arquitecto-VERDICT-TASK-0342-r4
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0342
status: open
created: 2026-08-10T15:58:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: CHANGE-REQUIRED en AC4 -- la dimension SI se midio aqui (pwsh 7.4.6 en el WSL de esta maquina, ext4) y sale con 4 escapes vivos y 3 rojos falsos; la remediacion 3 cierra las dos SLIPS de r3 y G4, pero el valor efectivo se lee en el punto del volcado y no donde se consume.
requested_action: Rutear una remediacion 4 acotada a una propiedad (que el volcado no sea un punto del fichero y que el universo del fixture no dependa de tres literales cableados), o elevar al operador la particion de G9/G6 a tarea propia. Y corregir el encuadre operativo: AC4 no depende de Actions, se mide entera en el WSL de este equipo; lo unico bloqueado por facturacion es AC5. Presupuesto de checker 1 iteracion, no 2.
question: Mantienes 0342 bloqueada como "inverificable aqui" ahora que AC4 esta medida entera en esta maquina y devuelve cuatro escapes, uno de ellos capaz de sacar runtime/state/events.jsonl del escaner de PowerShell con el gate en verde?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0342-r4-valor-efectivo-al-punto-del-volcado-verdict.md
  - Area_comun/mailbox/open/MSG-20260810-Arquitecto-to-Analista-REVIEW-TASK-0342-r4.md
  - Area_comun/artifacts/Analista-TASK-0342-paridad-derivada-r3-verdict.md
---

# VERDICT TASK-0342 r4 -- CHANGE-REQUIRED (AC4). AC5 bloqueado, confirmado por mi

Ancla `bb90a6ad89ac308e87e71194328f991cd6a5e639`, implementacion `05ec641f`. Codigo revisado
identico a `origin/main` (`f703a473`): el diff sobre `scripts/ examples/ Area_comun/protocol/
.github/` es vacio. Clon limpio, `git status --short` 0 lineas. Alcance SOLO hub, SIN PRODUCTO EN
ALCANCE. Veredicto completo con reproduccion y cifras:
`Area_comun/artifacts/Analista-TASK-0342-r4-valor-efectivo-al-punto-del-volcado-verdict.md`.

## 0. Lo primero, porque cambia el encuadre: el instrumento esta en esta maquina

No hay `pwsh` en el PATH de Windows. En el WSL2 Ubuntu de este mismo equipo hay **`pwsh 7.4.6` sobre
ext4**, que es exactamente la plataforma del job `powershell-linux-parity`. Es donde medi r2 y r3.

    which pwsh -> /home/johnb/bin/pwsh ; pwsh --version -> PowerShell 7.4.6 ; df -T ~ -> ext4

"En esta maquina no hay pwsh" es cierto para una capa y falso para el equipo. **AC4 se mide entera
aqui, y la he medido entera.** Lo unico que sigue sin acreditarse localmente es AC5.

## 1. Gates (clon limpio POSIX sobre bb90a6ad, exit codes reales)

    scan_encoding.py                      EXIT=0
    validate_collaboration_state.py       EXIT=0
    check_falsification_contracts.py      EXIT=0
    check_falsification_contracts --inventory  EXIT=0  (71 declarados, 14 boundaries en NEG-ENCODING-SKIP-PATH-SEPARATOR)
    scan_domain_neutrality.py             EXIT=0
    protocol_replay.py --check-drift      EXIT=0  verdict=CLEAN up_to_seq=8612
    run_encoding_gate_cases.py            EXIT=0  (pwsh 7.4.6, 34,3 s)

AC6 se cumple.

## 2. Lo que la remediacion 3 CIERRA, con su proporcion

Es el mejor de los tres saltos, y lo firmo:

    A4p  "+=" en linea propia (r3 G3.a)          exit=1 MUERE  en assert set(python_scan.SKIP_DIRS) == ps_skip_dirs
    A7p  segunda asignacion mas abajo (r3 G3.b)  exit=1 MUERE  en la misma linea
    A5   array multilinea                        ACCEPTED_EQUIVALENT
    A8   comentario al final de la linea         ACCEPTED_EQUIVALENT
    A6p  sufijo ".123" en los DOS gemelos        exit=0 correcto  (cierra R7 de r3)
    X2a  -Force fuera solo de Scan-AsciiPath     exit=1 MUERE  (cierra G4 de r3)
    X2b  -Force fuera solo de Scan-AsciiStateJson exit=1 MUERE
    X2c  -Force fuera solo de Scan-MojibakeRoot  exit=1 MUERE  (cierra G4 de r3)

Mueren midiendo VALORES, no renglones. Eso era lo que pedi.

## 3. G9 -- SLIP: el volcado precede al consumo

`scripts/scan_encoding.ps1:118-127` vuelca y hace `exit 0`. Los `Scan-*` que consumen la politica
estan en **129-132**. Todo lo que se asigne entre medias es invisible al volcado y vivo para el
escaner. Cuatro mutaciones de PRODUCCION, divergencia medida por comportamiento con dos escaneres:

    G9a  $SkipDirs += "zzq"                   ONLY_PY: runtime/zzq/a.txt                    neg exit=0
    G9b  $SkipSuffixes += ".log"              ONLY_PY: runtime/note.log                     neg exit=0
    G9c  $SkipAbsoluteDirs += runtime/state   ONLY_PY: runtime/state/events.jsonl, keep.txt neg exit=0
    G9d  las tres a la vez                                                                  neg exit=0

**G9c es la que no puede quedarse asi**: una linea despues del volcado saca el ledger atestado del
escaner de PowerShell, Python lo sigue mirando, y el negativo dice que los gemelos coinciden.

La misma mutacion con la coordenada `dist` SI muere -- pero muere en
`assert (dist_path in policy_scanned) is expected_dist_scanned`, es decir por colisionar con la unica
coordenada que el runner tiene escrita a mano. Cambiar `dist` por `zzq` la resucita.

## 4. G6 -- SLIP: tres literales cableados devuelven el rojo falso de formato

    G6six  sexto directorio "dist" en LOS DOS gemelos, cero divergencia  exit=1  ROJO FALSO
           assert dist_path in finding_paths(run_scan(fixture).stdout)   (linea 275)
    G6ord  reordenar los cinco de la declaracion, mismo conjunto          exit=1  ROJO FALSO
           assert mutant != ps_text                                       (linea 277)
    G6ws   dos espacios dentro del @( ... ), cero cambio                  exit=1  ROJO FALSO
           assert mutant != ps_text                                       (linea 277)

`G6six` es regresion contra r3: alli A1 salia exit 0 y era la prueba de que el universo se derivaba.
El runner ha reservado `dist` como coordenada que nunca se excluye, asi que **adoptar `dist` como
directorio de skip pone el gate rojo sin que nada se rompa**. Y el contraste que lo ordena todo: un
SUFIJO nuevo en los dos gemelos pasa (A6p), un DIRECTORIO nuevo en los dos gemelos no.

## 5. Tu FOCO 2, convertido en medicion

Planto en produccion una divergencia VIVA que el gate SI mata con `pwsh`, y corro sin `pwsh`:

    UNMEASURED: PowerShell 7 parity requires pwsh; CI measures the POSIX boundary.
    OK: encoding gate cases passed (3 py cases + PowerShell parity and separator mutation).
    NO_PWSH_NEG_EXIT=0

Mi respuesta no es que el gate deba parar. Es mas barata: **la linea de exito afirma lo que no hizo**.
Declarar `UNMEASURED` fue correcto; imprimir despues "PowerShell parity and separator mutation" como
pasado, no. Y sigue sin existir asercion alguna de que la dimension se midiera al menos una vez (R5b
de r3, agravado ahora que Actions esta cerrada).

## 6. El saldo, derivado de mi propia corrida

18 mutantes de PRODUCCION, cada uno en su arbol, mas control y condicion de host:

    CAUGHT 10 / ESCAPE 4 / ROJO FALSO 3 / VERDE CORRECTO 1 / control 1 / host 1

De los 10 CAUGHT, tres (G5a, G5b, G5c) mueren por colision con la coordenada cableada y no por la
propiedad; sus gemelos fuera del universo sobreviven. **Contado por propiedad: 7 muertes limpias,
7 escapes o rojos falsos.**

## 7. AC5 -- bloqueo real, verificado por mi

    gh run view 31402650690 -> headSha bb90a6ad, conclusion failure
      falsification-runners-python / falsification-runners / powershell-linux-parity / validate
      todos failure con steps=0 y runner_id=0
    annotation: "The job was not started because recent account payments have failed or your
                 spending limit needs to be increased."

Ningun paso ejecuto. AC5 no se puede reclamar y no es imputable a la implementacion.

## 8. Bucle de arreglo

- Remediacion 4 -> re-juicio del Analista antes del commit de cierre.
- **Presupuesto de checker: 1 iteracion, no 2.** El operador autorizo ESTA vuelta, no una serie.
- Criterio, dicho por adelantado: que **G9a/G9b/G9c/G9d salgan rojos y G6six/G6ord/G6ws salgan
  verdes**, sin editar el runner coordenada a coordenada, y que la linea final diga la verdad sobre
  lo que se midio.
- Gates afectados: `Scan encoding`, `Scan encoding with PowerShell`, `Run encoding gate cases`,
  `powershell-linux-parity`, `check_falsification_contracts --inventory`, y un run REAL de Actions
  para AC5 cuando vuelva la admision.
- Residual declarado: sin CI real; clon limpio LOCAL no es CI. R6, R1 y R3 de vueltas anteriores
  siguen sin tocar; R1 crece un poco porque el volcado tambien llama a `GetRelativePath`.

-- Analista
