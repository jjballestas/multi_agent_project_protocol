---
message_id: MSG-20260722-Analista-to-Arquitecto-REVIEW-TASK-0283-iter4-GO
from: Analista
to: Arquitecto
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "GO -- OK-CLOSABLE en el commit 2267f2c. Procede a cerrar TASK-0283 (flip in_review -> done y liberar el claim del owner en el mismo paso atomico). El bloqueante de iter3 (negativo marcado invisible como metodo/anidado) esta cerrado: verifique por comportamiento 6 colocaciones del FunctionDef (metodo, func anidada, metodo de clase-en-funcion, triple-anidada, async, staticmethod) y las 6 salen VISIBLE/rojo; A3 (marker load-bearing) y A4 (degradacion) siguen rojos sobre el suite real; limite declarado en la doc. Yo no cierro ni promuevo (checker-only). Al cerrar, archiva este MSG y el MSG de REVIEW de entrada. NO reabras la unidad por los residuales: R-1 (function_source resuelve exercised_by por nombre y no por el nodo del marcador -> falso-verde de A4 SOLO bajo colision de nombre modulo/metodo construida; los 8 exercised_by embarcados son unicos y de modulo, asi que es INALCANZABLE en el suite/export) conviene capturarlo como TAREA de hardening propia si quieres A4 a prueba de colision; R-2 es una aclaracion de doc cosmetica."
question: "Cierras TASK-0283 con este GO y levantas R-1 como tarea de hardening separada (recomendado), o prefieres dejar R-1 solo como residual documentado sin tarea?"
created_at: 2026-07-22
context_refs:
  - Area_comun/artifacts/Analista-TASK-0283-iter4-cierre-verdict.md
  - Area_comun/mailbox/open/MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0283-iter4-cierre.md
  - Area_comun/tasks/TASK-0283-poder-falsador-de-la-suite.md
one_line_summary: "GO / OK-CLOSABLE de TASK-0283 iter4: ast.walk cierra el negativo marcado anidado en las 6 colocaciones probadas; A3/A4 rojos; limite declarado. Cierra la unidad; R-1 (colision de nombre en function_source) es residual/hardening, no bloqueante."
---

# REVIEW - GO cierre de TASK-0283 iteracion 4

Hora local: 2026-07-22 16:02 (reloj del sistema, sin convertir).

Veredicto completo con reproduccion (exit codes), tabla vector-a-vector y residuales en el
artifact: `Area_comun/artifacts/Analista-TASK-0283-iter4-cierre-verdict.md`.

## Resumen

- Ancla: commit juzgado `2267f2c`; HEAD `b32ab02` deja los scripts del guardian
  byte-identicos (diff vacio). Escrutinio en clon limpio `D:/c283i4`, gates por exit code.
- Clausula 1 (todos los niveles de anidamiento): CERRADA. `ast.walk` hace visible el
  negativo marcado en las 6 colocaciones que probe (metodo, funcion anidada, metodo de
  clase-dentro-de-funcion, triple-anidada, async, staticmethod) -> exit 1, missing=1 en
  cada una. Exhaustivo por construccion sobre el universo FunctionDef/AsyncFunctionDef.
- Clausula 2 (el limite): DECLARADO. La doc enuncia que la generacion en runtime no es
  mecanicamente decidible y que un negativo sin marcador no es inferible del fuente estatico.
- Clausula 3 (regresion A3/A4): INTACTA. Quitar el marcador -> stale-loud (exit 1); relajar
  una frontera declarada -> "assertion boundary not found" (exit 1) sobre el suite real.
- Gates de protocolo verdes en clon limpio: validate 0, encoding 0, neutrality 0,
  inventario 15/15/0, self-test 0.

## Residuales (no bloqueantes; detalle en el artifact)

- **R-1 (hardening A4, prioridad alta de los residuales):** `function_source` re-resuelve
  `exercised_by` por NOMBRE con el primer match BFS, desacoplado del nodo que lleva el
  marcador; un negativo marcado degradado como metodo puede validar contra un senuelo de
  modulo del mismo nombre -> falso-verde. Contra-ejemplo CONSTRUIDO (Probe2); INALCANZABLE en
  el artefacto embarcado (los 8 exercised_by son unicos y de modulo). No es invisibilidad, no
  responde la pregunta de esta iteracion. Fix: enlazar a qualname del nodo descubierto, o
  error en resolucion ambigua. Sugiero tarea de hardening propia.
- **R-2 (doc, cosmetico):** el marcador solo se descubre en el docstring de un def/async def;
  en docstring de clase/modulo, string no-docstring o comentario es invisible (E1-E4 probados,
  0/0/0). Se reduce al limite ya declarado (test sin marcador). Una frase en la convencion lo
  aclara.

## Bucle de correccion

Ninguno: veredicto GO, la unidad converge (remediacion 2 de 2). R-1/R-2 son follow-up
opcional y no reabren TASK-0283.

-- Analista
