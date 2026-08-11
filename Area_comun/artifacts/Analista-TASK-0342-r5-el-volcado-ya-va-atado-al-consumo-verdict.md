# Veredicto Analista -- TASK-0342 (r5): el volcado ya va atado al consumo; el liston que publique se cumple entero

Autor: Analista (voz adversarial independiente)
Fecha: 2026-08-11 17:32 hora local (UTC+2)
Veredicto: **OK-CLOSABLE (AC4)**, con dos clases residuales declaradas y medidas.
AC5: **excluido de esta review por instruccion del Arquitecto** (diferido por facturacion de Actions).
No lo he medido ni lo cuento como incumplido.

## Ancla canonica

- Commit bajo revision: `6cd15d9c95d24400ca47fbbe6c78d7f6bc49af0d`.
  Implementacion: `14686290e47fb3d32cc561e202a3dc13b5fe064a` (`fix(TASK-0342): bind policy dump to consumption`).
- Codigo revisado == `origin/main` (`d749dbcb`) en las rutas del alcance:
  `git diff --stat 6cd15d9c origin/main -- scripts/ examples/ Area_comun/protocol/` es **vacio** (0 lineas).
  Lo unico que difiere entre el ancla y `origin/main` es `.github/workflows/validate.yml`
  (35 inserciones / 11 borrados), que pertenece a otra cadena (0336/0354) y no toca esta review.
- Estado canonico al arrancar: `python scripts/validate_collaboration_state.py` exit **0**.
  Arbol de trabajo sin modificaciones en ninguna ruta gobernada (solo `personal/` ajeno, no tocado).
- Alcance declarado por la instruccion: **solo hub, sin producto**. Respetado.
- Clon limpio: `git clone --depth 20` + `git fetch --depth 2000` sobre
  `/home/johnb/Aegis_Scratch/multi_agent_project_protocol/an0342r5/cc`, checkout de `6cd15d9c`,
  `git status --short` **0 lineas**. Todo medido ahi y en copias de ese arbol, nunca en el caliente.
  (Se profundizo el clon porque `commit_trailers` necesita alcanzar el commit genesis `57f6250f`;
  con `--depth 20` el validador salia rojo por historia truncada, no por estado.)
- Plataforma de medicion: **PowerShell 7.4.6 sobre `Linux ... WSL2 x86_64`, ext4, sensible a
  mayusculas**, que es la plataforma del job `powershell-linux-parity`. Es la misma capa donde medi
  r2, r3 y r4. En la capa Windows de este equipo sigue sin haber `pwsh`.

## Lo que pedi por adelantado, y lo que sale

El liston que publique al final de r4, palabra por palabra: **G9a, G9b, G9c y G9d rojos; G6six,
G6ord y G6ws verdes; sin editar el runner por coordenada; y el mensaje final diciendo la verdad
sobre lo que se midio.** Esta review es aritmetica, asi que va la aritmetica.

    G9a  $ScanPolicy.SkipDirs        += "zzq"                        exit=1  ROJO   OK
    G9b  $ScanPolicy.SkipSuffixes    += ".log"                       exit=1  ROJO   OK
    G9c  $ScanPolicy.SkipAbsoluteDirs += runtime/state               exit=1  ROJO   OK
    G9d  las tres a la vez                                           exit=1  ROJO   OK
    G6six sexto directorio "dist" declarado en LOS DOS gemelos       exit=0  VERDE  OK
    G6ord reordenar los cinco de la declaracion de PS                exit=0  VERDE  OK
    G6ws  dos espacios dentro del @( ... )                           exit=0  VERDE  OK

**7 de 7.** Cada mutante en su propio arbol, copiado del clon limpio, mutando **produccion**
(`scripts/scan_encoding.ps1`, y en `G6six` tambien `scripts/scan_encoding.py`), nunca el runner.

Los G9 mueren donde tienen que morir, en la comparacion de valores efectivos, no en un ancla de texto:

    G9a  run_encoding_gate_cases.py:222  assert set(python_scan.SKIP_DIRS) == ps_skip_dirs
    G9b  run_encoding_gate_cases.py:224  assert set(python_scan.SKIP_SUFFIXES) == ps_skip_suffixes
    G9c  run_encoding_gate_cases.py:223  assert set(python_scan.SKIP_RELATIVE_DIRS) == ps_policy[...]
    G9d  run_encoding_gate_cases.py:222  (idem G9a)

### Por que el escape de r4 ya no existe como colocacion

En r4 el escape era colocar la mutacion **despues** del volcado. Hoy el volcado esta al final
(`scripts/scan_encoding.ps1:134-146`), despues de las cuatro llamadas `Scan-*`, y lee el mismo objeto
vivo `$ScanPolicy` que `Should-Scan` consulta. "Despues del volcado" es codigo muerto: el bloque
termina en `exit 0`. No queda ningun punto del fichero donde una asignacion cambie el escaneo y no
cambie el volcado **por orden**.

Lo confirme atacando esa misma frontera por el otro lado. `N1_revert` muta despues de la
construccion y **revierte** justo antes del volcado, que es la unica forma de recuperar el desfase
por orden:

    N1_revert  += "zzq" tras la construccion + restauracion antes del volcado   exit=1  MUERE
               run_encoding_gate_cases.py:342
               assert (policy_mutant["skip_dirs"] == ps_skip_dirs) is expected_policy_equal

Muere porque la restauracion tambien anula el mutante `A4_plus_equals` que el runner se fabrica; el
efecto es correcto aunque la ruta sea indirecta. Lo anoto como tal.

### Y las coordenadas ya no estan cableadas

`dist_path` desaparecio. En su sitio hay `fresh_directory_coordinate()` y `fresh_suffix_coordinate()`
(`run_encoding_gate_cases.py:166-186`), que derivan `contract-control-N` / `.contractN` **del valor
volcado**, buscando el primer nombre que no este ocupado. Por eso `G6six` con `dist` ya no revienta:
`dist` dejo de ser una palabra reservada del runner. Y `insert_after_policy_build` ancla en
`^\$ScanPolicy\s*=\s*New-ScanPolicy\s*(#.*)?$`, que esta **fuera** de la declaracion de los arrays;
por eso reordenar o espaciar la declaracion (`G6ord`, `G6ws`) ya no toca ningun ancla.

### El mensaje final dice la verdad, medido

Corri el arbol de `G9a` -- que tiene una divergencia VIVA que el gate mata cuando hay `pwsh` -- con un
PATH sin `pwsh`:

    UNMEASURED: PowerShell 7 parity requires pwsh; CI measures the POSIX boundary.
    OK: encoding gate cases passed (3 py cases; PowerShell parity UNMEASURED).
    NOPWSH_G9a_EXIT=0

La linea de exito ya no afirma una paridad que no ocurrio. El cuarto punto de mi direccion de r4 esta
cerrado. Lo que **no** cambia es que el gate sigue saliendo verde sin `pwsh` teniendo una divergencia
viva delante: eso es R5b y sigue vivo, pero ahora al menos lo declara.

## El defecto original, comprobado por comportamiento sobre POSIX

No me quedo en el contrato. Sobre un arbol sonda propio, con los dos escaneres del clon limpio:

    runtime/memory/index.db   (SQLite binario)  -> NINGUNO lo reporta      (exclusion aplicada)
    runtime/Memory/case.txt   (mojibake)        -> LOS DOS lo reportan     (frontera exact-case)
    resto de la sonda (6 ficheros)              -> conjuntos IDENTICOS
    PY_EXIT=1   PS_EXIT=1

Y sobre el arbol real del clon limpio, en POSIX, los dos salen limpios y el volcado es el esperado:

    pwsh scripts/scan_encoding.ps1 -Root .              exit 0  "OK: encoding scan is clean."
    python3 scripts/scan_encoding.py --root .           exit 0  "OK: encoding scan is clean."
    pwsh scripts/scan_encoding.ps1 -Root . -DumpPolicy  exit 0
      {"skip_dirs":[".git",".venv","venv","__pycache__","node_modules"],
       "skip_relative_dirs":["runtime/memory"],
       "skip_suffixes":[".pyc",".png",".jpg",".jpeg",".gif",".ico",".pdf",".zip"]}

**AC1, AC2 y AC3 se sostienen medidos aqui, en la plataforma donde el defecto se manifestaba.**

## Lo que fui a buscar de nuevo, y encontre

El liston se cumple, asi que la parte util de esta review es lo que sigue abierto. Dos clases, las dos
**preexistentes** (no las introduce la remediacion 4) y las dos declaradas por mi en rondas
anteriores. Las mido con instancias concretas para que no se discutan de palabra.

### E1 -- el guarda puede excluir sin pasar por la politica (escape)

`Should-Scan` consulta `$ScanPolicy`, pero nada obliga a que sea **lo unico** que consulte. Una linea
cableada dentro del guarda excluye ficheros sin tocar el objeto, asi que el volcado sale intacto y el
contrato no ve nada:

    N2_guard_bypass   if ($File.FullName -match "zzq") { return $false }
                      negativo exit=0  SOBREVIVE
                      divergencia VIVA medida: ONLY_PY = runtime/zzq/a.txt

    N2b_ledger_bypass if ($File.FullName -match "runtime/state") { return $false }
                      negativo exit=0  SOBREVIVE
                      divergencia VIVA medida: ONLY_PY = runtime/state/events.jsonl,
                                                         runtime/state/keep.txt

`N2b` es la que importa: es la **misma consecuencia** que marque en r4 como la que no podia quedarse
(el ledger atestado `runtime/state` cae del canal de PowerShell y el negativo permanente dice que los
gemelos coinciden), alcanzada por otra puerta. Que la remediacion 4 cerrara la puerta del orden no
cierra esta.

Y acoto la clase honestamente, porque tiene suelo: el mismo ataque **sobre una coordenada que si esta
en el universo derivado muere**.

    N2c_in_universe   if ($File.FullName -match "Area_comun/tasks") { return $false }
                      negativo exit=1  MUERE
                      run_encoding_gate_cases.py:311
                      powershell_missing: Area_comun/tasks/.gitkeep, Area_comun/tasks/.hidden.md

Es decir: el contrato cubre todo lo que la politica declara y todo lo que de ella se deriva; lo que no
cubre es una coordenada **inventada** que ni esta declarada ni se deriva. Ninguna fixture finita cubre
un espacio de nombres infinito, asi que esto no se cierra anadiendo coordenadas: se cierra cambiando
lo que se observa (por ejemplo, que el guarda emita su decision por fichero y el contrato compare
decisiones, no conjuntos sobre un universo pre-elegido). Eso es otra tarea, no un retoque.

### E2 -- quedan mutantes atados al texto exacto de produccion (rojo falso)

Los tres literales que denuncie en r4 (`skip_dirs_line`, la cadena de `A7_later_assignment`,
`dist_path`) se fueron. Pero `separator_text`, `case_text`, `skip_dir_case_text`, `mutant_text` y
`mutate_function` siguen anclando en texto exacto de produccion, con `assert mutant != ps_text`
detras. Es el X4 que declare en r3 como residual: sigue ahi, y estas son tres instancias nuevas,
todas con **divergencia CERO medida** entre los dos gemelos sobre mi arbol sonda:

    N3_comment       reescribir el COMENTARIO de Should-Scan            exit=1  ROJO FALSO
                     run_encoding_gate_cases.py:401  assert separator_text != ps_text
                     divergencia medida: NO

    N4_param_order   " -File -Force" -> " -Force -File" (identico en PS)  exit=1  ROJO FALSO
                     run_encoding_gate_cases.py:147
                     "mutation anchor missing in Scan-AsciiPath:  -File -Force"
                     divergencia medida: NO

    N5_rename_var    renombrar $PathComparison -> $PathCmp               exit=1  ROJO FALSO
                     run_encoding_gate_cases.py:401  assert separator_text != ps_text
                     divergencia medida: NO

`N3` es la mas facil de pisar sin querer: **editar un comentario pone el gate rojo**. Que el ancla
incluya la linea `# Compare one host-native directory boundary, never a literal slash shape.` hace que
la prosa del codigo sea parte del contrato.

## Tabla vector por vector

| # | Vector | Divergencia viva medida | Negativo | Resultado |
|---|--------|-------------------------|----------|-----------|
| M0 | baseline sin mutar (30 s) | no | exit 0 | OK (control) |
| G9a | `SkipDirs += "zzq"` | si | exit 1 | **PASS** (liston r4) |
| G9b | `SkipSuffixes += ".log"` | si | exit 1 | **PASS** (liston r4) |
| G9c | `SkipAbsoluteDirs += runtime/state` | si | exit 1 | **PASS** (liston r4) |
| G9d | las tres a la vez | si | exit 1 | **PASS** (liston r4) |
| G6six | sexto directorio en LOS DOS gemelos | no | exit 0 | **PASS** (cierra rojo falso r4) |
| G6ord | orden de la declaracion | no | exit 0 | **PASS** (cierra rojo falso r4) |
| G6ws | espacios en la declaracion | no | exit 0 | **PASS** (cierra rojo falso r4) |
| N1 | mutar tras construir + revertir antes de volcar | si | exit 1 | PASS |
| NOPWSH | divergencia viva sin `pwsh` | si | exit 0 + "UNMEASURED" | PASS parcial (mensaje veraz; R5b vivo) |
| MEM | `runtime/memory/index.db` sobre POSIX | no | conjuntos identicos | PASS (AC1/AC2/AC3) |
| N2c | cableado dentro del universo derivado | si | exit 1 | PASS (acota E1) |
| N2 | cableado en `Should-Scan`, coordenada `zzq` | **si** | **exit 0** | **ESCAPE (E1)** |
| N2b | cableado en `Should-Scan`, `runtime/state` | **si** | **exit 0** | **ESCAPE (E1)** |
| N3 | reescribir un comentario | **no** | **exit 1** | **ROJO FALSO (E2)** |
| N4 | `-File -Force` -> `-Force -File` | **no** | **exit 1** | **ROJO FALSO (E2)** |
| N5 | renombrar `$PathComparison` | **no** | **exit 1** | **ROJO FALSO (E2)** |

Saldo de esta ronda, contado por propiedad y no por exit code: **7 de 7 del liston publicado**, mas
1 muerte adicional (N1) y 1 acotacion (N2c); **2 escapes** y **3 rojos falsos**, todos de clases
preexistentes que ya estaban declaradas antes de esta remediacion.

## Reproduccion con exit codes -- clon limpio POSIX sobre `6cd15d9c`

    python3 scripts/scan_encoding.py --root .                        -> 0   OK: encoding scan is clean.
    python3 scripts/validate_collaboration_state.py --root .         -> 0   OK: collaboration state is valid.
    python3 scripts/check_falsification_contracts.py --root .        -> 0
    python3 scripts/check_falsification_contracts.py --root . --inventory -> 0
                                                                            73 declarados;
                                                                            NEG-ENCODING-SKIP-PATH-SEPARATOR boundaries=16
    python3 scripts/scan_domain_neutrality.py --root .               -> 0
    python3 runtime/protocol_replay.py --check-drift --root .        -> 0   verdict=CLEAN up_to_seq=8783
    python3 examples/encoding_gate_cases/run_encoding_gate_cases.py  -> 0   (pwsh 7.4.6 sobre ext4, 30 s)
        POLICY_MUTATION      A4_plus_equals      CAUGHT_DIVERGENCE
        POLICY_MUTATION      A7_later_assignment CAUGHT_DIVERGENCE
        POLICY_MUTATION      A5_multiline        ACCEPTED_EQUIVALENT
        POLICY_MUTATION      A8_trailing_comment ACCEPTED_EQUIVALENT
        LATE_POLICY_MUTATION G9a/G9b/G9c/G9d     CAUGHT_DIVERGENCE
        OK: encoding gate cases passed (3 py cases + measured PowerShell parity and separator mutation).

**Los gates del repo estan verdes. AC6 se cumple.**

E1 es falsable en cuatro comandos, sin CI: insertar
`if ($File.FullName -match "runtime/state") { return $false }` como primera linea de `Should-Scan` en
`scripts/scan_encoding.ps1`, crear `runtime/state/events.jsonl` con un byte >127, correr los dos
escaneres (Python lo reporta, PowerShell no) y correr
`python3 examples/encoding_gate_cases/run_encoding_gate_cases.py` (exit 0).

E2 es falsable en dos: cambiar el comentario
`# Compare one host-native directory boundary, never a literal slash shape.` por cualquier otro texto
y correr el mismo runner (exit 1, `assert separator_text != ps_text`).

## Residuales declarados

- **E1 (nuevo enunciado, clase preexistente):** el guarda puede excluir sin pasar por `$ScanPolicy`;
  el volcado no lo ve. Coordenadas dentro del universo derivado si mueren (`N2c`); las inventadas no
  (`N2`, `N2b`). Consecuencia peor medida: `runtime/state` cae del canal de PowerShell en silencio.
- **E2 (= X4 de r3, sin cerrar):** cinco mutantes del runner siguen anclados en texto exacto de
  produccion; tres cambios semanticamente nulos ponen el gate rojo (`N3`, `N4`, `N5`).
- **R5b (de r3, mitigado):** el negativo sigue saliendo verde sin `pwsh` con una divergencia viva
  delante. Ya **no miente** en la linea final. Queda que en ningun sitio se asevere que la dimension
  se midio al menos una vez.
- **R6 (de r2, sin tocar):** aserciones de mutante guardadas por `if os.name != "nt"`; en Windows con
  `pwsh` esas ramas no se ejercitan.
- **R1 (de r1, sin tocar):** `powershell.exe` 5.1 no tiene `GetRelativePath`. El volcado tambien lo
  llama, asi que la superficie del residual sigue siendo la de r4.
- **R3 (de r1, sin tocar):** paridad con `pwsh` 7 SOBRE Windows sigue sin medir.
- **Sin CI real.** No lo he medido en esta ronda por instruccion expresa. Clon limpio LOCAL no es CI:
  todo lo de arriba vale para AC1-AC4 y AC6, y **no** acredita AC5.
- **Capa de medicion.** Todo esto se mide en el WSL de este equipo, no en la capa Windows. Es la
  misma capa de r2/r3/r4 y es la del job `powershell-linux-parity`, pero es una capa, no las dos.

## Recomendacion de cierre

**OK-CLOSABLE sobre AC4.** El liston que publique por adelantado se cumple entero y por la razon
correcta: el volcado dejo de ser un punto del fichero y pasa a leer el objeto que el escaneo consumio,
las coordenadas se derivan del valor volcado en vez de estar escritas a mano, y el mensaje final
describe lo que se midio. AC1, AC2, AC3 y AC6 se sostienen medidos. AC5 esta **diferido por decision
del operador** y no lo he tocado: la tarea no la cierro yo, y su cierre efectivo sigue dependiendo de
esa decision, no de este veredicto.

Lo digo con su proporcion: **la remediacion 4 no movio la clase de sitio, la cerro.** Es el unico
salto de los cuatro del que puedo decir eso.

### Lo que recomiendo hacer con E1 y E2

**No abrir una remediacion 5 en 0342.** Las dos clases son preexistentes, ninguna es regresion de esta
entrega, y ninguna se arregla con un retoque: E1 pide cambiar **que** se observa (la decision por
fichero, no el conjunto sobre un universo pre-elegido) y E2 pide sustituir los cinco mutantes
anclados en texto por mutantes verificados **por efecto medido**. Eso es una tarea propia, enunciada
como propiedad, y quien decide si se abre es el Arquitecto con el operador. Mi papel aqui era juzgar
el liston, y el liston sale.

Lo unico que pido explicitamente: que E1 no se pierda. `runtime/state` es el ledger atestado.

### Bucle de arreglo

No lo hay para 0342: emito OK-CLOSABLE, no CHANGE-REQUIRED. Si el Arquitecto decide abrir la tarea de
E1/E2, mi presupuesto de checker para ella es el de siempre y se pacta al enunciarla, no aqui.

- **Gates afectados si se abre:** `Scan encoding`, `Scan encoding with PowerShell`,
  `Run encoding gate cases`, `powershell-linux-parity`, `check_falsification_contracts --inventory`.
- **AC5 de 0342** sigue esperando un run REAL de Actions cuando vuelva la admision.

-- Analista
