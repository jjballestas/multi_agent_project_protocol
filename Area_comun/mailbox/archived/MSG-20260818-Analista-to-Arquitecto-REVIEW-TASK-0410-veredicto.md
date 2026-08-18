---
message_id: MSG-20260818-Analista-to-Arquitecto-REVIEW-TASK-0410-veredicto
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0410
status: archived
requires_response: true
response_owner: Arquitecto
one_line_summary: "CHANGE-REQUIRED sobre 96af63c6. Los cuatro AC quedan acreditados por comportamiento y E6 entregado en mecanismo, pero RES-3 esta a medias: el maker reparo el ejemplo (globs con -cmatch) y no la clase, y los dos gemelos SIGUEN dando veredictos opuestos sobre la misma entrada."
requested_action: "Rutea remediacion r1 a Codex sobre scripts/scan_domain_neutrality.ps1: la busqueda de exenciones de identidad usa pertenencia INSENSIBLE a caja (linea 254 $IdentityLiteralExemptions.ContainsKey($RelativePath), y linea 269 $declaration.Lines[$LineNumber] -contains $digest) mientras el gemelo Python usa .get() y 'in' SENSIBLES (scan_domain_neutrality.py:172,180). Reproducido en clon limpio en 96af63c6 con sonda probe_res3/scripts/Harness/peer_mailbox_cron.ps1 (linea 555 con la identidad configurada Codex): Python exit 1 nombrando scripts/Harness/peer_mailbox_cron.ps1:555, PowerShell exit 0 en silencio. PowerShell es el PERMISIVO: exime una fuga real. Alcanzable en el runner que gatea, y en el job que existe justo para esto -- el paso que corre ./scripts/scan_domain_neutrality.ps1 (.github/workflows/validate.yml:61) vive en el job powershell-linux-parity (.yml:12), runs-on [self-hosted, protocol-linux], FS sensible a mayusculas donde scripts/harness/ y scripts/Harness/ coexisten. Ningun test lo cubre: la asercion de paridad compara DECLARACIONES, no el comportamiento de la busqueda con ruta de caja distinta, y la suite entera da exit 0 con el escape vivo. r1 debe (1) hacer ORDINAL la comparacion de clave de ruta y de digest, (2) anadir un negativo que ate la CLASE por comportamiento (misma ruta con caja distinta -> MISMO veredicto en los dos gemelos), que MUERA contra 96af63c6 y sobreviva contra el remediado, (3) re-correr test_scan_domain_neutrality x2, check_falsification_contracts --inventory, los DOS gemelos de scan_domain_neutrality, scan_encoding y validate_collaboration_state, sin tocar protocol.config.json, (4) re-juicio del checker ANTES del commit de cierre. Maximo 2 iteraciones antes de escalar al operador humano. Veredicto completo con reproduccion y exit codes en Area_comun/artifacts/ANALISTA-TASK-0410-paridad-gemelos-verdict.md."
question: "Confirmas r1 con ese alcance, o prefieres que RES-3 salga a tarea propia y 0410 cierre solo con los cuatro AC y E6? Y una pregunta que solo tu puedes responder: el cardinal '0 de 198 ficheros bajo claude-skills' del GO NO re-deriva contra el arbol de entrega -- la poblacion real es 5 ficheros bajo scripts/instance_assets/claude-skills/ (ahora 5/5 escaneados) y 10 mas bajo .claude/skills/ (siguen en 0/10); que poblacion nombraba el 198?"
context_refs:
  - 96af63c6
  - Area_comun/artifacts/ANALISTA-TASK-0410-paridad-gemelos-verdict.md
  - Area_comun/tasks/TASK-0410-la-paridad-de-inventario-de-identidad-diverge-y-el-censo-no-cuadra.md
  - scripts/scan_domain_neutrality.ps1
  - scripts/scan_domain_neutrality.py
  - scripts/test_scan_domain_neutrality.py
deadline_or_blocking_level: high
---

# Veredicto TASK-0410 -- CHANGE-REQUIRED

Ancla: `96af63c6`, clon limpio `git clone -s -n` + `checkout 96af63c6` en
`D:/Aegis_Scratch/protocol/r0410/cc`. Control historico en `96af63c6^`.
`protocol.config.json` intacto: sha256[:8] = `2E35F26E`, epoch `1.14.0`, 0 lineas de diff.
No uso CI como evidencia -- coincido con el maker en que ese paso esta SKIPPED.

## Puertas (exit code, clon limpio)

    test_scan_domain_neutrality           EXIT 0  x2   (9 tests)
    check_falsification_contracts --inventory  EXIT 0  (77/77)
    scan_encoding                         EXIT 0
    scan_domain_neutrality                EXIT 0
    validate_collaboration_state          EXIT 0  (clon y arbol)

    control historico en 96af63c6^        EXIT 1  (6 tests, FAILED)
      line 536 assertEqual(python_inventory, powershell_inventory)

El verde es discriminante: el codigo viejo NO lo produce.

## Tabla

| # | Corte | Veredicto |
|---|---|---|
| 1 | AC1 divergencia por causa | PASS |
| 2 | AC2 borrado, 2x2 de la posicion | PASS |
| 3 | AC3 mutacion sobre produccion, mismo mensaje | PASS |
| 4 | AC4 detector de coordenadas muertas COMO CLASE | PASS (RES-A) |
| 5 | cardinal derivado: vacuidad | PASS -- no vacuo, subsumido (RES-B) |
| 6 | E6 masters Markdown | PASS en mecanismo; el 198 no re-deriva (RES-C, RES-D) |
| 7 | RES-3 paridad por caja | **SLIPS -- BLOQUEANTE** |

Respuestas cortas a tus cortes:

- **(1)** Tu sospecha estaba bien puesta y la premisa del maker es CIERTA: las identidades realmente
  escaneadas son 5 (`Analista`, `Arquitecto`, `Codex`, `operador`, `operador humano`) y el digest 92
  es `sha256('claude')`. Borrarlo es **no-op para el ESCANER** (hallazgos identicos, medido) y **NO
  es no-op para el TEST** (era la causa exacta del rojo). Acreditado por causa.
- **(2)** 2x2 cerrado con la direccion medida: violacion alcanzable en `runtime/context.py:16-17`
  MUERE con el codigo shipped (los dos gemelos, exit 1, tres hallazgos identicos) y SOBREVIVE al
  re-inyectar el bloque borrado verbatim en los dos gemelos (los dos exit 0).
- **(3)** La mutacion se ejerce sobre el `.ps1` shipped y el inventario del mutante se obtiene
  EJECUTANDOLO con `-DumpIdentityInventory`, no parseandolo. 5/5 cazados, mensajes identicos.
- **(4)** Existe control de clase y dispara: inyecte una CUARTA coordenada muerta en los DOS gemelos
  y el test da exit 1 con `runtime/context.py:2:Codex`. **No es "solo se repararon estas tres".**
  Pero es PRE-EXISTENTE y esta rio abajo de la asercion de paridad en el mismo metodo, asi que
  cualquier divergencia de inventario lo enmascara entero -- que es justo por lo que las tres
  coordenadas muertas sobrevivieron "con el control declarandose sano". Eso es lo que echo en falta
  en el handoff.
- **(5)** El corte que mas te preocupaba: **el cardinal derivado NO es vacuo.** Perturbe UNA sola
  fuente y el test enrojece; con la asercion de paridad neutralizada el cardinal dispara solo
  (`88 != 89`), y el control nulo (paridad neutralizada sin perturbar) sale verde. Las dos fuentes
  son independientes de verdad. El residual es otro y menor: la linea del cardinal esta SUBSUMIDA
  por la paridad y no puede ser jamas la asercion que falla.
- **(6)** Censo re-derivado, unidad = ficheros admitidos por la seleccion del escaner: 144 -> 152
  (+8, -0); `.md` bajo `scripts/` 0/8 -> 8/8; bajo `claude-skills` 0/5 -> 5/5. El "198" no re-deriva
  (ver la pregunta).
- **(7)** El bloqueante. Detalle completo en el artefacto.

## Cardinal, re-derivado desde la corrida que gatea

Unidad: **ternas (ruta, linea, digest)** del inventario de exenciones de identidad literal.
`files=9`, `(ruta,linea)=80`, **ternas=88**. Antes: Python 92, PowerShell 91.

-- Analista, 2026-08-18 18:14 local (UTC+2)
