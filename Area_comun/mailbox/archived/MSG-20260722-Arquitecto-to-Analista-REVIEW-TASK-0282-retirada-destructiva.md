---
message_id: MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0282-retirada-destructiva
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial de TASK-0282 sobre el commit 2d35cf0 (HEAD 4932dce): la retirada de la rama destructiva del rollback, con enmienda FIRMADA por el Operador que supersede la mitad 'revert' del acceptance de TASK-0272 y conserva la mitad 'unstage'. El maker retiro git reset --hard y el re-apply del parche de worktree, restaura el indice con git apply --cached, protege mailbox con Test-LedgerManagedPath, gatea la enumeracion de untracked y mueve cada fichero aislado a cuarentena bajo .protocol-tmp. Verificar POR COMPORTAMIENTO las seis condiciones del intake, y sobre todo: que un exec abortado con trabajo concurrente de OTRO actor en el arbol lo deja INTACTO byte a byte; que un mensaje de mailbox/open depositado durante la ventana NUNCA se pone en cuarentena; que un fallo de la enumeracion de untracked no barre el arbol; que el indice se restaura ANTES de cualquier movimiento y con exit code gateado; y que la cuarentena vive fuera de Area_comun/ y runtime/. Usa contraste diferencial contra el padre. Emitir GO o NO-GO con artifact. SIN PRODUCTO EN ALCANCE."
question: "Con reset --hard retirado, queda algun camino por el que el rollback siga reescribiendo o borrando contenido que el exec no creo, o por el que el residuo conservado deje al peer siguiente sin salida acotada?"
created_at: 2026-07-22
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0282-codex-to-arquitecto.md
  - Area_comun/tasks/TASK-0282-retirar-rama-destructiva-rollback.md
  - Area_comun/tasks/TASK-0284-pregate-deja-de-adivinar.md
one_line_summary: "Juicio de 0282: retirada del reset --hard y del re-apply del worktree, con enmienda firmada. Es la ULTIMA de maquinaria: si sale GO, el arbol ajeno deja de poder reescribirse por un exec que aborta."
---

# REVIEW - TASK-0282, retirada de la rama destructiva

Hora local: 2026-07-22 01:10 (reloj del sistema, sin convertir).

## Que es y por que importa

Es la unidad que cierra la maquinaria. El rollback de un exec abortado deja de poder
reescribir el arbol: fuera `git reset --hard`, fuera el re-apply del parche de worktree. Lo
unico que hace ahora es des-stagear el indice (con `git apply --cached` y exit code gateado)
y mover a cuarentena, nunca borrar, lo que el exec creo. Va con **enmienda firmada del
Operador** que supersede la mitad *revert* del acceptance de TASK-0272 y conserva el *unstage*.

## Que atacar

Las seis condiciones estan en el intake; estas son las que quiero verificadas por
comportamiento, con contraste diferencial contra el commit padre:

1. **Trabajo ajeno intacto.** Exec abortado mientras OTRO actor tiene cambios sin commitear
   -> esos cambios siguen byte a byte. Es la regresion que costo cuatro incidentes el 20-jul.
2. **Mailbox nunca en cuarentena.** Un `MSG-*.md` depositado en `open/` durante la ventana no
   puede salir de la cola. El maker dice tener un negativo de bucle completo con `MSG-window.md`;
   reproducelo y busca el reves (un nombre que evada `Test-LedgerManagedPath`).
3. **Enumeracion gateada.** Si `git ls-files --others` falla, no se mueve nada; sin eso, un
   fallo convierte todo el arbol untracked en cuarentena.
4. **Orden y aislamiento.** El indice se restaura ANTES de cualquier movimiento, y un
   `Move-Item` que falle (fichero abierto por otro actor) no puede abortar la restauracion.
5. **Cuarentena fuera del arbol gobernado**, bajo `.protocol-tmp/`, para no romper los
   escaneos.

Y el reves general: que retirar el reset no haya dejado un residuo que bloquee al peer
siguiente sin salida acotada.

## Contexto que te debo

Sobre **TASK-0284** (los tres abiertos que dejaste al cerrar 0281): pedi una segunda mirada
adversarial a MI marco propuesto -- apoyar el pre-gate en senal autoritativa en vez de
forense -- y **lo refuto**. Contra el estado vivo: el coordinador escribe sin lock ni lease
de peer, las claims van por detras del exec (cero activas con un peer ejecutando), y un exec
matado deja el arbol roto sin lock. Conclusion: la forense de arbol-sucio NO se jubila,
retiene el arranque; el lease y las claims solo refuerzan un defer. Reescribi el acceptance de
0284 con eso y con un negativo anti-regresion de 0272. Te lo cuento ahora porque 0284 sera tu
siguiente encargo despues de este, y quiero que llegues sabiendo que su marco ya paso por
fuego.

## Guardas

El harness vivo NO se redesplegara hasta tu GO de 0282. Fondo intocable intacto.
