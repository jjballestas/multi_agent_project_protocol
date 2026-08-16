# Veredicto adversarial -- TASK-0337, cierre tras el revert de H-1 y la paridad del gemelo

**Revisor:** Analista (voz independiente / checker)
**Fecha:** 2026-08-16, 14:42 local (UTC+2) -- reloj leido, no estimado
**Instruccion:** `Area_comun/mailbox/open/MSG-20260816-Arquitecto-to-Analista-REVIEW-TASK-0337-cierre.md`
**Alcance recortado por el encargo:** AC7 y AC10 NO se re-juzgan (acreditados en r2). H-1 y H-3 quedan
fuera de este corte por decision del operador.
**Recomendacion de cierre: OK-CLOSABLE, con una condicion de publicacion (S-1).**

---

## 1. Ancla canonica

| Elemento | Valor |
|---|---|
| HEAD de protocolo revisado | `cef48839` (= `origin/main` al cerrar; re-anclado -- avanzo desde `60e365cf` durante la revision) |
| Revert de H-1 | `7ca0d74b` -- `revert(TASK-0337): remove ineffective H-1 exemption` |
| Cambio de H-1 revertido | `f2de3ad7`; control historico pre-H-1 = `f2de3ad7^` = `db8759b9` |
| Correccion del gemelo PowerShell | `3d357a28`; control historico pre-fix = `3d357a28^` = `231aa719` |
| Estado que acredite en r2 (AC7/AC10) | `623fb8b4` |
| Clon limpio de revision | `D:/Aegis_Scratch/protocol/rev0337c` (`git clone -s`, checkout `cef48839`) |
| Clon limpio de control | `D:/Aegis_Scratch/protocol/ctrl0337c` (checkout `db8759b9` y `231aa719`) |

Ningun gate se corrio en el arbol caliente. El arbol vivo solo tiene ficheros sin seguimiento de
terceros y una modificacion de skill que no es mia; no se toco ninguno. `60e365cf..cef48839` no toca
`scripts/`, `examples/` ni `.github/`: los dos commits que entraron durante la revision son ruteo de
mailbox y documentacion de skill, luego el re-anclaje no invalida ninguna medicion.

## 2. Puertas, en el clon limpio a `cef48839`

| Gate | Exit |
|---|---|
| `python scripts/validate_collaboration_state.py --root .` | **0** |
| `python scripts/scan_encoding.py --root .` | **0** |
| `python scripts/scan_domain_neutrality.py --root .` | **0** |
| `./scripts/scan_domain_neutrality.ps1 -Root .` | **0** |
| `python scripts/check_falsification_contracts.py --root .` | **0** -- `permanent_negatives=76 declared=76 missing=0` |
| `protocol_state_drift(.)` | `has_drift = False` |
| `run_residue_scope_pair_case()` | **0** |
| `python scripts/test_scan_domain_neutrality.py` | **1** -- ver **S-1** |
| `python scripts/test_exec_lease_harness.py` | **1** (`total=31 passed=28 failed=3`) -- R-2 de r2, sin cambio |

## 3. Punto 1 del encargo -- el revert dejo el arbol en su estado pre-`f2de3ad7`: **PASS**

No lo juzgo por el mensaje del commit sino por identidad de contenido. Blobs (`git rev-parse
<commit>:<ruta>`) del HEAD canonico contra los DOS anclas que importan:

| Fichero | identico a `f2de3ad7^` (pre-H-1) | identico a `623fb8b4` (lo que acredite en r2) |
|---|---|---|
| `scripts/harness/peer_mailbox_cron.ps1` | **SI** (`5b27160e`) | **SI** |
| `examples/mailbox_retry_cases/run_mailbox_retry_cases.py` | **SI** (`bd74b3d5`) | **SI** |
| `scripts/test_exec_lease_harness.py` | **SI** (`b4837edd`) | **SI** |
| `scripts/scan_domain_neutrality.py` | **SI** | **SI** |

Esto responde la pregunta del encargo con precision: **el estado no es solo "pre-`f2de3ad7`"; es byte
a byte el mismo sobre el que acredite AC7 y AC10 en r2.** No hay nada que re-pagar, y no lo re-pago.

`check_falsification_contracts.py`: **exit 0, 76 contratos**, como reporto Codex. Control historico en
clon limpio a `db8759b9`: **exit 0, `permanent_negatives=76 declared=76 missing=0`**. Cifra y unidad
identicas, luego el revert no dejo caer ni un contrato. Aviso de lectura que arrastro de mi propia
memoria: ese gate verifica **declaracion** (que las fronteras existan junto al test), no ejecucion;
por eso lo cruzo abajo con los runners.

El invariante que H-1 habia invertido esta restaurado, verificado en el fichero y no en el nombre del
test: `scripts/test_exec_lease_harness.py:2059-2060` vuelve a afirmar `rename["state"] == "none"` y
`rename["paths"] == []`; `:2095-2096` vuelve a afirmar `foreign_only == "none"` y
`foreign_paths == []`; las mismas cuatro cadenas reaparecen como fronteras declaradas en `:35-36`. Por
eso `NEG-HARNESS-PREEXEC-DEFER-STARVATION` vuelve a declararse con `boundaries=5` en vez de emitir el
`assertion boundary not found` de r3. **H-3 cerrado.**

## 4. Punto 2 del encargo -- la correccion del gemelo PowerShell: **PASS, y es discriminante**

Lo que habia que refutar es que 1515 sea la coordenada real y que el negativo de paridad se ejecutase
sobre ambos gemelos. No acepto el texto del entregable: mido con control historico y con mutante.

**A/B con control historico.** El instrumento se delata solo:

| Estado | `scan_domain_neutrality.ps1` | `scan_domain_neutrality.py` |
|---|---|---|
| `231aa719` (pre-fix, gemelo en 1474) | **exit 1**, emite `scripts/harness/peer_mailbox_cron.ps1:1515: Codex` | exit 0 |
| `cef48839` (post-fix, gemelo en 1515) | **exit 0** | exit 0 |

El propio escaner pre-fix **nombra 1515** como la ocurrencia no exenta. La coordenada no es una
afirmacion del maker que yo firme de confianza: es la que emite el instrumento cuando falla, asi que
el `1502` del ACTION era efectivamente obsoleto y Codex tenia razon al corregirlo. Linea 1515 leida en
el clon: `# subcommand. The reference agent (codex exec) reads the prompt from stdin via '-'.`

Y el rojo no era cosmetico: `./scripts/scan_domain_neutrality.ps1 -Root .` esta cableado en CI en
`.github/workflows/validate.yml:61` y `:526` **ya en el estado pre-H-1**. `3d357a28` apaga un rojo de
CI real; no decora un inventario.

**Negativo de paridad, ejecutado por mi sobre los dos gemelos.** Inserte una linea antes de la
ocurrencia vigilada en la produccion copiada del clon (`peer_mailbox_cron.ps1`), corri ambos escaneres
y restaure el fichero byte a byte (`git status --porcelain` vacio despues):

| Gemelo | Exit | Emision |
|---|---|---|
| `scan_domain_neutrality.py` | **1** | `scripts/harness/peer_mailbox_cron.ps1:1516: Codex` |
| `scan_domain_neutrality.ps1` | **1** | `scripts/harness/peer_mailbox_cron.ps1:1516: Codex` |

Ambos mueren, con la coordenada desplazada y la misma linea de salida. Reproducido lo que declaro
Codex. (Mi linea sonda contenia la palabra `Analista`, asi que ambos emitieron ademas
`:1515: Analista`; es artefacto de mi sonda, y aparece **identico en los dos gemelos**, lo que refuerza
la paridad en vez de debilitarla.)

## 5. Punto 3 del encargo -- residuo de H-1 vivo: **ninguno, ni en codigo ni en ledger**

- **Codigo:** las cuatro rutas de la seccion 3 son identicas a pre-H-1. La exencion de residuo propio
  vive solo donde vivia antes de H-1: `peer_mailbox_cron.ps1:931` y `:946`, ambas dentro de la rama de
  scope resoluble (`$candidateIsOwnPersonal` en `:927`, `$sourceIsOwnPersonal` en `:942`). No hay
  rastro de la exencion que H-1 anadia en la rama no resoluble.
- **Ledger:** `CLAIMS.json` no tiene **ningun** claim activo (`active_total = 0`); las 26 entradas de
  0337 en `CLAIMS_ARCHIVE.json` -- incluidas `CLAIM-20260816-Codex-TASK-0337-h1` y las tres del revert
  -- estan todas `released`. `TASK_INDEX.json` deja TASK-0337 en `in_review` con owner Codex, coherente
  con el fichero de tarea. Drift 0.
- **Gobierno de la correccion del gemelo:** `CLAIM-20260816-Codex-TASK-0337-ps1-parity` declaraba en su
  `scope` tanto `scripts/scan_domain_neutrality.py` como `scripts/scan_domain_neutrality.ps1`, asi que
  la ruta tocada fuera de los `scope_routes` del intake estaba cubierta por claim y no es un hallazgo.
- **Conducta:** `run_residue_scope_pair_case()` sale 0 sobre produccion, igual que en r2.

## 6. S-1 (NUEVO, no atribuible, pero rojo en una puerta enviada -- y mayor de lo declarado)

`python scripts/test_scan_domain_neutrality.py` sale **exit 1** en clon limpio a `cef48839`:

```
FAIL: test_identity_exemption_inventories_are_one_to_one_and_in_parity
PERMANENT_NEGATIVE: NEG-NEUTRALITY-IDENTITY-INVENTORY-PARITY
  (line 536) AssertionError: python_inventory != powershell_inventory
```

Ese runner esta cableado en CI en `.github/workflows/validate.yml:522`.

**Atribucion, con control historico y no supuesta:**

| Estado | `test_scan_domain_neutrality.py` | Negativos que fallan |
|---|---|---|
| `db8759b9` (pre-H-1) | exit 1, **2 fallos** | `...INVENTORY-PARITY` + `...EXEMPTION-PARITY` |
| `cef48839` (HEAD) | exit 1, **1 fallo** | `...INVENTORY-PARITY` |

La entrega **no introduce** este rojo: lo hereda y lo reduce a la mitad -- `3d357a28` mata
`NEG-NEUTRALITY-IDENTITY-EXEMPTION-PARITY` (el de arbol real, el mismo que encendia el escaner `.ps1`
en CI). Por eso **no bloqueo el cierre con esto**, y seria incoherente hacerlo: en r3 bloquee H-3
porque el control probaba que la entrega lo habia INTRODUCIDO; aqui el control prueba lo contrario.

**Pero el residuo declarado se queda corto, y esto si es hallazgo.** El cuerpo de la tarea declara
"Divergencias restantes: 1". Esa cifra es correcta **como diferencia de inventarios** -- lo verifique
volcando los dos con `-DumpIdentityInventory` y comparandolos entrada a entrada: 10 ficheros en cada
lado, **una** sola entrada divergente (`peer_mailbox_cron.ps1:553`, Python declara `_EXEMPT_TERM_1` y
`_EXEMPT_TERM_6`, PowerShell solo el primero). Lo que la cifra no dice es que **arreglar esa
divergencia no pone verde el contrato**, porque detras hay mas, oculto por el fallo temprano.

Medido, no razonado. Aplique en el clon la remediacion evidente -- quitar el digest `_EXEMPT_TERM_6`
del lado Python en `scan_domain_neutrality.py:70` -- y volvi a correr todo:

| Gate tras la remediacion evidente | Resultado |
|---|---|
| `scan_domain_neutrality.py` / `.ps1` | exit 0 / exit 0 |
| `test_scan_domain_neutrality.py` | **sigue exit 1**, ahora en `:611`: `AssertionError: 0 not greater than or equal to 1 : runtime/context.py:16:Codex` |

Es decir: la asercion de paridad pasa y aparece la siguiente, que hasta ahora nadie habia visto. El
mismo test exige que **cada coordenada exenta contenga de verdad el termino que exime**. Censo propio
sobre el inventario vivo (recomputo independiente, no lectura del entregable):

| Entrada declarada | Termino | Realidad en la linea |
|---|---|---|
| `runtime/context.py:16` | `Codex` | la linea es `"implementer": "implementer",` -- **el termino no esta** |
| `runtime/context.py:17` | `operador` | **el termino no esta** |
| `runtime/context.py:17` | `operador humano` | **el termino no esta** |
| `scripts/harness/peer_mailbox_cron.ps1:553` | digest `c857d09d` | **no es un termino de identidad configurado** (los configurados son exactamente `Analista`, `Arquitecto`, `Codex`, `operador`, `operador humano`) |

Y el censo total: `declared_exemption_count = 92` frente al `assertEqual(..., 91)` que el test fija.
El uno de diferencia es justo el digest muerto de 553.

Sobre el 553: el digest `c857d09d...` es el de `claude`, y la linea 553 contiene literalmente
`"claude"` y `"codex"`. Pero `claude` **no esta en la lista de terminos de identidad configurados**,
asi que la declaracion Python es **muerta**: quitarla deja el escaner Python en exit 0 (medido). La
direccion correcta de arreglo es por tanto **retirar el digest del lado Python**, no anadirlo al
gemelo PowerShell: anadirlo igualaria los inventarios concediendo al `.ps1` una exencion sobre un
termino que ese escaner no vigila -- un verde por construccion. Lo digo porque esa era mi primera
recomendacion y la medicion la desmintio.

Atribucion de las cuatro entradas: `scripts/scan_domain_neutrality.py` y `runtime/context.py` son
**blobs identicos** en `f2de3ad7^`, `623fb8b4`, `231aa719` y `HEAD` (`runtime/context.py` =
`8e96c0b0` en los cuatro). Ninguna de las cuatro la introduce esta entrega, ni ninguna entrega de
0337. Son deuda anterior.

**Lo que exijo es que no se silencie.** La frase del encargo *"con su negativo de paridad ejecutado
sobre ambos gemelos"* es cierta para el negativo de desplazamiento que reproduje en la seccion 4, y
**falsa** si se lee como "las puertas de paridad estan verdes": el contrato que lleva la palabra
*paridad* en el nombre esta rojo, y por cuatro entradas, no por una.

## 7. Residuales declarados

- **S-1 (medio, NO atribuible).** El de la seccion 6. Condicion de publicacion, no de cierre.
- **R-2 (de r2, vigente y sin cambio).** `python scripts/test_exec_lease_harness.py`, que es
  `verification_cmd` declarada de 0337, sale **exit 1** en clon limpio (`total=31 passed=28 failed=3`)
  con los **mismos tres** de r2: `test_silent_process_tree_cpu_is_work_derived_and_mutation_proven`,
  `test_live_unreadable_lease_is_preserved_and_deadline_mutant_dies`,
  `test_admission_liveness_path_uses_production_functions_and_kills_constant_mutants`. No atribuible;
  esta tarea no se cierra por exit code de su propia `verification_cmd`.
- **H-1 (abierto por decision del operador).** El interbloqueo circular sigue vivo para los mensajes
  cuyo scope NO es resoluble, y su causa no esta en el guardia de residuo sino en
  `message_scope_ambiguous` (`peer_mailbox_cron.ps1:1206`). Medido en r3, seccion 5.1.
- **R-1, R-3, R-4, R-5 (de r2/r3, vigentes).** Ancla en `$Root`; comodines descartados en silencio por
  `ConvertTo-ComparableScope`; `$ResiduePath` global escrito desde una vista por-mensaje; reinicio del
  reloj de `RETRY_EXHAUSTED` al cambiar el `reason`.
- **Agujeros del negativo M3/M4 (de r3).** Siguen abiertos: `retry-residue-scope-pair` no tiene vector
  con residuo propio DENTRO del scope ni vector de renombrado. Viajan con H-1.

## 8. Reproduccion

```
git clone -s D:/Agentes/multi_agent_project_protocol D:/Aegis_Scratch/protocol/rev0337c
cd D:/Aegis_Scratch/protocol/rev0337c && git checkout cef48839
python scripts/validate_collaboration_state.py --root .        # exit 0
python scripts/scan_encoding.py --root .                       # exit 0
python scripts/scan_domain_neutrality.py --root .              # exit 0
./scripts/scan_domain_neutrality.ps1 -Root .                   # exit 0
python scripts/check_falsification_contracts.py --root .       # exit 0  (76/76/0)
python scripts/test_scan_domain_neutrality.py                  # exit 1  <-- S-1
python scripts/test_exec_lease_harness.py                      # exit 1  (3/31; R-2)
python -c "from pathlib import Path; from runtime.protocol_replay import protocol_state_drift; print(protocol_state_drift(Path('.'))['has_drift'])"   # False
python -c "import importlib.util;s=importlib.util.spec_from_file_location('m','examples/mailbox_retry_cases/run_mailbox_retry_cases.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.run_residue_scope_pair_case()"   # exit 0

# identidad de contenido (punto 1):
for f in scripts/harness/peer_mailbox_cron.ps1 examples/mailbox_retry_cases/run_mailbox_retry_cases.py \
         scripts/test_exec_lease_harness.py scripts/scan_domain_neutrality.py ; do
  git rev-parse "f2de3ad7^:$f" "623fb8b4:$f" "HEAD:$f" ; done     # tres blobs iguales por fichero

# control historico del gemelo (punto 2):
git clone -s D:/Agentes/multi_agent_project_protocol D:/Aegis_Scratch/protocol/ctrl0337c
cd D:/Aegis_Scratch/protocol/ctrl0337c && git checkout 3d357a28^
./scripts/scan_domain_neutrality.ps1 -Root .                   # exit 1: ...peer_mailbox_cron.ps1:1515: Codex
python scripts/scan_domain_neutrality.py --root .              # exit 0
git checkout f2de3ad7^ && python scripts/test_scan_domain_neutrality.py   # exit 1, DOS fallos (S-1)
python scripts/check_falsification_contracts.py --root .       # exit 0 (76/76/0)

# negativo de paridad (punto 2), sobre la produccion copiada del clon, restaurada despues:
#   insertar una linea antes de peer_mailbox_cron.ps1:1515 -> ambos gemelos exit 1 y
#   ambos emiten "scripts/harness/peer_mailbox_cron.ps1:1516: Codex"

# censo de S-1 (seccion 6), en el clon:
./scripts/scan_domain_neutrality.ps1 -Root . -DumpIdentityInventory > inv_ps.json
#   y comparar con scanner.IDENTITY_LITERAL_EXEMPTIONS -> 10 ficheros por lado, 1 entrada divergente
#   recomputo de coordenadas muertas: para cada (ruta, linea, digest) declarado, comprobar que el
#   termino configurado correspondiente aparece de verdad en esa linea -> 4 entradas muertas, total 92
```

Bancos y sondas del revisor viven en `D:/Aegis_Scratch/protocol/` (fuera del arbol atestado, no
entregables). Todos los ficheros sondados se restauraron byte a byte y los clones quedaron con
`git status --porcelain` vacio.

## 9. Recomendacion de cierre

**OK-CLOSABLE.** Los tres puntos que el encargo pone a juicio pasan, medidos por contenido y por
conducta, nunca por el nombre de un test ni por el mensaje de un commit:

1. El revert dejo el arbol **byte a byte identico** a `f2de3ad7^` y, lo que mas importa, identico a
   `623fb8b4` -- el estado exacto sobre el que acredite AC7 y AC10 en r2.
   `check_falsification_contracts` exit 0 con 76/76/0, cifra confirmada tambien en el control pre-H-1.
   H-3 cerrado: las cuatro aserciones invertidas estan restauradas y su contrato vuelve a declarar sus
   cinco fronteras.
2. La correccion del gemelo esta en pie y es **discriminante**: el escaner pre-fix emitia el rojo
   nombrando 1515 el mismo, el post-fix sale 0, y el negativo de desplazamiento mata a los dos gemelos
   con emision identica.
3. No queda residuo de H-1: ni en las cuatro rutas de codigo, ni en claims (0 activos), ni en drift.

**Condicion de publicacion, no de cierre (S-1).** El paquete no puede embarcarse afirmando paridad de
gemelos sin nombrar que `NEG-NEUTRALITY-IDENTITY-INVENTORY-PARITY` esta **rojo** en
`test_scan_domain_neutrality.py`, cableado en `validate.yml:522`. Y hay que nombrarlo con la cifra
correcta: no es "1 divergencia" sino **1 divergencia de inventario + 3 coordenadas muertas en
`runtime/context.py` + un censo 92 frente a 91**. Es deuda heredada, la entrega la reduce de dos
fallos a uno, y por eso no retiene el cierre de 0337; pero si se publica como "residuo menor de
inventario" se estara publicando un gate rojo con aspecto de nota al pie.

Mi recomendacion concreta: **tarea propia**, porque no es de 0337 -- 0337 no la introdujo y los
ficheros implicados son identicos desde antes de la primera entrega. Su DoD, por conducta y en clon
limpio: `python scripts/test_scan_domain_neutrality.py` exit 0, con los dos escaneres en exit 0, y
sin usar la via facil de anadir al `.ps1` un digest que ese escaner no vigila.

**Bucle de arreglo:** no aplica -- emito OK-CLOSABLE, no CHANGE-REQUIRED, asi que no abro iteracion.
Las dos que declare en r2 se consumieron en r2 y r3, y su desenlace fue el revert, que era la salida
correcta. Si el Arquitecto decidiera en cambio retener 0337 hasta apagar S-1, lo juzgo en **una** ronda
y las puertas que vuelvo a correr en clon limpio son `test_scan_domain_neutrality.py`, ambos escaneres,
`check_falsification_contracts.py` y el censo de coordenadas muertas de la seccion 6.

-- Analista, 2026-08-16, 14:42 local (UTC+2)
