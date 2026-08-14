---
message_id: MSG-20260814-Operador-to-Arquitecto-GATE-COLABORACION-claim-producto
task_id: none
type: DECISION
from: Operador
to: Arquitecto
status: archived
requires_response: true
response_owner: Arquitecto
one_line_summary: "GO a la RAIZ del hallazgo del gate de colaboracion (4to de su familia): implementa los CUATRO puntos 6.1-6.4 del reporte NOVA, con el Punto 1 (claim obligatorio para commitear producto) como PRIORIDAD y viviendo en AMBOS ganchos: scripts/check_commit_trailers.py Y .githooks/pre-commit. El Punto 1 se prioriza y publica ya porque es desacoplable de la memoria hibrida (solo-lectura, esquema congelado); los Puntos 2 y 4 se coordinan con F2/F3. Criterio innegociable 2f: cada control entrega prueba de que RECHAZA, no de que pasa. Entregable: cambio de nucleo + nota de version adoptable por upgrade_instance.py; la instancia verifica el rechazo en clon limpio antes de activarlo."
requested_action: "Implementa en el nucleo del hub los 4 puntos del reporte (6.1-6.4), en este orden de prioridad. PUNTO 1 (bloqueante, primero): si el commit lleva Task-Id: TASK-XXXX, exigir claim ACTIVO del actor que commitea, leyendo TASK_INDEX.json y CLAIMS.json (ya se leen en ese punto). Exigir el Punto 1 en LOS DOS ganchos: (a) .githooks/pre-commit (rechazo local fail-closed, feedback inmediato) y (b) scripts/check_commit_trailers.py (gate autoritativo servidor/CI, corre aunque el hook se salte con --no-verify o falte en el clon). Cada gancho entrega su propia prueba de rechazo. Ambos nacen con la derivacion de prefijo de instancia de eb440d6 (cadena vacia cuando la instancia ES el repo) o repiten el defecto 1. PUNTOS 2,3,4 despues: 2 = liveness de maker/checker como PASO 0 del cold-start; 3 = plantilla del prompt declara el maker de cada pendiente (excepcion escrita con checker si el maker es el propio Arquitecto); 4 = el estado distingue tarea-pendiente de capacidad-caida. Entregable: cambio de nucleo + nota de version que las instancias adopten por upgrade_instance.py. Reporta plan y cierre en canonico."
question: none
context_refs:
  - scripts/check_commit_trailers.py
  - .githooks/pre-commit
  - scripts/validate_collaboration_state.py
  - scripts/upgrade_instance.py
  - D:/Agentes/NOVA-Suite/NOVA/Aegis/Area_comun/artifacts/REPORTE-HUB-GATE-COLABORACION-20260814.md
deadline_or_blocking_level: high
---

# DECISION - arregla la RAIZ: claim obligatorio para commitear PRODUCTO (Punto 1 primero, en ambos ganchos)

Arquitecto (mantenedor): recibido el reporte de campo de la instancia NOVA. Decision tomada.
Implementa la raiz. La instancia NO parchea el nucleo por su cuenta; adopta cuando publiques.
El reporte completo con la evidencia esta en
`D:/Agentes/NOVA-Suite/NOVA/Aegis/Area_comun/artifacts/REPORTE-HUB-GATE-COLABORACION-20260814.md`;
abajo va lo esencial para que actues sin depender de la instancia.

## Por que se hace esta solicitud (contexto)

Diagnostico en una linea: **el gate valida la etiqueta, no el proceso que la etiqueta nombra.**

Que paso, comprobado: dos commits de producto (`99a0802` y `10c0d26`, ~1.200 lineas) entraron
a `main` bajo `TASK-9411` con **0 claims activos, 0 eventos de ledger, la tarea sin moverse de
`in_progress`, sin review de nadie, y el mismo actor de maker y checker** -- y pasaron TODOS
los gates en verde, con `Task-Id` correcto.

Por que ningun control lo detuvo (por inspeccion, no suposicion):
- `.githooks/pre-commit`: cero menciones a `claim`, `maker` u `owner`.
- `scripts/check_commit_trailers.py`: cero referencias a `claim`; comprueba que el `Task-Id`
  EXISTE, no quien puede trabajar esa tarea.
- `scripts/validate_collaboration_state.py`: valida claims contra si mismos, nunca contra un
  commit de codigo.

Es decir: el claim y la separacion maker/checker se exigen para escribir el ESTADO gobernado y
**no** para escribir el PRODUCTO. El codigo queda fuera del perimetro de control, que es donde
viven el valor y el riesgo. **Es el CUARTO de la misma familia** (los tres previos ya corregidos
en la instancia: `eb440d6`, `7cf3952`). Los tres eran gates rotos; este es un gate que no existe.
Patron comun: un control que aparenta vigilar sin vigilar. Por eso se arregla en la RAIZ.

## Que implementar (los 4 puntos, en prioridad)

Criterio innegociable heredado de la leccion 2f: **un gate que nunca ha dicho que no, no esta
demostrado.** Para cada control, entrega la prueba de que RECHAZA, no de que pasa.

### PUNTO 1 -- PRIORIDAD, primero: claim obligatorio para commitear producto (6.1)

Si el mensaje lleva `Task-Id: TASK-XXXX`, esa tarea debe tener claim ACTIVO del actor que
commitea. `TASK_INDEX.json` y `CLAIMS.json` ya se leen en ese punto. Pruebas de rechazo:
- **RECHAZA** commit con `Task-Id` sin claim (habria frenado `99a0802` y `10c0d26`).
- **RECHAZA** `Task-Id` con claim de OTRO actor.
- **ACEPTA** con claim propio activo.
- **NO exige** nada con `Task-Id: none` + `Ops-Reason` (coordinacion, higiene).

**Decision de diseno del operador: el Punto 1 vive en LOS DOS ganchos, no en uno.**
- `.githooks/pre-commit`: rechazo local fail-closed en el instante del commit; para el commit
  malo antes de que exista y da feedback inmediato.
- `scripts/check_commit_trailers.py`: el gate autoritativo servidor/CI; corre aunque el hook
  local se salte (`--no-verify`) o no este instalado en el clon.

Un gate solo en el hook es advertencia (bypass trivial); solo en el trailer-check rechaza tarde.
En ambos = el requisito de claim es a la vez inmediato e imposible de saltar. **Cada gancho
entrega su propia prueba de rechazo** (2f por partida doble): pre-commit dice NO y trailer-check
dice NO, cada uno con los cuatro casos de arriba.

**Trampa conocida al portar (obligatoria en ambos):** en modelo 2.A git devuelve rutas como
`Aegis/...` y el nucleo las comparaba contra `Area_comun/` -> gates ciegos (defecto 1). Todo
gate nuevo NACE con la derivacion de prefijo de instancia de `eb440d6` (cadena vacia cuando la
instancia ES el repo -- caso del hub, sin cambio de comportamiento) o repite el defecto.

### PUNTO 2 -- liveness de maker y checker como PASO 0 del cold-start, no watchdog (6.2)

Un watchdog notifica; esta sesion demuestra que la notificacion se ignora sin consecuencia. Sin
checker vivo, la sesion puede disenar, investigar, preparar y pedir; no entregar producto bajo
una tarea. Prueba: **RECHAZA** intento de commit de producto sin checker vivo, nombrando causa y
salida.

### PUNTO 3 -- el maker de cada pendiente, nombrado en el punto de entrada (6.3)

La plantilla del prompt de arranque declara, por pendiente, QUIEN lo construye. Si el maker es el
propio Arquitecto, excepcion escrita con checker designado. Prueba: **revision de plantilla** que
detecta el prompt que declara un maker en el rol y ordena construir a otro en el trabajo.

### PUNTO 4 -- la caida del pipeline no es un pendiente (6.4)

El estado distingue "tarea pendiente" de "capacidad caida". Un maker o checker que no arrancan
restringen la sesion; no ocupan una linea junto a "archivar mensajes".

## Secuencia: por que el Punto 1 va YA y 2/4 se coordinan con la memoria hibrida

Verificado con el estado de la memoria hibrida de la instancia: es camino de **solo lectura**
sobre el canon, esquema INTACTO (`CLAIMS.json`/`TASK_INDEX.json`/`PROJECT_STATE.json` sin cambio;
invariantes I1/I2/I5 ya falsados; F2/AC2 acreditara en seco que `validate_collaboration_state`
sigue verde antes de que F3 mueva un byte).

- **El Punto 1 se apoya en el esquema ACTUAL**, anterior a la memoria hibrida (el mismo que ya
  usa `validate_collaboration_state.py`). Seria correcto aunque la memoria hibrida no existiera.
- **Dominios disjuntos:** el Punto 1 vigila commits de producto sobre tareas con claim activo
  (`in_progress`); la memoria hibrida enfria tareas `done` (cold-packs/stubs). No tocan el mismo
  estado.
- Por tanto: **Punto 1 (y el 3, que es lint de plantilla ortogonal) se publican ya.** Los Puntos
  2 y 4 se coordinan con el tablero F2/F3 -- no por riesgo de esquema (congelado) sino porque
  insertan logica en la misma secuencia de cold-start y semantica de estado que F2/F3 reescriben.

## Nota obligatoria para la nota de version

El Punto 1 para el incidente reportado (tenia 0 claims), pero por si solo deja medio abierta la
familia maker==checker: un actor puede auto-clamarse y commitear. La separacion en la ENTREGA la
cierra el Punto 2. **Decir esto explicito en la nota de version**, para no publicar justo lo que
el hallazgo denuncia: un control que parece completo sin serlo.

## Limites (del reporte, se mantienen)

- Sin ceremonia adicional en el camino feliz.
- No bloquear trabajo exploratorio ni commits de coordinacion (`Task-Id: none`).
- No impedir que el Arquitecto construya: que hacerlo sea excepcion declarada con checker, no el
  camino por defecto cuando nadie mira.

## Adopcion

Entregable = cambio de nucleo + nota de version adoptable por `upgrade_instance.py`. La instancia
NOVA no parchea por su cuenta: adopta cuando publiques y verifica en clon limpio que cada gate
nuevo RECHAZA su caso antes de declararlo activo.

Reporta el plan y el cierre en canonico. Canal ASCII.

-- Operador
