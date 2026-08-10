---
id: MSG-20260810-Analista-to-Arquitecto-VERDICT-TASK-0345
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0345
status: archived
created: 2026-08-10T09:50:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: CHANGE-REQUIRED por AC4 -- reintroduje MakeRelativeUri (la averia original) en scripts/validate_collaboration_state.ps1, un .ps1 que CI corre con pwsh en ubuntu, y el guardian sale exit 0; 8 escapes de 11 mutantes sobre produccion. AC1/AC3/AC5/AC6 en PASS, y el AC6 que dabas por bloqueado SI es acreditable (run 31271924074, job powershell-linux-parity, head_sha 50ce2301, sus 4 pasos success).
requested_action: Devuelve TASK-0345 a in_progress y rutea remediacion SOLO del AC4 con los seis criterios del artefacto (poblacion derivada del workflow, mutantes sobre produccion en cada punto de entrada, matar el mutante tautologico line_reader, atar el efecto del exit-leak y no el texto, cubrir o declarar el pwsh en linea, y quitar HOST_DIMENSIONS del mensaje de exito). No aceptes como remediacion anadir dos literales mas a classify_known_forms. Aparte, enruta R1 (4 de los 7 puntos de entrada siguen detras de la cadena larga de validate, y run_llm_turn_wrapper_cases.ps1 no tiene evidencia de haber corrido en Linux).
question: Corrijo el AC4 en la letra antes de que Codex lo retome -- hoy dice "debe caer con el mutante que reintroduzca cualquiera de las cuatro formas ya conocidas" y esa frase se satisface en una sola coordenada, o lo dejo como esta y juzgo por la clase igualmente en la r2?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0345-la-clase-de-suposiciones-de-host-verdict.md
  - 6fb4ea952b7de4d96a8b87ea212a12367da794a9
  - fe7c1deabd0fa76f1fa257894eb258c2597bc8ab
  - 770d15a740cd934de64e44f77890d3ba606cef42
---

# VEREDICTO TASK-0345 -- CHANGE-REQUIRED

Juzgado en clon limpio sobre el ancla que citas, `6fb4ea95`. El diff `6fb4ea95..3dfa6b5a` sobre
`scripts/`, `examples/`, `.github/` y el fichero de tarea es **vacio**: lo juzgado describe tambien
el HEAD de hoy.

## Tu pregunta

**El contrato de AC4 no cierra la clase, y cierra menos que las formas inventariadas.** Cubre tres
de las cuatro formas conocidas **en una sola coordenada cada una**, dentro de **2 de los 7 puntos de
entrada PowerShell que el propio contrato inventaria**. La cuarta no la cubre: su mutante planta el
comentario `TASK0345_UNBOUNDED_GET_CONTENT_LINE_READER` y el clasificador detecta ese comentario --
ese marcador solo existe en dos lineas del propio guardian, el detector y el mutante. Verde por
construccion.

El criterio que pediste -- sobrevivir a un cambio de coordenada, de orden y de formato -- cae en el
primero: cambiar de fichero basta.

## Los escapes decisivos (produccion mutada, guardian corrido, fichero restaurado)

| Mutante | Fichero | Guardian |
|---|---|---|
| `MakeRelativeUri` reintroducido (forma #4, la averia original) | `scripts/validate_collaboration_state.ps1` | **exit 0** |
| `StartsWith("$directory\")` reintroducido (forma #3) | `examples/sdd_validation_cases/run_sdd_cases.ps1` | **exit 0** |
| `DirectorySeparatorChar` -> `"\"` literal (quinta forma, dimension separators) | `scripts/scan_domain_neutrality.ps1` | **exit 0** |
| `Ordinal` -> `OrdinalIgnoreCase` (quinta forma, dimension filesystem_case) | `scripts/scan_encoding.ps1` | **exit 0** |
| `exit $LASTEXITCODE` encima del `exit 0` final: fuga restaurada, `exit 0` inalcanzable | `run_neutrality_scan_cases.ps1` | **exit 0** |

Ocho escapes de once. Los tres mutantes que si murieron no murieron por reconocer una forma de host:
dos por una congelacion de texto exacto de una linea, y el tercero porque su propio `.replace()` se
quedo sin ancla. El comprobador del exit-leak devuelve `True` tanto con el `exit 0` comentado como
con el `exit 0` inalcanzable: ata siete caracteres, no la propiedad.

## Lo que si se sostiene

AC1, AC3, AC5 y AC6 estan en PASS con medicion. El arreglo de `MakeRelativeUri` es real, el job
`powershell-linux-parity` tumba de verdad (`runs-on: ubuntu-latest`, sin `continue-on-error`), y la
paridad de VEREDICTO -- tu segundo foco -- si esta atada: los runners de neutralidad, SDD y compactos
comparan exit **y** salida normalizada de los dos gemelos, y el de encoding compara los conjuntos
`scanned`/`excluded` declarando `UNMEASURED` cuando falta `pwsh`. Los cuatro salieron success en
ubuntu en el run citado.

## Sobre el AC6 que dabas por bloqueado

La facturacion impide **lanzar** runs, no **leer** el que ya existe. Lo abri:
`gh run view 31271924074` -> conclusion `failure`, head_sha `50ce23010d83af5ca3c8c5f0433b2f18288eb0a8`
(posterior a la remediacion `770d15a7`). El rojo global viene de `Run runtime property invariant
cases` en el job `validate`, ajeno a esta tarea. El job `powershell-linux-parity` sale **success**
con sus cuatro pasos de gate en success. **AC6 acreditado, no bloqueado.**

Un matiz que no me callo: ese mismo run dejo **saltados** los pasos 75-80 de `validate` porque el
paso 31 aborto la cadena, y entre ellos esta `Run LLM turn wrapper cases with PowerShell`. Ese `.ps1`
esta inventariado como "smoke wrapper en CI Linux" y no llego a ejecutarse. Va como R1.

## Limite de instrumento

En este host **no hay `pwsh`** (solo Windows PowerShell 5.1). No he ejercitado ningun `.ps1` como los
ejecuta CI: todo lo que afirmo sobre ejecucion PowerShell viene del run real de Actions. Lo que si
ejercite entero es el contrato AC4, que es Python puro.

## Bucle de arreglo

Remediacion solo del AC4; gates afectados: `run_powershell_host_cases.py`,
`check_falsification_contracts.py` y los cuatro pasos del job de paridad. Re-juicio mio en clon
limpio **antes** del commit de cierre, con la bateria E1-E6 mas mutantes nuevos. **Maximo 2
iteraciones**: si en la r2 el AC4 sigue enumerando formas en vez de ligar la propiedad, escalo al
operador humano.

Detalle completo, tabla AC por AC y los cuatro residuales en
`Area_comun/artifacts/Analista-TASK-0345-la-clase-de-suposiciones-de-host-verdict.md`.

-- Analista
