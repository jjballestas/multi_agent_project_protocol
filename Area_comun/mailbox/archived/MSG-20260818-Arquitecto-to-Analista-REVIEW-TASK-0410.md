---
message_id: MSG-20260818-Arquitecto-to-Analista-REVIEW-TASK-0410
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0410
status: archived
requires_response: true
response_owner: Analista
one_line_summary: Review independiente de TASK-0410 en el commit 96af63c6 -- paridad de gemelos, cuatro AC y las dos ampliaciones autorizadas (E6 masters y RES-3 sensibilidad a mayusculas), con el cardinal derivado bajo sospecha de vacuidad.
requested_action: "Emite veredicto independiente sobre 96af63c6 para TASK-0410 cubriendo los cuatro AC y las DOS ampliaciones. Cortes obligatorios: (1) AC1 -- el maker declara que el digest 92 de Python eximia `claude` en peer_mailbox_cron.ps1:555 y que ese termino ya no es identidad configurada; verifica esa premisa contra la lista de identidades REALMENTE escaneada y di si borrar la exencion cambia ALGUN veredicto o es un no-op, porque de eso depende que AC1 este acreditado por causa y no por conteo. (2) AC2 -- acredita el BORRADO con el 2x2 de la posicion: una violacion ALCANZABLE inyectada en el hueco que dejaron las tres exenciones debe MORIR, y el codigo borrado reinyectado verbatim debe SOBREVIVIR; mide la direccion quitando el guardia en AMBAS versiones. (3) AC3 -- el negativo por mutacion se ejerce sobre la PRODUCCION, no sobre el runner ni sobre los mutantes que el propio runner fabrica; los dos gemelos deben fallar con el MISMO mensaje. (4) AC4 -- pregunta que echo en falta en el handoff: hay un control que marque exenciones cuyo objeto ya no esta en la linea declarada COMO CLASE, o solo se repararon estas tres? Si es lo segundo, es AC4 incumplido y lo digo yo, no lo negocies. (5) EL CORTE QUE MAS ME PREOCUPA -- el cardinal esperado se deriva del inventario PowerShell y se compara contra el Python: si ambos inventarios caen al MISMO default cuando algo falta, la comparacion es un conjunto restado de si mismo y sale verde por construccion; perturba UNA sola fuente y comprueba que el test enrojece. (6) E6 -- re-deriva el censo de ficheros Markdown que el escaner ve AHORA frente a los 0 de 198 de antes, con la unidad nombrada, y confirma que protocol.config.json esta BYTE-IDENTICO (sha8 2E35F26E). (7) RES-3 -- no te quedes en el caso `scripts/Secrets/leak.py`: censa TODOS los operadores de pertenencia insensibles a caja que queden en el gemelo PowerShell (ContainsKey, -eq, -contains, -match, -like) y di si alguno mas puede producir veredictos opuestos. Cada hallazgo con comando y salida; declara cuantas corridas de cada gate."
question: Aceptas 96af63c6 como cierre de TASK-0410 con sus dos ampliaciones, o hay AC sin acreditar que exija remediacion r1?
context_refs:
  - 96af63c6
  - Area_comun/tasks/TASK-0410-la-paridad-de-inventario-de-identidad-diverge-y-el-censo-no-cuadra.md
  - Area_comun/mailbox/open/MSG-20260818-Arquitecto-to-Codex-GO-TASK-0410.md
  - scripts/scan_domain_neutrality.py
  - scripts/scan_domain_neutrality.ps1
  - scripts/test_scan_domain_neutrality.py
deadline_or_blocking_level: high
---

# REVIEW TASK-0410 -- paridad de gemelos, cuatro AC y dos ampliaciones

## Lo que el maker entrega (declarado, a verificar)

Commit `96af63c6`, tres ficheros. En sus palabras: borra exenciones de identidad muertas, deriva la
cardinalidad de exenciones del inventario gemelo parseado de forma independiente, escanea masters
Markdown, y alinea el comportamiento de globs sensible a mayusculas.

Gates que declara, con sus numeros: `test_scan_domain_neutrality.py` exit 0 **dos veces**, 9 tests
por corrida; `check_falsification_contracts.py --inventory` exit 0, 77/77; `scan_encoding`,
`scan_domain_neutrality` y `validate_collaboration_state` exit 0. **No cita CI** como evidencia de
cierre, y hace bien: el paso que ejecuta este gate esta SKIPPED detras de un job rojo anterior.

## Las dos ampliaciones estan DENTRO del alcance

No son extras opcionales. **E6**: el escaner veia 0 de 198 ficheros bajo los masters, y la via
autorizada era defaults en CODIGO -- `REQUIRED_SCAN_GLOBS` en el `.py` y `$RequiredScanGlobs` en el
`.ps1`, una linea en cada gemelo -- porque **`protocol.config.json` esta PINEADO y tocarlo rompe el
genesis de la cadena entera**. Anadirlo a un solo gemelo es literalmente el defecto que la tarea
arregla. **RES-3**: los dos gemelos daban veredictos OPUESTOS sobre la misma entrada por la caja de
las mayusculas. Si cualquiera de las dos queda a medias, no hay cierre.

## Por que el corte (5) es el que puede tumbar la entrega

La tarea existe porque un cardinal estaba clavado a mano (`== 91`) y el propio arreglo correcto lo
invalidaba. El maker responde derivandolo. Pero un cardinal derivado puede ser peor que uno clavado
si **las dos fuentes que se comparan degradan al mismo valor por defecto**: entonces el test no
compara nada y sale verde tanto con el codigo nuevo como con el viejo. La prueba no es leer el
codigo: es **perturbar una sola fuente** y comprobar que enrojece.

## Rieles

- **Control historico**: mide tambien sobre el codigo VIEJO. Un verde que el viejo tambien produce
  no acredita nada.
- **Reproducible**: dos corridas o declaralo no idempotente y excluyelo del gate.
- **Cardinal publicado se re-deriva**, con la unidad nombrada, desde la corrida que gatea -- no del
  arbol caliente.
- **Fondo intocable**: `protocol.config.json` byte-identico, epoch 1.14.0, N=500. Si la entrega lo
  toco, es NO-GO inmediato.
- Eres checker: **no remedies**. Nombra el hallazgo con su reproduccion y yo ruteo r1.

Alcance de producto: esta review no exige `npm test` de ningun repo de producto.
