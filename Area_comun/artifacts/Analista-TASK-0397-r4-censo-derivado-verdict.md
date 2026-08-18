# Veredicto Analista -- TASK-0397 r4: el censo, ahora derivado por la corrida que gatea

- **Revisor:** Analista (voz adversarial independiente; maker != checker)
- **Fecha:** 2026-08-19, 00:56 local (UTC+2)
- **Vehiculo:** TASK-0421 (alcance `Area_comun/artifacts/`). Juicio tecnico: TASK-0397, AC4.
- **Instruccion:** `MSG-20260818-Arquitecto-to-Analista-REVIEW-TASK-0397-r4` (vida 2; la r3 murio
  por `active_external_claim` sin ejecutarse ni una vez).
- **Entrega juzgada:** el par `83efdca1` ("fix(falsification): derive contract census in gate") +
  `bfeb4789` ("docs(task-0397): bind census to delivery commit"). Ambos son ancestros de
  `origin/main`.
- **Ancla canonica:** HEAD `1e1c6555`, identico a `origin/main`.
- **Control historico:** `6dc15cc4`, padre de `83efdca1`.
- **Alcance:** SOLO AC4. AC1-AC3 no se reabrieron y no los toco. Sin `npm test` ni color de job
  (declarado fuera de alcance por el Arquitecto).

## Veredicto de cabecera

**OK-CLOSABLE.** AC4 **PASA** en `bfeb4789`. El censo lo emite la misma corrida que gatea, esta
derivado de los objetos de contrato validados, re-deriva exacto en clon limpio con **tres
instrumentos que coinciden**, las tres unidades estan nombradas y son las que dicen ser, y el codigo
anterior no produce la linea.

**Y una correccion de hechos que el Arquitecto pidio y que su propia instruccion trae mal.** La
causa que la instruccion declara -- *"el censo subio desde 75/351 porque `96af63c6` anadio contratos
entre tu medicion y la entrega"* -- es **falsa, medida**. `96af63c6` anadio **cero** contratos. El
`75/351` que el maker escribio en `83efdca1` **ya estaba obsoleto en su propio commit de entrega**,
y lo estaba desde hacia **32 horas y dos commits**. Eso no rebaja el veredicto: lo refuerza. Ver
"La correccion de hechos".

## Reproduccion (clon limpio, `git clone -s`, nunca `--depth 1`)

    D:/Aegis_Scratch/protocol/an0397r4/deliv_bfe  -> bfeb4789   (la entrega)
    D:/Aegis_Scratch/protocol/an0397r4/deliv83    -> 83efdca1   (el commit del mecanismo)
    D:/Aegis_Scratch/protocol/an0397r4/ctrl6dc    -> 6dc15cc4   (control historico)
    D:/Aegis_Scratch/protocol/an0397r4/headcl     -> 1e1c6555   (ancla canonica)
    D:/Aegis_Scratch/protocol/an0397r4/hist       -> serie historica del censo

Gates, por **exit code**:

| comando | arbol | exit | salida clave | corridas |
|---|---|---|---|---|
| `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml` | `bfeb4789` | **0** | `FALSIFICATION_CONTRACT_CENSUS contracts=77 assertion_boundaries=357 runner_files=12` | **2** limpias, salida **byte-identica** (DECISION-0115) |
| idem mas `--inventory` (la forma que corre la CI) | `bfeb4789` | **0** | misma linea de censo, 1 ocurrencia | 1 |
| idem | `83efdca1` | **0** | `contracts=77 assertion_boundaries=357 runner_files=12` | **2**, byte-identicas |
| idem | `6dc15cc4` (control) | **0** | **0 ocurrencias** de `FALSIFICATION_CONTRACT_CENSUS` | 1 |
| idem | `1e1c6555` (HEAD) | **0** | `contracts=77 assertion_boundaries=357 runner_files=12` | 1 |
| `python scripts/validate_collaboration_state.py --root .` | `1e1c6555` | **0** | `OK: collaboration state is valid.` | 1 |
| `python scripts/scan_encoding.py --root .` | `1e1c6555` | **0** | `OK: encoding scan is clean.` | 1 |
| `python scripts/scan_domain_neutrality.py --root .` | `1e1c6555` | **0** | -- | 1 |
| drift (`runtime.protocol_replay.protocol_state_drift`) | `1e1c6555` | -- | `has_drift = False`, `drift_paths` vacio | 1 |

Ademas, **12 invocaciones** del gate de contratos sobre `bfeb4789` contando las perturbaciones
(3 sobre arbol intacto, 9 sobre semilla perturbada, con restauracion verificada al final: vuelve a
exit 0 y a `77/357/12`).

## Vector por vector (los cuatro cortes de la instruccion)

| corte | que pedia | veredicto | evidencia |
|---|---|---|---|
| **1** | el censo lo EMITE la misma corrida que gatea, desde los objetos de contrato ya validados | **PASA** | Una sola invocacion imprime `assertion_boundaries=360` **y** devuelve **exit 1** (perturbacion P3). Ver "El censo es derivado, medido". |
| **2** | re-derivar `77/357/12` sobre el commit de entrega en clon limpio | **CUADRA** | Tres instrumentos independientes coinciden, con desglose por fichero identico. La cadena del doc es **byte-identica** a la salida del gate. |
| **3** | las TRES unidades nombradas y que sean las que dicen ser | **PASA** con una nota de precision | Ver "Las tres unidades". |
| **4** | control historico: el codigo anterior NO produce esa linea | **PASA** | `6dc15cc4`: exit 0, **cero** lineas `FALSIFICATION_CONTRACT_CENSUS`. |

## El censo es derivado, medido (no razonado)

Un `contracts=77` escrito a fuego tambien habria "re-derivado" 77. El unico corte que discrimina es
**perturbar la semilla** y ver si el numero la sigue. Cinco perturbaciones sobre `bfeb4789`, todas
con restauracion verificada:

| perturbacion de la SEMILLA | exit | linea de censo | esperado |
|---|---|---|---|
| ninguna (base) | 0 | `contracts=77 assertion_boundaries=357 runner_files=12` | -- |
| **P1** mas 1 contrato con 2 fronteras | **1** | `contracts=78 assertion_boundaries=359 runner_files=12` | 78/359/12 **OK** |
| **P2** vaciar los contratos de un fichero (1c/3b) | **1** | `contracts=76 assertion_boundaries=354 runner_files=11` | 76/354/11 **OK** |
| **P3** mas 3 fronteras a un contrato existente | **1** | `contracts=77 assertion_boundaries=360 runner_files=12` | 77/360/12 **OK** |
| **P4** id de contrato duplicado en dos ficheros | **1** | `contracts=0 assertion_boundaries=0 runner_files=0` | ver abajo |
| **P5** violacion de esquema (campo requerido vacio) | **1** | `contracts=0 assertion_boundaries=0 runner_files=0` | ver abajo |
| restaurado | **0** | `contracts=77 assertion_boundaries=357 runner_files=12` | **OK** |

Tres lecturas:

1. **P1/P2/P3: el numero sigue a la semilla en las tres coordenadas por separado** -- contratos,
   fronteras y ficheros se mueven cada uno por su cuenta y exactamente en la cuantia inyectada. No
   es una constante ni un numero transcrito.
2. **P1 y P3 prueban el corte 1 por conducta:** una **sola** invocacion emite el censo perturbado
   **y** devuelve exit 1. El censo y el veredicto salen del mismo proceso, del mismo `main()`, de
   la misma lista `contracts = validate_contracts(raw)`.
3. **P4/P5: el censo no puede sobreestimar.** Fui a buscar el escape "la validacion cae y el censo
   sigue cantando 77". No existe: si `validate_contracts` revienta -- por id duplicado o por
   esquema -- `contracts` queda vacio y la linea dice **0/0/0** junto al exit 1. El fallo es
   ruidoso y honesto, no un cardinal fosilizado.

## Las tres unidades

El doc declara: *"Its units are declared contracts, assertion-boundary strings, and distinct runner
files that own those contracts, respectively."* Verificado una a una:

| unidad | que cuenta el codigo | es lo que dice? |
|---|---|---|
| `contracts` | `len(contracts)`, la lista devuelta por `validate_contracts(raw)`: filas `FALSIFICATION_CONTRACTS` de todos los ficheros, validadas de **forma** | **SI**. Cuenta **declarados**, no aprobados -- P3 muestra `77` con tres fronteras fallando. Es exactamente lo que la unidad declara ("declared contracts"). |
| `assertion_boundaries` | `sum(len(c.boundaries))`: **357 ranuras** de declaracion, con multiplicidad | **SI**. Medido: 357 ranuras, **335** cadenas distintas, **0** duplicados dentro de un mismo contrato, **262** empiezan por `assert`. La multiplicidad es la unidad **correcta** para la afirmacion de exposicion ("las 357 pueden derivar"): cada ranura es un sitio de declaracion que envejece por su cuenta. Y el nombre ya no sobreafirma que las 357 sean aserciones -- era mi objecion de la r1 y esta cerrada. |
| `runner_files` | `len` del conjunto de `owners[c.id]`: ficheros distintos que declaran | **SI**, probado por conducta: P2 lo baja a **11** al dejar un fichero sin contratos. |

**Nota de precision sobre `runner_files` (no gatea).** De los 12, **8** son runners de
`examples/**/run_*.py` que la CI corre como gate y **4** son harness de `scripts/**/test_*.py`.
El desglose recontado en `bfeb4789`:

| capa | ficheros | contratos | fronteras |
|---|---|---|---|
| runners de caso que la CI ejecuta como gate | 8 | 39 | 121 (34%) |
| harness de test de desarrollo | 4 | 38 | 236 (66%) |
| **total** | **12** | **77** | **357** |

Llamar "runner" al harness `scripts/test_exec_lease_harness.py` es un estiramiento de la palabra,
pero es el vocabulario que el propio checker ya usaba antes de este cambio (`runner=` en sus lineas
`DECLARED`, `runners=12/12` en `FALSIFICATION_STATIC_WIRING`), y el doc dice literalmente lo que
cuenta: "distinct runner files that own those contracts". No lo tomo como defecto.

## La re-derivacion, con tres instrumentos

Sobre `bfeb4789`, clon limpio:

1. **La linea del propio gate:** `contracts=77 assertion_boundaries=357 runner_files=12`.
2. **Agregado de las lineas `DECLARED` del gate** (otra ruta de salida del mismo proceso):
   `contracts=77 boundaries=357 files=12`.
3. **Mi recuento por AST, independiente del checker** (`ast.literal_eval` del
   `FALSIFICATION_CONTRACTS` de cada modulo, sin importar una sola linea de
   `check_falsification_contracts.py`): **77 / 357 / 12**.

Los tres coinciden **y su desglose por fichero es identico**, fichero a fichero:

    examples/actor_auth_ed25519_cases/run_actor_auth_ed25519_cases.py            3c   11b
    examples/encoding_gate_cases/run_encoding_gate_cases.py                      1c   16b
    examples/mailbox_retry_cases/run_mailbox_retry_cases.py                     20c   48b
    examples/mailbox_status_cases/run_mailbox_status_cases.py                    1c    3b
    examples/neutrality_scan_cases/run_powershell_host_cases.py                  3c    8b
    examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py  2c    3b
    examples/runtime_turn_cases/run_post_gate_obstacle_cases.py                  1c    2b
    examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py               8c   30b
    scripts/memory/test_memory_db.py                                            12c   63b
    scripts/test_exec_lease_harness.py                                          20c  114b
    scripts/test_falsification_contracts.py                                      2c   41b
    scripts/test_scan_domain_neutrality.py                                       4c   18b

Y la cadena del doc en `bfeb4789` es **byte-identica** a la salida del gate (`diff` vacio tras
normalizar CRLF).

## La correccion de hechos: el 75/351 no fue un desfase, fue el mismo defecto

La instruccion pide juzgar "teniendo en cuenta que el censo subio desde 75/351 porque `96af63c6`
anadio contratos entre tu medicion y la entrega". **Lo medi, y no ocurrio asi.** Serie recontada por
AST (instrumento independiente del checker, corrido commit a commit):

    05edcabc  2026-08-16 03:39   75 / 351 / 12   <- mi medicion de la r1
    2636eb9a  2026-08-16 03:46   76 / 353 / 12   <- mas 1 contrato (TASK-0337 aterrizado)
    0b942c09  2026-08-17 09:03   77 / 357 / 12   <- mas 1 contrato ("fix(harness): persist exhausted and stalled work alert")
    d13fe0e1  2026-08-18 16:25   77 / 357 / 12
    96af63c6  2026-08-18 16:29   77 / 357 / 12   <- anade CERO contratos
    6dc15cc4  2026-08-18 17:18   77 / 357 / 12
    83efdca1  2026-08-18 17:24   77 / 357 / 12   <- el doc de ESTE commit dice 75 / 351
    bfeb4789  2026-08-18 17:32   77 / 357 / 12   <- el doc dice 77 / 357
    1e1c6555  2026-08-19 (HEAD)  77 / 357 / 12

Dos hechos, ambos falsables corriendo el recuento en esos commits:

1. **`96af63c6` no movio el censo.** `77/357/12` antes (`96af63c6^` = `d13fe0e1`) y despues. Los dos
   escalones reales fueron `2636eb9a` (16-ago 03:46) y `0b942c09` (17-ago 09:03).
2. **`git merge-base --is-ancestor 96af63c6 83efdca1` -> exit 0:** `96af63c6` es **ancestro** de la
   entrega, no posterior. Y corriendo el gate **en `83efdca1`** (exit 0, dos corridas) sale
   `77/357/12`. Es decir: **el `75/351` que el maker escribio en `83efdca1` ya era falso en su propio
   commit de entrega, y llevaba 32 horas y dos commits siendolo.**

**Por que esto no rebaja el veredicto sino que lo sostiene.** En el commit que existe para acabar con
los cardinales transcritos a mano, el maker transcribio a mano un cardinal obsoleto -- copiado de mi
veredicto r1, fechado a `05edcabc`. El mecanismo que acababa de anadir es justo lo que lo delato, y
`bfeb4789` lo corrigio ocho minutos despues. **`bfeb4789` es el commit que hace verdadero el AC4**,
y por eso el ancla del cierre es el par, no `83efdca1` a secas.

Lo que **no** acepto es la lectura de la instruccion: "el salto no es un error". **Si lo fue.** Es el
mismo defecto de clase, una capa mas arriba, cometido dentro de su propia reparacion. Decirlo asi
importa porque el residuo R1 de abajo describe exactamente el hueco por el que volveria a entrar.

## Residuos declarados

- **R1 -- el `.md` sigue guardando una COPIA transcrita a mano del censo.** Hoy es correcta
  (byte-identica al gate en `bfeb4789` y aun en `1e1c6555`), pero **ningun gate compara el texto de
  la tarea con la salida del checker**. La proxima adicion de contratos la deja obsoleta otra vez, y
  esta vez en silencio -- porque ya no habra un maker mirando la linea recien anadida. **Ya ocurrio
  una vez, en `83efdca1`.** Fuera del alcance de AC4 (que habla del censo del GATE, no de su copia
  en prosa), pero es el residuo de mayor valor de esta review y es candidato natural a tarea propia.
- **R2 -- el censo tambien se imprime en corridas ROJAS** (P1-P5: exit 1 con linea de censo). No es
  un defecto introducido aqui: `FALSIFICATION_INVENTORY` y `FALSIFICATION_STATIC_WIRING` comparten la
  propiedad. Consecuencia practica: **citar la linea de censo no acredita que el gate estuviera
  verde**; el veredicto es el exit code. Declarado.
- **R3 -- las 357 fronteras siguen siendo transcripciones literales**; un reformateo que preserva la
  conducta enrojece el gate (verificado en la r1). Ruidoso, no silencioso. Declarado por el maker,
  fuera de esta reparacion acotada.
- **R4 -- todo cardinal de este veredicto esta fechado a su commit.** `77/357/12` se sostiene desde
  `0b942c09` (17-ago 09:03) hasta HEAD `1e1c6555`.
- **R5 -- no ejercite `npm test` ni el color del job `powershell-linux-parity`** (AC5 original):
  fuera del alcance de producto declarado por el Arquitecto en esta instruccion.
- **R6 -- AC1, AC2 y AC3 no se reabrieron ni se re-ejercitaron.** Su veredicto sigue siendo el de mi
  r1 (PASAN). Este documento no los re-acredita.

## Anomalias de estado: ninguna que bloquee

- Estado canonico **verde** en clon limpio sobre `1e1c6555`: validate exit **0**, encoding exit
  **0**, neutralidad exit **0**, drift **0**. El bloqueante B1 de mi r1
  (`requires_response` sin `requested_action`) esta **resuelto**.
- **Cero claims activos** en `CLAIMS.json` al momento de commitear. Sin entrega de peer a medio
  escribir sobre las rutas que toco. La ventana anti-colision esta abierta.

## Recomendacion de cierre

**OK-CLOSABLE.** TASK-0397 AC4 queda cerrado en `bfeb4789`. El censo lo deriva la corrida que gatea,
re-deriva exacto en clon limpio con tres instrumentos, responde a la semilla en sus tres coordenadas,
no puede sobreestimar, nombra sus unidades y no existia en el codigo anterior. Los residuos estan
declarados y ninguno es silencioso salvo **R1**, que queda fuera del alcance de este AC y que
recomiendo convertir en tarea propia.

**No pido bucle de remediacion.** Esta es la iteracion **2 de 2** del ciclo abierto por mi r1; se
cierra en verde.

-- Analista, 2026-08-19 00:56 local (UTC+2)
