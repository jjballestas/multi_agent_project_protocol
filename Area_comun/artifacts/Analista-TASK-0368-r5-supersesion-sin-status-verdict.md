---
artifact_id: Analista-TASK-0368-r5-supersesion-sin-status-verdict
task_id: TASK-0368
type: adversarial_review
author: Analista
status: final
created: 2026-08-14
verdict: OK-CLOSABLE
---

# Veredicto adversarial -- TASK-0368 remediacion 5, y el arbitraje que me pediste

**OK-CLOSABLE.** La propiedad que el operador autorizo esta entregada, y esta entregada mas ancha de
lo que la acredita su propia fixture.

**Arbitraje: tu hallazgo NO bloquea el cierre. Sale como tarea propia.** Es real, lo reproduje, y
abajo esta el criterio falsable con el que lo decidi -- incluidas las tres condiciones que me habrian
hecho bloquear, las tres medidas y las tres ausentes.

## 0. Ancla canonica

    commit revisado    ecc1478e  (implementacion f50ecff3)
    HEAD del protocolo al medir  139d07e1
    clon limpio        D:/Aegis_Scratch/mapp/t0368r5   (git clone -s, checkout ecc1478e)
    clones auxiliares  e2e5 (corpus real + sondas), mut5 (mutantes), old_mdb.py (arm pre-r5)
    alcance            SOLO hub. No gatee `npm test`, tal como declaraste.

Nada de lo que sigue se midio en el arbol caliente.

## 1. La propiedad entregada, probada por conducta y no por su ejemplo

La fixture nueva (`DECISION-POINTER-NO-STATUS`) prueba UN punto: puntero escalar, `status` ausente.
El criterio no promete un punto: promete que la rama de `status` ausente **evalue** `superseded_by`.
Asi que no revise la fixture: revise la familia. Diecisiete formas de `superseded_by`, en las dos
ramas, llamando al clasificador directamente.

    payload                     status ausente (r5)   status=accepted (control)
    clave ausente               active                active
    None                        active                active
    cadena vacia                active                active
    cadena de espacios          superseded            superseded
    lista vacia                 active                active
    lista con cadena vacia      active                active
    lista de espacios           active                active
    escalar DECISION-0081       superseded            superseded
    lista de un id              superseded            superseded
    lista de dos ids            superseded            superseded
    lista mixta vacia+id        superseded            superseded
    escalar en minusculas       superseded            superseded
    escalar id + texto detras   superseded            superseded
    escalar texto no-id         superseded            superseded
    entero 0                    superseded            superseded
    booleano False              superseded            superseded
    diccionario                 superseded            superseded

**17 de 17 identicas.** Ese es el enunciado fuerte, y es mas de lo que pedia el encargo: despues de
r5 la frontera del puntero ya no depende del eje `status`. No es "el escalar tambien funciona": es
que las dos ramas son la misma funcion sobre el puntero.

Y el eje de grafias sigue como estaba (control, no lo tocaba r5): `retired`, `ACCEPTED` y `''`
mueren con `ValueError` nombrando valor y ruta, con y sin puntero.

## 2. Por que r5 es el arreglo CORRECTO y no un parche que casa con su prueba

Esto no lo dice el handoff y creo que es lo que sostiene el cierre. La politica atestada esta
**pineada por un guard duro** (`build_memory_db.py:578-590`): el motor rechaza cualquier politica
cuyo `non_current_when` no sea literalmente

    "superseded_by_present_or_status_declared_non_current"

Esa cadena es una **disyuncion incondicional**: puntero presente **O** estado declarado no vigente.
No dice "salvo que falte el status". Antes de r5, produccion cortocircuitaba en la rama de status
ausente y **nunca llegaba al primer termino de su propia disyuncion atestada** -- que es exactamente
la leccion 3 de mi r4, verificada ahora desde el otro lado. r5 no anade una regla nueva: pone a
produccion a obedecer el contrato que ya estaba atestado y pineado. Por eso lo doy por correcto en
sustancia y no solo por verde.

## 3. Extremo a extremo, sobre el corpus real

Sondas escritas como ficheros de decision, commiteadas, y leidas por `load_artifacts` -> `policy_row`
(el camino real, no el clasificador aislado). Clon `e2e5`, commit de sonda `f175d271`.

    id      forma declarada                       metadata.superseded_by   estado      hot
    P01     sin status, sin puntero               None                     active      1
    P02     sin status, puntero escalar           ['DECISION-0081']        superseded  0
    P03     sin status, puntero en lista          ['DECISION-0081']        superseded  0
    P04     sin status, dos punteros              ['0081','0090']          superseded  0
    P05     sin status, lista vacia               []                       active      1
    P06     sin status, puntero en minusculas     None (RECHAZADO)         active      1
    P07     sin status, puntero con texto detras  None (RECHAZADO)         active      1
    P08     accepted,  puntero en minusculas      None (RECHAZADO)         active      1
    P09     accepted,  puntero en lista           ['DECISION-0081']        superseded  0
    P10     sin status, puntero cadena vacia      None                     active      1
    0071    real: accepted + puntero              ['DECISION-0081']        superseded  0
    0078    real: proposed                        []                       superseded  0
    0026    real: accepted                        []                       active      1
    0059    real: SIN status, sin puntero         None                     active      1

Dos cosas que esto anade a lo que ya sabias:

1. **La forma lista y la escalar dejan de ser dos casos.** `validate_metadata` normaliza toda clave
   de relacion a lista antes de que el clasificador la vea (`value = values`, l.847). Es decir, en el
   punto de llamada real la distincion escalar/lista **ya no existe**. Que la fixture use la escalar
   no deja hueco: no hay una pierna "lista" sin cubrir.
2. **P06/P07/P08 son el mismo residuo en las dos ramas**, no una fuga nueva de r5. Ver seccion 7.

## 4. Censo A/B: control y sonda DENTRO del mismo commit

No compare conteos de dos commits (mi propia leccion de r4: cada commit tiene su corpus). Corri el
**mismo corpus de ecc1478e** contra los **dos brazos de codigo**: el modulo de `f50ecff3~1` y el de
ecc1478e.

    corpus                       ecc1478e, 113 decisiones (identico en ambos brazos)
    censo con codigo PRE-r5      {'active': 111, 'superseded': 2}
    censo con codigo POST-r5     {'active': 111, 'superseded': 2}
    filas que se mueven          NINGUNA, en ninguna de las dos direcciones

Y cruza con la puerta: el `active_decision_count` del drift sobre ese HEAD dice **111**, que es el
numero que yo re-derive por mi cuenta. El cardinal publicado re-deriva.

Corolario honesto, y lo declaro como residual R4: **el corpus real no ejercita el cambio de r5**. Su
unica cobertura viva es la fixture declarada.

## 5. Que el verde DISCRIMINA: mutantes contra el runner declarado

Clon `mut5` en ecc1478e, runner declarado
`MemoryDbTests.test_current_decision_is_attested_property_not_status_literal`.

    control (produccion intacta)                                  EXIT=0   OK  (8.8 s)
    M-R5a  revertir a pre-r5 (ignorar el puntero)                 EXIT=1   'superseded' != 'active'
    M-R5b  invertir (siempre no vigente si falta status)          EXIT=1   'active' != 'superseded'
    M-R5c  leer la clave equivocada (`supersedes`)                EXIT=1   'superseded' != 'active'
    M-R5d  verdad-de-valor sin `value_list`                       EXIT=0   SOBREVIVE
    control-after (restaurado)                                    EXIT=0   OK

**M-R5d es un mutante EQUIVALENTE y lo declaro como tal, no como fuga.** En el punto de llamada real
`metadata["superseded_by"]` es siempre una lista de cadenas no vacias ya recortadas (seccion 3.1), asi
que `value_list(x)` y `x not in (None,"",[])` son la misma condicion sobre todo dominio alcanzable, en
los dos unicos llamantes (`policy_row:1220` y `check_memory_db_drift.py:34`). Un mutante equivalente no
acusa a la suite.

El par a/b es lo que importa: la fixture mata **las dos direcciones**, no solo la del defecto.

## 6. Puertas: seis, dos rondas, clon limpio, por exit code

    ronda 1 (clon t0368r5 @ ecc1478e)
      check_memory_db_drift.py --root . --fast                                    EXIT=0  (pass, 111, 4889 artefactos)
      test_memory_db.py                                                           EXIT=0
      validate_collaboration_state.py --root .                                    EXIT=0
      check_falsification_contracts.py --root . --workflow ... --inventory        EXIT=0
      scan_encoding.py --root .                                                   EXIT=0
      scan_domain_neutrality.py --root .                                          EXIT=0

    ronda 2, mismo clon, misma orden: las SEIS en EXIT=0 (reproducibilidad DECISION-0115)

Verde reproducible **y** discriminante: la seccion 5 es la mitad que un verde solo no da.

## 7. EL ARBITRAJE

Tu pregunta:

> *El aviso que acompana al caso arreglado sigue diciendo "attested policy treats it as current" para
> una decision que produccion acaba de clasificar superseded -- bloquea eso el cierre por AC4, o es
> tarea aparte?*

**Tarea aparte. No bloquea.** Reproduje el aviso (P02/P03/P04 lo emiten mientras su fila sale
`superseded`/`hot=0`), asi que el hecho es tuyo y es correcto. Lo que discuto es la calificacion.

**Por que no dispara AC4.** AC4 condiciona su exigencia: *"si el criterio la clasifica mal, tiene que
decirlo RUIDOSAMENTE"*. El antecedente es una **clasificacion erronea**. Aqui no la hay: la familia
sale bien clasificada en las diecisiete formas, la fila es correcta, `hot_required` es correcto y el
censo es correcto. No hay nada mal clasificado sobre lo que haya que hacer ruido. Ademas el sujeto
propio de AC4 -- una **tercera grafia** -- muere del modo mas ruidoso que existe: `ValueError` con
ruta y valor, exit distinto de 0, medido en la seccion 1. AC4 esta acreditado por su propio objeto.

**Las tres condiciones que me habrian hecho bloquear, y su medicion.**

    C1  que existiera HOY una decision real con status ausente Y puntero
        -> medido: el corpus de ecc1478e tiene exactamente UNA decision sin status, DECISION-0059,
           y NO tiene puntero. Para todos los artefactos que existen, la frase del aviso es VERDAD.
           La falsedad solo vive en un artefacto que nadie ha escrito.
    C2  que la clasificacion de esa familia fuera erronea en cualquier direccion
        -> medido: 17/17 correctas, e2e correcto, censo A/B sin movimiento.
    C3  que el aviso fuera la unica senal Y que lo que oculta decidiera una puerta
        -> medido: ninguna puerta consume el aviso; lo que decide es la fila, y la fila es correcta.

Ninguna de las tres se cumple. Si alguna se hubiera cumplido, este veredicto seria CHANGE-REQUIRED.

**Y sin embargo el defecto es real, asi que lo nombro por su clase y no por su cadena de texto:** el
aviso **afirma un desenlace que no calcula**. Esta escrito en `build_memory_db.py:985-987`, en la
frontera de carga, donde el clasificador **todavia no ha corrido**; por eso puede hablar del resultado
solo cableandolo. Es la misma familia de defecto que TASK-0368 existe para cerrar -- derivar una
propiedad de un literal en vez de computarla -- mudada un piso arriba, al canal de reporte. Por eso el
arreglo no es cambiar la frase: es que el aviso por artefacto reporte **el estado que el clasificador
produjo para ESE artefacto**. Eso es un cambio de diseno en la frontera de carga, no un parche de cinco
lineas, y no cabe en una iteracion que el operador acoto a UNA propiedad despues de mi propio escalado.

Lo digo tambien como cortafuegos de rol: **agrandar por criterio del revisor un lazo que el operador
acaba de estrechar seria yo decidiendo el alcance, que no me toca.** La propiedad autorizada esta
entregada y es la correcta. El residuo se declara en el cierre y se abre con su propio encargo.

**Hiciste bien en no rutearlo tu.** Un coordinador que se autoconcede una sexta vuelta sobre su propia
cadena de remediacion es el maker haciendo de checker; pasarmelo como arbitraje es lo que separa esas
dos manos. Lo dejo escrito porque el mecanismo importa mas que este caso.

## 8. Vector por vector

| # | Vector | Resultado |
|---|--------|-----------|
| V1 | Rama `status` ausente evalua `superseded_by` (la propiedad autorizada) | **PASS** |
| V2 | Familia completa de 17 formas del puntero, no solo la de la fixture | **PASS** 17/17 |
| V3 | Paridad con la rama `status` presente (misma funcion sobre el puntero) | **PASS** 17/17 identicas |
| V4 | Forma lista, que es la del corpus real, y forma escalar | **PASS** (y son la misma en el llamante real) |
| V5 | Extremo a extremo por `load_artifacts` -> `policy_row`, 10 sondas + 4 reales | **PASS** |
| V6 | Censo A/B, mismo corpus, dos brazos de codigo, dos direcciones | **PASS** cero filas movidas |
| V7 | Cardinal publicado re-derivado por mi (111) contra el de la puerta (111) | **PASS** |
| V8 | Fixture discrimina: mutantes a/b/c mueren, control vive | **PASS** 3/3 + 1 equivalente declarado |
| V9 | Tercera grafia sigue muriendo ruidosa (`retired`, `ACCEPTED`, `''`) | **PASS** |
| V10 | Produccion obedece la disyuncion `non_current_when` atestada y pineada | **PASS** |
| V11 | Seis puertas, clon limpio, dos rondas, por exit code | **PASS** 6/6 x2 |
| V12 | Aviso de `missing_status` afirma un desenlace que no calcula | **RESIDUO R1** -- no bloquea, ver s.7 |

Sin SLIPS bloqueantes.

## 9. Residuales declarados

- **R1 (el arbitraje).** `build_memory_db.py:985-987` afirma "attested policy treats it as current"
  para todo `status` ausente, incluido el caso que r5 clasifica `superseded`. Clase: **un mensaje que
  afirma un desenlace que no computa**. Criterio para la tarea sucesora, no cadena a parchear: *el
  aviso por artefacto debe reportar el estado que el clasificador produjo para ese artefacto*.
  Cero instancias vivas hoy.
- **R2 (residuo pre-existente, simetrico).** Un `superseded_by` que no case con
  `ID_RE = ^[A-Z]+-[0-9A-Za-z._-]+$` lo **descarta** `validate_metadata` y la decision sale `active`.
  Medido en P06/P07/P10. **No lo introduce r5**: P08 demuestra que la rama `status: accepted` hace
  exactamente lo mismo. Ademas es RUIDOSO ("rejected frontmatter key superseded_by") y yerra hacia
  **mas** visibilidad (`hot_required=1`), que es la cara fail-CLOSED de I4, no la fail-open que este
  bloqueante existe para cerrar. Encaja natural en el alcance de R1 si se abre.
- **R3 (cosmetico, lo declaro para que nadie lo redescubra como hallazgo).** `value_list` es asimetrico
  con espacios en blanco: `"   "` da lista no vacia, `["   "]` da vacia. Simetrico en las dos ramas e
  **inalcanzable** por el camino real (`validate_metadata` normaliza antes, y un escalar de espacios
  no pasa `ID_RE`). Sin efecto.
- **R4.** El corpus real no ejercita el cambio de r5 (censo A/B sin movimiento). Su unica cobertura
  viva es la fixture declarada, y la puerta de inventario ata esa declaracion **por PRESENCIA**, no por
  poder de matar mutantes (hallazgo 7 de mi r4). La seccion 5 de este veredicto **es** el registro de
  que la fixture discriminaba el 2026-08-14; si alguien la diluye manana, la puerta no lo dira.

## 10. Lo que NO revise, y por que

Declaraste fuera de alcance lo que yo cerre en r4: normalizacion de un solo punto, allowlist sin
ampliar, M1/M2/M7/M8/M9, inventario 10->12. No los re-abro. Lo unico que toque de ahi fue incidental y
salio confirmando: el eje de grafias de la seccion 1 vuelve a acreditar la frontera de la allowlist y
la muerte ruidosa de la tercera grafia. Tampoco gatee `npm test`: declaraste sin producto en alcance.

## 11. Recomendacion de cierre

**OK-CLOSABLE.** TASK-0368 puede pasar a `done`. El flip es tuyo, no mio.

Al cerrar, declara R1 (y R2 con el, si te cabe en el mismo encargo) como tarea propia con el criterio
de la seccion 9 -- no como "arreglar el texto del aviso". Si el operador prefiere que R1 entre como
condicion del cierre en vez de como sucesora, es su llamada, no la mia: mi dictamen es que **por AC4 no
lo es**.

Sin lazo de remediacion pendiente por mi parte. Si abres la sucesora y quieres que la revise, es una
review nueva sobre una tarea nueva, con su propio par de iteraciones.

-- Analista, 2026-08-14 15:14 local (UTC+2)
