---
message_id: MSG-20260720-Operador-to-Arquitecto-DIRECTIVA-grafo-memoria-clon-y-revision
from: Operador
to: Arquitecto
type: DIRECTIVA
status: open
requires_response: true
response_owner: Arquitecto
requested_action: "Rutear al Analista la REVISION ADVERSARIAL del diseno de medicion del Asesor (personal/asesor/DISENO-medicion-grafo-memoria-hibrida-v0.1.md), incluyendo el estudio del repositorio externo github.com/DeusData/codebase-memory-mcp como insumo. La revision puede adelantarse si el Analista queda libre antes del cierre de la tanda 0103; la EJECUCION del experimento NO arranca hasta ese cierre. Confirmar ruteo y calendario por mailbox."
question: "Puedes rutear la revision adversarial del diseno al Analista, y adelantarla si queda libre antes del cierre de 0103?"
created_at: 2026-07-20
context_refs:
  - personal/asesor/DISENO-medicion-grafo-memoria-hibrida-v0.1.md
  - personal/asesor/DRAFT-DECISION-0104-camino-de-subida-instancia-a-master.md
one_line_summary: "NUEVA LINEA (preparada, NO arrancada): medir si indexar la memoria hibrida con un grafo de aristas tipadas mejora la recuperacion, como condicion previa a firmar su promocion al master. Clon creado en D:/Aegis_Scratch/Nova-Payroll/memhib-graph-probe. Diseno del Asesor listo y PENDIENTE DE REVISION ADVERSARIAL del Analista. Insumo externo a estudiar: github.com/DeusData/codebase-memory-mcp (se toma la IDEA del grafo, no sus claims). La ejecucion NO arranca hasta cerrar la tanda 0103."
---

# DIRECTIVA - grafo sobre la memoria hibrida: clon creado, diseno a revision

Buen trabajo esta noche con la tanda del harness. Esto NO la interrumpe.

## Por que esta linea existe

No voy a firmar la promocion de la memoria hibrida al master sin verificar antes si
indexarla con grafos la mejora. La DRAFT-DECISION-0104 (camino de subida) dice que el
checklist hace ELEGIBLE y que la firma es mia; esta medicion es lo que condiciona esa
firma.

## Lo que ya esta hecho

- **Clon creado**: `D:/Aegis_Scratch/Nova-Payroll/memhib-graph-probe` (convencion de
  DECISION-0098). 279 commits, la memoria hibrida completa, **0 secretos** (protocol-secrets
  esta gitignored y no se rastrea).
- **Diseno de medicion redactado** por el Asesor:
  `personal/asesor/DISENO-medicion-grafo-memoria-hibrida-v0.1.md`.

## Lo que pido

### 1. Revision adversarial del diseno (al Analista, proveedor diverso)

El diseno del Asesor **no se ejecuta sin pasar revision adversarial**. Que el checker lo
ataque como ataca el codigo. Puntos donde quiero que apriete especialmente:

- **?los umbrales pre-declarados son honestos**, o estan puestos para que el brazo B gane?
- **?el corpus de consultas basta**, o esta sobreajustado a las consultas de B-bis que ya
  sabemos que fallan? (el diseno anade Q2 cross-agente y Q3 distractoras justo por eso).
- **?los tres costes de R5 estan bien definidos** y no dejan fuera ningun overhead?
- **?el firewall de PII cubre el caso del grafo**, que indexa contenido que ya paso otros
  controles?
- **?que confusor falta?** Los conocidos estan en la seccion 10; quiero los que no estan.

El Analista fija ademas el tamano y la seleccion exacta del corpus, y sella el set de
verificacion EX-ANTE (leccion de A-bis).

### 2. Estudio del repositorio externo

`https://github.com/DeusData/codebase-memory-mcp`

**De ahi tomaremos lo que necesitemos para mejorar la memoria hibrida.** Que lo revisen
Arquitecto y Analista con estas advertencias, que son parte del encargo:

- Ataca un problema **DISTINTO**: indexa estructura de codigo, que es **re-derivable** (si
  el indice miente, abres el fichero). Nuestra memoria guarda contexto **no re-derivable**.
  Por eso ellos pueden no atestar el contenido y nosotros no podemos.
- Su "atestacion" (SLSA-3, sigstore, VirusTotal) cubre **el binario**, no las respuestas.
- Sus cifras (120x menos tokens, indexado en minutos) son **claims de README sin verificar
  por nosotros**. No entran como supuesto de nada.
- Licencia MIT declarada: verificar compatibilidad antes de tomar **codigo**; para tomar
  **ideas** no hace falta, pero el limite hay que tenerlo claro.

Lo que nos interesa es el **modelo de grafo con aristas tipadas** y su modelo de
nodos/relaciones como referencia de diseno.

## Calendario y limites

- **La EJECUCION no arranca hasta que cierre la tanda 0103.** No quiero trabajo a medias.
- **La REVISION del diseno SI puede adelantarse** si el Analista queda libre antes de ese
  cierre. Es trabajo de lectura, no toca el harness.
- **Nada de esto entra en la ventana de medicion del N=6.** Un indice que cambia el coste
  de exploracion durante la medicion de Contabilidad la invalidaria.
- **Gobernanza**: el trabajo se gobierna EN EL CLON (tareas, claims, gate). Las decisiones
  y los reportes hacia mi van por el mailbox del HUB citando el sha del clon -- el mismo
  patron del probe de peones y del de memoria.
- **Declarado privado y NO citable** (decision-support). El firewall anti-HARKing queda
  intacto: esto no restringe el diseno de una eventual Fase B.

## Guardas de siempre

Reservadas N=6 intactas, fondo intocable (2E35F26E / epoch 1.14.0 / N=500), sin encender
supervised_autonomy ni real_invoker.

-- Operador
