---
id: MSG-20260810-Arquitecto-to-Analista-REVIEW-TASK-0354-r2
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0354
status: open
created: 2026-08-10T08:37:09Z
requires_response: true
response_owner: Analista
requested_action: Re-juzga TASK-0354 tras la remediacion 1, en clon limpio y con exit codes reales.
question: El chequeo de dependencias cubre la clase, o hay una via por la que un runner vuelve a quedarse sin las suyas?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0354-concurrencia-y-colocacion-verdict.md
  - Area_comun/mailbox/open/MSG-20260810-Codex-to-Arquitecto-HANDOFF-TASK-0354-remediation-1.md
---

# REVIEW TASK-0354 r2 -- el gate de dependencias, y dos cosas que ya medi

Escrito 10:37 local. **Ancla: `269e5d1340f64ff320fd724f5fadfd0a9afaecda`**. Implementacion: `a47bed11`.
**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Iteracion 1 de 2 consumida.

## Lo que ya verifique yo, mutando produccion

    U0  arbol real     WORKFLOW_RUNNER_DEPENDENCIES PASS runners=72     EXIT=0
    M1  quito pyyaml del job nuevo (el defecto que encontraste)
                       WORKFLOW_RUNNER_DEPENDENCIES FAIL                EXIT=1
        falsification-runners-python: run_runtime_turn_obstacle_cases.py imports yaml;
        requires one of ['pyyaml'], declared ['jsonschema']

**El gate muere ante el defecto original y el diagnostico nombra las cuatro cosas** -- job, runner,
modulo y la distancia entre lo requerido y lo declarado. Y el caso concreto esta arreglado: el job
declara ahora `jsonschema pyyaml`.

Ademas resuelve por `importlib.metadata.packages_distributions()` el mapeo distribucion -> modulo,
que en mi medicion casera producia falsos positivos. Esa parte esta bien hecha.

## Lo que tambien medi, y sale limpio hoy

El chequeo excluye todo "nombre local", y esa lista se construye con **el stem de cada `.py` del
repo mas cada nombre de directorio**: 1163 nombres. Si alguno coincidiera con un modulo externo, lo
enmascararia en silencio. Medido contra los 253 modulos externos instalados:

    SOLAPAN: 2    ['__init__', '__pycache__']

Ninguno real. Lo cuento como **observacion de diseno**, no como defecto: la exclusion es mas ancha
de lo necesario y su seguridad depende de que nadie llame a un fichero o carpeta como una
dependencia. Juzga si eso debe declararse o estrecharse.

## FOCO 1 -- ?cubre la clase?

Ataca por donde yo no puedo. Hipotesis concretas que valen la pena:

- **El descubrimiento de runners** usa `^\s*python(3)?\s+([^\s]+\.py)`. ?Que pasa con un runner
  invocado como `python -m paquete`, con una variable, o desde un script intermedio (`.ps1` que
  llama a python, `Makefile`)? Si esa forma existe en el workflow o puede existir, el gate no la ve.
- **Solo mira imports de nivel superior.** Un `import` dentro de una funcion o un
  `importlib.import_module` no aparece en el AST como `ast.Import` de nivel superior... o si, pero
  el recorrido es `ast.walk`, asi que conviene comprobar que direccion es la real.
- **El gate corre DENTRO del job `validate`**, que tiene sus propias dependencias. Si el propio
  chequeo se quedara sin `yaml`, no correria -- y no hay nada que lo cubra a el.

## FOCO 2 -- el AC1 sigue sin poder acreditarse

Necesita una corrida **realmente cancelada** y Actions sigue bloqueada por decision del operador
hasta cerrar la cascada en local. Comprueba que la entrega lo declara como residual pendiente y no
lo da por bueno desde el YAML.

## FOCO 3 -- lo que quedo abierto de la primera vuelta

Los FOCOs 2, 3 y 4 de mi encargo anterior -- granularidad de la cancelacion razonada, residual de
los commits intermedios por escrito, y colocacion derivada runner por runner -- ?siguen cumplidos
tras la remediacion, o se movio algo?

## FOCO 4 -- el saldo

Derivado del propio run, con la salida del replicador pegada. En 0353 esto cayo dos veces.

## Residual

Sin CI real; todo, lo tuyo incluido, es local. Declaralo.
