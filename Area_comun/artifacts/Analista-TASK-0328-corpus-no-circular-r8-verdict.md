---
artifact_id: Analista-TASK-0328-corpus-no-circular-r8-verdict
task_id: TASK-0328
reviewer: Analista
role: adversarial checker (maker != checker)
created_at: 2026-08-10T21:20:00Z
anchor_commit: 034e4f48e68ad553dfd425fc893945c6186685e9
verdict: OK-CLOSABLE
iteration: 9 (r8 del maker; noveno juicio del checker)
---

# Re-juicio TASK-0328 -- remediacion 7 (commit `b1e2eb1c`): dos preguntas, dos respuestas

Voz del Analista. Yo no implemento, no promuevo, no cierro. Este veredicto gatea el cierre.
Encargo corto, veredicto corto. Respondo tus dos preguntas y declaro lo que queda.

## Anclaje canonico

- Ancla del encargo: `034e4f48e68ad553dfd425fc893945c6186685e9` (`memory(Codex): persist TASK-0328
  remediation 7`). Implementacion: `b1e2eb1c` (`fix(TASK-0328): guard integral contiguous
  silhouettes`). `scripts/memory/build_memory_db.py` en el ancla es **byte-identico** al de
  `b1e2eb1c` (`diff -q` limpio).
- `git diff --stat 034e4f48 origin/main -- scripts/` (con `origin/main` en `86b2d32f`) toca
  UNICAMENTE `scan_domain_neutrality.ps1` y `test_scan_domain_neutrality.py`. **Ningun cambio en
  `scripts/memory/` despues del ancla.**
- Clon limpio detached en `D:/Aegis_Scratch/multi_agent_project_protocol/an0328r8_gate`
  (DECISION-0104), `git status --short` con 0 lineas. Las sondas corren en un clon HERMANO
  (`an0328r8_probe`) para no ensuciar el clon de gates.
- Cuatro motores cargados como MODULOS INDEPENDIENTES via `git show`, ninguna regex copiada a
  mano: `f732292a` (base, previo a la tarea), `df5de987` (r6), `17629f4f` (r7, el que refute),
  `b1e2eb1c` (r8, el entregable).
- Alcance declarado por el Arquitecto: SOLO hub. **SIN PRODUCTO EN ALCANCE.** No corri gates de
  producto.
- Hora local del juicio: 2026-08-10 23:20 (UTC+2).

## Reproduccion -- gates en clon limpio pristino sobre el ancla

    python scripts/validate_collaboration_state.py --root .   EXIT=0
    python scripts/scan_encoding.py --root .                  EXIT=0
    python scripts/scan_domain_neutrality.py --root .         EXIT=0
    python scripts/check_falsification_contracts.py --root .  EXIT=0
    python runtime/protocol_replay.py --check-drift --root .  EXIT=0   verdict=CLEAN up_to_seq=8634
    python scripts/memory/test_memory_db.py                   EXIT=0   Ran 72 tests in 566.469s OK

El clon de gates queda con `git status --short` en 0 lineas antes y despues.

Y la instantanea EXACTA que publico -- `9f38ebd5` mas mis tres ficheros, en un tercer clon limpio,
para no gatear sobre el arbol caliente (que lleva escrituras de ledger del peer sin commitear):

    python scripts/validate_collaboration_state.py --root .   EXIT=0
    python scripts/scan_encoding.py --root .                  EXIT=0

## PREGUNTA 1 -- el corpus dejo de filtrarse por la guarda bajo prueba?

**SI. Y esta vez lo mido sin creerme el nombre del filtro.**

El filtro circular que refute en r7 -- `if not account_identifier_grouped_is_detected(rendered,
coordinate_bound=False): continue` -- **ya no existe**. El unico filtro de admision que queda es
de SUPERVIVENCIA DEL PARSER: descarta el caso si la presentacion compacta sobrevive entera dentro
de algun `pii_values_for_coordinate(...)`, es decir, si la envoltura NO ciega el payload. Ese
predicado no invoca ninguna de las dos guardas bajo prueba.

No me quedo en la lectura del codigo. Instrumente el generador ENTREGADO (parche minimo sobre el
propio test del commit, sin reescribirlo) para volcar los casos admitidos **y los excluidos**, y
mido las dos poblaciones contra el motor entregado:

    poblacion total generada     6.978
      ADMITIDOS al contrato      1.001   detectados por r8  1.001   CIEGOS 0
      EXCLUIDOS por el filtro    5.977   detectados por r8  5.977   CIEGOS 0

**El filtro restante no esconde ni un caso ciego.** Esa es la comprobacion que faltaba en r7 y es
la que decide: da igual por donde se corte, la poblacion entera se ve.

Composicion del corpus admitido, con la clase que en r7 no aparecia NI UNA VEZ:

    clase de formato        poblacion   detectados   ciegos
    invalid-contiguous            768          768        0     <- clase AUSENTE en r7
    valid-grouped                 169          169        0
    valid-contiguous               64           64        0
    coordenadas 9 (task_id, decision_id, spec_id, relates_to, linked_decisions,
                   supersedes, superseded_by, message_id, file)
    ordenes 3 (before, inside, after)

Y la prueba de que la asercion NO esta satisfecha por construccion -- el mismo corpus, otros
motores:

    motor                        detectados   CIEGOS   (ciegos que son invalid-contiguous)
    r8 (entregable)                   1.001        0    0
    r7 (el que refute)                  256      745    745
    r8 sin la clausula nueva            256      745    745
    r8 sin la guarda entera               0    1.001    768

El corpus **mata al motor que yo refute**: 745 de 1.001 renderizaciones que r7 no veia. Un corpus
espejo no puede hacer eso. Y mata a los dos mutantes que el contrato declara
(`coordinate_raw_contiguous_blind` pierde 745, `coordinate_raw_account_blind` pierde 1.001), con
lo que `mutant_raw_guard_lost[name] > 0` no es una asercion decorativa.

Comprobacion extra que nadie pidio, porque el corpus invalido sale de un generador con prefijo
constante `ES00`: reutilizo las 768 renderizaciones y cambio SOLO la identidad del payload por
otras seis familias invalidas.

    familia invalida            poblacion   CIEGAS en r8
    MAL TECLEADO (ES21..)             768        0
    TRUNCADO (22 caracteres)          768        0
    ENMASCARADO (ES91XXXX..)          768        0
    otro pais (DE00..)                768        0
    minusculas (es00..)               768        0
    longitud maxima (30)              768        0

La propiedad no depende de la constante. Sobrevive a cambio de payload, de pais, de caja y de
longitud.

## PREGUNTA 2 -- la silueta contigua sin checksum valido, por el camino real?

**SI, en las nueve coordenadas gobernadas y por los dos sitios de produccion.**

No por llamada directa a `contains_pii`: por `validate_metadata(...)` y por
`require_safe_text(field='path')`. Cinco familias invalidas x once formas = 55 filas. La columna
`fmt` acredita que el valor pasa el chequeo de FORMA, luego el unico motivo de rechazo posible es
la PII (aisla el falso verde de "lo rechaza el `ID_RE`, no la guarda").

    familia invalida       forms  fmt-validas  pii_base  pii_r7  pii_r8  gate_r8  PERDIDAS vs base
    silueta ES00 (test)       11          4/11     11/11    5/11   11/11    11/11         0
    silueta ES90 (r7)         11          3/11     11/11    1/11   11/11    11/11         0
    MAL TECLEADO              11          3/11     11/11    1/11   11/11    11/11         0
    TRUNCADO                  11          3/11     11/11    1/11   11/11    11/11         0
    ENMASCARADO               11          3/11     11/11    2/11   11/11    11/11         0

    PERDIDAS vs el motor previo a la tarea: 0 / 55

Las once filas que en mi veredicto r7 marque como PERDIDA -- `REQ-<X>-20260809`,
`<X>-TASK-0002`, `<X>-DECISION-0001`, `<X>-SPEC-0071`, `relates_to`, `supersedes`,
`superseded_by`, `linked_decisions`, `MSG-20260605-<X>-...`, `Area_comun/specs/<X>-SPEC-0114..`,
y la ruta por `require_safe_text` -- **estan cerradas las once**, y lo estan para las cinco
familias, no solo para el ejemplo que yo di.

### El precio, medido sobre el corpus gobernado REAL (parser propio)

Recorro los 4.399 `.md` del clon limpio con un parser de frontmatter INDEPENDIENTE (no reutilizo
`iter_source_paths`) y evaluo cada cadena en clave permitida por su coordenada:

    cadenas gobernadas medidas   22.655
    marcadas por r7                   5
    marcadas por r8                   5
    MARCAS NUEVAS r8 vs r7            0
    MARCAS PERDIDAS r8 vs r7          0

**Cero falsos positivos nuevos y cero perdidas** sobre el corpus real. Coincide con el precio 0
que yo mismo estime en r7 sobre 22.918 cadenas.

Negativo especifico sobre los FP que motivaron la exencion: `REQ-SG-2026-0001-20260809` sale
False en base, r7 y r8. `REQ-SK-0210-20260809` sale False en base y True en r7 **y en r8** -- lo
verifique por atribucion: `account_identifier_contiguous_is_bounded` y
`account_identifier_grouped_is_detected(cb=True)` devuelven **False** ambas sobre ese valor en los
dos motores, luego la marca **NO la pone la guarda de esta remediacion**; es anterior a r8 y ya
estaba en el motor que juzgue en r7. Lo declaro como residual ajeno, no como regresion de r8.

## Tabla vector-a-vector

    #  criterio prometido                                              resultado
    0  los 4 gates de protocolo verdes en clon limpio pristino          PASS (exit 0 los cuatro)
    0  drift 0 en el ancla                                              PASS (CLEAN, seq 8634)
    0  el clon de gates queda con git status vacio                      PASS (0 lineas)
    0  el modulo del ancla es el de la implementacion                   PASS (byte-identico)
    0  ningun cambio de codigo de memoria despues del ancla             PASS (diff vacio)
    1  el corpus no se admite por la guarda bajo prueba                 PASS (filtro circular
                                                                          eliminado; el que queda
                                                                          es supervivencia del parser)
    1  el filtro restante no esconde casos ciegos                       PASS (5.977 excluidos,
                                                                          0 ciegos)
    1  el corpus contiene la clase que faltaba                          PASS (768 invalid-contiguous;
                                                                          en r7 eran 0)
    1  la asercion no se satisface por construccion                     PASS (mata a r7 en 745/1001)
    1  los mutantes de la rama nueva mueren                             PASS (745 y 1.001 perdidas)
    1  la propiedad no depende de la constante del payload              PASS (6 familias, 0 ciegas)
    2  silueta contigua sin checksum por validate_metadata              PASS (9 coordenadas,
                                                                          5 familias)
    2  silueta contigua sin checksum por require_safe_text              PASS (5 familias)
    2  las 11 formas que r7 perdia estan cerradas                       PASS (0 perdidas de 55)
    2  precio sobre el corpus gobernado real                            PASS (0 marcas nuevas /
                                                                          22.655 cadenas)
    -  regresion r8 vs r6 sobre el corpus del contrato                  PASS (0 perdidas)
    -  presentacion AGRUPADA con checksum invalido                      RESIDUAL (ver abajo;
                                                                          no es perdida vs base)

## Residuales declarados

1. **La clase queda abierta por un eje: la presentacion AGRUPADA con checksum invalido.** Misma
   envoltura, misma coordenada, mismo payload invalido, cambiando solo la presentacion de
   contigua a agrupada:

        agrupada por guion       poblacion 768   CIEGAS en r8 681
        agrupada por punto       poblacion 768   CIEGAS en r8 681
        agrupada por guion bajo  poblacion 768   CIEGAS en r8 681
        CONTROL agrupada VALIDA  poblacion 768   CIEGAS en r8   0

   **No es regresion**: el motor previo a la tarea es ciego a las 768 (`PERDIDAS r8 vs base = 0`;
   r8 gana 87). Y es coherente con el diseno declarado: la rama agrupada exige mod-97 a proposito,
   como control de falsos positivos (R3 de la remediacion 2, que el encargo me pidio no
   re-juzgar). Lo declaro porque el motivo que hizo INCONDICIONAL la rama contigua -- "un
   identificador mal tecleado, truncado o enmascarado sigue siendo PII" -- se aplica igual a la
   presentacion agrupada, y hoy esa mitad no se ve. **Es material para una tarea nueva, no para
   bloquear esta.**
2. **Estrechamiento r6 -> r7/r8 que sigue en pie, y es de una sola fila.** El caso que trace en
   r7 (`Area_comun/tasks/ES90-6604-...-TASK-0312-front-supervisor.md`, coordenada `file`) sigue
   r6=True / r8=False. Pero sobre el corpus del contrato **r6 detecta 2 de 1.001 y r8 detecta
   1.001, con 0 perdidas de r8 contra r6**, y contra el motor previo a la tarea ese caso es
   base=False. Es un estrechamiento contra un motor intermedio que nunca se publico, no contra la
   linea base. Lo mantengo declarado, no lo cuento como defecto.
3. **`REQ-SK-0210-20260809` marcado desde antes de r8.** Atribuido arriba: no lo pone ninguna de
   las dos guardas. Anterior a esta remediacion; si alguien lo quiere cerrado, es otra tarea.
4. **Sin CI real.** La cuenta sigue bloqueada; no hay corrida de Actions que respalde estos exit
   codes. Todo lo de arriba es clon limpio LOCAL, que no es CI. Limitacion, no equivalencia.
5. No re-juzgue R1-R5 de la remediacion 2 (separadores no admitidos, minimo estructural de 14,
   identificadores nacionales sin mod-97, tasa de sobre-deteccion de la forma agrupada), ni corri
   el replicador entero, tal y como me pediste.
6. La asercion de TEXTO `self.assertEqual(1, source.count(raw_contiguous_clause))` sigue fijando
   la FORMA del bloque. No la cuento como defecto porque el mutante de COMPORTAMIENTO
   (`coordinate_raw_contiguous_blind`) existe y mata con 745 perdidas medidas; la senalo para que
   no se confunda una cosa con la otra.
7. No corri gates de producto: SIN PRODUCTO EN ALCANCE.

## Recomendacion de cierre

**OK-CLOSABLE.**

Las dos propiedades del encargo estan cumplidas y medidas por comportamiento: el corpus dejo de
medir su propia ausencia (5.977 excluidos, 0 ciegos; mata a r7 en 745 casos) y la silueta contigua
sin checksum valido se ve por los dos sitios de produccion en las nueve coordenadas gobernadas,
con 0 perdidas contra el motor previo y precio 0 sobre 22.655 cadenas gobernadas reales.

En r7 declare el presupuesto en 1 iteracion y dije que, si no cerraba la propiedad, volvia al
operador. **Cerro la propiedad**, asi que no abro iteracion ni escalo por este eje.

## Senal al Arquitecto (DECISION-0018)

El eje agrupado-sin-checksum (residual 1, 681 de 768 ciegas) es un hallazgo NUEVO de esta vuelta,
no una reapertura de la anterior. Recomiendo registrarlo como tarea propia -- con su propia
decision sobre si el control de falsos positivos de la rama agrupada debe seguir exigiendo mod-97
-- y NO como remediacion 8 de TASK-0328. Meterlo aqui repetiria el patron que ya nos costo ocho
vueltas: ensanchar el alcance de una tarea ya cerrada en vez de abrir la clase entera de una vez.

-- Analista
