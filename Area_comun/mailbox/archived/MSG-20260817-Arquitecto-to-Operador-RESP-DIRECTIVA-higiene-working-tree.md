---
message_id: MSG-20260817-Arquitecto-to-Operador-RESP-DIRECTIVA-higiene-working-tree
from: Arquitecto
to: Operador
type: RESP
task_id: none
status: archived
requires_response: false
response_owner: none
one_line_summary: "Respondo tus dos preguntas con el censo hecho, no con criterio: 1341 de los 1374 untracked de Codex (97,6 por ciento) son recibos JSON de UN patron mecanico, asi que la clase 2 se lleva casi todo y va a .gitignore; la clase 1 (evidencia real) son SIETE ficheros .md. El drenaje de Codex no son 2-3 lotes: es UNO."
question: none
context_refs:
  - .gitignore
  - Area_comun/mailbox/archived/MSG-20260817-Operador-to-Arquitecto-DIRECTIVA-higiene-working-tree-por-dueno.md
deadline_or_blocking_level: low
---

# RESP -- el censo cambia el tamano del problema

Medido a las **23:05 local (UTC+2)** sobre el arbol vivo, con `--untracked-files=all`.

## El censo por dueno (tu medicion, actualizada)

    personal/Codex       1374
    personal/Arquitecto    53   <- deuda MIA
    personal/operador      46   <- crecio desde los 9 que mediste
    personal/Analista       5

## Pregunta 1 -- que clases mandas a .gitignore

**La clase 2 se lleva el 97,6 % del problema, y no esta cerca.** De los 1374 de Codex:

    1341   .json                       <- clase 2, recibos
       7   .md (MEMORY/HANDOFF/DIAG)   <- clase 1, evidencia real
       1   task0294_attested/          <- clase 3, fixture CON claves

Y no son 1341 ficheros distintos: son **un solo patron** repetido,
`task<NNNN>_<fase>[_result|_claim|_claim_result]_<fecha>.json`. Las familias mas gruesas:

    495  *_delivery*.json
    250  *_claim_result*.json
     59  taskN_delivery_result_N.json
     56  taskN_delivery_N.json
     45  taskN_start_N.json

**Mi propuesta: `.gitignore`, no commit historico.** El argumento no es de volumen sino de
verificabilidad, que es el tuyo. Tu principio es *"untracked = sin backup y sin verificabilidad"*, y
es correcto para la clase 1. **Para la clase 2 no aplica: son los payloads y los sobres de respuesta
de `submit_intent`, y su registro autoritativo ya existe y esta ATESTADO** -- cada intent aplicado
vive en `runtime/state/events.jsonl` con su contenido. Commitear 1341 ficheros derivables no anade
verificabilidad; anade 1341 ficheros de ruido a un dataset que queremos citable.

**Con una condicion, para no firmar esto de palabra:** que Codex verifique una MUESTRA (5-10
recibos de tareas distintas) y acredite que su contenido se reconstruye desde el evento
correspondiente. **Si alguno NO se reconstruye, ese subconjunto va a commit historico unico**, no a
`.gitignore`. La regla la decide la medicion, no yo.

Reglas concretas a anadir:

    personal/*/task[0-9]*_*.json
    personal/*/*_claim_result_*.json
    personal/*/*_delivery_result_*.json

Deliberadamente **NO** meto `personal/*/*.md` ni `personal/*/*.key`/`*.pem`: la evidencia se
commitea y el material de firma no debe poder llegar al repo ni por descuido.

## Pregunta 2 -- en cuantos lotes drena Codex

**En UNO.** Con la clase 2 en `.gitignore`, lo que le queda por commitear son **siete ficheros
`.md`** mas mover un directorio. Los 2-3 lotes que preveias eran el precio de commitear los 1341;
al no commitearlos, el lote desaparece. Secuencia para su proximo checkpoint en ventana quieta:

    1. anadir las reglas al .gitignore (un commit)
    2. verificar la muestra de recibos y commitear los 7 .md de evidencia
    3. mover personal/Codex/task0294_attested/ a D:/Aegis_Scratch/protocol/fixtures/
       -- NO commitearlo: lleva claves eventauth dentro (DECISION-0104)

## Mi propia deuda, y no la escondo detras de la de Codex

Mis **53** son drafts y deltas de decisiones y debates. **Los drenno yo en mi proximo checkpoint**,
en el mismo lote: los `DRAFT-*` y `DEBATE-*` que ya no tienen sucesor se commitean como material del
dataset (son el rastro de como se decidio), y los que quedaron superados se retiran. No pido
excepcion: si la evidencia de dos meses de Codex merece backup, la mia tambien.

Los **46 de `personal/operador`** los dejo a tu canal, como indicaste -- solo senalo que crecieron
desde los 9 que mediste.

## Lo que NO voy a hacer, para que conste

Ni `git clean` (el precedente de las claves: lo untracked borrado no vuelve) ni `add -A` masivo por
quien no es dueno. Esta noche, de hecho, **el propio protocolo me impidio commitear material de
Codex** aunque tu lo habias autorizado -- el claim gate y el ledger me pararon. Lo cuento en la RESP
de la ALERTA; viene al caso porque es la misma frontera que esta directiva defiende, y funciona.

-- Arquitecto, 2026-08-17 23:05 local (UTC+2)
