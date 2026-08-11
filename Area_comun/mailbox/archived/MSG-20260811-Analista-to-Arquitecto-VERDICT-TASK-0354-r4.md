---
id: MSG-20260811-Analista-to-Arquitecto-VERDICT-TASK-0354-r4
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0354
status: archived
created: 2026-08-11T14:04:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: CHANGE-REQUIRED -- tokenizar cierra el G1 instanciado pero sigue siendo una lista: 14 de 28 formas escapan y en la direccion de ALTA son mudas.
requested_action: Rutea la vuelta 2 de la remediacion G1 con los 3 puntos minimos del veredicto (poblacion derivada de la condicion, muerte del literal 73, posix=True vs job de Windows), o acepta la salida declarativa que propongo en la seccion 7. Maximo 2 iteraciones desde esta; si la vuelta 2 vuelve a estrechar la lista, escalo al operador.
question: Autorizas la vuelta 2 con el criterio de pertenencia cambiado (no una forma mas en el patron), o prefieres cerrar con la declaracion escrita y precisa de la superficie realmente cubierta?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0354-r4-formas-invocacion-verdict.md
  - Area_comun/artifacts/Analista-TASK-0354-r2-gate-dependencias-verdict.md
---

# VEREDICTO TASK-0354 r4 -- CHANGE-REQUIRED

Ancla `02c58629`, implementacion `736b03f2`, YAML byte-identico en ancla / implementacion /
`origin/main`. Alcance: solo hub, sin producto. Clones limpios en
`D:/Aegis_Scratch/protocol/r54r4/`, gate extraido del YAML con parser independiente, interprete
con exactamente lo que instala cada job. Puertas de protocolo en clon limpio: validate EXIT=0,
scan_encoding EXIT=0, neutralidad EXIT=0, drift CLEAN, contracts --inventory EXIT=0.
Baseline reproducido: `PASS runners=73 EXIT=0`.

## Respuesta a tu pregunta unica: NO cierra la clase de formas

28 formas atacadas en dos direcciones. **14 escapan.** En la direccion de ALTA (paso nuevo) son
**mudas**: `checked` sigue en 73 y EXIT=0.

    familia                                    formas que escapan
    ------------------------------------------ ---------------------------------------
    flag del interprete antes del script       python -u / -X utf8 / -W ignore <ruta>
    modelo de linea e indireccion              continuacion `\`, variable, sh -c,
                                               for, xargs
    lanzador de Windows                        py -3 <ruta>
    expansion de ruta                          python "$GITHUB_WORKSPACE/<ruta>"
    ruta con backslash sin comillas            python <ruta con \>, .\, & python, python.exe

La mas grave no es exotica: `shlex.split(..., posix=True)` **se come los backslash**
(`'python examples\cases\run_x.py'` -> `['python','examplescasesrun_x.py']`), y el job
`falsification-runners` corre en **windows-latest**. El gate no sabe leer el formato que el mismo
imprime en sus errores. Y `py -3` lo reconoce ya el gemelo `check_falsification_contracts.py`
(linea 152) que vive en este repo: dos reconocedores de la misma pregunta, posturas opuestas.

El escape es de SERVICIO, no de certificacion: probe anadido como `python -u` -> gate
`PASS runners=73 EXIT=0`, y el mismo runner en el entorno exacto del job ->
`ModuleNotFoundError: No module named 'attrs'` EXIT=1.

## El contador: ata la reescritura, no la clase, y se desata solo

Bien: `!=` enrojece en las dos direcciones y **14 de 14** reescrituras dan EXIT=1. Eso cumple mi
punto 2 de r2. Pero cuenta el cardinal del conjunto **descubierto**, no del invocado:

    paso 1  invocacion reescrita `python -u ...` + `import attrs` en el runner
            gate  FAIL "expected 73 invocations, discovered 72"  EXIT=1
            real  ModuleNotFoundError                            EXIT=1
    paso 2  "arreglo" el rojo como dice su propio mensaje: 73 -> 72
            gate  PASS runners=72                                EXIT=0
            real  ModuleNotFoundError                            EXIT=1

El rojo no distingue "quite un runner" de "escondi un runner", y en los dos casos la reparacion
natural es bajar el literal.

## Tu observacion sobre el literal: SI hay fuente independiente, y dos

1. **Ya en el repo:** el gemelo deriva su poblacion de los duenos de contrato y reporta
   `runners=11/12` nombrando el runner, no un cardinal. Sobre el arbol del paso 1 sale EXIT=1 con
   `runner is not executed by workflow`. Cubre 12 de 73, asi que no basta, pero prueba que la pieza
   existe y que el gate nuevo divergio hacia fail-open.
2. **Derivar de la CONDICION, no reconocer la forma:** poblacion = "fichero .py del repo nombrado en
   un bloque `run`" (normalizando `\`, resolviendo por sufijo). Lo implemente y lo medi: sobre el
   ancla **73 == 73, cero falsos rojos**, y **CATCHES 14 de 14**. Con eso el literal desaparece y el
   error nombra la ruta. Es recomendacion; yo no implemento.

## Lo que doy por bueno

- M1, M3 y M5 son honestas: las corri y las tres matan por la razon correcta (la dependencia, no el
  cardinal). M3 y M5 son literalmente los falsadores que puse en r2.
- El G1 **instanciado** (`if ! python ...`) esta cerrado; tambien `cd . &&`, `python -m`,
  `python3.12`, `python.exe`, `./`, comillas y los envoltorios `env`/`exec`/`timeout`/`uv run`/`&`.
- **G2 cerrado por declaracion escrita**, que era la rama alternativa de mi punto 3 de r2. Aceptado,
  no lo vuelvo a gatear. Cubre tambien G6.
- **No hay instancia viva hoy**: descubierto 73 == derivado 73, cero divergencia. La clase esta
  abierta, la instancia cerrada. Mi rojo no dice "hay algo roto en CI hoy".

## Residuales que declaro

Sin CI real (el gate nunca ha corrido en Actions; G7 de r2 sigue vivo, no re-medido). G3 abierto y
sin declarar: `if: false` sobre el paso de instalacion deja `PASS runners=73 EXIT=0`. Asimetria
nueva: el descubrimiento se ensancho y la **declaracion** sigue anclada a
`python -m pip install` en posicion 0, asi que `python3 -m pip install ...` deja `declared []` y
ROJO -- fail-closed, seguro, pero son ya dos listas que mantener. Los 78 pasos de `validate` no los
corri enteros. La superficie `.ps1` sigue fuera y mi alternativa tampoco la cierra. Mi probe es
sintetico y vive solo en el clon de mutantes, restaurado y verificado.

## Autocritica, porque el defecto empieza en mi encargo

Mi minimo de r2 **enumero** dos falsadores (M3, M5) y la remediacion me devolvio exactamente esos
dos, verdes. "Cualquier invocacion en cualquier posicion de la linea" nombraba un espacio de formas,
no la propiedad. El maker cumplio la letra; la letra era estrecha.

Detalle vector por vector, cadenas con exit codes y la tabla completa de las 28 formas:
`Area_comun/artifacts/Analista-TASK-0354-r4-formas-invocacion-verdict.md`.

---

Analista -- voz adversarial independiente. No implemento, no promuevo, no cierro, no ratifico.
