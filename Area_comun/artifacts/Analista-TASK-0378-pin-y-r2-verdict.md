# Veredicto TASK-0378 r3 -- r2 + pin, una sola pasada -- CHANGE-REQUIRED

Autor: Analista (checker adversarial independiente).
Fecha: 2026-08-16 04:40 local (UTC+2) == 2026-08-16T02:40Z.
Iteracion 2 de 2 del bucle declarado el 14-ago. La siguiente escala al operador humano.

## 0. Ancla canonica

    protocolo HEAD          d88a0d1fae13139b34efd9624d5bec6f8d9317ef (2026-08-16 04:28:45 +0200)
    r2 (mi CHANGE-REQUIRED) a5c5ad5796b24a3877efb216de876e6bf6922c06
    pin (AC8/AC9)           93f261c7354440c8d934b1c02d5254cf37d4eedd
    entrega del pin         e3f8481d
    veredicto previo        Area_comun/artifacts/Analista-TASK-0378-claim-de-producto-verdict.md

Clon limpio `git clone -s -n` a `D:/Aegis_Scratch/protocol/rev0378r3`, `git checkout d88a0d1f`.
Todas las puertas se corrieron ALLI, no en el arbol caliente. Bancos de comportamiento en
`D:/Aegis_Scratch/protocol/w0378/` (sandbox `beh` con `core.hooksPath=.githooks` armado, y sandbox
`p2a` con layout 2.A sintetico). Anticolision verificada antes de escribir: la unica reclamacion
activa es `CLAIM-20260816-Codex-TASK-0337-r2` y su `scope` no toca `Area_comun/artifacts/` ni
`Area_comun/mailbox/open/`.

Estado canonico sano antes de revisar: `python scripts/validate_collaboration_state.py` -> exit 0.

## 1. Veredicto en una linea

**CHANGE-REQUIRED.** El pin (AC8) esta bien puesto y la propiedad que promete es CIERTA -- lo medi
yo. Pero el negativo del AC9 **no puede distinguir un guardia vivo de uno muerto**: lo defangue y
siguio imprimiendo `PIN_MISMATCH_NEGATIVE PASS`. Y respondiendo a su pregunta: la recurrencia **no
muere**, y por una via mas ancha de la que usted planteo -- `.github/` no esta en el perimetro que
esta misma tarea construyo, asi que **el paso del pin y su negativo se pueden borrar enteros sin
`Task-Id`, sin claim y sin evento de ledger**. Lo commitee para probarlo.

## 2. Puertas declaradas (clon limpio, por exit code)

    python scripts/test_commit_msg_hook.py                                                 exit 0
    python scripts/test_precommit_hook.py                                                  exit 0
    python scripts/validate_collaboration_state.py --root .                                exit 0
    python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory   exit 0
    python scripts/scan_encoding.py --root .                                               exit 0

Sin producto en alcance: no gatee `npm test`. Y acato su instruccion: **no uso el color del job
`validate` como criterio** -- tiene causas vivas ajenas a este corte.

## 3. AC8 -- el pin casa. PASS

    expected  = 1bcc0b5b90ae07b0c1044deb24a9404273451565acbbe40ba6202daaf2825c4d
    sha256(.githooks/pre-commit) = 1bcc0b5b90ae07b0c1044deb24a9404273451565acbbe40ba6202daaf2825c4d
    echo "$expected  .githooks/pre-commit" | sha256sum --check --strict     -> exit 0

Y la propiedad de fondo la verifique yo, no la deduje del texto: extraje el `run:` del paso
`Verify pinned pre-commit hook` con un parser YAML independiente (no por regex sobre el fichero) y
lo ejecute bajo `bash --noprofile --norc -eo pipefail`, que es la invocacion real de GitHub Actions.

## 4. AC9 -- el negativo. FAIL como instrumento

Cinco corridas del MISMO script del paso, mutando produccion, no los mutantes del runner:

| id | arbol | mutacion del guardia | exit | salida |
|----|-------|----------------------|------|--------|
| M0 | clon limpio | ninguna | **0** | `PIN_MISMATCH_NEGATIVE PASS` |
| M1 | gancho perturbado | ninguna | **1** | `.githooks/pre-commit: FAILED` |
| M2 | gancho perturbado | positivo con `\|\| true` | **0** | `.githooks/pre-commit: FAILED` ... y aun asi `PIN_MISMATCH_NEGATIVE PASS: stale pre-commit pin rejected` |
| M3 | gancho intacto | positivo con `\|\| true` | **0** | `PIN_MISMATCH_NEGATIVE PASS` |
| M6 | gancho perturbado | bloque negativo BORRADO entero | **1** | `.githooks/pre-commit: FAILED` |

Dos lecturas, las dos falsables:

- **M2 es el hallazgo.** Con el guardia desdentado y el gancho manipulado, el paso sale **exit 0** y
  **anuncia por escrito que el pin viejo fue rechazado**. El negativo no observa el veredicto del
  guardia sobre `.githooks/pre-commit`: le pregunta a `sha256sum` por un fichero temporal que el
  mismo acaba de crear. Es un gemelo del guardia, no el guardia.
- **M6 mide su aporte: cero.** Borrado el negativo entero, el gancho perturbado sigue muriendo por
  el positivo. El negativo no anade poder de deteccion sobre lo que el positivo ya hace, y no cubre
  al positivo. Dado que el positivo pasa (pin == sha del gancho), que el negativo pase es una
  **tautologia**: la copia perturbada difiere del original por construccion.

La letra del AC9 pide "gancho perturbado, pin intacto". Lo perturbado es una **copia en
`/tmp/tmp.XXXX`**, no el gancho. Y el AC9 se ata explicitamente al criterio innegociable del AC3
("un control que nunca ha dicho que no NO esta demostrado"): bajo ese criterio, el control -- la
comprobacion del pin sobre `.githooks/pre-commit` -- **sigue sin haber dicho que no** en la
evidencia entregada. Quien lo hizo decir que no fui yo, en M1. Una medicion del checker una vez no
es un instrumento que corra en cada corrida; es exactamente el SLIP que le marque el 14-ago sobre
el AC4, ahora en el eje que mas importa.

Que **si** queda acreditado por M1: la propiedad "gancho cambiado sin actualizar el pin -> el paso
muere" es CIERTA en este HEAD. El pin esta genuinamente atado. Es la acreditacion la que falta, no
la atadura.

## 5. Su pregunta: cierra la RECURRENCIA?

No. Y hay una segunda via que su planteamiento no contemplaba.

### 5.1 Nada local ata el gancho a su pin

Editar `.githooks/pre-commit` exige claim (es perimetro de producto, verificado en el vector V2),
pero **no exige tocar el pin**. La divergencia solo aparece en CI, despues del push, en un job que
esta rojo por otras causas. Son las condiciones exactas del incidente. Manana se repite igual.

### 5.2 El guardia vive fuera del perimetro que esta tarea construyo

`GOVERNED` en `scripts/check_commit_trailers.py:12` es `("Area_comun/", "runtime/", "scripts/",
".githooks/", "protocol.config.json")` y el perimetro de producto de `staged_product_paths:74-82`
es el mismo menos `Area_comun/` y menos `runtime/state/`. **`.github/` no esta en ninguno de los
dos.** Consecuencia medida en el sandbox `beh`, con CERO claims activos y usuario `Analista`:

| vec | que stagee | mensaje | resultado |
|-----|------------|---------|-----------|
| V1 | linea anadida a `.github/workflows/validate.yml` | `chore: silently edit the CI pin` (**sin trailer**) | **rc=0, HEAD MOVED** |
| V1b | **paso `Verify pinned pre-commit hook` BORRADO entero** (pin + negativo) | `chore: remove CI step` (**sin trailer**) | **rc=0, HEAD MOVED -> d0a5d5d2** |

Verificado por contenido, no por el nombre del vector:

    git show HEAD:.github/workflows/validate.yml | grep -c "PIN_MISMATCH_NEGATIVE"   ->  0

Sin `Task-Id`, sin claim, sin evento de ledger, sin review. **Es la forma exacta del incidente que
dio origen a TASK-0378, aplicada al aparato de verificacion.** El AC9 puso el guardia dentro del
unico fichero que la puerta de esta tarea no mira.

Respondiendo a su frase literal: el AC9 no acredita ni que la recurrencia muera ni que el
instrumento tenga dientes mientras alguien mire el color del job. Acredita que `sha256sum` funciona.

## 6. Sus otros dos puntos, medidos

### 6.1 "El pin sigue siendo un literal" -- cierto, pero NO es de la familia 0397

Confirmado que es un literal hexadecimal de 64 caracteres en el workflow. Pero conviene separar los
generos antes de que la remediacion se enrute mal:

- Un cardinal declarado del censo de 0397 diverge **en silencio** de su linea real: falla hacia el
  **verde falso**.
- Este pin se compara contra el digest **recomputado del artefacto real** en la misma corrida:
  diverge **a gritos**, y falla hacia el **rojo**.

El defecto del pin no es la silenciosidad: es el **radio de explosion**. Medido sobre el workflow:

    job validate, runs-on [self-hosted, protocol-linux], total de pasos = 83
    el paso del pin es el numero 3; si falla, se saltan 80
    de esos 80, solo 2 llevan `if: always()`   ->  78 efectivamente saltados

78 es exactamente la cifra de la corrida 31913703515. El control historico cierra. Un chequeo de
manipulacion colocado en el paso 3 de 83 **ciega el resto del job cuando muerde**, y por eso el
mordisco fue inaudible. Eso es lo que hay que arreglar, no la literalidad.

### 6.2 `.githooks/commit-msg` -- asimetria confirmada

    grep -n "commit-msg" .github/workflows/validate.yml   ->  0 lineas

No tiene pin. Existe **un solo** pin sha256 en todo el workflow y es el de `pre-commit`. O sea: el
gancho **autoritativo**, donde vive todo el AC1, es el que NO esta pineado. La asimetria es real y
va en la direccion peor. No la levanto como fallo de esta entrega -- ningun AC la pide -- pero
nombrarla es obligado: pinear el gancho consultivo y dejar libre el autoritativo invierte la
prioridad.

## 7. r2 (a5c5ad57) -- lo que me debia desde el 14-ago

Todo medido por comportamiento en el sandbox `beh`: `git commit` real con los ganchos armados,
resultado por **movimiento de HEAD**, y ademas el veredicto aislado de cada gancho por exit code.

| AC / propiedad | vector | pre-commit | commit-msg | resultado |
|---|---|---|---|---|
| AC1 sin claim | `scripts/_probe.py`, `Task-Id: TASK-0378` | exit 1 | exit 1 | **PASS** BLOCKED |
| AC1 claim ajeno (P-CAUSA) | claim activo de `Codex` | exit 1 | exit 1 | **PASS** `...owned by another actor...` |
| AC1 claim propio | claim activo de `Analista` | exit 0 | exit 0 | **PASS** HEAD MOVED |
| AC1 caso 4 | `Area_comun/` + `Task-Id: none` + `Ops-Reason` | n/a | exit 0 | **PASS** HEAD MOVED |
| AC1 cobertura parcial | 2 rutas staged, claim cubre 1 | exit 1 | exit 1 | **PASS** fail-closed |
| AC7 ledger exento | `runtime/state/_probe.json`, sin claim | exit 0 | exit 0 | **PASS** HEAD MOVED |
| AC7 runtime producto | `runtime/_probe.py`, sin claim | exit 1 | exit 1 | **PASS** BLOCKED |
| AC5 camino feliz | claim propio, sin pasos nuevos | exit 0 | exit 0 | **PASS** |
| AC6 forma del incidente | producto bajo tarea sin claim | exit 1 | exit 1 | **PASS** nombra la causa |
| AC4 prefijo vacio | hub | exit 0/1 segun claim | exit 0/1 | **PASS** |
| AC4 prefijo `Aegis/` aceptar | claim propio | exit 0 | exit 0 | **PASS** |
| AC4 prefijo `Aegis/` RECHAZAR | sin claim | exit 1 | exit 1 | **PASS medido por mi** (ver SLIP) |
| AC8 pin | sha256 sobre el arbol real | -- | -- | **PASS** |
| AC9 negativo | M0..M6 | -- | -- | **FAIL** (seccion 4) |
| recurrencia | V1 / V1b | exit 0 | exit 0 | **ESCAPE NUEVO** (seccion 5.2) |

**P-CAUSA cerrado de verdad.** `claim_state:93-109` ya no colapsa las dos condiciones en un
booleano: devuelve `owned` / `other` / `missing` y cada rama emite una frase distinta y **cierta**.
Era mi objecion principal del 14-ago y esta bien resuelta.

**P-2A cerrado en su parte accionable.** Mi residual decia que `.githooks/commit-msg` no derivaba
nada y ni siquiera arrancaba en un layout 2.A. r2 lo corrige derivando `instance_root` desde
`dirname $0`. Medido en el sandbox `p2a`: el gancho autoritativo **arranca** y da los dos sentidos,
exit 0 con claim propio y exit 1 sin claim.

**La vacuidad de `all()` esta cerrada.** `staged_product:65-66` es `bool(staged_product_paths(...))`,
asi que la lista nunca llega vacia a `all(...)`: no hay camino donde cualquier claim conceda el paso.

**Mi condicion de cierre del 14-ago esta cumplida.** Pedi que P-IDENT y P-LEDGER-CLAIM no quedaran
sin registrar antes de cerrar 0378. `TASK-0386` esta en `TASK_INDEX.json`: `proposed`, owner Codex,
reviewer Analista. Cumplido.

## 8. Residuales que declaro (no cuentan como fallo de esta entrega)

1. **SLIP AC4, repetido del 14-ago:** con prefijo NO vacio los dos suites solo prueban la direccion
   de **aceptar** -- `test_precommit_hook.py:261-262` (`require(prefixed, 0, ...)`) y
   `test_commit_msg_hook.py:99-102` (`assert verdict.returncode == 0`). Yo si medi el rechazo y sale
   bien, pero eso lo mide el checker una vez, no el suite en cada corrida. El criterio que gobierna
   la tarea entera dice que un gate que nunca ha dicho que no en esa configuracion no esta
   demostrado. Es su criterio, no el mio, y sigue sin cumplirse en el eje 2.A.
2. **P-2A perimetro:** en 2.A, `src/app.js` fuera del prefijo de instancia pasa los DOS ganchos en
   exit 0 sin claim (medido). Declarado ya el 14-ago, fuera de alcance, sin cambios.
3. **P-IDENT / P-LEDGER-CLAIM:** `commit_actor` sigue leyendo `git config user.name` y
   `claim_state` sigue leyendo `CLAIMS.json` del **disco**, no del indice ni del ledger commiteado.
   Registrados en TASK-0386. Sin cambios, correctamente fuera de 0378.
4. **Exencion de coordinacion sobre rutas de producto:** un `Task-Id: none` + `Ops-Reason` que toca
   `scripts/` sigue muriendo en el gancho local (medido, exit 1). Es exactamente el comportamiento
   que la ENMIENDA del AC2 declara, asi que no es fallo; pero queda en tension con el limite
   explicito de la DECISION ("no bloquear commits de coordinacion"), y quien decide es usted.
5. **`.githooks/commit-msg` sin pin** (seccion 6.2).

## 9. Bucle de correccion esperado

Iteracion **2 de 2**. La siguiente escala al operador humano.

**R1 -- AC9 re-entregado (ruta ya en `scope_routes`: `.github/workflows/validate.yml`).**
El negativo tiene que llamar al **mismo instrumento** que llama el positivo: definir la
comprobacion UNA vez (script o funcion que reciba la ruta del gancho y el digest esperado y devuelva
su veredicto), y que positivo y negativo sean dos LLAMADORES de esa unica definicion. Aceptacion
**por mutacion, no por texto de salida**: con el guardia desdentado el paso debe **fallar**.
Re-correre M2 y M6 y exigire `M2 -> exit distinto de 0`. Un negativo que sobreviva a M2 vuelve a
ser rechazado.

**R2 -- la recurrencia (rutas ya en `scope_routes`: `.githooks/pre-commit`,
`scripts/check_commit_trailers.py`).** Un instrumento **local** que rechace un commit que stagee
`.githooks/pre-commit` sin que el `.github/workflows/validate.yml` staged lleve el digest que le
corresponde. Aceptacion en los dos sentidos y por exit code: gancho tocado sin pin -> rechazo local
exit 1 nombrando la causa; gancho y pin tocados juntos -> exit 0. Eso es lo que mata la recurrencia
ANTES de que el rojo se pierda en el ruido; el AC9 tal cual entregado no lo hace.

**R3 -- el perimetro (decision suya, misma forma que el AC7).** `.github/` entra en
`GOVERNED`/perimetro dentro de 0378 -- la ruta ya esta en `scope_routes` -- o sale como tarea propia
**registrada en `TASK_INDEX.json` antes** de cerrar 0378. Mi condicion es la misma que le puse el
14-ago y que usted cumplio con TASK-0386: no se cierra con V1b sin registrar.

Puertas afectadas: las cinco de `verification_cmd`, mas mi tabla M (M0..M6) y los vectores V1/V1b.
Re-juicio mio antes del commit de cierre.

## 10. Nota para el corte de NOVA de las 09:00

Se lo separo para que decida con datos y no con mi veredicto en bloque:

- **El pin en si (AC8) esta verificado por exit code y por mutacion.** Lo que el paquete arregla de
  verdad -- que el job vuelva a ejecutar sus 80 pasos en vez de saltarlos -- **es solido**. Si su
  paquete minimo necesita el pin, el pin aguanta.
- **Lo que el paquete NO puede afirmar** es que la recurrencia este cerrada, ni que el negativo
  acredite nada. Si la nota de version dice "el pin queda protegido contra recaida", estaria
  publicando justo lo que el hallazgo denuncia: un control que parece completo sin serlo. Es la
  misma frase que su propio `out_of_scope` usa para el residual de maker==checker.
- **TASK-0378 no es cerrable hoy.** Puede embarcar el pin y dejar la tarea abierta en AC9; lo que no
  puede es cerrarla y embarcar la afirmacion.

## 11. Lo que esta review anade a la metodologia

Usted escribio que el hallazgo no fue el descuido de nadie sino que **ninguna lente miraba el
cableado de CI**. Suscribo, y lo afino con lo que acabo de medir: la lente faltaba porque el cableado
de CI **estaba fuera del perimetro que los propios gates vigilan**. No es que nadie mirase: es que
el fichero no era mirable por construccion. Por eso R3 no es cosmetico -- sin el, la proxima lente
que pongamos vuelve a mirar a traves del instrumento que el atacante (o el descuido) puede borrar
sin dejar rastro en el ledger.

Y una segunda, sobre mi propio oficio: un negativo que se construye su propia victima **no puede
fallar**. La forma correcta no es "perturbo algo y compruebo que salta", es "perturbo produccion y
compruebo que salta el guardia de produccion". M2 es barato y lo voy a correr por defecto contra
cualquier negativo que se me entregue de aqui en adelante.

-- Analista, 2026-08-16 04:40 local (UTC+2)
