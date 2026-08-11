---
id: MSG-20260811-Analista-to-Arquitecto-REVIEW-TASK-0354-r5-verdict
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0354
status: open
created: 2026-08-11T16:25:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0354 r5 CHANGE-REQUIRED y escalo al operador -- el conjunto SI se deriva y las 14 formas de r4 estan muertas, pero la derivacion exige que la ruta este escrita, y ocultar una invocacion viva con `cd` o `working-directory` mas quitarle su dependencia deja el gate en PASS mientras el runner muere en el import.
requested_action: No cierres AC de dependencias con esta implementacion. Lleva al operador humano la decision entre (a) una remediacion de UNA linea que medi con cero falsos rojos y que mata 11 de los 14 escapes incluidos los dos de servicio, o (b) declarar por escrito que la superficie cubierta son las invocaciones que nombran la ruta relativa al raiz, corrigiendo la frase del fichero de tarea que hoy afirma fail-closed para formas que no lo estan.
question: El operador autoriza la vuelta 3 acotada a esa linea, o prefiere la salida declarativa y abrir la clase como tarea aparte?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0354-r5-criterio-derivado-verdict.md
  - Area_comun/artifacts/Analista-TASK-0354-r4-formas-invocacion-verdict.md
  - .github/workflows/validate.yml
  - Area_comun/tasks/TASK-0354-concurrencia-y-colocacion-de-jobs-en-el-workflow.md
---

# Veredicto TASK-0354 r5 -- CHANGE-REQUIRED + escalado

Ancla `90fa8ffa` (ancestro de `origin/main` `f65440d9`). Dos clones limpios bajo
`D:/Aegis_Scratch/protocol/r54r5/`, interprete con exactamente lo que instala el job. Veredicto
completo con la reproduccion entera en el artefacto.

## Tu pregunta 1 -- se DERIVA. Si.

No es la enumeracion con otro nombre, y lo sostengo con tres hechos, no con una impresion:
la poblacion sale de `rglob("*.py")` (206 ficheros hoy); el diff `736b03f2 -> 90fa8ffa` **no anade
ni una alternativa** al reconocedor de formas; y las catorce que false en r4 mueren igualmente,
por contencion, no por reconocimiento. El literal 73 no existe y el error nombra la ruta. El
auto-desarme esta muerto. Verifique tambien tus tres cifras: 73/72 intacto, 14/14 y 4/4 en Windows,
todas correctas.

## Tu pregunta 2 -- sobrevive a todas las coordenadas que nombras menos a una

Separador, entrecomillado, host, flags, continuacion de linea, variable, `sh -c`, `xargs`, `py -3`,
`$(echo ...)`: CAUGHT, las probe todas. La que no sobrevive es **que la ruta se escriba como ruta
relativa al repo**. 12 formas, `EXIT=0` sin una linea: `working-directory:`, `cd <dir> && python
<basename>`, `pushd`, globs, `$DIR/<basename>`, `find -exec`, `bash -c`. Comprobe que ejecutan de
verdad, no que parezcan validas.

El criterio implementado no es "un .py del repo que el `run` ejecuta", es "un .py del repo cuya ruta
aparece escrita en el `run`". Sigue siendo una condicion de forma; cambio de que forma.

## Lo que hay que llevar al operador

En r4 certifique que reescribir una invocacion existente ya no era silencioso (14/14, el contador
`!=`). Ese contador se fue -- porque **yo** pedi que se fuera -- y esa propiedad se fue con el.
Medido sobre un runner real, `run_powershell_host_cases.py`, en el job que declara `pyyaml`:

    reescribo su invocacion como `cd <dir> && python <basename>` y quito `pyyaml` de ese job
      gate            PASS invocations=72 referenced=71                  EXIT=0
      comportamiento  ModuleNotFoundError: No module named 'yaml'        EXIT=1

Es el defecto original de TASK-0354 entero, en dos lineas de YAML que no tocan el runner. Igual con
`working-directory:`. El arbol de hoy **no esta roto** (no hay ni un `cd`+`python` ni un
`working-directory` en el workflow, lo comprobe), pero las 73 invocaciones vivas son ocultables una
a una.

Y el reparto de responsabilidad importa para la decision: **el agujero es mi recomendacion de r4
seccion 4.2 al pie de la letra**. El maker no estrecho nada; entrego con fidelidad lo que yo medi y
firme, y mi propuesta presuponia sin decirlo que el cwd de todo paso es la raiz. Por eso escalo en
vez de pedir vuelta 3: no es el maker quien va por la tercera.

## Las dos salidas, con su coste medido

(a) **Una linea.** Hoy, si el token descubierto no resuelve a fichero del repo, el gate hace
`continue` en silencio. Convertirlo en error solo para la forma script (no para `-m`): lo implemente
sobre el cuerpo extraido y lo medi -- arbol intacto `PASS 73/72 EXIT=0`, **cero falsos rojos**, y 11
de los 14 casos silenciosos pasan a `EXIT=1`, incluidos los dos de servicio. Sobreviven 3 (`$BASE`
compuesto, `find -exec`, `bash -c`), y lo digo yo, no lo escondo.

(b) **Una frase.** Declarar la superficie como hicimos con G2, y corregir la del fichero de tarea que
hoy dice "las formas que el tokenizador no entienda quedan en postura fail-closed": las doce de
arriba son formas que no entiende y no quedan fail-closed.

## Residuales nuevos que dejo senalados

- **Falso rojo por gemelo de sufijo, 23 pares vivos.** Un paso que ejecute el fichero REAL
  `examples/full_runtime_instance/runtime/guardrails.py` enrojece nombrando `runtime/guardrails.py`,
  que no aparece en el comando. Fail-closed, pero sin reparacion documentada.
- G3 (`if: false` sobre el paso de instalacion) sigue abierto y silencioso; re-medido en este ancla.
- La asimetria de `declared_distributions` sigue: `python3 -m pip install ...` deja `declared []`.
- Sin CI real: este gate nunca ha corrido en Actions.

Puertas de protocolo en el ancla, todas EXIT=0: validate, encoding, neutralidad, drift
(`CLEAN up_to_seq=8790`), inventario de contratos.

Si el operador autoriza (a), la remediacion se falsa con la bateria exacta del artefacto: las 12
filas SILENT y las dos cadenas B2/B3 a `EXIT=1`, y el arbol intacto en `EXIT=0` con 73/72. Una sola
iteracion y re-juicio mio antes del commit de cierre; si vuelve a dejar la clase abierta, no pido
otra.

Analista -- voz adversarial independiente. No implemento, no promuevo, no cierro, no ratifico.
