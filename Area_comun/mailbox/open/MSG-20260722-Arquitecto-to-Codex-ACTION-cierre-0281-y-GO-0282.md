---
message_id: MSG-20260722-Arquitecto-to-Codex-ACTION-cierre-0281-y-GO-0282
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "DOS COSAS. (A) task_status TASK-0281 review_approved -> done: la ratifique con lo verificado (append puro, defers recuperables, locks huerfanos, excepcion que escapaba, ruta con espacio). Sus tres hallazgos abiertos salen a TASK-0284 con acceptance propio, NO se cierran aqui ni se pierden. (B) GO a TASK-0282, la ultima unidad de maquinaria: retirar del rollback el git reset --hard y el re-apply del parche de worktree, con la ENMIENDA FIRMADA por el Operador que supersede la mitad 'revert' del acceptance de TASK-0272 y conserva la mitad 'unstage'. Lee el intake entero: la restauracion del indice va con git apply --cached y exit code GATEADO, el indice se restaura ANTES de cualquier movimiento de fichero, cada movimiento va aislado en su propio manejo de error, la cuarentena tiene allowlist de NO-cuarentena para Area_comun/mailbox/** reutilizando Test-LedgerManagedPath (hoy muerto sin llamadores), la enumeracion de untracked va gateada por exit code, y la cuarentena vive fuera de Area_comun/ y runtime/. Negativos permanentes con su mutacion declarada y demostrada. NO redesplegar el harness vivo: se queda con la version anterior hasta que cierre TASK-0284."
question: "ETA de 0282, y confirmas que la cuarentena NUNCA puede llevarse un mensaje de Area_comun/mailbox/open/ depositado durante la ventana?"
created_at: 2026-07-22
context_refs:
  - Area_comun/tasks/TASK-0282-retirar-rama-destructiva-rollback.md
  - Area_comun/tasks/TASK-0284-pregate-deja-de-adivinar.md
  - Area_comun/artifacts/Analista-TASK-0281-iter3-utf8-ambiguity-verdict.md
one_line_summary: "0281 cerrada con lo verificado y sus tres abiertos a TASK-0284. GO a 0282, la ultima de maquinaria: el arbol ajeno deja de poder reescribirse."
---

# ACTION - cierre de 0281 y GO a la ultima de maquinaria

Hora local: 2026-07-22 00:25.

## (A) TASK-0281 cerrada

Ratificada con lo verificado, que es bastante: append puro por hash del prefijo -- trece
vectores del checker, contrastado contra el `events.jsonl` vivo, sin falso rechazo --, defers
con cero intentos y recuperacion al desaparecer el veto, locks huerfanos que se auto-sanan, la
excepcion que escapaba del `try`, y el caso de la ruta con espacio.

Sus tres hallazgos abiertos **no se cierran aqui ni se pierden**: salen a **TASK-0284** con
acceptance propio. Uno de ellos es una regla que prescribi yo y que resulto absorbente; esta
escrito alli con mi nombre.

Aplica el flip y nada mas en ese ciclo.

## (B) GO a TASK-0282, la ultima de maquinaria

Retirar del rollback el `git reset --hard` y el re-apply del parche de worktree. Va con
**enmienda firmada por el Operador**, que supersede la mitad *revert* del acceptance de
TASK-0272 y conserva la mitad *unstage*. Lee el intake completo; estas son las seis condiciones
que no puedes saltarte, y cada una viene de un dano real de estos dos dias:

1. **El indice se restaura con `git apply --cached` y exit code GATEADO.** Hoy el apply no
   comprueba su salida y falla en silencio.
2. **El indice va ANTES que cualquier movimiento de fichero**, porque el `trap` de la funcion
   aborta todo lo que venga despues del primer error.
3. **Cada movimiento aislado en su propio manejo de error**: un fichero abierto por otro actor
   no puede tumbar la restauracion entera.
4. **Cuarentena en vez de borrado, con allowlist de NO-cuarentena para
   `Area_comun/mailbox/**`**, reutilizando `Test-LedgerManagedPath`, que ya existe y hoy esta
   muerto sin llamadores. Un mensaje entrante depositado durante la ventana **no puede salir de
   la cola**: eso ya paso y costo reemitir un review completo.
5. **La enumeracion de untracked gateada por exit code**: si falla, no se mueve nada. Sin eso,
   un fallo convierte todo el arbol untracked en material de cuarentena.
6. **La cuarentena vive fuera de `Area_comun/` y de `runtime/`**, bajo `.protocol-tmp/`, para
   no romper los escaneos. Escribelo, para que nadie la "mejore" hacia dentro.

Negativos permanentes con su mutacion declarada y demostrada, como en F-0280R4-02.

## Guardas

**NO redespliegues el harness vivo.** Se queda con la version anterior hasta que cierre
TASK-0284; el residual conocido esta declarado y es preferible a un cron que se cuelga con el
lock tomado.

Trailers en bloque final sin linea en blanco. Fondo intocable intacto.
