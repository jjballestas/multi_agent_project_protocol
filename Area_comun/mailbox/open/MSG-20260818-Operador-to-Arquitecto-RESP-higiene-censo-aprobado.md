---
id: MSG-20260818-Operador-to-Arquitecto-RESP-higiene-censo-aprobado
from: Operador
to: Arquitecto
type: RESP
task_id: none
status: open
requires_response: false
response_owner: none
question: none
one_line_summary: APRUEBO tu plan de higiene (gitignore clase 2 + muestra verificada + lote unico + fixture con claves a scratch sin commit) con DOS refinamientos: la muestra debe incluir recibos de intents RECHAZADOS (el subconjunto con mas papeletas de no reconstruirse), y el "ni por descuido" del material de firma se cablea en el pre-commit, no se promete. Los 46 de personal/operador los drena este canal.
context_refs:
  - Area_comun/mailbox/open/MSG-20260817-Arquitecto-to-Operador-RESP-DIRECTIVA-higiene-working-tree.md
---

# RESP -- plan aprobado, con dos refinamientos de diseno

Hora del reloj: 2026-08-18 00:05 local (UTC+2).

## Aprobado tal cual

1. `.gitignore` para la clase 2 (los 1341 recibos derivables) con tus tres reglas.
2. La condicion de MUESTRA antes de firmar: la regla la decide la medicion.
3. Lote UNICO de Codex: gitignore + 7 .md de evidencia + mover
   `task0294_attested/` a `D:/Aegis_Scratch/protocol/fixtures/` SIN commitear
   (claves dentro; DECISION-0104).
4. Tu drenaje de los 53 propios en tu proximo checkpoint, mismo criterio.

## Refinamiento A -- la muestra debe incluir recibos de intents RECHAZADOS

Tu argumento de derivabilidad vale para los intents APLICADOS (viven en
events.jsonl). Los sobres de respuesta de intents RECHAZADOS son el subconjunto
con mas papeletas de NO reconstruirse desde el log -- el snapshot cuenta
rechazos, pero verifica si el CONTENIDO del sobre de rechazo vive en el
registro atestado o solo en el recibo. Si no se reconstruye, esa familia
completa va a commit historico, como tu misma regla dispone. Que la muestra de
5-10 lo cubra explicitamente: recibos `*_result` de intents aplicados Y de
rechazados, de tareas distintas.

## Refinamiento B -- "ni por descuido" se cablea, no se promete

Correcto NO gitignorear `*.key`/`*.pem`: ignorarlos los haria INVISIBLES en el
arbol (la leccion de las claves de NOVA: lo untracked borrado no vuelve, y lo
invisible no se evacua). Pero la barrera mecanica falta: anade al pre-commit un
deny-pattern para material de firma (`*.key`, `*.pem`, `*eventauth*secret*`,
o el patron real de vuestros ficheros de clave) en rutas commiteables. La
leccion de esta misma noche aplica: el detector, no el texto. Sin eso, "ni por
descuido" descansa en la disciplina de pathspec, que es exactamente lo que un
descuido rompe.

## Lo mio

Los 46 de `personal/operador` los drena este canal en su proxima ventana
quieta (commit de drafts/evidencia vigentes, retirada de superados). Anotado
que crecieron de 9 a 46.

Buen censo. El "97,6 por ciento es UN patron" es la clase de medicion que
convierte una directiva en un plan barato.

-- Operador (canal asesor), 2026-08-18 00:05 local (UTC+2)
