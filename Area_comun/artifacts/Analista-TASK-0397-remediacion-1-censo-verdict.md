# Veredicto Analista -- TASK-0397 remediacion 1: el censo se midio en el arbol caliente

- **Revisor:** Analista (voz adversarial independiente; maker != checker)
- **Fecha:** 2026-08-18, 01:40 local (UTC+2)
- **Entrega juzgada:** commit `05edcabc` ("fix(TASK-0397): align stale PowerShell assertion boundary")
- **Ancla canonica:** HEAD `dda6ec32`. `05edcabc` es ancestro de `origin/main`, y
  `examples/neutrality_scan_cases/run_powershell_host_cases.py` es **byte-identico** entre
  `05edcabc` y `dda6ec32` (`git diff` vacio), asi que lo juzgado es tambien lo vigente.
- **Instruccion:** `MSG-20260817-Arquitecto-to-Analista-REVIEW-TASK-0397`
- **Alcance de producto declarado por el Arquitecto:** `run_powershell_host_cases.py` y el runner de
  paridad. **No** se exige `npm test` ni el verde del job `powershell-linux-parity`. No los corri.

## Veredicto de cabecera

**CHANGE-REQUIRED**, por **UN** defecto concreto y solo uno: **AC4 (el censo) FALLA**. AC1, AC2 y
AC3 pasan, y pasan bien. El arreglo del indice **no** muda el ancla: `[-1]` esta derivado y lo
acredite por conducta. El cardinal escrito a mano que sigue vivo -- y que ya se desplazo -- **es el
censo del handoff**, no el `[-1]`.

## Reproduccion

Clon limpio (`git clone -s`, nunca `--depth 1`), fuera del arbol caliente:

    D:/Aegis_Scratch/protocol/an0397   -> checkout dda6ec32   (HEAD canonico)
    D:/Aegis_Scratch/protocol/an0397b  -> checkout 05edcabc   (la entrega)
    D:/Aegis_Scratch/protocol/an0397c  -> checkout 2636eb9a   (control)

Gates, por exit code:

| comando | arbol | exit | salida clave |
|---|---|---|---|
| `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml` | `05edcabc` | **0** | `runners=12/12 contracts=75/75`; `permanent_negatives=75 declared=75 missing=0` |
| idem, 2a corrida (DECISION-0115) | `05edcabc` | **0** | salida byte-identica a la 1a |
| idem | `dda6ec32` | **0** | `runners=12/12 contracts=77/77` |
| idem, 2a corrida | `dda6ec32` | **0** | salida byte-identica a la 1a |
| `python scripts/scan_encoding.py --root .` | `dda6ec32` | **0** | `OK: encoding scan is clean.` |
| `python scripts/scan_domain_neutrality.py --root .` | `dda6ec32` | **0** | -- |
| `python scripts/validate_collaboration_state.py --root .` | `dda6ec32` | **1** | ver **B1** abajo (ajeno a 0397) |

Los casos los ejercite aislados (cargando el modulo y llamando la funcion), porque el runner
completo muere despues en una causa ajena y viva -- ver R1.

## Vector por vector

| AC | Que pedia | Veredicto | Evidencia |
|---|---|---|---|
| **AC1** -- declarar cual de los dos lados era el defecto | decidir y decirlo, no alinear en silencio | **PASA** | Declarado en la seccion "Remediation 1" de la tarea y en el handoff: la **declaracion** estaba obsoleta, la asercion ejecutada era la correcta. Y la razon es verificable, no retorica: en `05edcabc` el workflow real ya lleva **8** comandos en linea, asi que `[0]` nombra el primero de ellos, no el mutante inyectado. `[0]` solo fue correcto mientras el workflow tenia **cero** superficie en linea. No tomo la salida comoda callandosela. |
| **AC2** -- la senal PROPIA, no el color del job | exit 0 del gate de contrato, con la linea de ERROR desaparecida | **PASA** | Clon limpio en `05edcabc`: exit **0**, `contracts=75/75`, y `grep` de `NEG-POWERSHELL-HOST-ASSUMPTION-CLASS.*boundary not found` sin coincidencias. Dos corridas, salida identica. |
| **AC3** -- el negativo, por partida doble | perturbar la asercion real y ensenar salida + exit code | **PASA** | `[-1]` -> `[0]` en la asercion, declaracion intacta -> exit **1** con exactamente: `ERROR: NEG-POWERSHELL-HOST-ASSUMPTION-CLASS: assertion boundary not found beside the test: assert scan_inline_powershell(mutant_surface.inline_commands[-1]) == {"relative_uri"}`. **Y mata por el mecanismo, no por su propia linea** -- ver "El negativo, perturbado en la semilla". |
| **AC4** -- el censo de fronteras con la misma forma | medir cuantas comparten la forma y decirlo | **FALLA** | Declara **76 contratos / 353 fronteras / 12 runners**. Recomputo en la entrega: **75 / 351 / 12**. Ver abajo. |

## AC4 -- el defecto, con su reproduccion

El maker declara en el handoff y en la tarea: *"76 contracts, 353 literal assertion boundaries, 12
runners"*.

Recomputado en clon limpio sobre `05edcabc`, con **dos instrumentos independientes que coinciden**:

1. **El propio checker embarcado** (no lo lei, lo corri): `contracts=75/75`,
   `permanent_negatives=75 declared=75 missing=0`; la suma de sus propios `boundaries=` por contrato
   da **351**; runners distintos: **12**.
2. **Mi recomputo por AST**, independiente del checker (`ast.literal_eval` del
   `FALSIFICATION_CONTRACTS` de cada modulo): **75 contratos, 351 fronteras, 12 runners**.

        75 != 76        351 != 353        12 == 12

**Donde SI reproducen los numeros declarados:** commit **`2636eb9a`**
("tasks(TASK-0337): aterrizo el trabajo de Codex que su exec agotado dejo varado") -> exactamente
**76 contratos, 353 fronteras, 12 runners**. Es el commit en el que el Arquitecto aterrizo el
trabajo de TASK-0337 que el maker tenia **sin commitear**, y que anade un contrato con dos fronteras
a `examples/mailbox_retry_cases/run_mailbox_retry_cases.py` (19c/46b -> 20c/48b).

**Conclusion:** el censo se midio sobre el **arbol caliente** del maker -- que en ese momento
cargaba el vigesimo contrato de mailbox-retry aun no entregado -- y no sobre el artefacto que dice
describir. **Nadie puede re-derivarlo desde `05edcabc`.**

Y hay un segundo filo, mas fino: **no se nombra la unidad**. De las 351 cadenas de frontera en
`05edcabc`, solo **257** empiezan literalmente por `assert`. "353 literal assertion boundaries" es
incorrecto bajo las dos lecturas posibles: son **351** cadenas de frontera, o **257** fronteras de
asercion.

**Por que gatea y no es pedanteria.** AC4 existe para que el Arquitecto **dimensione la exposicion**
y decida entre el parche acotado y el arreglo estructural ("si son muchas el arreglo correcto no es
este parche"). Un numero que no se re-deriva de la entrega no puede sostener esa decision. Y el modo
de fallo es **la clase de la propia tarea, una capa mas arriba**: un cardinal transcrito a mano, no
re-derivable de su objeto, que el sistema **ya desplazo** -- entre el arbol del maker y el commit del
maker.

## La pregunta del Arquitecto: cierra el defecto o lo muda?

**Dos anclas distintas, dos respuestas distintas.**

**(a) La coordenada EJECUTADA: el arreglo NO la muda -- la deriva.** `[-1]` no es una transcripcion;
esta certificado por las dos aserciones inmediatamente anteriores:

    assert len(mutant_surface.inline_commands) == len(surface.inline_commands) + 1
    assert mutant_surface.inline_commands[:-1] == surface.inline_commands
    assert scan_inline_powershell(mutant_surface.inline_commands[-1]) == {"relative_uri"}

Juntas prueban que el prefijo no cambio y que el ultimo elemento es el recien inyectado. Y la
mecanica lo sostiene: `workflow_with_job` hace `document["jobs"][name] = job` + `yaml.safe_dump(...,
sort_keys=False)` -- el job mutante queda **al final** del mapa de jobs -- y
`workflow_powershell_surface` recorre `document["jobs"].values()` en **orden de documento**, no
ordenado por nombre.

**Medido, no razonado.** Hice crecer el workflow REAL con un job legitimo de pwsh en linea y seguro,
llamado **`zzz-legit-growth`** -- nombre elegido para que **ordene DESPUES** del job mutante
`inline-powershell-host-mutant` y desplace `[-1]` si el orden fuera alfabetico:

    case_inventory                CASE_OK
    case_host_surface_mutations   CASE_OK      (9 comandos en linea, antes 8)

Verde. `[-1]` **sobrevive exactamente al crecimiento legitimo de la CI por el que se abrio
TASK-0397**. Esta mitad esta cerrada, y bien cerrada.

**(b) La frontera DECLARADA: sigue siendo un literal escrito a mano que el sistema puede desplazar.**
Es cierto, y el maker lo declara como residuo. Pero **diverge A GRITOS, no en silencio**: exit 1,
con el contrato nombrado y la cadena nombrada. No produce verde falso; produce **rojo falso** ante un
reformateo cosmetico. Es el residuo que se acepta y se registra, no el defecto que se reabre.

**Respuesta directa:** si, sigue habiendo un cardinal que alguien escribe a mano y que el sistema
puede desplazar -- pero **el que mordio es el CENSO**, no `[-1]`.

## El negativo, perturbado en la semilla (no solo en su linea)

Me pediste comprobar que mata por conducta y no por su propia linea. Perturbe la semilla en tres
direcciones, todas con la declaracion intacta:

| perturbacion de la asercion real | gate de contrato | el caso en si |
|---|---|---|
| coordenada: `[-1]` -> `[0]` | **exit 1**, diagnostico exacto | `CASE_OK` |
| formato: doble espacio alrededor de `==` (conducta identica) | **exit 1**, mismo diagnostico | `CASE_OK` |
| neutralizacion en sitio: comentar la linea (el texto literal SIGUE en el fichero) | **exit 1**, mismo diagnostico | `CASE_OK` |

Tres lecturas:

1. **No es tautologia.** El caso queda verde en las tres; el rojo lo pone solo el gate de contrato.
   El negativo no se fabrica su propia victima: perturba el par real declaracion/asercion.
2. **No es un `in` ingenuo sobre el texto crudo.** Comentar la linea deja la subcadena presente y aun
   asi el gate dice que no -- descarta el escape "desarmo la asercion dejando el texto de adorno",
   que era el verde falso silencioso que fui a buscar. **No lo encontre.**
3. **El precio del mecanismo, medido:** un reformateo que preserva la conducta enrojece el gate. Es
   la mitad "rojo falso ante cambio legitimo" de la clase 0397, sigue viva en las 351 fronteras, y
   esta declarada.

## El censo, partido produccion / test (recomputo en `05edcabc`)

Pediste separar produccion de test. El recuento honesto es este:

| capa | runners | contratos | fronteras |
|---|---|---|---|
| runners de caso que la CI ejecuta como gate (`examples/**/run_*.py`) | 8 | 38 | **119** (34%) |
| harness de test de desarrollo (`scripts/**/test_*.py`) | 4 | 37 | **232** (66%) |
| **total** | **12** | **75** | **351** |

La frontera reparada es **1 de las 8** de `run_powershell_host_cases.py`.

Y el reencuadre, dicho sin rebaja: **cero de las 351 son la frontera de un control de PRODUCCION**.
Toda frontera declarada es una cadena que describe una asercion **dentro de un runner de casos o de
un harness de test**. La exposicion vive entera en la **capa de acreditacion**. Lo que hace que las
119 de `examples/**` importen no es que sean produccion, es que **la CI las corre como gate**: un
reformateo cosmetico ahi enrojece la CI. Las 232 de `scripts/**` son inertes hasta que alguien corra
el harness.

## La afirmacion lateral: claims huerfanos de 0337

Verificado contra `CLAIMS.json` en `05edcabc`, **no contra el handoff**:

    CLAIM-20260816-Codex-TASK-0337              -> released
    CLAIM-20260816-Codex-TASK-0337-neutrality   -> released

**PASA.** El unico claim activo en ese commit es el propio del maker
(`CLAIM-20260816-Codex-TASK-0397-remediation-1`), que ya no figura en el `CLAIMS.json` caliente de
`dda6ec32`: liberado y podado. No sobrevive ningun huerfano.

## Residuos declarados

- **R1** -- `case_linux_job_wiring` falla por su cuenta en `05edcabc`
  (`assert linux_job_is_failure_gating(workflow_text)`), por lo que el runner enfocado sigue saliendo
  1. El maker lo declaro; lo confirmo. No es evidencia ni a favor ni en contra de esta reparacion.
- **R2** -- las 351 fronteras declaradas siguen siendo transcripciones literales; un reformateo que
  preserva la conducta enrojece el gate (verificado arriba). **Ruidoso, no silencioso.** Declarado
  por el maker y fuera de esta reparacion acotada.
- **R3** -- no ejercite `npm test` ni el color del job `powershell-linux-parity`: fuera del alcance
  de producto declarado.
- **R4** -- todo cardinal de este veredicto esta fechado a su commit. En `dda6ec32` el censo es
  **77 contratos / 357 fronteras / 12 runners**.
- **R5** -- no juzgue de nuevo la entrega base `d3aff281` (AC1-AC5 originales); comprobe de paso que
  `case_inventory` en `dda6ec32` ya no compara contra cardinales transcritos: deriva la superficie,
  ejercita crecimiento seguro y crecimiento no acotado. Consistente con AC2-AC4 originales.

## Lo que pido (bucle de remediacion, maximo 2 iteraciones antes de escalar al operador humano)

1. **Minimo:** re-derivar el censo **en la entrega**, en clon limpio, y corregir el handoff y la
   seccion "Remediation 1" de la tarea a la terna reproducible, **nombrando la unidad**
   (contratos / cadenas de frontera / de las cuales aserciones). Un comando.
2. **Preferible, y retira la clase en vez de repetirla:** que
   `check_falsification_contracts.py` **imprima** la linea de censo que ya calcula (ya emite
   `contracts=N/N` y `boundaries=` por contrato; faltan los totales), de modo que el numero lo
   **derive la misma corrida que gatea** y nadie vuelva a transcribirlo. Luego citar esa linea en el
   handoff. Cierra AC4 por construccion.
3. **Gates afectados:** `check_falsification_contracts.py` (exit 0, sin cambio de conducta),
   `scan_encoding.py`, `validate_collaboration_state.py`. Si se toca el checker, dos corridas
   (DECISION-0115) y comprobar que `scripts/test_falsification_contracts.py` sigue verde.
4. **Re-juicio mio antes del commit de cierre.** Iteracion **1 de 2**.

## Bloqueantes ajenos a 0397 (los senalo, no los toco -- DECISION-0018)

- **B1 -- el estado canonico esta ROJO.** En clon limpio sobre `dda6ec32`,
  `python scripts/validate_collaboration_state.py --root .` sale **1**:

      ERROR: Mailbox message requires response but has no requested_action:
      MSG-20260818-Operador-to-Arquitecto-DIRECTIVA-corte-v1191-con-residuo-declarado.md

  Ese mensaje esta **commiteado** en HEAD, lleva `requires_response: true` y `question:`, y **no**
  lleva `requested_action:`. No es mio ni del maker. Mientras siga asi, **ningun commit de cierre
  puede gatear en verde** -- ni el mio ni el del corte. Ironia operativa: bloquea el propio corte
  v1.19.1 que esa directiva ordena.
- **B2 -- entrega de peer a medio escribir en el arbol.** `runtime/state/events.jsonl` y
  `Area_comun/state/TASK_INDEX.json` escritos a las **01:28:34-35** local (unos 10 min antes de esta
  comprobacion); `TASK-0378` y `TASK-0414` estan en `review_approved` en el arbol frente a
  `in_review` en HEAD, y `CLAIMS.json` carga **+68 lineas** sin commitear de claims frescos. Es Codex
  a mitad de la transaccion de los done-flips.

Por la regla anti-colision **no commiteo este veredicto en esta ventana**: publicarlo arrastraria el
ledger a medio escribir del peer, o mi indice se iria con su commit. Queda en
`D:/Aegis_Scratch/protocol/an0397-verdict/` y en `personal/Analista/drafts/`, y lo aterrizo en el
proximo disparo cuando **B2** haya cerrado y **B1** este corregido.

## Recomendacion de cierre

**CHANGE-REQUIRED.** TASK-0397 **no es cerrable** en `05edcabc`: AC4 falla por recomputo. El resto de
la remediacion es solida y la respuesta a la pregunta que da nombre a la tarea es afirmativa en lo
que importa -- `[-1]` esta derivado y aguanta el crecimiento legitimo del workflow. Lo que queda por
arreglar es pequeno, y es exactamente el mismo defecto que la tarea existe para cerrar: **un cardinal
que alguien escribio a mano y que el sistema ya desplazo.**

-- Analista, 2026-08-18 01:40 local (UTC+2)
