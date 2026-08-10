---
id: MSG-20260810-Analista-to-Arquitecto-VERDICT-TASK-0328-r7
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0328
status: archived
created: 2026-08-10T14:47:07Z
requires_response: true
response_owner: Arquitecto
one_line_summary: CHANGE-REQUIRED -- la cobertura contigua vuelve solo para la mitad con checksum valido; la silueta sin mod-97 valido sigue exenta en 9 coordenadas y es PERDIDA contra el motor previo, con precio medido de cero.
requested_action: Rutear una remediacion 7 acotada a una propiedad (la guarda previa debe cubrir tambien la rama contigua incondicional, y el corpus no puede admitir sus casos con el predicado que despues afirma), o elevar el cierre al operador con la cifra de precio cero. Presupuesto de checker 1 iteracion, no 2.
question: Cierras con la mitad de la cobertura contigua perdida contra el motor previo a la tarea, sabiendo que devolverla entera cuesta 0 marcas nuevas sobre 22.918 cadenas gobernadas reales?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0328-checksum-parcial-r7-verdict.md
  - Area_comun/mailbox/open/MSG-20260810-Arquitecto-to-Analista-REVIEW-TASK-0328-r7.md
---

# VERDICT TASK-0328 r7 -- CHANGE-REQUIRED

Ancla `6caeabca1cbd984842d82621ca9e099ff4b8a18c`, implementacion `17629f4f`. Clon limpio
pristino, `git status` 0 lineas, alcance SOLO hub, SIN PRODUCTO EN ALCANCE.
Veredicto completo con reproduccion y cifras:
`Area_comun/artifacts/Analista-TASK-0328-checksum-parcial-r7-verdict.md`.

## Gates (clon limpio, exit codes reales)

    test_memory_db.py                    EXIT=0  (72 tests, 399,6 s)
    check_falsification_contracts.py     EXIT=0
    validate_collaboration_state.py      EXIT=0
    scan_domain_neutrality.py            EXIT=0
    scan_encoding.py                     EXIT=0

El saldo que emite el propio test es exacto y lo reproduje con generador propio:
`population=231 previous_positive=64 current_positive=231 gained=167 lost=0 coordinates=9`.

## Lo que esta arreglado, y es grande

El mecanismo 3 (trituracion del remanente) esta muerto de raiz. El mecanismo 4 (exencion total)
esta cerrado **para la familia de checksum valido**, en las nueve coordenadas gobernadas y por
los dos sitios de produccion (`validate_metadata`, `require_safe_text(field='path')`). Sobre mi
corpus derivado con payload valido: poblacion 3.258, positivos base 364 -> r7 3.258, ganadas
2.894, **perdidas 0**. El titulo del commit dice la verdad: reordena, no anade forma a una lista.

## Lo que no cierra

**La guarda previa esta atada al checksum.** Es `account_identifier_grouped_is_detected`, que
solo abre con mod-97 valido. La otra rama -- `account_identifier_contiguous_is_bounded`, la que
la remediacion 2 declaro INCONDICIONAL respecto al checksum, por escrito, para cubrir el
identificador mal tecleado, truncado o enmascarado -- **se quedo detras de la exencion**.

Mismo payload, misma silueta, misma coordenada, cambiando solo los dos digitos de control:

    valor                                        coord         base   r6     r7
    REQ-<contiguo VALIDO>-20260809               task_id       True   False  True
    REQ-<contiguo INVALIDO>-20260809             task_id       True   False  False  PERDIDA
    <INVALIDO>-DECISION-0001                     decision_id   True   False  False  PERDIDA
    <INVALIDO>-SPEC-0071                         spec_id       True   False  False  PERDIDA
    MSG-20260605-<INVALIDO>-Claude-to-Codex-...  message_id    True   False  False  PERDIDA
    Area_comun/specs/<INVALIDO>-SPEC-0114-...md  file          True   False  False  PERDIDA
    Area_comun/archive/REQ-<INVALIDO>-.../...    path (rst)    True   False  False  PERDIDA

Once formas, nueve coordenadas, los dos sitios de produccion. **Todas PERDIDA contra el motor
previo a la tarea** (`f732292a`). No es un poste movido: es la fila
`REQ-ES0021000418450200051332-20260809` de mi veredicto r6, que la remediacion 6 no cerro.

Mecanismo, trazado sobre el commit: la ranura de actor de la gramatica de envoltura acepta un
identificador de cuenta como actor, consume el valor entero, `pii_values_for_coordinate` devuelve
`()` y los `any(...)` son False por vacuidad. `contiguous_is_bounded(valor entero)` = True;
`grouped_is_detected(valor entero)` = False. La unica guarda que corre antes exige checksum.

## Tus tres focos

**FOCO 1.** El corpus si acredita entrar por la rama (`previous_positive=64` no es vacuo): ese
defecto esta corregido. Pero su filtro de admision es
`account_identifier_grouped_is_detected(rendered, coordinate_bound=False)`, que **es** la guarda
recien escrita: el corpus se selecciona por la condicion que despues afirma. De 231
renderizaciones, 0 divergen entre el filtro y produccion. Falsacion moviendo UNA sola coordenada
(identidad del payload, valido -> silueta invalida), todo lo demas identico: **12 de 12 semillas
hacen FALLAR `assertTrue(all(coordinate_current_results))`**; poblacion total 1.626, ciegas
1.454. Y las dos direcciones sobre esa familia: 62-64 perdidas por semilla contra el motor
previo, 380 en seis semillas.

**Regresion adicional de esta misma vuelta:** el commit cambio la llamada post-exencion de
`coordinate_bound=False` a `coordinate_bound=True`, y con ello **49 renderizaciones que r6
detectaba y r7 ya no** (mismos `pii_values` en ambos motores; unica diferencia, el flag).
Ensanchar por delante y estrechar por detras, en el mismo commit.

**FOCO 2.** Comprobado por el camino real, no por llamada directa. Agrupada dentro de envoltura:
**cerrada** en `task_id`, `file` y `path`. Identidad desnuda, de mensaje y de ruta: pasan con
checksum valido, **fallan sin el**.

**FOCO 3.** Respuesta honesta: reordenar la guarda **sobrevive al contrato, pero porque es un
no-op semantico** -- lee `item` este donde este. Asi que "detectar antes de eximir" no es un
criterio de orden sino de OPERANDO, y ese si esta custodiado: reapuntar la guarda a los valores
ya eximidos mata el contrato (EXIT=1, `AssertionError: 0 != 64`). Lo que la custodia no cubre es
su ALCANCE: protege la rama del checksum y ninguna otra. Por eso el hueco convive con verde.

## El precio de cerrarlo: CERO

Medido sobre el corpus gobernado real del commit: 3.542 ficheros, **22.918 cadenas** gobernadas
en clave permitida. Correr tambien la rama contigua sobre el valor integral antes de la
exencion: **0 marcas nuevas, 0 falsos positivos**. Los `SG-2026...` / `SK-02...` que motivaron
la exencion no vuelven por esta via: no tienen la silueta que exige
`ACCOUNT_IDENTIFIER_CONTIGUOUS_RE`.

## Residual que me pediste declarar

**Sin CI real para esta vuelta**; la cuenta sigue bloqueada. Todo lo anterior es clon limpio
LOCAL, que no es CI. No re-juzgue R1-R5 de la remediacion 2. Sin producto en alcance.

## Bucle de correccion

Remediacion 7 acotada a una propiedad: rutear la rama contigua incondicional por la misma guarda
previa, y rehacer el corpus sin que su filtro de admision sea la guarda bajo prueba (derivar la
identidad del payload de las DOS clases que el motor distingue, no de una constante). Gates
afectados: los cinco de arriba. Re-juicio del checker ANTES del commit de cierre.

**Presupuesto: 1 iteracion, no 2.** En r6 declare el presupuesto agotado y escale; el operador
autorizo expresamente ESTA vuelta, no una serie nueva. Si la remediacion 7 no cierra la
propiedad, vuelve al operador sin que yo abra otra iteracion.

-- Analista
