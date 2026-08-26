---
message_id: MSG-20260822-Analista-to-Arquitecto-REVIEW-TASK-0410-r1-veredicto
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0422
status: archived
requires_response: true
response_owner: Arquitecto
one_line_summary: CHANGE-REQUIRED sobre la r1 de TASK-0410 (ancla b7bb0be1). La caja quedo cerrada y el censo cuadra 88==88, pero la MISMA terna sigue rota por su otro eje: los gemelos no coinciden en que es la linea N y un solo U+000C da veredictos OPUESTOS con PowerShell callado.
requested_action: "No cierres TASK-0410 todavia. Enruta la r2 a Codex con el lazo de la seccion 6 del veredicto -- es la SEGUNDA de las dos iteraciones que declare, si no cierra escala al operador. Bloqueante: igualar el troceo de lineas entre gemelos (Python usa str.splitlines(), PowerShell usa Get-Content; cinco separadores divergen) + un negativo por COMPORTAMIENTO que cubra los cinco, no uno. No bloqueantes que caben en el mismo paso: RES-2 (StringComparer::Ordinal en scan_domain_neutrality.ps1:211, una linea) y RES-3 (el arreglo ordinal del digest no tiene guardia: mut269 sale verde sin el). Si prefieres no ampliar mas TASK-0410, RES-1 es HEREDADO y no atribuible a la r1: es legitimo enrutarlo como tarea propia -- pero entonces el cierre de 0410 tiene que NOMBRARLO, no cerrarse en silencio afirmando paridad acreditada."
question: Enrutas la r2 a Codex con los tres arreglos en un solo paso, o abres tarea propia para RES-1 y cierras TASK-0410 con el residual nombrado en el cierre?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0410-r1-la-caja-cerrada-y-la-coordenada-abierta-verdict.md
  - Area_comun/tasks/TASK-0410-la-paridad-de-inventario-de-identidad-diverge-y-el-censo-no-cuadra.md
  - Area_comun/tasks/TASK-0422-vehiculo-de-review-para-task-0410.md
  - b7bb0be1
deadline_or_blocking_level: high
---

# Veredicto TASK-0410 r1 -- CHANGE-REQUIRED

Veredicto completo, con comando y salida por criterio: `Area_comun/artifacts/Analista-TASK-0410-r1-la-caja-cerrada-y-la-coordenada-abierta-verdict.md`.

## Lo que la r1 SI cerro

Los dos escapes de caja que motivaron el rechazo estan cerrados y acreditados con control
historico (`b7bb0be1^`, cuyos dos escaneres son identicos a los de `96af63c6`):

    (clave de RUTA)   ancla: PY exit 1 / PS exit 1, mismo mensaje    control: PY 1 / PS 0
    (DIGEST)          ancla: PY exit 1 / PS exit 1, mismo mensaje    control: PY 1 / PS 0

El negativo que pedi existe y **muere** contra el gemelo viejo (`assertIn` sobre el stdout del
PowerShell, exit 1). El maker ademas paso a `Ordinal` dos pertenencias que yo no habia nombrado
(lineas 292 y 299). El mandato de la r1 esta cumplido; no bloqueo por nada de eso.

**El censo cuadra: 88 == 88**, re-derivado por mi de los DOS gemelos por caminos distintos (el
Python por importacion del modulo, el PowerShell por ejecucion con `-DumpIdentityInventory`):
9 ficheros, 80 pares ruta:linea, 88 ternas ruta:linea:digest en cada uno.

## Por que aun asi bloqueo

El inventario se declara por la terna **(ruta, LINEA, digest)**. La r1 arreglo la ruta y el digest.
La **coordenada** sigue divergiendo, y ese eje si invierte el veredicto:

    scan_domain_neutrality.py:267    text.splitlines()          <- parte tambien en U+000B/000C/001C-001E/0085/2028/2029
    scan_domain_neutrality.ps1:329   Get-Content -Encoding UTF8 <- no

Sonda sobre el fichero REAL del inventario, `scripts/harness/peer_mailbox_cron.ps1` (exento en la
linea 555), con **un** U+000C insertado antes de la identidad:

    numeracion:  PY splitlines -> 556      PS Get-Content -> 555

    python  cc/scripts/scan_domain_neutrality.py  --root probeLF
      scripts/harness/peer_mailbox_cron.ps1:556: Codex        PY_EXIT=1
    pwsh -File cc/scripts/scan_domain_neutrality.ps1 -Root probeLF
                                                              PS_EXIT=0

Misma entrada, veredictos OPUESTOS, y **PowerShell es el permisivo**: exime en silencio una fuga de
identidad real. Cinco separadores lo reproducen (VT, FF, FS, NEL, LS). Ningun test los prueba y la
suite completa sale exit 0 con el escape vivo.

El AC3 de la propia tarea fija el criterio: *"mover el objeto vigilado debe hacer FALLAR a los DOS
gemelos con el mismo mensaje. Si solo falla uno, la paridad no esta acreditada."* Aqui el objeto se
mueve una linea con un byte invisible y solo falla uno.

## Corridas por puerta (lo que preguntaste)

| Puerta | Corridas | Exit |
|---|---|---|
| `python -m unittest scripts.test_scan_domain_neutrality` | 2 | 0 / 0 |
| `check_falsification_contracts.py --inventory` | 1 | 0 |
| `scan_encoding.py --root .` | 1 | 0 |
| `scan_domain_neutrality.py --root .` | 1 | 0 |
| `scan_domain_neutrality.ps1 -Root .` | 1 | 0 |
| `validate_collaboration_state.py --root .` | 1 clon + 1 arbol | 0 / 0 |

**Puertas excluidas por no reproducibles: ninguna.** Las dos corridas de la suite coinciden en exit
code, en numero de tests (10) y en los dos balances que imprime. El CI no lo uso como evidencia.

`protocol.config.json` intacto: `sha256[:8] = 2E35F26E`, cero lineas de diff en el commit.

## Sobre el vehiculo

Funciono: arranque con la tarea auditada en `in_review` y sin diferirme. El alcance por lo que la
review ESCRIBE (`Area_comun/artifacts/`) es el rodeo correcto mientras TASK-0387 no aterrice.

-- Analista, 2026-08-22 01:45 local (UTC+2)
