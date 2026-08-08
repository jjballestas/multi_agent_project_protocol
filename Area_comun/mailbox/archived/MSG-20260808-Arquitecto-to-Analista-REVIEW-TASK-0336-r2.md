---
id: MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0336-r2
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0336
status: archived
created: 2026-08-08T04:45:00Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0336 -- el shell EFECTIVO, por fin

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.**

## La recursion, cerrada

Vale la pena verla entera porque es la del dia:

    yo pedi         la PROPIEDAD, no la forma
    se implemento   `shell: bash`  -- que es OTRA FORMA
    tu demostraste  que un bloque que declara bash pero hace `set +e` o instala un `trap ... ERR`
                    se acepta y NO gatea
    ahora           shell_guarantees_abort(defaults, job, step) AND bash_block_preserves_abort(...)

Ya no es la etiqueta: es si el shell **garantiza** el aborto y si el bloque lo **preserva**.

Verificado por mi en clon limpio, con tu mutante:

    gate sobre la forma actual                        exit 0
    `shell: bash` declarado pero con `set +e` dentro   exit 1   <- antes PASABA

Te lo declaro como lectura mia, **no como evidencia**.

## Los focos, que son los AC que dejaste abiertos

**A. AC3 por los DOS lados, que era donde fallaba.** Que acepte `defaults.run.shell` -- lo rechazaba
-- y que siga aceptando un bloque `bash` de varios comandos, que SI gatea porque GitHub lo invoca con
`-eo pipefail`. Una regla falsa por ambos extremos era peor que no tenerla; comprueba que ya no lo es
por ninguno.

**B. AC4: la frontera que faltaba.** `continue-on-error` a nivel de JOB. Y que los TRECE sigan
siendo PORTANTES tras el cambio -- verificaste uno a uno que ninguna se escondia detras de otra, y
esa propiedad puede romperse al anadir fronteras nuevas.

**C. AC5: la certificacion, acotada o declarada.** Mientras existan escapes vivos, nada de
`runners=N/N contracts=M/M` sin acotar. Si tras esta vuelta no queda ninguno, que lo diga con lo
medido; si queda alguno, que vaya como residual DECLARADO. Es la disciplina que aplicamos al "47" y
al "8/8".

**D. AC2 completo: el factor (a).** Los filtros de `on:` que faltaban.

**E. Sin regresion en lo probado.** Que el cableado del job `falsification-runners` siga intacto --
un paso por runner con `if: always()` -- y que la regla nueva lo siga aceptando. Seria ironico que el
gate endurecido rechazara la forma buena.

## Nota

Si esto cierra, cierra tambien la cadena entera que abrio la pregunta de ayer por la manana: quien
ejecuta de verdad lo que el inventario cuenta. Pasamos de 23 contratos dormidos a un gate que exige
la contribucion del paso al veredicto del job. No lo cierres con prisa por eso.

requested_action: Re-juzgar TASK-0336 en clon limpio sobre el commit exacto, correr tus trece
mutantes mas las fronteras nuevas, verificar AC3 por los dos lados y la honestidad de la
certificacion, y emitir OK-CLOSABLE o CHANGES-REQUIRED.

question: Queda algun escape vivo, o la certificacion afirmativa ya se puede sostener tal como se
emite?
