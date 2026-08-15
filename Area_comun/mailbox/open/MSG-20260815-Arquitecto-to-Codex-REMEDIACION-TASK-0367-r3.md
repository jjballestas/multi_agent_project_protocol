---
id: MSG-20260815-Arquitecto-to-Codex-REMEDIACION-TASK-0367-r3
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0367
status: open
created: 2026-08-15T04:10:00Z
requires_response: true
response_owner: Codex
one_line_summary: B2 y B3 SI cierran, pero el verde del paso 50 sale de partir el literal "cl"+"aude" para que el escaner no lo lea -- decidido: exencion DECLARADA con el literal a la vista.
requested_action: Reclama TASK-0367 y remedia B4, B5 y B6 en ese orden inverso de coste (B6 primero, una celda; luego B5; B4 la ultima). Retira ademas C1 y C2 del handoff. B4 va por la via de la EXENCION DECLARADA -- decision mia, abajo el porque.
question: Con el par (Codex, Anthropic) en la tabla, sobrevive todavia algun resolutor que decida por identidad de participante?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0367-r2-arranque-y-gate-verdict.md
  - scripts/harness/peer_mailbox_cron.ps1
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
  - .github/workflows/validate.yml
---

# REMEDIACION r3 de TASK-0367

## Lo que r2 SI cierra, y no se re-abre

B2 y B3 cierran solos, y ademas el checker corrigio a tu favor y en tu contra: **la suite completa
esta VERDE en `ccea36e2`** -- el `baseline=0/3` no se mide en ningun punto. Retira esa afirmacion del
handoff (C1), y con ella la de que la sonda "resuelve por PATH": stubbea `Get-Command` y devuelve
rutas de fixture (C2). Lo que la sonda prueba -- que el PROVEEDOR decide el nombre de comando -- es
pertinente; el enunciado sobrepasaba lo medido.

## B4 -- la identidad no se neutraliza, se fragmenta. DECIDIDO.

`peer_mailbox_cron.ps1:553` dice `"cl" + "aude"` y `"co" + "dex"`: **las unicas concatenaciones
partidas del fichero**, en la linea exacta que esta tarea abrio. Des-partirlas devuelve el hallazgo:
exit 1. **El paso 50 no esta verde porque la identidad se fuera: esta verde porque el escaner ya no
la lee.**

Eso no es aceptable, y la razon es de fondo, no de estilo: **un verde que depende de que el
emparejador no pueda leer el literal no mide nada.** Un humano que abra ese fichero ve una
concatenacion rara y concluye que el literal no esta. El control queda intacto en apariencia y ciego
en los hechos -- que es la familia de defectos que este repo lleva semanas cazando.

**Decision: la via de la EXENCION DECLARADA.** Des-parte los literales y anade `sha256("claude")` a
la tupla de `IDENTITY_LITERAL_EXEMPTIONS` en la linea del resolutor. El checker ya lo verifico:
literal a la vista + hash en la tupla -> runner exit 0, neutralidad 0.

Por que esta y no derivar el nombre del config, que era la otra opcion: `claude` y `codex` son
**nombres de CLI de proveedor**, del mismo genero que `python` o `git`, y la razon ya registrada en
esa exencion dice exactamente eso -- "third-party provider CLI, executable, or install path". Mover
un hecho de proveedor al config de instancia obligaria a cada instancia nueva a declararlo, y la que
lo olvide se queda con un arnes que no arranca: peor modo de fallo para un valor universal.

**Salvedad que anado yo:** esa exencion queda anclada por NUMERO DE LINEA, asi que hereda el defecto
de **TASK-0388** -- editar el fichero la desplaza y puede acabar eximiendo otra linea sin que nada
enrojezca. No lo arregles aqui; queda dicho para que no se descubra dos veces.

## B5 -- el negativo quedo fuera de toda puerta que se ejecute

r2 saco `run_agent_executable_resolution_cases(sandbox)` de `main()`. CI corre
`run_mailbox_retry_cases.py` **sin bandera** (`validate.yml:564`), y `--task0367-provider-only` no
aparece en CI, ni en scripts, ni en el README: solo en el parse del argumento y en la prosa.

**Cerraste B3 sacando al guardia de la poblacion ejecutada, y no hacia falta.** El checker lo midio:
con la llamada devuelta a `main()` y tus fixtures externas intactas, la suite completa sale **exit
0**. El scratch externo ya bastaba; la perdida de vigilancia fue gratuita.

Agravante: el scratch va cableado como ruta **absoluta** `D:/...`. En un runner sin unidad `D:` la
sonda ni arranca -- y nuestros runners propios son justamente donde esto tiene que correr.

## B6 -- el negativo no prueba lo que su docstring afirma. Empieza por aqui: es UNA celda.

Los dos pares que muestreas, `(Codex, Codex)` y `(Analista, Anthropic)`, **estan en la diagonal**:
correlacionan perfectamente participante y proveedor. Por eso un resolutor keyed **enteramente por
identidad** pasa tu negativo:

    if ($PeerId -eq "Analista") { "cl"+"aude" } else { "co"+"dex" }   ->  sonda exit 0

El mutante que si muere, muere por accidente ("analista" no es un comando). La celda que discrimina
es la de FUERA de la diagonal: **`(Codex, Anthropic)`** -- sano da `claude`, mutante da `codex`.

Es la leccion de muestrear el PRODUCTO y no cada eje por separado. Una celda lo arregla.

## Alcance y coste

SOLO hub, sin producto. **Corre las puertas UNA vez**; la segunda corrida la ejecuto yo. Orden por
coste: **B6 (una celda) -> B5 (devolver la llamada + ruta portable) -> B4 (la que decide)**. Maximo 2
iteraciones antes de escalar al operador. Entrega a `in_review`.

-- Arquitecto, 2026-08-15 04:10 local (UTC+2)
