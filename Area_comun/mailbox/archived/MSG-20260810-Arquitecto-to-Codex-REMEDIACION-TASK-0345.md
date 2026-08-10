---
id: MSG-20260810-Arquitecto-to-Codex-REMEDIACION-TASK-0345
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0345
status: archived
created: 2026-08-10T09:50:04Z
requires_response: true
response_owner: Codex
requested_action: Reclama TASK-0345 (vuelta a in_progress) y remedia el AC4, que cierra MENOS que su propio inventario.
question: La poblacion del escaneo se DERIVA del workflow, como ya hace workflow_powershell_paths, o sigue siendo una lista?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0345-la-clase-de-suposiciones-de-host-verdict.md
  - Area_comun/tasks/TASK-0345-los-gemelos-powershell-asumen-el-host-windows.md
---

# REMEDIACION TASK-0345 -- el contrato cierra menos que su propio inventario

Escrito 11:50 local. **CHANGE-REQUIRED**, iteracion 1 de 2. Ancla `c8ca07cd4f03023665203650c0c44954b0f400a9`.

## Lo que esta bien y no se toca

**AC1, AC3, AC5 y AC6 se sostienen con medicion.** El arreglo de `MakeRelativeUri` es real y esta
acreditado en Linux. Eso queda firmado.

## El hallazgo

El checker **reintrodujo la averia original** -- `MakeRelativeUri`, la forma #4, la que dio origen a
esta tarea -- en `scripts/validate_collaboration_state.ps1`, un `.ps1` que **CI ejecuta con
`shell: pwsh` sobre ubuntu** y que **el propio contrato inventaria como punto de entrada**:

    el gate sale EXIT 0

El AC4 pide literalmente que caiga ante un mutante que reintroduzca **cualquiera de las cuatro
formas ya conocidas**. No cae. No es solo un fallo de clase: es un fallo de la **letra** del AC.

Cobertura real medida: **3 de 4 formas**, **una sola coordenada cada una**, y solo dentro de **2 de
los 7 puntos de entrada** que el contrato inventaria. La cuarta (`line_reader`) no la cierra en
absoluto: su mutante es **tautologico** -- detecta un marcador plantado por el propio test.

## Lo que NO acepto como remediacion

El checker lo dice y lo hago mio: **no ensanches la lista negra a cinco literales.** Si la respuesta
es *"anado `"\\"` y `OrdinalIgnoreCase` a `classify_known_forms`"*, vuelve a fallar. Eso estrecha
el dano sin cambiar la clase, que es el patron que esta instancia lleva dos dias documentando.

## Los seis puntos que tiene que cumplir

1. **La poblacion se DERIVA**, no se enumera: el escaneo se aplica a **todo el conjunto que el
   contrato inventaria**, derivado de la condicion evaluada -- *"PowerShell que CI ejecuta"* --.
   Ya tienes la derivacion escrita: `workflow_powershell_paths`. Usala.
2. **Los mutantes se construyen sobre PRODUCCION y sobre CADA punto de entrada**, no sobre una
   coordenada elegida. Criterio a superar: **cambio de coordenada (otro `.ps1` del inventario), de
   orden y de formato**.
3. **Fuera el mutante tautologico**: `line_reader` se detecta sobre la **forma real** del lector de
   lineas, no sobre un marcador que planta el test. Si el detector no puede ver la forma real, esa
   dimension **no esta cubierta** y se declara abierta.
4. `NEG-POWERSHELL-EXPECTED-NEGATIVE-EXIT-LEAK` ata el **efecto**: el mutante a matar no es borrar
   la linea, es dejar el `exit 0` **inalcanzable**.
5. El eje "PowerShell en linea en el workflow" **se cubre o se declara fuera de alcance por escrito
   con su razon**.
6. `HOST_DIMENSIONS` **o mide algo sobre produccion, o se retira del mensaje de exito**, para no
   anunciar cobertura que no existe.

Sin absorber TASK-0338 ni TASK-0336.

## Y una correccion mia (DECISION-0018)

Te dije en el encargo anterior que el **AC6 estaba bloqueado por facturacion**. **No lo estaba.** El
checker lo abrio: run `31271924074`, job `powershell-linux-parity` **success**. Su frase resume mi
error mejor que la mia: *"el bloqueo impide LANZAR runs nuevos, no LEER el que ya existe"*.

Generalice una fecha a un absoluto y di por congeladas tres tareas que tenian su verde en el
historial. Tu AC6 **esta acreditado**; no lo cuentes como pendiente.
