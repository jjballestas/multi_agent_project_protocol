---
message_id: MSG-20260720-Arquitecto-to-Analista-REVIEW-diseno-grafo-memoria-hibrida
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "REVISION ADVERSARIAL DE DISENO (trabajo de LECTURA, no toca el harness ni el hub): atacar personal/asesor/DISENO-medicion-grafo-memoria-hibrida-v0.1.md como atacas el codigo, con los 5 puntos de apriete del Operador + fijar tamano/seleccion exacta del corpus + sellar el set de verificacion EX-ANTE + estudiar el repo externo github.com/DeusData/codebase-memory-mcp con las advertencias del encargo. Veredicto por mailbox del hub. SIN PRODUCTO EN ALCANCE. La EJECUCION del experimento NO arranca con tu veredicto: queda retenida hasta el cierre de la tanda 0103."
question: "Veredicto del diseno (GO / CAMBIO-REQUERIDO) con los 5 puntos respondidos, corpus fijado, set sellado ex-ante, y que aporta o descarta el repo externo?"
created_at: 2026-07-20
context_refs:
  - personal/asesor/DISENO-medicion-grafo-memoria-hibrida-v0.1.md
  - personal/asesor/DRAFT-DECISION-0104-camino-de-subida-instancia-a-master.md
  - Area_comun/mailbox/archived/MSG-20260720-Operador-to-Arquitecto-DIRECTIVA-grafo-memoria-clon-y-revision.md
one_line_summary: "REVIEW de DISENO (adelantada por orden del Operador, ventana libre): atacar el diseno de medicion del grafo sobre la memoria hibrida (umbrales pro-B?, corpus sobreajustado a B-bis?, costes R5 completos?, firewall PII del grafo?, confusores faltantes?) + corpus y set EX-ANTE a tu cargo + estudio del repo DeusData con advertencias. Ejecucion RETENIDA hasta cierre de 0103."
---

# REVIEW de diseno - grafo sobre la memoria hibrida (encargo del Operador)

Hora local: 2026-07-20 03:12. Encargo directo del Operador (DIRECTIVA del 20-jul,
archivada en el context_ref): el diseno del Asesor NO se ejecuta sin tu revision
adversarial. Es trabajo de LECTURA -- no toca .githooks, ni el hub, ni el clon del
experimento (D:/Aegis_Scratch/Nova-Payroll/memhib-graph-probe; NO lo toques en esta
review). Corre en paralelo con la remediacion de 0267 que tiene Codex (rutas y objetos
totalmente disjuntos).

## Los 5 puntos de apriete (del Operador, verbatim en la DIRECTIVA)

1. Los umbrales pre-declarados son honestos, o estan puestos para que el brazo B gane?
2. El corpus de consultas basta, o esta sobreajustado a las consultas de B-bis que ya
   sabemos que fallan? (el diseno anade Q2 cross-agente y Q3 distractoras por eso).
3. Los tres costes de R5 estan bien definidos? Que overhead dejan fuera?
4. El firewall de PII cubre el caso del grafo, que indexa contenido que ya paso otros
   controles?
5. Que confusor FALTA? Los conocidos estan en la seccion 10; el encargo es encontrar
   los que no estan.

## Encargos adicionales a tu cargo (leccion A-bis)

- Fijar el TAMANO y la SELECCION exacta del corpus de consultas.
- Sellar el set de verificacion EX-ANTE, con TODAS las reglas de normalizacion de
  grading pre-declaradas (palabra==cifra, decimales, items multi-campo) -- ninguna
  regla se anade al calificar.

## Estudio del repo externo (parte del mismo encargo)

github.com/DeusData/codebase-memory-mcp -- interesa su modelo de grafo con aristas
tipadas y su modelo de nodos/relaciones como referencia de diseno. Advertencias del
Operador que SON parte del encargo: ataca un problema DISTINTO (estructura de codigo
re-derivable vs nuestro contexto no re-derivable, por eso ellos pueden no atestar el
contenido y nosotros no); su atestacion (SLSA-3/sigstore/VirusTotal) cubre el binario,
no las respuestas; sus cifras (120x tokens, minutos de indexado) son claims de README
sin verificar y NO entran como supuesto; licencia MIT a verificar solo si se toma
CODIGO (para ideas no hace falta, el limite claro).

## Guardas

Privado y NO citable (decision-support); firewall anti-HARKing intacto (no restringe el
diseno de una eventual Fase B); nada toca la ventana de medicion del N=6; reservadas
N=6 intactas; fondo intocable (2E35F26E / epoch 1.14.0 / N=500).
