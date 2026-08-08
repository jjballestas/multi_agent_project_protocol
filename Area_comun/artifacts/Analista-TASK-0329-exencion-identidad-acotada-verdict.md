---
artifact: Analista-TASK-0329-exencion-identidad-acotada-verdict
task_id: TASK-0329
reviewer: Analista
role: checker (adversarial, independent)
created_at: 2026-08-08
local_time: 2026-08-08 06:52 (+02:00)
anchor_commit: bd664a864cbf71b489a92047b45ae4f641d4b7e7
protocol_head_at_review: 8a6cc313
verdict: CHANGE-REQUIRED
---

# TASK-0329 -- la exencion se acoto en UN escaner de los DOS

## Resumen en una linea

El acotamiento del escaner Python es solido y lo he intentado romper por cinco vias sin
conseguirlo: los diez ficheros cazan una fuga fuera de sus lineas declaradas, las 91 exenciones
declaradas corresponden una a una a una ocurrencia real (cero exenciones muertas), y el negativo
nuevo mata tambien las tres formas de CODIGO MUERTO que le construi. **Pero
`scripts/scan_domain_neutrality.ps1` -- el gemelo en paridad declarada por DECISION-0006, que CI
ejecuta en `validate.yml:267` y que `scripts/new_instance.py:90` copia a TODA instancia nueva --
conserva intacta la allowlist por FICHERO COMPLETO, con el mismo comentario justificativo.** La
exencion del tamano de un fichero no se cerro: se cerro en la mitad del gate que no se exporta.
**CHANGE-REQUIRED.**

**Respuesta a tu pregunta.** Los otros ocho quedaron **acotados de verdad**, no declarados a mano
ondulada: cada uno cazo mi fuga inyectada, y ninguno arrastra exenciones sobrantes. Ese era el AC3 y
ese lado aguanta. Lo que no aguanta es que la misma pregunta, hecha al escaner PowerShell, tiene la
respuesta contraria para los diez.

## Anclaje canonico y reproduccion

Clon limpio en `D:/Aegis_Scratch/hub/rev0329/cc`, `git checkout bd664a86`, arbol vacio.
Gates recomputados POR EXIT CODE en el clon, nunca en caliente:

    python scripts/scan_domain_neutrality.py --root .                 -> exit 0
    python scripts/test_scan_domain_neutrality.py                     -> exit 0   (4/4 OK)
    python scripts/check_falsification_contracts.py --root .          -> exit 0
    python scripts/check_falsification_contracts.py --root .
        --workflow .github/workflows/validate.yml                     -> exit 0   (54/54, missing=0)
    python scripts/test_falsification_contracts.py                    -> exit 0
    python scripts/validate_collaboration_state.py --root .           -> exit 0
    python scripts/scan_encoding.py --root .                          -> exit 0
    powershell scripts/scan_domain_neutrality.ps1 -Root .             -> exit 0
    protocol_state_drift(Path('.'))   has_drift=False                 -> exit 0
    git status --porcelain (clon)                                     -> vacio

AC5 (sin regresion, sin falso positivo nuevo sobre el arbol actual): **PASA**. Ambos escaneres dan
exit 0 sobre el arbol limpio.

Los vectores se ejercitan en una copia de trabajo del clon (`rev0329/probe`, sin `.git`), inyectando
y restaurando el fichero original en cada iteracion; la copia vuelve a exit 0 al final de cada
bloque.

## Vector por vector

| # | Vector | Resultado |
|---|--------|-----------|
| A | Fuga de identidad en linea NO declarada, en cada uno de los 10 ficheros (escaner Python) | **PASS** 10/10 exit 1 y nombrada |
| A2 | Termino DISTINTO del exento, en la MISMA linea declarada | **PASS** 4/4 exit 1 y nombrada |
| A3 | MISMO termino, texto de fuga NUEVO, sobre la linea declarada | **SLIP declarado** exit 0 (residual R1, admitido por AC2) |
| A4 | Exenciones declaradas que no corresponden a ninguna ocurrencia real | **PASS** 91 triples, 0 muertas |
| B | Inventario de lo que destapo el acotamiento | **PASS** ningun fichero fuente tocado; todo declarado, nada limpiado en silencio |
| C | La exencion legitima (CLI de proveedor) sigue viva | **PASS** arbol limpio exit 0 en ambos escaneres |
| D | Mutantes de CODIGO MUERTO contra el negativo nuevo | **PASS** 3/3 formas muertas, mas el control |
| E | Movimiento de linea | **PASS** falla cerrado; coste declarado como R2 |
| **F** | **Gemelo PowerShell del mismo gate** | **SLIP BLOQUEANTE** 10/10 ciego |

### A -- los diez ficheros, uno a uno (esto es el AC3)

Anado `# DEFAULT_COORDINATOR = "Arquitecto"` al final de cada fichero antes exento (linea nunca
declarada) y recomputo el gate Python:

    runtime/apply.py                        L578    exit 1   nombrada
    runtime/budget.py                       L300    exit 1   nombrada
    runtime/context.py                      L229    exit 1   nombrada
    runtime/eventlog.py                     L1391   exit 1   nombrada
    runtime/ledger_ops.py                   L362    exit 1   nombrada
    runtime/metrics.py                      L345    exit 1   nombrada
    runtime/router.py                       L576    exit 1   nombrada
    scripts/harness/peer_mailbox_cron.ps1   L1520   exit 1   nombrada
    scripts/memory/test_memory_db.py        L2217   exit 1   nombrada
    scripts/prune_state.py                  L692    exit 1   nombrada

El conjunto de claves del diccionario nuevo es identico al de la lista vieja: no se perdio ni se
colo ningun fichero por el camino.

### A2 -- la exencion es por TERMINO, no solo por linea

    runtime/apply.py:440           exento codex     inyecto Arquitecto  -> exit 1  nombrada
    runtime/budget.py:68           exento analista  inyecto Codex       -> exit 1  nombrada
    peer_mailbox_cron.ps1:9        exento codex     inyecto Arquitecto  -> exit 1  nombrada
    runtime/router.py:120          exento operador  inyecto Codex       -> exit 1  nombrada

### A4 -- ninguna exencion sobra (esto es lo que hace honesto al AC3)

Resolvi los cinco digests contra los terminos de identidad que el propio escaner deriva de
`protocol.config.json` -- `Analista`, `Arquitecto`, `Codex`, `operador`, `operador humano` -- y
comprobe cada triple `(fichero, linea, termino)` contra el contenido real de esa linea en
`bd664a86`, con el mismo patron de frontera de palabra que usa el escaner:

    triples declarados = 91
    triples cuya linea NO contiene el termino declarado = 0

Esto importa mas de lo que parece: una exencion declarada sobre una linea que hoy no la necesita es
un agujero pre-autorizado esperando a que alguien escriba ahi. No hay ninguno. La superficie exenta
es exactamente el conjunto de ocurrencias preexistentes, ni un hueco de mas.

### B -- no hubo limpieza silenciosa

`git show --stat bd664a86` no toca ninguno de los diez ficheros fuente: solo el escaner, su test,
estado y la ficha. Combinado con A4, la conclusion es firme: **todo lo que el acotamiento destapo
quedo DECLARADO como exencion con su razon, y nada se arreglo en masa por detras.** Es literalmente
lo que el AC3 pedia.

### C -- la exencion legitima sigue viva

Arbol limpio, exit 0 en ambos escaneres: las nueve ocurrencias del nombre de proveedor en
`peer_mailbox_cron.ps1` (lineas 9, 420, 427, 437, 446, 447, 454, 470, 1337) siguen exentas y su
vecindario ya no (vector A: L1520 se caza). El gate no se vuelve ruidoso y nadie tendra motivo para
desactivarlo por esta via.

### D -- el mutante de codigo muerto (la forma que se escapo en 0324)

Construi tres mutantes que dejan `is_identity_literal_exempt` PRESENTE en el fuente pero sin efecto,
mas el control declarado por el propio contrato, y corri la suite entera contra cada uno:

    D1  skip por fichero completo ANTES de la guarda estrecha (guarda inalcanzable) -> KILLED
    D2  la funcion corta a `return True` en cuanto el fichero esta declarado        -> KILLED
    D3  identity_scan_path devuelve False para los ficheros exentos                 -> KILLED
    D0  control: revertir a la regla por fichero (la mutacion que el test declara)  -> KILLED

Los cuatro mueren por la asercion de BASELINE del negativo nuevo, no por su mutacion: el test exige
que `peer_mailbox_cron.ps1:10` aparezca en la salida del escaner **real** antes de mutar nada. Esa
asercion es la que ata el EFECTO y no la forma, y es lo que le faltaba a 0324. En los cuatro casos
el gate sobre el arbol limpio sigue en exit 0, asi que ninguno se delata por ruido: mueren porque el
contrato mira el comportamiento correcto.

El contrato ademas se EJECUTA, no solo se declara: `validate.yml:263` corre
`scripts/test_scan_domain_neutrality.py`, y el inventario con `--workflow` da 54/54 y `missing=0`.

### F -- SLIP BLOQUEANTE: el gemelo PowerShell conserva la exencion por fichero

`scripts/scan_domain_neutrality.ps1` no aparece en el commit. Sigue teniendo, en su linea 6, la
lista literal de los diez ficheros -- con el mismo comentario, palabra por palabra: *"The
provider-name collision refers to a third-party CLI, not a protocol agent"* -- y la sigue aplicando
por fichero completo en su linea 172:

    if (-not (Test-IdentityScanPath ...) -or $LegacyIdentityLiteralFiles -contains $file.RelativePath) {
        continue
    }

Es la linea que TASK-0329 existe para borrar, viva.

Falsado por comportamiento, misma fuga, mismo arbol, los dos escaneres a la vez:

    fichero (fuga anadida en linea no declarada)      PY    PS1
    runtime/apply.py                                   1      0
    runtime/budget.py                                  1      0
    runtime/context.py                                 1      0
    runtime/eventlog.py                                1      0
    runtime/ledger_ops.py                              1      0
    runtime/metrics.py                                 1      0
    runtime/router.py                                  1      0
    scripts/harness/peer_mailbox_cron.ps1              1      0
    scripts/memory/test_memory_db.py                   1      0
    scripts/prune_state.py                             1      0

Diez de diez. El caso concreto que abre la ficha -- `$DefaultCoordinator = "Arquitecto"` en el
fichero donde TASK-0316 corrigio la fuga -- da `PY_EXIT=1` con la fuga nombrada y `PS1_EXIT=0` con
cero hallazgos que nombren el fichero.

**Por que esto no es cosmetico:**

1. **DECISION-0006 declara PARIDAD explicita** entre los dos escaneres ("Scripts
   `scan_domain_neutrality.py` y `.ps1` (paridad)") y dice que CI tiene ambos runtimes instalados
   "precisamente para que la paridad se ejercite de verdad, no se saltee". La paridad esta rota hoy,
   en el eje exacto de esta tarea.
2. **Se exporta.** `scripts/new_instance.py:90` copia el `.ps1` a toda instancia nueva y su linea
   175 lo cablea en el CI generado. Cada instancia creada desde `bd664a86` nace con la exencion del
   tamano de un fichero dentro.
3. **El AC2 no se cumple en esa mitad.** "La exencion deja de ser por archivo": en el `.ps1` sigue
   siendo por archivo. El AC4 tampoco: no hay ningun negativo que mate la regla por fichero del
   `.ps1` -- lo acabo de demostrar dejandolo ciego diez veces con la suite en verde.
4. **El test de paridad no lo ve.** `test_powershell_scanner_matches_required_coverage_when_available`
   solo comprueba cuatro rutas sonda, ninguna de ellas un fichero exento. Es un test de cobertura de
   globs, no de semantica de exenciones.

Atenuante que declaro honestamente: en **este** repo CI corre ambos pasos, asi que una fuga real
seguiria poniendo CI en rojo por el paso Python. El gate compuesto del hub no esta ciego. Lo que
esta ciego es el escaner que se envia, y la propiedad que AC2/AC3/AC4 prometen sobre el. Es
exactamente el patron de DECISION-0105 reaparecido dentro de su propia correccion: **el alcance del
arreglo es mas estrecho que el alcance del defecto.**

## Residuales declarados

- **R1 (admitido por AC2, no bloqueante).** La exencion es `(linea, termino)`: sustituir el
  contenido de una linea declarada por una fuga NUEVA del MISMO termino sigue siendo invisible.
  Falsado: `runtime/apply.py:440` reescrita como `# DEFAULT_IMPLEMENTER = "Codex"` -> exit 0;
  `peer_mailbox_cron.ps1:420` idem -> exit 0. El AC2 admite explicitamente granularidad de linea, asi
  que lo declaro como residual, no como fallo. La superficie cayo de fichero entero a una linea y un
  termino; la forma del patron sobrevive a esa escala.
- **R2 (coste operativo).** Fallar cerrado ante movimiento de linea es correcto pero caro: insertar
  UNA linea al principio de `scripts/memory/test_memory_db.py` produce **58 hallazgos** de golpe;
  en `runtime/router.py`, 4. Es el riesgo que nombras en el foco C por otra puerta: un gate que se
  pone rojo por un cambio inocuo invita a que alguien lo relaje. No pido cambiarlo -- pido que quede
  escrito, porque el siguiente que edite ese fichero se lo va a encontrar.
- **R3 (auditabilidad).** Las exenciones se declaran por digest SHA-256. La eleccion es correcta (en
  claro, el escaner se auto-delataria: se escanea a si mismo bajo `scripts/**.py`), pero un humano
  leyendo `{17: (_EXEMPT_TERM_4, _EXEMPT_TERM_5)}` no puede saber que identidad esta exenta sin
  computar hashes. La razon escrita por fichero mitiga a medias; por linea no hay ninguna.
- **R4 (arrastrado).** `scope_routes` de la ficha lista
  `Area_comun/protocol/FALSIFICATION_CONTRACTS.json`, que no existe en el arbol: el registro real
  vive en la tupla `FALSIFICATION_CONTRACTS` dentro del propio fichero de test. La ruta declarada
  esta obsoleta; no afecta al fondo.

## Veredicto

**CHANGE-REQUIRED.**

AC1, AC2 (Python), AC3 (Python), AC4 (Python) y AC5 pasan, y pasan bien: el lado Python es de los
acotamientos mas limpios que he revisado -- cero exenciones muertas, cero limpieza silenciosa, y un
negativo que mata las tres formas de codigo muerto que le lance. No es eso lo que bloquea.

Bloquea que el mismo gate tiene dos implementaciones en paridad declarada, que solo se corrigio una,
y que la que no se corrigio es la que se copia a cada instancia nueva. El defecto de la ficha --
"exencion del tamano de un fichero" -- sigue en el arbol, en `scan_domain_neutrality.ps1:6` y
`:172`, con su justificacion original intacta.

## Bucle de correccion esperado

- **Remediacion 1:** acotar `scripts/scan_domain_neutrality.ps1` con la misma semantica
  `(fichero, linea, termino)` que el Python, **y** anadir un negativo que mate la regla por fichero
  en el `.ps1` -- el test de paridad actual no lo caza, asi que la remediacion debe incluir su propia
  falsacion, no apoyarse en la existente. Si se decide que el `.ps1` deja de ser un gate en paridad,
  eso es un cambio de DECISION-0006 y necesita DECISION, no un borrado.
- **Gates afectados:** `scan_domain_neutrality.py` + `.ps1` (ambos exit 0 en arbol limpio),
  `test_scan_domain_neutrality.py`, `check_falsification_contracts.py --workflow`,
  `validate_collaboration_state.py`, `scan_encoding.py`, drift 0.
- **Re-juicio por mi antes del commit de cierre.** Repetire la tabla de diez ficheros con los DOS
  escaneres y exigire `PY=1 / PS1=1` en las diez filas, mas mutacion del negativo nuevo del `.ps1`.
- **Maximo 2 iteraciones** antes de escalar al operador humano.

-- Analista
