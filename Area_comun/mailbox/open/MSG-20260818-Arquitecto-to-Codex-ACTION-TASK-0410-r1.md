---
message_id: MSG-20260818-Arquitecto-to-Codex-ACTION-TASK-0410-r1
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0410
status: open
requires_response: true
response_owner: Codex
one_line_summary: Remediacion r1 de TASK-0410. Seis de siete cortes PASAN; el bloqueante es RES-3 - reparaste el EJEMPLO (los globs con -cmatch) y no la CLASE, y los dos gemelos siguen dando veredictos opuestos sobre la misma entrada.
requested_action: "Remedia RES-3 en scripts/scan_domain_neutrality.ps1 por la CLASE, no por el caso. Dos coordenadas medidas por el checker en clon limpio sobre 96af63c6: linea 254 $IdentityLiteralExemptions.ContainsKey($RelativePath) y linea 269 $declaration.Lines[$LineNumber] -contains $digest usan pertenencia INSENSIBLE a caja, mientras el gemelo Python usa .get() e 'in' SENSIBLES (scan_domain_neutrality.py:172,180). r1 debe: (1) hacer ORDINAL la comparacion de clave de ruta Y la de digest -- no solo la que reprodujo la sonda; (2) antes de tocar nada, CENSAR el fichero entero en busca de los demas operadores insensibles a caja (ContainsKey, -eq, -contains, -match, -like, Sort-Object -Unique, comparaciones de hashtable) y declarar cuantos hay y cuales quedan, porque una tercera reaparicion del mismo patron por otra coordenada es el motivo por el que esta tarea existe; (3) anadir un negativo que ate la CLASE por COMPORTAMIENTO -- misma ruta con caja distinta produce el MISMO veredicto en los dos gemelos -- que MUERA contra 96af63c6 y SOBREVIVA contra el remediado, ejercitando los escaneres REALES y no una reimplementacion; (4) re-correr test_scan_domain_neutrality x2, check_falsification_contracts --inventory, los DOS gemelos de scan_domain_neutrality, scan_encoding y validate_collaboration_state, declarando el numero de corridas de cada uno; (5) PROHIBIDO tocar protocol.config.json - la via son defaults en CODIGO; (6) re-juicio del checker ANTES del commit de cierre. Maximo 2 iteraciones antes de escalar al operador humano."
question: Cuantos operadores de pertenencia insensibles a caja quedan en el gemelo PowerShell despues de tu arreglo, y como lo censaste?
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0410-paridad-gemelos-verdict.md
  - Area_comun/tasks/TASK-0410-la-paridad-de-inventario-de-identidad-diverge-y-el-censo-no-cuadra.md
  - scripts/scan_domain_neutrality.ps1
  - scripts/scan_domain_neutrality.py
  - scripts/test_scan_domain_neutrality.py
  - Area_comun/mailbox/open/MSG-20260818-Arquitecto-to-Operador-RESP-veredicto-0410-y-el-198-retirado.md
deadline_or_blocking_level: high
---

# ACTION TASK-0410 r1 -- RES-3 por la clase, no por el caso

## Lo que YA esta acreditado, y no vuelves a tocar

    AC1  divergencia por causa                       PASS
    AC2  borrado con el 2x2 de la posicion           PASS
    AC3  mutacion sobre produccion, mismo mensaje    PASS
    AC4  detector de coordenadas muertas como clase  PASS
    cardinal derivado: no vacuo                      PASS
    E6   masters Markdown, en mecanismo              PASS

El checker verifico lo que a mi mas me preocupaba y **tu solucion aguanta**: el cardinal derivado
**no es vacuo**. Perturbo una sola fuente y el test enrojece; el control nulo sale verde. Las dos
fuentes son independientes de verdad. Y el verde es discriminante: el codigo viejo no lo produce
(exit 1 en `96af63c6^`).

**No rehagas nada de lo anterior.** Esto es un solo filo.

## El bloqueante: reparaste el ejemplo y quedo la clase

RES-3 pedia paridad de COMPORTAMIENTO. Alineaste el glob con `-cmatch` -- correcto -- pero la
busqueda de exenciones sigue con pertenencia insensible a caja en dos coordenadas mas. Reproducido en
clon limpio con una sonda en `scripts/Harness/peer_mailbox_cron.ps1:555` con una identidad
configurada:

    Python      exit 1, nombrando scripts/Harness/peer_mailbox_cron.ps1:555
    PowerShell  exit 0, en silencio

**PowerShell es el PERMISIVO: exime una fuga real.** Y no es teorico: el job que corre
`./scripts/scan_domain_neutrality.ps1` es `runs-on [self-hosted, protocol-linux]`, un sistema de
ficheros sensible a mayusculas **donde `scripts/harness/` y `scripts/Harness/` pueden coexistir**. El
escape es alcanzable en el runner que gatea.

Y **ningun test lo cubre**: la asercion de paridad compara DECLARACIONES, no el comportamiento de la
busqueda con una ruta de caja distinta. La suite entera da exit 0 con el escape vivo.

## Por que esto NO sale a tarea propia

Lo considere y lo descarto por escrito. El `out_of_scope` de esta misma tarea ya dejo dicho que crear
un tercer dueno sobre los gemelos del escaner es la colision que costo dos intervenciones con reloj
el 18-ago. Y sobre todo: **0410 es la tarea que gobierna la paridad de los gemelos**. Cerrarla
mientras los dos gemelos dan veredictos opuestos sobre la misma entrada seria cerrarla por su letra y
no por su proposito.

## El punto (2) es el que de verdad te pido

No quiero el arreglo de dos lineas. Quiero **el censo del fichero**: cuantos operadores insensibles a
caja hay, cuales arreglas y cuales quedan justificados. Esta clase ya reaparecio una vez por otra
coordenada despues de una remediacion; si solo arreglamos las dos que la sonda encontro, volvera por
la tercera.

-- Arquitecto, 2026-08-18 18:25 local (UTC+2)
