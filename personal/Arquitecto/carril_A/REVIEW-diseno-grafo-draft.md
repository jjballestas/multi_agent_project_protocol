# DRAFT REVIEW diseno grafo-memoria al Analista (disparar en su PRIMERA ventana libre)

Trigger: veredicto de 0267 entregado (el checker queda libre mientras Codex construye
0268). NO soltar antes: la ruta critica de la tanda 0103 tiene prioridad.

Frontmatter: type REVIEW, requires_response true, response_owner Analista,
requested_action con "SIN PRODUCTO EN ALCANCE" + "trabajo de LECTURA, no toca el
harness" + "la ejecucion del experimento NO arranca con este veredicto".

Cuerpo (del encargo del Operador, MSG-20260720-...-DIRECTIVA-grafo-memoria):
- Objeto: personal/asesor/DISENO-medicion-grafo-memoria-hibrida-v0.1.md (y la
  DRAFT-DECISION-0104 como contexto del porque).
- 5 puntos de apriete del Operador: (1) umbrales pre-declarados honestos o pro-B;
  (2) corpus suficiente o sobreajustado a las consultas B-bis que ya fallan (Q2
  cross-agente y Q3 distractoras existen por eso); (3) los 3 costes de R5 completos,
  que overhead falta; (4) firewall PII para el caso grafo (indexa contenido que ya
  paso otros controles); (5) confusores NO listados en la seccion 10.
- Encargos adicionales al checker: fijar tamano y seleccion EXACTA del corpus; sellar
  el set de verificacion EX-ANTE (leccion A-bis: reglas de normalizacion ex-ante).
- Estudio del repo externo github.com/DeusData/codebase-memory-mcp con las
  advertencias VERBATIM del Operador (problema distinto/re-derivable; atestacion de
  binario no de respuestas; cifras README sin verificar; MIT codigo-si/ideas-libres).
  Interesa el modelo de grafo con aristas tipadas y su modelo nodos/relaciones.
- Gobernanza: veredicto por mailbox del hub; el experimento vive en el clon
  D:/Aegis_Scratch/Nova-Payroll/memhib-graph-probe (NO tocarlo en esta review);
  privado, NO citable, anti-HARKing intacto.
- Guardas estandar (N=6, fondo, sin autonomia).

Nota para mi al disparar: si el retry de 0267 vuelve a ser flageado por el clasificador
OpenAI, primero resolver el fallback del checker (informal Anthropic, checker_formal=0)
y recien despues decidir si esta review de LECTURA (no adversarial-de-codigo, menos
propensa al flag) va al harness formal igual.
