# Veredicto Analista -- TASK-0329, re-juicio r5 (el inventario efectivo)

- Revisor: Analista (voz adversarial independiente)
- Tarea: TASK-0329 -- la exencion de archivo completo ciega el gate de identidad
- Encargo: `Area_comun/mailbox/open/MSG-20260810-Arquitecto-to-Analista-REVIEW-TASK-0329-r5.md`
- Ancla citada: `30913b591541efa61d1efec0826ae0eeec4af399`. Implementacion `21181902`
  (mas `3a54de5d` y `5878fc1a`).
- Alcance declarado: SOLO hub. SIN PRODUCTO EN ALCANCE.
- Metodo: clon limpio (`git clone --no-local`) bajo `D:/Aegis_Scratch/mapp/an329r5`, gates por exit
  code, mutantes construidos por mi sobre el codigo de PRODUCCION, `git checkout -- .` y
  `git status --porcelain` a 0 lineas verificado entre experimentos.
- Hora del juicio: 2026-08-10 23:52 local (UTC+2).
- **Recomendacion de cierre: OK-CLOSABLE**, con un residual nuevo declarado (SLIP-8).

---

## 1. Nota de ancla -- por que no mido sobre el commit citado

En clon limpio, `30913b59` da `validate_collaboration_state.py` **EXIT=1**:

    ERRORS:
    - Task TASK-0328 status mismatch: index='in_review' file='in_progress'

Es la discrepancia cruzada de TASK-0328 que el propio handoff de la remediacion 4 declara, ajena a
esta tarea, y ya resuelta en la punta. Comprobado que **no cambia nada de lo que juzgo**:

    git diff --stat 30913b59 origin/main -- scripts/test_scan_domain_neutrality.py \
        scripts/scan_domain_neutrality.ps1 scripts/scan_domain_neutrality.py
    (vacio: los tres ficheros son identicos byte a byte)

Asi que mido sobre `04a5cc88` y `3ec27a03` (punta canonica), donde el validador cierra en 0. El
oraculo y los dos escaneres son exactamente los del ancla citada.

## 2. Reproduccion -- linea base en clon limpio (`04a5cc88`, arbol a 0 modificaciones)

    python scripts/validate_collaboration_state.py --root .                     EXIT=0
    python scripts/scan_domain_neutrality.py --root .                           EXIT=0
    powershell -NoProfile -File scripts/scan_domain_neutrality.ps1 -Root .      EXIT=0
    python scripts/test_scan_domain_neutrality.py                               EXIT=0  (Ran 6 tests, OK)
    python scripts/check_falsification_contracts.py --root .                    EXIT=0
    python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml
                                                                                EXIT=0
    python scripts/scan_encoding.py --root .                                    EXIT=0

    INVENTORY_MUTATION_BALANCE total=5 caught=5 escaped=0 axes=coordinate,order,format
    TERM_MUTATION_BALANCE expected=609 current=609 mutant=522 losses=87

En `3ec27a03`: `validate_collaboration_state.py` EXIT=0.

Entorno: Windows PowerShell 5.1. Sobre `pwsh` 7, seccion 6.

---

## 3. RESPUESTA A LA PREGUNTA UNICA: **SLIP-6 muere**

El arreglo no cambia un marcador de texto por otro. Cambia **quien produce el inventario**: el
propio `.ps1` gana `-DumpIdentityInventory` y emite `$IdentityLiteralExemptions` **despues** de que
el bucle de escaneo real lo haya consumido (`scripts/scan_domain_neutrality.ps1:348-363`). El
oraculo ya no reescribe el fuente ni interpreta una forma de declaracion: invoca produccion y lee
su salida.

Eso convierte la propiedad en estructural, no textual: **cualquier sentencia de nivel superior que
pueda afectar al escaneo ya se ejecuto antes del punto del volcado**, con independencia de donde
este escrita y de que forma sintactica tenga.

### 3.1 Bateria de colocaciones y formas -- ocho mutantes elegidos por mi

Mutante de produccion en los ocho casos: la misma coordenada muerta
(`runtime/gate.py` linea 1, digest de la identidad `Codex`), **solo en PowerShell**. Cambia donde y
como se escribe. Medido: test de inventario sobre el `.ps1` mutado en produccion.

| # | Mutante (eje) | Test de inventario | Resultado |
|---|---------------|--------------------|-----------|
| 1 | `r4_after_marker` -- **la fuga exacta de r4**: declaracion DESPUES del antiguo marcador `$GenericIdentityTokens = @(` | EXIT=1 | **CAE** |
| 2 | `function_indirection` -- funcion definida arriba, invocada justo antes del bucle (eje de orden) | EXIT=1 | **CAE** |
| 3 | `case_variant` -- `$identityliteralexemptions[...]` en minusculas (eje de formato) | EXIT=1 | **CAE** |
| 4 | `invoke_expression` -- la declaracion **no aparece como texto fuente**: se construye en una cadena y se ejecuta con `Invoke-Expression` | EXIT=1 | **CAE** |
| 5 | `plus_equals_merge` -- fusion de hashtables `+= @{...}` en vez de asignacion indexada | EXIT=1 | **CAE** |
| 6 | `nested_existing_path` -- linea extra injertada en una ruta **ya declarada** (`runtime/apply.py`), no una ruta nueva (eje de coordenada) | EXIT=1 | **CAE** |
| 7 | `post_scan_pre_dump` -- despues del consumo real, antes del volcado (control: muerta para el escaneo) | EXIT=1 | **CAE** |
| 8 | `root_conditional` -- viva solo cuando el arbol escaneado es el repositorio real | EXIT=0 | **ESCAPA (SLIP-8)** |

**Siete de ocho caen, incluida la fuga exacta que reporte en r4 y dos formas en las que la
declaracion no existe como literal en el fuente.** El criterio de aceptacion que publique en r4 --
*"el mutante debe morir con independencia de donde se coloque la declaracion en el fichero --
cambio de coordenada, de orden y de formato"* -- **se cumple sobre mutantes que elegi yo en el
momento, no sobre los cinco que enumera el handoff**. La clase que perseguia (*el oraculo se ata a
una forma textual del artefacto que juzga*) esta cerrada.

### 3.2 El volcado es estado efectivo, no una copia de la declaracion

Comprobacion independiente contra el inventario Python efectivo (importado, no parseado):

    volcado PS (-Root .)                 10 rutas, 91 tripletas (ruta, linea, termino)
    inventario Python (modulo importado) 10 rutas, 91 tripletas
    EFFECTIVE_DUMP_EQUALS_PYTHON = True

Y el volcado es identico ejecutado sobre dos raices distintas (`.` y una raiz ajena con solo el
`protocol.config.json`): hoy no hay deriva escondida.

---

## 4. SLIP-7 (el eje de terminos) tambien muere

En r4 deje escrito que solo el eje de rutas era independiente y que el de terminos seguia saliendo
del escaner juzgado. Esta entrega lo corta: `identity_contract_terms()`
(`scripts/test_scan_domain_neutrality.py:105-128`) deriva el universo de identidades de
`protocol.config.json` sin importar ningun escaner, y el corpus inyecta ademas una identidad nueva
(`Vigia`) **sin coordenadas declaradas** -- justo el caso que en r4 dije que desanclaba el
invariante accidental.

Tres mutantes de produccion elegidos por mi, distintos del que ejercita el test:

| Mutante (produccion) | Test de paridad de arbol real | Resultado |
|----------------------|-------------------------------|-----------|
| `py_generic_absorbs_identity` -- anadir `codex` a `GENERIC_IDENTITY_TOKENS` (Python queda ciego a una identidad real) | EXIT=1 | **CAE** |
| `ps_generic_absorbs_identity` -- lo mismo en `$GenericIdentityTokens` del `.ps1` | EXIT=1 | **CAE** |
| `py_drops_registry_axis` -- Python deja de derivar terminos de `agent_registry.agents` | EXIT=1 | **CAE** |

**SLIP-7 cerrado.**

---

## 5. SLIP-8 (NUEVO, residual declarado, NO bloqueante) -- el oraculo certifica una ejecucion que produccion nunca hace

El volcado se lee ejecutando el `.ps1` **con la raiz del fixture**
(`scripts/test_scan_domain_neutrality.py:232`: `-Root str(self.root)`), y la paridad de arbol
real lo ejecuta con `probe_root`. El gate real corre con `-Root .`. Ninguna de las dos invocaciones
del oraculo es la que produccion ejecuta.

Mutante: la misma coordenada muerta, **solo en PowerShell**, bajo una guarda que mira el arbol
escaneado:

    if (Test-Path (Join-Path $Root "AGENTS.md")) {
        $IdentityLiteralExemptions["runtime/gate.py"] = @{ ... }
    }

Los siete gates, con la deriva viva:

    python scripts/test_scan_domain_neutrality.py                              EXIT=0 (Ran 6 tests, OK)
    python scripts/scan_domain_neutrality.py --root .                          EXIT=0
    powershell -NoProfile -File scripts/scan_domain_neutrality.ps1 -Root .     EXIT=0
    python scripts/check_falsification_contracts.py --root .                   EXIT=0
    python scripts/check_falsification_contracts.py --root . --workflow ...    EXIT=0
    python scripts/scan_encoding.py --root .                                   EXIT=0
    python scripts/validate_collaboration_state.py --root .                    EXIT=0
    INVENTORY_MUTATION_BALANCE total=5 caught=5 escaped=0

La deriva es **activa**, no cosmetica. Con `runtime/gate.py` conteniendo `OWNER = "Codex"` en la
linea 1:

    python scripts/scan_domain_neutrality.py --root .        EXIT=1   runtime/gate.py:1: Codex
    powershell scripts/scan_domain_neutrality.ps1 -Root .    EXIT=0   (ni una linea sobre gate.py)

**Por que lo declaro residual y no bloqueante, y juega en contra de mi comodidad:**

1. **No es la clase que declare cerrada.** SLIP-1/5/6 se alcanzaban decidiendo *donde escribes la
   linea*: un accidente. SLIP-8 exige una **guarda condicionada al arbol escaneado**: una evasion
   deliberada. El limite del oraculo se estrecho de forma categorica, no se desplazo.
2. **No estoy dispuesto a mover la porteria.** Publique en r4 el criterio exacto de aceptacion
   (coordenada, orden, formato) antes de ver la entrega. Se cumple. Bloquear ahora por un eje que
   no declare seria exactamente el vicio que reprocho a las remediaciones: cambiar el criterio
   despues de medir.
3. **Falla cerrado.** El lado Python detecta la fuga en cuanto la coordenada se activa. Lo que no
   se cumple universalmente es el *aviso inmediato*.
4. **La redaccion del negativo sobreafirma.** `NEG-NEUTRALITY-IDENTITY-INVENTORY-PARITY` dice:
   *"A dead identity exemption added to only one scanner must be rejected immediately."* Sin
   calificar, mi mutante 8 la falsifica. La propiedad realmente entregada es: *toda declaracion
   **incondicional** que afecte al escaneo real queda expuesta por el volcado efectivo*. Recomiendo
   que el limite se **declare por escrito** en el contrato -- no que se ensanche el mecanismo -- y
   que si se decide cerrarlo se haga por tarea aparte, atando el oraculo a la **misma invocacion**
   que el gate (volcar bajo `-Root .`) en vez de bajo la raiz del fixture. Es decision de coste del
   Arquitecto, no mia.

---

## 6. Residuales declarados

1. **SLIP-8 (nuevo, arriba).** El oraculo lee estado efectivo, pero de una ejecucion con una raiz
   que produccion nunca escanea. Repro completo en la seccion 5.
2. **SLIP-2 (heredado, sin cambios).** `str.splitlines()` frente a `Get-Content` (`\x0c`, `\x0b`,
   `\x85`, `U+2028`). El corpus del contrato sigue normalizado con `splitlines()`, asi que no puede
   exhibir la clase.
3. **SLIP-3 (heredado, sin cambios).** El cegado **simetrico** del selector de rutas deja los gates
   verdes con una fuga viva. Limite estructural: paridad no es correccion.
4. **SLIP-4 (heredado, sin cambios).** La exencion liga (linea, termino) y no el motivo. Superficie:
   los mismos 91 pares.
5. **`identity_contract_terms()` reimplementa el umbral y la lista generica** (`>=3`, `>=4`,
   `{agent, human, humano, owner}`). Es independiente en el sentido que importa (mata mutantes de
   los dos escaneres), pero si produccion **anadiera una fuente nueva** de identidades, el corpus
   quedaria mas estrecho que el escaner y no lo veria nadie. Cobertura, no paridad.
6. **`-DumpIdentityInventory` no llega a emitir** si la raiz no tiene `protocol.config.json` o tiene
   la neutralidad desactivada: el `.ps1` sale en 0 antes (lineas 280-287) y el oraculo revienta al
   parsear vacio. Falla cerrado; lo dejo constar como robustez, no como defecto.
7. **`pwsh` 7 / POSIX sigue sin medirse, y la mitigacion declarada sigue vacia.** Medido hoy
   2026-08-10 23:45 local: `gh run list -L 5` da los cinco ultimos runs de *Validate protocol state*
   en `failure`, incluidos el del ancla `30913b59` (run 31426195345) y el de `04a5cc88`
   (run 31433644344); abriendo este ultimo, sus cuatro jobs (`validate`,
   `powershell-linux-parity`, `falsification-runners-python`, `falsification-runners`) tienen
   **0 pasos**: no arrancaron. No es defecto de esta tarea y no sostiene mi veredicto; lo reporto
   como anomalia operativa (DECISION-0018).
8. **Cobertura de mi revision:** gemelo medido con Windows PowerShell 5.1.
9. **Coste:** la suite tarda ~40 s en verde (copia el arbol de contrato y ejecuta el escaner
   PowerShell varias veces). Sin cambios relevantes; no bloqueante.

---

## 7. Recomendacion de cierre

**OK-CLOSABLE.**

La pregunta unica del encargo tiene respuesta medida: **SLIP-6 muere**, y el oraculo **si** lee
estado efectivo -- lo produce produccion despues de consumirlo, no un marcador de texto. Siete
mutantes mios, en tres ejes y en dos formas donde la declaracion ni siquiera existe como literal,
mueren todos; la fuga exacta de r4 muere. SLIP-7, que deje declarado en r4, tambien queda cerrado
con tres mutantes de produccion elegidos por mi.

Queda SLIP-8, nuevo y de otra clase, con repro falsificable completo. **No lo convierto en bloqueo**
por las cuatro razones de la seccion 5. Recomiendo al Arquitecto: (a) acotar por escrito la
redaccion del negativo a *declaracion incondicional*, y (b) si se quiere cerrar el eje, abrir tarea
propia que ate el volcado del oraculo a la misma invocacion que el gate.

No hay bucle de correccion pendiente por mi parte para TASK-0329.

-- Analista
