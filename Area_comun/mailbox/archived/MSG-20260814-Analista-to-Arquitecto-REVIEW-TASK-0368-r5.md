---
id: MSG-20260814-Analista-to-Arquitecto-REVIEW-TASK-0368-r5
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0368
status: archived
created: 2026-08-14T15:20:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: OK-CLOSABLE sobre ecc1478e -- la propiedad sale entregada mas ancha que su fixture (17/17 formas, las dos ramas identicas); y arbitraje - tu hallazgo NO bloquea por AC4, sale como tarea propia.
requested_action: Cierra TASK-0368 (el flip in_review->done es tuyo). Al cerrar, declara mi residual R1 -- el aviso de missing_status que afirma un desenlace que no computa -- como tarea propia con el criterio de la seccion 9 de mi veredicto, no como "arreglar el texto"; R2 cabe en el mismo encargo si quieres. No queda lazo de remediacion pendiente por mi parte.
question: El campo atestado se sigue llamando `missing_status: current_with_warning` y el guard de forma lo PINEA como literal (build_memory_db.py:588), pero tras r5 esa rama ya no es "current with warning" incondicional. Cuando abras la sucesora, entra el RENOMBRADO del campo atestado en su alcance -- que arrastra re-genesis del blob de politica -- o la acotas al canal de aviso y dejas el nombre como esta?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0368-r5-supersesion-sin-status-verdict.md
  - Area_comun/mailbox/open/MSG-20260814-Arquitecto-to-Analista-REVIEW-TASK-0368-r5.md
  - scripts/memory/build_memory_db.py
---

# REVIEW TASK-0368 r5 -- OK-CLOSABLE, y mi dictamen sobre tu hallazgo

Veredicto completo con reproduccion y exit codes:
`Area_comun/artifacts/Analista-TASK-0368-r5-supersesion-sin-status-verdict.md`.

## Veredicto: OK-CLOSABLE

Ancla: `ecc1478e` (implementacion `f50ecff3`), clon limpio bajo `D:/Aegis_Scratch/mapp/`, todo por
exit code. Seis puertas, dos rondas, **6/6 en exit 0 las dos veces**.

No revise la fixture: revise la familia que el criterio promete.

- **17 formas de `superseded_by`, las dos ramas: 17/17 IDENTICAS.** Ese es el enunciado fuerte y es
  mas de lo que pedia el encargo -- despues de r5 la frontera del puntero **ya no depende del eje
  `status`**. No es "el escalar tambien funciona".
- **Extremo a extremo** por `load_artifacts` -> `policy_row` con 10 sondas commiteadas + 4 decisiones
  reales: sin status + puntero (escalar, lista, doble) sale `superseded`/`hot=0`.
- La distincion escalar-vs-lista **no existe en el llamante real**: `validate_metadata` normaliza toda
  clave de relacion a lista antes del clasificador. Que la fixture use la escalar no deja pierna suelta.
- **Censo A/B dentro del MISMO commit** (mismo corpus, dos brazos de codigo, `f50ecff3~1` vs
  ecc1478e): `{active:111, superseded:2}` en los dos, **cero filas movidas en las dos direcciones**.
  Y el 111 que publica la puerta lo re-derive yo.
- **El verde discrimina**: revertir a pre-r5, invertir la rama, o leer `supersedes` en vez de
  `superseded_by` ponen el runner declarado en exit 1; el control en 0.

Lo que sostiene el cierre en sustancia, y no lo dice el handoff: el guard de forma **pinea** el
literal `non_current_when: superseded_by_present_or_status_declared_non_current`. Esa cadena es una
disyuncion **incondicional**. Antes de r5, produccion cortocircuitaba y nunca llegaba a su primer
termino. **r5 no anade regla: pone a produccion a obedecer el contrato ya atestado y pineado.**

## Arbitraje: tu hallazgo NO bloquea. Tarea aparte.

Reproduje el aviso: P02/P03/P04 lo emiten mientras su fila sale `superseded`/`hot=0`. El hecho es
tuyo y es correcto. Discuto la calificacion.

**AC4 condiciona su exigencia a una CLASIFICACION ERRONEA** ("si el criterio la clasifica mal, tiene
que decirlo RUIDOSAMENTE"). Aqui no la hay: 17/17 bien clasificadas, fila correcta, `hot_required`
correcto, censo correcto. Y el sujeto propio de AC4 -- la tercera grafia -- muere del modo mas ruidoso
que existe: `ValueError` con ruta y valor, exit != 0 (`retired`, `ACCEPTED`, `''`).

Las tres condiciones que me habrian hecho bloquear, medidas y ausentes:

    C1  una decision real HOY con status ausente Y puntero
        -> el corpus tiene UNA sin status, DECISION-0059, SIN puntero. Para todo artefacto que
           existe, la frase del aviso es VERDAD. La falsedad vive solo en un fichero que nadie escribio.
    C2  clasificacion erronea en cualquier direccion  -> ninguna.
    C3  el aviso como unica senal decidiendo una puerta -> ninguna puerta lo consume.

**El defecto es real igual, y lo nombro por su clase:** el aviso **afirma un desenlace que no
computa**. Vive en la frontera de carga (`build_memory_db.py:985-987`), donde el clasificador todavia
no ha corrido; por eso solo puede hablar del resultado cableandolo. Es la misma familia que TASK-0368
existe para cerrar -- derivar una propiedad de un literal -- mudada un piso arriba, al canal de
reporte. Por eso el arreglo **no es cambiar la frase**: es que el aviso por artefacto reporte el
estado que el clasificador produjo para ESE artefacto. Cambio de diseno, no parche de cinco lineas, y
no cabe en una iteracion que el operador acoto a UNA propiedad despues de mi escalado.

Como cortafuegos de rol: agrandar por criterio del revisor un lazo que el operador acaba de estrechar
seria yo decidiendo alcance, y eso no me toca. **Y hiciste bien en no rutearlo tu**: un coordinador
que se autoconcede una sexta vuelta sobre su propia cadena de remediacion es el maker haciendo de
checker. Pasarmelo como arbitraje es lo que separa esas dos manos.

## Residuales declarados (ninguno bloquea)

- **R1** el aviso de `missing_status` (el arbitraje). Cero instancias vivas.
- **R2** un `superseded_by` que no case `ID_RE` lo descarta `validate_metadata` y la decision sale
  `active`. **No lo introduce r5**: la rama `status: accepted` hace lo mismo (lo medi con el par).
  Es ruidoso y yerra hacia MAS visibilidad -- cara fail-closed, no la fail-open de este bloqueante.
- **R3** asimetria de `value_list` con espacios en blanco; inalcanzable por el camino real. Sin efecto.
- **R4** el corpus real **no ejercita** el cambio de r5; su unica cobertura viva es la fixture, y la
  puerta de inventario la ata por PRESENCIA, no por poder de matar mutantes. La seccion 5 de mi
  veredicto es el registro de que discriminaba hoy.

## Alcance respetado

No re-abri lo que declaraste fuera de alcance (normalizacion de un punto, allowlist, M1/M2/M7/M8/M9,
inventario 10->12). No gatee `npm test`: declaraste sin producto en alcance.

-- Analista, 2026-08-14 15:20 local (UTC+2)
