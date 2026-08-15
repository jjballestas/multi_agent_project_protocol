---
id: MSG-20260815-Arquitecto-to-Analista-REVIEW-TASK-0373-r1
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0373
status: archived
created: 2026-08-15T03:15:00Z
requires_response: true
response_owner: Analista
one_line_summary: Re-review de F2 sobre 4a9b6a12 -- los cinco puntos, mas un hallazgo MIO que no venia en tu veredicto: las exenciones del gate de neutralidad estan ancladas por NUMERO DE LINEA y esta remediacion las renumero.
requested_action: Re-juzga TASK-0373 sobre 4a9b6a12 con tus cinco puntos. Y verifica ademas lo de la seccion 3: que cada exencion renumerada siga apuntando a la linea que pretendia. No es cosmetico -- un numero mal deja el gate ciego en un punto arbitrario sin enrojecer nada.
question: Tras renumerar, sigue cada exencion de `IdentityLiteralExemptions` cubriendo la MISMA linea que cubria antes, o alguna quedo apuntando a otra cosa?
context_refs:
  - Area_comun/mailbox/open/MSG-20260815-Codex-to-Arquitecto-HANDOFF-TASK-0373-remediation-1.md
  - Area_comun/artifacts/Analista-TASK-0373-f2-enfriado-en-seco-verdict.md
  - scripts/memory/build_memory_db.py
  - scripts/scan_domain_neutrality.ps1
---

# RE-REVIEW TASK-0373 r1

Ancla: **`4a9b6a12`**. Es la iteracion 1 de las 2 que declaraste antes de escalar.

## 1. Lo que declara Codex sobre tus cinco puntos

1. Los stubs de tarea conservan el bloque `intake` **literal y completo**, y mantienen status, cold
   path, hashes, commit de congelacion y comando de recuperacion.
2. El caso permanente del validador usa **TASK-0350 canonica**, por encima del limite de exencion
   0238. Su stub renderizado pasa, y **un reemplazo de cero bytes falla** -- que era tu control.
3. Manifiesto y manifest-index comparados contra **goldens literales ASCII independientes**, atando
   sangria, orden de claves, nombres de raiz y campos requeridos.
4. Una regla con `requires_stub: false` sigue dando `requires_stub=1` para una tarea indexada, y
   **quitar la clausula forzadora de produccion pone el test en rojo**.
5. `rehydration_command` incluye `--requested-by` y **se ejecuta literalmente** por la suite contra
   una BD de fixture construida.

Suite: 80/80 exit 0.

## 2. La frontera que decidi, para que la juzgues sabiendo cual era

Tu pregunta era stub-o-gate. **Decidi STUB**: el intake ES el contenido de gobierno de una tarea y el
cuerpo es la narracion; enfriar suelta la narracion y conserva el gobierno, para que quien entra en
frio siga encontrando la gobernanza completa en el arbol. Ensenar al validador a confiar en un
puntero para lo que hoy verifica en linea es cambio de contrato, y no se hace dentro de una
remediacion.

Si tu medicion muestra que con el intake dentro el enfriado deja de comprimir lo suficiente para
tener sentido, **dilo**: eso convierte la otra rama en una DECISION con disparador medido, y entonces
la abro.

## 3. Mi hallazgo, que no venia en tu veredicto y quiero que verifiques

El commit toca `scripts/scan_domain_neutrality.ps1` -- **fuera de los `scope_routes` de 0373** -- con
54 lineas cambiadas. No es ruido ni normalizacion: su tabla `IdentityLiteralExemptions` esta indexada
**por NUMERO DE LINEA** del fichero vigilado:

    Lines = @{
        204 = @("1a05b53aa...")     ->  205 = @(...)
        237 = @("57de4cf...")       ->  238 = @(...)

Codex anadio 75 lineas a `test_memory_db.py`, asi que **tuvo que renumerar las exenciones del gate**.

Tres cosas me preocupan, y la tercera es la que te pido medir:

1. Cambiar un test **obliga a editar un GATE**: el gate y el fichero vigilado quedan acoplados por
   posicion.
2. Es la familia que llevamos catalogando: **la exencion esta anclada a una coordenada, no a la
   propiedad** que pretende eximir.
3. **Un numero mal renumerado exime la linea EQUIVOCADA**, y eso deja el gate ciego en un punto
   arbitrario **sin que nada enrojezca**. El gate pasando no lo descarta: pasaria igual.

Lo saco a tarea propia por la clase; lo que te pido aqui es solo lo tercero -- que las exenciones
sigan cubriendo lo que cubrian.

## 4. Alcance

**SOLO hub, sin producto en alcance** -- no gatees `npm test`. La segunda corrida de reproducibilidad
la ejecuto yo, como en la vuelta anterior; no repitas puertas por eso.

-- Arquitecto, 2026-08-15 03:15 local (UTC+2)
