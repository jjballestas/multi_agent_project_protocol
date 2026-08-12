---
id: MSG-20260812-Analista-to-Arquitecto-VERDICT-TASK-0354-r8
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0354
status: open
created: 2026-08-12T00:15:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: CHANGE-REQUIRED declarativo y ESCALA AL OPERADOR -- la seccion 4 esta transcrita literal y correcta, pero el cardinal 72 que puse yo tampoco re-deriva (son 73 invocaciones y 72 ficheros, dos criterios distintos cuya coincidencia era accidental), y el goal de TASK-0363 sigue con la propiedad de UNA condicion que su propio AC5 nuevo refuta.
requested_action: NO cierres TASK-0354 todavia. Lleva al operador la eleccion A/B de la seccion 8 del veredicto. Si autoriza A, aplica la seccion 6 como TRANSCRIPCION (el texto exacto y los cardinales medidos estan escritos ahi): cardinal 73 invocaciones / 72 ficheros con la asimetria del duplicado, en TASK-0354 y en el goal y AC1 de TASK-0363; la propiedad de DOS condiciones tambien en el goal de TASK-0363; N2 deja de ser "atrapada" tambien en el cuerpo de TASK-0363; repara el empalme roto del goal; y anade el falso rojo por mencion-no-invocada al inventario de residuales. Cero cambios en .github/workflows/validate.yml. Reenvia y lo re-juzgo antes de tu commit de cierre.
question: Llevas la eleccion A/B al operador antes de tocar nada, o prefieres que la lleve yo por escrito en el mismo hilo?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0354-r8-cardinal-73-y-goal-refutado-verdict.md
  - Area_comun/artifacts/Analista-TASK-0354-r7-censo-y-resolucion-verdict.md
  - Area_comun/tasks/TASK-0354-concurrencia-y-colocacion-de-jobs-en-el-workflow.md
  - Area_comun/tasks/TASK-0363-el-token-pegado-al-interprete-no-es-el-objetivo.md
---

# VEREDICTO TASK-0354 r8 -- CHANGE-REQUIRED declarativo + escalada

Ancla: texto en `665d00fb` (== origin/main), implementacion en `cf918584`. El YAML no se toco: diff
vacio y sha256 `f2d1e8a3...` identico. Clon limpio `git clone -s` con historia completa bajo
`D:/Aegis_Scratch/mapp/t354r8/`, gate extraido del YAML con PyYAML, gateado por exit code.
Solo hub, sin producto en alcance.

## Lo primero: la seccion 4 esta bien aplicada

Transcrita literal en TASK-0354. Las dos condiciones, las dos direcciones opuestas, el `\` normalizado
y el `./` opcional. Verifique una a una contra el mecanismo las nueve afirmaciones del parrafo y las
cuatro cifras con que refuta el 69 (66 / 64 / 72 / 76): las trece confirman. Y elegir AC propio para la
mitad de modulo es la decision correcta por la razon correcta.

## Lo que bloquea

**1. El 72 tampoco re-deriva.** La poblacion reescribible son **73 invocaciones** (todas las que la
puerta cuenta, todas forma script, todas con componente de directorio), no 72. Mi criterio de r7 estaba
anclado a la LINEA (`^python <ruta>.py`) y descartaba en silencio la invocacion numero 73:
`if ! python scripts/prune_state.py --root . --check; then`. Falsado: ocultarla deja el gate en verde y
**si** le quita la cobertura a ese fichero (`referenced` 72 -> 71). Y los dos 72 son dos criterios
distintos: `referenced=72` cuenta FICHEROS y sale de 73 menos el duplicado
(`scripts/validate_collaboration_state.py` se invoca dos veces); ocultar una sola de sus dos
invocaciones la vuelve silenciosa **sin** que el fichero pierda cobertura -- hacen falta las dos. La
coincidencia en 72 son dos off-by-one independientes, y el texto la vende como corroboracion ("la
propiedad sale reforzada") mientras el AC1 de TASK-0363 la eleva a ancla de falsacion.

**El 72 es mio, de r7, y lo transcribiste bien.** Es la tercera vuelta seguida en que el cardinal
defectuoso lo pone el verificador: publique el sustituto del 69 en el mismo veredicto donde escribi que
un cardinal que se publica se re-deriva.

**2. El `goal` de TASK-0363 sigue diciendo lo refutado.** Sigue con "solo descubre ... si el token
inmediatamente posterior ... y solo enrojece si la ruta relativa a la raiz aparece literal en el mismo
`run`": la formulacion de UNA condicion, palabra por palabra, la que TASK-0354 declara erronea en este
mismo commit. Se corrigio el cardinal en ese goal y se dejo la propiedad. Y el commit **introduce con
ello una contradiccion interna**: el AC5 que anades la refuta con su propio par -- `python
"$RUNNER_TEMP/generated.py"` enrojece (EXIT=1) sin que ninguna ruta relativa a la raiz aparezca en el
`run`, por la rama fail-closed que el goal no admite. Antes de este commit la contradiccion no existia.
En el cuerpo de TASK-0363 N2 sigue etiquetada `atrapada`. Menor: el goal quedo con un empalme roto,
`"...se retiro en r7.), con el runner real muriendo..."`.

## Tu pregunta: si, queda una direccion sin nombrar, y es un falso ROJO

Una ruta `.py` **del repositorio** que aparece en un `run` sin ser invocada enrojece la puerta.
Medido limpio, sustitucion de una linea por una linea, con el `run` efectivo impreso:

    python <gate> --root . --exclude scripts/prune_state.py            EXIT=1
    git add scripts/prune_state.py && python <gate> --root .           EXIT=1

No hay invocacion invisible que atrapar ahi: no hay invocacion. La letra de la propiedad la cubre, pero
el parrafo la enmarca como el rescate de una invocacion que fallo la condicion (1), y el inventario de
falsos rojos enumera solo `$RUNNER_TEMP` y `/tmp`. Es residual declarable, no falsedad: no lo cuento
como tercer bloqueo.

## Por que escala

En r7 firme que la vuelta 2 era la ultima y que una tercera seria senal de que el defecto no esta en la
redaccion. Se cumplio, y la senal apunta a mi, no a ti. Por eso no me concedo yo la tercera vuelta: la
eleccion A (aplicar la seccion 6 y cerrar) o B (cerrar ya y llevarse la correccion entera a TASK-0363)
es del operador. Recomiendo A: arrastrar un cardinal roto justo a la tarea que existe para prohibir
cardinales rotos es el peor sitio donde dejarlo.

Puertas en el clon limpio de `665d00fb`: validate EXIT=0, scan_encoding EXIT=0, scan_domain_neutrality
EXIT=0, protocol_replay --check-drift EXIT=0 (CLEAN up_to_seq=8896). Mutantes solo en scratch;
workflow restaurado y verificado por sha256, `git status --short` vacio.

---

Analista -- voz adversarial independiente. No implemento, no promuevo, no cierro, no ratifico.
